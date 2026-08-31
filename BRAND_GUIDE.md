# Probavi brand guide

Version 2.0 · 2026-08-31

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

| Name | Hex | Role |
|---|---|---|
| Ink | `#050709` | Dark ground. Dark surfaces; on them the ring is drawn from Paper. |
| Paper | `#FCFDFE` | Light ground; light elements on Ink. |
| Evidence green | `#00856E` | The check on Paper, success, "proven". Accent only — never large surfaces. |
| Mint | `#4AD1B3` | The check on Ink; success in dark UI. |
| Iris | `#7D5EAF` | Secondary accent on Paper. Product UI only — never in a brand asset. |
| Lilac | `#C4A5FB` | Secondary accent on Ink. Product UI only. |
| Fault red | `#9F0E1A` | Failed verification on Paper. Product UI only. |
| Fault rose | `#EE7781` | Failed verification on Ink. Product UI only. |
| Border paper | `#8A949F` | Hairlines on Paper. |
| Border ink | `#525D69` | Hairlines on Ink. |

**The palette is derived, not picked.** What `tools/_palette.py` declares is a vector: two
grounds, two accent hues, one neutral hue, and the contrast floors every tone has to clear. The
table above is the output. Change a hue and rerun, and the whole system moves together — a colour
cannot be nudged by hand into a value that fails a floor, because no colour here is written by
hand.

**The neutral scale takes the ground's own hue.** Every grey, hairline and text tone in a theme is
built from the hue that theme's background already has. This is the correction that matters most.
The previous palette named only eight colours, so every consumer invented the rest by mixing the
two grounds into each other — a blue-purple navy and a yellow cream, nine steps of it — and the
result was the muddy, slightly bruised grey that made finished pages read as drab rather than
calm. The scale is now complete and shipped: twenty-two semantic roles per theme in
`tokens/tokens.css`. **A consumer that mixes its own is rebuilding the defect.**

**The accent has two strengths, and they are found two different ways.** Text takes the least
extreme tone that clears 4.5:1 — the right rule for text, which should not be darker than it needs
to be. A drawn element — the check, the ring, a rule, a diagram stroke — only has to clear 3:1, and
takes the colour that was chosen, moving only if that colour would fail. The distinction is not
academic: "least extreme" means *closest to the background*, so applying the text rule to a mark
drew a seal on Ink at 3.48:1, fainter than the link text beside it. Use `--probavi-accent` where it
is read and `--probavi-accent-graphic` where it is drawn.

**Every ratio here is measured, and the generator refuses to emit below the floor.** WCAG 2.1's
numbers where WCAG has one: 4.5:1 for anything read as text, 3:1 for non-text that carries
structure. Body text is held to AAA, 7:1, because it is what every page is made of. The floors are
not left to prose — `tools/gen_tokens.py` measures all thirty-five of them on every run and prints
each one. Every defect this package has shipped fails that table: a dark hairline that resolved to
its own background at 1.00:1, a light one left at 1.33:1 when the dark side was fixed, and a green
at 2.98:1 on Paper, unreadable as the success state it names.

**Red is the fixed anchor.** A failed restore is red; every other hue works around it, and the
generator measures that it does. Two colours in one hue family stop being two colours, whatever
their lightness measures — so the accent stands 149.6° from Fault red and the secondary 85.4°, both
well past the 40° floor. This is the check the previous palette had no way to state, and it is why
the secondary accent is a violet and not another warm: an amber sits about 30° from Fault red, close
enough that a status list would ask the reader to tell two warms apart.

**Never let colour carry the state alone.** Proven and failed differ first by glyph — the brand
check against a cross, drawn at the same stroke weight and with the same round caps — and only then
by colour. Around one man in twelve cannot separate red from green, and for that reader the glyph
is the whole message. The two are also held apart in lightness (1.52:1 on Paper, 1.51:1 on Ink) so
a status list survives grayscale, and `gen_tokens.py` enforces that separation alongside the
contrast floors. That floor cuts both ways: it is also what stops the accent being darkened past
the point where proven and failed meet.

**The secondary accent is declared, not assigned.** Iris and Lilac exist so the product does not
have to invent a second voice — for a diagram's other axis, a code string, a tab indicator, an
editorial highlight. They carry no state in this package. Whether the product gives one of them a
state is a product decision, and not this repository's to take.

Rules: one accent carries the proof, used sparingly — the check owns the green, and UI should not
compete with it. On Ink, always pair Paper (structure) with Mint (proof); hairlines on Ink are
Border ink, never Ink itself and never the accent. Neither fault colour nor either secondary ever
appears in a brand asset — no mark, badge or export in this package contains one, and the
generators are not given a constant for them.

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
- Design tokens (`tokens/tokens.json`, `tokens/tokens.css`) are generated from the same source by `tools/gen_tokens.py` — consume these in the website and dashboard rather than hardcoding hex values, and consume the **semantic roles** rather than the named colours: a surface, a text tone or a hairline that a consumer derives for itself is a colour the brand can no longer move.
- The palette itself is derived. `tools/_palette.py` holds the vector and the floors; `tools/_oklch.py` holds the arithmetic — OKLab conversion, WCAG contrast, and the search that finds the lightness which just clears a given floor at a given hue.
- Standard exports included: icon PNGs at 16–1024 px, lockup at heights 64/128/256, `favicon.ico` (16+32+48), badges at 1×/2× and heights 32/48/64.

## 6. Voice (one paragraph, for completeness)

Probavi speaks in measured, verifiable statements. Prefer "proven", "measured", "recorded" over "amazing", "blazing", "revolutionary". Numbers over adjectives; the strongest marketing sentence the brand can utter is a fact with a timestamp.
