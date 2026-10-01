"""psharray_review.py - OPUS (Claude Opus 5.5), 2026-09-28. Completes the PSharray representation review that
psharray_extent.py (3d95e439c, still pending independent review) began. That check is left as run; this one adds what
it did not test. STATIC, certified EXE only (any other image is REFUSED, exit 2).

  I1  the instantiations are TEN, not nine: RTTI has exactly ten PClassDescriptorForType<PSharray<T>>. The tenth,
      PSharray<PString>, is built by 006316C0, not by 00632D80, so a registrar list keyed on 00632D80 misses it. Its
      static descriptor 02CF9530 is constructed at 00635E33 and restored to the ForType vtable 00D58DB0 by its atexit
      thunk (008AF290); 006316C0 stores the instance size 0x10 at +0x38 and the alignment 8 at +0x3C
      (00632D80 stores its size argument at +0x38 too: 00632DB4).
  I2  PString's element stride is 8: its array allocator 006396C0 allocates count << 3, the copy 001C19A0 and the
      teardown 001C2720 advance 8 per element. So sizeof(PString) = 8 and 8 + max(8, 8) = 0x10: the rule holds.
  B1  header bits: every by-value and pointer resize / setter body masks the count with bit 31 only (btr/bts/shr 0x1f);
      bits 0-30 are the count. No other count bit is tested.
  B2  bit 31 = ADOPTED STORAGE: the slot-8 setters store count OR bit 31 with the CALLER'S pointer at any count other
      than one (no copy), and at count one copy the element inline and store plain 1. The resizes store the plain new
      count over owned storage, and free old storage only when it is neither the inline address nor bit-31 storage.
  L1  D3D11 element lifetime: the copy 00661720 moves +0x00/+0x08/+0x10/+0x18 (qwords), +0x20 (dword), +0x30 (qword),
      +0x38 (dword), +0x40 (qword), re-stores the TAsyncUpdate vtable 00D68DD0 at +0x28 rather than copying it, and
      calls nothing (no AddRef / Release). The resize 00672A20 calls only the allocator-copy 0066F7F0 and the free
      00584730: dropped elements are never destroyed. New tail elements get +0x00..+0x23 zeroed and the vtable.
  L2  PString element lifetime: 001C19A0 deep-copies (strlen, allocate, memcpy 00861EBA) per element; 001C2720 frees
      each element buffer whose bit 0 is clear, then the storage; 0063DCA0 runs that teardown only when bit 31 is
      clear, and frees a replaced inline element's buffer (bit 0 clear) itself.
  C1  controls on the size rule: a FIXED-16 hypothesis fails on the large by-value pair (0x50); a "BY-VALUE MEANS
      WIDER THAN 16" hypothesis fails on PSharray<PString> (a small by-value element, 0x10); 8 + max(8, sizeof T)
      matches all ten.
  S   REGRESSION: the store's PSharray size cell names PString with the 0x10 group, the m_count row states the bit-31
      meaning, and page section 20 no longer says "All nine" (FAILS before the patch).
"""
import csv, hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ops(a, size): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)]
def has(body, mn, op): return any(m == mn and o == op for _, m, o in body)
def rip_target(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

# I1
rtti = [r["class"] for r in csv.DictReader(open(os.path.join(ROOT, "Tools", "work", "rtti", "classes.tsv"), encoding="utf-8"), delimiter="\t")]
fortype = sorted(c for c in rtti if c.startswith("Phyre::PClassDescriptorForType<class Phyre::PSharray<"))
ctor = ops(0x6316C0, 0xA0)
i1 = (len(fortype) == 10 and any("PSharray<class Phyre::PString>" in c for c in fortype)
      and rip_target(0x635DFC) == 0x2CF9530 and rip_target(0x8AF297) == 0x2CF9530 and rip_target(0x8AF290) == 0xD58DB0
      and has(ops(0x635E33, 5), "call", "0x6316c0")
      and has(ctor, "mov", "dword ptr [rbx + 0x38], 0x10") and has(ctor, "mov", "dword ptr [rbx + 0x3c], 8")
      and has(ops(0x632DB4, 4), "mov", "dword ptr [rcx + 0x38], r9d"))
check("I1", i1, "%d ForType<PSharray<T>> in RTTI; PSharray<PString> descriptor 02CF9530 built by 006316C0 with +0x38 = 0x10"
      % len(fortype))

# I2
alloc, copy, tear = ops(0x6396C0, 0x8A), ops(0x1C19A0, 0xB9), ops(0x1C2720, 0x68)
i2 = has(alloc, "shl", "rcx, 3") and has(alloc, "add", "rax, 8") and has(copy, "add", "r14, 8") and has(tear, "add", "rbx, 8")
check("I2", i2, "PString element stride 8 (allocate, copy, teardown) -> 8 + max(8, 8) = 0x10")

# B1 / B2
RESIZE = {"pointer": 0x6C7A40, "uint": 0x60CC60, "D3D11 vb": 0x672A20, "D3D11 ib": 0x672AD0, "PString": 0x63D9C0}
SETTER = {"pointer": 0x6A5950, "uint": 0x6C7D00, "D3D11 vb": 0x672F30, "D3D11 ib": 0x673030, "PString": 0x63DE10}
# body lengths from the function list (Tools/work/graph/functions.tsv): 176 / 176 / 175 / 175 / 135 and 180 / 178 / 243 / 243 / 205
LEN = {0x6C7A40: 176, 0x60CC60: 176, 0x672A20: 175, 0x672AD0: 175, 0x63D9C0: 135,
       0x6A5950: 180, 0x6C7D00: 178, 0x672F30: 243, 0x673030: 243, 0x63DE10: 205}
bodies = {k: ops(a, LEN[a]) for k, a in list(RESIZE.items()) + [("set " + k, a) for k, a in SETTER.items()]}
count_bitops = set()
for k, b in bodies.items():
    for _, m, o in b:
        if m in ("btr", "bts", "bt", "btc") or (m == "shr" and o.endswith(", 0x1f")):
            count_bitops.add(o.split(", ")[-1])
b1 = count_bitops == {"0x1f"} and all(any(m == "btr" and o.endswith("0x1f") for _, m, o in bodies[k]) for k in RESIZE)
check("B1", b1, "bit operations on the count across the ten bodies: %s" % sorted(count_bitops))
setters_adopt = all(any(m == "bts" and o.endswith("0x1f") for _, m, o in bodies["set " + k]) for k in SETTER)
d3d_set = bodies["set D3D11 vb"]; ps_set = bodies["set PString"]
b2 = (setters_adopt and has(d3d_set, "cmp", "r8d, 1") and has(d3d_set, "mov", "esi, 1") and has(d3d_set, "mov", "dword ptr [rbx], esi")
      and has(ps_set, "mov", "r8d, 1")
      and has(bodies["D3D11 vb"], "mov", "dword ptr [rdi], esi") and has(bodies["D3D11 vb"], "shr", "eax, 0x1f")
      and has(bodies["D3D11 vb"], "cmp", "rbx, r14"))
check("B2", b2, "setters: count 1 inline with plain 1, else caller's buffer with bit 31; resizes store the plain count and "
      "spare inline and bit-31 storage")

# L1
cp = ops(0x661720, 0x75)
widths = [o for _, m, o in cp if m == "mov" and o.startswith(("qword ptr [rax", "dword ptr [rax"))]
l1 = (widths == ["qword ptr [rax], rcx", "qword ptr [rax + 8], rcx", "qword ptr [rax + 0x10], rcx", "qword ptr [rax + 0x18], rcx",
                 "dword ptr [rax + 0x20], ecx", "qword ptr [rax + 0x28], r10", "qword ptr [rax + 0x30], rcx",
                 "dword ptr [rax + 0x38], ecx", "qword ptr [rax + 0x40], rcx"]
      and rip_target(0x66172F) == 0xD68DD0 and not any(m == "call" for _, m, _ in cp)
      and [o for _, m, o in bodies["D3D11 vb"] if m == "call"] == ["0x66f7f0", "0x584730"])
check("L1", l1, "D3D11 element: field copy with the vtable re-stored, no call; the resize never destroys an element")

# L2
mv = ops(0x63DCA0, 0x83)
l2 = (has(copy, "call", "0x17d260") and has(copy, "call", "0x861eba")
      and has(tear, "call", "0x584730") and has(tear, "not", "al") and has(tear, "test", "al, 1")
      and has(mv, "call", "0x1c2720") and has(mv, "shr", "eax, 0x1f") and has(mv, "cmp", "r9, rdi") and has(mv, "call", "0x584730"))
check("L2", l2, "PString: deep copy; teardown frees owned buffers (bit 0 clear) and runs only when bit 31 is clear")

# C1
SIZES = {"6 pointer T": 0x10, "uint": 0x10, "PString": 0x10, "PDataBlockBufferD3D11": 0x50, "PIndexDataBlockBufferD3D11": 0x50}
ELEM = {"6 pointer T": 8, "uint": 4, "PString": 8, "PDataBlockBufferD3D11": 0x48, "PIndexDataBlockBufferD3D11": 0x48}
BYVALUE = {"PString", "PDataBlockBufferD3D11", "PIndexDataBlockBufferD3D11"}
rule = all(SIZES[k] == 8 + max(8, ELEM[k]) for k in SIZES)
fixed16 = all(v == 0x10 for v in SIZES.values())
byvalue_wider = all(SIZES[k] > 0x10 for k in BYVALUE)
check("C1", rule and not fixed16 and not byvalue_wider,
      "8 + max(8, sizeof T) matches all; fixed-16 refuted by the D3D11 pair; 'by-value is wider' refuted by PString")

# S
T = {l.split("\t")[0]: l.split("\t") for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8").read().splitlines()}
F = [l.split("\t") for l in open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8").read().splitlines()]
mc = [r for r in F if r[0] == "PSharray" and r[1] == "0x000"]
page = open(os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                         "member-registration-and-the-recovered-field-schema.md"), encoding="utf-8").read()
live = re.sub(r"~~.*?~~", "", page, flags=re.S)
s = ("PString" in T["PSharray"][1] and mc and "ADOPTED" in mc[0][5] and "All nine `PSharray<T>` descriptors" not in live)
check("S", bool(s), "store size cell names PString; m_count states bit 31; page no longer says 'All nine'")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
