#!/usr/bin/env python3
"""Build the 7x10in print interior PDF (KDP paperback) from the mdBook HTML output.

Reuses the rendered chapter HTML in book/, adds book front matter (title page,
copyright, TOC with resolved page numbers), a generated index, and print CSS.
Requires: beautifulsoup4, weasyprint, pymupdf (see requirements-pdf.txt).
"""
import re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
OUTDIR = ROOT / "print"
OUT = OUTDIR / "blockchain-scalability-book-interior-7x10.pdf"
CSS = ROOT / "theme" / "print-7x10.css"
SITE = "https://neilydhan.github.io/Blockchain-Scalability-Book/"

# (slug, built HTML path relative to book/, part)
SECTIONS = [
    ("preface",   "chapters/00_preface.html", "front"),
    ("ch01", "chapters/01_introduction.html", "core"),
    ("ch02", "chapters/02_blockchain_trilemma.html", "core"),
    ("ch03", "chapters/03_layer_1_vs_layer_2.html", "core"),
    ("ch04", "chapters/04_layer_1_on_chain_scalability.html", "core"),
    ("ch05", "chapters/05_layer_2_off_chain_scalability.html", "core"),
    ("ch06", "chapters/06_rollups.html", "core"),
    ("ch07", "chapters/07_modular_vs_monolithic.html", "core"),
    ("ch08", "chapters/08_data_availability_scaling.html", "core"),
    ("ch09", "chapters/09_parallel_execution.html", "core"),
    ("ch10", "chapters/10_consensus_scaling.html", "core"),
    ("ch11", "chapters/11_future_directions.html", "core"),
    ("glossary",   "chapters/12_glossary.html", "ref"),
    ("review",     "chapters/13_review_questions.html", "ref"),
    ("handbook",   "chapters/14_evaluation_handbook.html", "ref"),
    ("credits",    "chapters/15_figure_credits.html", "ref"),
    ("worksheets", "chapters/16_threat_model_worksheets.html", "ref"),
    ("template",   "chapters/17_benchmark_reporting_template.html", "ref"),
]
PAGE2SLUG = {p: s for s, p, _ in SECTIONS}
PAGE2SLUG.update({p.split("/")[-1]: s for s, p, _ in SECTIONS})

CURATED = [
    "Arbitrum", "Optimism", "ZKsync", "Starknet", "Scroll", "Solana", "Sui",
    "Aptos", "NEAR Protocol", "Cosmos", "Polygon", "Celestia", "EigenDA",
    "Avail", "Bitcoin", "Ethereum", "Lightning Network", "Plasma", "Block-STM",
    "HotStuff", "Sync HotStuff", "Narwhal", "Mysticeti", "CometBFT", "Gasper",
    "Nightshade", "BoLD", "MEV-Boost", "EIP-4844", "PeerDAS", "EIP-7594",
    "ERC-4337", "Blobstream", "danksharding", "BLOCKBENCH", "L2BEAT", "OP Stack",
    "watchtower", "fraud proof", "validity proof", "zero-knowledge proof",
    "data availability sampling", "erasure coding", "state channel",
    "optimistic rollup", "ZK rollup", "sequencer", "sharding", "finality",
    "account abstraction", "shared sequencing", "Verkle tree",
]
SKIP_PARENTS = {"pre", "code", "script", "style", "a"}

def load_section(slug, rel):
    soup = BeautifulSoup((BOOK / rel).read_text(encoding="utf-8"), "html.parser")
    content = soup.select_one("#content")
    if content is None:
        raise SystemExit(f"error: no #content in {rel}")
    # Namespace every id and same-page anchor to avoid collisions across sections.
    for tag in content.find_all(id=True):
        tag["id"] = f"{slug}--{tag['id']}"
    for a in content.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#"):
            a["href"] = f"#{slug}--{href[1:]}"
        elif href.endswith(".html") or ".html#" in href:
            page, _, frag = href.partition("#")
            target = PAGE2SLUG.get(page) or PAGE2SLUG.get(page.split("/")[-1])
            if target:
                a["href"] = f"#{target}--{frag}" if frag else f"#sec-{target}"
            else:
                a["href"] = SITE + page.split("/")[-1] + (("#" + frag) if frag else "")
    for a in content.select("a.header"):
        a.unwrap()
    for img in content.find_all("img", src=True):
        img["src"] = img["src"].lstrip("./").removeprefix("../")
    return content

def first_text_occurrence(root_tag, pattern):
    """Insert an anchor span before the first regex match in normal text."""
    for node in root_tag.find_all(string=True):
        if not isinstance(node, NavigableString):
            continue
        if any(p.name in SKIP_PARENTS or "footnote-definition" in (p.get("class") or [])
               for p in node.parents if isinstance(p, Tag)):
            continue
        m = pattern.search(str(node))
        if m:
            text = str(node)
            before_txt, after_txt = text[: m.start()], text[m.start():]
            span = Tag(name="span")
            span["class"] = "idx"
            before = NavigableString(before_txt)
            node.replace_with(before)
            before.insert_after(span)
            span.insert_after(NavigableString(after_txt))
            return span
    return None

def build():
    if not (BOOK / "index.html").exists():
        subprocess.run(["bash", str(ROOT / "scripts" / "build-book.sh")], check=True, cwd=ROOT)

    sections = {}
    titles = {}
    for slug, rel, part in SECTIONS:
        content = load_section(slug, rel)
        h1 = content.find("h1")
        titles[slug] = h1.get_text(strip=True) if h1 else slug
        sections[slug] = (content, part)

    # Glossary terms: bold standalone paragraphs in the glossary section.
    glossary, _ = sections["glossary"]
    terms = {}
    for st in glossary.find_all("strong"):
        if st.parent.name == "p" and st.parent.get_text(strip=True) == st.get_text(strip=True):
            t = st.get_text(strip=True).rstrip(".")
            if 2 < len(t) < 60:
                terms[t.lower()] = t
    for c in CURATED:
        terms.setdefault(c.lower(), c)
    pats = {}
    for key, label in sorted(terms.items(), key=lambda kv: -len(kv[0])):
        flags = 0 if key in {c.lower() for c in CURATED} and key == label.lower() and any(ch.isupper() for ch in label) else re.IGNORECASE
        pats[key] = (label, re.compile(r"(?<![\w-])" + re.escape(label) + r"(?![\w-])", flags))

    # Index: first occurrence per section per term; glossary definitions marked.
    index = {}  # key -> {"label": str, "refs": [(slug, anchor)], "def": anchor|None}
    n_anchor = 0
    for slug, rel, part in SECTIONS:
        content, _ = sections[slug]
        for key, (label, pat) in pats.items():
            span = first_text_occurrence(content, pat)
            if span is not None:
                n_anchor += 1
                aid = f"idx-{n_anchor}"
                span["id"] = aid
                entry = index.setdefault(key, {"label": label, "refs": [], "def": None})
                entry["refs"].append((slug, aid))
    # Glossary definitions join the ref list in section order, flagged as bold.
    order = {slug: i for i, (slug, _, _) in enumerate(SECTIONS)}
    for st in glossary.find_all("strong"):
        t = st.get_text(strip=True).rstrip(".").lower()
        if t in index:
            n_anchor += 1
            aid = f"idx-{n_anchor}"
            span = BeautifulSoup(f"<span class='idx' id='{aid}'></span>", "html.parser").span
            st.insert_before(span)
            entry = index[t]
            entry["refs"] = [(s, a) for s, a in entry["refs"] if s != "glossary"]
            entry["refs"].append(("glossary", aid))
            entry["refs"].sort(key=lambda sa: order[sa[0]])
            entry["def"] = aid

    # Assemble document.
    doc = BeautifulSoup("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>Mastering Blockchain Scalability - Print Interior</title></head><body></body></html>", "html.parser")
    body = doc.body

    body.append(BeautifulSoup("""
<div class="tp titlepage">
  <div class="t">Mastering Blockchain Scalability</div>
  <div class="st">A mechanism-first guide to blockchain scalability, security, trust, and recovery</div>
  <div class="au">Neil Han</div>
  <div class="ed">Version 1.1.1 &middot; Print Edition Candidate</div>
</div>""", "html.parser"))

    body.append(BeautifulSoup("""
<div class="fm copyright">
  <p class="spacer"></p>
  <p><b>Mastering Blockchain Scalability</b><br>Version 1.1.1, print edition candidate</p>
  <p>&copy; 2026 Neil Han. Book prose, exercises, tables, and original figures are licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/). Build software under scripts/, theme/, and .github/ is licensed under the MIT License. Third-party quotations, trademarks, and credited materials retain their respective rights. Figure sources and credits appear in the Figure Credits chapter.</p>
  <p>Free digital editions (web, PDF, EPUB): https://github.com/neilydhan/Blockchain-Scalability-Book/releases</p>
  <p>Independently published. Print ISBN: to be assigned through Amazon KDP.</p>
  <p>10 9 8 7 6 5 4 3 2 1</p>
  <p>This book is educational material, not financial, legal, or investment advice. Protocol details change; every time-sensitive claim carries a source and a date, and readers should verify the current specification.</p>
  <p>Cite this edition: Han, Neil. <i>Mastering Blockchain Scalability</i>. Version 1.1.1, 2026.</p>
</div>""", "html.parser"))

    # TOC
    toc = BeautifulSoup("<div class='fm toc'><h1>Contents</h1></div>", "html.parser")
    toc_div = toc.div
    part_labels = {"front": None, "core": "Core Chapters", "ref": "Reference and Practice"}
    seen_parts = set()
    for slug, rel, part in SECTIONS:
        if part_labels[part] and part not in seen_parts:
            seen_parts.add(part)
            p = doc.new_tag("p", attrs={"class": "part"})
            p.string = part_labels[part]
            toc_div.append(p)
        content, _ = sections[slug]
        h1 = content.find("h1")
        if h1:
            p = doc.new_tag("p", attrs={"class": "t1"})
            a = doc.new_tag("a", href=f"#{h1['id']}")
            a.string = h1.get_text(strip=True)
            p.append(a)
            toc_div.append(p)
        for h2 in content.find_all("h2"):
            p = doc.new_tag("p", attrs={"class": "t2"})
            a = doc.new_tag("a", href=f"#{h2['id']}")
            a.string = h2.get_text(strip=True)
            p.append(a)
            toc_div.append(p)
    body.append(toc_div)

    for slug, rel, part in SECTIONS:
        content, _ = sections[slug]
        sec = doc.new_tag("section", attrs={"class": "chapter", "id": f"sec-{slug}"})
        for child in list(content.children):
            sec.append(child.extract() if isinstance(child, Tag) else child)
        body.append(sec)

    # Index
    idx = BeautifulSoup("<div class='index'><h1>Index</h1></div>", "html.parser")
    idx_div = idx.div
    letter = None
    MAXREFS = 10
    for key in sorted(index):
        entry = index[key]
        refs = entry["refs"][:MAXREFS]
        if not refs and not entry["def"]:
            continue
        first = entry["label"][0].upper()
        if first != letter:
            letter = first
            h = doc.new_tag("h2"); h.string = letter; idx_div.append(h)
        p = doc.new_tag("p")
        p.append(entry["label"] + " ")
        links = []
        for s, a in refs:
            cls = " class='def'" if a == entry["def"] else ""
            links.append(f"<a{cls} href='#{a}'></a>")
        p.append(BeautifulSoup(", ".join(links), "html.parser"))
        idx_div.append(p)
    body.append(idx_div)

    OUTDIR.mkdir(exist_ok=True)

    # WeasyPrint mis-renders some styled SVGs; rasterize all figures with cairosvg.
    import cairosvg
    raster_dir = BOOK / "raster"
    raster_dir.mkdir(exist_ok=True)
    for img in doc.find_all("img", src=True):
        src_attr = img["src"]
        if src_attr.lower().endswith(".svg"):
            svg_path = BOOK / src_attr
            png_name = src_attr.replace("/", "_")[:-4] + ".png"
            cairosvg.svg2png(url=str(svg_path),
                             write_to=str(raster_dir / png_name),
                             output_width=2400)
            img["src"] = f"raster/{png_name}"

    html_path = OUTDIR / "print-7x10.html"
    html_path.write_text(str(doc), encoding="utf-8")

    from weasyprint import HTML
    HTML(filename=str(html_path), base_url=str(BOOK) + "/").write_pdf(
        str(OUT), stylesheets=[str(CSS)])
    print(f"print interior: {OUT}")

    import fitz
    d = fitz.open(str(OUT))
    sizes = {(round(p.rect.width, 1), round(p.rect.height, 1)) for p in d}
    fonts = set()
    for pno in range(min(len(d), 50)):
        for f in d.get_page_fonts(pno):
            fonts.add(f[3])
    blanks = [i + 1 for i in range(len(d)) if len(d[i].get_text().strip()) == 0 and not d[i].get_images()]
    print(f"pages: {len(d)}; sizes(pt): {sizes}; blank pages: {blanks[:10]}")
    print(f"fonts (first 50 pages): {sorted(fonts)}")
    print(f"index entries: {sum(1 for k in index if index[k]['refs'] or index[k]['def'])}; anchors: {n_anchor}")

if __name__ == "__main__":
    build()
