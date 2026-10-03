"""move_rows.py [--apply] [--root DIR] [--only FN,FN] [--moves FILE] - FABLE's batch-6 host-fit repairs (FABLE,
2026-10-03; SWE2-AUDIT-SPEC's REJECT and ACCEPT-WITH-NARROWING reviews of FABLE's 1003 homing records).

Copy of fable-home-host-moves-b5-1003/move_rows.py, changed for:
- THE HOST RULE (subjects.py): a host must document the caller - or, for `host: callee`, each callee - as a SUBJECT
  outside this record's section: an address in a heading, the first address of a table row, or the first address of
  a paragraph or list item. b5 asked only that the address occur on the page.
- `host: thunk`: the entered_from caller is a thunk (a body that is one `jmp` to the function); the host documents
  each listed caller of the thunk as a subject, every listed site calls or jumps to the thunk, and the section carries
  the review's line naming the thunk as the lead of its own bullet.
- `text_edit` on a move: the review's replacement wording; the target receives the new text (it never said the old).
  `lea_checks` confirm a named address at the bytes.
- `edits`: a row that stays on its page and only changes text. Each struck span must occur on that row the recorded
  number of times (a strike only strikes real text); the cell becomes `~~old~~ new` per span plus a dated note, and
  the record's rows.json text is set to the new cell (its applier then prints ALREADY). The record keeps the edit in
  a `narrowed` list.
- `drops` with `host_fails`: the row leaves its rejected host for the frontier because the host the review names
  does not document the caller. Verify re-derives the raw transfer index into the body (E8/E9 rel32, 0F 8x rel32,
  EB/7x rel8, each decoded as a direct call or jump to the entry) by owning function, which must equal the record;
  on each named page the caller must NOT be a subject, and each quoted passing mention must still be there. It also
  prints, for information, every bearing page where a caller is a subject (LEAD lines), which is where the row can
  be re-homed later. `already_bound_on` drops are kept from b4.
- `target_before`: a target section is inserted before the named heading instead of at the end of the page.

Verifies, in the certified image, for every move against its TARGET page: every `entered_from` site is a direct call
or jump to the function from inside the named caller; every anchor is an instruction boundary strictly inside the
function with the recorded mnemonic; no text has a pipe; the host basis above; every evidence quote is still on the
target page.

Without --apply it only verifies, and reports what --apply would do (DRY). With --apply (byte-preserving, CRLF-aware):
SOURCE PAGE loses the row from its FABLE homed section (the whole section when it empties); SOURCE RECORD moves the
row from `rows` to `moved` / `dropped`; TARGET PAGE gains the row in this record's section; EDIT pages and records are
narrowed in place. Idempotent: a step already done prints ALREADY. --root runs against a COPY of the tree (the
directory that holds the pages); the image always comes from the certified kit. --only limits the run to the listed
functions. Prints VERIFY, per-step PATCHED / ALREADY / DRY, and FAILS n."""
import argparse, bisect, json, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REAL_DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(REAL_DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import subjects  # noqa: E402
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
from capstone.x86 import X86_REG_RIP  # noqa: E402

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
EDITS = [m for m in CFG.get("edits", []) if not ONLY or m["fn"] in ONLY]
DROPS = [m for m in CFG.get("drops", []) if not ONLY or m["fn"] in ONLY]
HEAD = CFG["target_heading"]
BEFORE = CFG.get("target_before", {})
REC = os.path.basename(HERE)
SITE = re.compile(r"`?([0-9A-F]{8})`?\s*\+\s*0x([0-9A-Fa-f]+)")
FABLE_HEAD = "## Homed frontier bodies called from this page's functions (FABLE, %s"
NOTE = " *(narrowed %s, FABLE, on SWE2-AUDIT-SPEC's review: %s)*"
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


def text_lines(rel):
    return open(path(rel), "rb").read().decode("utf-8").replace("\r", "").split("\n")


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


def site_parts(s):
    m = SITE.fullmatch(s.strip())
    return (m.group(1), int(m.group(2), 16)) if m else (None, None)


def row_line(m, size):
    site = m["entered_from"].strip()
    site = site if site.startswith("`") else "`%s`" % site
    depth = "../" * m["target_page"].count("/")
    src = m["source_page"]
    frm = "[%s](%s%s)" % (os.path.splitext(os.path.basename(src))[0], depth, src)
    return "| `%s` | %d B | %s | %s | %s | %s |" % (
        m["fn"], size, site, m["text"], "; ".join("Interior anchor `%s`" % x for x, _mn in m["anchors"]), frm)


KIND = {"heading": "a heading", "row": "a table row", "paragraph": "a paragraph", "item": "a list item"}


def kinds(m, addr):
    ks = []
    for e in m["evidence"]:
        if e["addr"] == addr and KIND[e["kind"]] not in ks:
            ks.append(KIND[e["kind"]])
    return ", ".join(ks)


def basis(m):
    h = m["host"]
    fn = m["fn"]
    c = site_parts(m["entered_from"])[0]
    out = []
    if h["by"] == "caller":
        s = "`%s`: this page documents its caller `%s` as a subject (%s)." % (fn, c, kinds(m, c))
    elif h["by"] == "callee":
        s = "`%s`: this page documents %s as a subject, which the body calls directly." % (
            fn, " and ".join("`%s`" % x for x in h["callees"]))
    else:
        out.append("- %s." % h["lead"])
        cs = [site_parts(x)[0] for x in h["thunk_callers"]]
        s = "`%s`: its caller is the thunk `%s` (the line above); this page documents %s as subjects (%s)." % (
            fn, h["thunk"], " and ".join("`%s`" % x for x in cs), "; ".join(kinds(m, x) for x in cs))
    if h.get("why"):
        s += " " + h["why"]
    if m.get("text_edit"):
        s += " The sentence carries the review's replacement wording (%s)." % m["text_edit"]["why"]
    out.append("- " + s)
    return "\n".join(out)


def section_text(target_page):
    depth = "../" * target_page.count("/")
    rows = [m for m in CFG["moves"] if m["target_page"] == target_page]
    return (HEAD + "\n\n"
            "*FABLE's homing stream (cloud-drafted, FABLE-verified) homed these bodies on other pages. SWE2-AUDIT-SPEC "
            "reviewed each sentence, site and anchor set and rejected the host, because that page named the caller "
            "only in passing. The sentences are unchanged except where the review gave replacement wording, which "
            "the row's line below says. Each states what the body does (access and representation, not purpose), "
            "and the anchors are instructions inside it that do it. Why each row is here:*\n\n"
            + "\n".join(basis(m) for m in rows) + "\n\n"
            "*Verified by [`move_rows.py`](%s_index/candidates/%s/move_rows.py): every site transfers to its "
            "function; the caller named above (for a thunk, the thunk's callers) is a subject of this page outside "
            "this section - an address in a heading, the first address of a table row, or the first address of a "
            "paragraph or list item; and every anchor is an instruction boundary inside its function that decodes "
            "to the recorded mnemonic.*\n\n"
            "| function | size | entered from | what the body does | interior anchors | moved from |\n"
            "|---|---|---|---|---|---|\n" % (depth, REC))


def marked(source_text, spans, why):
    t = source_text
    for old, new, n in spans:
        if t.count(old) != n:
            return None
        t = t.replace(old, "~~%s~~ %s" % (old, new))
    return t + NOTE % (CFG["date"], why)


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


def raw_callers(targets):
    """{target hex: {owner entry hex: [site hex, ...]}} for every decoded direct transfer to a target in .text."""
    T = {int(x, 16) for x in targets}
    tva, tpr, n = text_section()
    b = d[tpr:tpr + n]
    out = {x: {} for x in targets}
    for i in range(n - 1):
        op = b[i]
        t = None
        if op in (0xE8, 0xE9) and i + 5 <= n:
            t = tva + i + 5 + struct.unpack_from("<i", b, i + 1)[0]
        elif op == 0x0F and i + 6 <= n and 0x80 <= b[i + 1] <= 0x8F:
            t = tva + i + 6 + struct.unpack_from("<i", b, i + 2)[0]
        elif op == 0xEB or 0x70 <= op <= 0x7F:
            t = tva + i + 2 + struct.unpack_from("<b", b, i + 1)[0]
        if t in T and direct_to(decode1(tva + i), t):
            o = owner(tva + i)
            out["%08X" % t].setdefault("%08X" % o if o else "unlisted", []).append("%08X" % (tva + i))
    return out


def bearing_pages():
    for r, ds, fs in os.walk(DB):
        ds[:] = [x for x in ds if not x.startswith((".", "_"))]
        for x in fs:
            if x.endswith(".md"):
                yield os.path.relpath(os.path.join(r, x), DB).replace(os.sep, "/")


def check_site(fn, f, s):
    """the site is a direct call/jmp to f from inside its named function; returns the function hex or None."""
    c, o = site_parts(s)
    if c is None:
        fail("%s: site %r is not `function` + 0xNN" % (fn, s))
        return None
    cn = sizes.get(int(c, 16))
    ci = decode1(int(c, 16) + o) if cn and o < cn else None
    if not ci or ci.mnemonic not in ("call", "jmp") or not direct_to(ci, f):
        fail("%s: %s is not a direct call/jmp to %08X" % (fn, s, f))
        return None
    return c


# ---- verify
for m in MOVES:
    fn = m["fn"]
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        fail("%s: not a function entry" % fn)
        continue
    tl = text_lines(m["target_page"])
    own = section_bounds(tl, HEAD)
    skip = own if own else None
    outside = "\n".join(tl[:own[0]] + tl[own[1]:]) if own else "\n".join(tl)
    host = m["host"]
    c = check_site(fn, f, m["entered_from"])
    if c and host["by"] == "caller" and not subjects.subject_lines(tl, c, skip):
        fail("%s: the target page does not document the caller %s as a subject outside the batch-6 section" % (fn, c))
    if host["by"] == "callee":
        tg = {t.operands[0].imm for t in md.disasm(d[off(f):off(f) + n], f)
              if t.operands and t.operands[0].type == 2 and (t.mnemonic in ("call", "jmp") or t.mnemonic.startswith("j"))}
        for x in host["callees"]:
            if int(x, 16) not in tg:
                fail("%s: the body does not call %s directly" % (fn, x))
            if not subjects.subject_lines(tl, x, skip):
                fail("%s: the target page does not document the callee %s as a subject" % (fn, x))
    if host["by"] == "thunk":
        th = host["thunk"]
        tn = sizes.get(int(th, 16))
        body = list(md.disasm(d[off(int(th, 16)):off(int(th, 16)) + (tn or 0)], int(th, 16)))
        if c != th:
            fail("%s: entered_from caller %s is not the thunk %s" % (fn, c, th))
        if not tn or len(body) != 1 or not direct_to(body[0], f) or body[0].mnemonic != "jmp":
            fail("%s: %s is not a one-instruction jmp thunk to it" % (fn, th))
        for s in host["thunk_callers"]:
            x = check_site(fn, int(th, 16), s)
            if x and not subjects.subject_lines(tl, x, skip):
                fail("%s: the target page does not document the thunk's caller %s as a subject" % (fn, x))
            if s not in host["lead"]:
                fail("%s: the lead line does not name the thunk site %s" % (fn, s))
        if th not in host["lead"] or fn not in host["lead"]:
            fail("%s: the lead line does not name the thunk and the body" % fn)
    if host["by"] not in ("caller", "callee", "thunk"):
        fail("%s: unknown host basis %r" % (fn, host["by"]))
    for e in m["evidence"]:
        if e["quote"] not in outside:
            fail("%s: evidence quote no longer on the target page: %r" % (fn, e["quote"][:60]))
    for site, want in m.get("lea_checks", []):
        ci = decode1(int(site, 16))
        ok = ci and ci.mnemonic == "lea" and len(ci.operands) == 2 and ci.operands[1].mem.base == X86_REG_RIP \
            and ci.address + ci.size + ci.operands[1].mem.disp == int(want, 16)
        if not ok:
            fail("%s: %s does not load %s" % (fn, site, want))
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for x, mn in m["anchors"]:
        av = int(x, 16)
        if not (f < av < f + n):
            fail("%s: anchor %s outside the body" % (fn, x))
        elif ins.get(av) != mn:
            fail("%s: %s decodes to %r, recorded %r" % (fn, x, ins.get(av), mn))
    if "|" in m["text"]:
        fail("%s: pipe in text" % fn)
    te = m.get("text_edit")
    if te and (m["source_text"].count(te["removed"]) != 1 or m["source_text"].replace(te["removed"], te["kept"]) != m["text"]):
        fail("%s: text_edit does not turn the source text into the moved text" % fn)
    if not te and m["text"] != m["source_text"]:
        fail("%s: moved text differs from the source text with no text_edit" % fn)
for tp, h in BEFORE.items():
    if tp in {m["target_page"] for m in MOVES}:
        hits = [l for l in text_lines(tp) if l.startswith(h)]
        if len(hits) != 1:
            fail("%s: the insert-before heading %r occurs %d times" % (tp, h, len(hits)))
for e in EDITS:
    fn = e["fn"]
    new = marked(e["source_text"], e["spans"], e["why"])
    if new is None:
        fail("%s: a struck span does not occur on the row the recorded number of times" % fn)
        continue
    if "|" in new:
        fail("%s: pipe in text" % fn)
    plain = e["source_text"]
    for old, nw, _n in e["spans"]:
        plain = plain.replace(old, nw)
    if plain != e["plain"]:
        fail("%s: the spans do not give the recorded wording" % fn)
    tl = text_lines(e["page"])
    sec = section_bounds(tl, e["section"])
    row = [tl[k] for k in range(*sec) if tl[k].startswith("| `%s` |" % fn)] if sec else []
    if len(row) != 1 or (" | %s | " % e["source_text"] not in row[0] and " | %s | " % new not in row[0]):
        fail("%s: the row on %s is neither the recorded text nor its narrowed form" % (fn, e["page"]))
LEADS = {}
HF = [m for m in DROPS if "host_fails" in m]
if HF:
    want = sorted({c for m in HF for c in m["host_fails"]["callers"]})
    rc = raw_callers(sorted({m["fn"] for m in HF}))
    pages = {}
    for p in bearing_pages():
        t = open(path(p), "rb").read().decode("utf-8", "replace")
        if any(c in t for c in want):
            pages[p] = t.replace("\r", "").split("\n")
    for c in want:
        LEADS[c] = sorted("%s (L%d %s)" % (p, ln, k) for p, ls in pages.items() for k, ln in subjects.subject_lines(ls, c))
for m in DROPS:
    fn = m["fn"]
    f = int(fn, 16)
    if not sizes.get(f):
        fail("%s: not a function entry" % fn)
        continue
    if "already_bound_on" in m:
        bp = m["already_bound_on"]
        if bp["quote"] not in "\n".join(text_lines(bp["page"])) or fn not in bp["quote"]:
            fail("%s: already-bound quote no longer on %s: %r" % (fn, bp["page"], bp["quote"][:60]))
        continue
    hf = m["host_fails"]
    if rc[fn] != hf["callers"]:
        fail("%s: raw callers %s, recorded %s" % (fn, rc[fn], hf["callers"]))
    for pg in hf["pages"]:
        ls = text_lines(pg["page"])
        if pg["addr"] not in hf["callers"]:
            fail("%s: %s is not a recorded caller" % (fn, pg["addr"]))
        sl = subjects.subject_lines(ls, pg["addr"])
        if sl:
            fail("%s: %s documents the caller %s as a subject (%s) - the row has a host there" % (
                fn, pg["page"], pg["addr"], ", ".join("L%d %s" % (ln, k) for k, ln in sl)))
        for q in pg["quotes"]:
            if q not in "\n".join(ls) or pg["addr"] not in q:
                fail("%s: passing-mention quote no longer on %s: %r" % (fn, pg["page"], q[:60]))
    print("HOST-FAILS %s raw callers %s; named host(s) %s: caller not a subject" % (
        fn, ", ".join("%s (%s)" % (k, "/".join(v)) for k, v in sorted(rc[fn].items())),
        ", ".join(os.path.basename(p["page"]) for p in hf["pages"])))
for c, ls in sorted(LEADS.items()):
    print("LEAD %s is a subject on %d bearing page(s)%s" % (c, len(ls), (": " + "; ".join(ls)) if ls else ""))
print("VERIFY %d functions, %d anchors, %d target pages, %d edits, %d drops" % (
    len(MOVES), sum(len(m["anchors"]) for m in MOVES), len({m["target_page"] for m in MOVES}), len(EDITS),
    len(DROPS)))
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
    elif m["target_page"] in BEFORE:
        k = next(i for i, l in enumerate(lines) if l.startswith(BEFORE[m["target_page"]]))
        block = (section_text(m["target_page"]) + line + "\n").rstrip("\n").split("\n")
        text = "\n".join(lines[:k] + block + [""] + lines[k:])
    else:
        text = text.rstrip("\n") + "\n\n" + section_text(m["target_page"]) + line + "\n"
    print("%s target %s %s" % (mode, fn, m["target_page"]))
    if a.apply:
        write(m["target_page"], text, crlf)


def narrow(e):
    """Edits: strike-and-replace on the page row, and the same cell text into the record's rows.json."""
    fn = e["fn"]
    new = marked(e["source_text"], e["spans"], e["why"])
    b, crlf = read(e["page"])
    lines = b.decode("utf-8").replace("\r\n", "\n").split("\n")
    sec = section_bounds(lines, e["section"])
    i = next(k for k in range(*sec) if lines[k].startswith("| `%s` |" % fn))
    if " | %s | " % new in lines[i]:
        print("ALREADY page %s %s" % (fn, e["page"]))
    else:
        old = " | %s | " % e["source_text"]
        if lines[i].count(old) != 1:
            fail("%s: the row text is not on the page once" % fn)
            return
        lines[i] = lines[i].replace(old, " | %s | " % new)
        print("%s page %s %s" % (mode, fn, e["page"]))
        if a.apply:
            write(e["page"], "\n".join(lines), crlf)
    rp = os.path.join(DB, *e["record"].split("/"), "rows.json")
    rec = json.load(open(rp, encoding="utf-8"))
    row = next(r for r in rec["rows"] if r["fn"] == fn)
    if row["text"] == new:
        print("ALREADY record %s %s" % (fn, e["record"]))
        return
    if row["text"] != e["source_text"]:
        fail("%s: the record's text is neither the recorded text nor its narrowed form" % fn)
        return
    row["text"] = new
    rec.setdefault("narrowed", []).append({
        "fn": fn, "by": "FABLE", "on": CFG["date"], "record": "_index/candidates/" + REC, "review": e["review"],
        "struck": [[o, nw] for o, nw, _n in e["spans"]], "previous_text": e["source_text"], "plain": e["plain"]})
    print("%s record %s %s" % (mode, fn, e["record"]))
    if a.apply:
        open(rp, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, ensure_ascii=True))


for m in MOVES:
    if not remove_source(m):
        continue
    note = {"moved_to": m["target_page"], "moved_by": "FABLE", "moved_on": CFG["date"],
            "moved_record": "_index/candidates/" + REC, "review": m["review"]}
    if m.get("text_edit"):
        note["moved_text"] = m["text"]
        note["text_edit"] = m["text_edit"]
    note_record(m, "moved", note)
    add_target(m)

for e in EDITS:
    narrow(e)

# drops: steps 1 and 2 only; no target
for m in DROPS:
    if not remove_source(m):
        continue
    note = {"dropped_by": "FABLE", "dropped_on": CFG["date"], "dropped_record": "_index/candidates/" + REC,
            "review": m["review"]}
    if "already_bound_on" in m:
        note["already_bound_on"] = m["already_bound_on"]["page"]
    else:
        note["host_fails"] = m["host_fails"]["reason"]
    note_record(m, "dropped", note)

print("FAILS", fails)
sys.exit(1 if fails else 0)
