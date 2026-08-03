#!/usr/bin/env python3
"""Generate outlined (path-based) wordmark lockups — pixel-identical without Inter installed."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from _fonts import inter
from _palette import INK, GREEN, MINT, PAPER, WHITE

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FS = 120
font = TTFont(inter("Medium"))
upm = font["head"].unitsPerEm
S = FS / upm
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()

def glyph_path(ch):
    gname = cmap[ord(ch)]
    pen = SVGPathPen(glyphset)
    glyphset[gname].draw(pen)
    return pen.getCommands(), glyphset[gname].width * S

def word_paths(text, x, baseline):
    out, cx = [], x
    for ch in text:
        d, adv = glyph_path(ch)
        if d:
            out.append((cx, d))
        cx += adv
    return out, cx

ICON_S, GAP_IT = 200, 44
X_ICON, Y_ICON, BASE = 20, 20, 165
X_TEXT = X_ICON + ICON_S + GAP_IT
CHK_W, CHK_GAP = int(FS*0.74), int(FS*0.10)

proba_paths, end_proba = word_paths("proba", X_TEXT, BASE)
X_CHK = int(end_proba) + CHK_GAP
X_I = X_CHK + CHK_W + CHK_GAP
i_paths, end_i = word_paths("i", X_I, BASE)
LOGO_W, LOGO_H = int(end_i) + 24, 240
P1 = (X_CHK,                BASE - int(FS*0.34))
P2 = (X_CHK + int(FS*0.27), BASE - int(FS*0.02))
P3 = (X_CHK + CHK_W,        BASE - int(FS*0.72))
CHK_STROKE = int(FS*0.135)

def outlined_svg(text_c, check_c):
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LOGO_W} {LOGO_H}" width="{LOGO_W}" height="{LOGO_H}">
  <g transform="translate({X_ICON},{Y_ICON}) scale({ICON_S/240})">
    <circle cx="120" cy="120" r="98" fill="none" stroke="{text_c}" stroke-width="9" stroke-dasharray="16 9" stroke-linecap="round"/>
    <path d="M 72 122 L 109 166 L 172 81" fill="none" stroke="{check_c}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </g>''']
    for x, d in proba_paths + i_paths:
        parts.append(f'  <path transform="translate({x:.1f},{BASE}) scale({S:.6f},{-S:.6f})" d="{d}" fill="{text_c}"/>')
    parts.append(f'  <path d="M {P1[0]} {P1[1]} L {P2[0]} {P2[1]} L {P3[0]} {P3[1]}" fill="none" stroke="{check_c}" stroke-width="{CHK_STROKE}" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('</svg>')
    return "\n".join(parts)

variants = {"logo-outlined": (INK, GREEN), "logo-mono-outlined": (INK, INK),
            "logo-mint-outlined": (PAPER, MINT), "logo-white-outlined": (WHITE, WHITE)}
for name, (tc, cc) in variants.items():
    open(f"{ROOT}/svg/logo/{name}.svg", "w").write(outlined_svg(tc, cc))
    print(name, "OK  (canvas:", LOGO_W, "x", LOGO_H, ")")
