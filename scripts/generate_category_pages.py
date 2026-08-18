#!/usr/bin/env python3
"""
Scans _posts/*.md front matter for `categories:` and writes one
/categories/<slug>.md page per unique category so site.categories[cat]
has somewhere to link to. Re-run any time you add a post with a new
category.

Usage:  python3 scripts/generate_category_pages.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "_posts")
OUT_DIR = os.path.join(ROOT, "categories")


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def extract_categories(text):
    m = re.search(r"^categories:\s*\[(.*?)\]", text, re.M)
    if m:
        return [c.strip().strip("'\"") for c in m.group(1).split(",") if c.strip()]
    m = re.search(r"^categories:\s*\n((?:\s*-\s*.+\n)+)", text, re.M)
    if m:
        return [re.sub(r"^\s*-\s*", "", line).strip().strip("'\"")
                for line in m.group(1).splitlines() if line.strip()]
    return []


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cats = set()
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        cats.update(extract_categories(text))

    for cat in sorted(cats):
        slug = slugify(cat)
        out_path = os.path.join(OUT_DIR, f"{slug}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(
                "---\n"
                "layout: category\n"
                f"title: {cat}\n"
                f"category: {cat}\n"
                f"permalink: /categories/{slug}/\n"
                "---\n"
            )
        print("wrote", out_path)


if __name__ == "__main__":
    main()
