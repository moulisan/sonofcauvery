import json
import os
import re
from bs4 import BeautifulSoup

def sanitize_filename(title):
    return re.sub(r'[^\w\-]', '-', title.lower())

def remove_images_and_captions(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    for figure in soup.find_all('figure'):
        figure.decompose()
    
    for img in soup.find_all('img'):
        img.decompose()
    
    caption_classes = ['wp-caption-text', 'caption']
    for caption in soup.find_all(class_=caption_classes):
        caption.decompose()
    
    for p in soup.find_all('p'):
        if len(p.get_text(strip=True)) == 0:
            p.decompose()
    
    return str(soup)

def create_html(title, content, book_num):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <img src="header-image.png" alt="Ponniyin Selvan Header" class="header-image">
            <h1>{title}</h1>
        </header>
        <main>
            {content}
        </main>
        <footer>
            <div class="navigation-links">
                <a href="index.html">Back to Home</a> | 
                <a href="book-{book_num}-toc.html">Back to Book {book_num} TOC</a>
            </div>
            <p>© 2024 Son Of Cauvery - A Ponniyin Selvan Retelling</p>
        </footer>
    </body>
    </html>
    """

def create_toc_page(book_num, chapters):
    content = "<ul>"
    for chapter in chapters:
        content += f'<li><a href="{chapter["filename"]}">{chapter["title"]}</a></li>'
    content += "</ul>"
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book {book_num} - Table of Contents</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <img src="header-image.png" alt="Ponniyin Selvan Header" class="header-image">
            <h1>Book {book_num} - Table of Contents</h1>
        </header>
        <main>
            {content}
        </main>
        <footer>
            <div class="navigation-links">
                <a href="index.html">Back to Home</a>
            </div>
            <p>© 2024 Son Of Cauvery - A Ponniyin Selvan Retelling</p>
        </footer>
    </body>
    </html>
    """

def create_landing_page(books):
    book_tiles = ""
    for book_num in range(1, 6):
        if book_num in books:
            book_tiles += f'<a href="book-{book_num}-toc.html" class="book-tile"><h3>Book {book_num}</h3><p>Table of Contents</p></a>'
        else:
            book_tiles += f'<div class="book-tile coming-soon"><h3>Book {book_num}</h3><p>Coming Soon</p></div>'
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Son of Cauvery - A Ponniyin Selvan Retelling</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <img src="header-image.png" alt="Ponniyin Selvan Header" class="header-image">
            <h1>Son of Cauvery - A Ponniyin Selvan Retelling</h1>
        </header>
        <main class="landing-page">
            <section class="blurb">
                <h2>About the Retelling</h2>
                <p>[Insert your blurb here]</p>
            </section>
            <section class="book-tiles">
                {book_tiles}
            </section>
        </main>
        <footer>
            <p>© 2024 Son Of Cauvery - A Ponniyin Selvan Retelling</p>
        </footer>
    </body>
    </html>
    """

def process_wordpress_json(json_file, output_dir):
    with open(json_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    books = {}
    for post in posts:
        title = post['title']['rendered']
        content = post['content']['rendered']
        
        content = remove_images_and_captions(content)
        
        match = re.match(r'Book (\d+)\s*\|\s*Chapter (\d+)', title)
        if match:
            book_num = int(match.group(1))
            chapter_num = int(match.group(2))
            
            if book_num not in books:
                books[book_num] = {}
            
            # Only process this chapter if it's not already in the book
            if chapter_num not in books[book_num]:
                filename = f"book-{book_num}--chapter-{chapter_num}--{sanitize_filename(title)}.html"
                books[book_num][chapter_num] = {"title": title, "filename": filename}
                
                html_content = create_html(title, content, book_num)
                
                with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(html_content)
    
    # Create TOC pages
    for book_num, chapters in books.items():
        sorted_chapters = [chapters[num] for num in sorted(chapters.keys())]
        toc_content = create_toc_page(book_num, sorted_chapters)
        with open(os.path.join(output_dir, f'book-{book_num}-toc.html'), 'w', encoding='utf-8') as f:
            f.write(toc_content)
    
    # Create landing page
    landing_page_content = create_landing_page(books)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(landing_page_content)

    print(f"Processed {len(posts)} posts into {sum(len(chapters) for chapters in books.values())} unique chapters across {len(books)} books.")
    print(f"Created landing page and {len(books)} table of contents pages.")

if __name__ == "__main__":
    process_wordpress_json('wordpress_content.json', 'html_output')