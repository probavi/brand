"""OKLab/OKLCH conversion, WCAG contrast, and contrast-targeted tone finding.

The palette is not a list of hexes somebody liked; it is a small vector of hues
and chromas, plus rules for turning those into tones that clear a floor. This
module is the arithmetic those rules are written in, so `_palette.py` can stay a
statement of intent and `gen_tokens.py` can keep measuring what it emits.
"""
import math


def _s2l(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _l2s(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(min(1.0, max(0.0, v)) * 255):02X}" for v in rgb)


def _lin_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = math.cbrt(l), math.cbrt(m), math.cbrt(s)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _oklab_to_lin(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def hex_to_oklch(h):
    L, a, b = _lin_to_oklab(*(_s2l(c) for c in hex_to_rgb(h)))
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a))
    return L, C, (H + 360) % 360


def _in_gamut(lin):
    return all(-0.0002 <= v <= 1.0002 for v in lin)


def oklch(L, C, H):
    """OKLCH to hex, reducing chroma until the colour fits in sRGB."""
    Lc = min(1.0, max(0.0, L))
    rad = math.radians(H)

    def at(c):
        return _oklab_to_lin(Lc, c * math.cos(rad), c * math.sin(rad))

    lin = at(C)
    if not _in_gamut(lin):
        lo, hi = 0.0, C
        for _ in range(24):
            mid = (lo + hi) / 2
            if _in_gamut(at(mid)):
                lo = mid
            else:
                hi = mid
        lin = at(lo)
    return rgb_to_hex(tuple(_l2s(v) for v in lin))


def shift_l(h, dl):
    L, C, H = hex_to_oklch(h)
    return oklch(L + dl, C, H)


def mix(a, b, t):
    """Perceptual mix in OKLab. t = 0 returns a, t = 1 returns b."""
    A = _lin_to_oklab(*(_s2l(c) for c in hex_to_rgb(a)))
    B = _lin_to_oklab(*(_s2l(c) for c in hex_to_rgb(b)))
    m = tuple(A[i] + (B[i] - A[i]) * t for i in range(3))
    return rgb_to_hex(tuple(_l2s(v) for v in _oklab_to_lin(*m)))


def luminance(h):
    r, g, b = (_s2l(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def hue_distance(a, b):
    a = a if isinstance(a, (int, float)) else hex_to_oklch(a)[2]
    b = b if isinstance(b, (int, float)) else hex_to_oklch(b)[2]
    d = abs(a - b) % 360
    return 360 - d if d > 180 else d


def tone_on(bg, C, H, target, up):
    """The lightness that just clears `target` against `bg`, at hue H, chroma C.

    Returns the *least extreme* tone that passes, so a muted grey stays muted
    instead of collapsing into the text colour. That is the right rule for text
    and the wrong one for a mark — see `hold_or_tone`.
    """
    bg_l = hex_to_oklch(bg)[0]
    lo, hi = (bg_l, 1.0) if up else (0.0, bg_l)
    for _ in range(32):
        mid = (lo + hi) / 2
        ok = contrast(oklch(mid, C, H), bg) >= target
        # Going up, contrast rises with lightness, so a passing midpoint becomes
        # the new ceiling; going down it is the other way round. Either way the
        # bound that keeps passing is the one returned.
        if ok == up:
            hi = mid
        else:
            lo = mid
    out = oklch(hi if up else lo, C, H)
    # Gamut clamping costs a sliver of chroma, and sometimes of contrast with it.
    base = hi if up else lo
    i = 0
    while contrast(out, bg) < target and i < 40:
        out = oklch(min(1.0, max(0.0, base + (1 if up else -1) * 0.004 * (i + 1))), C, H)
        i += 1
    return out


def hold_or_tone(h, bg, target, up):
    """Keep `h` if it already clears `target` on `bg`; otherwise re-tone it.

    This is the rule for anything drawn rather than read: it keeps the colour
    that was chosen, and moves only when that colour would fail its own floor.
    """
    if contrast(h, bg) >= target:
        return h
    _, C, H = hex_to_oklch(h)
    return tone_on(bg, C, H, target, up)
