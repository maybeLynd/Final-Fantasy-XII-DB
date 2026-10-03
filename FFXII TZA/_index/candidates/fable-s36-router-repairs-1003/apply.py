"""apply.py - FABLE, 2026-10-03: stage the S-36 router repairs (SWE2-AUDIT-SEM S-36 D2, point 3, D3).

  python apply.py            dry run: check every anchor, show what would change, write nothing
  python apply.py --apply    write the edits (only when every check passes)

Edits:
  E1  16-UI/CONTRACT-ui-request-router.md: insert section_3a.txt after section 3, before the line "## 4. The three refusals".
  E2  16-UI/CONTRACT-ui-request-router.md: insert section_5a.txt after section 5, before the line "## 6. The invariants".
  E3  _index/L2-VERDICTS.md line 255 (the S-36 row): replace OLD 1 -> NEW 1 and OLD 2 -> NEW 2 from d3_replacement.txt.
      The cell is SWE2-AUDIT-SEM's; this edit is staged for that lane's acceptance (README, consumer check).

Guards:
  - a page with uncommitted content changes (git diff HEAD) is REFUSED, and so is a page the index differs on;
  - every anchor heading must occur exactly once and in order (3 < 4 < 5 < 6), and every OLD text exactly once on line 255;
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: an edit whose result is already present is reported ALREADY and skipped;
  - the staged contract is run through contract_named_state_census's own section parser: 5a must be read as a state
    section and 3a must not; with fields_proposal.tsv + types_proposal.tsv loaded into the store, 5a must resolve with
    0 UNDECLARED rows;
  - no NEW text may contain a '|' (it would split the register row).

Prints FAILS N last.
"""
import csv
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
CONTRACT = os.path.join(DB, "16-UI", "CONTRACT-ui-request-router.md")
VERDICTS = os.path.join(DB, "_index", "L2-VERDICTS.md")
APPLY = "--apply" in sys.argv
fails = 0


def report(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)


def dirty(p):
    a = git("diff", "--quiet", "HEAD", "--", rel(p)).returncode
    b = git("diff", "--quiet", "--cached", "--", rel(p)).returncode
    return a != 0 or b != 0


def load(p):
    raw = io.open(p, "rb").read()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), eol


def section_text(name):
    t = io.open(os.path.join(HERE, name), encoding="utf-8").read().replace("\r\n", "\n")
    return t.rstrip("\n") + "\n"


def insert_before(text, heading_re, block, marker):
    if marker in text:
        return text, "ALREADY"
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if re.match(heading_re, l)]
    if len(idx) != 1:
        return None, "anchor %r found %d times" % (heading_re, len(idx))
    i = idx[0]
    new = lines[:i] + block.rstrip("\n").split("\n") + [""] + lines[i:]
    if i > 0 and lines[i - 1].strip():
        new = lines[:i] + [""] + block.rstrip("\n").split("\n") + [""] + lines[i:]
    return "\n".join(new), "inserted before line %d (%s)" % (i + 1, lines[i][:40])


def parse_d3():
    t = io.open(os.path.join(HERE, "d3_replacement.txt"), encoding="utf-8").read().replace("\r\n", "\n")
    blocks = {}
    for m in re.finditer(r"^=== (OLD \d|NEW \d) ===\n(.*?)\n(?==== )", t, re.M | re.S):
        blocks[m.group(1)] = m.group(2).strip()
    return blocks


print("FABLE S-36 router repairs, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
head = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
print("HEAD %s" % head)

# ---- E1 / E2 on the contract ----
cdirty = dirty(CONTRACT)
report("G1", not cdirty, "%s is %s" % (rel(CONTRACT), "DIRTY - refused (uncommitted content changes)" if cdirty else "clean"))
if cdirty:
    src = git("show", "HEAD:" + rel(CONTRACT)).stdout.decode("utf-8")
    _, ceol = load(CONTRACT)
    print("      staging against the HEAD blob instead, to check the anchors; nothing can be applied")
else:
    src, ceol = load(CONTRACT)
src = src.replace("\r\n", "\n")
print("      line endings kept: %s" % ("CRLF" if ceol == "\r\n" else "LF"))
order = []
for h in (r"^## 3\. Dispatch\s*$", r"^## 4\. The three refusals", r"^## 5\. The mailbox is a single slot", r"^## 6\. The invariants"):
    hits = [i for i, l in enumerate(src.split("\n")) if re.match(h, l)]
    order.append(hits[0] if len(hits) == 1 else None)
    report("A%d" % len(order), len(hits) == 1, "anchor %s occurs %d time(s)%s" % (h, len(hits),
                                                                                    " at line %d" % (hits[0] + 1) if len(hits) == 1 else ""))
report("A5", None not in order and order == sorted(order), "anchors are in order 3 < 4 < 5 < 6: %s" % [o and o + 1 for o in order])
s3a, s5a = section_text("section_3a.txt"), section_text("section_5a.txt")
staged, m1 = insert_before(src, r"^## 4\. The three refusals", s3a, "## 3a. Pre-emption of the open UI")
report("E1", staged is not None, "3a %s" % m1)
staged2, m2 = insert_before(staged or src, r"^## 6\. The invariants", s5a, "## 5a. State (FABLE, 2026-10-03")
report("E2", staged2 is not None, "5a %s" % m2)
staged = staged2 or staged or src
lines = staged.split("\n")
pos = {k: next((i for i, l in enumerate(lines) if l.startswith(k)), None)
       for k in ("## 3. Dispatch", "## 3a.", "## 4.", "## 5. The mailbox", "## 5a.", "## 6.")}
report("E3x", all(v is not None for v in pos.values()) and pos["## 3. Dispatch"] < pos["## 3a."] < pos["## 4."]
       < pos["## 5. The mailbox"] < pos["## 5a."] < pos["## 6."],
       "staged order 3 < 3a < 4 < 5 < 5a < 6: %s" % {k: (v + 1 if v is not None else None) for k, v in pos.items()})
link = "../_index/candidates/fable-s36-router-repairs-1003/census_router_state.py"
report("L1", os.path.exists(os.path.normpath(os.path.join(os.path.dirname(CONTRACT), link))),
       "5a's census link resolves from the contract's folder")

# ---- the census parser on the staged page ----
sys.path.insert(0, KIT)
import contract_named_state_census as C  # noqa: E402
import check_static_spans as SS  # noqa: E402
secs = {}
for sec, line, fenced in C.state_sections(staged):
    secs.setdefault(sec, []).append(line)
s5 = [k for k in secs if k.startswith("5a. State")]
s3 = [k for k in secs if k.startswith("3a.")]
report("C1", bool(s5), "the census reads 5a as a state section: %s" % (s5 or "NO"))
report("C2", not s3, "the census does not read 3a as a state section")
spans, fields, sizes = C.load_store()


def classify(spans_, fields_, sizes_):
    out, seen = [], set()
    for sec in s5:
        for line in secs[sec]:
            for m in C.ADDR.finditer(line):
                v = int(m.group(1), 16)
                if v in seen:
                    continue
                if C.DATA_LO <= v < C.DATA_HI:
                    seen.add(v)
                    out.append(("%08X" % v, C.resolve(v, spans_, fields_, sizes_)[0]))
                elif C.RDATA_LO <= v < C.DATA_LO:
                    seen.add(v)
                    out.append(("%08X" % v, "CONSTANT"))
    return out


before = classify(spans, fields, sizes)
print("      5a rows against the store at HEAD: %s" % before)
for r in csv.DictReader(io.open(os.path.join(HERE, "types_proposal.tsv"), encoding="utf-8"), delimiter="\t",
                        quoting=csv.QUOTE_NONE):
    size = int(r["size"], 16)
    sizes[r["type"]] = size
    for kind, lo, hi, text in SS.spans_from(r["type"], r["route"], size):
        mm = re.search(r"stride=(0x[0-9A-Fa-f]+|\d+)", text)
        spans.append((lo, hi, r["type"], kind, int(mm.group(1), 0) if mm else None))
for r in csv.DictReader(io.open(os.path.join(HERE, "fields_proposal.tsv"), encoding="utf-8"), delimiter="\t",
                        quoting=csv.QUOTE_NONE):
    fields[r["type"]].append((int(r["offset"], 16), int(r["size"]), r["name"], r["readiness"], r["ctype"]))
after = classify(spans, fields, sizes)
print("      5a rows with the two proposals loaded: %s" % after)
und = [a for a, c in after if c == "UNDECLARED"]
report("C3", not und, "with the proposals, 5a has %d rows and %d UNDECLARED %s" % (len(after), len(und), und))

# ---- E3 on L2-VERDICTS.md ----
vdirty = dirty(VERDICTS)
report("G2", not vdirty, "%s is %s" % (rel(VERDICTS), "DIRTY - refused" if vdirty else "clean"))
vsrc, veol = load(VERDICTS)
if vdirty:
    vsrc = git("show", "HEAD:" + rel(VERDICTS)).stdout.decode("utf-8").replace("\r\n", "\n")
print("      line endings kept: %s" % ("CRLF" if veol == "\r\n" else "LF"))
d3 = parse_d3()
report("D0", sorted(d3) == ["NEW 1", "NEW 2", "OLD 1", "OLD 2"], "d3_replacement.txt blocks: %s" % sorted(d3))
vl = vsrc.split("\n")
row = vl[254] if len(vl) > 254 else ""
report("R1", row.startswith("| **S-36**"), "line 255 is the S-36 row")
for k in ("1", "2"):
    old, new = d3.get("OLD " + k, ""), d3.get("NEW " + k, "")
    report("D%sp" % k, "|" not in new, "NEW %s carries no '|'" % k)
    if new and new in row and old not in row:
        print("      OLD %s -> NEW %s: ALREADY" % (k, k))
        continue
    n = row.count(old) if old else 0
    report("D%s" % k, n == 1, "OLD %s occurs %d time(s) on line 255" % (k, n))
    if n == 1:
        row = row.replace(old, new)
        print("      OLD %s -> NEW %s: %d chars -> %d chars" % (k, k, len(old), len(new)))
cells_before = vl[254].count("|") if len(vl) > 254 else 0
report("D3", row.count("|") == cells_before, "line 255 keeps its %d cell separators" % cells_before)
vstaged = "\n".join(vl[:254] + [row] + vl[255:])

# ---- write ----
if APPLY:
    if fails:
        print("NOT APPLIED: %d check(s) failed" % fails)
    else:
        # --contract-only (FABLE, 2026-10-03): the L2-VERDICTS step E3 waits for SWE2-AUDIT-SEM's acceptance
        targets = ((CONTRACT, staged, ceol, src),) if "--contract-only" in sys.argv else \
            ((CONTRACT, staged, ceol, src), (VERDICTS, vstaged, veol, vsrc))
        for p, txt, eol, orig in targets:
            if txt == orig:
                print("      %s unchanged (ALREADY)" % rel(p))
                continue
            io.open(p, "wb").write(txt.replace("\n", eol).encode("utf-8"))
            back, _ = load(p)
            report("W", back == txt, "wrote %s" % rel(p))
else:
    print("      dry run: contract +%d lines, L2-VERDICTS line 255 %s" % (
        len(staged.split("\n")) - len(src.split("\n")), "changed" if vstaged != vsrc else "unchanged"))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
