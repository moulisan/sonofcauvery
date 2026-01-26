#!/usr/bin/env python3
"""
Batch update Son of Cauvery TOC and chapter pages with new design.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

HTML_DIR = Path(__file__).parent.parent / "html"

# Google Fonts link
FONTS_LINK = '''<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">'''

# Head template
HEAD_TEMPLATE = '''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <!-- Google Fonts -->
    {fonts}

    <link rel="stylesheet" href="styles.css">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-F9K2M7CC99"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-F9K2M7CC99');
    </script>
</head>'''

SITE_TITLE = '''<div class="site-title">
    <a href="index.html">Son of Cauvery - A Ponniyin Selvan Retelling in English</a>
</div>'''

FOOTER = '''<footer>
    <p>&copy; 2025 Son of Cauvery - A Ponniyin Selvan Retelling</p>
</footer>'''


def extract_title(soup):
    """Extract title from HTML."""
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()
    return "Son of Cauvery"


def extract_header_h1(soup):
    """Extract h1 from header."""
    header = soup.find('header')
    if header:
        h1 = header.find('h1')
        if h1:
            return h1.get_text().strip()
    return ""


def extract_main_content(soup):
    """Extract main content."""
    main = soup.find('main')
    if main:
        return main.decode_contents()
    return ""


def extract_toc_links(soup):
    """Extract TOC links."""
    links = []
    for a in soup.find_all('a', class_='toc-link'):
        href = a.get('href', '')
        text = a.get_text().strip()
        links.append((href, text))
    return links


def extract_nav_links(soup):
    """Extract navigation links from footer."""
    footer = soup.find('footer')
    if footer:
        nav = footer.find('div', class_='navigation-links')
        if nav:
            links = []
            for a in nav.find_all('a'):
                href = a.get('href', '')
                text = a.get_text().strip()
                links.append((href, text))
            return links
    return []


def get_book_number(filename):
    """Extract book number from filename."""
    match = re.match(r'book-(\d+)', filename)
    if match:
        return match.group(1)
    return "1"


def update_toc_page(file_path):
    """Update a TOC page."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        title = extract_title(soup)
        header_text = extract_header_h1(soup)
        toc_links = extract_toc_links(soup)
        book_num = get_book_number(file_path.name)

        # Build TOC links HTML
        toc_html = '\n'.join([
            f'            <a href="{href}" class="toc-link">{text}</a>'
            for href, text in toc_links
        ])

        new_html = f'''<!DOCTYPE html>
<html lang="en">
{HEAD_TEMPLATE.format(title=title, fonts=FONTS_LINK)}
<body>
    {SITE_TITLE}

    <header>
        <h1>{header_text}</h1>
    </header>

    <main>
{toc_html}

        <div class="navigation-links">
            <a href="index.html">Back to Home</a>
        </div>
    </main>

    {FOOTER}
</body>
</html>
'''

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        return True, None

    except Exception as e:
        return False, str(e)


def update_chapter_page(file_path):
    """Update a chapter page."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        title = extract_title(soup)
        header_text = extract_header_h1(soup)
        book_num = get_book_number(file_path.name)

        # Extract main content (paragraphs) from article if exists, otherwise from main
        article = soup.find('article')
        if article:
            paragraphs = [str(p) for p in article.find_all('p')]
        else:
            main = soup.find('main')
            paragraphs = []
            if main:
                for p in main.find_all('p'):
                    paragraphs.append(str(p))

        content_html = '\n'.join(paragraphs)

        # Generate navigation links based on book number
        nav_html = f'<a href="index.html">Back to Home</a> | \n            <a href="book-{book_num}-toc.html">Back to Book {book_num} TOC</a>'

        new_html = f'''<!DOCTYPE html>
<html lang="en">
{HEAD_TEMPLATE.format(title=title, fonts=FONTS_LINK)}
<body>
    {SITE_TITLE}

    <header>
        <h1>{header_text}</h1>
    </header>

    <main>
        <article>
{content_html}
        </article>

        <div class="navigation-links">
            {nav_html}
        </div>
    </main>

    {FOOTER}
</body>
</html>
'''

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

        return True, None

    except Exception as e:
        return False, str(e)


def main():
    """Update all TOC and chapter pages."""
    # Update TOC pages
    toc_files = list(HTML_DIR.glob('book-*-toc.html'))
    print(f"Updating {len(toc_files)} TOC pages...")

    for toc_file in sorted(toc_files):
        ok, error = update_toc_page(toc_file)
        if ok:
            print(f"  Updated {toc_file.name}")
        else:
            print(f"  Error {toc_file.name}: {error}")

    # Update chapter pages
    chapter_files = list(HTML_DIR.glob('book-*--chapter-*.html'))
    print(f"\nUpdating {len(chapter_files)} chapter pages...")

    success = 0
    errors = []

    for i, chapter_file in enumerate(sorted(chapter_files)):
        ok, error = update_chapter_page(chapter_file)
        if ok:
            success += 1
        else:
            errors.append((chapter_file.name, error))

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{len(chapter_files)}")

    print(f"\nCompleted: {success}/{len(chapter_files)} chapters updated")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, error in errors[:10]:
            print(f"  - {name}: {error}")


if __name__ == '__main__':
    main()
