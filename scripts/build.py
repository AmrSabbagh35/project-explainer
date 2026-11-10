#!/usr/bin/env python3
"""Build an Arabic project explainer page from a DATA JSON file.

Usage:
    python3 -I build.py <data.json> <out.html>

Reads the template next to this script (../assets/template.html), swaps the
sample DATA block for the JSON you wrote, sets the <title>, and checks the
data for the mistakes that break the page: missing fields, links that point
at node ids that don't exist, duplicate ids, and empty flows.
"""
import base64
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "template.html"


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


MODES = {
    "quick": {"nodes": (5, 12), "omit": ("database", "story", "parts", "exercises", "tree", "moreFlows", "notes", "figures")},
    "full": {"nodes": (12, 22), "omit": ("moreFlows", "notes")},
    "deep": {"nodes": (16, 32), "omit": ()},
}
NOTE_KINDS = {"gap", "risk", "security", "debt", "perf"}


def check(d):
    warnings = []
    for key in ("project", "layers", "flow"):
        if key not in d:
            fail("missing top-level field: " + key)
    if not d["project"].get("name"):
        fail("project.name is empty")
    ids = {}
    for li, layer in enumerate(d["layers"]):
        if not layer.get("nodes"):
            fail("layer %d (%s) has no nodes" % (li, layer.get("name")))
        for n in layer["nodes"]:
            for f in ("id", "name", "short", "file", "what"):
                if not n.get(f):
                    fail("node %r is missing %s" % (n.get("id"), f))
            if n["id"] in ids:
                fail("duplicate node id: " + n["id"])
            ids[n["id"]] = n
    for n in ids.values():
        for l in n.get("links", []):
            if l.get("to") not in ids:
                fail("node %r links to unknown id %r" % (n["id"], l.get("to")))
    mode = d["project"].get("mode", "full")
    if mode not in MODES:
        fail("project.mode must be one of %s" % ", ".join(MODES))
    flows = [("flow", d["flow"])] + [("moreFlows[%d]" % i, f) for i, f in enumerate(d.get("moreFlows") or [])]
    for name, fl in flows:
        if not fl.get("steps"):
            fail("%s.steps is empty" % name)
        if name != "flow" and not fl.get("title"):
            fail("%s has no title" % name)
        for i, s in enumerate(fl["steps"], 1):
            for ref in ([s["at"]] if s.get("at") else []) + list(s.get("lit", [])):
                if ref not in ids:
                    fail("%s step %d points at unknown node id %r" % (name, i, ref))
        if len(flows) > 1 and not fl.get("tab"):
            warnings.append("%s has no short 'tab' label, so its tab shows the whole title" % name)
        if not any(s.get("at") for s in fl["steps"]):
            warnings.append("no %s step has 'at', so the travelling ball is hidden" % name)
    for n in ids.values():
        for m in n.get("inside", []):
            if not m.get("name") or not m.get("what"):
                fail("node %r: every inside item needs name and what" % n["id"])
            if m.get("line") is not None and not isinstance(m["line"], int):
                fail("node %r: inside %r line must be a number" % (n["id"], m["name"]))
    for it in (d.get("notes") or {}).get("items", []):
        if it.get("kind") not in NOTE_KINDS:
            fail("note %r: kind must be one of %s" % (it.get("title"), ", ".join(sorted(NOTE_KINDS))))
        if not it.get("title") or not it.get("text"):
            fail("note is missing title or text: %r" % it)

    # each mode has its own size; a page far outside it is usually the wrong mode
    total = len(ids)
    lo, hi = MODES[mode]["nodes"]
    if total > hi:  # small projects may fall below the range; only too many is a mistake
        warnings.append("%s mode allows up to %d layer nodes, this page has %d" % (mode, hi, total))
    for f in MODES[mode]["omit"]:
        if d.get(f):
            warnings.append("%s mode usually leaves out %r" % (mode, f))

    db = d.get("database")
    if db:
        names = set()
        for t in db.get("tables", []):
            if not t.get("name") or not t.get("what"):
                fail("database table is missing name or what: %r" % t)
            names.add(t["name"])
        for r in db.get("relations", []):
            for end in ("from", "to"):
                if r.get(end) not in names:
                    fail("database relation %s=%r is not a table" % (end, r.get(end)))
            if not r.get("text"):
                fail("database relation %s→%s has no plain-Arabic text" % (r.get("from"), r.get("to")))

    story = d.get("story")
    if story:
        kinds = {"start", "feature", "architecture", "fix", "release", "docs"}
        for e in story.get("events", []):
            for f in ("date", "title", "text"):
                if not e.get(f):
                    fail("story event is missing %s: %r" % (f, e.get("title")))
            if e.get("kind") and e["kind"] not in kinds:
                fail("story event kind %r must be one of %s" % (e["kind"], ", ".join(sorted(kinds))))
    linked = {l["to"] for n in ids.values() for l in n.get("links", [])} | {
        n["id"] for n in ids.values() if n.get("links")
    }
    lonely = [i for i in ids if i not in linked]
    if lonely:
        warnings.append("nodes with no connections: " + ", ".join(lonely))
    return warnings


MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml"}


def embed_image(d, base, warnings):
    """Turn analogy.image.src from a local file path into a data: URI.

    Artifact pages can't load images from other hosts, so a local file is
    inlined. URLs and existing data: URIs are left alone.
    """
    img = (d.get("analogy") or {}).get("image")
    if not img or not img.get("src"):
        return
    src = img["src"]
    if src.startswith(("data:", "http://", "https://")):
        if src.startswith("http"):
            warnings.append("analogy.image.src is a remote URL; artifact pages block remote images")
        return
    p = pathlib.Path(src).expanduser()
    if not p.is_absolute():
        p = base / p
    if not p.exists():
        fail("analogy.image.src file not found: %s" % p)
    mime = MIME.get(p.suffix.lower())
    if not mime:
        fail("unsupported image type %s (use png, jpg, webp or svg)" % p.suffix)
    raw = p.read_bytes()
    if len(raw) > 3 * 1024 * 1024:
        warnings.append("illustration is %.1f MB; resize it under 1 MB for a fast page" % (len(raw) / 1048576))
    img["src"] = "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))


SECTIONS = {"top", "analogy", "layers", "flow", "database", "parts", "story", "end"}
UNSAFE = [
    (re.compile(r"<script\b.*?</script\s*>", re.S | re.I), ""),
    (re.compile(r"<foreignObject\b.*?</foreignObject\s*>", re.S | re.I), ""),
    (re.compile(r"\son[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*')", re.I), ""),
    (re.compile(r"(href\s*=\s*[\"'])\s*javascript:[^\"']*", re.I), r"\1#"),
]


def clean_svg(svg, fid, alt, warnings):
    """Make a Claude-drawn SVG safe and accessible to inline in the page."""
    svg = re.sub(r"<\?xml[^>]*>", "", svg).strip()
    svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg, flags=re.I).strip()
    if not svg.lower().startswith("<svg"):
        fail("figure %r: svg must start with <svg" % fid)
    for pat, rep in UNSAFE:
        svg = pat.sub(rep, svg)
    if re.search(r"(?:href|src)\s*=\s*[\"']https?://", svg, re.I):
        fail("figure %r: svg loads a remote file; artifact pages block those, draw it inline instead" % fid)
    head = svg[: svg.index(">") + 1]
    if "viewbox" not in head.lower():
        fail("figure %r: the <svg> tag needs a viewBox so it scales" % fid)
    if re.search(r"\s(width|height)\s*=", head):
        svg = re.sub(r"\s(?:width|height)\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg[: len(head)], count=2) + svg[len(head):]
        warnings.append("figure %r: removed fixed width/height so it scales with the page" % fid)
    if "role=" not in head:
        label = (alt or fid).replace('"', "'")
        svg = svg.replace("<svg", '<svg role="img" aria-label="%s"' % label, 1)
    ids = re.findall(r"\sid\s*=\s*[\"']([^\"']+)", svg)
    bad = [i for i in ids if not i.startswith(fid + "-")]
    if bad:
        warnings.append("figure %r: ids %s should start with %r so markers don't clash between figures" % (fid, ", ".join(bad[:4]), fid + "-"))
    if len(svg) > 200_000:
        warnings.append("figure %r is %d KB of SVG; simplify it" % (fid, len(svg) // 1024))
    return svg


def prepare_figures(d, base, warnings):
    figs = d.get("figures") or []
    seen = set()
    for f in figs:
        fid = f.get("id")
        if not fid or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fid):
            fail("figure id %r must be lowercase letters, digits and hyphens" % fid)
        if fid in seen:
            fail("duplicate figure id: " + fid)
        seen.add(fid)
        if f.get("section", "end") not in SECTIONS:
            fail("figure %r: section must be one of %s" % (fid, ", ".join(sorted(SECTIONS))))
        if not f.get("caption") and not f.get("title"):
            fail("figure %r needs a title or a caption in Arabic" % fid)
        if bool(f.get("svg")) == bool(f.get("src")):
            fail("figure %r needs exactly one of svg (inline or .svg path) or src (image path)" % fid)
        if f.get("svg"):
            svg = f["svg"]
            if not svg.lstrip().startswith("<"):
                p = pathlib.Path(svg).expanduser()
                p = p if p.is_absolute() else base / p
                if not p.exists():
                    fail("figure %r: svg file not found: %s" % (fid, p))
                svg = p.read_text(encoding="utf-8")
            f["svg"] = clean_svg(svg, fid, f.get("alt") or f.get("title") or f.get("caption"), warnings)
            node_ids = {n["id"] for l in d["layers"] for n in l["nodes"]}
            for k in re.findall(r"data-key\s*=\s*[\"']([^\"']+)", f["svg"]):
                if k not in node_ids:
                    fail("figure %r: data-key %r is not a node id on the layer map" % (fid, k))
            if "data-key" not in f["svg"]:
                warnings.append("figure %r has no <g data-key> groups, so its boxes carry no letters" % fid)
        else:
            holder = {"analogy": {"image": {"src": f["src"]}}}
            embed_image(holder, base, warnings)
            f["src"] = holder["analogy"]["image"]["src"]
    if len(figs) > 6:
        warnings.append("%d figures; more than 6 usually means some repeat what the page already shows" % len(figs))


def main():
    if len(sys.argv) != 3:
        fail("usage: build.py <data.json> <out.html>")
    data_path, out_path = map(pathlib.Path, sys.argv[1:])
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail("data.json is not valid JSON: %s" % e)
    warnings = check(data)
    embed_image(data, data_path.parent, warnings)
    prepare_figures(data, data_path.parent, warnings)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    block = "// DATA:START\nvar DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n// DATA:END"
    out, count = re.subn(r"// DATA:START.*?// DATA:END", lambda _m: block, tpl, flags=re.S)
    if count != 1:
        fail("template DATA markers not found")
    title = data["project"].get("title") or ("شرح " + data["project"]["name"])
    out = out.replace("__TITLE__", title.replace("<", "").replace(">", ""), 1)
    out_path.write_text(out, encoding="utf-8")
    for w in warnings:
        print("WARNING: " + w)
    nodes = sum(len(l["nodes"]) for l in data["layers"])
    flows = 1 + len(data.get("moreFlows") or [])
    print("OK: wrote %s (%s mode, %d layers, %d nodes, %d flow%s)" % (
        out_path, data["project"].get("mode", "full"), len(data["layers"]), nodes, flows, "" if flows == 1 else "s"))


if __name__ == "__main__":
    main()
