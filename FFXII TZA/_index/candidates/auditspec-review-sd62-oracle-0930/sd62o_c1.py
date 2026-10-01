r"""sd62o_c1.py - SWE2-AUDIT-SPEC, SD-62 ORACLE review: C1 re-derived, and its blind shape named.

Defect named: the package's C1 looks only for `lea r,[x+0x50]` then a non-self store of r. 00639160's own base-class path
forms its node by `add rdx, 0x50` (0063921A), which that shape cannot see. Instrument: over every .pdata chunk whose
start lies in 00630000-0063FFFF (lane loader, aligned linear decode), find `lea r,[x+0x50]` OR `add r,0x50` (x, r not
rsp/rbp/rip), then within the next 14 instructions a `mov qword ptr [y(+d)], r` with y != r, stopping at a redefinition
of r. Positive controls: 00639160 must be found in BOTH shapes (lea 00639231 / 00639212, add 0063921A).
Also: the package's C1 gate asserts only `0x00639160 in fs`; a second writer would still PASS. And its store regex
`(?: \+ 0x[0-9a-f]+)?` cannot match `[y + 8]` (capstone prints displacements below 10 in decimal); this script
accepts both. Section X prints what the package's own regex would have matched, for comparison.
"""
import os, re, struct, sys, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

IB = T.IB
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))


def root(e):
    while True:
        uo = T.off(IB + e[2])
        if not (T.raw[uo] >> 3) & 4:
            return e
        cnt = T.raw[uo + 2]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


R64 = {}
for r64, subs in {"rax": "eax ax al", "rbx": "ebx bx bl", "rcx": "ecx cx cl", "rdx": "edx dx dl", "rsi": "esi si sil",
                  "rdi": "edi di dil"}.items():
    for s in [r64] + subs.split():
        R64[s] = r64
for n in range(8, 16):
    for s in ("r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n):
        R64[s] = "r%d" % n

hits = []
nchunks = 0
for e in PD:
    if not 0x00630000 <= IB + e[0] < 0x00640000:
        continue
    nchunks += 1
    ins = T.dis(IB + e[0], IB + e[1])
    for k, i in enumerate(ins):
        m = re.match(r"(\w+), \[(\w+) \+ 0x50\]$", i.op_str) if i.mnemonic == "lea" else None
        if m and m.group(2) not in ("rsp", "rbp", "rip"):
            r, shape = m.group(1), "lea"
        elif i.mnemonic == "add" and re.match(r"(\w+), 0x50$", i.op_str) and i.op_str.split(",")[0] not in ("rsp", "rbp"):
            r, shape = i.op_str.split(",")[0], "add"
        else:
            continue
        for c in ins[k + 1:k + 15]:
            mm = re.match(r"qword ptr \[(\w+)(?: \+ (?:0x[0-9a-f]+|\d+))?\], (\w+)$", c.op_str)   # capstone prints disp < 10 in decimal
            if c.mnemonic == "mov" and mm and mm.group(2) == r and mm.group(1) != r:
                hits.append((IB + root(e)[0], shape, i.address, c.address, "%s %s" % (c.mnemonic, c.op_str)))
                break
            first = c.op_str.split(",")[0].strip()
            if c.mnemonic not in ("cmp", "test", "push") and not first.startswith(("qword", "dword", "word", "byte")) \
                    and R64.get(first) == R64.get(r):
                break
print("chunks in 00630000-0063FFFF: %d" % nchunks)
fs = sorted({h[0] for h in hits})
print("+0x50 node writers (lea or add shape, non-self store): %d sites in %d functions: %s" % (
    len(hits), len(fs), " ".join("%08X" % f for f in fs)))
for h in hits:
    print("  %08X  %s at %08X -> store %08X  %s" % h)
own = [h for h in hits if h[0] == 0x00639160]
print("positive control 00639160 lea shape: %s; add shape: %s" % (
    "PASS" if any(h[1] == "lea" for h in own) else "FAIL", "PASS" if any(h[1] == "add" for h in own) else "FAIL"))

print("== X. same sweep with the PACKAGE's store regex (hex-only displacement)")
PK = re.compile(r"qword ptr \[(\w+)(?: \+ 0x[0-9a-f]+)?\], (\w+)$")
print("  [r8 + 8] matched by package regex: %s; by this script's: %s" % (
    bool(PK.match("qword ptr [r8 + 8], rdx")), bool(re.match(r"qword ptr \[(\w+)(?: \+ (?:0x[0-9a-f]+|\d+))?\], (\w+)$", "qword ptr [r8 + 8], rdx"))))
