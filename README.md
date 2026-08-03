# Probavi brand

Visual identity for [Probavi](https://github.com/probavi/probavi) — logos, colours, badges, and the rules for using them.

**This repository is public but not open source.** The marks are reserved; see [LICENSE](LICENSE) for what you may and may not do. The short version: quote us, link us, and display the badge if your drills really pass — but do not ship your own product under this name or logo.

Start with **[BRAND_GUIDE.md](BRAND_GUIDE.md)** — it explains the mark, the palette, clearspace, minimum sizes, and badge usage.

## Contents

| Path | What it is |
|---|---|
| `BRAND_GUIDE.md` | The design manual. Read before using anything here. |
| `svg/icon/` | Seal icon: default, mono, white, and app tile. Editable masters. |
| `svg/logo/` | Lockup (icon + wordmark). Live-text masters **and** outlined distribution copies. |
| `svg/badge/` | README shield and the "Proven by Probavi" web badge, light and dark. |
| `png/` | Exports: icon 16–1024 px, lockup at heights 64/128/256, badges at 1×/2× and 32/48/64. |
| `favicon.ico` | Multi-resolution favicon (16 + 32 + 48). |
| `tokens/` | Machine-readable design tokens: `tokens.json` and generated `tokens.css`. |
| `tools/` | Generators — the whole package rebuilds from these. |

## Which file do I need?

- **Website header, docs, slides, README top** → `svg/logo/logo.svg` (dark backgrounds: `logo-white.svg`)
- **Favicon, avatar, app icon** → `favicon.ico`, `svg/icon/icon-tile.svg`
- **Sending to a printer, partner, or press** → the `*-outlined.svg` lockups (wordmark converted to paths; renders identically without Inter installed)
- **Styling a site or dashboard** → `tokens/tokens.css`, or `tokens.json` if your build wants structured data
- **Single-colour printing or engraving** → `*-mono.svg`

## Using the tokens

```css
@import "tokens/tokens.css";

.button { background: var(--probavi-accent); color: var(--probavi-paper); }
```

Light/dark switching is built in, and answers to two signals. By default the tokens follow the OS via `prefers-color-scheme`. If the page sets `data-theme="dark"` or `data-theme="light"` on `<html>` — as Starlight's theme toggle does — that wins over the OS preference in both directions, so a visitor on a light OS who switches the site to dark gets the dark values, and the reverse. Either way `--probavi-accent` resolves to Evidence green on light backgrounds and Mint on dark ones, and `--probavi-border` to Border sand on Paper and Border slate on Ink, as the guide requires.

## Regenerating

Everything derives from one source of truth — colours and geometry are declared once in `tools/`, so a change propagates to every size and variant consistently.

```bash
pip install cairosvg pillow fonttools
python3 tools/gen_brand.py     # icons, lockups, badges, PNG exports, favicon
python3 tools/gen_outlined.py  # outlined distribution copies of the lockups
python3 tools/gen_tokens.py    # tokens.json + tokens.css
```

Requires [Inter](https://rsms.me/inter/) (SIL Open Font License) installed locally for the live-text masters and PNG rendering.

**Never edit files under `png/` or `tokens/` by hand** — they are generated. Change the source in `tools/` (or the SVG masters) and rerun.

## Using this repo from other projects

The website consumes it as a read-only git submodule; the core repo just references a couple of files directly. Either way: this repo is the source, edits happen here.
