#!/usr/bin/env python3
"""Derive the quick and full sample files from the deep ones.

    python3 -I examples/make-depths.py

sample-deep.json    -> sample.json, sample-quick.json        (Arabic)
sample-deep-en.json -> sample-en.json, sample-quick-en.json  (English)
Edit the deep files, then rerun this so all depths stay in step.
"""
import copy
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
TEXT = {
    "ar": {"full_title": "شرح تطبيق مكتبتي", "quick_title": "شرح سريع لتطبيق مكتبتي",
           "facts": ["React 18", "Node.js + Express", "PostgreSQL عبر Prisma"],
           "intro": "في أي مكتبة يوجد قارئ، وأمين مكتبة، وسجل للاستعارة. التطبيق فيه نفس الوظائف.",
           "step1": "الشاشة ترسل `POST /loans` ومعها رقم الكتاب.", "between": "ترسل الطلبات إلى الخادم",
           "verbs": ["ترسل طلب الحجز", "تجلب استعاراتي", "يكتب في جدول loans", "يبحث عن المواعيد القريبة", "يبحث عن القارئ"],
           "footer_full": "مثال خيالي يوضح شكل صفحة /explain.", "footer_quick": "مثال خيالي يوضح شكل صفحة /explain سريع.",
           "drop_layer": "الواجهة · الحالة والاتصال"},
    "en": {"full_title": "My Library, explained", "quick_title": "My Library, a quick look",
           "facts": ["React 18", "Node.js + Express", "PostgreSQL via Prisma"],
           "intro": "A library has a reader, a librarian and a loan ledger. The app has the same jobs.",
           "step1": "The screen sends `POST /loans` with the book's id.", "between": "send requests to the server",
           "verbs": ["sends the reservation", "loads my loans", "writes to the loans table", "finds loans due soon", "looks up the reader"],
           "footer_full": "A fictional sample that shows what an /explain page looks like.", "footer_quick": "A fictional sample that shows what an /explain quick page looks like.",
           "drop_layer": "Front end · state and requests"},
}


def derive(deep_name, full_name, quick_name, t):
    deep = json.loads((HERE / deep_name).read_text(encoding="utf-8"))
    full = copy.deepcopy(deep)
    full["project"].update(mode="full", title=t["full_title"])
    for k in ("moreFlows", "notes"):
        full.pop(k, None)
    full["flow"].pop("tab", None)
    for L in full["layers"]:
        for n in L["nodes"]:
            n.pop("inside", None)
    full["exercises"] = full["exercises"][:3]
    full["footer"] = t["footer_full"]
    (HERE / full_name).write_text(json.dumps(full, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    q = copy.deepcopy(full)
    q["project"].update(mode="quick", title=t["quick_title"], facts=t["facts"])
    keep = {"list", "mine", "loansR", "guard", "loanSvc", "reminder", "db"}
    layers = []
    for L in q["layers"]:
        L["nodes"] = [n for n in L["nodes"] if n["id"] in keep]
        if L["nodes"] and L["name"] != t["drop_layer"]:
            layers.append(L)
    by = {n["id"]: n for L in layers for n in L["nodes"]}
    v = t["verbs"]
    by["list"]["links"] = [{"to": "loansR", "verb": v[0]}]
    by["mine"]["links"] = [{"to": "loansR", "verb": v[1]}]
    by["loanSvc"]["links"] = [{"to": "db", "verb": v[2]}]
    by["reminder"]["links"] = [{"to": "db", "verb": v[3]}]
    by["guard"]["links"] = [{"to": "db", "verb": v[4]}]
    by["loansR"]["links"] = [l for l in by["loansR"]["links"] if l["to"] in keep]
    layers[0]["between"] = t["between"]
    layers[-1].pop("between", None)
    q["layers"] = layers
    q["analogy"]["cast"] = [c for c in q["analogy"]["cast"] if c["code"] in ("", "loanService", "PostgreSQL")]
    q["analogy"]["intro"] = t["intro"]
    q["analogy"].pop("bigIdea", None)
    s = q["flow"]["steps"]
    q["flow"]["steps"] = [s[0], s[2], s[3], s[4]]
    q["flow"]["steps"][0]["text"] = t["step1"]
    for st in q["flow"]["steps"]:
        st["lit"] = [x for x in st.get("lit", []) if x in keep]
    q["glossary"] = q["glossary"][2:7]
    q["change"] = q["change"][:5]
    for k in ("database", "story", "parts", "exercises", "tree", "figures"):
        q.pop(k, None)
    q["footer"] = t["footer_quick"]
    (HERE / quick_name).write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


derive("sample-deep.json", "sample.json", "sample-quick.json", TEXT["ar"])
derive("sample-deep-en.json", "sample-en.json", "sample-quick-en.json", TEXT["en"])
print("ok")
