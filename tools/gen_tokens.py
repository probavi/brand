#!/usr/bin/env python3
"""Generate machine-readable design tokens from the single source of truth."""
import json, os
from _oklch import contrast, hex_to_oklch, hue_distance
from _palette import COLORS, FAULT, FLOOR, THEMES, ACCENT, SECOND

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# The semantic roles, in emission order. Every one of them is a surface, a text
# tone, a line or a state — a consumer that reaches past these for a raw colour
# is rebuilding the scale by hand, which is the drift this package exists to
# stop. The scale is deliberately complete: the previous token set stopped at
# five roles, and every consumer invented the missing ones by mixing the two
# grounds together, which is what made the surfaces read as muddy.
ROLES = [
    "bg", "surface", "raised", "code-bg",
    "fg", "muted", "subtle",
    "line", "line-strong", "line-soft",
    "accent", "accent-graphic", "accent-fill", "accent-fg", "accent-soft",
    "second", "second-graphic", "second-fill", "second-fg", "second-soft",
    "fault", "fault-soft",
]

TYPOGRAPHY = {
    "family": {
        "sans": "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif",
        "mono": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    },
    "weight": {"regular": 400, "medium": 500},
    "note": "Wordmark: Inter Medium (500), lowercase. Never use weights above 500.",
}

GEOMETRY = {
    "seal": {
        "viewbox": 240, "center": [120, 120], "radius": 98,
        "ring_stroke": 9, "ring_dasharray": [16, 9],
        "check_path": "M 72 122 L 109 166 L 172 81", "check_stroke": 16,
    },
    "clearspace": "3 × ring stroke width on all sides",
    "min_size_px": {"icon": 16, "lockup_height": 24},
}

# Why each floor exists, printed with the failure so a broken run explains
# itself rather than naming a number.
REASONS = {
    "fg": "text that cannot be read is text that is not there",
    "muted": "a secondary tone still has to be read, on every surface it can land on",
    "subtle": "a tone too faint to see is decoration pretending to be information",
    "accent": "an accent that cannot be read is decoration, not a state",
    "accent-graphic": "a mark that cannot be seen is a mark that is not there",
    "second": "a secondary accent that cannot be read is not a second voice",
    "second-graphic": "a mark that cannot be seen is a mark that is not there",
    "fault": "a failure that cannot be read is a failure that was never reported",
    "line": "a divider that cannot be seen is a divider that is not there",
    "line-strong": "an edge that carries structure has to carry it visibly",
    "on-fill": "a label on a filled control is the control",
}

# Text tones are measured against the worst surface they can land on, never
# against the page alone. Measuring against the page is how a palette passes
# review and fails an audit: the previous one cleared 5.75:1 on the page and
# 2.98:1 on the surface inline code brought with it.
TEXT_ROLES = {"fg": "fg", "muted": "muted", "subtle": "subtle"}
STATE_ROLES = {"accent": "accent", "accent-graphic": "graphic",
               "second": "state", "second-graphic": "graphic", "fault": "state"}
LINE_ROLES = {"line": "line", "line-strong": "line_strong"}


def check(theme_name):
    t = THEMES[theme_name]
    fails = []

    def measure(label, a, b, floor, reason_key):
        ratio = contrast(a, b)
        print(f"  {theme_name:5s} {label:34s} = {ratio:5.2f}:1  (floor {floor:g})")
        if ratio < floor:
            fails.append(f"{theme_name}: {label} is {ratio:.2f}:1, below {floor:g}:1 — {REASONS[reason_key]}")

    # Body text has to hold on every surface the palette declares, not only the
    # one it was derived against.
    for surface in ("bg", "surface", "raised", "code-bg"):
        measure(f"fg on {surface}", t["fg"], t[surface], FLOOR["fg"], "fg")
    for role, key in TEXT_ROLES.items():
        if role == "fg":
            continue
        measure(f"{role} on worst surface", t[role], t["_worst_text"], FLOOR[key], role)
    for role, key in STATE_ROLES.items():
        measure(f"{role} on worst surface", t[role], t["_worst_state"], FLOOR[key], role)
    for role, key in LINE_ROLES.items():
        measure(f"{role} on bg", t[role], t["bg"], FLOOR[key], role)
    for side in ("accent", "second"):
        measure(f"{side}-fg on {side}-fill", t[f"{side}-fg"], t[f"{side}-fill"], FLOOR["on_fill"], "on-fill")

    apart = contrast(t["fault"], t["accent"])
    print(f"  {theme_name:5s} {'fault vs accent (lightness)':34s} = {apart:5.2f}:1  (floor {FLOOR['separation']:g})")
    if apart < FLOOR["separation"]:
        fails.append(
            f"{theme_name}: fault and accent are only {apart:.2f}:1 apart — proven and failed "
            f"would read as one colour in grayscale"
        )
    return fails


def check_hues():
    """Two colours in one hue family stop being two colours, whatever their
    lightness measures. Red is the fixed anchor: a failed restore is red, so the
    accent and the secondary are the ones that have to stand clear of it."""
    fault_h = hex_to_oklch(FAULT["light"])[2]
    pairs = [
        ("accent vs fault", ACCENT["H"], fault_h),
        ("second vs fault", SECOND["H"], fault_h),
        ("second vs accent", SECOND["H"], ACCENT["H"]),
    ]
    fails = []
    for label, a, b in pairs:
        d = hue_distance(a, b)
        print(f"  hue   {label:34s} = {d:5.1f}°   (floor {FLOOR['hue_separation']:g}°)")
        if d < FLOOR["hue_separation"]:
            fails.append(f"{label} is {d:.1f}° apart, below {FLOOR['hue_separation']:g}° — "
                         f"the two would read as one colour family")
    return fails


def by_hex():
    """Named colours indexed by value, so a semantic role that happens to be one
    of them emits the reference rather than a second copy of the number."""
    return {c["hex"]: name for name, c in COLORS.items()}


def semantic_block(theme, indent):
    pad = " " * indent
    names = by_hex()
    out = [f"{pad}/* semantic ({theme}) */"]
    for role in ROLES:
        hexv = THEMES[theme][role]
        value = f"var(--probavi-{names[hexv]})" if hexv in names else hexv
        out.append(f"{pad}--probavi-{role}: {value};")
    return out


def main():
    tokens = {
        "color": COLORS,
        "theme": {t: {r: THEMES[t][r] for r in ROLES} for t in THEMES},
        "typography": TYPOGRAPHY,
        "geometry": GEOMETRY,
    }
    with open(f"{ROOT}/tokens/tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)
        f.write("\n")

    lines = [
        "/* Probavi design tokens — GENERATED by tools/gen_tokens.py. Do not edit. */",
        ":root {",
    ]
    for name, c in COLORS.items():
        lines.append(f"  --probavi-{name}: {c['hex']};")
    lines += [
        f"  --probavi-font-sans: {TYPOGRAPHY['family']['sans']};",
        f"  --probavi-font-mono: {TYPOGRAPHY['family']['mono']};",
        "",
    ]
    lines += semantic_block("light", 2)
    lines += [
        "}",
        "",
        "/* Automatic: follow the OS preference when the page states no preference. */",
        "@media (prefers-color-scheme: dark) {",
        "  :root {",
    ]
    lines += semantic_block("dark", 4)
    lines += [
        "  }",
        "}",
        "",
        "/* Manual: an explicit theme on <html> wins over the OS preference, in both",
        "   directions (Starlight and friends set data-theme from their toggle).",
        "   Placed after the media query so source order says so too, not only",
        "   selector specificity. */",
        ':root[data-theme="dark"] {',
    ]
    lines += semantic_block("dark", 2)
    lines += [
        "}",
        "",
        ':root[data-theme="light"] {',
    ]
    lines += semantic_block("light", 2)
    lines += ["}"]

    with open(f"{ROOT}/tokens/tokens.css", "w") as f:
        f.write("\n".join(lines) + "\n")

    print("Generated tokens/tokens.json and tokens/tokens.css")


if __name__ == "__main__":
    os.makedirs(f"{ROOT}/tokens", exist_ok=True)
    problems = check("light") + check("dark") + check_hues()
    if problems:
        raise SystemExit("\n".join(problems))
    main()
