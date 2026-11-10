# DATA file: shape and field rules

Read this once before writing the DATA JSON. Every string is Arabic except code names, file paths and code snippets.

**Quick mode** uses only `project`, `layers`, `flow`, `change`, and optionally `analogy` (3 roles) and `glossary` (up to 5). Skip the other fields in the shape and their rules below. Where a rule below gives a count, the sizes table wins for your depth.

```json
{
  "project": {
    "name": "كيف يعمل تطبيق ...",
    "title": "شرح تطبيق ...",
    "tag": "شرح مشروع",
    "path": "~/Projects/...",
    "oneLiner": "ما هو المشروع، لمن، وماذا يفعل، في جملتين.",
    "facts": ["Flutter 3.19", "flutter_bloc لإدارة الحالة", "بدون خادم"],
    "mode": "full"
  },
  "analogy": {
    "title": "تعرّف على الفريق",
    "intro": "...",
    "cast": [
      {"icon": "person", "role": "أنت، اللاعب", "job": "...", "code": "", "key": false, "handoff": "«نقطة لي!»"}
    ],
    "bigIdea": "لكل جزء مهمة واحدة..."
  },
  "layers": [
    {"name": "الشاشات · ما تراه وتضغطه", "folder": "lib/presentation/pages", "between": "ترسل الأحداث وتعيد الرسم",
     "nodes": [
       {"id": "scoreboard", "name": "ScoreboardPage", "short": "اضغط لتسجيل نقطة",
        "file": "lib/presentation/pages/scoreboard_page.dart",
        "what": "شرح بسيط في 2–3 جمل.",
        "links": [{"to": "bloc", "verb": "يرسل حدث ScorePoint"}],
        "inside": [{"name": "_onPointTap()", "line": 42, "what": "deep فقط: ماذا تفعل هذه الدالة في جملة."}]}
     ]}
  ],
  "flow": {"title": "ماذا يحدث عندما ...؟", "intro": "...",
    "steps": [{"who": "ScoreboardPage", "title": "...", "text": "...", "file": "lib/... · functionName()", "at": "scoreboard", "lit": []}]},
  "moreFlows": [{"tab": "تسجيل الدخول", "title": "ماذا يحدث عندما ...؟", "intro": "...", "steps": [{"who": "...", "title": "...", "text": "...", "file": "...", "at": "..."}]}],
  "notes": {"title": "ملاحظات المراجعة", "intro": "",
    "items": [{"kind": "gap", "title": "قبول العرض لا ينشئ عقدًا", "text": "...", "where": "lib/... · acceptOffer()"}]},
  "database": {"title": "أين تُحفظ البيانات؟", "intro": "...",
    "tables": [{"name": "cases", "what": "كل حالة يكتبها الطبيب.", "file": "supabase/migrations/0001_core.sql",
                "columns": [{"name": "user_id", "type": "text", "note": "صاحب الحالة"}]}],
    "relations": [{"from": "cases", "to": "profiles", "kind": "many-to-one", "text": "كل حالة تخص مستخدمًا واحدًا، وللمستخدم حالات كثيرة."}]},
  "story": {"title": "قصة المشروع", "intro": "...",
    "events": [{"date": "2026-05-11", "phase": "المرحلة 0", "kind": "start", "title": "...", "text": "...", "commit": "64f6692"}]},
  "parts": {"title": "الشاشات", "intro": "", "items": [{"name": "...", "how": "lib/...", "points": ["...", "..."]}]},
  "glossary": [{"term": "ويدجت", "en": "Widget", "meaning": "..."}],
  "change": [{"want": "تغيير قواعد التسجيل", "where": "lib/domain/entities/match.dart · applyPoint"}],
  "exercises": [{"title": "...", "text": "...", "file": "lib/... · السطر 12", "before": "...", "after": "...", "answer": ""}],
  "tree": "lib/\n├── main.dart   # ...\n└── ...",
  "footer": "مبني على قراءة الكود الحقيقي في ..."
}
```

## Sizes per depth

`project.mode` is `quick`, `full` (the default) or `deep`. `build.py` warns when a page is far outside its depth's size.

| Field | quick | full | deep |
|---|---|---|---|
| layers / layer nodes | 2–4 / 5–12 | 3–6 / 12–22 | 3–7 / 16–32 |
| `flow.steps` | 3–5 | 5–7 | 5–9 |
| `moreFlows` | omit | omit | 1–2 more flows |
| `inside` | omit | omit | 3–5 members on each of the 5–8 central parts |
| `notes` | omit | omit | 5–10 items |
| `analogy.cast` | 0 or 3 roles | 4–6 | 4–6 |
| `database`, `story`, `parts`, `tree` | omit | when they exist | when they exist, with more columns |
| `glossary` | 0–5 | 8–10 | 10–14 |
| `change` | 4–6 | 6–8 | 8–12 |
| `exercises` | omit | 3 | 4–5, the last one a trace or a fix |
| `figures` | omit | 0–2 | 0–3, only where a drawing explains what the sections can't |

In every mode, `what` is at most 2 sentences and every other prose string at most 1–2 sentences. Depth comes from more parts and more sections, not longer paragraphs.

## Field rules


- A cast role's `code` is the class, module or file that plays the role (in module-based code, a file name like `lib/matchmaking.ts` is fine).
- `icon` is one of: person, screen, phone, brain, book, notebook, database, server, cloud, gear, key, mail, bell, shield, ball, box.
- `layers`: top (what the user touches) to bottom (storage, network, device); layer count per the sizes table. Each layer gets 1–6 nodes. `between` is the short label on the arrow to the next layer; leave it out on the last layer. In full and deep, put startup and helper services in their own last layer ("البدء والأدوات المساعدة") rather than leaving them out; quick skips them.
- `links` go from a node to what it uses. Every `to` must be an existing `id`; the build script rejects broken links. Aim for every node to have at least one connection.
- `flow.steps`: the most common action (a tap, an HTTP request, a CLI command). Each step names who does it and cites the function.
- `flow.steps[].at`: the node `id` where the request is during that step. The page shows a compact copy of the layer map and a ball that travels to that node, so the reader sees the request cross layers. Give every step an `at`; use `lit` for extra node ids to light up at the same time (for example the database and the service writing to it).
- `database`: tables in order of importance (the main entity first), each with a one-sentence plain-Arabic `what` and 3–8 important columns (skip housekeeping like `created_at` unless it matters). Every relation needs a plain-Arabic `text` sentence a beginner can read ("كل حالة تخص مستخدمًا واحدًا"). `kind` is one of one-to-many, many-to-one, one-to-one, many-to-many. List only relations that exist in the schema; unrelated tables simply have none. Omit the whole field when there is no database.
- `story`: 6–10 events, oldest first, grouped by `phase` (a release, a phase or a quarter). `kind` is one of start, feature, architecture, fix, release, docs. Say why each moment matters for someone reading the code today ("لهذا يوجد مجلدان للواجهة"), not just what the commit message says. Omit the field when there is no git history or fewer than about 15 commits.
- `figures`: optional extra diagrams you draw yourself. Read `references/figures.md` only when you add one; most pages need 0–2.
- `parts`: the screens for an app, the API routes for a backend, the commands for a CLI. Change `title` to match.
- `glossary`: words the learner will meet in this codebase, framework terms first.
- `change`: rows of "I want to…" → file.
- `exercises`: easiest first. In full, two small safe edits with visible results (a text, a color, a constant) and one "read and explain" task with the answer in `answer`. Use real `before`/`after` lines copied from the file. `file` is written as `path · السطر N` (or `السطور A–B`). `before` is the cited line's text; leading spaces don't matter, and `verify.py` checks it. For the read-and-explain task, leave `before` empty and put the cited code in `after` (several lines joined with `\n`; the first one must sit at the cited line).
- `moreFlows` (deep): other common actions, each a complete flow like `flow` with its own `title`, a short `tab` label (2–3 words; give the main `flow` a `tab` too) and steps with `at`. Pick actions that cross different parts from the main flow (sign-in, a background job, an admin action), not variations of it.
- `inside` (deep): the members of a part a maintainer would open first. `name` is the function, method or field as written in the code (`acceptOffer()`, `state.score`); `line` is where it is declared; `what` says what it does in one sentence. `verify.py` checks that each name sits in the part's `file` near that line, so you don't need to grep each one yourself: write your best line, run verify, and fix only what it reports.
- `notes` (deep): what you noticed while reading that a maintainer must know. `kind` is one of gap (something missing or unfinished), risk (it breaks under a real case), security, debt (code that will slow the next change), perf. Every note cites `where` and says what happens and why it matters, in plain words. Report only what the code shows; no generic advice ("add more tests") and no guesses.
- In any prose string, wrap a code name in backticks (`` `MatchBloc` ``) and it renders as left-to-right code.

## Beginners and experts on one page

The page has a مبتدئ / خبير switch. Beginner mode hides file paths, folders, commit hashes, step file references and table columns, leaving the analogy, the plain explanations and the relations. Expert mode shows everything. So write every `what`, `text` and relation sentence so it makes sense **without** the path next to it, and put the technical precision (function names, line numbers, column types) in the fields the switch hides: `file`, `columns`, `commit`, `folder`, `inside`, and a note's `where`.
