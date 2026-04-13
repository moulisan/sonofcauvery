# Son of Cauvery — Publisher

Take a final approved chapter (pasted as plain text) and publish it to the GitHub Pages site. This means: create the chapter HTML file, update the book TOC, commit, and push.

## Repo location

`/Users/chandramouligopalakrishnan/web/sonofcauvery/`

All HTML files live in the `html/` subdirectory.

---

## Step 1 — Get chapter details

Ask the user (or confirm from context):
- Book number (e.g. 4)
- Chapter number (e.g. 5)
- Chapter title (e.g. "The Old Fort")
- Book name (e.g. "Manimagudam" for Book 4)

If the user pastes the chapter with a `# Book N | Chapter N | Title` heading, extract these from the heading automatically.

---

## Step 2 — Generate the filename

Pattern: `book-{N}--chapter-{M}--book-{N}---chapter-{M}---{slug}.html`

To generate the slug from the title:
- Lowercase everything
- Replace spaces with hyphens
- Remove apostrophes, commas, and other punctuation
- Example: "The Old Fort" → "the-old-fort"
- Example: "Who's That?" → "whos-that"

Full filename example for Book 4, Chapter 5, "The Old Fort":
`book-4--chapter-5--book-4---chapter-5---the-old-fort.html`

---

## Step 3 — Convert chapter text to HTML paragraphs

The chapter body is `<p>` tags only. Rules:
- Each paragraph in the source text becomes one `<p>` element
- Markdown italics `*word*` → `<em>word</em>`
- No `<strong>`, no `<h2>`, no `<blockquote>` — prose only
- Strip the `# Book N | Chapter N | Title` heading line — it goes in `<h1>` and `<title>`, not in the article body
- Preserve paragraph breaks exactly as in the source

---

## Step 4 — Write the chapter HTML file

Use this exact template. Fill in BOOK_NUM, CHAPTER_NUM, TITLE, BOOK_NAME, FILENAME_SLUG, and CHAPTER_BODY.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book BOOK_NUM | Chapter CHAPTER_NUM | TITLE</title>
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
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-F9K2M7CC99');
    </script>
</head>
<body>
    <div class="site-title">
    <a href="index.html">Son of Cauvery - A Ponniyin Selvan Retelling in English</a>
</div>

    <header>
        <h1>Book BOOK_NUM | Chapter CHAPTER_NUM | TITLE</h1>
    </header>

    <main>
        <article>
CHAPTER_BODY
        </article>

        <div class="navigation-links">
            <a href="index.html">Back to Home</a> |
            <a href="book-BOOK_NUM-toc.html">Back to Book BOOK_NUM TOC</a>
        </div>
    </main>

    <footer>
    <p>&copy; 2025 Son of Cauvery - A Ponniyin Selvan Retelling</p>
</footer>
</body>
</html>
```

Write the file to: `/Users/chandramouligopalakrishnan/web/sonofcauvery/html/{filename}`

---

## Step 5 — Update the book TOC

TOC file location: `/Users/chandramouligopalakrishnan/web/sonofcauvery/html/book-BOOK_NUM-toc.html`

Find the `<div class="toc-list">` block. Add a new `<a>` entry at the end, before the closing `</div>`:

```html
            <a href="{filename}" class="toc-link">Chapter CHAPTER_NUM: TITLE</a>
```

---

## Step 6 — Commit and push

Run from `/Users/chandramouligopalakrishnan/web/sonofcauvery/`:

```bash
git add html/{chapter-filename} html/book-BOOK_NUM-toc.html
git commit -m "Add Book BOOK_NUM Chapter CHAPTER_NUM: TITLE"
git push
```

Confirm push succeeded. Report the filename created, the TOC entry added, and the commit hash.

---

## Pipeline reference

This skill is part of the Son of Cauvery writing pipeline. All skill files and the publish script are versioned at `scripts-and-data/pipeline/` in the `moulisan/sonofcauvery` GitHub repo.

---

## What NOT to do

- Do not modify `index.html` or any other file
- Do not create new CSS or JS files
- Do not add prev/next chapter navigation (not used in this site)
- Do not update the sitemap manually (GitHub Actions handles deployment)
- Do not push if the chapter HTML already exists — ask the user to confirm overwrite
