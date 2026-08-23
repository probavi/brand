# Probavi brand guide

Version 1.4 · 2026-08-23

Probavi is Latin for **"I have proven."** Everything in this identity serves that sentence: the mark is a seal, not a mascot; the palette says trust, not hype; the checkmark is a certificate, not a to-do item.

---

## 1. The mark

The icon is a **seal**: a dashed ring enclosing a checkmark.

- **The dashed ring** is not decoration — the segments represent the hash chain, the linked sequence of evidence records. Keep the dash rhythm exactly as drawn; never replace it with a solid circle.
- **The check** rises past the ring's midline, ending high — proof with momentum, not a passive tick.
- **The wordmark** sets the product name in Inter Medium, lowercase, with the letter "v" replaced by the brand check in Evidence green. The name shows what it says. Never typeset "probavi" with a plain "v" in logo contexts; in running text, ordinary spelling ("Probavi") is correct.
- **The check-v beyond the lockup.** The wordmark's spelling is also permitted in **featured display** — a hero headline, a footer signature, a section or slide title — where the name is the subject of the view rather than a word inside a sentence. Keep it rare: a few anchor points per site, not every mention. Set the check in Evidence green (Mint on Ink), on the same baseline and at the same weight as the surrounding letters, and leave the underlying text as the plain string "probavi" so it copies, searches, and is read aloud correctly — the check is styling, not a glyph swap or an image. Where the name is inflected, joined to other words, or set in body copy, captions, or legal text, ordinary spelling stands.

### Variants and when to use them

| File | Use |
|---|---|
| `icon.svg` / `icon-*.png` | Default icon on light backgrounds |
| `icon-mono.svg` | Single-color contexts: print, engraving, embossing, fax-grade reproduction |
| `icon-mint.svg` | On Ink: Paper ring, Mint check |
| `icon-white.svg` | Flat white reverse, where the surface allows one color only: photography, a third party's dark background |
| `icon-tile.svg` | App icon / avatar: Ink rounded square, Paper ring, Mint check |
| `logo.svg` | Default lockup (icon + wordmark) on light backgrounds |
| `logo-mono.svg` | Single-color lockup |
| `logo-mint.svg` | Lockup on Ink: Paper wordmark and ring, Mint check |
| `logo-white.svg` | Flat white reverse lockup, on photography or a third party's dark background |

**On Ink, reach for the mint variants.** They keep the two voices the color rules ask for — Paper draws the structure, Mint carries the proof. The white marks are a concession to surfaces that grant a single color, not the house treatment for a dark background: on the brand's own Ink they flatten the check into the ring and the proof stops reading as proof.

**Choosing icon vs. lockup:** use the full lockup wherever the audience may not know the product (website header, docs, presentations, README top). Use the icon alone only where the name is nearby or the context is established (favicon, app icon, social avatar, CLI, repeated UI elements).

### Clearspace and minimum sizes

- **Clearspace:** keep a margin of at least **one ring-stroke-width × 3** (≈ the length of one dash segment) around the mark on all sides. Nothing enters this zone — no text, rules, or other logos.
- **Minimum sizes:** icon 16 px (favicon floor); lockup 24 px height. Below that, drop to icon only.
- Never stretch, rotate, recolor outside the palette, add shadows/gradients/outlines, or place the color icon on low-contrast backgrounds.

## 2. Color

| Name | Hex | RGB | Role |
|---|---|---|---|
| Ink | `#1E2A4A` | 30 42 74 | Primary. Text, ring, dark surfaces. Trust and gravity. |
| Evidence green | `#0E9F6E` | 14 159 110 | The check, success states, "proven". Accent only — never large surfaces. |
| Mint | `#4ADE9D` | 74 222 157 | The check on dark surfaces (Ink backgrounds), success text in dark UI. |
| Fault red | `#9F0E1A` | 159 14 26 | Failed verification on Paper. Product UI only — never in a brand asset. |
| Fault rose | `#EE7781` | 238 119 129 | Failed verification on Ink (dark UI). Product UI only. |
| Paper | `#F5F0E8` | 245 240 232 | Light background, light elements on Ink. |
| Border sand | `#8E8A81` | 142 138 129 | Hairlines on Paper (badge borders, dividers). |
| Border slate | `#6E7CA6` | 110 124 166 | Hairlines on Ink (dark-surface dividers, card edges, table rules). |

Both hairlines are their background's own hue, pushed until it separates: Border slate is Ink desaturated and lightened, Border sand is Paper darkened. Both are measured, and both clear the 3:1 floor for non-text that carries structure — **Border sand 3.03:1 against Paper, Border slate 3.43:1 against Ink**. Hairlines are structure, not decoration: a divider that cannot be seen is a divider that is not there, and that holds in daylight as much as in the dark. The floor is not left to prose — `tools/gen_tokens.py` measures every theme's hairline on each run and refuses to emit tokens that fall below it.

Rules: one accent, used sparingly — the check carries the green; UI should not compete with it. On Ink, always pair Paper (structure) with Mint (proof); hairlines on Ink are Border slate, never Ink itself and never the accent.

**The fault pair.** Red is reserved exclusively for failed-verification states in the product, and never appears in a brand asset — no mark, badge, or export in this package contains it, and the generators are not even given a constant for it. It is declared here so the product does not have to invent one: `--probavi-fault` resolves to **Fault red, 7.25:1 against Paper**, and on dark surfaces to **Fault rose, 5.11:1 against Ink**. Both clear the 4.5:1 floor for text, because a failed drill is read, not merely noticed. Fault red carries Evidence green's own saturation and value, rotated to red; Mint's construction could not be mirrored the same way — red is the darkest hue on the wheel, and the naive mirror lands at 3.51:1 on Ink — so the dark counterpart is measured to the floor instead of derived.

**Never let color carry the state alone.** Proven and failed differ first by glyph — the brand check against a cross, drawn at the same stroke weight and with the same round caps — and only then by color. Around one man in twelve cannot separate red from green, and for that reader the glyph is the whole message. The two colors are held apart in lightness as well (2.43:1 in light, 1.61:1 on Ink) so a status list survives grayscale, and `tools/gen_tokens.py` enforces that separation alongside both 4.5:1 floors on every run.

## 3. Typography

- **Brand and UI face: Inter** (SIL Open Font License; https://rsms.me/inter/). Wordmark: Inter Medium (500), lowercase, default tracking. Product/docs: Regular (400) for body, Medium (500) for emphasis and headings. Avoid weights above 500 — the brand voice is calm, not loud.
- **Code and evidence excerpts:** any neutral monospace (product default terminal font); evidence record snippets are part of the brand's visual language — show them often.
- Sentence case everywhere. No all-caps except unavoidable acronyms (RTO, DORA).

## 4. Badges

**README shield** (`badge-shield.svg`, `badge-shield.png`, `@2x`): a shields.io-style flat badge, Ink "probavi" segment + Evidence green "restore proven" segment. Intended for repositories whose backups are verified by a Probavi drill in CI. Markdown:

```markdown
[![restore proven](badge-shield.png)](https://github.com/CHANGEME/probavi)
```

**Web badge** (`badge-web-light/dark`, heights 32/48/64): "Proven by Probavi" pill for status pages, trust pages, and footer placement. Pick the variant matching the page background; do not restyle. The badge is a claim — display it only where drills are actually running and passing. (Product idea, deliberate: one day the badge can link to a live, publicly verifiable evidence summary.)

## 5. Editing the assets

- **Masters are the SVGs** (`svg/`), hand-editable text: geometry lives in a handful of `stroke-dasharray`, `path`, and `text` attributes. PNGs are exports — never edit them directly; re-export instead.
- The lockup ships in two forms. The **live-text masters** (`logo.svg`, `logo-mono.svg`, `logo-mint.svg`, `logo-white.svg`) use `<text>` with font-family Inter — these are the editable source. The **outlined distribution copies** (`logo-outlined.svg`, `logo-mono-outlined.svg`, `logo-mint-outlined.svg`, `logo-white-outlined.svg`) have the wordmark converted to vector paths, so they render pixel-identically everywhere, with or without Inter installed. **Rule: send outlined copies to third parties (printers, partners, press kits); edit only the live-text masters, then regenerate the outlined copies** (`tools/gen_outlined.py`).
- Everything regenerates from one script (`tools/gen_brand.py` in this package): colors, geometry, and layout are defined once; change a constant, rerun, and every size and variant stays consistent.
- Design tokens (`tokens/tokens.json`, `tokens/tokens.css`) are generated from the same source by `tools/gen_tokens.py` — consume these in the website and dashboard rather than hardcoding hex values.
- Standard exports included: icon PNGs at 16–1024 px, lockup at heights 64/128/256, `favicon.ico` (16+32+48), badges at 1×/2× and heights 32/48/64.

## 6. Voice (one paragraph, for completeness)

Probavi speaks in measured, verifiable statements. Prefer "proven", "measured", "recorded" over "amazing", "blazing", "revolutionary". Numbers over adjectives; the strongest marketing sentence the brand can utter is a fact with a timestamp.
