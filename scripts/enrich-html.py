#!/usr/bin/env python3
"""Add publication metadata and discovery files to an mdBook HTML build."""
from __future__ import annotations
import html, json, re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "book"
BASE = "https://neilydhan.github.io/Blockchain-Scalability-Book/"
REPO = "https://github.com/neilydhan/Blockchain-Scalability-Book"
DESC = "A mechanism-first guide to blockchain scalability, security, trust, and recovery."

if not (OUT / "index.html").exists():
    raise SystemExit("error: book/index.html does not exist; run mdbook build first")

book_schema = {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "Mastering Blockchain Scalability",
    "author": {"@type": "Person", "name": "Neil Han", "url": "https://github.com/neilydhan"},
    "bookFormat": "https://schema.org/EBook",
    "inLanguage": "en",
    "isAccessibleForFree": True,
    "description": DESC,
    "url": BASE,
    "sameAs": [REPO, f"{REPO}/releases/latest"],
    "version": (ROOT / "VERSION").read_text().strip(),
    "datePublished": "2026-09-02",
    "keywords": "blockchain scalability, rollups, data availability, parallel execution, consensus, distributed systems",
}
urls=[]
for path in sorted(OUT.rglob("*.html")):
    rel=path.relative_to(OUT).as_posix()
    if rel == "404.html": continue
    text=path.read_text()
    soup=BeautifulSoup(text,"html.parser")
    for tag in soup.find_all(href=True):
        if tag["href"] in {"README.html", "./README.html"}:
            tag["href"] = "index.html" if path.parent == OUT else "../index.html"
    if rel == "print.html":
        path.write_text(str(soup))
        continue
    head=soup.head
    if not head: continue
    canonical = BASE if rel == "index.html" else BASE + rel
    title_text = soup.title.get_text(" ", strip=True) if soup.title else "Mastering Blockchain Scalability"
    for selector in ['link[rel="canonical"]','meta[name="description"]','meta[property="og:title"]','meta[property="og:description"]','meta[property="og:url"]','meta[property="og:type"]','meta[name="twitter:card"]','meta[name="twitter:title"]','meta[name="twitter:description"]']:
        for old in head.select(selector): old.decompose()
    def meta(**attrs):
        tag=soup.new_tag("meta");
        for k,v in attrs.items(): tag[k.replace("_","-")]=v
        head.append(tag)
    link=soup.new_tag("link", rel="canonical", href=canonical); head.append(link)
    meta(name="description", content=DESC)
    meta(property="og:title", content=title_text)
    meta(property="og:description", content=DESC)
    meta(property="og:url", content=canonical)
    meta(property="og:type", content="book")
    meta(name="twitter:card", content="summary")
    meta(name="twitter:title", content=title_text)
    meta(name="twitter:description", content=DESC)
    if rel == "index.html":
        script=soup.new_tag("script", type="application/ld+json")
        script.string=json.dumps(book_schema, ensure_ascii=False)
        head.append(script)
    path.write_text(str(soup))
    urls.append(canonical)

(OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
entries="\n".join(f"  <url><loc>{html.escape(u)}</loc></url>" for u in urls)
(OUT/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')
print(f"enriched {len(urls)} HTML pages; wrote robots.txt and sitemap.xml")
