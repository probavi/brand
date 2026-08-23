#!/usr/bin/env python3
"""The Probavi palette — declared once, consumed by every generator.

This is the source BRAND_GUIDE.md §2 documents. gen_tokens.py emits it as
design tokens; gen_brand.py and gen_outlined.py paint the marks with it. Change
a value here and rerun the generators — no hex literal belongs anywhere else.

Key order is meaningful: it fixes the order of tokens.json and of the custom
properties in tokens.css.
"""

COLORS = {
    "ink":          {"hex": "#1E2A4A", "rgb": [30, 42, 74],     "role": "Primary. Text, ring, dark surfaces."},
    "green":        {"hex": "#0B7B55", "rgb": [11, 123, 85],    "role": "The check, success, 'proven'. Accent only."},
    "mint":         {"hex": "#4ADE9D", "rgb": [74, 222, 157],   "role": "The check on dark surfaces; success text in dark UI."},
    "fault-red":    {"hex": "#9F0E1A", "rgb": [159, 14, 26],    "role": "Failed verification on Paper."},
    "fault-rose":   {"hex": "#EE7781", "rgb": [238, 119, 129],  "role": "Failed verification on Ink."},
    "paper":        {"hex": "#F5F0E8", "rgb": [245, 240, 232],  "role": "Light background; light elements on Ink."},
    "border-sand":  {"hex": "#8E8A81", "rgb": [142, 138, 129],  "role": "Hairlines on Paper."},
    "border-slate": {"hex": "#6E7CA6", "rgb": [110, 124, 166],  "role": "Hairlines on Ink."},
}

INK          = COLORS["ink"]["hex"]
GREEN        = COLORS["green"]["hex"]
MINT         = COLORS["mint"]["hex"]
PAPER        = COLORS["paper"]["hex"]
BORDER_SAND  = COLORS["border-sand"]["hex"]
BORDER_SLATE = COLORS["border-slate"]["hex"]

# The fault pair gets no module-level constant, unlike every colour above: red
# marks a product state, never a brand asset (guide §2), so no generator here
# has any business painting with it. It reaches the product through the tokens.

# Plain white, for the reversed marks that sit on photography or a third
# party's dark background, where one flat colour is all the surface allows.
# On Ink the brand's own dark surface, the mint variants (Paper + Mint) carry
# the mark instead, as the guide requires. Deliberately outside COLORS: white
# is a printing instruction, not a brand colour, and must never reach
# tokens.json.
WHITE = "#FFFFFF"


def luminance(name):
    """WCAG 2.1 relative luminance of a palette entry."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = COLORS[name]["rgb"]
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    """WCAG 2.1 contrast ratio between two palette entries."""
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
