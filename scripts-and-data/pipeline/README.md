# Son of Cauvery — Writing Pipeline

This directory contains the tooling for the Son of Cauvery chapter pipeline: four Claude Code skills and a Python publishing script.

---

## The Four Skills

These are Claude Code skills stored locally at `~/.claude/skills/`. The `skills/` subfolder here is the GitHub mirror — it is kept in sync automatically after every editor-feedback run.

| Skill | Invoke as | Does |
|-------|-----------|------|
| `sonofcauvery-retell` | `/sonofcauvery-retell` | Takes a pasted English translation of a Kalki chapter and produces a Mouli-style abridgement |
| `sonofcauvery-style-check` | `/sonofcauvery-style-check` | Runs a mechanical checklist pass on a draft chapter; outputs corrected chapter + change list |
| `sonofcauvery-ingest-feedback` | `/sonofcauvery-ingest-feedback` | Takes editor corrections, identifies patterns, appends new rules to the style-check skill, and syncs to GitHub |
| `sonofcauvery-publish` | `/sonofcauvery-publish` | Takes final approved chapter text, generates HTML, updates TOC, commits and pushes |

---

## Chapter workflow

```
Kalki translation (pasted)
        ↓
   /sonofcauvery-retell
        ↓
   Draft chapter
        ↓
   /sonofcauvery-style-check
        ↓
   Corrected chapter + change list
        ↓
   Editor review (Word doc with tracked changes)
        ↓
   /sonofcauvery-ingest-feedback  ──→  updates style-check skill (local + GitHub)
        ↓
   Accepted final text (copy-pasted)
        ↓
   /sonofcauvery-publish
        ↓
   Live on sonofcauverybook.in
```

---

## publish.py

`publish.py` is the Python script that converts chapter text to HTML and writes the chapter file. It is invoked by the `sonofcauvery-publish` skill but can also be run directly.

**Usage:**

```bash
# Convert a single chapter file
python3 publish.py chapter.txt

# Read from stdin
cat chapter.txt | python3 publish.py

# Generate + commit + push in one step
python3 publish.py chapter.txt --commit
```

The chapter file must start with a heading line of the form:
```
# Book N | Chapter N | Title
```

The script will:
1. Generate `html/book-N--chapter-M--book-N---chapter-M---{slug}.html`
2. Update `html/book-N-toc.html`
3. Optionally commit and push if `--commit` is passed

---

## Style rules

The full style checklist is in `skills/style-check.md`. This file is the versioned record of all rules accumulated from editor feedback. It is updated automatically by the `sonofcauvery-ingest-feedback` skill after every feedback session.

Key rule categories:
- Voice and abridgement philosophy
- Sentence structure and vocabulary
- Numbers, capitalisation, tense
- Tamil words, honorifics, spelling
- Checks 14–21: rules added from Book 4 Chapters 4–10 editor feedback (April 2026)

---

## Source of truth

- **Live working copies of skills:** `~/.claude/skills/sonofcauvery-*/SKILL.md`
- **GitHub mirror (version-controlled):** `scripts-and-data/pipeline/skills/*.md`
- The `sonofcauvery-ingest-feedback` skill syncs the style-check file to GitHub after every feedback run. Other skill files should be manually copied here when materially updated.
