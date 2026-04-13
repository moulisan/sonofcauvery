#!/usr/bin/env python3
"""
publish.py — Son of Cauvery chapter publisher

Converts a plain-text chapter file to HTML, writes the chapter file,
and updates the book TOC.

Usage:
    python3 publish.py chapter.txt           # generate HTML only
    python3 publish.py chapter.txt --commit  # generate + git commit + push
    cat chapter.txt | python3 publish.py     # read from stdin

The chapter file must start with a heading line of the form:
    # Book N | Chapter N | Title

Paragraphs are separated by blank lines.
Markdown italics (*word*) are converted to <em>word</em>.
"""

import sys
import os
import re
import argparse
import subprocess
import shutil

REPO = os.path.expanduser("~/web/sonofcauvery")
HTML_DIR = os.path.join(REPO, "html")

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="styles.css">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-F9K2M7CC99"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-F9K2M7CC99');
    </script>
</head>
<body>
    <div class="site-title">
    <a href="index.html">Son of Cauvery - A Ponniyin Selvan Retelling in English</a>
</div>

    <header>
        <h1>{h1}</h1>
    </header>

    <main>
        <article>
{body}
        </article>

        <div class="navigation-links">
            <a href="index.html">Back to Home</a> |
            <a href="book-{book_num}-toc.html">Back to Book {book_num} TOC</a>
        </div>
    </main>

    <footer>
    <p>&copy; 2025 Son of Cauvery - A Ponniyin Selvan Retelling</p>
</footer>
</body>
</html>"""


def slugify(title):
    slug = title.lower()
    slug = re.sub(r"['\",!?.:;]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug


def parse_heading(line):
    """Parse '# Book N | Chapter M | Title' into (book_num, chapter_num, title)."""
    m = re.match(r"#\s*Book\s+(\d+)\s*\|\s*Chapter\s+(\d+)\s*\|\s*(.+)", line.strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), m.group(3).strip()


def markdown_italics(text):
    """Convert *word* to <em>word</em>."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)


def text_to_body(text):
    """Convert blank-line-separated paragraphs to <p> tags."""
    paras = [p.strip() for p in re.split(r"\n{2,}", text.strip()) if p.strip()]
    lines = []
    for p in paras:
        p = p.replace("\n", " ")
        p = markdown_italics(p)
        lines.append(f"<p>{p}</p>")
    return "\n".join(lines)


def make_filename(book_num, chapter_num, slug):
    return f"book-{book_num}--chapter-{chapter_num}--book-{book_num}---chapter-{chapter_num}---{slug}.html"


def write_chapter_html(book_num, chapter_num, title, body_text):
    slug = slugify(title)
    fname = make_filename(book_num, chapter_num, slug)
    h1 = f"Book {book_num} | Chapter {chapter_num} | {title}"
    body = text_to_body(body_text)
    html = TEMPLATE.format(title=h1, h1=h1, body=body, book_num=book_num)
    out_path = os.path.join(HTML_DIR, fname)
    if os.path.exists(out_path):
        print(f"WARNING: {fname} already exists. Overwriting.")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {fname}")
    return fname


def update_toc(book_num, chapter_num, title, chapter_fname):
    toc_path = os.path.join(HTML_DIR, f"book-{book_num}-toc.html")
    if not os.path.exists(toc_path):
        print(f"WARNING: TOC file not found: {toc_path}")
        return
    with open(toc_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_entry = f'            <a href="{chapter_fname}" class="toc-link">Chapter {chapter_num}: {title}</a>'
    if chapter_fname in content:
        print(f"TOC entry already exists for {chapter_fname}, skipping.")
        return
    content = content.replace("        </div>", f"{new_entry}\n        </div>", 1)
    with open(toc_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"TOC updated: added Chapter {chapter_num}: {title}")
    return toc_path


def git_commit_push(files, message):
    subprocess.run(["git", "-C", REPO, "add"] + files, check=True)
    subprocess.run(["git", "-C", REPO, "commit", "-m", message], check=True)
    subprocess.run(["git", "-C", REPO, "push"], check=True)
    result = subprocess.run(
        ["git", "-C", REPO, "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True
    )
    print(f"Pushed. Commit: {result.stdout.strip()}")


def process(text, do_commit=False):
    lines = text.strip().splitlines()

    # Find heading
    heading_line = None
    heading_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            parsed = parse_heading(line)
            if parsed:
                heading_line = parsed
                heading_idx = i
                break

    if not heading_line:
        print("ERROR: No heading found. First line must be '# Book N | Chapter N | Title'")
        sys.exit(1)

    book_num, chapter_num, title = heading_line
    body_text = "\n".join(lines[heading_idx + 1:])

    chapter_fname = write_chapter_html(book_num, chapter_num, title, body_text)
    toc_fname = update_toc(book_num, chapter_num, title, chapter_fname)

    if do_commit:
        files_to_add = [f"html/{chapter_fname}"]
        if toc_fname:
            files_to_add.append(f"html/book-{book_num}-toc.html")
        git_commit_push(
            [os.path.join(REPO, f) for f in files_to_add],
            f"Add Book {book_num} Chapter {chapter_num}: {title}"
        )


def main():
    parser = argparse.ArgumentParser(description="Publish a Son of Cauvery chapter")
    parser.add_argument("file", nargs="?", help="Chapter text file (default: stdin)")
    parser.add_argument("--commit", action="store_true", help="Git commit and push after generating")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    process(text, do_commit=args.commit)


if __name__ == "__main__":
    main()
