# Son of Cauvery — Ingest Editor Feedback

Take editor corrections (pasted text, described changes, or screenshot-extracted markup), identify the pattern behind each correction, and append new rules to the Style Checker skill. Also flag regressions.

## Input

The user will provide editor feedback in one of these forms:
- Pasted before/after text
- A description of corrections ("she changed X to Y throughout")
- Extracted tracked changes from a Word doc

## What to do

For each correction:

1. **Identify the pattern.** What rule does this correction represent? Is it already covered in the Style Checker checklist? If yes, it is a regression — flag it. If no, it is a new rule.

2. **For new rules:** Formulate a concise, mechanical rule that can be checked against any chapter. Add it to the Style Checker skill file at `/Users/chandramouligopalakrishnan/.claude/skills/sonofcauvery-style-check/SKILL.md` under the appropriate checklist section (or as a new numbered section if it does not fit an existing one).

3. **For regressions:** Do not add a duplicate rule. Instead, flag it clearly: "REGRESSION — rule already exists in check [N], but was violated in [chapter]."

## Output

Two parts:

1. **Rules added** — list each new rule added, which section it was added to, and the example correction that prompted it
2. **Regressions flagged** — list any corrections that match existing rules (these indicate Skill 1 or Skill 2 is not applying rules correctly)

## How to update the Style Checker file

Edit `/Users/chandramouligopalakrishnan/.claude/skills/sonofcauvery-style-check/SKILL.md` directly using the Edit tool. Append new rules under the relevant section. If a new category is needed, add a new numbered section before the final italicised maintenance note.

Keep rules mechanical and specific. A good rule says exactly what to find and what to do. Avoid vague guidance like "improve the flow."

## After updating — sync to GitHub

After every feedback run, sync the updated style-check file to the GitHub repo mirror and commit it. Run from `/Users/chandramouligopalakrishnan/web/sonofcauvery/`:

```bash
cp ~/.claude/skills/sonofcauvery-style-check/SKILL.md scripts-and-data/pipeline/skills/style-check.md
git add scripts-and-data/pipeline/skills/style-check.md
git commit -m "Update style-check rules from editor feedback"
git push
```

This keeps a versioned history of all rule changes in GitHub alongside the published chapters.

## GitHub mirror location

`scripts-and-data/pipeline/skills/` in the `moulisan/sonofcauvery` repo. The style-check file there is the authoritative versioned record. Other skill files in that folder are reference copies — update them manually when materially changed.

## Example

Editor correction: changed "the soldiers marched complement to the cavalry" to "the soldiers marched compliment to the cavalry" — wait, that does not apply here. Better example:

Editor correction: changed "he felt a deep sense of dread" to "dread settled over him" — pattern: avoid abstract emotion statements with "he felt a [adjective] sense of". New rule: flag "he felt a [adjective] sense of" as over-stated interiority.
