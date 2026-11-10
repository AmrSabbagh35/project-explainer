---
name: /explain
description: شرح المشاريع بالعربية. A lettered mechanical plate for any codebase, in Arabic, right to left.
colors:
  key: "#EE6A4C"
  key-light: "#C2391F"
  on-key: "#0B1222"
  on-key-light: "#FFFFFF"
  gilt: "#C29A4F"
  gilt-light: "#8E6A28"
  gilt-soft: "rgba(194, 154, 79, .32)"
  gilt-soft-light: "rgba(142, 106, 40, .30)"
  mast-gilt: "#D2AC63"
  mast-gilt-light: "#E0BE7A"
  lapis: "#6F9BEA"
  lapis-light: "#1E4FA8"
  ground: "#0B1222"
  ground-light: "#F3F5F9"
  plate: "#13224A"
  plate-light: "#FFFFFF"
  plate-2: "#1A2D5C"
  plate-2-light: "#E6EDF8"
  mast: "#13224A"
  mast-light: "#1E3A78"
  mast-ink: "#EEF1F7"
  mast-ink-2: "#B4C0DA"
  ink: "#E8ECF4"
  ink-light: "#111A2C"
  ink-2: "#A3AFC4"
  ink-2-light: "#4A576D"
  code-bg: "#0E182C"
  code-bg-light: "#EDF1F8"
  c1: "#6F9BEA"
  c2: "#C29A4F"
  c3: "#A3AFC4"
  c4: "#8FB0EE"
  c5: "#9C8A62"
typography:
  display:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "clamp(36px, 5.2vw, 60px)"
    fontWeight: 700
    lineHeight: 1.25
  headline:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "clamp(28px, 3.4vw, 38px)"
    fontWeight: 700
    lineHeight: 1.35
  title:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.5
  lede:
    fontFamily: "Noto Sans Arabic, Segoe UI, Tahoma, system-ui, sans-serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.75
  body:
    fontFamily: "Noto Sans Arabic, Segoe UI, Tahoma, system-ui, sans-serif"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.85
  subhead:
    fontFamily: "Noto Sans Arabic, Segoe UI, Tahoma, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 700
    lineHeight: 1.6
  label:
    fontFamily: "Noto Sans Arabic, Segoe UI, Tahoma, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 600
  code:
    fontFamily: "JetBrains Mono, ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "12.5px"
    fontWeight: 400
  key-letter:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1
rounded:
  hair: "2px"
  plate: "4px"
  sm: "6px"
  art: "10px"
  pill: "999px"
  disc: "50%"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "20px"
  xl: "28px"
  rail-gap: "56px"
  section: "88px"
  rail: "236px"
  measure: "68ch"
  page: "1240px"
components:
  letter-key:
    textColor: "{colors.key}"
    typography: "{typography.key-letter}"
    rounded: "{rounded.disc}"
    size: "1.75em"
  letter-key-selected:
    backgroundColor: "{colors.key}"
    textColor: "{colors.on-key}"
    rounded: "{rounded.disc}"
  part-node:
    rounded: "{rounded.sm}"
    padding: "9px 10px"
  part-node-selected:
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  button-pill:
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "6px 14px"
  button-pill-primary:
    backgroundColor: "{colors.key}"
    textColor: "{colors.on-key}"
    rounded: "{rounded.pill}"
    padding: "6px 14px"
  level-switch-on:
    backgroundColor: "{colors.mast-ink}"
    textColor: "{colors.mast}"
    rounded: "{rounded.pill}"
    padding: "3px 14px"
  plate-frame:
    backgroundColor: "{colors.plate}"
    rounded: "{rounded.plate}"
    padding: "6px"
  step-card:
    backgroundColor: "{colors.plate}"
    rounded: "{rounded.sm}"
    padding: "20px 22px"
  code-block:
    backgroundColor: "{colors.code-bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 14px"
  masthead:
    backgroundColor: "{colors.mast}"
    textColor: "{colors.mast-ink}"
    padding: "28px 0 40px"
---

# Design System: /explain

## Overview

**Creative North Star: "The Lettered Plate"**

Every codebase is drawn as one of Al-Jazari's mechanical plates. Each part receives an abjad letter (أ ب ج د…) in vermilion, and that letter follows the part through the whole page: the mechanism map, the route of one request, the database register, the change table, the figures and the inline prose. The reader moves letter, then part, then file, the way one reads a lettered plate. Choosing a letter anywhere lights the same part everywhere.

The page is dark-first: a lapis-black ground, lapis plate fields, gilt hairlines for every frame and rule, paper-white ink. The light theme is cool paper with lapis ink, the same vermilion deepened, and darkened gilt. Classical naskh carries titles and keys, a calm Arabic sans carries reading, mono appears only for code. Density is moderate: one fixed reading measure, generous section spacing, and structure drawn by hairlines rather than boxed cards.

The layout is fixed across projects; only the data changes. A lapis masthead band opens the page, a sticky index rail sits at the right (RTL start) edge, and one main column runs beside it.

**Key Characteristics:**
- Abjad letter keys in vermilion, the single signature device, shared by every section.
- Gilt hairlines (1px) as the only framing and dividing material.
- A double-ruled plate frame (gilt outer, soft gilt inner) around the mechanism and figures.
- Naskh display for titles, keys and numerals; Arabic sans for reading; LTR mono for every identifier.
- Flat, tonal depth; no drop shadows.
- Two themes from one token set, switched by `prefers-color-scheme` or `data-theme`.

## Colors

A lapis-and-gilt night palette with one vermilion rubric; every value has a light-theme twin under the same token name.

### Primary
- **Vermilion Rubric** (`key`; `key-light` in the paper theme): reserved for letter keys and the selected part. It marks the current part's border and tint, the active index entry, the route's progress line and current station, the primary step button, and the struck-through line in a code diff. Nothing else is vermilion.

### Secondary
- **Gilt Hairline** (`gilt`, `gilt-light`): plate outer frames, masthead bottom rule, footer rule, rail heading, table headers, story phase titles, exercise numerals, relation kinds, the disclosure triangle and figure-caption labels.
- **Soft Gilt** (`gilt-soft`, `gilt-soft-light`): every row divider, section top rule, inner plate frame, card border and quiet button border. This is the commonest line on the page.
- **Masthead Gilt** (`mast-gilt`, `mast-gilt-light`): the brighter gilt used only on the lapis masthead band (the `/explain` mark, legend dots, level-switch frame, focus rings inside the band).

### Tertiary
- **Lapis Link** (`lapis`, `lapis-light`): links, disclosure summaries ("show columns", "answer") and every focus ring outside the masthead.
- **Layer Tints** (`c1` to `c5`): five quiet hues assigned to layers in rotation (layer index mod 5). They tint node borders and backgrounds at low strength (34% border, 6% fill), colour story event kinds, mark added lines in diffs (`c2`) and fill figure boxes `f-c1` to `f-c5`. Light-theme values are darker equivalents in the template.

### Neutral
- **Lapis-Black Ground** (`ground`, `ground-light` cool paper): page background, also the fill behind route stations so they punch out of the line.
- **Lapis Plate** (`plate`, `plate-light`): raised fields: the mechanism plate, step card, hovered and selected rows, the key-role row.
- **Plate Two** (`plate-2`, `plate-2-light`): figure box fill (`f-box`).
- **Masthead Lapis** (`mast`, `mast-light`) with **Masthead Ink** (`mast-ink`) and **Masthead Ink Two** (`mast-ink-2`): the band and its text.
- **Paper Ink** (`ink`, `ink-light`): primary text.
- **Muted Ink** (`ink-2`, `ink-2-light`): secondary text, file paths, metadata, section intros.
- **Code Well** (`code-bg`, `code-bg-light`): inline code chips and code or tree blocks.

### Named Rules
**The Rubric Rule.** Vermilion belongs to letter keys and the selected part only. Never fill a box, a heading, a decoration or a figure shape with it; highlights that are not selection use gilt (`f-acc`).

**The Hairline Rule.** Structure is drawn with 1px gilt lines, soft gilt for dividers and full gilt for frames. Do not introduce grey borders or filled card backgrounds to separate content.

**The Twin Token Rule.** Colour only through the tokens. Every surface, including Claude-drawn figures, must render correctly in both themes without a single hex value.

## Typography

**Display Font:** Amiri (with Noto Naskh Arabic, Times New Roman, serif)
**Body Font:** Noto Sans Arabic (with Segoe UI, Tahoma, system-ui, sans-serif)
**Label/Mono Font:** JetBrains Mono (with ui-monospace, SF Mono, Menlo, Consolas, monospace)

**Character:** A classical naskh voice for titles, letters and numerals set against a calm, highly legible Arabic sans; code stays in a technical mono, always left-to-right and isolated from the Arabic flow.

### Hierarchy
- **Display** (Amiri 700, clamp(36px, 5.2vw, 60px), 1.25): the project title in the masthead, balanced, at most 22ch.
- **Headline** (Amiri 700, clamp(28px, 3.4vw, 38px), 1.35): section titles, each sitting under a soft gilt top rule.
- **Title** (Amiri 700, 20 to 24px): step-card title, story phase titles (21px, gilt), figure titles (20px), the analogy's big idea (22px, 400). The selected-part letter in the key box is Amiri 700 at 56px in vermilion; exercise numerals are Amiri 700 at 30px in gilt.
- **Lede** (Noto Sans Arabic 400, 20px, 1.75): the one-line answer in the masthead, max 64ch.
- **Body** (Noto Sans Arabic 400, 16.5px, 1.85): all reading text, held to the 68ch measure; secondary paragraphs run 15 to 15.5px in muted ink.
- **Subhead** (Noto Sans Arabic 700, 17px, 1.6): card and row headings.
- **Label** (Noto Sans Arabic 600 to 700, 13 to 14.5px): band headers, table headers (gilt), counts and metadata; tabular numerals wherever numbers align.
- **Code** (JetBrains Mono 400 to 600, 11 to 14.5px; 12.5px is the norm): part names, file paths, line numbers, hashes. Inline code is 0.84em on a code-well chip.

### Named Rules
**The Three Voices Rule.** Naskh for titles, keys and numerals; sans for reading; mono for identifiers only. Never set Arabic prose in mono or code in naskh.

**The Isolated Code Rule.** Every identifier, path and snippet is `direction: ltr` with bidi isolation, aligned to the right edge of its column so paths line up in strict tabular columns.

## Layout

A centred page of 1240px. The masthead band spans full width with its content aligned to the same 1240px column (padding 28px top, 40px bottom). Below it, a two-column shell: the index rail (236px) at the right, a 56px gap, and the main column; shell padding is 40px top, 96px bottom. Main sections are separated by 88px, each section's own parts by 20px. Reading text holds a fixed 68ch measure. Page gutters are at least 16px and respect safe-area insets.

The rail is sticky (20px from the top) and carries the section table of contents and the lettered parts index. The flow section splits into a step list and a sticky step card (1fr / 1.15fr, 28px gap). Registers (database, glossary, story, relations) are two-column grids of label column and content column, divided by hairlines.

At 960px and below, the shell collapses to one column; the rail becomes a sticky horizontal tab strip on the ground colour with a soft gilt bottom rule, the parts index hides, the active tab is underlined in vermilion, and section spacing drops to 72px. At 620px and below, registers stack to a single column and the masthead legend stacks vertically. Wide content (route, change table, figures, code) scrolls inside its own container, never the page.

## Elevation & Depth

Flat. Depth comes from tone (ground, plate, plate two) and from gilt framing, never from drop shadows. Selection is shown by vermilion border and a 10% vermilion tint; focus mode dims unrelated parts to soft gilt and muted ink. The single exception is the route's current station, which carries a soft vermilion halo ring.

### Shadow Vocabulary
- **Station Halo** (`box-shadow: 0 0 0 6px color-mix(in srgb, var(--key) 22%, transparent)`): only on the route station currently being played.

### Named Rules
**The Tonal Depth Rule.** Lift a surface by moving it from ground to plate, never by shadow.

## Shapes

Round where it is a letter or a control, nearly square where it is a plate. Letter keys and role icons are full discs (50%) with a 1px rim. Buttons, the level switch and tags are pills (999px). Part nodes, step cards, code blocks and hover rows use a gentle 6px corner. The mechanism plate and figure frames are double-ruled: a 4px outer frame in full gilt, 6px of plate, then a 2px inner frame in soft gilt. Inline code chips round at 4px; the cast illustration frame at 10px. Section boundaries and register rows are straight hairlines with no corners at all.

## Components

### Letter Key (signature)
The page's identity. A naskh letter centred in a disc (1.75em, 15px Amiri 700) with a vermilion letter and a 55% vermilion rim on a transparent fill. Selected: solid vermilion disc with ground-coloured letter. Smaller sizes for inline references and table rows (1.45 to 1.5em, 12px); 38px with 18px letter on route stations, which sit on the ground colour. In figures the page draws the same key (a vermilion-stroked circle with an Amiri letter) in the top-right corner of every keyed box.

### Buttons
- **Shape:** pill (999px).
- **Default:** transparent with a soft gilt border, ink text, 14px 600, padding 6px 14px; icon-only variant 6px 10px.
- **Primary:** vermilion fill with on-key text; used only for the play control of the route.
- **Hover / Focus:** border moves to full gilt; focus is a 2px lapis outline at 2px offset (masthead gilt inside the band).
- **Level switch:** a pill track with a masthead-gilt rim holding beginner and expert options; the pressed option inverts to masthead ink on lapis.

### Part Node
A clickable cell on the mechanism plate: letter key spanning two rows, mono part name (12.5px 600) and a short Arabic description (13px muted). Border is the layer tint at 34% with a 6% tint fill; hover strengthens the border to the full layer tint. Selected: vermilion border and 10% vermilion fill; related parts keep their full layer border; when a part is selected every other node dims to soft gilt with muted names.

### Plate and Figure Frame
The double-ruled frame (see Shapes) on plate colour. The mechanism plate holds layer bands, each with a header (bold layer name, muted mono folder) and an auto-fill grid of nodes (min 250px, 8px gap). Figures use the same frame, a naskh title, and a muted caption whose lead label is gilt.

### Key Box
The selected part's detail: a 56px vermilion naskh letter, mono name at 18px, gilt layer label, muted mono file path, prose, and a list of linked parts as hover rows. Ruled above and below in soft gilt.

### Route
One request as a line of lettered stations: a 2px soft gilt track with a vermilion fill that grows (0.75s, cubic-bezier(.16, 1, .3, 1)). Passed stations take a vermilion rim and letter; the current station fills vermilion with the halo; numbers below use tabular numerals.

### Registers and Tables
Rows divided by soft gilt hairlines, no backgrounds at rest; hover and selection lift a row to plate. Headers are gilt label type. Paths sit in an LTR mono column aligned right, with the part's letter key beside them. Selected rows: plate fill and vermilion name.

### Navigation (Index Rail)
A gilt naskh heading over a list of section links, each with a soft gilt right rule; the current section takes ink colour, weight 600 and a vermilion rule. The parts index below lists letter keys with mono names. On narrow screens it becomes the horizontal tab strip described in Layout.

### Code Blocks
Code-well background, soft gilt border, 6px corners, 12px 14px padding, JetBrains Mono 13px at 1.75, always LTR and scrollable. Diffs strike removed lines in muted ink with a vermilion strike and set added lines in `c2` at 600.

### Figure Classes (for Claude-drawn SVG)
Figures are inline SVG coloured only through these classes, so they follow both themes:
- **Boxes:** `f-box` (plate-two fill, soft gilt stroke 1.2); `f-acc` gilt highlight box (16% gilt over plate, gilt stroke 1.6); `f-c1` to `f-c5` layer-tinted boxes (14% tint over plate, tint stroke 1.4), matching the layer colours of the map; `f-band` dashed background band (ground fill, soft gilt 4 4 dash).
- **Lines:** `f-line` (muted ink, 1.6, no fill); `f-dash` (same, 5 4 dash); `f-head` arrowhead fill in muted ink.
- **Text:** plain `<text>` gets the Arabic body font, ink colour, 14px, RTL; `f-t` bold title text; `f-m` muted 12px note; `f-code` mono 11px LTR in muted ink.
- **Keys:** a `<g data-key>` wrapping a box makes it a part: the page adds the `f-key` letter in its top-right corner, and selection turns that box's stroke vermilion at 2.4 and fills its key.

## Do's and Don'ts

### Do:
- **Do** give every part its abjad letter and show that same letter wherever the part appears.
- **Do** draw structure with 1px gilt hairlines: soft gilt for dividers, full gilt for frames and the masthead rule.
- **Do** set titles, letters and numerals in Amiri 700, reading text in Noto Sans Arabic at 16.5px / 1.85 within 68ch, and identifiers in JetBrains Mono, LTR and isolated.
- **Do** colour figures only with the `f-` classes, start them on the right, and wrap part boxes in `data-key` groups with a 26px clear top-right corner.
- **Do** keep wide content scrolling inside its own container so the page never scrolls sideways.
- **Do** use a 2px lapis focus ring (masthead gilt inside the band) on every interactive element.

### Don't:
- **Don't** use vermilion for anything except letter keys and the selected part; use `f-acc` gilt for emphasis in figures.
- **Don't** use hex values or inline colours in figures or data; both themes must work from the tokens.
- **Don't** add drop shadows; depth is tonal, and the route halo is the only ring.
- **Don't** fall back to a docs-site arrangement of a left sidebar tree and white cards; the rail sits at the right and content is ruled, not boxed.
- **Don't** set Arabic prose in mono or code in the naskh face.
