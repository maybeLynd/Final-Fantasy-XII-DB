"""gr8_page_check.py - re-reads, in the certified image, every byte fact apply_gr8.py writes onto the formula scratch
block (section 2.5 and the section 4 layout block) and the battle-unit field map (rows 0033D890 / 0033CB10)
(DATA-REQ-FABLE-GR8-PAGE-CORRECTIONS-0930; FABLE, 2026-09-30). Static only.

Instructions are decoded linearly from the start of the function that holds them (retool's extents), so an address
that is not an instruction boundary fails. Where a site's base register must be the per-unit record, the function's
bank lea (0208D480 / 0208DE80, or the +0x14 anchors 0208D494 / 0208DE94) is checked too; the full base tracking is
OPUS's structflow census (gr8_record_census_check.py), not repeated here.

Positive controls: P1 the preview's known restore 003857E1 must decode as a word store of r15w to [rbx + 0x10]; P2 the
bank lea count - a raw .text scan for `lea r64, [rip + disp32]` into 0208D480..0208E67F must give OPUS's 34 (16 + 16 +
2); P3 a deliberately wrong expectation (the solver tests value 2 at 0033D953) must NOT match.
Prints PASS/FAIL per step and FAILS n last."""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import disasm_fn as D  # noqa: E402

R, SZ = T.R, T.sizes()
IMG = D.Image(D.DEFAULT_EXE)
fails = 0
_cache = {}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def insns(f):
    if f not in _cache:
        _cache[f] = {i.address: i for i in R.md.disasm(R.at(f, SZ[f]), f)}
    return _cache[f]


def ins(a):
    f = T.func_of(a, SZ)
    return insns(f).get(a) if f is not None else None


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)) if i else "<not an instruction boundary>"


def expect(tag, a, *parts):
    t = txt(a)
    check(tag, all(p in t for p in parts), "%08X  %s" % (a, t))


def bank_leas(f):
    out = set()
    for i in insns(f).values():
        if i.mnemonic == "lea":
            for op in i.operands:
                if op.type == 3 and op.mem.base == T.RIP:
                    out.add(i.address + i.size + op.mem.disp)
    return out & {0x0208D480, 0x0208DE80, 0x0208D494, 0x0208DE94}


def raw_lea_sites(lo, hi):
    out = []
    for name, sva, vs, ra, rs in IMG.secs:
        if name != ".text":
            continue
        d = IMG.d[ra:ra + rs]
        base = IMG.base + sva
        for k in range(len(d) - 7):
            if d[k] in (0x48, 0x4C) and d[k + 1] == 0x8D and (d[k + 2] & 0xC7) == 0x05:
                g = base + k + 7 + struct.unpack_from("<i", d, k + 3)[0]
                if lo <= g < hi:
                    out.append((base + k, g))
    return out


print("== controls")
expect("P1 the preview restores the saved word", 0x003857E1, "mov word ptr [rbx + 0x10], r15w")
sites = raw_lea_sites(0x0208D480, 0x0208E680)
by = {}
for _s, g in sites:
    by[g] = by.get(g, 0) + 1
check("P2 raw bank lea count = 34", len(sites) == 34, " ".join("%08X x%d" % kv for kv in sorted(by.items())))
t = txt(0x0033D953)
check("P3 a wrong expectation fails (value 2 at 0033D953)", not t.endswith(", 2"), "0033D953  %s" % t)

print("== scratch block 2.5: +0x10 is not the previewed id")
expect("S1 save the word", 0x003857A3, "movzx r15d, word ptr [rbx + 0x10]")
expect("S2 clear +0x00..+0x07 (qword)", 0x003857AB, "mov qword ptr [rbx], rax")
expect("S3 clear +0x08..+0x0F (qword)", 0x003857AE, "mov qword ptr [rbx + 8], rax")
expect("S4 clear +0x10..+0x13 (dword)", 0x003857B2, "mov dword ptr [rbx + 0x10], eax")
expect("S5 write the saved word back", 0x003857E1, "word ptr [rbx + 0x10], r15w")
expect("S6 the previewed id goes to 02AEDFD4", 0x003857EC, "mov dword ptr [rip + ")
i = ins(0x003857EC)
check("S6' target", i is not None and i.address + i.size + i.operands[0].mem.disp == 0x02AEDFD4, "")
expect("S7 the 0x9F draw stores an id", 0x00387ADE, "mov word ptr [rbx + 0x10], ax")
check("S8 00385680 forms the record from the banks", bank_leas(0x00385680) >= {0x0208D480, 0x0208DE80},
      " ".join("%08X" % x for x in sorted(bank_leas(0x00385680))))

print("== scratch block 2.5: the reader column")
for f, a in ((0x00388D50, 0x00388E60), (0x0038DA00, 0x0038DA68), (0x0038EBE0, 0x0038ED17), (0x0038ED40, 0x0038EDD6)):
    expect("R1 +0x00 dword read", a, "mov eax, dword ptr [r")
    check("R1' in %08X, which leas a bank" % f, T.func_of(a, SZ) == f and bool(bank_leas(f)), "")
for a in (0x00388E51, 0x0038DA5D, 0x0038ECD5, 0x0038ECFF):
    expect("R2 +0x00 dword write (not u64)", a, "mov dword ptr [r")
expect("R3 +0x04 load", 0x0038633F, "mov eax, dword ptr [rdi + 4]")
expect("R3 bt", 0x00386342, "bt eax, ecx")
expect("R3 kind 6", 0x00386347, "mov byte ptr [rbx + 4], 6")
expect("R4 +0x08 load", 0x003862FB, "mov eax, dword ptr [rdi + 8]")
expect("R4 bt", 0x003862FE, "bt eax, ecx")
expect("R4 kind 0xA", 0x00386303, "mov byte ptr [rbx + 4], 0xa")
check("R5 00385F60 forms the record from the banks", bool(bank_leas(0x00385F60)), "")

print("== scratch block 2.5: the missing rows")
expect("M1 +0x0C mark", 0x00387B97, "or dword ptr [rbx + 0xc], eax")
c = T.scan()
n = len(c["calls"].get(0x00387B00, ()))
check("M1' 00387B00 has 15 direct call sites", n == 15, str(n))
expect("M2 +0x0C reader", 0x002FA352, "mov ecx, dword ptr [rbx + 0xc]")
expect("M2 bt", 0x002FA355, "bt ecx, eax")
expect("M3 +0x0C cleared at activation", 0x00386C5E, "mov qword ptr [rax + 8], rcx")
check("M4 00386860 uses the +0x14 anchors", bank_leas(0x00386860) >= {0x0208D494, 0x0208DE94},
      " ".join("%08X" % x for x in sorted(bank_leas(0x00386860))))
for a, p in ((0x003869E0, "mov word ptr [rbx], cx"), (0x00386A27, "inc word ptr [rbx]"),
             (0x00386A2C, "mov word ptr [rbx], r15w"), (0x003869A2, "movzx eax, word ptr [rbx]")):
    expect("M5 +0x14 tick counter", a, p)
check("M6 002F9400 forms the record from the banks", bank_leas(0x002F9400) >= {0x0208D480, 0x0208DE80}, "")
expect("M6 +0x18 write", 0x002F95A6, "movss dword ptr [rsi + 0x18], xmm7")
expect("M6 +0x18 read", 0x002F9474, "movss xmm0, dword ptr [rsi + 0x18]")
for a in (0x00386C5B, 0x00386C5E, 0x00386C62, 0x00386C66):
    expect("M7 activation clear", a, "mov qword ptr [rax")
expect("M7' last clear covers +0x18..+0x1F", 0x00386C66, "[rax + 0x18], rcx")

print("== field map: +0x1C bit 0 and bit 1")
check("F1 0033CB10 forms the record from the banks by +4 / +0xEA9", bank_leas(0x0033CB10) >= {0x0208D480, 0x0208DE80}, "")
expect("F1 slot byte", 0x0033CB46, "movzx eax, byte ptr [rax + 0xea9]")
expect("F2 0033CB10 sets value 1 = bit 0", 0x0033CB60, "or dword ptr [rax + 0x1c], 1")
check("F3 0033D890 forms the record the same way", bank_leas(0x0033D890) >= {0x0208D480, 0x0208DE80}, "")
expect("F3 slot byte", 0x0033D935, "movzx ebx, byte ptr [rax + 0xea9]")
expect("F4 the solver tests value 1", 0x0033D953, "test byte ptr [rbx + 0x1c], 1")
expect("F5 its own latch, value 2", 0x0033DA73, "or dword ptr [rbx + 0x1c], 2")
expect("F6 tested at", 0x0033DA77, "test byte ptr [rbx + 0x1c], 2")

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
