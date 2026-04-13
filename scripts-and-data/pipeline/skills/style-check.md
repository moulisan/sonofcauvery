# Son of Cauvery — Style Checker

Run a mechanical checklist pass on a draft chapter. Output a corrected version of the chapter plus a list of every change made.

## Input

The user pastes a draft chapter. Run every check below. Do not skip checks. Do not skim.

## Output

Two parts, in this order:

1. **Corrected chapter** — the full chapter text with all fixes applied
2. **Changes made** — a numbered list: what was changed, what rule it violated, old text → new text

If no violations found for a section, note "No issues" for that section in the changes list.

---

## CHECKLIST

### 1. Em-dashes
Find every em-dash (—). Replace with a comma, full stop, or sentence break as appropriate. No em-dashes anywhere in the chapter body.

### 2. Banned vocabulary
Scan for and remove or replace:
- utterly, spellbound, in that moment, he could not help but, rooted to the spot
- a wave of, washed over him, heart leapt, blood ran cold
- seamlessly, testament to, navigating, unbeknownst
- at once both X and Y

### 3. Numbers
- Above ten: must be numerals with commas — "30,000 men", "3 lakh soldiers", "25 years ago", "80-year-old king"
- Ten and under: must be words — "six sons", "ten days"
- "lakh" not "lakhs" as a modifier

### 4. Capitalisation
- "king", "prince", "princess", "emperor", "chief" must be lowercase unless directly preceding a name
- Correct: "Emperor Sundara Chozhan", "the emperor was ill", "Prince Karikalan", "the prince rode on", "the chief treasurer"
- "pallipadai" as part of a proper named site is capitalized: "Thirupurambiyam Pallipadai" — but italicised and lowercase when used as a standalone Tamil common noun

### 5. Tense for geographical/standing facts
- Must be present tense: "One of the rivers that inundates..." not "inundated"

### 6. Tamil words — italics
- Common nouns in prose must be italicised: mandapam, pallipadai, ambari, prasadam
- Honorifics in dialogue must be italicised: devi, amma, akka, kumara, ammamma, ammani, acharyare, manthravadi, thambi, vaishnavare, ayya
- Exception: "thatha" is NOT italicised
- Proper nouns (place names, character names) must NOT be italicised

### 7. Tamil month names
- First use of a Tamil month must have Gregorian gloss: "Aippasi (mid-October)"

### 8. Spelling
Check and correct:

| Correct | Wrong |
|---------|-------|
| Udayar | Wudaiyar |
| Boodhukan | Koodhukan |
| Pandiyan / Pandiyas | Pandyan |
| Aditya Karikalan | Adhitha Karikalan |
| Alwarkadiyan Nambi | Azhwarkadiyan |
| Kodumbalur Velar | Kodumbalur Velir |
| compliment (to praise) | complement |
| darisanam | darshanam, darsanam |
| Ayyanaar | Iyyanaar |

### 9. Oxford comma
Every list of three or more items must have an Oxford comma before the final "and" or "or".

### 10. Bold
No bold anywhere in the chapter body. Remove all `**bold**` markup.

### 11. Formatting
- Chapter heading must be: `# Book N | Chapter N | Title`
- Royal announcements must be prose narration, not block quotes

### 12. Sentence structure
- Flag any sentence over 40 words for review (do not auto-fix, just flag)
- Flag any paragraph over 6 sentences for review

### 13. Invented content check
Flag (do not auto-fix) any passage that appears to:
- Add interiority or emotion not implied by the scene
- Invent a closing hook not in the source
- Rearrange the sequence of plot beats

### 14. Narrative tense consistency
All narrative prose must be past tense. Flag any present-tense verb in narration (not in dialogue, not in geographical/standing facts covered by Check 5).
- Wrong: "He thinks that...", "She is angry", "They can sleep there"
- Correct: "He thought that...", "She was angry", "They could sleep there"

### 15. Sentence openers — wordy constructions
Flag and replace:
- "At the same time when X" → "While X"
- "At this time," → "Right then," or "Just then,"
- "At the same time," (when meaning simultaneous action) → "Meanwhile,"

### 16. "as to" before question words
Remove "as to" before question words. Always simplify.
- "Do you have any idea as to where it leads?" → "Do you have any idea where it leads?"
- "He was not sure as to what to do" → "He was not sure what to do"

### 17. "in order to" → "to"
Always replace "in order to" with plain "to".

### 18. Dialogue verbs
Do not use "hissed" for urgent whispering. Use "whispered" or "said" instead.
- Wrong: "he hissed to his companion"
- Correct: "he whispered to his companion"

### 19. Exclamation marks
Use sparingly. Default to "." in narration sentences. In dialogue, keep "!" only for genuine exclamations or commands. Flag more than 2 "!" per chapter.

### 20. Compound modifier hyphens
Number + noun compound modifiers before a noun require a hyphen.
- "1000-pillar hall", "above-mentioned", "Shanku-Chakram"
- Check for unhyphenated compound modifiers of the form [number/word]-[noun] before a noun

### 21. Redundant preamble sentences
Flag sentences that announce the topic of the immediately following sentence without adding information.
- Pattern: "They spoke about X. They got to know that [specific X detail]." — the first sentence is redundant; cut it.

---

*This checklist is maintained by the sonofcauvery-ingest-feedback skill. New rules are appended below as the editor provides corrections. After each feedback run, this file is synced to `scripts-and-data/pipeline/skills/style-check.md` in the `moulisan/sonofcauvery` GitHub repo.*
