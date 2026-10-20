#!/usr/bin/env python3
"""Builds docs/*.html from docs-src/*.html fragments: adds the shared header, guide list and footer.

Each fragment starts with a comment line: <!-- title: Page title | summary: One sentence for the guide index -->
Run: python3 build_docs.py   (then commit docs/)
"""
import re
from pathlib import Path

ORDER = ["getting-started", "photos", "settings", "screens-and-buttons", "privacy", "updating", "home-screen", "troubleshooting"]
ROOT = Path(__file__).parent
SRC, OUT = ROOT / "docs-src", ROOT / "docs"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Halcyon Frame guides</title>
<meta name="description" content="{summary}">
<link rel="icon" href="../img/mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="../"><img src="../img/mark.svg" alt="" width="30" height="30"><span>Halcyon Frame</span></a>
  <nav>
    <a href="../#how">How it works</a>
    <a href="../#install">Install</a>
    <a href="./" aria-current="page">Guides</a>
    <a href="https://github.com/halcyonframe/halcyonframe">GitHub</a>
  </nav>
</header>
<main class="doc">
  <nav class="guides" aria-label="Guides">
    <p class="guides-title">Guides</p>
    {nav}
  </nav>
  <article>
{body}
    <p class="pager">{pager}</p>
  </article>
</main>
<footer>
  <img src="../img/mark.svg" alt="" width="24" height="24">
  <p>Halcyon Frame · MIT licensed · <a href="https://github.com/halcyonframe">GitHub</a><br>
    <span class="fine">Found a mistake in a guide? <a href="https://github.com/halcyonframe/website/issues">Tell us</a>.</span></p>
</footer>
</body>
</html>
"""

meta = {}
for name in ORDER:
    text = (SRC / f"{name}.html").read_text()
    m = re.match(r"<!-- title: (.*?) \| summary: (.*?) -->\n", text)
    assert m, f"{name}: first line must be the title/summary comment"
    meta[name] = (m.group(1), m.group(2), text[m.end():])


def nav(current):
    items = []
    for n in ORDER:
        cur = ' aria-current="page"' if n == current else ""
        items.append(f'<a href="{n}.html"{cur}>{meta[n][0]}</a>')
    return "\n    ".join(items)


for i, name in enumerate(ORDER):
    title, summary, body = meta[name]
    prev = f'<a href="{ORDER[i-1]}.html">&larr; {meta[ORDER[i-1]][0]}</a>' if i else '<a href="./">&larr; All guides</a>'
    nxt = f'<a href="{ORDER[i+1]}.html">{meta[ORDER[i+1]][0]} &rarr;</a>' if i + 1 < len(ORDER) else ""
    (OUT / f"{name}.html").write_text(PAGE.format(title=title, summary=summary, nav=nav(name), body=body.rstrip(), pager=f"{prev} {nxt}"))

cards = "\n".join(f'    <a class="guide-card" href="{n}.html"><h3>{meta[n][0]}</h3><p>{meta[n][1]}</p></a>' for n in ORDER)
index_body = f"""    <h1>Guides</h1>
    <p class="lede">How to set up, use and look after your Halcyon Frame. If something isn't working, start with <a href="troubleshooting.html">Troubleshooting</a>.</p>
    <div class="guide-cards">
{cards}
    </div>"""
(OUT / "index.html").write_text(PAGE.format(title="Guides", summary="How to set up, use and look after your Halcyon Frame.", nav=nav(None), body=index_body, pager=""))
print("built", len(ORDER) + 1, "pages")
