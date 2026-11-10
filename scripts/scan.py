#!/usr/bin/env python3
"""One-shot, compact map of a codebase for /explain.

Usage:
    python3 -I scan.py <project-root>

Prints, in a few thousand tokens: size and languages, manifest dependencies,
README head, folder tree with file counts, entry points, the biggest source
files with the classes/functions they declare, route registrations, database
schema (tables, models, foreign keys), tests, and git history highlights.
It replaces a dozen exploratory commands, so Claude reads only the few files
the page really needs. Standard library only.
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

IGNORE = {
    ".git", "node_modules", "build", "dist", "out", ".dart_tool", "Pods", "vendor", ".next",
    ".nuxt", ".venv", "venv", "env", "__pycache__", ".idea", ".vscode", "target", "bin", "obj",
    ".gradle", "coverage", ".turbo", ".cache", "DerivedData", ".expo", ".svelte-kit", "ephemeral",
    ".impeccable", ".pytest_cache", ".mypy_cache", "Flutter", "generated",
}
PLATFORM = {"android", "ios", "macos", "linux", "windows", "web"}
TESTY = re.compile(r"(^|/)(test|tests|__tests__|spec|integration_test)/|[._-](test|spec)\.\w+$")
GENERATED = re.compile(r"\.(g|freezed|gr|pb|mocks)\.\w+$|(^|/)(l10n|generated|gen)/.*localizations|\.min\.js$")
SRC = {".dart", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".py", ".go", ".rs", ".java", ".kt", ".swift",
       ".cs", ".rb", ".php", ".vue", ".svelte", ".scala", ".ex", ".exs", ".c", ".cpp", ".h"}
ENTRY = {"main.dart", "index.ts", "index.js", "main.ts", "main.js", "app.ts", "app.js", "server.ts",
         "server.js", "main.py", "app.py", "manage.py", "wsgi.py", "asgi.py", "main.go", "Program.cs",
         "main.rs", "lib.rs", "App.tsx", "App.jsx", "App.vue", "_app.tsx", "layout.tsx", "page.tsx",
         "routes.ts", "router.ts", "app_router.dart", "urls.py", "Application.java", "MainActivity.kt"}
DECL = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+|final\s+|sealed\s+|public\s+|data\s+|async\s+)*"
    r"(class|interface|enum|mixin|struct|trait|function|def|func|fn|type)\s+([A-Za-z_][\w]*)")
ROUTE = re.compile(
    r"""(?:\b(?:app|router|[a-zA-Z]+Router|server|api)\.(get|post|put|patch|delete|use|route)\(\s*['"`]([^'"`]+)"""
    r"""|@(?:app|bp|router|api)\.(?:route|get|post|put|patch|delete)\(\s*['"]([^'"]+)"""
    r"""|@(Get|Post|Put|Patch|Delete|Request)Mapping\(\s*(?:value\s*=\s*)?['"]([^'"]+)"""
    r"""|GoRoute\(\s*path:\s*['"]([^'"]+)"""
    r"""|path\(\s*['"]([^'"]*)['"]\s*,)""")
MILESTONE = re.compile(
    r"\b(initial|first|init|launch|release|v\d+(\.\d+)*|phase|rewrite|rebuild|refactor|migrat\w*|"
    r"replace\w*|switch\w*|introduc\w*|add(ed|s)?\s+(the\s+)?\w+\s+(integration|support|auth|database|api)|"
    r"auth|database|deploy\w*|feat(ure)?\b)", re.I)


def out(title, lines, cap):
    lines = [l for l in lines if l is not None]
    if not lines:
        return
    print("\n## " + title)
    for l in lines[:cap]:
        print(l)
    if len(lines) > cap:
        print("… (%d more)" % (len(lines) - cap))


def walk(root):
    files = []
    for d, dirs, fs in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in IGNORE and not x.startswith("."))
        for f in fs:
            if f.startswith("."):
                continue
            p = os.path.join(d, f)
            files.append(os.path.relpath(p, root))
    return files


def lines_of(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read().splitlines()
    except OSError:
        return []


def manifests(root):
    res = []
    pj = os.path.join(root, "package.json")
    for p in [pj] + [os.path.join(root, d, "package.json") for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d)) and d not in IGNORE]:
        if os.path.isfile(p):
            try:
                data = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            deps = sorted(list((data.get("dependencies") or {}).keys()))
            dev = sorted(list((data.get("devDependencies") or {}).keys()))
            scripts = list((data.get("scripts") or {}).keys())
            res.append("%s: %s | deps: %s | dev: %s | scripts: %s" % (
                os.path.relpath(p, root), data.get("name", ""), ", ".join(deps[:30]), ", ".join(dev[:15]), ", ".join(scripts[:12])))
    for p in sorted(set(os.path.join(dp, "pubspec.yaml") for dp in [root] + [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and d not in IGNORE])):
        if os.path.isfile(p):
            ls = lines_of(p)
            deps, on = [], False
            for l in ls:
                if re.match(r"^(dependencies|dev_dependencies):", l):
                    on = True
                    continue
                if on and re.match(r"^\S", l):
                    on = False
                m = re.match(r"^  ([a-z_0-9]+):\s*(\S*)", l)
                if on and m:
                    deps.append(m.group(1) + (" " + m.group(2) if m.group(2) else ""))
            res.append("%s: %s" % (os.path.relpath(p, root), ", ".join(deps[:40])))
    for name in ("pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "composer.json", "Gemfile", "pom.xml", "build.gradle", "build.gradle.kts"):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            ls = [l.strip() for l in lines_of(p) if l.strip() and not l.strip().startswith("#")]
            res.append("%s: %s" % (name, " | ".join(ls[:25])[:900]))
    return res


def git(root, *args):
    try:
        return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return ""


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: scan.py <project-root>")
    root = os.path.abspath(os.path.expanduser(sys.argv[1]))
    files = walk(root)
    src = [f for f in files if os.path.splitext(f)[1] in SRC]
    print("# scan: %s" % root)
    ext = Counter(os.path.splitext(f)[1] or "(none)" for f in files)
    print("files: %d total, %d source | top types: %s" % (len(files), len(src), ", ".join("%s %d" % e for e in ext.most_common(8))))

    out("manifests", manifests(root), 12)

    readmes = sorted((f for f in files if "readme" in os.path.basename(f).lower() and f.count(os.sep) <= 1), key=lambda f: (f.count(os.sep), len(f)))
    if readmes:
        readme = readmes[0]
        txt = [l for l in lines_of(os.path.join(root, readme)) if l.strip()][:25]
        out("README head (%s)" % readme, ["> " + l[:160] for l in txt], 25)

    # folder tree, depth 3, with file counts
    counts = defaultdict(int)
    for f in files:
        parts = f.split(os.sep)[:-1]
        depth = 1 if parts and parts[0] in PLATFORM else 3
        for i in range(1, min(len(parts), depth) + 1):
            counts[os.sep.join(parts[:i])] += 1
    tree = ["%s%s/  (%d)" % ("  " * (d.count(os.sep)), os.path.basename(d), n) for d, n in sorted(counts.items(), key=lambda kv: kv[0].split(os.sep))]
    out("folders (depth 3, file counts)", tree, 90)

    entries = [f for f in files if os.path.basename(f) in ENTRY]
    out("entry points", entries, 25)

    # biggest source files and what they declare
    sized = []
    for f in src:
        if TESTY.search(f) or GENERATED.search(f) or f.split(os.sep)[0] in PLATFORM:
            continue
        ls = lines_of(os.path.join(root, f))
        decl = []
        for l in ls:
            m = DECL.match(l)
            if m and m.group(2) not in decl:
                decl.append(m.group(2))
            if len(decl) >= 6:
                break
        sized.append((len(ls), f, decl))
    sized.sort(reverse=True)
    out("largest source files (lines · declarations)", ["%5d  %s  · %s" % (n, f, ", ".join(d)) for n, f, d in sized[:40]], 40)

    # routes
    routes = []
    for n, f, _ in sized:
        for i, l in enumerate(lines_of(os.path.join(root, f)), 1):
            m = ROUTE.search(l)
            if m:
                verb = m.group(1) or m.group(4) or ("route" if m.group(3) or m.group(6) or m.group(7) is not None else "")
                path = next(g for g in (m.group(2), m.group(3), m.group(5), m.group(6), m.group(7)) if g is not None)
                routes.append("%s:%d  %s %s" % (f, i, verb.upper(), path))
    out("routes", routes, 70)

    # database schema
    schema = []
    for f in files:
        b = os.path.basename(f)
        low = f.lower()
        if b.endswith(".sql") and ("migration" in low or "schema" in low or "supabase" in low or "db" in low):
            for i, l in enumerate(lines_of(os.path.join(root, f)), 1):
                if re.search(r"create table|references\s+\S+|alter table .* add column", l, re.I):
                    schema.append("%s:%d  %s" % (f, i, l.strip()[:110]))
        elif b == "schema.prisma":
            for i, l in enumerate(lines_of(os.path.join(root, f)), 1):
                if re.match(r"\s*(model|enum)\s+\w+", l) or "@relation" in l:
                    schema.append("%s:%d  %s" % (f, i, l.strip()[:110]))
        elif b in ("models.py",) or "/entities/" in low or "/models/" in low and b.endswith((".ts", ".py")):
            for i, l in enumerate(lines_of(os.path.join(root, f)), 1):
                if re.search(r"class \w+\(.*Model\)|ForeignKey\(|@Entity|@ManyToOne|@OneToMany|new Schema\(|Table\(", l):
                    schema.append("%s:%d  %s" % (f, i, l.strip()[:110]))
    out("database schema", schema, 50)

    tests = [f for f in files if TESTY.search(f)]
    tdirs = Counter(f.split(os.sep)[0] for f in tests)
    out("tests", ["%d test files: %s" % (len(tests), ", ".join("%s %d" % t for t in tdirs.most_common(6)))] if tests else [], 2)

    if os.path.isdir(os.path.join(root, ".git")) or git(root, "rev-parse", "--git-dir").strip():
        log = [l for l in git(root, "log", "--reverse", "--date=short", "--pretty=%ad %h %s").splitlines() if l.strip()]
        if log:
            months = Counter(l[:7] for l in log)
            print("\n## git")
            print("commits: %d | first %s | last %s | branch %s" % (len(log), log[0][:10], log[-1][:10], git(root, "branch", "--show-current").strip()))
            print("per month: " + ", ".join("%s %d" % m for m in sorted(months.items())))
            tags = git(root, "tag").split()
            if tags:
                print("tags: " + ", ".join(tags[:20]))
            cand = [log[0]] + [l for l in log[1:] if MILESTONE.search(l[19:]) and not re.search(r"\bmerge\b|\bwip\b|typo", l, re.I)]
            step = max(1, len(cand) // 32)
            out("milestone candidates (date hash subject)", [l[:110] for l in cand[::step]] + ([log[-1][:110]] if cand[-1] != log[-1] else []), 35)


if __name__ == "__main__":
    main()
