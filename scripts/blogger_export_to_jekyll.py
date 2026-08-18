#!/usr/bin/env python3
"""
Converts a Blogger BLOG CONTENT export (Settings > Manage Blog > Back up
Content -> an Atom XML full of <entry> posts) into Jekyll _posts/*.md files.

This is NOT the same file as the theme/template XML (theme-*.xml) - that
file only contains design, not posts. Export your actual posts separately
from Blogger's dashboard: Settings -> Manage blog -> Back up content.

Usage:
    python3 scripts/blogger_export_to_jekyll.py path/to/blog-MM-DD-YYYY.xml

Writes one file per blog post entry into _posts/, converting Blogger's
HTML post body straight through (Jekyll/kramdown renders raw HTML fine)
and mapping Blogger labels -> Jekyll categories.
"""
import sys
import os
import re
import html
from xml.etree import ElementTree as ET

NS = {
    "atom": "http://www.w3.org/2005/Atom",
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "_posts")


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src = sys.argv[1]
    tree = ET.parse(src)
    root = tree.getroot()
    os.makedirs(OUT_DIR, exist_ok=True)

    count = 0
    for entry in root.findall("atom:entry", NS):
        kinds = [c.get("term", "") for c in entry.findall("atom:category", NS)
                 if c.get("scheme", "").endswith("#kind")]
        if not any(k.endswith("#post") for k in kinds):
            continue  # skip comments, settings entries, template entries etc.

        title_el = entry.find("atom:title", NS)
        title = (title_el.text or "Untitled").strip() if title_el is not None else "Untitled"

        published_el = entry.find("atom:published", NS)
        published = published_el.text if published_el is not None else None
        if not published:
            continue
        date_str = published[:10]  # YYYY-MM-DD

        content_el = entry.find("atom:content", NS)
        body = content_el.text or "" if content_el is not None else ""

        labels = [c.get("term") for c in entry.findall("atom:category", NS)
                  if c.get("scheme", "").endswith("#label")]

        slug = slugify(title)
        filename = f"{date_str}-{slug}.md"
        out_path = os.path.join(OUT_DIR, filename)

        front = "---\n"
        front += f"title: {title!r}\n".replace("'", '"')
        if labels:
            front += "categories: [" + ", ".join(f'"{l}"' for l in labels) + "]\n"
        front += "---\n\n"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(front)
            f.write(body)

        count += 1
        print("wrote", out_path)

    print(f"\nConverted {count} posts into {OUT_DIR}/")
    print("Run scripts/generate_category_pages.py next to build category pages.")


if __name__ == "__main__":
    main()
