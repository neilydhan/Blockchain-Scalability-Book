#!/usr/bin/env python3
"""Build book front matter, a paginated print TOC, page labels, and PDF outline."""
import argparse, json, re
from pathlib import Path
from bs4 import BeautifulSoup

TOC_ID = "pdf-table-of-contents"
HEADING_PREFIX = "pdf-heading-"
CHAPTER_ONE = "Chapter 1:"


def clean_main(soup):
    main = soup.find("main")
    if main is None:
        raise SystemExit("error: print.html has no <main>")
    first = next((h for h in main.find_all("h1") if h.get_text(" ", strip=True).startswith(CHAPTER_ONE)), None)
    if first is None:
        raise SystemExit("error: could not find Chapter 1 in print.html")
    # The PDF has purpose-built front matter. Remove the web landing page and
    # preface so Chapter 1 follows the contents, as in a conventional book.
    for node in list(main.contents):
        if node is first:
            break
        node.extract()
    return main


def make_front_matter(soup, version):
    cover = soup.new_tag("section", attrs={"class": "pdf-front-page pdf-cover"})
    h = soup.new_tag("h1"); h.string = "Mastering Blockchain Scalability"; cover.append(h)
    sub = soup.new_tag("p"); sub.string = "Mechanisms, Trade-offs, and Engineering Practice"; cover.append(sub)

    title = soup.new_tag("section", attrs={"class": "pdf-front-page pdf-title-page"})
    h = soup.new_tag("h1"); h.string = "Mastering Blockchain Scalability"; title.append(h)
    p = soup.new_tag("p"); p.string = "A systems guide to scaling execution, data availability, settlement, and consensus"; title.append(p)
    p = soup.new_tag("p", attrs={"class": "pdf-author"}); p.string = "Neil Han"; title.append(p)

    copyright_page = soup.new_tag("section", attrs={"class": "pdf-front-page pdf-copyright-page"})
    h = soup.new_tag("h1"); h.string = "Copyright"; copyright_page.append(h)
    for text in (
        "Copyright © 2024 Mastering Blockchain Scalability Contributors.",
        f"Version {version}.",
        "Licensed under the MIT License.",
        "This book is provided without warranty. Protocols and roadmaps change; readers should verify current implementation and security details against primary sources.",
    ):
        p = soup.new_tag("p"); p.string = text; copyright_page.append(p)
    return cover, title, copyright_page


def content_headings(main):
    return list(main.find_all(["h1", "h2", "h3"]))


def prepare(html_path, map_path, version):
    soup = BeautifulSoup(html_path.read_text(), "html.parser")
    main = clean_main(soup)
    records = []
    for number, h in enumerate(content_headings(main), 1):
        title = h.get_text(" ", strip=True)
        anchor = f"{HEADING_PREFIX}{number:04d}"
        h["id"] = anchor
        header_link = h.find("a", class_="header", recursive=False)
        if header_link:
            header_link["href"] = f"#{anchor}"
        records.append({"level": int(h.name[1]), "title": title, "anchor": anchor})

    toc = soup.new_tag("section", id=TOC_ID)
    h = soup.new_tag("h1"); h.string = "Contents"; toc.append(h)
    listing = soup.new_tag("ol", attrs={"class": "pdf-toc-list"})
    for i, record in enumerate(records):
        if record["level"] > 2:
            continue
        item = soup.new_tag("li", attrs={"class": f"pdf-toc-level-{record['level']}"})
        link = soup.new_tag("a", href=f"#{record['anchor']}")
        title = soup.new_tag("span", attrs={"class": "pdf-toc-title"}); title.string = record["title"]
        page = soup.new_tag("span", attrs={"class": "pdf-toc-page", "data-toc-index": str(i)}); page.string = "0000"
        link.extend([title, page]); item.append(link); listing.append(item)
    toc.append(listing)
    cover, title, copyright_page = make_front_matter(soup, version)
    main.insert(0, toc); main.insert(0, copyright_page); main.insert(0, title); main.insert(0, cover)
    html_path.write_text(str(soup))
    map_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")


def physical_pages(pdf_path, records):
    import fitz
    doc = fitz.open(pdf_path); names = doc.resolve_names(); pages = []
    for record in records:
        destination = names.get(record["anchor"])
        if not destination or destination.get("page", -1) < 0:
            raise SystemExit(f"error: could not resolve PDF destination {record['anchor']}")
        pages.append(destination["page"] + 1)
    return pages


def arabic_pages(pdf_path, records):
    physical = physical_pages(pdf_path, records)
    chapter_one_page = physical[0]
    return [page - chapter_one_page + 1 for page in physical]


def fill(html_path, map_path, pdf_path):
    records = json.loads(map_path.read_text()); pages = arabic_pages(pdf_path, records)
    soup = BeautifulSoup(html_path.read_text(), "html.parser")
    nodes = soup.select(f"#{TOC_ID} .pdf-toc-page")
    printed = [(i, r) for i, r in enumerate(records) if r["level"] <= 2]
    if len(nodes) != len(printed):
        raise SystemExit("error: printed TOC HTML no longer matches heading map")
    for node, (index, _record) in zip(nodes, printed):
        node.string = str(pages[index])
    html_path.write_text(str(soup)); return len(printed)


def roman(number):
    values = [(1000,"m"),(900,"cm"),(500,"d"),(400,"cd"),(100,"c"),(90,"xc"),(50,"l"),(40,"xl"),(10,"x"),(9,"ix"),(5,"v"),(4,"iv"),(1,"i")]
    out = ""
    for value, token in values:
        while number >= value: out += token; number -= value
    return out


def paginate(pdf_path, map_path):
    import fitz
    from pypdf import PdfReader, PdfWriter
    records = json.loads(map_path.read_text()); physical = physical_pages(pdf_path, records)
    first_main = physical[0]
    doc = fitz.open(pdf_path)
    for index, page in enumerate(doc):
        physical_number = index + 1
        if physical_number == 1:  # Cover has no running matter.
            continue
        if physical_number < first_main:
            label = roman(physical_number - 1)
            header = "Mastering Blockchain Scalability · Front Matter"
        else:
            label = str(physical_number - first_main + 1)
            # The latest h1 at or before this page provides a stable running head.
            chapters = [r["title"] for r, p in zip(records, physical) if r["level"] == 1 and p <= physical_number]
            header = chapters[-1] if chapters else "Mastering Blockchain Scalability"
        page.insert_text((54, 24), header, fontsize=8, color=(0.35, 0.35, 0.35))
        width = page.rect.width
        page.insert_text((width / 2 - len(label) * 2, page.rect.height - 18), label, fontsize=9, color=(0.25, 0.25, 0.25))
    stamped = pdf_path.with_suffix(".stamped.pdf"); doc.save(stamped); doc.close()

    reader = PdfReader(str(stamped)); writer = PdfWriter(clone_from=reader)
    # PDF viewer labels: cover has a deliberately blank label, title starts
    # roman i, and Chapter 1 restarts at arabic 1.
    writer.set_page_label(0, 0, prefix=" ", start=1)
    writer.set_page_label(1, first_main - 2, style="/r", start=1)
    writer.set_page_label(first_main - 1, len(reader.pages) - 1, style="/D", start=1)
    with pdf_path.open("wb") as f: writer.write(f)
    stamped.unlink()
    return first_main


def outline(pdf_path, map_path):
    from pypdf import PdfReader, PdfWriter
    records = json.loads(map_path.read_text()); pages = physical_pages(pdf_path, records)
    reader = PdfReader(str(pdf_path)); writer = PdfWriter(clone_from=reader); parents = {}
    for record, page in zip(records, pages):
        level = record["level"]; parent = parents.get(level - 1)
        parents[level] = writer.add_outline_item(record["title"], page - 1, parent=parent)
        for deeper in list(parents):
            if deeper > level: del parents[deeper]
    tmp = pdf_path.with_suffix(".outlined.pdf")
    with tmp.open("wb") as f: writer.write(f)
    tmp.replace(pdf_path); return len(records)


def verify(pdf_path, map_path):
    import fitz
    from pypdf import PdfReader
    records = json.loads(map_path.read_text()); physical = physical_pages(pdf_path, records)
    arabic = arabic_pages(pdf_path, records); doc = fitz.open(pdf_path); toc = doc.get_toc(simple=True)
    expected = [[r["level"], r["title"], page] for r, page in zip(records, physical)]
    if toc != expected: raise SystemExit("error: PDF outline hierarchy or destinations are wrong")
    printed = [r for r in records if r["level"] <= 2]; seen = 0; mismatches = []
    expected_printed = [p for r, p in zip(records, arabic) if r["level"] <= 2]
    for page_number, page in enumerate(doc, 1):
        links = [x for x in page.get_links() if x.get("nameddest", "").startswith(HEADING_PREFIX)]
        words = page.get_text("words")
        for link in sorted(links, key=lambda x: (x["from"].y0, x["from"].x0)):
            if seen == len(printed): break
            middle = (link["from"].y0 + link["from"].y1) / 2
            row = [w for w in words if abs((w[1] + w[3]) / 2 - middle) < 4]
            numbers = [int(w[4]) for w in row if re.fullmatch(r"[0-9]+", w[4])]
            visible = numbers[-1] if numbers else None
            if visible != expected_printed[seen]: mismatches.append((page_number, visible, expected_printed[seen]))
            seen += 1
        if seen == len(printed): break
    labels = PdfReader(str(pdf_path)).page_labels
    first_main = physical[0]
    if labels[0].strip() != "" or labels[1] != "i" or labels[first_main-2] != roman(first_main-2) or labels[first_main-1] != "1":
        raise SystemExit("error: PDF page labels do not follow cover/roman/arabic scheme")
    if seen != len(printed) or mismatches:
        raise SystemExit(f"error: TOC validation failed: {seen} rows, {len(mismatches)} mismatches")
    print(f"Verified {seen} printed TOC rows, {len(toc)} outline entries, and roman/arabic page labels")


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="command", required=True)
    for name in ("prepare", "fill", "paginate", "outline", "verify"):
        p = sub.add_parser(name); p.add_argument("--map", type=Path, required=True)
        p.add_argument("--html", type=Path, required=name in ("prepare", "fill"))
        p.add_argument("--pdf", type=Path, required=name not in ("prepare",))
        if name == "prepare": p.add_argument("--version", required=True)
    args = ap.parse_args()
    if args.command == "prepare": prepare(args.html, args.map, args.version)
    elif args.command == "fill": print(f"Resolved {fill(args.html, args.map, args.pdf)} printed TOC page numbers")
    elif args.command == "paginate": print(f"Applied running matter and page labels; Chapter 1 begins on physical page {paginate(args.pdf, args.map)}")
    elif args.command == "outline": print(f"Added {outline(args.pdf, args.map)} PDF outline entries")
    else: verify(args.pdf, args.map)

if __name__ == "__main__": main()
