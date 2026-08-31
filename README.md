# Probavi brand

Visual identity for [Probavi](https://github.com/probavi/probavi) — logos, colours, badges, and the rules for using them.

**This repository is public but not open source.** The marks are reserved; see [LICENSE](LICENSE) for what you may and may not do. The short version: quote us, link us, and display the badge if your drills really pass — but do not ship your own product under this name or logo.

Start with **[BRAND_GUIDE.md](BRAND_GUIDE.md)** — it explains the mark, the palette, clearspace, minimum sizes, and badge usage.

## Contents

| Path | What it is |
|---|---|
| `BRAND_GUIDE.md` | The design manual. Read before using anything here. |
| `svg/icon/` | Seal icon: default, mono, mint (on Ink), white reverse, and app tile. Editable masters. |
| `svg/logo/` | Lockup (icon + wordmark). Live-text masters **and** outlined distribution copies. |
| `svg/badge/` | README shield and the "Proven by Probavi" web badge, light and dark. |
| `png/` | Exports: icon 16–1024 px, lockup at heights 64/128/256, badges at 1×/2× and 32/48/64. |
| `favicon.ico` | Multi-resolution favicon (16 + 32 + 48). |
| `tokens/` | Machine-readable design tokens: `tokens.json` and generated `tokens.css`. |
| `tools/` | Generators — the whole package rebuilds from these. |

## Which file do I need?

- **Website header, docs, slides, README top** → `svg/logo/logo.svg` (on Ink: `logo-mint.svg`; on photography or someone else's dark background: `logo-white.svg`)
- **Favicon, avatar, app icon** → `favicon.ico`, `svg/icon/icon-tile.svg`
- **Sending to a printer, partner, or press** → the `*-outlined.svg` lockups (wordmark converted to paths; renders identically without Inter installed)
- **Styling a site or dashboard** → `tokens/tokens.css`, or `tokens.json` if your build wants structured data
- **Single-colour printing or engraving** → `*-mono.svg`

## Using the tokens

```css
@import "tokens/tokens.css";

.page   { background: var(--probavi-bg); color: var(--probavi-fg); }
.note   { color: var(--probavi-muted); border-top: 1px solid var(--probavi-line); }
.button { background: var(--probavi-accent-fill); color: var(--probavi-accent-fg); }
.seal   { stroke: var(--probavi-accent-graphic); }
.drill--failed { color: var(--probavi-fault); }
```

**Reach for the semantic roles, not the named colours.** There are twenty-two of them per theme —
surfaces (`bg`, `surface`, `raised`, `code-bg`), text tones (`fg`, `muted`, `subtle`), hairlines
(`line`, `line-strong`, `line-soft`), both accents in five strengths each, and the fault pair. The
set is deliberately complete: a consumer that derives its own surface or grey by mixing two brand
colours together is rebuilding the exact defect this palette was rebuilt to remove.

The accent ships in two strengths, and which one you want depends on whether it is read or drawn.
`--probavi-accent` clears 4.5:1 and is for text; `--probavi-accent-graphic` clears 3:1 and keeps
more of the colour, for the mark, a rule or a diagram stroke. `--probavi-accent-fill` is the
filled-control background, and `--probavi-accent-fg` is the only label colour measured against it.

Light/dark switching is built in, and answers to two signals. By default the tokens follow the OS via `prefers-color-scheme`. If the page sets `data-theme="dark"` or `data-theme="light"` on `<html>` — as Starlight's theme toggle does — that wins over the OS preference in both directions, so a visitor on a light OS who switches the site to dark gets the dark values, and the reverse. Either way `--probavi-accent-graphic` resolves to Evidence green on light backgrounds and Mint on dark ones, and `--probavi-line` to Border paper on Paper and Border ink on Ink, as the guide requires. `--probavi-fault` is the failed-verification color the product needs and the brand assets never use — Fault red on Paper, Fault rose on Ink. Pair it with a glyph rather than relying on the color alone; the guide says why. Every semantic role is measured at generation time and clears its WCAG floor in both themes — 4.5:1 for what is read as text, 3:1 for what is drawn, 7:1 for body text — so anything built from these tokens stays legible either way. The generator prints all thirty-five measurements on each run and refuses to emit tokens that fall below them.

## Regenerating

Everything derives from one source of truth — colours and geometry are declared once in `tools/`, so a change propagates to every size and variant consistently. The palette is not a list of hexes: `tools/_palette.py` declares the vector it rests on (two grounds, two accent hues, one neutral hue) and the floors every tone must clear, and `tools/_oklch.py` holds the arithmetic that turns one into the other.

```bash
pip install -r requirements.txt
python3 tools/gen_brand.py     # icons, lockups, badges, PNG exports, favicon
python3 tools/gen_outlined.py  # outlined distribution copies of the lockups
python3 tools/gen_tokens.py    # tokens.json + tokens.css
```

`requirements.txt` pins the toolchain exactly, transitive dependencies included, because a rasteriser version is an input to the artifacts: the pinned set reproduces every text-free PNG export byte for byte. Bump it deliberately and re-check the exports when you do.

Two prerequisites pip cannot supply: the **system cairo library** (`cairocffi` binds to it), and **[Inter](https://rsms.me/inter/)** (SIL Open Font License) as a TTF on disk, needed by `gen_brand.py` for PNG text and by `gen_outlined.py` for the wordmark outlines. `gen_tokens.py` needs neither — it is standard library only, so tokens regenerate anywhere.

Inter is looked up in the usual font directories (`~/.fonts`, `~/.local/share/fonts`, the system ones) and via fontconfig. To use an unpacked release without installing it, point `INTER_DIR` at the directory holding `Inter-Medium.ttf` and `Inter-Regular.ttf`:

```bash
INTER_DIR=~/Downloads/Inter-4.1/extras/ttf python3 tools/gen_brand.py
```

Reproducibility is verified, not assumed: with the pinned toolchain and Inter 4.1, rerunning all three generators reproduces every committed artifact — 49 files across `png/`, `svg/`, `favicon.ico` and `tokens/` — byte for byte.

**Never edit files under `png/` or `tokens/` by hand** — they are generated. Change the source in `tools/` (or the SVG masters) and rerun.

## Using this repo from other projects

**This repository is the source. Edits happen here, never in a consumer's copy.**

There are no submodules. Every Probavi repository sits side by side in one workspace, so a person or an agent reads this one from the sibling directory — a fresh read is the default rather than a manual act.

A build has no sibling: CI clones a single repository. So a consumer commits the files it actually uses — `tokens/tokens.css`, an icon, the favicon — with the brand commit they were taken from and a digest per file recorded beside them, and refreshes them with a script that runs first in every local check and build. The committed copy is transport to CI, not a pin: a token diff turning up in an unrelated pull request means the brand moved, which is the signal working.

There is nothing to pin to in any case. `tokens.css` and `tokens.json` carry no version and nothing asserts one; the version in the guide's header is a document version, written for humans. Consumers import the tokens rather than restating them — a brand value copied into someone else's stylesheet as a literal is how a retired colour keeps shipping.
