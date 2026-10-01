#!/usr/bin/env python
"""Measure real-body spans for EXP-108 bodies.json.

BFS over each body's instructions: calls stay intra-body (callee is a
different entry), conditional jumps fork, direct unconditional jumps and
jump-table arms seed continuations, ret / tail-jmp to another entry
terminates.
"""
import hashlib, json, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

import check

raw, secs = check.load_image()


def img(va, n):
    rva = va - check.IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + vs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("va %x not in image" % va)


ENTRIES = {
    check.PASS: "pass",     # 003B6020 shadow-draw pass (~677 B)
    check.BLD:  "bld",      # 003B62D0 record builder (~1301 B)
    check.SWAP: "swap",     # 003A1DB0 buffer swap/finalize (84 B)
    check.FIN:  "fin",      # 0036F360 ring finalizer (150 B)
    check.K3F:  "k3f",      # 00264670 kind-3 float read (35 B)
    check.RLUT: "rlut",     # 0046FAE0 ramp LUT lookup (84 B)
    check.RES1: "res1",     # 003B6BF0 actor-rec resolve (43 B)
    check.GATE: "gate",     # 003E6F70 q[rec+0x400] gate (17 B)
    check.RES2: "res2",     # 00421FF0 secondary resolve (85 B)
    check.BASE: "base",     # 0020E600 base add (10 B)
}

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def walk(entry):
    todo, seen, indirect = [entry], set(), []
    hi = entry
    while todo:
        va = todo.pop()
        while True:
            if va in seen:
                break
            try:
                b = img(va, 16)
            except KeyError:
                break
            ins = next(md.disasm(b, va, count=1), None)
            if ins is None:
                break
            seen.add(va)
            hi = max(hi, ins.address + ins.size)
            nxt = ins.address + ins.size
            if ins.mnemonic.startswith("j") and ins.mnemonic != "jmp":
                tgt = ins.operands[0].imm
                if tgt not in ENTRIES or tgt == entry:
                    todo.append(tgt)   # sibling targets are tail calls
                va = nxt
                continue
            if ins.mnemonic == "jmp":
                op = ins.operands[0]
                if op.type == X86_OP_IMM:
                    if op.imm in ENTRIES and op.imm != entry:
                        break          # tail call to a sibling entry
                    if not (entry <= op.imm < entry + 0x400):
                        break          # tail call to a foreign body
                    va = op.imm        # intra-body jump
                    continue
                indirect.append(ins.address)
                # MSVC jump tables are dword RVAs from the image base:
                # find the longest run of consecutive dwords whose
                # IMG_LO + value lands in [entry, entry+0x2000)
                lo, lim = entry, entry + 0x2000
                best = []
                for sva, vs, ra, rs in secs:
                    sva_lo = check.IMG_LO + sva
                    if not (sva_lo <= ins.address < sva_lo + vs):
                        continue
                    start = (ra + (ins.address - sva_lo) + ins.size + 3) & ~3
                    end = min(start + 0x400, ra + rs)
                    for off in range(start, end - 4, 4):
                        t0 = check.IMG_LO + struct.unpack_from(
                            "<I", raw, off)[0]
                        if not (lo <= t0 < lim):
                            continue
                        run = [t0]
                        o2 = off + 4
                        while o2 <= end - 4:
                            t2 = check.IMG_LO + struct.unpack_from(
                                "<I", raw, o2)[0]
                            if not (lo <= t2 < lim):
                                break
                            run.append(t2)
                            o2 += 4
                        if len(run) > len(best):
                            best = run
                for t in best:
                    if t not in seen and t not in todo:
                        todo.append(t)
                break
            if ins.mnemonic in ("ret", "retf", "int3"):
                break
            va = nxt
    return sorted(seen), hi, indirect


out = {"real": [], "scripted": [
    {"name": "e56", "va": "0x%x" % check.E56,
     "note": "003E56A0 deep object resolver (358 B, reaches the "
             "0020E600/002ED570/004FE2F0 subtree): entry-intercepted, "
             "planted OBJ_S returned, arg captured"},
    {"name": "mids", "va": "0x%x" % check.MIDS,
     "note": "002ED570 mid-array resolver (deep subtree): entry-"
             "intercepted, planted MID_A+i*0x100 returned, args captured"},
    {"name": "outr", "va": "0x%x" % check.OUTR,
     "note": "00370F60 outer resolver (deep subtree): entry-intercepted, "
             "planted OBJ_14/OBJ_15 cycled per call pair, args captured"},
]}
for entry, name in sorted(ENTRIES.items()):
    covered, hi, indirect = walk(entry)
    # contiguous span entry..hi (arms/tables interleave inside the image)
    span = img(entry, hi - entry)
    gaps = [a for a in range(entry, hi)
            if a not in covered and img(a, 1) not in (b"\x00", b"\xcc", b"\x90")]
    out["real"].append({
        "name": name, "va": "0x%x" % entry, "end": "0x%x" % hi,
        "size": hi - entry,
        "sha256": hashlib.sha256(span).hexdigest()})
    print("%-9s 0x%x-0x%x  %4d B  cov=%d  gaps=%d  indirect=%s"
          % (name, entry, hi, hi - entry, len(covered), len(gaps),
             ["0x%x" % a for a in indirect] or "-"))

json.dump(out, open("bodies.json", "w"), indent=1)
