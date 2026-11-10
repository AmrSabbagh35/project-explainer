---
name: explain
description: Explain any software project in full, simple Arabic as an interactive right-to-left explainer page with a real-world analogy, a clickable map of the project's layers, a step-by-step flow of one request, the screens or entry points, a glossary, a "where do I change what" table and starter exercises. Use whenever the user wants to understand, explain, document, teach or onboard someone to a codebase in Arabic, for example "اشرح لي هذا المشروع", "شرح كامل بالعربية", "كيف يعمل هذا الكود", "ارسم لي مكونات المشروع", "أريد أن أفهم مشروع استلمته", "اشرح المشروع للطلاب", or a vibe-coded project they don't understand yet, even if they don't say "skill", "diagram" or "page". Also use when they ask in English for an Arabic explanation of a repo. Three depths: quick (سريع، نظرة سريعة), full (default) and deep (عميق، مفصل، للمراجعة) with extra flows, function-level detail and review notes.
license: MIT
---

# شرح المشروع بالعربية (Arabic project explainer)

Turn a real codebase into one Arabic page that a learner can read top to bottom and a developer can use as a map. The page layout is a fixed template filled from a JSON file, so your effort goes into understanding the code and writing clear Arabic. Readers are students, junior developers, or anyone who inherited or vibe-coded a project.

`SKILL` below means this skill's folder (`~/.claude/skills/explain` for a personal install, `.claude/skills/explain` for a project install).

## Keep it cheap

Tokens go to three places: reading code, writing the DATA file, and re-reading things. Spend them only on the first two.

- Start from `scan.py`, not from exploring by hand. One call gives the tree, dependencies, entry points, the biggest files and their classes, routes, schema and git milestones.
- Read only files you will cite, and only the part you need (use offsets, or `grep -n` for one function). Never read generated files, tests, lockfiles, assets or platform folders (`ios/`, `android/`).
- Don't spawn a subagent for projects under about 400 source files (in `deep`, about 200). For bigger ones, send one Explore subagent on the `haiku` model with a narrow question (the main flow's files and functions; in `deep`, one subagent per extra flow), never "map everything". `quick` never needs one.
- Write the DATA file once with one Write. Fix build or verify errors with Edit, never by rewriting the file. Don't read back the JSON or the built HTML.
- Don't syntax-check the page; the template is fixed and already tested. `build.py` and `verify.py` are the only checks.

## Three depths

Every page is built at one depth. Pick it from the user's words; default to `full`. Set it as `project.mode`.

| Mode | Words that pick it | Who it's for | What the page has | Rough cost |
|---|---|---|---|---|
| `quick` | سريع، مختصر، نظرة سريعة، quick, short, overview, tl;dr | "What is this?" in 5 minutes | the one-liner, 2–4 layers with 5–12 parts, one flow of 3–5 steps, 4–6 "where do I change" rows, optionally a 3-role analogy and 5 words | ~25k tokens |
| `full` | كامل، شرح، (nothing), full | learning the project, onboarding | everything below at the normal size: analogy, 12–22 parts, one flow, database, story, screens, glossary, change table, 3 exercises, tree | ~40–50k |
| `deep` | عميق، مفصل، تفصيلي، للمراجعة، deep, detailed, in depth, review | maintainers and reviewers who will change the code | full, plus: 16–32 parts, 2–3 flows (`moreFlows`), what is inside each central part (`inside`: key functions with line numbers), review notes (`notes`: gaps, risks, security, tech debt, performance), 4–5 exercises, and figures where they help | ~90–100k, plus Haiku helpers on big repos |

Depth changes how much you read and write, never the template. In `quick`, stop reading as soon as you can name the layers and the one flow: grep the flow files for function signatures and read only the lines around them (about 100 lines in all is usually enough); don't read the database or git history. In `deep`, check every note yourself in the code before keeping it (drop any a subagent can't back with a line), but leave line numbers in `inside` to `verify.py` instead of grepping each one.

## Workflow

### 1. Find the project and the depth

The user usually types `/explain`. Whatever follows is the input, in any order: a depth word (above), a path (`/explain ~/Projects/shop`), a part to focus on (`/explain the payment flow`), or nothing (the current project at `full`). `/explain سريع ~/Projects/shop` and `/explain deep payments` both work. A focus doesn't change the depth; it makes the main flow follow that focus. If the working directory isn't a project and no path was given, ask which project; don't guess.

### 2. Map it in one call

```bash
python3 -I SKILL/scripts/scan.py <project-root>
```

From the output decide, within the depth's budget: the layers, the parts (layer nodes) that matter, the most common user action, whether there is a database worth a section, and whether git history is rich enough for a story. Then read only the central files: the entry point, the main state holder, controller or service, the data model, and the two or three files on the main flow's path.

### 3. Choose the analogy

Pick one analogy from the project's own world, so the reader already knows the roles: a scoreboard and umpire for a sports app, reception, doctor and medical file for a clinic, cashier and warehouse for a shop, a post office for chat, a restaurant for a generic backend. Map each role to one real class; mark the most central one `key: true`. 4–6 roles.

### 4. Write the DATA file

Read `SKILL/references/data.md` for the JSON shape, the rules for each field and each depth's sizes, then write the file in a scratch folder (not inside the user's project) in one go. Read `SKILL/references/figures.md` only if a figure would explain something the built-in sections can't (where things run, a safety or payment pipeline, a state machine); most pages need none.

### 5. Verify and build

```bash
python3 -I SKILL/scripts/verify.py <data.json> <project-root>
python3 -I SKILL/scripts/build.py <data.json> <out.html>
```

`verify.py` checks every cited path, every exercise line number and snippet, and every story commit against the repo, and prints only problems. Fix each one with a small Edit and rerun. `build.py` checks the structure (ids, links, sections) and writes the page. Put the HTML in the scratch folder unless the user wants it in the project (for example `docs/شرح-المشروع.html`).

### 6. Deliver

If the Artifact tool is available, publish the HTML as an artifact (icon `book`) and give the link; otherwise open the file in the browser and give its absolute path. The page is one self-contained file. Remind the user that it shows their file names, folders and commit messages before they share it. Reply in Arabic: the depth, what the page covers, and anything you could not verify. After a `quick` or `full` page, mention in one line that a deeper one is available.

## Writing the Arabic

The page succeeds or fails on the writing. Write how a good teacher talks, not how a translated manual reads.

- Clear Modern Standard Arabic, short sentences, one idea per sentence.
- Say what a part does in the reader's terms before naming the technology: «يحفظ النتيجة في ذاكرة الهاتف بعد كل نقطة» before «يستخدم SharedPreferences».
- Code names, file names and packages stay in English exactly as in the code. On first use of a concept give both: «المستودع (Repository)».
- If a sentence sounds translated, rewrite it from scratch. Western digits (0–9) for numbers and line numbers.
- No padding. Every sentence teaches something about this project.

## What to avoid

- Inventing parts, or describing what a framework usually does instead of what this project does.
- Listing every file; the folder tree covers the rest.
- An analogy from the wrong world (a restaurant for a booking system).
- Changing the template's layout. Consistency across projects is the point; put the effort into the content.
