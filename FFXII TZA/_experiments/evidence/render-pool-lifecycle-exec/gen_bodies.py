#!/usr/bin/env python
"""Measure real-body spans for EXP-109 bodies.json.

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
    check.CTOR:  "ctor",    # 004269A0 pool constructor
    check.LKUP:  "lkup",    # 004278E0 name lookup (active+pending)
    check.ALOC:  "aloc",    # 004279B0 pending-record allocate
    check.PROM:  "prom",    # 00428710 pending->active promote
    check.RETI:  "reti",    # 00427C90 retire flagged actives
    check.RELE:  "rele",    # 00429140 release
    check.CLR:   "clr",     # 0041F730 0x740 reset/default writer
    check.F4W:   "f4w",     # 006C0520 float4 default writer
    check.CPY:   "cpy",     # 0046D110 -> 00202C70 const copy thunk
    0x00202C70:  "cpy2",    # 00202C70 0x40B copy from shipped 0x1F204E0
    check.A8W:   "a8w",     # 003E5D00 array default writer
    check.Z50:   "z50",     # 003E37E0 -> memset(0x580,0,0x50) thunk
    check.BASE:  "base",    # 0020E600 index -> object resolve
    check.BAS2:  "bas2",    # 0020E620 object -> index resolve
    check.T1W:   "t1w",     # 0041D6C0 name-table writer 1
    check.T2W:   "t2w",     # 0041D6D0 name-table writer 2
    check.T3W:   "t3w",     # 0041D6E0 name-table writer 3
    check.DRAIN: "drain",   # 00426EC0 child-chain unlink
    check.HC1:   "hc1",     # 003B6000 slot-table enable clear
    check.HC2:   "hc2",     # 003AFBE0 handle-table id clear
    check.G68:   "g68",     # 003E68E0 q[rec+0x400] gate
    check.L2D:   "l2d",     # 00422D50 d[rec+0xC4] gate
    check.SLTI:  "slti",    # 003B6890 slot-table init
    check.HTI:   "hti",     # 003AFCD0 handle-table init
    check.T3I:   "t3i",     # 004778A0 0x40-stride table init
    check.T4I:   "t4i",     # 003AF2B0 table init
    check.T5I:   "t5i",     # 0042F000 table init
    check.S53:   "s53",     # 003B53C0 globals init
    check.E0720: "e0720",   # 003E0720 init tail (S512+D40 calls)
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
    {"name": "rinit", "va": "0x%x" % check.RINIT,
     "note": "00420480 record-init boundary: entry-intercepted, args "
             "(rec,name,buf1,obj,stack:orig r8d/r9d) captured"},
    {"name": "ptd", "va": "0x%x" % check.PTD,
     "note": "0041FCF0 pending-teardown boundary: entry-intercepted, "
             "arg captured"},
    {"name": "hid", "va": "0x%x" % check.HID,
     "note": "003B56D0 handle-id allocator: entry-intercepted, planted "
             "hid_ret+i returned, arg w[rec] captured"},
    {"name": "phook", "va": "0x%x" % check.PHOOK,
     "note": "0042C410 promotion hook: entry-intercepted, fx writes "
             "applied, arg captured; caller pins +0x48818 bit0"},
    {"name": "tdown", "va": "0x%x" % check.TDOWN,
     "note": "004200A0 record resource teardown (frees ~10 sub-objects "
             "then tail-jmps 0041F730): entry-intercepted, arg captured"},
    {"name": "f4c0", "va": "0x%x" % check.F4C0,
     "note": "0042F4C0 retire pre-teardown boundary: entry-intercepted, "
             "arg captured"},
    {"name": "e56", "va": "0x%x" % check.E56,
     "note": "003E56A0 deep object resolver: entry-intercepted, planted "
             "E56O returned, arg captured; caller tests b[ret]"},
    {"name": "mids", "va": "0x%x" % check.MIDS,
     "note": "002ED570 mid resolver (deep subtree): entry-intercepted, "
             "planted MIDO returned, args captured"},
    {"name": "t51", "va": "0x%x" % check.T51,
     "note": "0051B9E0 resolver tail target of 00422D50: entry-"
             "intercepted, planted T51O returned, args captured"},
    {"name": "s512", "va": "0x%x" % check.S512,
     "note": "00512EF0 subsystem boundary: entry-intercepted"},
    {"name": "d40", "va": "0x%x" % check.D40,
     "note": "0040DB70 subsystem boundary: entry-intercepted"},
    {"name": "e400", "va": "0x%x" % check.E400,
     "note": "0032E400 subsystem boundary: entry-intercepted"},
    {"name": "e620", "va": "0x%x" % check.E620,
     "note": "0032E620 subsystem boundary: entry-intercepted"},
    {"name": "e520", "va": "0x%x" % check.E520,
     "note": "0032E520 subsystem boundary: entry-intercepted"},
    {"name": "al1", "va": "0x%x" % check.AL1,
     "note": "0036C1D0 allocator (unplanted-table path only): entry-"
             "intercepted, planted table returned"},
    {"name": "al2", "va": "0x%x" % check.AL2,
     "note": "0036A100 allocator (unplanted-table path only): entry-"
             "intercepted, planted table returned"},
    {"name": "al3", "va": "0x%x" % check.AL3,
     "note": "0036C140 allocator (unplanted-table path only): entry-"
             "intercepted, planted table returned"},
    {"name": "memset", "va": "0x%x" % check.MEMSET,
     "note": "00861EC0 memset thunk: entry-intercepted, implemented as "
             "a real byte-fill (its writes ARE the semantics), args "
             "captured"},
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
