"""Every `or <w> ptr [r (- 0x80)], imm` whose r is loaded from [X+0x6A0] (disp 0) or [X+0x698] (disp -0x80) in the same
function, taint dropped at calls and killed on redefinition (the section 12/13 census's rule). Positive control: the
eight AL-10 bit-7 sites in 003112F0 must appear."""
import os, re, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
exec(open("disw.py").read().split("fn = int")[0])
def canon(r):
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp"}
    if r in m: return m[r]
    mm = re.match(r"(r\d+)[dwb]?$", r)
    return mm.group(1) if mm else r
hits = []
for fn, sz in sorted(funcs.items()):
    o = off(fn)
    if o is None or sz <= 0: continue
    t6a0, t698 = set(), set()
    for x in md.disasm(d[o:o + sz], fn):
        ops = x.op_str
        if x.mnemonic == "call":
            t6a0, t698 = set(), set(); continue
        m = re.match(r"(?:byte|word|dword|qword) ptr \[(\w+)(?: - 0x80)?\], (0x[0-9a-f]+|\d+)$", ops)
        if x.mnemonic == "or" and m:
            r = m.group(1); neg = " - 0x80" in ops
            if (not neg and r in t6a0) or (neg and r in t698):
                hits.append((x.address, fn, int(m.group(2), 0), "698" if neg else "6a0"))
            continue
        m = re.match(r"(\w+), qword ptr \[(\w+) \+ 0x(6a0|698)\]$", ops)
        if x.mnemonic == "mov" and m:
            (t6a0 if m.group(3) == "6a0" else t698).add(canon(m.group(1)))
            (t698 if m.group(3) == "6a0" else t6a0).discard(canon(m.group(1)))
            continue
        dst = ops.split(",")[0].strip()
        if x.mnemonic not in ("cmp", "test", "push") and dst and not re.match(r"(byte|word|dword|qword|xmmword) ptr", dst):
            t6a0.discard(canon(dst)); t698.discard(canon(dst))
c = collections.Counter(h[2] for h in hits)
print("or sites on the record flag byte via the two routes:", len(hits), "by immediate:", {hex(k): v for k, v in sorted(c.items())})
for a, f, imm, route in hits:
    print("  %08X %-45s %s route %s" % (a, names.get(f, ""), hex(imm), route))
ctrl = {0x31195E, 0x311986, 0x3119AE, 0x3119D6, 0x311A00, 0x311A2A, 0x311A54, 0x311A7E}
print("control: AL-10 bit-7 sites found", len(ctrl & {h[0] for h in hits}), "of", len(ctrl))
