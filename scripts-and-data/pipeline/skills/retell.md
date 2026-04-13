# Son of Cauvery — Reteller

Take a pasted English translation of a Kalki chapter and produce a Mouli-style abridgement ready for the style-check pass.

## What this is

Abridgement, not creative rewriting. Stay close to Kalki's original sequence. Retain every plot beat in original order. Cut ornament, repetition, and padding. Do not invent scenes, add interiority not in the source, rearrange beats, or add closing hooks not in the original.

## Input

The user will paste a full English translation of a Kalki chapter. They may also specify the book number, chapter number, and chapter title. If not specified, ask before proceeding.

## Output

A complete abridged chapter in Mouli's style, ready for style-check. Format the heading as:
`# Book N | Chapter N | Title`

No other metadata. No preamble. Just the heading and the chapter body.

---

## Abridgement rules

**Keep:**
- Every plot beat, in original order
- Long speeches when plot-critical (e.g. a character recounting a battle, delivering key information, making an argument that drives the story)
- The crowd gossip device: bystanders deliver exposition through whispered dialogue — preserve this, it is a structural feature
- Vandhiyathevan's interior monologue — freely used, it is his character
- Light banter between characters (Karikalan and Kandanmaran, Vandhiyathevan and Nambi)
- Key revelations given full weight, not compressed

**Cut:**
- Ornamental descriptions (lengthy nature descriptions, repetitive similes)
- Devotional tangents — keep a brief identifier ("Saint Appar received salvation here") but cut elaborate hagiographic passages
- Kalki's chapter-opening recaps of prior events
- Repetitive dialogue exchanges where one pass captures the point
- Filler transitions that add no information

**Chapter length:** 400–700 words typical; 900+ acceptable for plot-heavy chapters. Do not pad to hit a minimum. Do not compress a plot-heavy chapter to hit a maximum.

**Chapter end:** End exactly where Kalki ends the chapter. No invented hooks, no closing summary sentences.

---

## Voice and sentence style

- Short to medium sentences, active voice
- Tight paragraphs, 2–5 sentences
- Dialogue punchy and direct — no elaborate speech introductions ("he said, clearing his throat and looking gravely at the assembled men")
- Plain and direct vocabulary — no literary or archaic words unless Mouli uses them deliberately

---

## Vocabulary — banned phrases

Never use these:
- utterly, spellbound, in that moment, he could not help but, rooted to the spot
- a wave of, washed over him, heart leapt, blood ran cold
- seamlessly, testament to, navigating, unbeknownst
- at once both X and Y

---

## Numbers

- Above ten: numerals with commas — "30,000 men", "3 lakh infantrymen", "25 years ago", "80-year-old king"
- Ten and under: words — "six sons", "ten days", "three or four years"
- "lakh" not "lakhs" as a modifier — "3 lakh soldiers"

---

## Capitalisation

- "king", "prince", "emperor" lowercase unless directly before a name
- "Emperor Sundara Chozhan" but "the emperor was ill"
- "Prince Karikalan" but "the prince rode on"

---

## Tense

- Present tense for geographical and standing facts: "One of the rivers that inundates the lands of Thirumunaipadi is Kedilam" — not "inundated"

---

## Tamil words and names

**Proper nouns (places, temples, character names):** plain, no italics.

**Common nouns in prose:** italicised — *mandapam*, *pallipadai*, *ambari*, *prasadam*

**Month names:** Tamil month with Gregorian gloss on first use — "Aippasi (mid-October)"

**Honorifics in dialogue:** italicised — *devi*, *amma*, *akka*, *kumara*, *ammamma*, *ammani*, *acharyare*, *manthravadi*, *thambi*, *vaishnavare*, *ayya*

**Exception — thatha:** not italicised.

---

## Spelling (exact, confirmed)

| Use | Not |
|-----|-----|
| Udayar | Wudaiyar |
| Boodhukan | Koodhukan |
| Pandiyan / Pandiyas | Pandyan |
| Aditya Karikalan | Adhitha Karikalan |
| Alwarkadiyan Nambi | Azhwarkadiyan |
| Kodumbalur Velar | Kodumbalur Velir |
| compliment (to praise) | complement |

Oxford comma throughout.

---

## Formatting

- Chapter heading: `# Book N | Chapter N | Title`
- Royal announcements: described in prose narration, not block-quoted
- No bold anywhere in chapter body
- No em-dashes anywhere — use commas, full stops, or sentence breaks instead

---

## Plot accuracy note

Malaiyaman's argument: "Going to Kadambur now gets the Pazhuvettarayars on your side" — the Pazhuvettarayars come onto Karikalan's side, not the other way around. Do not reverse this.

---

## Pipeline reference

This skill is part of the Son of Cauvery writing pipeline. All skill files and the publish script are versioned at `scripts-and-data/pipeline/` in the `moulisan/sonofcauvery` GitHub repo.

---

## Character name reference

| Full name | Short form |
|-----------|------------|
| Aditya Karikalan | Karikalan |
| Arulmozhi Varman | Ponniyin Selvan |
| Alwarkadiyan Nambi | Nambi |
| Kodumbalur Velar | — |
| Vandhiyathevan | Vandhiyathevan |
