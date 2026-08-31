#!/usr/bin/env python3
"""The Probavi palette — declared once, consumed by every generator.

This is the source BRAND_GUIDE.md §2 documents. gen_tokens.py emits it as design
tokens; gen_brand.py and gen_outlined.py paint the marks with it.

What is declared here is not a list of hexes. It is the small vector of choices
the palette rests on — two grounds, two accent hues, one neutral hue — plus the
rules that turn those into tones. Every colour below is derived and measured, so
changing a hue and rerunning moves the whole system coherently, and nothing can
be nudged by hand into a value that fails a floor.

The vector was settled by pairwise comparison over the full colour wheel: eight
accent families, six dark grounds, six light grounds, forty-six rounds. What it
replaced was a navy-and-cream pair whose every neutral was a mix of the two,
which is what made the resulting surfaces read as muddy rather than calm.

Key order is meaningful: it fixes the order of tokens.json and of the custom
properties in tokens.css.
"""
from _oklch import (
    contrast, hex_to_oklch, hold_or_tone, hue_distance, luminance, mix, oklch,
    shift_l, tone_on,
)

# --- the vector ------------------------------------------------------------

# Grounds, in OKLCH. The dark one is a near-neutral black rather than a saturated
# navy; the light one is very close to white. Both carry a trace of chroma so the
# neutrals built from them are not dead grey.
DARK_GROUND = {"L": 0.125, "C": 0.00625, "H": 250.0}
LIGHT_GROUND = {"L": 0.994, "C": 0.002, "H": 250.0}

# The accent is the check, and it is the one colour the mark is drawn in.
ACCENT = {"H": 175.0, "C": 0.125}

# The secondary accent. It carries no state of its own in this package: what the
# product does with it is not this repository's decision (see §2).
SECOND = {"H": 300.0, "C": 0.125}

# The neutral scale takes the ground's own hue, which is what keeps a grey from
# looking like a different colour's grey laid over the page.
NEUTRAL = {"light": {"C": 0.020, "H": LIGHT_GROUND["H"]},
           "dark": {"C": 0.024, "H": DARK_GROUND["H"]}}

# The one fixed anchor. A failed restore is red; every other hue works around it,
# and gen_tokens.py measures that it does.
FAULT = {"light": "#9F0E1A", "dark": "#EE7781"}

# Plain white, for the reversed marks that sit on photography or a third party's
# dark background, where one flat colour is all the surface allows. Deliberately
# outside the palette: white is a printing instruction, not a brand colour, and
# must never reach tokens.json.
WHITE = "#FFFFFF"

# --- the floors ------------------------------------------------------------

# WCAG 2.1's numbers where WCAG has one: 4.5:1 for text (1.4.3), 3:1 for non-text
# that carries structure (1.4.11). `fg` is held to AAA (1.4.6) because body text
# is the one thing every page is made of; `fg_target` is what generation aims at
# — the contrast the previous palette's headings measured — and on a ground this
# dark it is not always reachable. Aiming high and gating at the standard is what
# keeps an unreachable number from failing a palette that is fine.
FLOOR = {
    "fg": 7.0, "fg_target": 11.5,
    "muted": 4.9, "subtle": 3.5,
    "accent": 4.6, "graphic": 3.0, "state": 4.6,
    "line": 3.0, "line_strong": 4.2, "line_soft": 1.5,
    "on_fill": 4.5,
    # Proven and failed must stay apart from each other, not only from the
    # background. Colour never carries a state alone — the guide gives that job
    # to the glyph — but where both land in one list they must not collapse into
    # one grey for the reader who cannot separate red from green. A house floor,
    # and it cuts both ways: it is what stops the accent being darkened past the
    # point where proven and failed meet.
    "separation": 1.5,
    # Two colours in one hue family stop being two colours, however their
    # lightness measures. This is the check the previous palette had no way to
    # state, and it is why the secondary is violet and not another warm.
    "hue_separation": 40.0,
}

TINT = {"light": 0.12, "dark": 0.13}


def _fill_at(H, C, dark):
    """A filled accent has to admit a readable label, so its lightness is not
    fixed: the hue and chroma are what the palette chose, and the lightness moves
    until white or near-black clears the floor on it."""
    ladder = [0.74, 0.79, 0.84, 0.69, 0.88, 0.64] if dark else [0.60, 0.55, 0.50, 0.65, 0.45, 0.70]
    for L in ladder:
        f = oklch(L, C, H)
        if contrast(f, _fg_on(f)) >= FLOOR["on_fill"] + 0.05:
            return f
    return oklch(0.90 if dark else 0.38, C, H)


def _fg_on(fill):
    return WHITE if contrast(fill, WHITE) >= contrast(fill, "#0B0B0E") else "#0B0B0E"


def _separate(c, other, bg, floor, sep):
    """Step `c` away from `other` until they are `sep` apart in lightness,
    without letting `c` fall below its own floor on `bg`."""
    if contrast(c, other) >= sep:
        return c
    L, C, H = hex_to_oklch(c)
    away = -1 if luminance(c) < luminance(other) else 1
    for step in (away, -away):
        for i in range(1, 61):
            cand = oklch(L + step * 0.004 * i, C, H)
            if contrast(cand, bg) < floor:
                break
            if contrast(cand, other) >= sep:
                return cand
    return c


def _theme(dark):
    ground = DARK_GROUND if dark else LIGHT_GROUND
    fam = NEUTRAL["dark" if dark else "light"]
    up = dark
    step = 1 if dark else -1
    tint = TINT["dark" if dark else "light"]

    bg = oklch(ground["L"], ground["C"], ground["H"])
    surface = bg
    # The raised band steps further on the dark ground than on the light one: a
    # near-black needs more lift to separate than a near-white needs shade.
    raised = shift_l(bg, step * (0.030 if dark else 0.022))
    code_bg = shift_l(bg, -step * 0.016)

    raw_accent = oklch(0.78 if dark else 0.55, ACCENT["C"], ACCENT["H"])
    raw_second = oklch(0.78 if dark else 0.55, SECOND["C"], SECOND["H"])
    fault = FAULT["dark" if dark else "light"]

    # A tinted fill is a surface too, and text lands on it. Counting the page
    # alone is how a palette passes review and fails an audit.
    softs = [mix(bg, c, tint) for c in (raw_accent, raw_second, fault)]
    pick = (lambda xs: max(xs, key=luminance)) if dark else (lambda xs: min(xs, key=luminance))
    worst_text = pick([bg, surface, raised, code_bg] + softs)
    worst_state = pick([bg, surface, raised] + softs)

    accent = tone_on(worst_state, ACCENT["C"], ACCENT["H"], FLOOR["accent"], up)
    second = tone_on(worst_state, SECOND["C"], SECOND["H"], FLOOR["state"], up)
    accent_fill = _fill_at(ACCENT["H"], ACCENT["C"], dark)
    second_fill = _fill_at(SECOND["H"], SECOND["C"], dark)

    return {
        "bg": bg,
        "surface": surface,
        "raised": raised,
        "code-bg": code_bg,
        "fg": tone_on(worst_text, min(fam["C"] * 2.4, 0.055), fam["H"], FLOOR["fg_target"], up),
        "muted": tone_on(worst_text, fam["C"] * 1.35, fam["H"], FLOOR["muted"], up),
        "subtle": tone_on(worst_text, fam["C"] * 1.2, fam["H"], FLOOR["subtle"], up),
        "line": tone_on(bg, fam["C"], fam["H"], FLOOR["line"], up),
        "line-strong": tone_on(bg, fam["C"], fam["H"], FLOOR["line_strong"], up),
        "line-soft": tone_on(bg, fam["C"], fam["H"], FLOOR["line_soft"], up),
        # Two strengths of one accent, found two different ways. Text takes the
        # least extreme tone that clears 4.5:1 — right for text, which should not
        # be darker than it needs to be. A mark takes the colour that was chosen
        # and moves only if it would fail its own 3:1 floor: least-extreme means
        # closest to the background, which on a dark ground drew a seal fainter
        # than the link text beside it.
        "accent": accent,
        "accent-graphic": hold_or_tone(raw_accent, worst_state, FLOOR["graphic"], up),
        "accent-fill": accent_fill,
        "accent-fg": _fg_on(accent_fill),
        "accent-soft": mix(bg, raw_accent, tint),
        "second": second,
        "second-graphic": hold_or_tone(raw_second, worst_state, FLOOR["graphic"], up),
        "second-fill": second_fill,
        "second-fg": _fg_on(second_fill),
        "second-soft": mix(bg, raw_second, tint),
        "fault": _separate(hold_or_tone(fault, worst_state, FLOOR["state"], up),
                           accent, worst_state, FLOOR["state"], FLOOR["separation"]),
        "fault-soft": mix(bg, fault, tint),
        "_worst_text": worst_text,
        "_worst_state": worst_state,
    }


THEMES = {"light": _theme(False), "dark": _theme(True)}

# --- the named colours -----------------------------------------------------

# What the guide's table names and the marks are painted with: a view onto the
# roles above, never a second set of values. A name that stopped being true was
# renamed rather than kept — Border sand is a cool grey now, and calling it sand
# would be the kind of drift this file exists to prevent.
COLORS = {
    "ink":           {"hex": THEMES["dark"]["bg"],              "role": "Dark ground. Dark surfaces, and the ring on them is drawn from Paper."},
    "paper":         {"hex": THEMES["light"]["bg"],             "role": "Light ground; light elements on Ink."},
    "green":         {"hex": THEMES["light"]["accent-graphic"], "role": "Evidence green. The check on Paper, success, 'proven'."},
    "mint":          {"hex": THEMES["dark"]["accent-graphic"],  "role": "The check on Ink; success in dark UI."},
    "iris":          {"hex": THEMES["light"]["second-graphic"], "role": "Secondary accent on Paper. Never a brand asset."},
    "lilac":         {"hex": THEMES["dark"]["second-graphic"],  "role": "Secondary accent on Ink. Never a brand asset."},
    "fault-red":     {"hex": FAULT["light"],                    "role": "Failed verification on Paper."},
    "fault-rose":    {"hex": FAULT["dark"],                     "role": "Failed verification on Ink."},
    "border-paper":  {"hex": THEMES["light"]["line"],           "role": "Hairlines on Paper."},
    "border-ink":    {"hex": THEMES["dark"]["line"],            "role": "Hairlines on Ink."},
}

for _c in COLORS.values():
    _c["rgb"] = [int(_c["hex"][i:i + 2], 16) for i in (1, 3, 5)]

INK = COLORS["ink"]["hex"]
PAPER = COLORS["paper"]["hex"]
GREEN = COLORS["green"]["hex"]
MINT = COLORS["mint"]["hex"]
BORDER_PAPER = COLORS["border-paper"]["hex"]

# The fault pair gets no module-level constant, unlike the colours above: red
# marks a product state, never a brand asset (guide §2), so no generator here has
# any business painting with it. It reaches the product through the tokens. The
# secondary pair is withheld for the same reason.
