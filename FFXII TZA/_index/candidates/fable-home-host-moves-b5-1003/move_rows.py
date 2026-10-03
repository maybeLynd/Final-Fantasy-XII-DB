"""move_rows.py [--apply] [--root DIR] [--only FN,FN] - move FABLE-homed rows that SWE2-AUDIT-SPEC rejected for
host fit to a host that cites their caller or a callee, or return them to the frontier (FABLE, 2026-10-03; AUDIT-SPEC
batch 5: the steal-roll review of commit 6435250e4 and the three rows batch 4 deferred).

Copy of fable-home-host-moves-b4-1003/move_rows.py (itself OPUS's opus-fable-home-host-moves-1003 script plus
`drops`), extended only for:
- `host` on each move: `caller` (the b4 rule: the target cites the entered_from caller outside this record's
  section), `callee` (the target cites each listed function outside the section, and the body calls or jumps to
  each of them directly), or `row-caller` (the caller is itself homed in this record's section on the same page);
- `adds`: a row for a body no page states yet, written to the target only (no source page, no source record);
- `drops` with `unbound` instead of `already_bound_on`: the row is removed from its rejected host and returned to the
  frontier. Verify re-derives, from the image, the raw transfer index into the body (E8/E9 rel32, 0F 8x rel32,
  EB/7x rel8, each decoded as a direct call or jump to the entry) grouped by owning function, and the body's direct
  targets outside itself; both must equal the record. Every bearing page (no path part starting `_`) that names one
  of those functions must be listed in `cites` with a quote that is still on it.

moves.json beside this file (built by build_moves.py) lists, per row: the source page, the source record, the
target page, the row text and anchors, the host basis, and quotes from the target page's own text. The moved rows
were reviewed exact (sentence, site, anchors) by SWE2-AUDIT-SPEC; only their host was wrong. No text is edited.

Verifies, in the certified image, exactly what the source homing_applier.py verified, against the TARGET page:
- every `entered_from` site is a direct call or jump to the function, from inside the named caller;
- every anchor is an instruction boundary strictly inside the function with the recorded mnemonic;
- no text has a pipe.
It also checks the host basis above, and that every evidence quote is still on the target page.

Without --apply it only verifies, and reports what --apply would do.
With --apply, for each row (byte-preserving and CRLF-aware):
- SOURCE PAGE: removes the row's table line from the FABLE homed section dated `source_section_date`. When that
  leaves the section's table empty, removes the whole section, which is what the reviews call withdrawing it.
- SOURCE RECORD: removes the row from rows.json `rows` and appends it to a `moved` (or `dropped`) list, with the
  target and the date (indent=1, no trailing newline, as the records are written).
- TARGET PAGE: adds the row to one FABLE section, `target_heading`, appending the section when absent. `adds` are
  written before `moves`, so a homed caller precedes the body it enters.
Idempotent: a step already done prints ALREADY, and a second --apply changes nothing.
--root runs against a COPY of the tree (the directory that holds `FFXII TZA`'s pages); the image always comes from
the certified kit. --only limits the run to the listed functions. Prints VERIFY, per-step PATCHED / ALREADY / DRY,
and FAILS n. --moves reads another moves.json (used only by the sensitivity controls in README.md)."""
import argparse, bisect, json, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REAL_DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(REAL_DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
ap.add_argument("--root", default=REAL_DB)
ap.add_argument("--only", default="")
ap.add_argument("--moves", default=os.path.join(HERE, "moves.json"), help="moves.json to use (controls)")
a = ap.parse_args()
DB = os.path.abspath(a.root)
CFG = json.load(open(a.moves, encoding="utf-8"))
ONLY = a.only.upper().split(",") if a.only else None
MOVES = [m for m in CFG["moves"] if not ONLY or m["fn"] in ONLY]
ADDS = [m for m in CFG.get("adds", []) if not ONLY or m["fn"] in ONLY]
DROPS = [m for m in CFG.get("drops", []) if not ONLY or m["fn"] in ONLY]
HEAD = CFG["target_heading"]
REC = os.path.basename(HERE)
SITE = re.compile(r"`?([0-9A-F]{8})`?\s*\+\s*0x([0-9A-Fa-f]+)")
FABLE_HEAD = "## Homed frontier bodies called from this page's functions (FABLE, %s"
fails = 0


def fail(msg):
    global fails
    print("VERIFY FAIL " + msg)
    fails += 1


def path(rel):
    return os.path.join(DB, *rel.split("/"))


def read(rel):
    b = open(path(rel), "rb").read()
    return b, b"\r\n" in b[:4000]


def write(rel, text, crlf):
    s = text.replace("\r\n", "\n")
    open(path(rel), "wb").write((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


def section_bounds(lines, head_prefix):
    """(start, end) of the `## ` section whose heading starts with head_prefix; end is the next `## ` or len."""
    for i, l in enumerate(lines):
        if l.startswith(head_prefix):
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("## "):
                    return i, j
            return i, len(lines)
    return None


def caller_of(m):
    return SITE.fullmatch(m["entered_from"].strip()).group(1)


def row_line(m, size):
    site = m["entered_from"].strip()
    site = site if site.startswith("`") else "`%s`" % site
    depth = "../" * m["target_page"].count("/")
    if m.get("source_page"):
        src = m["source_page"]
        frm = "[%s](%s%s)" % (os.path.splitext(os.path.basename(src))[0], depth, src)
    else:
        frm = "newly homed ([review](%s%s))" % (depth, m["review"])
    return "| `%s` | %d B | %s | %s | %s | %s |" % (
        m["fn"], size, site, m["text"], "; ".join("Interior anchor `%s`" % x for x, _mn in m["anchors"]), frm)


def basis(m):
    h = m.get("host", {"by": "caller"})
    fn, c = m["fn"], caller_of(m)
    if h["by"] == "caller":
        s = "`%s`: this page cites its caller `%s` in its own text." % (fn, c)
    elif h["by"] == "callee":
        cs = " and ".join("`%s`" % x for x in h["callees"])
        s = "`%s`: this page states %s, which the body calls directly." % (fn, cs)
    else:
        s = "`%s`: its only caller, `%s`, is homed in this section." % (fn, c)
    if h.get("why"):
        s += " " + h["why"]
    if not m.get("source_page"):
        s += " No page stated this body before."
    return "- " + s


def section_text(target_page):
    depth = "../" * target_page.count("/")
    rows = [m for m in CFG.get("adds", []) + CFG["moves"] if m["target_page"] == target_page]
    return (HEAD + "\n\n"
            "*FABLE's homing stream (cloud-drafted, FABLE-verified) homed these bodies on other pages. SWE2-AUDIT-SPEC "
            "reviewed each sentence, site and anchor set exact and rejected only the host, because that page named "
            "the caller only as a foreign or boundary mention. A body newly homed here is marked so, with the "
            "review that gives its sentence. The sentences are unchanged. Each states what the body does (access "
            "and representation, not purpose), and the anchors are instructions inside it that do it. Why each "
            "row is here:*\n\n"
            + "\n".join(basis(m) for m in rows) + "\n\n"
            "*Verified by [`move_rows.py`](%s_index/candidates/%s/move_rows.py): every site transfers to its "
            "function, the caller or callee named above is cited on this page outside this section (or homed in "
            "it), and every anchor is an instruction boundary inside its function that decodes to the recorded "
            "mnemonic.*\n\n"
            "| function | size | entered from | what the body does | interior anchors | moved from |\n"
            "|---|---|---|---|---|---|\n" % (depth, REC))


# ---- image
sizes = cd.load_functions()
ENTS = sorted(sizes)
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def text_section():
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    image = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        if d[o:o + 8].rstrip(b"\0") == b".text":
            vs, va, rs, pr = struct.unpack_from("<IIII", d, o + 8)
            return image + va, pr, min(vs, rs)
    raise SystemExit("no .text")


def owner(x):
    i = bisect.bisect_right(ENTS, x) - 1
    return ENTS[i] if i >= 0 and ENTS[i] <= x < ENTS[i] + sizes[ENTS[i]] else None


def decode1(x):
    return next(md.disasm(d[off(x):off(x) + 16], x), None)


def direct_to(ci, t):
    return ci is not None and ci.operands and ci.operands[0].type == 2 and ci.operands[0].imm == t \
        and (ci.mnemonic in ("call", "jmp") or ci.mnemonic.startswith("j"))


def raw_callers(t):
    """{owner entry hex: [site hex, ...]} for every decoded direct transfer to t in .text."""
    tva, tpr, n = text_section()
    b = d[tpr:tpr + n]
    out = {}
    for i in range(n - 1):
        x, op = tva + i, b[i]
        hit = False
        if op in (0xE8, 0xE9) and i + 5 <= n:
            hit = x + 5 + struct.unpack_from("<i", b, i + 1)[0] == t
        elif op == 0x0F and i + 6 <= n and 0x80 <= b[i + 1] <= 0x8F:
            hit = x + 6 + struct.unpack_from("<i", b, i + 2)[0] == t
        elif op == 0xEB or 0x70 <= op <= 0x7F:
            hit = x + 2 + struct.unpack_from("<b", b, i + 1)[0] == t
        if hit and direct_to(decode1(x), t):
            o = owner(x)
            out.setdefault("%08X" % o if o else "unlisted", []).append("%08X" % x)
    return out


def direct_targets(f, n):
    """{target hex: [site hex, ...]} of direct calls/jumps from the body to outside it."""
    out = {}
    for ci in md.disasm(d[off(f):off(f) + n], f):
        if ci.operands and ci.operands[0].type == 2 and (ci.mnemonic in ("call", "jmp") or ci.mnemonic.startswith("j")):
            t = ci.operands[0].imm
            if not (f <= t < f + n):
                out.setdefault("%08X" % t, []).append("%08X" % ci.address)
    return out


def bearing_pages():
    for r, ds, fs in os.walk(DB):
        ds[:] = [x for x in ds if not x.startswith((".", "_"))]
        for x in fs:
            if x.endswith(".md"):
                yield os.path.relpath(os.path.join(r, x), DB).replace(os.sep, "/")


# ---- verify
RUN_FNS = {m["fn"] for m in MOVES + ADDS}
for m in ADDS + MOVES:
    fn = m["fn"]
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        fail("%s: not a function entry" % fn)
        continue
    sm = SITE.fullmatch(m["entered_from"].strip())
    tb, _ = read(m["target_page"])
    tlines = tb.decode("utf-8").replace("\r\n", "\n").split("\n")
    own = section_bounds(tlines, HEAD)
    outside = "\n".join(tlines[:own[0]] + tlines[own[1]:]) if own else "\n".join(tlines)
    inside = "\n".join(tlines[own[0]:own[1]]) if own else ""
    host = m.get("host", {"by": "caller"})
    if not sm:
        fail("%s: entered_from %r is not `caller` + 0xNN" % (fn, m["entered_from"]))
    else:
        c, o = int(sm.group(1), 16), int(sm.group(2), 16)
        cn = sizes.get(c)
        ci = decode1(c + o) if cn and o < cn else None
        if not ci or ci.mnemonic not in ("call", "jmp") or not ci.operands or ci.operands[0].type != 2 \
                or ci.operands[0].imm != f:
            fail("%s: %s is not a direct call/jmp to it" % (fn, m["entered_from"]))
        elif host["by"] == "caller" and sm.group(1) not in outside:
            fail("%s: the target page does not cite the caller %s outside the FABLE batch-5 section" % (fn, sm.group(1)))
        elif host["by"] == "row-caller":
            homed = [x for x in CFG.get("adds", []) + CFG["moves"]
                     if x["fn"] == sm.group(1) and x["target_page"] == m["target_page"]]
            if not homed:
                fail("%s: row-caller %s is not homed by this record on the target" % (fn, sm.group(1)))
            elif sm.group(1) not in RUN_FNS and "| `%s` |" % sm.group(1) not in inside:
                fail("%s: row-caller %s is neither in this run nor already on the target" % (fn, sm.group(1)))
    if host["by"] == "callee":
        tg = direct_targets(f, n)
        for x in host["callees"]:
            if x not in tg:
                fail("%s: the body does not call %s directly" % (fn, x))
            if x not in outside:
                fail("%s: the target page does not cite the callee %s outside the FABLE batch-5 section" % (fn, x))
    for e in m["evidence"]:
        if e["quote"] not in outside:
            fail("%s: evidence quote no longer on the target page: %r" % (fn, e["quote"][:60]))
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for x, mn in m["anchors"]:
        av = int(x, 16)
        if not (f < av < f + n):
            fail("%s: anchor %s outside the body" % (fn, x))
        elif ins.get(av) != mn:
            fail("%s: %s decodes to %r, recorded %r" % (fn, x, ins.get(av), mn))
    if "|" in m["text"]:
        fail("%s: pipe in text" % fn)
PAGES = None
for m in DROPS:
    fn = m["fn"]
    f = int(fn, 16)
    if not sizes.get(f):
        fail("%s: not a function entry" % fn)
        continue
    if "already_bound_on" in m:
        bp = m["already_bound_on"]
        bb, _ = read(bp["page"])
        if bp["quote"] not in bb.decode("utf-8") or fn not in bp["quote"]:
            fail("%s: already-bound quote no longer on %s: %r" % (fn, bp["page"], bp["quote"][:60]))
        continue
    ub = m["unbound"]
    got_c, got_t = raw_callers(f), direct_targets(f, sizes[f])
    if got_c != ub["callers"]:
        fail("%s: raw callers %s, recorded %s" % (fn, got_c, ub["callers"]))
    if sorted(got_t) != sorted(ub["callees"]):
        fail("%s: direct targets %s, recorded %s" % (fn, sorted(got_t), ub["callees"]))
    if PAGES is None:
        PAGES = {p: open(path(p), encoding="utf-8", errors="replace").read() for p in bearing_pages()}
    for x in sorted(set(got_c) | set(got_t)):
        hits = sorted(p for p, t in PAGES.items() if x in t)
        listed = {(c["page"]) for c in ub["cites"] if c["addr"] == x}
        for p in hits:
            if p not in listed:
                fail("%s: bearing page %s names %s and is not listed as a non-host cite" % (fn, p, x))
        for c in ub["cites"]:
            if c["addr"] == x and (c["quote"] not in PAGES.get(c["page"], "") or x not in c["quote"]):
                fail("%s: cite quote for %s no longer on %s" % (fn, x, c["page"]))
    print("UNBOUND %s raw callers %s; direct targets %s; bearing pages naming them %d (all listed non-host)" % (
        fn, ", ".join("%s (%s)" % (k, "/".join(v)) for k, v in sorted(got_c.items())) or "none",
        ", ".join(sorted(got_t)) or "none",
        len({p for x in set(got_c) | set(got_t) for p in PAGES if x in PAGES[p]})))
print("VERIFY %d functions, %d anchors, %d target pages, %d adds, %d drops" % (
    len(MOVES) + len(ADDS), sum(len(m["anchors"]) for m in MOVES + ADDS),
    len({m["target_page"] for m in MOVES + ADDS}), len(ADDS), len(DROPS)))
if fails:
    print("FAILS", fails)
    sys.exit(1)

# ---- apply (or dry-run report)
mode = "PATCHED" if a.apply else "DRY"


def remove_source(m):
    """Step 1, shared by moves and drops: remove the row from the FABLE section; False when its text differs."""
    fn = m["fn"]
    tag = "`%s`" % fn
    b, crlf = read(m["source_page"])
    lines = b.decode("utf-8").replace("\r\n", "\n").split("\n")
    sec = section_bounds(lines, FABLE_HEAD % m["source_section_date"])
    hit = [i for i in range(*sec) if lines[i].startswith("| %s |" % tag)] if sec else []
    if not hit:
        print("ALREADY source %s %s" % (fn, m["source_page"]))
        return True
    i = hit[0]
    if m["source_text"] not in lines[i]:
        fail("%s: source row text differs from the record" % fn)
        return False
    new = lines[:i] + lines[i + 1:]
    s2 = section_bounds(new, FABLE_HEAD % m["source_section_date"])
    left = [k for k in range(*s2) if new[k].startswith("| `")]
    withdrawn = not left
    if withdrawn:
        start = s2[0]
        while start > 0 and new[start - 1].strip() == "":
            start -= 1
        tail = new[s2[1]:]
        new = new[:start] + ([""] + tail if tail else [""])
    print("%s source %s %s%s" % (mode, fn, m["source_page"], " (section withdrawn)" if withdrawn else ""))
    if a.apply:
        write(m["source_page"], "\n".join(new), crlf)
    return True


def note_record(m, key, note):
    """Step 2, shared by moves and drops: move the row from rows.json `rows` to `key`, with `note` added."""
    fn = m["fn"]
    rp = os.path.join(DB, *m["source_record"].split("/"), "rows.json")
    rec = json.load(open(rp, encoding="utf-8"))
    row = next((r for r in rec["rows"] if r["fn"] == fn), None)
    declared = {(x.get("fn") if isinstance(x, dict) else x) for x in (rec.get("moved") or [])} \
        if isinstance(rec.get("moved"), list) else set((rec.get("moved") or {}).keys())
    if row is None or fn in declared:
        print("ALREADY record %s %s" % (fn, m["source_record"]))
        return
    # 2026-10-03: the row STAYS in `rows` (so the record keeps its shape) and is DECLARED under `moved`, which
    # check_record_rows_present.py honours; drops are declared there too, with the drop note.
    moved = dict(row)
    moved.update(note)
    moved["fn"] = fn
    if not isinstance(rec.get("moved"), list):
        rec["moved"] = [{"fn": k, "why": v} for k, v in (rec.get("moved") or {}).items()]
    rec["moved"].append(moved)
    if key != "moved":
        rec.setdefault(key, []).append(dict(moved))
    print("%s record %s %s" % (mode, fn, m["source_record"]))
    if a.apply:
        open(rp, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, ensure_ascii=True))


def add_target(m):
    """Step 3: add the row to this record's FABLE section on the target page."""
    fn = m["fn"]
    tag = "`%s`" % fn
    b, crlf = read(m["target_page"])
    text = b.decode("utf-8").replace("\r\n", "\n")
    lines = text.split("\n")
    line = row_line(m, sizes[int(fn, 16)])
    own = section_bounds(lines, HEAD)
    if own and any(lines[k].startswith("| %s |" % tag) for k in range(*own)):
        print("ALREADY target %s %s" % (fn, m["target_page"]))
        return
    if own:
        last = max(k for k in range(*own) if lines[k].startswith("|"))
        lines = lines[:last + 1] + [line] + lines[last + 1:]
        text = "\n".join(lines)
    else:
        text = text.rstrip("\n") + "\n\n" + section_text(m["target_page"]) + line + "\n"
    print("%s target %s %s" % (mode, fn, m["target_page"]))
    if a.apply:
        write(m["target_page"], text, crlf)


# adds: step 3 only (no source page, no source record)
for m in ADDS:
    add_target(m)

for m in MOVES:
    if not remove_source(m):
        continue
    note_record(m, "moved", {"moved_to": m["target_page"], "moved_by": "FABLE", "moved_on": CFG["date"],
                             "moved_record": "_index/candidates/" + REC, "review": m["review"]})
    add_target(m)

# drops: steps 1 and 2 only; no target
for m in DROPS:
    if not remove_source(m):
        continue
    note = {"dropped_by": "FABLE", "dropped_on": CFG["date"], "dropped_record": "_index/candidates/" + REC,
            "review": m["review"]}
    if "already_bound_on" in m:
        note["already_bound_on"] = m["already_bound_on"]["page"]
    else:
        note["unbound"] = m["unbound"]["reason"]
    note_record(m, "dropped", note)

print("FAILS", fails)
sys.exit(1 if fails else 0)
