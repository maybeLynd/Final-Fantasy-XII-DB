#!/usr/bin/env python3
"""Census of authored `attach` (verb 0x0D9) / `attachoff` (0x0DA) call
sites over every shipped .ebp container in FFXII_TZA.vbf, for
OPUS-REQ-SWE2-DATA-SCRIPT-NATIVE-ARG1.

Reuses the decode + backward stack-slot attribution of
25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py
(opcode table, diroff-bounded script regions, verb-table arity model).

Answers: for each site, the call opcode and each operand's provenance
(constant, call result, expression).  Conclusion read 2026-09-20:
attach's second operand is always a small PUSHII literal
({0,1,2,3,0xd,0x13,0x14,0x100,0x104}, 0x2 dominant) - an authored index,
never an actor handle; the native's RDX arg is the VM-supplied actor
record, not a script operand (dispatch convention at 002621D0).

Usage: gen_attach_arg_census.py [vbf-path]
    -> writes attach-arg-census.tsv beside this script.
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS_DIR = os.path.normpath(os.path.join(
    HERE, "..", "..", "..",
    "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))

sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..", "agent_flow", "tools")))
sys.path.insert(0, CENSUS_DIR)

import gen_req_channel_census as G
import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

TARGETS = (0x0D9, 0x0DA)          # attach, attachoff


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    verbs = G.load_verbs()
    ebps = sorted(p for p in names if p.lower().endswith(".ebp"))
    rows = []
    seen = set()
    files = scripts = 0
    for path in ebps:
        try:
            b = V.read_entry(f, names, blocks, path)
        except Exception:
            continue
        if len(b) < 0x80 or G.U32(b, 0x80) != 0x8000000B:
            continue
        files += 1
        sec = b[0x80:0x80 + G.U32(b, 0x84)]
        diroff = G.U32(sec, 0x18)
        cnt = G.U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
            continue
        starts = sorted(G.U32(sec, diroff + 4 + s * 0x30 + 8)
                        for s in range(cnt))
        bounds = sorted(set(starts) | {diroff, len(sec)})
        for si, start in enumerate(starts):
            end = min((x for x in bounds if x > start), default=len(sec))
            if start >= len(sec) or end <= start:
                continue
            scripts += 1
            ins, _ = G.decode(sec[start:end])
            for j, (pc, op, imm) in enumerate(ins):
                if op not in (0x58, 0x59, 0x5D, 0x5E) or imm not in TARGETS:
                    continue
                key = (path, start + pc)
                if key in seen:
                    continue
                seen.add(key)
                v = verbs[imm]
                need = (v[0] or 0) + (1 if op in (0x59, 0x5E) else 0)
                args, st = G.resolve_args(ins, j, need, verbs) \
                    if need else ([], "ok")
                argstr = ";".join(
                    "%s:%x" % (a[0], a[1]) if a[1] is not None else a[0]
                    for a in args) if args else ""
                rows.append((path, str(si), "%x" % (start + pc),
                             G.OPN[op], v[2], st, argstr))

    out = os.path.join(HERE, "attach-arg-census.tsv")
    with io.open(out, "w", encoding="utf-8", newline="\n") as w:
        w.write("# attach (0x0D9) / attachoff (0x0DA) call-site operand "
                "census over all shipped .ebp containers\n")
        w.write("# args_push_order: operand 0 first; CALLACT*'s leading "
                "entry is the actor-id pop\n")
        w.write("file\tscript\tpc\topcode\tverb\tstatus\targs_push_order\n")
        for r in rows:
            w.write("\t".join(r) + "\n")
    print("files=%d scripts=%d sites=%d -> %s"
          % (files, scripts, len(rows), out))
    agg = collections.Counter()
    for p, si, pc, opn, vn, st, argstr in rows:
        agg[(opn, vn, st, tuple(argstr.split(";")) if argstr else ())] += 1
    for k in sorted(agg):
        print(agg[k], k)


if __name__ == "__main__":
    main()
