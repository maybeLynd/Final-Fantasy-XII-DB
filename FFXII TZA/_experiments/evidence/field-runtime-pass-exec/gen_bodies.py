#!/usr/bin/env python
"""Measure real-body spans for EXP-106 bodies.json.

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
    check.PASS_: "pass", check.WRES: "wres", 0x002620E0: "initc",
    # hooked real leaf bodies (token = dict value)
    check.NOOP: "noop", check.COOKIE: "cookie",
    check.F_BUSY: "busy", check.F_PSLT: "pslt", check.F_GT3: "gt3",
    check.F_FH: "fh", check.F_DEFR: "dfr", check.F_PCHK: "pck",
    check.F_610: "g610", check.F_D60: "gd60", check.F_B40: "gb40",
    check.F_8F0: "g8f0", check.F_860: "g860", check.F_RC: "rc",
    check.F_D0: "gd0", check.F_DA0: "gda0", check.F_REC: "grec",
    check.F_RES: "gres", check.F_550: "g550", check.F_9B8: "g9b8",
    check.F_TAD: "gtad", check.F_97B: "g97b", check.F_A71: "ga71",
    check.F_B64: "gb64", check.F_C05: "gc05", check.F_4A1: "g4a1",
    check.F_DDA: "gdda",
    # additional real leaves folded into HOOKS
    0x00357760: "g760", 0x00357770: "g770", 0x002EF2B0: "gefb",
    0x001EC560: "gc56", 0x00265760: "g576", 0x002E0540: "ge05",
    0x00314910: "g491", 0x0022A030: "ga03", 0x0022A080: "ga08",
    0x00265270: "g527", 0x0020AA30: "gaa3", 0x0020AA40: "gaa4",
    0x002EFE40: "xe40", 0x002EFE50: "xe50", 0x00363A80: "xa80",
    0x00377C20: "g7c2", 0x003148F0: "g48f", 0x002EF640: "gf64",
    0x00269860: "x986",
    # unhooked real internals (run silently inside hooked callers)
    0x00263FF0: "gres2",    # 3588B0's inner focus/fam resolver
    0x0030D9A0: "mode",     # g8f0/g860's mode bit-scan (-> g7c2)
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
    {"name": "interp", "va": "0x%x" % check.S_INTERP,
     "note": "0025E4C0 bytecode VM interpreter (14.6KB): disclosed "
             "boundary -- the interpreter contract's own subject; "
             "invocation + return-driven continuation are modelled"},
    {"name": "audio", "va": "0x%x" % check.S_AUDIO,
     "note": "00261F90 audio subsystem call: scripted stub "
             "(separate audio contract)"},
    {"name": "dreq", "va": "0x%x" % check.S_DREQ,
     "note": "0032FC30 deferred mode request: scripted stub, "
             "args (ecx=1, edx=0xD4) captured"},
    {"name": "initc chain", "va": "00259B30/003E8980/0025ACA0/0017D490/"
             "0026FAD0/00379860/00379290/003DE920/00363B40/003601C0",
     "note": "002620E0's ten external calls: scripted stubs; "
             "ice/icf carry captured args + sequenced qrets"},
    {"name": "lifecycle helpers",
     "va": "0025B600/0025B740/0025B820/0025C170/0025B250/0025E400/"
           "0026A5F0/00233AA0/00263660/00250960/00259FB0/00268690/"
           "003B7130/002E1C40/00254A90/00234150/002EFD20/002F1A30/"
           "00183070/002677B0/002EFA70/003EAA70/002E6310/002681E0/"
           "002E5030/002E5750/003E6EF0/003E68B0/003E6A70/0026D6F0/"
           "0017E7D0",
     "note": "pass/wres/settle helper calls: scripted stubs, "
             "qret-configured where the return steers flow"},
    {"name": "wres predicate closures",
     "va": "001ED180/001ED130/001EDE80/001EC5C0/001EC5E0",
     "note": "resolver-family predicates (xd1/xd3/xde8/xc5c/xc5e): "
             "scripted stubs; their real leaf readers (g527/g576/"
             "gc56/ga03/ga08/ge05/gdda) are measured separately"},
    {"name": "wres arm checkers",
     "va": "003DBF60/003DB2A0/002674B0/00267420/002E4380",
     "note": "kind-3/4/5/7 checker calls: scripted stubs "
             "(gb64/gc05 run real)"},
    {"name": "planted fn-ptrs", "va": "fixture",
     "note": "record+0x38 callback target + scratch bodies: "
             "planted xor eax;ret / mov rax,imm;ret"},
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
