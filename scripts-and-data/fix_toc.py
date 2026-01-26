#!/usr/bin/env python3
"""
Regenerate TOC pages for Son of Cauvery with proper chapter links.
"""

import os
import re
from pathlib import Path

HTML_DIR = Path(__file__).parent.parent / "html"

# Google Fonts link
FONTS_LINK = '''<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">'''

BOOK_TITLES = {
    "1": "New Floods",
    "2": "The Cyclone",
    "3": "The Sword of Sacrifice",
    "4": "Manimagudam",
    "5": "The Dawn"
}

def extract_chapter_info(filename):
    """Extract chapter number and title from filename."""
    # Pattern: book-X--chapter-Y--book-X---chapter-Y---title.html
    match = re.match(r'book-(\d+)--chapter-(\d+)--book-\d+---chapter-\d+---(.+)\.html', filename)
    if match:
        book_num = match.group(1)
        chapter_num = int(match.group(2))
        title_slug = match.group(3)
        # Convert slug to title
        title = title_slug.replace('-', ' ').title()
        return book_num, chapter_num, title
    return None, None, None


def generate_toc_page(book_num, chapters):
    """Generate TOC HTML for a book."""
    book_title = BOOK_TITLES.get(book_num, f"Book {book_num}")

    # Sort chapters by number
    chapters.sort(key=lambda x: x[0])

    # Build TOC links HTML
    toc_links = []
    for chapter_num, filename, title in chapters:
        toc_links.append(f'            <a href="{filename}" class="toc-link">Chapter {chapter_num}: {title}</a>')
    toc_html = '\n'.join(toc_links)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book {book_num}: {book_title} - Son of Cauvery</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <!-- Google Fonts -->
    {FONTS_LINK}

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
        <h1>Book {book_num}: {book_title}</h1>
    </header>

    <main>
{toc_html}

        <div class="navigation-links">
            <a href="index.html">Back to Home</a>
        </div>
    </main>

    <footer>
    <p>&copy; 2025 Son of Cauvery - A Ponniyin Selvan Retelling</p>
</footer>
</body>
</html>
'''
    return html


def main():
    """Regenerate all TOC pages."""
    # Find all chapter files and group by book
    books = {}

    for filepath in HTML_DIR.glob('book-*--chapter-*.html'):
        book_num, chapter_num, title = extract_chapter_info(filepath.name)
        if book_num and chapter_num:
            if book_num not in books:
                books[book_num] = []
            books[book_num].append((chapter_num, filepath.name, title))

    # Generate TOC for each book
    for book_num in sorted(books.keys()):
        chapters = books[book_num]
        toc_html = generate_toc_page(book_num, chapters)

        toc_file = HTML_DIR / f"book-{book_num}-toc.html"
        with open(toc_file, 'w', encoding='utf-8') as f:
            f.write(toc_html)

        print(f"Generated {toc_file.name} with {len(chapters)} chapters")


if __name__ == '__main__':
    main()
