#!/usr/bin/env python3
"""Check every code fact in an /explain DATA file against the repository, in one call.

Usage:
    python3 -I verify.py <data.json> <project-root>

Checks:
  - file paths cited by parts, steps (all flows), changes, parts sections, tables, notes and exercises exist;
  - deep mode: each part's "inside" members exist in its file, near the cited line;
  - exercise line numbers: the `before` line (or the first line of `after` on a
    read-only task) really sits at the cited line (within 3 lines);
  - story commits exist in git.
Prints only problems, then a one-line summary. Exit code 1 when something is wrong.
This replaces checking each line by hand with grep.
"""
import json
import os
import re
import subprocess
import sys

IGNORE = {".git", "node_modules", "build", "dist", ".dart_tool", "Pods", "vendor", ".next", "venv", ".venv", "target"}
PATHISH = re.compile(r"[\w@~.\-]+(?:/[\w@.\-*]+)+/?|[\w@.\-]+\.[A-Za-z]{1,6}\b")
LINE_AR = re.compile(r"(?:السطر|السطور|line|lines)\s*(\d+)(?:\s*[–-]\s*(\d+))?", re.I)


def norm(s):
    return re.sub(r"\s+", " ", s).strip().rstrip(",;")


def index(root):
    byname, allpaths = {}, set()
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in IGNORE]
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), root)
            allpaths.add(rel)
            byname.setdefault(f, []).append(rel)
        allpaths.add(os.path.relpath(d, root))
    return byname, allpaths


def resolve(tok, root, byname, allpaths):
    tok = tok.strip().rstrip("/.,)").lstrip("(")
    if not tok or "*" in tok or tok.endswith("_") or tok.startswith(("@", "package:")):
        return "skip"
    tok = os.path.expanduser(tok)
    if os.path.isabs(tok):
        return tok if os.path.exists(tok) else None
    if tok in allpaths or os.path.exists(os.path.join(root, tok)):
        return tok
    # paths written relative to a sub-app (frontend_v2/lib/... cited as lib/...), or a bare file name
    hits = [p for p in allpaths if p == tok or p.endswith("/" + tok)]
    if hits:
        return hits[0]
    base = os.path.basename(tok)
    if "/" not in tok and base in byname:
        return byname[base][0]
    return None


def paths_in(s):
    out = []
    for m in PATHISH.finditer(s or ""):
        t = m.group(0)
        if re.fullmatch(r"\d+(\.\d+)*", t) or t.startswith(("http", "www.")) or re.fullmatch(r"[A-Za-z]+\.[A-Za-z]+", t) and "/" not in t and not re.search(r"\.(dart|ts|tsx|js|jsx|py|go|rs|sql|json|yaml|yml|md|html|css|kt|swift|java|cs|rb|php|vue|svelte|arb|prisma|toml)$", t):
            continue
        out.append(t)
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: verify.py <data.json> <project-root>")
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    root = os.path.abspath(os.path.expanduser(sys.argv[2]))
    byname, allpaths = index(root)
    problems, checked = [], 0

    def check(where, s):
        nonlocal checked
        for t in paths_in(s):
            r = resolve(t, root, byname, allpaths)
            if r == "skip":
                continue
            checked += 1
            if not r:
                problems.append("%s: path not found: %s" % (where, t))

    for L in data.get("layers", []):
        for n in L.get("nodes", []):
            check("part %s" % n.get("id"), n.get("file", ""))
    for fi, fl in enumerate([data.get("flow", {})] + list(data.get("moreFlows") or [])):
        for i, s in enumerate(fl.get("steps", []), 1):
            check("step %d" % i if fi == 0 else "flow %d step %d" % (fi + 1, i), s.get("file", ""))
    for it in (data.get("notes") or {}).get("items", []):
        check("note «%s»" % it.get("title", "")[:30], it.get("where", ""))

    # deep mode: every "inside" member really sits in its part's file, near the cited line
    for L in data.get("layers", []):
        for n in L.get("nodes", []):
            if not n.get("inside"):
                continue
            toks = paths_in(n.get("file", ""))
            path = resolve(toks[0], root, byname, allpaths) if toks else None
            if not path or path == "skip":
                continue
            src = open(os.path.join(root, path) if not os.path.isabs(path) else path, encoding="utf-8", errors="ignore").read().splitlines()
            for m in n["inside"]:
                word = re.split(r"[(\s<]", m.get("name", "").strip())[0].split(".")[-1]
                if not word:
                    continue
                checked += 1
                pat = re.compile(r"\b%s\b" % re.escape(word))
                hits = [j + 1 for j, l in enumerate(src) if pat.search(l)]
                if not hits:
                    problems.append("part %s: %s is not in %s" % (n.get("id"), word, path))
                elif m.get("line") and not any(abs(h - m["line"]) <= 3 for h in hits):
                    problems.append("part %s: %s is at line %s, not %d" % (n.get("id"), word, ", ".join(map(str, hits[:3])), m["line"]))
    for c in data.get("change", []):
        check("change «%s»" % c.get("want", "")[:30], c.get("where", ""))
    for p in (data.get("parts") or {}).get("items", []):
        check("parts «%s»" % p.get("name", ""), p.get("how", ""))
    for t in (data.get("database") or {}).get("tables", []):
        check("table %s" % t.get("name"), t.get("file", ""))

    for i, ex in enumerate(data.get("exercises", []), 1):
        f = ex.get("file", "")
        toks = paths_in(f)
        if not toks:
            continue
        path = resolve(toks[0], root, byname, allpaths)
        checked += 1
        if not path or path == "skip":
            problems.append("exercise %d: path not found: %s" % (i, toks[0]))
            continue
        m = LINE_AR.search(f)
        want = (ex.get("before") or "").splitlines()[:1] or (ex.get("after") or "").splitlines()[:1]
        if not m or not want:
            continue
        line = int(m.group(1))
        try:
            src = open(os.path.join(root, path) if not os.path.isabs(path) else path, encoding="utf-8", errors="ignore").read().splitlines()
        except OSError:
            problems.append("exercise %d: cannot read %s" % (i, path))
            continue
        target = norm(want[0])
        near = [j for j in range(max(1, line - 3), min(len(src), line + 3) + 1) if norm(src[j - 1]) == target or (len(target) > 12 and target in norm(src[j - 1]))]
        checked += 1
        if not near:
            anywhere = [j + 1 for j, l in enumerate(src) if norm(l) == target or (len(target) > 12 and target in norm(l))]
            problems.append("exercise %d: %s line %d does not contain «%s»%s" % (
                i, path, line, target[:70], (" (found at line %s)" % ", ".join(map(str, anywhere[:3]))) if anywhere else " (not in file)"))
        elif line not in near:
            problems.append("exercise %d: «%s» is at line %d, not %d" % (i, target[:50], near[0], line))

    commits = [e.get("commit") for e in (data.get("story") or {}).get("events", []) if e.get("commit")]
    for h in commits:
        checked += 1
        ok = subprocess.run(["git", "-C", root, "cat-file", "-e", h + "^{commit}"], capture_output=True).returncode == 0
        if not ok:
            problems.append("story: commit %s not found" % h)

    for p in problems:
        print("PROBLEM: " + p)
    print("%s: %d facts checked, %d problems" % ("OK" if not problems else "FIX", checked, len(problems)))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
