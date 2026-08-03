#!/usr/bin/env python3
"""Locate the Inter TTFs the generators need.

Inter is not vendored — it ships under the SIL Open Font License and has to be
present on the machine (https://rsms.me/inter/). Look for it in the places a
font actually lives rather than one hardcoded path, so the build runs as any
user, and fail with the search list when it is genuinely missing.

Point INTER_DIR at an unpacked Inter release to override the search.
"""
import os, shutil, subprocess

def _dirs():
    return [d for d in (
        os.environ.get("INTER_DIR"),
        os.path.expanduser("~/.fonts"),
        os.path.expanduser("~/.local/share/fonts"),
        "/usr/local/share/fonts",
        "/usr/share/fonts",
        "/root/.fonts",
    ) if d]

def _search_dirs(filename):
    for d in _dirs():
        if not os.path.isdir(d):
            continue
        try:
            for root, _, files in os.walk(d):
                if filename in files:
                    return os.path.join(root, filename)
        except PermissionError:
            continue  # e.g. /root/.fonts as a normal user
    return None

def _search_fontconfig(style):
    """Ask fontconfig, but only accept a genuine Inter match.

    fc-match always answers, falling back to whatever it likes, so the family
    has to be checked or the build would silently render in DejaVu.
    """
    if not shutil.which("fc-match"):
        return None
    try:
        out = subprocess.run(
            ["fc-match", "-f", "%{family}\t%{file}", f"Inter:style={style}"],
            capture_output=True, text=True, timeout=5,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    family, _, path = out.partition("\t")
    if "inter" in family.lower() and os.path.isfile(path):
        return path
    return None

def inter(style):
    """Return the path to Inter-<style>.ttf, or exit with an actionable message."""
    filename = f"Inter-{style}.ttf"
    return (
        _search_dirs(filename)
        or _search_fontconfig(style)
        or _missing(filename)
    )

def _missing(filename):
    raise SystemExit(
        f"{filename} not found. Inter is required to build the lockups and PNG "
        f"text (SIL OFL, https://rsms.me/inter/).\n"
        f"Install it, or set INTER_DIR to an unpacked release.\n"
        f"Searched:\n" + "\n".join(f"  {d}" for d in _dirs())
    )
