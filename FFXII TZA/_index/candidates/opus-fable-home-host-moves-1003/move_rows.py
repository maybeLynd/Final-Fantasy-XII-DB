"""move_rows.py [--apply] [--root DIR] [--only FN,FN] - move FABLE-homed rows that SWE2-AUDIT-SPEC rejected for
host fit to the page each review names (OPUS, 2026-10-03).

moves.json beside this file (built by build_moves.py from the source records) lists, per row: the source page, the
source record, the target page, the row text and anchors, and quotes from the target page's own text that cite the
caller. The rows were reviewed exact (sentence, site, anchors) by SWE2-AUDIT-SPEC (commit 4522aeff6); only their host
was wrong. Two texts are edited so that bits are written as values; `text_edit` records each.

Verifies, in the certified image, exactly what the source homing_applier.py verified, against the TARGET page:
- every `entered_from` site is a direct call or jump to the function, from inside the named caller;
- every anchor is an instruction boundary strictly inside the function with the recorded mnemonic;
- no text has a pipe.
It also checks that the target page cites the caller outside the OPUS section this script writes, and that every
evidence quote is still on the target page.

Without --apply it only verifies, and reports what --apply would do.
With --apply, for each row (byte-preserving and CRLF-aware):
- SOURCE PAGE: removes the row's table line from the FABLE homed section dated `source_section_date`. When that
  leaves the section's table empty, removes the whole section, which is what the reviews call withdrawing it.
- SOURCE RECORD: removes the row from rows.json `rows` and appends it to a `moved` list, with the target and the
  date (indent=1, no trailing newline, as the records are written).
- TARGET PAGE: adds the row to one OPUS section, `target_heading`, appending the section when absent.
Idempotent: a step already done prints ALREADY, and a second --apply changes nothing.
--root runs against a COPY of the tree (the directory that holds `FFXII TZA`'s pages); the image always comes from
the certified kit. --only limits the run to the listed functions. Prints VERIFY, per-step PATCHED / ALREADY / DRY,
and FAILS n."""
import argparse, json, os, re, sys

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
a = ap.parse_args()
DB = os.path.abspath(a.root)
CFG = json.load(open(os.path.join(HERE, "moves.json"), encoding="utf-8"))
MOVES = [m for m in CFG["moves"] if not a.only or m["fn"] in a.only.upper().split(",")]
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


def row_line(m, size):
    site = m["entered_from"].strip()
    site = site if site.startswith("`") else "`%s`" % site
    src = m["source_page"]
    depth = "../" * m["target_page"].count("/")
    return "| `%s` | %d B | %s | %s | %s | [%s](%s%s) |" % (
        m["fn"], size, site, m["text"], "; ".join("Interior anchor `%s`" % x for x, _mn in m["anchors"]),
        os.path.splitext(os.path.basename(src))[0], depth, src)


def section_text(target_page):
    depth = "../" * target_page.count("/")
    return (HEAD + "\n\n"
            "*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). "
            "SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page "
            "cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because "
            "this page cites the caller in its own text. The sentence is unchanged except where `moves.json` "
            "records a bits-as-values edit. Each sentence states what the body does (access and representation, not "
            "purpose), and the anchors are instructions inside it that do it. Verified by "
            "[`move_rows.py`](%s_index/candidates/%s/move_rows.py): every site transfers to its function, this page "
            "cites the caller outside this section, and every anchor is an instruction boundary inside its function "
            "that decodes to the recorded mnemonic.*\n\n"
            "| function | size | entered from | what the body does | interior anchors | moved from |\n"
            "|---|---|---|---|---|---|\n" % (depth, REC))


# ---- verify
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
for m in MOVES:
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
    if not sm:
        fail("%s: entered_from %r is not `caller` + 0xNN" % (fn, m["entered_from"]))
    else:
        c, o = int(sm.group(1), 16), int(sm.group(2), 16)
        cn = sizes.get(c)
        ci = next(md.disasm(d[off(c + o):off(c + o) + 16], c + o), None) if cn and o < cn else None
        if not ci or ci.mnemonic not in ("call", "jmp") or not ci.operands or ci.operands[0].type != 2 \
                or ci.operands[0].imm != f:
            fail("%s: %s is not a direct call/jmp to it" % (fn, m["entered_from"]))
        elif sm.group(1) not in outside:
            fail("%s: the target page does not cite the caller %s outside the OPUS section" % (fn, sm.group(1)))
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
print("VERIFY %d functions, %d anchors, %d target pages" % (
    len(MOVES), sum(len(m["anchors"]) for m in MOVES), len({m["target_page"] for m in MOVES})))
if fails:
    print("FAILS", fails)
    sys.exit(1)

# ---- apply (or dry-run report)
mode = "PATCHED" if a.apply else "DRY"
for m in MOVES:
    fn = m["fn"]
    tag = "`%s`" % fn

    # 1. source page
    b, crlf = read(m["source_page"])
    lines = b.decode("utf-8").replace("\r\n", "\n").split("\n")
    sec = section_bounds(lines, FABLE_HEAD % m["source_section_date"])
    hit = [i for i in range(*sec) if lines[i].startswith("| %s |" % tag)] if sec else []
    if not hit:
        print("ALREADY source %s %s" % (fn, m["source_page"]))
    else:
        i = hit[0]
        if m["source_text"] not in lines[i]:
            fail("%s: source row text differs from the record" % fn)
            continue
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

    # 2. source record
    rp = os.path.join(DB, *m["source_record"].split("/"), "rows.json")
    rec = json.load(open(rp, encoding="utf-8"))
    row = next((r for r in rec["rows"] if r["fn"] == fn), None)
    if row is None:
        print("ALREADY record %s %s" % (fn, m["source_record"]))
    else:
        rec["rows"] = [r for r in rec["rows"] if r["fn"] != fn]
        moved = dict(row)
        moved.update({"moved_to": m["target_page"], "moved_by": "OPUS", "moved_on": CFG["date"],
                      "moved_record": "_index/candidates/" + REC, "review": m["review"]})
        rec.setdefault("moved", []).append(moved)
        print("%s record %s %s" % (mode, fn, m["source_record"]))
        if a.apply:
            open(rp, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1, ensure_ascii=True))

    # 3. target page
    b, crlf = read(m["target_page"])
    text = b.decode("utf-8").replace("\r\n", "\n")
    lines = text.split("\n")
    line = row_line(m, sizes[int(fn, 16)])
    own = section_bounds(lines, HEAD)
    if own and any(lines[k].startswith("| %s |" % tag) for k in range(*own)):
        print("ALREADY target %s %s" % (fn, m["target_page"]))
        continue
    if own:
        last = max(k for k in range(*own) if lines[k].startswith("|"))
        lines = lines[:last + 1] + [line] + lines[last + 1:]
        text = "\n".join(lines)
    else:
        text = text.rstrip("\n") + "\n\n" + section_text(m["target_page"]) + line + "\n"
    print("%s target %s %s" % (mode, fn, m["target_page"]))
    if a.apply:
        write(m["target_page"], text, crlf)

print("FAILS", fails)
sys.exit(1 if fails else 0)
