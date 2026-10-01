"""SWE2-AUDIT-SEM inline bulk-copy census (own code). FABLE's bulk table (bulkcalls.tsv) lists CRT memcpy/memset/
memcpy_s calls and rep-string sites only; an inline copy loop (the compiler's unrolled movups loop, e.g. 002EF4A0)
is invisible to it and, because its stores use small negative displacements off an advancing pointer, also to
displacement sweeps. This census finds every such loop image-wide:
  - every .pdata fragment is decoded linearly;
  - a loop is a backward jcc/jmp inside the fragment;
  - in the loop body, a pointer register R advanced by a constant (add R, imm / lea R, [R + imm]) that is the base of
    at least one memory store (any width) is an inline bulk writer;
  - its base is the last write of R before the loop head (rip-relative lea -> constant address; otherwise printed),
    its per-iteration stride is the advance, and its trip count is the constant loaded into the counter register
    that the loop decrements (sub X, 1 / dec X / cmp against an immediate), when there is one.
Output: one TSV row per loop: loop head, jump, R, stride, store span per iteration (min..max disp, width),
base form, base value (constant when rip-lea), trip count (or ?), extent = count*stride.
Controls: 002EF4A0 (rcx = lea 021B290C, stride 0x80, count 0xC0, extent 0x6000) and 00229B98 (rax = image + 0x2200)
must be found.
"""
import struct, re, sys
import img

PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE))
R64 = {}
for r in ("ax", "bx", "cx", "dx", "si", "di", "bp"):
    R64["r" + r] = "r" + r
    R64["e" + r] = "r" + r
for n in range(8, 16):
    R64["r%d" % n] = "r%d" % n
    R64["r%dd" % n] = "r%d" % n
MEM = re.compile(r"^(byte|word|dword|qword|xmmword|ymmword) ptr \[([^\]]+)\]$")
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}

def parse_mem(inner):
    toks = re.findall(r"([+-]?)\s*([\w*]+)", inner)
    base, disp, idx = None, 0, None
    for sign, t in toks:
        if re.fullmatch(r"0x[0-9a-f]+|\d+", t):
            disp += int(t, 0) * (-1 if sign == "-" else 1)
        elif base is None:
            base = t
        else:
            idx = t
    return base, idx, disp

def rip_target(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)
    if not m:
        return None
    return x.address + x.size + int(m.group(2), 0) * (1 if m.group(1) == "+" else -1)

# leaf functions have no .pdata entry: add every uncovered .text gap, trimmed of int3/nop padding
t0, t1, _ = img.text_range()
cov = sorted(PD)
gaps, cur = [], img.BASE + t0
for b, e in cov:
    if b > cur:
        gaps.append((cur, b))
    cur = max(cur, e)
if cur < img.BASE + t1:
    gaps.append((cur, img.BASE + t1))
for gb, ge in gaps:
    raw = img.rd(gb, ge - gb) or b""
    k = 0
    while k < len(raw) and raw[k] in (0xCC, 0x90):
        k += 1
    if ge - gb - k > 4:
        PD.append((gb + k, ge))
sys.stderr.write("fragments %d (with %d gaps)" % (len(PD), len(gaps)) + chr(10))
rows = []
for fb, fe in PD:
    ins = list(img.md.disasm(img.rd(fb, fe - fb) or b"", fb))
    if not ins:
        continue
    pos = {x.address: i for i, x in enumerate(ins)}
    for j, x in enumerate(ins):
        if not (x.mnemonic.startswith("j") and re.fullmatch(r"0x[0-9a-f]+", x.op_str)):
            continue
        tgt = int(x.op_str, 16)
        if tgt > x.address or tgt not in pos:
            continue
        body = ins[pos[tgt]:j + 1]
        adv = {}
        for y in body:
            o = [s.strip() for s in y.op_str.split(",")]
            if y.mnemonic == "add" and len(o) == 2 and o[0] in R64 and o[0].startswith("r") and re.fullmatch(r"0x[0-9a-f]+|\d+", o[1]):
                adv[R64[o[0]]] = int(o[1], 0)
            m = re.fullmatch(r"\[(\w+) \+ (0x[0-9a-f]+|\d+)\]", o[1]) if y.mnemonic == "lea" and len(o) == 2 else None
            if m and o[0] in R64 and R64.get(m.group(1)) == R64[o[0]]:
                adv[R64[o[0]]] = int(m.group(2), 0)
        if not adv:
            continue
        for R, stride in adv.items():
            st = []
            for y in body:
                o = [s.strip() for s in y.op_str.split(",")]
                mm = MEM.match(o[0]) if o else None
                if not mm or y.mnemonic in ("cmp", "test") or y.mnemonic.startswith(("j", "prefetch", "bt")):
                    continue
                if len(o) < 2 and y.mnemonic not in ("inc", "dec", "not", "neg"):
                    continue
                b, idx, d = parse_mem(mm.group(2))
                if R64.get(b) == R and idx is None:
                    st.append((d, W[mm.group(1)]))
            if not st:
                continue
            # base: last write of R before the loop head
            basef, baseval = "?", None
            for y in reversed(ins[max(0, pos[tgt] - 40):pos[tgt]]):
                o = [s.strip() for s in y.op_str.split(",")]
                if o and R64.get(o[0]) == R and y.mnemonic not in ("cmp", "test", "push"):
                    basef = "%08X %s %s" % (y.address, y.mnemonic, y.op_str)
                    if y.mnemonic == "lea" and "rip" in y.op_str:
                        baseval = rip_target(y)
                    break
            # trip count: a register decremented in the body and loaded with an immediate before the head
            count = None
            for y in body:
                o = [s.strip() for s in y.op_str.split(",")]
                c = None
                if y.mnemonic == "sub" and len(o) == 2 and o[1] == "1" and o[0] in R64:
                    c = R64[o[0]]
                if y.mnemonic == "dec" and o and o[0] in R64:
                    c = R64[o[0]]
                if c:
                    for z in reversed(ins[max(0, pos[tgt] - 40):pos[tgt]]):
                        oz = [s.strip() for s in z.op_str.split(",")]
                        if oz and R64.get(oz[0]) == c and z.mnemonic not in ("cmp", "test", "push"):
                            if z.mnemonic == "mov" and len(oz) == 2 and re.fullmatch(r"0x[0-9a-f]+|\d+", oz[1]):
                                count = int(oz[1], 0)
                            break
            lo = min(d for d, w in st)
            hi = max(d + w for d, w in st)
            rows.append((tgt, x.address, R, stride, lo, hi, len(st), basef, baseval, count))

print("head\tjump\treg\tstride\tstore_lo\tstore_hi\tnstores\tbase_def\tbase_const\tcount\textent")
for r in rows:
    ext = r[3] * r[9] if r[9] else None
    print("%08X\t%08X\t%s\t%#x\t%d\t%d\t%d\t%s\t%s\t%s\t%s" % (
        r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], "%08X" % r[8] if r[8] else "-",
        "%#x" % r[9] if r[9] else "?", "%#x" % ext if ext else "?"))
sys.stderr.write("loops: %d\n" % len(rows))
