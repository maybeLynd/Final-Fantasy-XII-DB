"""rc12_slots.py - RC-12 (ORACLE, 2026-09-30): which footer word each reader of an actor entry's +0x18 asks for.

Part A (image). In each named function (full .pdata extent), every call to ImageAddress_ResolveRuntimePointer 0020E600
whose ecx was loaded from [X+0x18] with X loaded from [R+0x40] (the actor entry, record+0x40). After the call, the
first word read [rcx + base + D] gives the footer byte offset D, and the compare before it gives the bound constant C
(`cmp Creg16, word [rcx+base]`; Creg's last immediate). Every such reader is preceded by a record-override word
`movzx eax, word [R + O]` compared with 0xFFFF; O is printed as a second, independent operand.
  footer word index k = (D - 2) / 2  (the tool's tFuncFooter {u16 count; u16 special[18]}: special[k] at +2+2k)
Control A: 0025DF00's site must read D = 0x18 with C = 11.

Part B (authored data). For every actor in the 1,114 raw script images (corpus/us/*.s000), read the footer at the entry's
+0x18 and record, for each word index k, the NAME of the function it points at (function-name table at entry +0x10,
names pool at header +0x4C). This joins the byte offset directly to a function name, bypassing the decompiler's
printed number. Control B: the decompiler's printed number for a declaration equals k for every name (the tool's
_assignSpecialFunctions sets specialType = i for special[i]).
"""
import collections, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
FUNCS = [0x0025DF00, 0x0025AE00, 0x0025B820, 0x0025BAD0, 0x0025C230, 0x0025C830, 0x00263050, 0x00263D40]
R16 = {"ax": "eax", "cx": "ecx", "dx": "edx", "bx": "ebx", "si": "esi", "di": "edi", "bp": "ebp"}


def r32(r16):
    if r16 in R16:
        return R16[r16]
    return r16[:-1] + "d" if r16.endswith("w") else r16


def partA():
    rows = []
    for f in FUNCS:
        ins = img.fn_ins(img.owner(f))
        for k, x in enumerate(ins):
            if not (x.mnemonic == "call" and x.op_str == "0x20e600"):
                continue
            pre = [p.mnemonic + " " + p.op_str for p in ins[max(0, k - 5):k]]
            if not any(re.match(r"mov ecx, dword ptr \[r\w+ \+ 0x18\]", p) for p in pre):
                continue
            if not any(re.match(r"mov r\w+, qword ptr \[r\w+ \+ 0x40\]", p) for p in pre):
                continue
            D = C = O = None
            imm = {}
            for p in ins[max(0, k - 40):k]:
                m = re.match(r"(\w+), (0x[0-9a-f]+|\d+)$", p.op_str) if p.mnemonic == "mov" else None
                if m:
                    imm[m.group(1)] = int(m.group(2), 0)
                m = re.match(r"movzx eax, word ptr \[r\w+ \+ (0x[0-9a-f]+|\d+)\]$", p.mnemonic + " " + p.op_str)
                if m:
                    O = int(m.group(1), 0)
            for p in ins[k + 1:k + 10]:
                t = p.mnemonic + " " + p.op_str
                if p.mnemonic == "mov":
                    m = re.match(r"(\w+), (0x[0-9a-f]+|\d+)$", p.op_str)
                    if m:
                        imm[m.group(1)] = int(m.group(2), 0)
                m = re.match(r"cmp (\w+), word ptr \[rcx(?: \+ r\w+)?\]$", t)
                if m:
                    C = imm.get(r32(m.group(1)), "reg %s" % m.group(1))
                m = re.match(r"mov[sz]x \w+, word ptr \[rcx(?: \+ r\w+)? \+ (0x[0-9a-f]+|\d+)\]$", t)
                if m and D is None:
                    D = int(m.group(1), 0)
                    site = p.address
                    break
            else:
                site = None
            rows.append((f, x.address, site, D, C, O))
    return rows


def cstr(b, o):
    e = b.index(b"\0", o)
    return b[o:e].decode("cp932", "replace")


def partB():
    by_k = collections.defaultdict(collections.Counter)
    printed_mismatch, printed_ok, images, actors = 0, 0, 0, 0
    decl = re.compile(r"\bfunction\s+([^\s(]+)\((\d+)\)")
    for fn in sorted(os.listdir(CORPUS)):
        if not fn.endswith(".s000"):
            continue
        b = open(os.path.join(CORPUS, fn), "rb").read()
        if len(b) < 0x90 or struct.unpack_from("<I", b, 0)[0] != 0x8000000B:
            continue
        images += 1
        tab, pool = struct.unpack_from("<I", b, 0x18)[0], struct.unpack_from("<I", b, 0x4C)[0]
        n = struct.unpack_from("<I", b, tab)[0]
        names_here = collections.Counter()
        for a in range(n):
            e = tab + 4 + a * 0x30
            fnames, sepa = struct.unpack_from("<I", b, e + 0x10)[0], struct.unpack_from("<I", b, e + 0x18)[0]
            nf = struct.unpack_from("<I", b, fnames)[0]
            cnt = struct.unpack_from("<H", b, sepa)[0]
            actors += 1
            for k in range(min(cnt, 18)):
                w = struct.unpack_from("<H", b, sepa + 2 + 2 * k)[0]
                if w == 0xFFFF or w >= nf:
                    continue
                name = cstr(b, pool + struct.unpack_from("<I", b, fnames + 4 + 8 * w)[0])
                by_k[k][name] += 1
                names_here[(name, k)] += 1
        txt = os.path.join(CORPUS, fn[:-5] + ".txt")
        if os.path.exists(txt):
            for m in decl.finditer(open(txt, encoding="utf-8", errors="replace").read()):
                if (m.group(1), int(m.group(2))) in names_here:
                    printed_ok += 1
                else:
                    printed_mismatch += 1
    return by_k, images, actors, printed_ok, printed_mismatch


LISTED = {0x0025AE00, 0x0025B820, 0x0025BAD0, 0x0025C230, 0x0025C830, 0x00263050, 0x00263D40, 0x0025DF00}


def partC():
    """image-wide: every resolve call whose ecx is [R+0x18] with R loaded from [X+0x40] (the actor entry)."""
    out = []
    for a, kind in img.calls_to(0x0020E600):
        f = img.owner(a)
        if f is None:
            continue
        ins = img.fn_ins(f)
        pos = [i for i, x in enumerate(ins) if x.address == a]
        if not pos:
            continue
        i = pos[0]
        pre = ins[max(0, i - 6):i]
        m18 = [p for p in pre if p.mnemonic == "mov" and re.match(r"ecx, dword ptr \[(r\w+) \+ 0x18\]$", p.op_str)]
        if not m18:
            continue
        R = re.match(r"ecx, dword ptr \[(r\w+) \+ 0x18\]$", m18[-1].op_str).group(1)
        if not any(p.mnemonic == "mov" and re.match(R + r", qword ptr \[r\w+ \+ 0x40\]$", p.op_str) for p in pre):
            continue
        O = None
        for p in ins[max(0, i - 12):i]:
            mm = re.match(r"movzx \w+, word ptr \[r\w+ \+ (0x[0-9a-f]+|\d+)\]$", p.mnemonic + " " + p.op_str)
            if mm and 0xC8 <= int(mm.group(1), 0) <= 0xEA:
                O = int(mm.group(1), 0)
            mm = re.match(r"movzx \w+, word ptr \[r\w+ \+ r\w+\*2 \+ 0xc8\]$", p.mnemonic + " " + p.op_str)
            if mm:
                O = "0xc8+2*reg"
        form, val = "NONE", None
        for p in ins[i + 1:i + 12]:
            t = p.mnemonic + " " + p.op_str
            mm = re.match(r"mov[sz]x \w+, word ptr \[rcx(?: \+ r\w+)? \+ (0x[0-9a-f]+|\d+)\]$", t)
            if mm:
                form, val = "FIXED", (int(mm.group(1), 0) - 2) // 2
                break
            mm = re.match(r"mov[sz]x \w+, word ptr \[rcx \+ (r\w+)\*2 \+ 2\]$", t)
            if mm:
                form, val = "VARIABLE", mm.group(1)
                break
            mm = re.match(r"mov[sz]x \w+, word ptr \[rcx \+ (r\w+)\*2(?: \+ 2)?\]$", t)
            if mm or re.match(r"inc eax$", t):
                form, val = "LISTWALK", None
                break
            if p.mnemonic in ("call", "ret"):
                break
        out.append((f, a, form, val, O))
    return out


def main():
    rows = partA()
    print("PART A: footer reads (function, resolve call, read site, footer byte offset D, word index k=(D-2)/2, "
          "bound constant C, record override word O)")
    for f, call, site, D, C, O in rows:
        k = (D - 2) // 2 if D is not None else None
        print("  %08X call %08X read %s D=%s k=%s C=%s O=%s" % (f, call, "%08X" % site if site else "-",
                                                             hex(D) if D is not None else "-", k, C,
                                                             hex(O) if O is not None else "-"))
    ctl = [r for r in rows if r[0] == 0x0025DF00 and r[3] == 0x18 and r[4] == 11]
    print("CONTROL A 0025DF00 reads D=0x18 with bound 11: %s" % ("PASS" if ctl else "FAIL"))
    by_k, images, actors, ok, bad = partB()
    print("\nPART B: raw footers of %d images, %d actors; function name at each footer word index k" % (images, actors))
    for k in range(18):
        print("  k=%2d (byte +0x%02X): %s" % (k, 2 + 2 * k, ", ".join("%s x%d" % kv for kv in by_k[k].most_common(4)) or "(never set)"))
    print("CONTROL B decompiler's printed number == raw footer index k: %d declarations agree, %d disagree -> %s"
          % (ok, bad, "PASS" if ok > 0 and bad == 0 else "FAIL"))
    rc = partC()
    print("\nPART C: image-wide actor-entry footer resolves (base loaded from [..+0x40]); form FIXED k, VARIABLE index "
          "register, LISTWALK past the footer, NONE; O = record override word read first")
    names = {k: (by_k[k].most_common(1)[0][0] if by_k[k] else "(never set)") for k in range(18)}
    for f, a, form, val, O in rc:
        extra = ("k=%d %s" % (val, names[val])) if form == "FIXED" else (str(val) if val else "")
        print("  %s %08X call %08X %-8s %s O=%s" % ("listed" if f in LISTED else "OTHER ", f, a, form, extra,
                                                    hex(O) if isinstance(O, int) else O))
    got = set((f, a) for f, a, *_ in rc)
    ctlc = all((r[0], r[1]) in got for r in rows)
    print("CONTROL C every Part A site is found by the image-wide census: %s (%d sites, %d functions)"
          % ("PASS" if ctlc else "FAIL", len(rc), len(set(r[0] for r in rc))))
    return 0 if ctl and ok > 0 and bad == 0 and ctlc else 1


if __name__ == "__main__":
    sys.exit(main())
