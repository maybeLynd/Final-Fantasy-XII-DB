#!/usr/bin/env python3
"""uc1_pass2_extent_rows.py - pass 2 of the UC-1 citation worklist, the extent rows (OPUS, 2026-09-25).

Pass 1 (uc1_citation_worklist.py) flagged cited addresses that lie past the previous listed body's end
while that body appears to branch into the gap. Those are extent questions: is the cited address the
INTERIOR of the previous function whose listed size is short, or a separate, unlisted function?

EVIDENCE RULE. FINAL-AUDIT-PROTOCOL pass 6 bans .pdata / unwind metadata as supporting evidence, so
this uses CODE ONLY: a recursive-descent walk from the previous listed entry that follows fall-through,
jcc and jmp (direct targets only), stops at ret / int3 / an indirect jmp / a call to a no-return
target it cannot know, and never follows calls. If the walk reaches the cited address, the address is
the INTERIOR of that function and the listed size is short; if it does not, the address is reached
only from elsewhere (its own callers / pointers) or not at all. Read-only.

    uc1_pass2_extent_rows.py [--out rows.tsv]
"""
import argparse
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import check_default_instance_writers as W  # noqa: E402
from capstone.x86 import X86_OP_IMM  # noqa: E402

WORKLIST = "_index/candidates/uc1-citation-worklist-pass1.tsv"
ADMISSIONS = "99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv"
LIMIT = 0x4000


def walk(img, entry, stop_at=None):
    """Recursive descent from entry, jumps only. Returns (visited instruction set, max end)."""
    seen, todo, end = set(), [entry], entry
    while todo:
        a = todo.pop()
        while a not in seen and entry <= a < entry + LIMIT:
            b = img.read(a, 16)
            if not b:
                break
            ins = next(img.md.disasm(b, a), None)
            if ins is None:
                break
            seen.add(a)
            end = max(end, a + ins.size)
            m = ins.mnemonic
            if m in ("ret", "int3", "ud2") or (m == "jmp" and ins.operands[0].type != X86_OP_IMM):
                break
            if m.startswith("j") and ins.operands and ins.operands[0].type == X86_OP_IMM:
                t = ins.operands[0].imm
                if m == "jmp":
                    if entry <= t < entry + LIMIT and t not in img.sizes or t == entry:
                        a = t
                        continue
                    break                                  # tail jump to a listed body
                todo.append(t)
            a += ins.size
    return seen, end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    img = W.Image()
    rows = list(csv.DictReader(io.open(os.path.join(G.DB, WORKLIST), encoding="utf-8"), delimiter="\t"))
    rows = [r for r in rows if r["prev_reach"] in ("PREV-BRANCHES-INTO-GAP", "BRANCH-FROM-PREV")]
    # The residual population's own adjudication of the block that contains each address.
    adm = []
    for line in io.open(os.path.join(G.DB, ADMISSIONS), encoding="utf-8"):
        c = line.rstrip("\r\n").split("\t")
        if line.startswith("#") or len(c) < 10 or not c[1].isdigit():
            continue
        adm.append((int(c[0], 16), int(c[1]), c[8], c[9]))
    out = []
    for r in rows:
        v, p = int(r["address"], 16), int(r["prev_listed"], 16)
        seen, end = walk(img, p)
        listed_end = p + img.sizes.get(p, 0)
        reached = v in seen
        own, own_end = walk(img, v)
        verdict = ("INTERIOR - listed size short" if reached else
                   "NOT REACHED from the previous entry")
        blk = next(("%08X+%d %s (%s)" % (s, n, k, why) for s, n, k, why in adm if s <= v < s + n),
                   "not in the admissions table")
        out.append((r["address"], r["prev_listed"], r["prev_name"], "%08X" % listed_end, "%08X" % end,
                    "yes" if reached else "no", r["provenance"], r["boundary"], r["preceded_by"],
                    "%d" % (own_end - v), verdict, blk, r["first_citations"].split(";")[0]))
    for o in out:
        print("%s prev %s(%s) listed_end %s walk_end %s reached=%s prov=%s %s/%s own=%sB -> %s | %s" % o[:12])
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("address\tprev_listed\tprev_name\tlisted_end\twalk_end\treached_from_prev\tprovenance"
                    "\tboundary\tpreceded_by\town_walk_bytes\tverdict\tfirst_citation\n")
            for o in out:
                f.write("\t".join(o) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
