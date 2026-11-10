# Figures

You design the figures yourself as inline SVG. It costs nothing, works for every user, follows the page's light/dark theme, and can carry Arabic labels in the page's own font. Add a figure only when a picture explains something faster than the built-in sections do. The layer map, flow track, database cards and timeline already cover structure, flow, tables and history, so don't redraw them.

Figures that usually earn their place:

- **Where things run (deployment).** Phone or browser, server host, database, auth provider, AI or payment APIs, and what travels between them.
- **A pipeline the reader must trust.** Validation, safety filters, payments, a build or CI pipeline, with the branch where things get rejected.
- **A state machine.** Order, case, booking or ticket statuses and what moves an item between them.
- **An auth or sync sequence** between two or three parties.
- **The cast illustration:** one scene with every analogy role, as simple flat figures.

Add each figure to DATA:

```json
"figures": [
  {"id": "deploy", "section": "layers", "title": "أين يعمل كل جزء؟",
   "caption": "جملة عربية واحدة تشرح ما يجب أن يلاحظه القارئ.",
   "alt": "وصف نصي للشكل لقارئات الشاشة", "svg": "deploy.svg", "expertOnly": false}
]
```

- `section`: where it appears. One of top, analogy, layers, flow, database, parts, story, end.
- `svg`: a path to an `.svg` file you wrote (relative to the DATA file) or the SVG markup itself. Use `src` instead only for a raster image file the user supplied.
- `expertOnly: true` hides the figure in beginner mode, for very technical figures.

Drawing rules (the build script enforces the first three):

1. Start with `<svg viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg">`, with no fixed width or height. Keep W between 800 and 1000 so labels stay readable. The page lets it scroll sideways on phones.
2. No scripts, event handlers, `foreignObject` or remote files.
3. Prefix every `id` with the figure id (`deploy-arrow`), so arrow markers don't clash between figures.
4. Color only through the page's classes, never hex values, so it works in both themes:
   - boxes: `f-box`, gilt highlight box `f-acc` (vermilion stays reserved for letter keys and the selected part, so never colour a box with it), tinted boxes `f-c1`…`f-c5` (matching the layer colors), dashed background band `f-band`;
   - lines: `f-line`, dashed `f-dash`, arrowhead fill `f-head`;
   - text: `f-t` for titles, `f-m` for muted notes, `f-code` for code names (left-to-right mono). Plain `<text>` already gets the body font and color.
5. Arabic reads right to left, so put the starting point on the **right** and let arrows run leftward. The page sets `direction: rtl` on figure text, so mixed labels like «الخادم على Render» come out in the right order. With rtl, `text-anchor="start"` anchors the **right** edge of the text and `"end"` the left edge. Use `"middle"` for labels inside boxes and `"start"` for labels aligned to a right edge. `f-code` text stays left-to-right.
6. Short labels: 1–4 words at 12–14px. Leave at least 12px between any text and a box edge or line. Keep everything inside the viewBox with a 10px margin. Wrap the second line of a label as its own `<text>`.
7. Arrows: `<marker id="deploy-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="f-head"/></marker>`. Route lines around boxes, never through them.
8. Every name in a figure must match the code, the same as everywhere else on the page.
9. Key the drawing. Wrap each box that stands for a part on the layer map in `<g data-key="<node id>"> <rect …/> <text …/> … </g>`, with the `rect` first. The page then draws that part's abjad letter in the box's top corner, lights the box when the part is selected anywhere, and selects the part when the box is clicked. Leave a 26px clear corner at the box's top-right for the letter. Boxes for things that are not parts (the user, an outside idea) stay unwrapped.

Before building, re-read each SVG once with fresh eyes: add up the x positions and widths of each row of boxes and check nothing overlaps or runs past the edge.
