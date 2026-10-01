#!/usr/bin/env python
"""Measure real-body spans for EXP-110 bodies.json.

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
    check.D10:    "d10",    # 00684D10 script-execute wrapper (pool checkout)
    check.F60:    "f60",    # 00684F60 script-execute wrapper (setfield)
    check.C280:   "c280",   # 00686280 two-pool caller + marshal + dispatch
    check.GETTOP: "gettop", # 0080FD00 stack depth
    check.SETTOP: "settop", # 00811130 stack top move (no clear)
    check.PUSHB:  "pushb",  # 00810450 push boolean
    check.PUSHI:  "pushi",  # 00810580 push integer
    check.PUSHN:  "pushn",  # 00810640 push number
    check.PUSHP:  "pushp",  # 008105A0 push light userdata
    check.TOBOOL: "tobool", # 008113D0 toboolean
    check.TYPE:   "type",   # 008119F0 value type
    check.SING:   "sing",   # 006372A0 singleton const getter
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
    {"name": "load",   "va": "0x%x" % check.LOAD,
     "note": "00683C30 chunk loader: entry-intercepted, (buf,name) captured, "
             "ret planted"},
    {"name": "pcall",  "va": "0x%x" % check.PCALL,
     "note": "00810340 protected call: pops nargs entries, pushes planted "
             "result(s), ret from case sequence"},
    {"name": "errstr", "va": "0x%x" % check.ERRSTR,
     "note": "00811530 error-string getter: planted pointer"},
    {"name": "log",    "va": "0x%x" % check.LOG,
     "note": "005CDAA0 logger: (fmt,ecx,edx,r8) captured"},
    {"name": "pushls", "va": "0x%x" % check.PUSHLS,
     "note": "0080FB20 push-loaded-string: pushes planted TV "
             "{rdx, pushls_ty}"},
    {"name": "idxop",  "va": "0x%x" % check.IDXOP,
     "note": "00810730 index op: pushes nil TV"},
    {"name": "setfld", "va": "0x%x" % check.SETFLD,
     "note": "00810ED0 setfield: pops one TV; popped slot type recorded in "
             "trace (real consumer of PUSHP's tag)"},
    {"name": "copy",   "va": "0x%x" % check.COPY,
     "note": "00682AA0 deep copy (185 insns): boundary, args captured"},
    {"name": "marsh",  "va": "0x%x" % check.MARSH,
     "note": "00682D20 marshal helper: args captured"},
    {"name": "iter",   "va": "0x%x" % check.ITER,
     "note": "006811B0 iterator: writes cursor-holder pointer"},
    {"name": "disp",   "va": "0x%x" % check.DISP,
     "note": "00681010 unknown-tag marshal dispatch: args + optional "
             "error log"},
    {"name": "grow",   "va": "0x%x" % check.GROW,
     "note": "0080F420 stack-grow check: no-op (fixture stacks are large)"},
    {"name": "geta",   "va": "0x%x" % check.GETA,
     "note": "006810B0 fallback result getter A: planted {q,b} result"},
    {"name": "getb",   "va": "0x%x" % check.GETB,
     "note": "00681130 fallback result getter B: planted {q,b} result"},
    {"name": "tonum",  "va": "0x%x" % check.TONUM,
     "note": "00811470 tonumber: planted return value feeds result store"},
    {"name": "mshl",   "va": "0x%x" % check.MSHL,
     "note": "00636920 singleton-result helper: planted return"},
    {"name": "cpy86",  "va": "0x%x" % check.CPY86,
     "note": "00861EBA copy thunk: args captured"},
] + [{"name": "sent%d" % k, "va": "0x%x" % v,
      "note": "TLS singleton getter (gs:[0x58] — cannot run under "
              "Unicorn): returns planted token SENTB+%x" % (k * 0x10)}
     for k, v in enumerate(check.SENTS)]}


for entry, name in ENTRIES.items():
    addrs, hi, indirect = walk(entry)
    lo, hi = min(addrs), max(addrs)
    span = hi - lo
    cov = len(addrs) / span if span else 0
    h = hashlib.sha256(img(lo, span)).hexdigest()
    out["real"].append({
        "name": name, "va": "0x%x" % entry, "lo": "0x%x" % lo,
        "hi": "0x%x" % hi, "span": span, "insns": len(addrs),
        "cov": round(cov, 3), "sha256": h,
        "indirect": ["0x%x" % i for i in indirect]})

json.dump(out, open("bodies.json", "w"), indent=1)
for r in out["real"]:
    print("%-7s %s span=%4d insns=%3d cov=%.2f" %
          (r["name"], r["va"], r["span"], r["insns"], r["cov"]))
print("%d scripted boundaries" % len(out["scripted"]))
