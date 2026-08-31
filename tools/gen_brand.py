#!/usr/bin/env python3
"""Generate the complete Probavi brand package from one source geometry."""
import os, math, cairosvg
from PIL import Image, ImageDraw, ImageFont
from _fonts import inter
from _palette import INK, GREEN, MINT, PAPER, BORDER_PAPER, WHITE

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
F_MED = inter("Medium"); F_REG = inter("Regular")
for d in ["svg/icon","svg/logo","svg/badge","png/icon","png/logo","png/badge"]:
    os.makedirs(f"{ROOT}/{d}", exist_ok=True)

# ---------- ICON (viewBox 240x240, center 120) ----------
def icon_svg(ring, check, tile=None):
    tile_rect = f'<rect x="0" y="0" width="240" height="240" rx="52" fill="{tile}"/>' if tile else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  {tile_rect}
  <circle cx="120" cy="120" r="98" fill="none" stroke="{ring}" stroke-width="9" stroke-dasharray="16 9" stroke-linecap="round"/>
  <path d="M 72 122 L 109 166 L 172 81" fill="none" stroke="{check}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

# On Ink the mark keeps its two voices: Paper draws the structure, Mint the
# proof (guide §2). White-on-white is the reversed mark for surfaces that
# grant only one colour — photography, a third party's dark background.
icons = {
    "icon":      icon_svg(INK, GREEN),
    "icon-mono": icon_svg(INK, INK),
    "icon-mint": icon_svg(PAPER, MINT),
    "icon-white":icon_svg(WHITE, WHITE),
    "icon-tile": icon_svg(PAPER, MINT, tile=INK),
}
for name, svg in icons.items():
    open(f"{ROOT}/svg/icon/{name}.svg","w").write(svg)

for size in [16,32,48,64,128,256,512,1024]:
    cairosvg.svg2png(bytestring=icons["icon"].encode(), write_to=f"{ROOT}/png/icon/icon-{size}.png",
                     output_width=size, output_height=size)
for name in ["icon-mono","icon-mint","icon-white","icon-tile"]:
    for size in [256,1024]:
        cairosvg.svg2png(bytestring=icons[name].encode(), write_to=f"{ROOT}/png/icon/{name}-{size}.png",
                         output_width=size, output_height=size)

# favicon.ico (16+32+48)
imgs = [Image.open(f"{ROOT}/png/icon/icon-{s}.png") for s in (48,32,16)]
imgs[0].save(f"{ROOT}/favicon.ico", sizes=[(48,48),(32,32),(16,16)])

# ---------- WORDMARK GEOMETRY (shared by SVG + PNG) ----------
FS = 120                      # wordmark font size in master coordinates
font_wm = ImageFont.truetype(F_MED, FS)
def tw(t, f): b = f.getbbox(t); return b[2]-b[0]
W_PROBA, W_I = tw("proba", font_wm), tw("i", font_wm)
ICON_S, GAP_IT = 200, 44      # icon size in logo, gap icon->text
CHK_W, CHK_GAP = int(FS*0.74), int(FS*0.10)
X_ICON, Y_ICON = 20, 20
X_TEXT = X_ICON + ICON_S + GAP_IT
BASE = 165                    # text baseline
X_CHK = X_TEXT + W_PROBA + CHK_GAP
X_I   = X_CHK + CHK_W + CHK_GAP
LOGO_W, LOGO_H = X_I + W_I + 24, 240
# check points: rises above x-height like the icon check
P1 = (X_CHK,               BASE - int(FS*0.34))
P2 = (X_CHK + int(FS*0.27), BASE - int(FS*0.02))
P3 = (X_CHK + CHK_W,        BASE - int(FS*0.72))
CHK_STROKE = int(FS*0.135)

def logo_svg(text_c, check_c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LOGO_W} {LOGO_H}" width="{LOGO_W}" height="{LOGO_H}">
  <g transform="translate({X_ICON},{Y_ICON}) scale({ICON_S/240})">
    <circle cx="120" cy="120" r="98" fill="none" stroke="{text_c}" stroke-width="9" stroke-dasharray="16 9" stroke-linecap="round"/>
    <path d="M 72 122 L 109 166 L 172 81" fill="none" stroke="{check_c}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="{X_TEXT}" y="{BASE}" font-family="Inter, Arial, sans-serif" font-weight="500" font-size="{FS}" fill="{text_c}">proba</text>
  <path d="M {P1[0]} {P1[1]} L {P2[0]} {P2[1]} L {P3[0]} {P3[1]}" fill="none" stroke="{check_c}" stroke-width="{CHK_STROKE}" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="{X_I}" y="{BASE}" font-family="Inter, Arial, sans-serif" font-weight="500" font-size="{FS}" fill="{text_c}">i</text>
</svg>'''

logos = {"logo": (INK, GREEN), "logo-mono": (INK, INK),
         "logo-mint": (PAPER, MINT), "logo-white": (WHITE, WHITE)}
for name,(tc,cc) in logos.items():
    open(f"{ROOT}/svg/logo/{name}.svg","w").write(logo_svg(tc,cc))

def rline(d, pts, w, color):
    d.line(pts, fill=color, width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0]-w/2, p[1]-w/2, p[0]+w/2, p[1]+w/2], fill=color)

def render_logo_png(path, text_c, check_c, height):
    scale = 4  # supersample
    img = Image.new("RGBA", (LOGO_W*scale, LOGO_H*scale), (0,0,0,0))
    d = ImageDraw.Draw(img)
    icon_png = cairosvg.svg2png(bytestring=icon_svg(text_c, check_c).encode(),
                                output_width=ICON_S*scale, output_height=ICON_S*scale)
    import io; img.alpha_composite(Image.open(io.BytesIO(icon_png)), (X_ICON*scale, Y_ICON*scale))
    f = ImageFont.truetype(F_MED, FS*scale)
    d.text((X_TEXT*scale, BASE*scale), "proba", font=f, fill=text_c, anchor="ls")
    d.text((X_I*scale, BASE*scale), "i", font=f, fill=text_c, anchor="ls")
    rline(d, [tuple(c*scale for c in p) for p in (P1,P2,P3)], CHK_STROKE*scale, check_c)
    w = int(LOGO_W * height / LOGO_H)
    img.resize((w, height), Image.LANCZOS).save(path)

for h in [64,128,256]: render_logo_png(f"{ROOT}/png/logo/logo-h{h}.png", INK, GREEN, h)
render_logo_png(f"{ROOT}/png/logo/logo-mono-h128.png", INK, INK, 128)
render_logo_png(f"{ROOT}/png/logo/logo-mint-h128.png", PAPER, MINT, 128)
render_logo_png(f"{ROOT}/png/logo/logo-white-h128.png", WHITE, WHITE, 128)

# ---------- BADGE 1: README shield (h=20) ----------
f11 = ImageFont.truetype(F_REG, 11)
def shield_layout():
    lt, rt = "probavi", "restore proven"
    lw = 6 + 13 + 4 + tw(lt,f11) + 6
    rw = 7 + tw(rt,f11) + 7
    return lt, rt, int(lw), int(rw)
LT, RT, LW, RW = shield_layout()
shield_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{LW+RW}" height="20" viewBox="0 0 {LW+RW} 20">
  <clipPath id="r"><rect width="{LW+RW}" height="20" rx="3"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{LW}" height="20" fill="{INK}"/>
    <rect x="{LW}" width="{RW}" height="20" fill="{GREEN}"/>
  </g>
  <g transform="translate(6,3.5) scale({13/240})">
    <circle cx="120" cy="120" r="98" fill="none" stroke="{WHITE}" stroke-width="20" stroke-dasharray="26 15" stroke-linecap="round"/>
    <path d="M 72 122 L 109 166 L 172 81" fill="none" stroke="{MINT}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="23" y="14" font-family="Inter, Verdana, sans-serif" font-size="11" fill="{WHITE}">{LT}</text>
  <text x="{LW+7}" y="14" font-family="Inter, Verdana, sans-serif" font-size="11" fill="{WHITE}">{RT}</text>
</svg>'''
open(f"{ROOT}/svg/badge/badge-shield.svg","w").write(shield_svg)

def render_shield_png(path, scale_out):
    s = 8
    W,H = (LW+RW)*s, 20*s
    img = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0,0,W-1,H-1], radius=3*s, fill=INK)
    right = Image.new("RGBA",(W,H),(0,0,0,0)); dr = ImageDraw.Draw(right)
    dr.rounded_rectangle([0,0,W-1,H-1], radius=3*s, fill=GREEN)
    mask = Image.new("L",(W,H),0); ImageDraw.Draw(mask).rectangle([LW*s,0,W,H], fill=255)
    img.paste(right,(0,0),mask)
    ic = cairosvg.svg2png(bytestring=icon_svg(WHITE, MINT).encode(), output_width=13*s, output_height=13*s)
    import io; img.alpha_composite(Image.open(io.BytesIO(ic)), (6*s, int(3.5*s)))
    f = ImageFont.truetype(F_REG, 11*s)
    d.text((23*s, 14*s), LT, font=f, fill=WHITE, anchor="ls")
    d.text(((LW+7)*s, 14*s), RT, font=f, fill=WHITE, anchor="ls")
    out_w, out_h = (LW+RW)*scale_out, 20*scale_out
    img.resize((out_w,out_h), Image.LANCZOS).save(path)
render_shield_png(f"{ROOT}/png/badge/badge-shield.png",1)
render_shield_png(f"{ROOT}/png/badge/badge-shield@2x.png",2)

# ---------- BADGE 2: web badge "Proven by Probavi" (master h=64) ----------
f24 = ImageFont.truetype(F_MED, 24)
BT = "Proven by Probavi"
BW = 16 + 36 + 12 + int(tw(BT,f24)) + 18
def web_badge_svg(bg, text_c, ring_c, check_c, border):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="64" viewBox="0 0 {BW} 64">
  <rect x="1" y="1" width="{BW-2}" height="62" rx="14" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <g transform="translate(16,14) scale({36/240})">
    <circle cx="120" cy="120" r="98" fill="none" stroke="{ring_c}" stroke-width="14" stroke-dasharray="20 12" stroke-linecap="round"/>
    <path d="M 72 122 L 109 166 L 172 81" fill="none" stroke="{check_c}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <text x="64" y="40" font-family="Inter, Arial, sans-serif" font-weight="500" font-size="24" fill="{text_c}">{BT}</text>
</svg>'''
wb = {"badge-web-light": web_badge_svg(PAPER, INK, INK, GREEN, BORDER_PAPER),
      "badge-web-dark":  web_badge_svg(INK, PAPER, PAPER, MINT, INK)}
for n,s in wb.items(): open(f"{ROOT}/svg/badge/{n}.svg","w").write(s)

def render_web_badge(name, bg, text_c, ring_c, check_c, border, height):
    s = 6; W,H = BW*s, 64*s
    img = Image.new("RGBA",(W,H),(0,0,0,0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([s,s,W-s,H-s], radius=14*s, fill=bg, outline=border, width=int(1.5*s))
    ic = cairosvg.svg2png(bytestring=icon_svg(ring_c, check_c).encode(), output_width=36*s, output_height=36*s)
    import io; img.alpha_composite(Image.open(io.BytesIO(ic)), (16*s, 14*s))
    d.text((64*s, 40*s), BT, font=ImageFont.truetype(F_MED,24*s), fill=text_c, anchor="ls")
    w = int(BW*height/64)
    img.resize((w,height), Image.LANCZOS).save(f"{ROOT}/png/badge/{name}-h{height}.png")
for h in [32,48,64]:
    render_web_badge("badge-web-light", PAPER, INK, INK, GREEN, BORDER_PAPER, h)
    render_web_badge("badge-web-dark",  INK, PAPER, PAPER, MINT, INK, h)

print("Done. Generated:")
for d in ["svg/icon","svg/logo","svg/badge","png/icon","png/logo","png/badge"]:
    for f in sorted(os.listdir(f"{ROOT}/{d}")): print(f"{d}/{f}")
print("favicon.ico")
