#!/usr/bin/env python3
"""reader_search_returned.py - does anything READ offset X of a record an accessor returns?

The question this answers, and why the usual tools cannot.

A row whose entire evidence is `mov qword [rcx+0x30], rbx` in a constructor is a *weak* row: the
field's existence rests on a zero being written there once. If something reads it, it is a field. If
nothing does, the store is describing a cleared region as though it were one.

`check_alignment.py` can only catch such a row when the offset is misaligned. `RenderModelInstance
+0x30` and `+0x38` are 8-aligned, so they are invisible to it. And an image-wide sweep for
`[reg+0x30]` is worthless - that displacement belongs to hundreds of unrelated objects, which is the
exact trap that produced a 75-reader false population earlier in this work.

So the population is bounded the way the store itself bounds it: **the type's `route` column names
an accessor that RETURNS the record** (`RenderModelInstance` -> `FN 0x003E55B0+0x0`). Every caller
therefore holds the record in `rax` immediately after the call, and nowhere else does a bare
displacement mean this type. This walks each caller forward from the call site, keeps the set of
registers currently holding the record, drops a register the moment anything else writes it, and
records every access at the offsets asked for.

    python reader_search_returned.py --accessor 0x3E55B0 --offsets 0x30,0x38,0x40,0x4

LIMITS, stated rather than implied:
  * **Same-function only.** A record passed into a callee is not followed, so the count is a FLOOR.
  * **Direct calls only.** A caller reaching the accessor through a function pointer is invisible.
  * A read found here is proof; **zero reads is bounded evidence, not proof of absence** - it says
    no caller of this accessor reads the offset, which is the strongest statement the static image
    supports for a record with no other route.
"""
import argparse
import bisect
import collections
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RAX

import member_reach_scan as M
import kit_paths as KP  # noqa: E402

# FIXED 2026-09-20 (OPUS): this was os.path.join("..", "..", "work", "exe", …),
# a path relative to the CURRENT DIRECTORY, so the script ran only when invoked from
# inside gfz-scripts. Seventeen scripts shared the defect. kit_paths derives it from
# __file__, which is what this kit's own rule asks for.
EXE = KP.EXE


def load_text():
    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    base = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        if nm == ".text":
            return raw, base, base + va, vs, pr
        off += 40
    raise SystemExit("no .text")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accessor", required=True, help="VA of the function that RETURNS the record")
    ap.add_argument("--offsets", required=True, help="comma-separated offsets, e.g. 0x30,0x38")
    a = ap.parse_args()

    acc = int(a.accessor, 0)
    want = {int(x, 0) for x in a.offsets.split(",")}

    raw, base, tva, tvs, tpr = load_text()
    blob = raw[tpr:tpr + tvs]
    sizes, names = M.load_funcs()
    st = sorted(sizes)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def owner(v):
        i = bisect.bisect_right(st, v) - 1
        return st[i] if i >= 0 and st[i] <= v < st[i] + sizes[st[i]] else None

    # every direct call to the accessor
    callers = collections.defaultdict(list)
    i = 0
    while True:
        i = blob.find(b"\xe8", i)
        if i < 0 or i + 5 > len(blob):
            break
        site = tva + i
        if tva + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == acc:
            o = owner(site)
            if o is not None:
                callers[o].append(site)
        i += 1

    print("accessor %08X  %s" % (acc, names.get(acc, "?")))
    print("direct call sites: %d, in %d distinct body(ies)"
          % (sum(len(v) for v in callers.values()), len(callers)))
    print("offsets asked for: %s" % ", ".join(hex(x) for x in sorted(want)))
    print()

    found = collections.defaultdict(list)
    for fn in sorted(callers):
        body = blob[fn - tva:fn - tva + sizes[fn]]
        try:
            ins_list = list(md.disasm(body, fn))
        except Exception:
            continue
        idx = {ins.address: n for n, ins in enumerate(ins_list)}
        for site in callers[fn]:
            start = idx.get(site)
            if start is None:
                continue
            held = {X86_REG_RAX}
            for ins in ins_list[start + 1:]:
                # DO NOT STOP AT THE FIRST BRANCH. The first version did, and reported zero
                # accesses at every offset asked for -- including `+0xB6`, whose own store row
                # names its reader. Real bodies branch within a few instructions, so that window
                # was usually empty and the run looked like a clean negative. The technique this
                # kit uses elsewhere is same-register/same-function: walk the whole body and stop
                # trusting a register only when something writes it.
                if ins.group(CS_GRP_RET):
                    break
                for oi, op in enumerate(ins.operands):
                    if op.type == X86_OP_MEM and op.mem.base in held and op.mem.index == 0 \
                            and op.mem.base != X86_REG_RIP:
                        if op.mem.disp in want:
                            kind = "W" if oi == 0 else "R"
                            found[op.mem.disp].append((fn, ins.address, kind,
                                                       ins.mnemonic + " " + ins.op_str))
                # propagate  mov rX, rY  where rY holds the record
                if ins.mnemonic == "mov" and len(ins.operands) == 2 \
                        and ins.operands[0].type == X86_OP_REG and ins.operands[1].type == X86_OP_REG:
                    if ins.operands[1].reg in held:
                        held.add(ins.operands[0].reg)
                        continue
                # a call clobbers the volatile registers; stop trusting rax across it
                if ins.group(CS_GRP_CALL):
                    held.discard(X86_REG_RAX)
                    if not held:
                        break
                    continue
                # anything else that writes a held register drops it
                for op in ins.operands[:1]:
                    if op.type == X86_OP_REG and op.reg in held:
                        held.discard(op.reg)
                if not held:
                    break

    for d in sorted(want):
        hits = found[d]
        r = [h for h in hits if h[2] == "R"]
        w = [h for h in hits if h[2] == "W"]
        print("  +0x%-4X reads %-3d writes %-3d" % (d, len(r), len(w)))
        for fn, ad, kind, txt in hits[:6]:
            print("        %s %08X in %08X  %s" % (kind, ad, fn, txt))
        if len(hits) > 6:
            print("        ... +%d more" % (len(hits) - 6))
    print()
    print("A read here is proof. Zero reads is bounded evidence - no CALLER OF THIS ACCESSOR reads")
    print("the offset - and the count is a floor: records passed into a callee are not followed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
