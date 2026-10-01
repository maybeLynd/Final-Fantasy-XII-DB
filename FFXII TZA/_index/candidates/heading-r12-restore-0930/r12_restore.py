"""r12_restore.py - does 00533B20 give R12 back on its normal return? (OPUS, 2026-09-30.) Static. Reads only.

The heading contract's 0x67 reader 004607C0 zeroes r12d at 00460A5B and compares the flag with it at 00460ACA after three
calls to 00533B20 (00460A9A, 00460AB6, 00460AC5). ASTRA's accepted packet (8969fe745, SWE2-AUDIT-SPEC cd86f404d) grounds
R13/RSI/RBX through 00533B20's pushes; R12 is not pushed, and 00533B20 writes it. This checks the spill-slot route:

  S1  every R12 write in 00533B20 (decoded from its entry over direct branches; the packet found no indirect jump and no
      jump leaving the body) is dominated by a store of R12 to one stack slot [rsp+K] (the spill);
  S2  on every path from each R12 write to the single RET, a reload `mov r12, [rsp+K]` from the same slot is passed:
      removing the reload blocks makes RET unreachable from each write;
  S3  no other direct store to [rsp+K] lies in the body, and RSP changes only at the prologue sub / epilogue add (so the
      slot is the same bytes at spill and reload);
  S4  the body between the spill and the first write, and after the reload, writes R12 nowhere else.
Controls: C1 the same checker on R13 (pushed, restored by pop) finds no spill slot and reports "pushed" - it must not
claim a spill for a pushed register; C2 a private copy of the body with the reload's bytes changed to reload R13 instead
(`4C8BA424...` -> `4C8BAC24...`, same size) must fail S2.
Conditions it keeps: a normal return, calls returning normally with RSP coherent, no aliasing store into the slot through
a pointer (a direct-store check only). It proves nothing about what 00533B20 computes.
"""
import collections, os, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402

F, N = 0x00533B20, 9526
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def decode(blob):
    ins = {}
    work = [F]
    while work:
        a = work.pop()
        if a in ins or not (F <= a < F + N):
            continue
        i = next(md.disasm(blob[a - F:a - F + 16], a, 1), None)
        if i is None:
            continue
        ins[a] = i
        for t in succ(i):
            work.append(t)
    return ins


def succ(i):
    nxt = i.address + i.size
    if i.mnemonic in ("ret", "retn"):
        return []
    if i.mnemonic == "jmp":
        op = i.operands[0]
        return [op.imm] if op.type == X.X86_OP_IMM else []
    if i.mnemonic.startswith("j"):
        op = i.operands[0]
        return [nxt, op.imm] if op.type == X.X86_OP_IMM else [nxt]
    return [nxt]


def writes(i, name):
    try:
        _, wr = i.regs_access()
    except capstone.CsError:
        return False
    fam = {"r12": ("r12", "r12d", "r12w", "r12b"), "r13": ("r13", "r13d", "r13w", "r13b")}[name]
    return any(md.reg_name(x) in fam for x in wr)


def spill_store(i, name):
    """`mov qword [rsp+K], reg` -> K."""
    if i.mnemonic == "mov" and len(i.operands) == 2 and i.operands[0].type == X.X86_OP_MEM and i.operands[1].type == X.X86_OP_REG:
        m = i.operands[0].mem
        if md.reg_name(m.base) == "rsp" and m.index == 0 and md.reg_name(i.operands[1].reg) == name:
            return m.disp
    return None


def reload(i, name):
    if i.mnemonic == "mov" and len(i.operands) == 2 and i.operands[0].type == X.X86_OP_REG and i.operands[1].type == X.X86_OP_MEM:
        m = i.operands[1].mem
        if md.reg_name(i.operands[0].reg) == name and md.reg_name(m.base) == "rsp" and m.index == 0:
            return m.disp
    return None


def reach(ins, start, removed):
    seen, work = set(), [start]
    while work:
        a = work.pop()
        if a in seen or a in removed or a not in ins:
            continue
        seen.add(a)
        work += succ(ins[a])
    return seen


def check(blob, name):
    ins = decode(blob)
    rets = [a for a, i in ins.items() if i.mnemonic in ("ret", "retn")]
    pushes = [a for a, i in ins.items() if i.mnemonic == "push" and md.reg_name(i.operands[0].reg) == name]
    wr = [a for a, i in ins.items() if writes(i, name) and reload(i, name) is None and i.mnemonic != "pop"]
    spills = collections.defaultdict(list)
    for a, i in ins.items():
        k = spill_store(i, name)
        if k is not None:
            spills[k].append(a)
    reloads = collections.defaultdict(list)
    for a, i in ins.items():
        k = reload(i, name)
        if k is not None:
            reloads[k].append(a)
    out = {"instructions": len(ins), "rets": rets, "pushes": pushes, "writes": wr, "spills": dict(spills), "reloads": dict(reloads)}
    if pushes:
        out["verdict"] = "pushed"
        return out
    ok = True
    for k in set(spills) & set(reloads):
        # S1: removing the spill blocks makes every write unreachable from the entry
        s1 = all(w not in reach(ins, F, set(spills[k])) for w in wr)
        # S2: removing the reloads makes every RET unreachable from each write
        s2 = all(not (set(rets) & reach(ins, succ(ins[w])[0] if succ(ins[w]) else w, set(reloads[k]))) for w in wr)
        # S3: no other direct store to [rsp+k]; RSP changes only by push/pop/sub/add at the frame edges and calls
        other = [a for a, i in ins.items() if a not in spills[k] and i.operands and i.operands[0].type == X.X86_OP_MEM
                 and md.reg_name(i.operands[0].mem.base) == "rsp" and i.operands[0].mem.index == 0
                 and i.operands[0].mem.disp <= k < i.operands[0].mem.disp + i.operands[0].size
                 and i.operands[0].access & capstone.CS_AC_WRITE]
        rspw = [a for a, i in ins.items() if i.mnemonic in ("sub", "add", "lea", "mov", "and") and i.operands
                and i.operands[0].type == X.X86_OP_REG and md.reg_name(i.operands[0].reg) == "rsp"]
        out.update({"slot": k, "S1": s1, "S2": s2, "S3_other_stores": other, "rsp_writes": rspw})
        out["verdict"] = "restored" if s1 and s2 and not other and len(rspw) == 2 else "not established"
        return out
    out["verdict"] = "no spill/reload pair"
    return out


def main():
    blob = R.at(F, N)
    r12 = check(blob, "r12")
    r13 = check(blob, "r13")
    print("00533B20: %d instructions reached, RET at %s" % (r12["instructions"], " ".join("%08X" % a for a in r12["rets"])))
    print("R12 writes (not reloads): %s" % " ".join("%08X" % a for a in r12["writes"]))
    print("R12 spills %s; reloads %s" % ({hex(k): ["%08X" % a for a in v] for k, v in r12["spills"].items()},
                                         {hex(k): ["%08X" % a for a in v] for k, v in r12["reloads"].items()}))
    if "slot" in r12:
        print("slot [rsp+%#x]: S1 spill dominates every write %s; S2 reload on every write->RET path %s; S3 other stores %s; "
              "RSP writes %s" % (r12["slot"], r12["S1"], r12["S2"], r12["S3_other_stores"], ["%08X" % a for a in r12["rsp_writes"]]))
    print("R12 verdict: %s" % r12["verdict"])
    c1 = r13["verdict"] == "pushed"
    print("%s  C1 the same checker on R13 reports it pushed (no spill claimed)" % ("PASS" if c1 else "FAIL"))
    c2 = None
    if "slot" in r12 and r12["reloads"].get(r12["slot"]):
        a = r12["reloads"][r12["slot"]][0]
        i = next(md.disasm(blob[a - F:a - F + 16], a, 1))
        raw = bytearray(blob)
        o = a - F
        b = bytes(raw[o:o + i.size])
        # the ModRM reg field: r12 (100 with REX.R) -> r13 (101)
        mod = bytearray(b)
        mod[2] = (mod[2] & 0xC7) | (5 << 3)
        raw[o:o + i.size] = bytes(mod)
        mut = check(bytes(raw), "r12")
        c2 = mut["verdict"] != "restored"
        print("%s  C2 a private copy whose reload at %08X loads R13 instead (%s -> %s) fails: %s" % (
            "PASS" if c2 else "FAIL", a, b.hex(), bytes(mod).hex(), mut["verdict"]))
    return 0 if c1 and c2 else 1


if __name__ == "__main__":
    sys.exit(main())
