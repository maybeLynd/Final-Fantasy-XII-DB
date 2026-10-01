"""gr8_record_census_check.py - GR-8: every access to the per-unit 64-byte record (SWE2-STRUCT for OPUS, 2026-09-30)
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and structflow.py (seed_leas added
for this row: a `lea r, [rip -> address]` seeds the array base; with seed_leas omitted structflow is unchanged).

The record: 0208D480 + kind*0x40 (party, stats +4) or 0208DE80 + unit[+0xEA9]*0x40 (everyone else). The second bank
holds 32 records (slot index 0..31), so the two banks span 0208D480..0208E67F; 0208E680 is the next object.

S1  anchors: every rip-relative reference into 0208D480..0208E67F is a lea, 34 in 17 functions (0208D480 x16,
    0208DE80 x16, 0208D494 / 0208DE94 = record +0x14 x1 each, in 00386860); no load or store addresses a record directly.
S2  extent-independent: a raw byte scan of .text for rip displacements landing in the banks decodes to the same 34
    leas; no aligned dword / qword in any section holds a bank address (VA or RVA); no instruction carries a bank
    address as an absolute displacement or immediate.
S3  the neighbours cannot reach in: the lea anchors just below (0208D320..0208D354) are bounded short arrays ending
    at or before 0208D454; the lea anchors above (0208E680, 0208E6E0, 0208E6E4) index upward only.
S3b no memset / memcpy / memcpy_s call based on a static lea in 02000000..0208E67F reaches the banks (two memsets at
    02064E30, 0x200 and 0x4000 bytes).
S4  structflow from the 17 functions (stride 0x40, depth 3, returns followed): 57 accesses, all inside the 17 anchor
    functions, none at an unknown offset; no escape, copy, indirect call, stack argument or hand-off of a record pointer.
S5  no call or tail jump in any walked function receives a record pointer in rcx / rdx / r8 / r9 (callees outside the
    extent list included), and no rep stos / movs runs on one.
S6  every anchor function's extent ends in ret / jmp followed by padding or the next function (nothing is cut off).
S7  no access covers any byte of +0x20..+0x3F; the accessed bytes are exactly +0x00..+0x1F; +0x13, +0x16, +0x17 are
    written only by the wide clears and never read.
S8  positive controls: 00386C10 clears +0x00..+0x1F with four qword stores; +0x10 (00387ADE w, 0038710E r, 00385FF7 r),
    +0x12 (003857DD, 0038886B), +0x1C (0033CB60, 0033DA73) are found.
S9  the census is stable: depth 5, and depth 3 without following returns, give the same access set.
S10 readings the census rests on (instruction text): the preview's prefix clear restores +0x10 (003857A3 -> 003857E1),
    so it does not store the previewed id there; the resolver reads +0x08 -> result kind 0xA and +0x04 -> kind 6;
    +0x0C is set by 00387B00 (15 callers) and read by 002FA290, reached from 003B8670 via 00322850; +0x18 is compared
    with and set to the walking-MP accumulator (002F9474 / 002F95A6).
Prints PASS/FAIL per check, the per-offset census, and FAILS n last.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import structflow as S  # noqa: E402
import numpy as np  # noqa: E402
import pefile  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
LO, HI = 0x0208D480, 0x0208E680
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# S1 - anchors
refs = [(g, f, a, k) for g in c["refs"] if LO <= g < HI for f, a, k in c["refs"][g]]
kinds = sorted({k for _, _, _, k in refs})
funcs = sorted({f for _, f, _, _ in refs})
per = {g: sum(1 for x in refs if x[0] == g) for g in {x[0] for x in refs}}
ANCH = {0x002F9400, 0x002FA290, 0x0033CB10, 0x0033D890, 0x00385680, 0x00385F60, 0x00386860, 0x00386C10, 0x00387090,
        0x00387A50, 0x00387B00, 0x00388660, 0x00388D50, 0x00389C60, 0x0038DA00, 0x0038EBE0, 0x0038ED40}
check("S1", kinds == ["lea"] and len(refs) == 34 and set(funcs) == ANCH
      and per == {0x0208D480: 16, 0x0208DE80: 16, 0x0208D494: 1, 0x0208DE94: 1},
      "%d rip references into the banks, kinds %s, in %d functions; per target %s"
      % (len(refs), kinds, len(funcs), {"%08X" % g: n for g, n in sorted(per.items())}))

# S2 - extent-independent scans
pe = pefile.PE(R.b.EXE, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
raw, dw, qw = set(), [], []
for s in pe.sections:
    d = s.get_data()
    va = base + s.VirtualAddress
    a4 = np.frombuffer(d[:len(d) // 4 * 4], dtype="<u4")
    for lo, hi in ((LO, HI), (LO - base, HI - base)):
        dw += [va + 4 * i for i in np.nonzero((a4 >= lo) & (a4 < hi))[0]] if not s.Characteristics & 0x20000000 else []
    a8 = np.frombuffer(d[:len(d) // 8 * 8], dtype="<u8")
    qw += [va + 8 * i for i in np.nonzero((a8 >= LO) & (a8 < HI))[0]]
    if not s.Characteristics & 0x20000000:
        continue
    b = np.frombuffer(d, dtype=np.uint8).astype(np.int64)
    n = len(d) - 4
    disp = b[0:n] | (b[1:n + 1] << 8) | (b[2:n + 2] << 16) | (b[3:n + 3] << 24)
    disp = np.where(disp >= 1 << 31, disp - (1 << 32), disp)
    pos = np.arange(n, dtype=np.int64) + va
    for imm in (0, 1, 2, 4):
        tgt = pos + 4 + imm + disp
        for p in np.nonzero((tgt >= LO) & (tgt < HI))[0]:
            p = int(p) + va
            for back in range(11, 0, -1):          # earliest start first: a REX prefix is part of the instruction
                st = p - back
                try:
                    i = next(R.md.disasm(R.at(st, 16), st, 1))
                except StopIteration:
                    continue
                if i.address + i.size < p + 4:
                    continue
                if any(op.type == 3 and op.mem.base == T.RIP and i.address + i.size + op.mem.disp == int(tgt[p - va])
                       for op in i.operands):
                    raw.add((i.address, int(tgt[p - va])))
                    break
ref_sites = {(a, g) for g, f, a, k in refs}
absdisp = []
rx = re.compile(r"0x208d[4-9a-f][0-9a-f]{2}\b|0x208e[0-6][0-9a-f]{2}\b")
for f, n in sorted(SZ.items()):
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        if "rip" not in i.op_str and rx.search(i.op_str):
            absdisp.append(i.address)
check("S2", raw == ref_sites and not dw and not qw and not absdisp,
      "raw .text scan decodes %d rip leas into the banks (the S1 set: %s); aligned dwords (VA/RVA) outside code %d, "
      "qwords %d, absolute displacements/immediates %d" % (len(raw), raw == ref_sites, len(dw), len(qw), len(absdisp)))

# S3 - neighbours
below = sorted({(g, a) for g in c["refs"] if 0x0208D300 <= g < LO for f, a, k in c["refs"][g] if k == "lea"})
above = sorted({(g, a) for g in c["refs"] if HI <= g < HI + 0x100 for f, a, k in c["refs"][g] if k == "lea"})
neg = [i.address for i in R.md.disasm(R.at(0x003846F0, SZ[0x003846F0]), 0x003846F0)
       if re.search(r"\[r(?!sp|bp)\w+ - 0x", i.op_str)]
ab = [
    txt(0x00238861) == "call 0x3846f0" and not neg,                                                   # 0208E680 as an object
    txt(0x0023CD3C) == "lea rcx, [rax + rax*4]" and txt(0x0023CD48) == "mov eax, dword ptr [rcx + rdx + 4]",   # 0208E6E0 + 20*i
    txt(0x002418CC) == "lea rax, [rax + rax*4]" and txt(0x002418D0) == "mov ecx, dword ptr [rcx + rax*4]",     # 0208E6E4 + 20*i
]
nb = [
    txt(0x0031B4F0) == "cmp ecx, 0xf" and txt(0x0031B4FF) == "movzx eax, word ptr [rcx + rax*2]",      # 0208D334 + 2*i, i <= 15
    txt(0x00329213).startswith("lea rcx, [rip") and txt(0x0030C852) == "mov ecx, 1",                  # 0208D328 + 4*1
    txt(0x0031EB13).startswith("lea rcx, [rip") and txt(0x0034B043) == "call 0x53dd10" and txt(0x0053DD10) == "mov eax, 1",
    txt(0x002339BC) == "mov ecx, 0x40" and txt(0x002339D3) == "shl rdi, 7" and txt(0x002339E2) == "rep stosw word ptr [rdi], ax"
    and txt(0x00233933).startswith("xor byte ptr [rip"),                                             # 0208D354 + 0x80*(0|1), 0x80 bytes
    txt(0x00237D36) == "or dword ptr [rcx], ebx" and txt(0x00237D30) == "cmovne rcx, r15",           # 0208D320 / 0208D324 scalars
]
check("S3", [g for g, a in below] == [0x0208D320, 0x0208D324, 0x0208D328, 0x0208D328, 0x0208D334, 0x0208D334, 0x0208D354]
      and all(nb) and [g for g, a in above] == [0x0208E680, 0x0208E6E0, 0x0208E6E4, 0x0208E6E4] and all(ab),
      "lea anchors below the banks %s, each bounded (%s): the 0x80-byte halves at 0208D354 end at 0208D454; lea anchors "
      "above %s index upward only (%s: 0208E680 is 003846F0's object, no negative displacement in it; 0208E6E0 / "
      "0208E6E4 are 20-byte entries)" % (["%08X" % g for g, a in below], nb, ["%08X" % g for g, a in above], ab))

# S3b - bulk clears / copies from a base below: memset / memcpy / memcpy_s calls with a rip lea into 02000000..the banks'
# end among the 16 instructions before the call
BULK = {0x00861EC0: "memset", 0x00861EBA: "memcpy", 0x00861FC8: "memcpy_s"}
bulk = []
for tgt_, name in BULK.items():
    for f, site in sorted(c["calls"].get(tgt_, ())):
        st = max(f, site - 64)
        ins = [i for i in R.md.disasm(R.at(st, site - st + 5), st) if i.address <= site][-16:]
        for i in ins:
            for op in i.operands:
                if i.mnemonic == "lea" and op.type == 3 and op.mem.base == T.RIP \
                        and 0x02000000 <= i.address + i.size + op.mem.disp < HI:
                    ln = [j.op_str for j in ins if j.op_str.startswith("r8d, 0x")]
                    bulk.append((name, site, i.address + i.size + op.mem.disp, ln[-1] if ln else None))
check("S3b", sorted(bulk) == [("memset", 0x004ADDA4, 0x02064E30, "r8d, 0x200"), ("memset", 0x0051D1E3, 0x02064E30, "r8d, 0x4000")],
      "bulk calls based in 02000000..0208E67F: %s - both end by 02068E30, below the banks"
      % ["%s@%08X %08X %s" % b for b in sorted(bulk)])

# S4 - structflow
seeds = {(f, g): (0x14 if g in (0x0208D494, 0x0208DE94) else 0) for g, f, a, k in refs}


def flow(depth, follow=True):
    g = S.Flow(list(range(64)), depth, follow_returns=follow, stride=0x40, slot=0, seed_leas=seeds)
    g.run(sorted(ANCH))
    return g


g = flow(3)
RMW = ("or", "and", "xor", "add", "sub", "inc", "dec", "bts", "btr", "btc", "neg", "not", "shl", "shr", "sar")


def rw(h):
    f, a, kind, form, off, w, text = h
    m = text.split()[0]
    if kind == "r":
        return "rw" if m in ("inc", "dec", "neg", "not") else "r"
    return "rw" if m in RMW else "w"


hits = sorted(g.hits, key=lambda h: (h[4], h[0], h[1]))
outside = sorted({h[0] for h in hits} - ANCH)
check("S4", len(hits) == 57 and not outside and not g.unk and not g.esc and not g.copies and not g.indirect
      and not g.stackargs and not g.handoffs and len(g.seeded) == 34,
      "%d accesses from %d seeded leas over %d walked functions; outside the anchors %s; unknown %d, escapes %d, copies %d, "
      "indirect %d, stack args %d, hand-offs %d" % (len(hits), len(g.seeded), len(g.entry), outside, len(g.unk), len(g.esc),
                                                  len(g.copies), len(g.indirect), len(g.stackargs), len(g.handoffs)))
rets = sorted({(f, a) for f, a, t in g.rets})
print("      (return values: rax still holds a base or element at %d ret sites - %s; no caller dereferences it, S4 finds no "
      "access outside the anchors)" % (len(rets), " ".join("%08X" % f for f, a in rets)))

# S5 - call arguments and string ops through the probe
tagged_calls, strops = [], []
for f in g.entry:
    blocks, succ, ind, end = S.cfg(f)
    for b in blocks.values():
        for x in b:
            pr = g.probe.get(x.address, {})
            rowt = lambda r: [t for t in pr.get(r, ()) if t not in ("H", "F")]
            if x.mnemonic in ("call", "jmp") and (x.mnemonic == "call" or (x.operands and x.operands[0].type == 2
                                                                           and not f <= x.operands[0].imm < end)):
                if any(rowt(r) for r in ("rcx", "rdx", "r8", "r9")):
                    tagged_calls.append((f, x.address))
            if re.match(r"^(rep\w* )?(stos|movs|lods|scas|cmps)[bwdq]$", x.mnemonic) and "xmm" not in x.op_str \
                    and (rowt("rdi") or rowt("rsi")):
                strops.append((f, x.address))
check("S5", not tagged_calls and not strops,
      "calls / tail jumps with a record pointer in rcx/rdx/r8/r9: %s; rep stos/movs on one: %s"
      % (["%08X@%08X" % x for x in tagged_calls] or "none", ["%08X@%08X" % x for x in strops] or "none"))

# S6 - extents
bad = []
for f in sorted(ANCH):
    ins = list(R.md.disasm(R.at(f, SZ[f]), f))
    last = ins[-1]
    nxt = f + SZ[f]
    tail = R.at(nxt, 1)
    if not (last.address + last.size == nxt and last.mnemonic in ("ret", "jmp")
            and (tail in (b"\xcc", b"\x90") or nxt in SZ)):
        bad.append("%08X" % f)
check("S6", not bad, "17 anchor extents end in ret/jmp before padding or the next function; bad %s" % (bad or "none"))

# S7 - byte coverage
touched, readb = set(), set()
for h in hits:
    for j in range(h[5]):
        touched.add(h[4] + j)
        if rw(h) != "w":
            readb.add(h[4] + j)
second = sorted(b for b in touched if b >= 0x20)
wonly = sorted(set(range(0x20)) - readb)
check("S7", not second and touched == set(range(0x20)) and wonly == [0x13, 0x16, 0x17],
      "bytes accessed %s; in +0x20..+0x3F: %s; never read in the first half: %s"
      % ("+0x00..+0x1F" if touched == set(range(0x20)) else sorted(touched), second or "none",
         ["+0x%02X" % b for b in wonly]))

# S8 - positive controls
have = {(h[1], h[4]) for h in hits}
ctrl = {(0x00386C5B, 0x00), (0x00386C5E, 0x08), (0x00386C62, 0x10), (0x00386C66, 0x18), (0x00387ADE, 0x10),
        (0x0038710E, 0x10), (0x00385FF7, 0x10), (0x003857DD, 0x12), (0x0038886B, 0x12), (0x0033CB60, 0x1C),
        (0x0033DA73, 0x1C)}
clr = [h for h in hits if h[0] == 0x00386C10]
check("S8", ctrl <= have and len(clr) == 4 and all(h[5] == 8 and rw(h) == "w" for h in clr),
      "controls found %d/%d; 00386C10 = %s" % (len(ctrl & have), len(ctrl),
                                              ", ".join("+0x%02X w%d" % (h[4], h[5]) for h in clr)))

# S9 - stability
key = lambda gg: sorted((h[0], h[1], h[4], h[5]) for h in gg.hits)
g5, g3n = flow(5), flow(3, False)
check("S9", key(g5) == key(g) and key(g3n) == key(g) and not g5.unk and not g5.esc and not g5.handoffs,
      "depth 5: %d accesses, depth 3 without returns: %d, same set: %s" % (len(g5.hits), len(g3n.hits),
                                                                         key(g5) == key(g) == key(g3n)))

# S10 - readings
rd = [
    txt(0x003857A3) == "movzx r15d, word ptr [rbx + 0x10]" and txt(0x003857B2) == "mov dword ptr [rbx + 0x10], eax"
    and txt(0x003857E1) == "mov word ptr [rbx + 0x10], r15w" and txt(0x003857E6) == "movzx r15d, word ptr [rsp + 0x30]",
    txt(0x003857AB) == "mov qword ptr [rbx], rax" and txt(0x003857AE) == "mov qword ptr [rbx + 8], rax"
    and txt(0x00385792) == "cmp rax, rsi",
    txt(0x003862FE) == "bt eax, ecx" and txt(0x00386303) == "mov byte ptr [rbx + 4], 0xa"
    and txt(0x00386342) == "bt eax, ecx" and txt(0x00386347) == "mov byte ptr [rbx + 4], 6",
    len(c["calls"].get(0x00387B00, ())) == 15 and txt(0x00387B95) == "shl eax, cl" and txt(0x00387B97) == "or dword ptr [rbx + 0xc], eax",
    txt(0x002FA355) == "bt ecx, eax" and txt(0x003228C2) == "jmp 0x2fa290" and txt(0x003B88B3) == "call 0x322850",
    txt(0x002F9419) == "call 0x320450" and txt(0x002F9474) == "movss xmm0, dword ptr [rsi + 0x18]"
    and txt(0x002F95A6) == "movss dword ptr [rsi + 0x18], xmm7" and txt(0x002F95AE) == "call 0x329a20",
    txt(0x003869A2) == "movzx eax, word ptr [rbx]" and txt(0x00386A27) == "inc word ptr [rbx]",
]
check("S10", all(rd), "readings %s (+0x10 restore; preview clear gated on the primary target; +0x08/+0x04 -> kinds "
      "0xA/6; +0x0C mark/test; +0x18 walking-MP carry; +0x14 tick)" % rd)

# the census
print("census (offset, width, r/w, function, site, instruction):")
for h in hits:
    print("  +0x%02X w%d %-2s %08X %08X  %s" % (h[4], h[5], rw(h), h[0], h[1], h[6]))
print("FAILS %d" % fails)
