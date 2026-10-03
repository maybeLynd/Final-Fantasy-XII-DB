"""build_moves.py - writes moves.json for AUDIT-SPEC batch 5 host-fit repairs (FABLE, 2026-10-03).

Built on fable-home-host-moves-b4-1003/build_moves.py. It covers:
- the REJECT review of fable-home-the-steal-roll-1003 (SWE2-AUDIT-SPEC commit 6435250e4): both rows move to the
  hosts its Repair block names, and the caller `0017FF20` is newly homed beside `001DD0B0` (an `adds` entry);
- the three rows batch 4 deferred (`004EB910`, `00361480`, `00314D60`).

Each moved row's text, entered_from and anchors are copied from its SOURCE PAGE's FABLE homed section as it stands
at HEAD, never retyped. The page is the source of truth because `004EB910`'s page text was corrected in 4534596f2
after its record was written; for the other rows page and record agree (checked here). One edit (CLEAN below):
`004EB910` moves with its corrected clause but without the strike and the dated note, because the target page never
said the struck text (publish_correction_gate refuses that strike).

`host` says why the target fits:
- caller:     the target cites the entered_from caller in its own text;
- callee:     the target states the listed functions as its own, and the body calls each of them directly
              (`why` adds one sentence on where the caller is named, written into the section's basis list);
- row-caller: the caller is homed in the same section by this record (an `adds` entry).

`drops` with `unbound` return a row to the frontier: no bearing page reads a caller or callee of the body as its own.
move_rows.py re-derives the raw transfer index into the body and the body's direct targets, and checks that every
bearing page that names one of them is listed with a quote showing it is a non-host mention.

    python -B build_moves.py      (rewrites moves.json beside it)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
C = os.path.join(DB, "_index", "candidates")
DATE = "2026-10-03"

TITLE = "16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md"
CON = "00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md"
VIF = "17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md"
VERBS = "01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md"
STEAL = "08-Combat-Formula/Steal/the-steal-roll.md"
BOOTP = "00-Engine-Core-Runtime/CONTRACT-boot-fixups.md"
INPUT = "15-Input/CONTRACT-input-subsystem.md"
CFGP = "19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md"

R_STEAL = "_index/candidates/auditspec-review-fable-home-the-steal-roll-1003/REVIEW.md"
R_BOOT = "_index/candidates/auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md"
R_INPUT = "_index/candidates/auditspec-review-fable-home-contract-input-subsystem-1002/REVIEW.md"
R_CFG = "_index/candidates/auditspec-review-fable-home-ff12config-and-debglobal-1002/REVIEW.md"

Q_TITLE = [(42, "| Selected handler | `00394070` at `00394498` | `003939B0` at `00394571` |"),
           (44, "RSI in `003939B0`")]
Q_CON_GET = [(120, "| `001DDAB0` | 8 B | ~~10 arms~~ 10 call sites (2 arms) | `return *(void **)0x01F82D18` |"),
             (258, "`01F82D18` is the `0x180`-byte display object `001DDAB0` returns")]
Q_CON_SET = [(599, "| `001DC920` (31 B) | paired field setter")]
Q_VIF = [(383, "status flags, set **only** by `0022CC40` (`|= 0x40`) and `0022CC30` (`|= 0x80`)"),
         (387, "calls `0022CC40` when it is"),
         (389, "Forty functions call them"),
         (724, "| `0022CC40` / `0022CC30` | VU sticky Z / sticky S |")]
Q_VERBS = [(201, "| `005C5230` | `xor eax, eax; ret` — the stub `poll`, reports \"done\" immediately |"),
           (247, "`0034FB20` (`disposesummon`) calls `00314D40(1)` and tail-jumps")]

MOVES = [
    # fn, source page, section date, source record, review, target, host, evidence
    ("00394380", STEAL, "2026-10-03", "fable-home-the-steal-roll-1003", R_STEAL, TITLE, {"by": "caller"}, Q_TITLE),
    ("001DD0B0", STEAL, "2026-10-03", "fable-home-the-steal-roll-1003", R_STEAL, CON, {"by": "row-caller"},
     Q_CON_SET),
    ("004EB910", BOOTP, "2026-10-02", "fable-home-contract-boot-fixups-1002", R_BOOT, VIF,
     {"by": "callee", "callees": ["0022CC40", "0022CC30"],
      "why": "Its caller `004EBE80` is named on no other page except as a program pointer the boot fixups register."},
     Q_VIF),
    ("00314D60", CFGP, "2026-10-02", "fable-home-ff12config-and-debglobal-1002", R_CFG, VERBS,
     {"by": "callee", "callees": ["005C5230"],
      "why": "Its caller `0050C8A0` is named on no other page except in a cross-subsystem neighbours line."},
     Q_VERBS),
]

ADDS = [{
    "fn": "0017FF20",
    "target_page": CON,
    "review": R_STEAL,
    "entered_from": "`0023B530` + 0xC5",
    # the sentence of R_STEAL's Repair item 2, as given there; verified at the bytes (README)
    "text": "calls `001DDAB0`; when it returns null returns that null, otherwise calls `001DDAB0` again and "
            "tail-jumps to `001DD0B0` with the result in `rcx`",
    "anchors": [["0017FF24", "call"], ["0017FF2C", "je"], ["0017FF2E", "call"], ["0017FF33", "mov"],
                ["0017FF3A", "jmp"]],
    "host": {"by": "callee", "callees": ["001DDAB0"],
             "why": "Its caller `0023B530` is read on the steal-roll page; SWE2-AUDIT-SPEC's review homes it here, "
                    "beside `001DD0B0`, the body it tail-jumps to."},
    "evidence": [{"line": l, "quote": q} for l, q in Q_CON_GET],
}]

DROPS = [{
    "fn": "00361480",
    "source_page": INPUT,
    "source_section_date": "2026-10-02",
    "source_record": "_index/candidates/fable-home-contract-input-subsystem-1002",
    "review": R_INPUT,
    "unbound": {
        "reason": "returned to the frontier: no host cites a caller or callee",
        # raw E8/E9 / 0F 8x / rel8 transfer index into the body, by owning function, and the body's direct targets
        "callers": {"00342770": ["003427F3"], "00341C80": ["00341C96"]},
        "callees": [],
        # every bearing page that names a caller or callee, with the line that shows it is not a host reading
        "cites": [{"addr": "00342770", "page": INPUT,
                   "quote": "56 script-verb bodies, among them `0033F330`, `00342770`"}],
    },
}]


def page_row(page, date, fn):
    lines = open(os.path.join(DB, *page.split("/")), encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    head = "## Homed frontier bodies called from this page's functions (FABLE, %s" % date
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    for l in lines[i + 1:]:
        if l.startswith("## "):
            break
        if l.startswith("| `%s` |" % fn):
            cells = [c.strip() for c in l.strip().strip("|").split(" | ")]
            return cells
    raise SystemExit("%s not in the FABLE section of %s" % (fn, page))


def record_row(rec, fn):
    r = json.load(open(os.path.join(DB, *rec.split("/"), "rows.json"), encoding="utf-8"))
    return next(x for x in r["rows"] if x["fn"] == fn)


# The one text edit: 004EB910's page row carries the 4534596f2 correction as a strike plus a dated note. The moved
# row keeps the corrected clause, word for word, and drops only the strike and the note.
CLEAN = {"004EB910": (
    "to ~~1.0 (`01E0283C`)~~ the sum of the `.data` floats `01E02838` + `01E0283C` (file values 0.0 and 1.0) "
    "*(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's review: `004EBD39` / `004EBD44` load and add the two cells, "
    "`004EBDD6` / `004EBDDE` store the sum)*,",
    "to the sum of the `.data` floats `01E02838` + `01E0283C` (file values 0.0 and 1.0),")}

out = {"date": DATE, "by": "FABLE",
       "target_heading": "## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 5)",
       "review_commits": {"steal-roll": "6435250e4", "batch-4 deferred": "95d495604"},
       "moves": [], "adds": ADDS, "drops": []}
for fn, src, date, rec, review, target, host, ev in MOVES:
    recp = "_index/candidates/" + rec
    cells = page_row(src, date, fn)
    rr = record_row(recp, fn)
    text = cells[3]
    if text != rr["text"]:
        print("NOTE %s: page text differs from the record (page is used)" % fn)
    anchors = [a[len("Interior anchor `"):-1] for a in cells[4].split("; ")]
    if anchors != [a for a, _ in rr["anchors"]] or cells[2] != rr["entered_from"]:
        raise SystemExit("%s: page anchors/site differ from the record" % fn)
    moved, edit = text, None
    if fn in CLEAN:
        old, new = CLEAN[fn]
        if text.count(old) != 1:
            raise SystemExit("%s: correction markup not found once in the page text" % fn)
        moved = text.replace(old, new)
        edit = {"why": "the target page never said the struck clause; publish_correction_gate refuses a strike of "
                       "text a page never said, so the row moves in its corrected form without the strike and note "
                       "(the correction stays recorded in fable-corr-004eb910-1003 and the source record)",
                "removed": old, "kept": new}
    out["moves"].append({
        "fn": fn, "source_page": src, "source_record": recp, "source_section_date": date, "review": review,
        "target_page": target, "entered_from": rr["entered_from"], "source_text": text, "text": moved,
        "text_edit": edit, "anchors": rr["anchors"], "host": host,
        "evidence": [{"line": l, "quote": q} for l, q in ev]})
for d in DROPS:
    rr = record_row(d["source_record"], d["fn"])
    cells = page_row(d["source_page"], d["source_section_date"], d["fn"])
    if cells[3] != rr["text"]:
        raise SystemExit("%s: page text differs from the record" % d["fn"])
    d = dict(d)
    d["source_text"] = rr["text"]
    out["drops"].append(d)
open(os.path.join(HERE, "moves.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print("moves %d, adds %d, drops %d" % (len(out["moves"]), len(out["adds"]), len(out["drops"])))
