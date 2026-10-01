#!/usr/bin/env python
"""Measure real-body spans for EXP-105 bodies.json.

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
    # subjects
    check.FORK: "fork", check.SEB: "seb", check.SEP: "sep",
    check.RCAL: "rcal", check.WSHIM: "wshim", check.WSEB: "wseb",
    check.PSHIM: "pshim", check.WSEP: "wsep",
    # hooked leaf helpers
    check.NOOP: "noop", check.GET2: "get2", check.XREF: "xref",
    check.COOKIE: "cookie",
    check.S580: "w18", check.S590: "w10", check.S6A0: "r14",
    check.S6B0: "rst", check.S6E0: "w2c", check.S6F0: "pan",
    check.S7C0: "w24", check.S7D0: "w14", check.S7E0: "vol",
    check.S670: "r2c", check.S680: "t10", check.S690: "r24",
    # quiet bodies: real bytes, one entry token, inner hooks suppressed
    check.Q_L: "lazy", check.Q_A: "alloc", check.Q_E: "getv",
    check.Q_F1: "fslot", check.Q_F2: "fid", check.Q_SW: "sweep",
    check.Q_O: "osweep", check.Q_VC: "vctor",
    # pool machinery (real on planted structures)
    0x00220CE0: "popb",      # 221d10's lazy pool-B pop (vctx+8)
    0x00220D30: "popw",      # 221d60's voice-pool thunk (vctx+0xa0)
    0x002204A0: "poolpop",   # pool pop body (freelist -> ctor arg)
    0x00220550: "voicepop",  # voice pop body + 2255c0 ctor call
    0x00221710: "vctx",      # G_VCTX getter
    0x00221210: "pushb",     # reap push: pool+0xa0 -> 219d80
    0x00219D80: "treeins",   # pool busy-tree insert
    # grow path (real bodies; not exercised in nonempty fixtures)
    0x00210A60: "grow",      # 221d60's refill: 3x 212910
    0x00212910: "relscan",   # per-obj 222050 release walk
    # locks (real on planted mutex structures)
    0x005CD4F0: "lock",
    0x005CD820: "unlock",
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
    {"name": "spin", "va": "0x%x" % check.SPIN,
     "note": "mixer-wait fence 005CC930: entry-intercepted; stub "
             "writes configured state to the elem register's +0x30"},
    {"name": "spn2", "va": "0x%x" % check.SPIN2,
     "note": "second fence 005CCB80 inside the spin loop; "
             "sequence-configured states"},
    {"name": "s6d", "va": "0x%x" % check.T6D,
     "note": "shared_ptr carrier 007A6DB0: copies src ptr to dst, "
             "plants dst+0x110 flag byte (s6d_flag)"},
    {"name": "s70", "va": "0x%x" % check.T70,
     "note": "refcount read 007A7010 -> eax (==3 arms the s7a reset)"},
    {"name": "s78", "va": "0x%x" % check.T78,
     "note": "weak-lock/validity 007A78B0 -> eax; nonzero arms "
             "002256B0 voice reset"},
    {"name": "s7a", "va": "0x%x" % check.T7A,
     "note": "shared_ptr reset 007A7A20"},
    {"name": "s8c", "va": "0x%x" % check.T8C,
     "note": "polymorphic bounds/contains 007A8CF0 -> al "
             "(default 1; case-configured)"},
    {"name": "s5a/s80/s81/s87/se0/se9",
     "va": "0x%x/0x%x/0x%x/0x%x/0x%x/0x%x" % (
         check.T5A, check.T80, check.T81, check.T87,
         check.TE0, check.TE9),
     "note": "0x7a* carrier bodies inside the ~at/~ac arms and the "
             "PAN/VOL tails -- entry-intercepted, configured returns"},
    {"name": "at", "va": "0x%x" % check.AT,
     "note": "bus-attach arm A 00221940 (callback path): scripted "
             "stub -- the attach closure is a separate contract's "
             "subject"},
    {"name": "ac", "va": "0x%x" % check.AC,
     "note": "bus-attach arm B 00221C70: scripted stub (same "
             "disclosure class)"},
    {"name": "d6d/da6", "va": "0x%x/0x%x" % (check.TD6D, check.TDA6),
     "note": "pool tree extract/relink STL utilities inside the pool "
             "pops -- entry-intercepted (silent inside quiet zones)"},
    {"name": "m99", "va": "0x%x" % check.TM99,
     "note": "std::map insert 00199DB0: writes the out-pair at r8; "
             "bookkeeping result unused by the pool pops"},
    {"name": "vt", "va": "0x%x" % check.SCR,
     "note": "planted vtail target (elem.vtable+0x50): fixture "
             "scratch body, disclosed"},
    {"name": "allocator fns", "va": "planted",
     "note": "list allocator alloc/free member fn-ptrs at obj+0x10/"
             "+0x18 -> fixture scratch bodies (mov rax,imm;ret / "
             "xor eax;ret)"},
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
