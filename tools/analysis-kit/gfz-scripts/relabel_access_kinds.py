#!/usr/bin/env python3
"""relabel_access_kinds.py - re-derive the `kind` cell of committed *-accesses.tsv rows.

OPUS, 2026-09-24. Access-direction labels in the store came from three sources, all defective:
reg_tracking.op_kind trusted capstone's operand flags (movups/movq stores read as r, unflagged
`test [m], reg` fell to "w"), and eight producers hand-rolled `"w" if operand 0 else "r"`, which
calls `cmp [m], x` / `bt [m], n` a write and every RMW a plain w. The repaired classifier is
reg_tracking.op_kind, controlled against iced-x86 over the whole image (0 disagreements,
opkind_vs_iced.py / regwrites_vs_iced.py).

THIS IS A RELABELLER, NOT A SCANNER. It never adds or drops a row. For each row it decodes the
ONE instruction at `site`, checks the decoded text equals the row's `instruction` cell (else the
row is reported MISMATCH and left alone), and recomputes the kind of that instruction's memory
operand. A row whose instruction has more than one memory operand (movs) is reported and left.
Each row's own lea token (`a` or `addr`) is kept; `#` provenance lines before the header
are skipped and preserved.

    relabel_access_kinds.py --report out.tsv FILE...          # measure only
    relabel_access_kinds.py --apply --report out.tsv FILE...  # rewrite the kind cells in place

Every change is written to --report with the preimage kind, so the patch is exactly reversible.
"""
import argparse
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_default_instance_writers as W  # noqa: E402
import reg_tracking as RT  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402


def norm_text(s):
    return " ".join(s.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    img = W.Image()
    classes = collections.Counter()
    report = []
    for path in a.files:
        raw = io.open(path, encoding="utf-8", newline="").read()
        eol = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(eol)
        h0 = 0
        while h0 < len(lines) and lines[h0].startswith("#"):
            h0 += 1                          # emit_seeded_census files carry # provenance lines
        hdr = lines[h0].split("\t") if h0 < len(lines) else []
        try:
            ks, kk, ki = hdr.index("site"), hdr.index("kind"), hdr.index("instruction")
        except ValueError:
            classes[(path, "no-site/kind/instruction-columns")] += 1
            continue
        changed = False
        for n in range(h0 + 1, len(lines)):
            ln = lines[n]
            if not ln.strip() or ln.startswith("#"):
                continue
            c = ln.split("\t")
            if len(c) <= max(ks, kk, ki):
                classes["short-row"] += 1
                continue
            try:
                site = int(c[ks], 16)
            except ValueError:
                classes["bad-site"] += 1
                continue
            b = img.read(site, 16)
            ins = next(img.md.disasm(b, site), None) if b else None
            if ins is None:
                classes["undecodable"] += 1
                continue
            if norm_text("%s %s" % (ins.mnemonic, ins.op_str)) != norm_text(c[ki]):
                classes["MISMATCH-instruction"] += 1
                report.append((path, n + 1, c[ks], c[kk], "", "MISMATCH", c[ki]))
                continue
            mems = [(oi, op) for oi, op in enumerate(ins.operands) if op.type == X86_OP_MEM]
            if len(mems) != 1:
                classes["multi-memory-left"] += 1
                continue
            new = RT.op_kind(ins, mems[0][1], mems[0][0])
            old = c[kk]
            if new == "addr" and old == "a":
                new = "a"                    # the row's own lea token is kept
            if new == "rw" and old == "wr":
                new = "wr"                   # ... and its own read-modify-write token
            if new == old:
                classes["same"] += 1
                continue
            cls = "%s->%s" % (old, new)
            classes[cls] += 1
            report.append((path, n + 1, c[ks], old, new, cls, c[ki]))
            c[kk] = new
            lines[n] = "\t".join(c)
            changed = True
        if changed and a.apply:
            io.open(path, "w", encoding="utf-8", newline="").write(eol.join(lines))
    with io.open(a.report, "w", encoding="utf-8", newline="\n") as f:
        f.write("file\tline\tsite\tkind_before\tkind_after\tclass\tinstruction\n")
        for r in report:
            f.write("\t".join(str(x) for x in r) + "\n")
    for k, v in sorted(classes.items(), key=lambda kv: -kv[1]):
        print("  %-28s %d" % (k if isinstance(k, str) else "%s %s" % k, v))
    print("%s %d change(s) -> %s" % ("APPLIED" if a.apply else "measured",
                                      sum(1 for r in report if r[5] != "MISMATCH"), a.report))


if __name__ == "__main__":
    main()
