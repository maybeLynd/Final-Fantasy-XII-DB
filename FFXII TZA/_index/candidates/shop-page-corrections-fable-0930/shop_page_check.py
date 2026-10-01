"""shop_page_check.py - re-reads, in the certified image, every byte fact apply_shop.py writes onto the shop page
(DATA-REQ-FABLE-SHOP-PAGE-GR13-15-0930; FABLE, 2026-09-30). Static only.

Instructions are decoded LINEARLY FROM THE START OF THE FUNCTION that holds them (retool's extents), so a cited
address that is not an instruction boundary fails. Band-table reference sites are found twice: from retool's
rip-reference index (every instruction kind, inside the extents) and from a raw .text byte scan for
`lea r64, [rip + disp32]` (independent of the extents).

Positive controls: P1 the transaction driver's known price read (0056D461 dword [.. + 0x10], 0056D468 btr 0x1f) must
decode; P2 the raw lea scanner must find the known bank lea 0033CB2C -> 0208D480 when pointed at that bank; P3 a
deliberately wrong expectation (0057DAD0's price store at cursor +0x10) must NOT match, so the matcher can fail.
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
    if f is None:
        return None
    return insns(f).get(a)


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)) if i else "<not an instruction boundary>"


def expect(tag, a, *parts):
    t = txt(a)
    check(tag, all(p in t for p in parts), "%08X  %s" % (a, t))


def rip_target(a):
    i = ins(a)
    for op in (i.operands if i else []):
        if op.type == 3 and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
    return None


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
expect("P1a driver price read", 0x0056D461, "dword ptr [", "+ 0x10]")
expect("P1b driver clears bit 31", 0x0056D468, "btr", "0x1f")
p2 = raw_lea_sites(0x0208D480, 0x0208D481)
check("P2 raw lea scanner finds the known bank lea 0033CB2C", 0x0033CB2C in [s for s, _ in p2], "%d sites on 0208D480" % len(p2))
t = txt(0x0057DB9F)
check("P3 a wrong expectation fails (price at cursor + 0x10)", "[rbx + 0x10]" not in t, "0057DB9F  %s" % t)

print("== statement 1: 0057DAD0 writes layout A, read from the entry")
expect("1a cursor = entry + 8", 0x0057DAFF, "lea rbx, [rcx + 8]")
expect("1b entry = cursor - 8", 0x0057DB55, "lea r14, [rbx - 8]")
expect("1c name pointer at entry +0", 0x0057DB98, "mov qword ptr [r14], rax")
expect("1d id at entry +8", 0x0057DB7E, "mov word ptr [rbx], ax")
expect("1e class byte at entry +0xA", 0x0057DB85, "mov byte ptr [rbx + 2], al")
expect("1f owned count / 0xFFFF at entry +0xC", 0x0057DB76, "mov word ptr [rbx + 4], ax")
expect("1g bit 3 selects the owned count", 0x0057DB67, "test bpl, 8")
expect("1h channel 1 at entry +0xE", 0x0057DBA2, "mov word ptr [rbx + 6], ax")
for a in (0x0057DB9F, 0x0057DBCC, 0x0057DBE0):
    expect("1i price at entry +0x10", a, "mov dword ptr [rbx + 8]")
expect("1j zero-price bts", 0x0057DBDC, "bts eax, 0x1f")
expect("1k sale test: mode bit 0", 0x0056E715, "test byte ptr [rdx], 1")
expect("1l sale test: +0x10 against bit 31", 0x0056E71A, "cmp dword ptr [rcx + 0x10], 0x80000000")
expect("1m sale test: score 8", 0x0056E721, "mov edx, 8")
expect("1n sale test: score 0 below bit 31", 0x0056E72B, "cmovb edx, eax")
expect("1o driver calls the sale test", 0x0056D576, "call 0x56e700")
expect("1p driver declines a non-zero score", 0x0056D57D, "jne")

print("== statement 2: message 26 on the shop widget and the driver")
b = IMG.read(0x005C5230, 3)
check("2a 005C5230 is xor eax, eax / ret", b == b"\x33\xC0\xC3", b.hex())
expect("2b shop widget procedure 0056E140 tail-jumps to the stub", 0x0056E3B3, "jmp 0x5c5230")
expect("2c driver 0056D370 calls the stub", 0x0056D3B8, "call 0x5c5230")
c = T.scan()
PROCS = (0x005636F0, 0x00563930, 0x00563B10, 0x00563D20)
cs = sorted(T.func_of(s, SZ) for _f, s in c["calls"].get(0x005651E0, ()))
check("2d 005651E0 is entered only from the four list procedures", cs == list(PROCS)
      and not c["refs"].get(0x005651E0) and not T.qword_sites(0x005651E0), " ".join("%08X" % x for x in cs))
lf = [sorted((T.func_of(s, SZ), k) for _f, s, k in c["refs"].get(p, ())) for p in PROCS]
check("2e each procedure is named only by one lea in 00564B90, never by a call or a data qword",
      all(x == [(0x00564B90, "lea")] for x in lf) and not any(c["calls"].get(p) for p in PROCS)
      and not any(T.qword_sites(p) for p in PROCS), repr([[("%08X" % f, k) for f, k in x] for x in lf]))

print("== statement 3: band-table reference sites")
LOW, HIGH = (0x00D23960, 0x00D23980), (0x00D23988, 0x00D2399C)
idx = sorted({(s, g) for g, v in c["refs"].items() if LOW[0] <= g < LOW[1] or HIGH[0] <= g < HIGH[1] for _f, s, _k in v})
raw = sorted(set(raw_lea_sites(*LOW) + raw_lea_sites(*HIGH)))
want = {0x00563E37: 0x00D23962, 0x00563F5B: 0x00D23962, 0x003FE2C5: 0x00D2398A,
        0x00565C25: 0x00D23960, 0x00565D06: 0x00D23960}
check("3a rip-reference index: exactly five sites", dict(idx) == want, ", ".join("%08X->%08X" % x for x in idx))
check("3b raw .text lea scan agrees", dict(raw) == want, ", ".join("%08X->%08X" % x for x in raw))
for a, callsite in ((0x00563E3E, 0x00563E42), (0x00563F62, 0x00563F7D), (0x003FE2CC, 0x003FE2D5)):
    expect("3c second word read", a, "movzx", "word ptr [rax + ")
    expect("3d into 00293110", callsite, "call 0x293110")
for a, tbl in ((0x0057D093, 0x00D23988), (0x0057D0C2, 0x00D23D00), (0x0057D0E9, 0x00D23960)):
    i = ins(a)
    ok = i is not None and i.mnemonic == "lea" and ("+ 0x%x]" % (tbl - 0x120000)) in i.op_str
    check("3e builder site is image-base-relative", ok, "%08X  %s" % (a, txt(a)))

print("== statement 4: the high band and head arm 4's default")
w = struct.unpack("<10H", IMG.read(0x00D23988, 20))
check("4a high band = five records {1,1} {2,3} {2,4} {2,4} {3,5}", w == (1, 1, 2, 3, 2, 4, 2, 4, 3, 5), repr(w))
expect("4b head switch bound", 0x0057CF91, "cmp ecx, 0x3c")
expect("4c default goes to head arm 4", 0x0057CF94, "ja 0x57d08b")
expect("4d head arm 4 band test", 0x0057D08B, "cmp esi, 0x40")

print("== statement 5: bit 5 for selector 0x0F only")
expect("5a or 0x20", 0x0057D3EA, "or ebx, 0x20")
expect("5b selector 0x0F", 0x0057D3ED, "cmp esi, 0xf")
expect("5c else the plain tag", 0x0057D3F0, "cmovne ebx, r14d")
expect("5d class 7", 0x0057D3FF, "mov r9d, 7")
expect("5e filler 0057DAD0", 0x0057D411, "call 0x57dad0")

print("== statement 6: the driver is the shop widget's +0xC0")
expect("6a shop widget procedure 0056E140", 0x0056DD66, "lea r9, [rip + ")
check("6a' target", rip_target(0x0056DD66) == 0x0056E140, "%08X" % (rip_target(0x0056DD66) or 0))
expect("6b shop widget created", 0x0056DD79, "call 0x564ac0")
expect("6c rdi = the shop widget", 0x0056DD88, "mov rdi, rax")
expect("6d rcx = rdi", 0x0056DE62, "mov rcx, rdi")
expect("6e into 0056C950", 0x0056DE78, "call 0x56c950")
expect("6f rbx = the argument", 0x0056C969, "mov rbx, rcx")
check("6g procedure 0056D370", rip_target(0x0056C9BC) == 0x0056D370, "0056C9BC  %s" % txt(0x0056C9BC))
expect("6h create", 0x0056C9C3, "call 0x244f50")
expect("6i stored at +0xC0", 0x0056C9CB, "mov qword ptr [rbx + 0xc0], rax")

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
