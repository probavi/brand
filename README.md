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

.button { background: var(--probavi-accent); color: var(--probavi-paper); }
.drill--failed { color: var(--probavi-fault); }
```

Light/dark switching is built in, and answers to two signals. By default the tokens follow the OS via `prefers-color-scheme`. If the page sets `data-theme="dark"` or `data-theme="light"` on `<html>` — as Starlight's theme toggle does — that wins over the OS preference in both directions, so a visitor on a light OS who switches the site to dark gets the dark values, and the reverse. Either way `--probavi-accent` resolves to Evidence green on light backgrounds and Mint on dark ones, and `--probavi-border` to Border sand on Paper and Border slate on Ink, as the guide requires. Both hairline pairings are measured at generation time and clear the 3:1 contrast floor — 3.03:1 and 3.43:1 — so a border taken from these tokens stays visible in either theme. `--probavi-fault` is the failed-verification color the product needs and the brand assets never use — Fault red on Paper, Fault rose on Ink, both above the 4.5:1 floor for text (7.25:1 and 5.11:1). Pair it with a glyph rather than relying on the color alone; the guide says why.

## Regenerating

Everything derives from one source of truth — colours and geometry are declared once in `tools/`, so a change propagates to every size and variant consistently.

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

The website consumes it as a read-only git submodule; the core repo just references a couple of files directly. Either way: this repo is the source, edits happen here.
