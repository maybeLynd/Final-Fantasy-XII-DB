#!/usr/bin/env python
"""Measure real-body spans for EXP-104 bodies.json.

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
    check.SINK: "sink", check.TAIL: "tail",
    check.GCHK: "gchk", check.FAM: "fam", check.ORC: "orc",
    check.REL: "rel", check.LSCAN: "lscan", check.BRES: "bres",
    check.MEMB: "memb", check.BSCAN: "bscan", check.B7E0: "b7e0",
    check.HDEC: "hdec", check.B760: "b760", check.E30: "e30",
    check.FAMIDX: "famidx", check.UFLAG: "uflag", check.UIDX: "uidx",
    check.UBASE: "ubase", check.UGLB: "uglb", check.RESOLVE: "resolve",
    check.COUNT: "count", check.GET: "getter", check.FIND: "find",
    check.NOOP: "noop", check.UNOT: "unot", check.RNG: "rng",
    check.GHDL: "ghdl", check.GHGET: "ghget", check.VEXT: "vext",
    check.COOKIE: "cookie",
    # phase-B subjects
    check.RESET: "reset", check.APPLY: "apply", check.CASC: "casc",
    # quiet bodies: real bytes, one entry token, inner hooks suppressed
    check.R780: "r780", check.C970: "c970", check.O280: "o280",
    check.K6CF0: "k6cf0", check.W91B0: "w91b0", check.ZC9B0: "zc9b0",
    check.A_F22: "f22gate", check.A_EA4: "ea4", check.A_BE0: "be0",
    check.A_B50: "b50", check.A_B70: "b70",
    check.A_479: "n479", check.A_472: "n472", check.A_79B: "b79b",
    check.A_FED: "fed",
    # verified real inner bodies reached under quiet zones
    0x0030EDA0: "eda0",     # unit+0xB88 0x4F0-byte xmm copy -> +0x6B0
    0x00308270: "s8270",    # bit22-gated unit field writes (RESET)
    0x00290B90: "lctx",     # G_CTX29 linked-list walk (RESET->319140)
    0x00319420: "hub420",   # path to 2EAEA0->S24FE30 stub
    0x002EAEA0: "thunkEA0", # jmp thunk into S24FE30 stub
    0x00336710: "ecopy",    # element copy w/ GET(byte[src+0x177]) (z9b)
    0x003839F0: "ffill",    # 0xFF fill (w91)
    0x002FEF30: "notify",   # NOTIFY: zeroes obj+0x24..0x47, rebuilds
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
    {"name": "fmt", "va": "0x%x" % check.FMT,
     "note": "scripted boundary (P token + arg capture; ~500-body "
             "CRT/string formatter closure)"},
    {"name": "vnorm", "va": "0x%x" % check.VNORM,
     "note": "entry-intercepted: body tail-jumps an unmapped IAT thunk "
             "(CRT sqrt); harness computes the float norm and writes xmm0"},
    {"name": "memset", "va": "0x%x" % check.MEMSET,
     "note": "jmp-thunk into unresolved IAT hint/name data; "
             "entry-intercepted, harness zeroes rcx..rcx+r8"},
    {"name": "sqrtf", "va": "0x%x" % check.SQRTF,
     "note": "jmp-thunk into unresolved IAT data; entry-intercepted, "
             "harness computes xmm0"},
    {"name": "s24fe30", "va": "0x%x" % check.S24FE30,
     "note": "scripted ret-0 stub: 950-body carrier reached via "
             "319420->2EAEA0 thunk inside RESET quiet zones"},
    {"name": "s300fc0", "va": "0x%x" % check.S300FC0,
     "note": "scripted ret-0 stub: 1085-body eligibility eval "
             "(CASCADE bitidx 0/1/31 rec-ok arm)"},
    {"name": "s17d470", "va": "0x%x" % check.S17D470,
     "note": "scripted ret-0 stub: context carrier via 30B7F0 inside "
             "CASC eligibility wrappers"},
    {"name": "s3112f0", "va": "0x%x" % check.S3112F0,
     "note": "scripted ret-0 stub: mega-dispatcher, APPLY/CASC builder "
             "flag dispatch"},
    {"name": "s33e1f0", "va": "0x%x" % check.S33E1F0,
     "note": "scripted ret-0 stub: element serializer with CRT vararg "
             "tail inside z9b"},
    {"name": "sb9b0", "va": "0x%x" % check.V_B9B,
     "note": "value stub: CASC eligibility wrapper; ret from "
             "case qret (default 0)"},
    {"name": "sb8e0", "va": "0x%x" % check.V_B8E,
     "note": "value stub: second CASC eligibility wrapper, is34 only"},
    {"name": "s773", "va": "0x%x" % check.V_773,
     "note": "value stub: CASC arg4<0 decoder -> dword write"},
    {"name": "s76d", "va": "0x%x" % check.V_76D,
     "note": "value stub: CASC arg5<0 decoder -> word write"},
    {"name": "s0140", "va": "0x%x" % check.V_014,
     "note": "value stub: CASC arm 5/27 RESET-family carrier"},
    {"name": "s1140", "va": "0x%x" % check.V_114,
     "note": "value stub: CASC arm 0 carrier (2E9600 closure)"},
    {"name": "s2280", "va": "0x%x" % check.V_228,
     "note": "value stub: CASC arm serializer carrier"},
    {"name": "s99b0", "va": "0x%x" % check.V_99B,
     "note": "value stub: CASC arm helper (46A7xx carrier)"},
    {"name": "s4d0", "va": "0x%x" % check.V_4D0,
     "note": "value stub: CASC range helper (RNG closure)"},
    {"name": "s46a8", "va": "0x%x" % check.V_46A8,
     "note": "value stub: CASC flag60 helper, action in {3,4}"},
    {"name": "s4b1", "va": "0x%x" % check.A_4B1,
     "note": "value stub: rand() bit-picker inside ~be0 (unresolved "
             "IAT closure)"},
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
