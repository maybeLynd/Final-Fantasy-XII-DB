"""rc14_sweep.py - RC-14 (ORACLE, 2026-09-30): image-wide sweep for a byte store of 2 that can land on an actor resource
entry's +0x11 run state. Every .pdata chain root is disassembled whole (all fragments). Candidate shapes:
  S1  mov byte [R + 0x11], 2                       (immediate 2 at displacement 0x11)
  S2  mov byte [R + 0x11], reg8                    where reg's last straight-line write is the immediate 2
  S3  mov byte [R (+ d)], 2 or reg8=2              where R was advanced by 0x11 earlier in the function
                                                   (`add R, 0x11` or `lea R, [.. + 0x11]`), effective displacement d+0x11
  S4  cmp byte [P], 1 ... mov byte [P], 2          the promotion shape with the SAME memory operand, any displacement,
                                                   within 6 instructions
  S5  mov byte [R + 0x11], reg8 (reg not provably 2) in an ENTRY function (below): listed so a variable writer that
      could be 2 is not missed
  S6  the same variable store at displacement 0x11 in any other function, for a by-hand base verdict
Coverage: every .pdata chain root, plus a linear sweep of the .text bytes no .pdata entry covers (leaf code has no
unwind data), split into runs at ret / int3 / jmp.
ENTRY evidence for a function: it loads a qword from [.. + 0xa0] (the record's entry-array pointer) AND uses the 0x14
stride (`add r, 0x14`, `lea r, [r + r*4]`, or `imul r, r, 0x14`). A hit in a function without it is printed with the
base register's last straight-line definition, for a by-hand verdict.
Controls: 003DBB35 (S3/S4), 003DB245 (S3/S4), 003DBCAC (S3/S4) and the insert's 003DB8E9 / 003DB9E4 (S5, r12b = the
caller's state argument) must all be found.
"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img

R8 = {"al": "eax", "bl": "ebx", "cl": "ecx", "dl": "edx", "sil": "esi", "dil": "edi", "bpl": "ebp", "r8b": "r8d",
      "r9b": "r9d", "r10b": "r10d", "r11b": "r11d", "r12b": "r12d", "r13b": "r13d", "r14b": "r14d", "r15b": "r15d"}
FAM = {}
for b8, d32 in R8.items():
    q = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}.get(d32, d32[:-1])
    for n in (b8, d32, q):
        FAM[n] = d32


def last_def(ins, k, reg):
    fam = FAM.get(reg, reg)
    for j in range(k - 1, max(-1, k - 40), -1):
        x = ins[j]
        ops = [o.strip() for o in x.op_str.split(",")]
        if x.mnemonic == "call":
            if fam in ("eax", "ecx", "edx", "r8d", "r9d", "r10d", "r11d"):
                return "clobbered by call %s" % x.op_str
            continue
        if ops and FAM.get(ops[0], ops[0]) == fam and x.mnemonic not in ("cmp", "test", "bt", "push"):
            return "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
    return "?"


def imm_of(defn):
    m = re.search(r" mov \w+, (0x[0-9a-f]+|\d+)$", defn)
    if m:
        return int(m.group(1), 0)
    if re.search(r" xor (\w+), \1$", defn):
        return 0
    return None


def gap_streams():
    """linear disassembly of .text bytes no .pdata entry covers (leaf code without unwind data), split at ret/int3."""
    cov = sorted((b, e) for b, e, u in img.PDATA)
    gaps, cur = [], img.T0
    for b, e in cov:
        if b > cur:
            gaps.append((cur, b))
        cur = max(cur, e)
    if cur < img.T0 + img.TN:
        gaps.append((cur, img.T0 + img.TN))
    for b, e in gaps:
        pos = b
        while pos < e:
            chunk = img.rd(pos, e - pos)
            got = list(img.md.disasm(chunk, pos))
            if not got:
                pos += 1
                continue
            run = []
            for x in got:
                run.append(x)
                if x.mnemonic in ("ret", "int3", "jmp"):
                    if len(run) > 1:
                        yield ("GAP%08X" % run[0].address, run)
                    run = []
            if len(run) > 1:
                yield ("GAP%08X" % run[0].address, run)
            pos = got[-1].address + got[-1].size
            if pos < e:
                pos += 1


def streams():
    for root in sorted(img.ROOTS):
        try:
            yield (root, img.fn_ins(root))
        except Exception:
            continue
    for name, ins in gap_streams():
        yield (name, ins)


def main():
    hits = []
    nfun = 0
    for root, ins in streams():
        nfun += 1
        txt = [x.mnemonic + " " + x.op_str for x in ins]
        entry = any(re.search(r"qword ptr \[r\w+ \+ 0xa0\]", t) for t in txt) and any(
            re.match(r"add r\w+, 0x14$", t) or re.match(r"lea r\w+, \[(r\w+) \+ \1\*4\]$", t) or
            re.match(r"imul r\w+, r\w+, 0x14$", t) for t in txt)
        adv = {}
        for k, x in enumerate(ins):
            t = txt[k]
            m = re.match(r"add (r\w+), 0x11$", t) or re.match(r"lea (r\w+), \[r\w+(?: \+ r\w+\*\d)? \+ 0x11\]$", t)
            if m:
                adv[m.group(1)] = x.address
            if x.mnemonic != "mov" or not x.op_str.startswith("byte ptr ["):
                continue
            m = re.match(r"byte ptr \[(r\w+)(?: \+ (r\w+)(?:\*(\d))?)?(?: ([+-]) (0x[0-9a-f]+|\d+))?\], (\w+)$", x.op_str)
            if not m or m.group(1) in ("rsp", "rip"):
                continue
            base, disp = m.group(1), (int(m.group(5), 0) * (-1 if m.group(4) == "-" else 1) if m.group(5) else 0)
            src = m.group(6)
            val = int(src, 0) if re.match(r"^(0x[0-9a-f]+|\d+)$", src) else None
            srcdef = None
            if val is None and src in FAM:
                srcdef = last_def(ins, k, src)
                val = imm_of(srcdef)
            shapes = []
            if disp == 0x11 and val == 2:
                shapes.append("S1" if re.match(r"^(0x[0-9a-f]+|\d+)$", src) else "S2")
            if base in adv and val == 2 and adv[base] < x.address:
                shapes.append("S3(eff +0x%x)" % (disp + 0x11))
            if val == 2:
                mem = x.op_str.rsplit(",", 1)[0]
                for j in range(max(0, k - 6), k):
                    if ins[j].mnemonic == "cmp" and ins[j].op_str == mem + ", 1":
                        shapes.append("S4")
                        break
            if disp == 0x11 and val != 2 and entry:
                shapes.append("S5")
            elif disp == 0x11 and val is None:
                shapes.append("S6")
            if shapes:
                hits.append((root, x.address, t, shapes, entry, last_def(ins, k, base), srcdef))
    print("streams disassembled (.pdata roots + uncovered-gap runs): %d; candidate stores: %d" % (nfun, len(hits)))
    for root, a, t, shapes, entry, bdef, sdef in hits:
        print("%-11s %08X %-40s %-22s %s  base<-%s%s" % (root if isinstance(root, str) else "%08X" % root, a, t, "+".join(shapes), "ENTRY-FN" if entry else "other ",
                                                     bdef, ("  src<-" + sdef) if sdef else ""))
    got = set(h[1] for h in hits)
    ctl = {c: (c in got) for c in (0x003DBB35, 0x003DB245, 0x003DBCAC, 0x003DB8E9, 0x003DB9E4)}
    print("CONTROLS: " + ", ".join("%08X %s" % (c, "PASS" if v else "FAIL") for c, v in ctl.items()))
    return 0 if all(ctl.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
