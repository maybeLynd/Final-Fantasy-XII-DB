"""DD residue batch 6 (SWE2-CONTRACT, 2026-09-30): static checks behind the typed-list page's reconciled residue.

Page: 02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md
Image: the certified shipping EXE (sha256 printed and asserted). Every check is an instruction pin or a byte decode; each
negative carries a positive control. Run: python -B b6_typed_list.py  (exit 0 and FAILS 0 expected)

  K1-K3  kind-7 ids 111 / 127 through SWE2-DATA's kind7.py path-array reader (control: 0xBF = Loca.mrp, the cl2 page's id)
  B1-B6  slot flag bit 7 (0x80 at slot +0x38) gates the texture-memory layout pass 0024A710(k)
  B7     every immediate or/and 0x80 at [rax+0x38] in 0027F5D0..002D7600 follows, within 6 instructions, a 0024A5A0 (find slot by name)
  B8     0024A5A0 returns 0 on a miss (unlike 0024A610, which returns index 0)
  E1-E3  the sprite emitter 002D9380 takes the node's atlas slot and reads the descriptor 0024A710 wrote (+0x30) and +0x38
  S1-S4  the 8-byte sub-image record: one array serves types 2/9 and 7; its fields as type 7 unpacks them; byte 7 default
  R1     002A0060's callers are the two constructors and 001D7150; no list drawer calls 002A0060 or 0024A610 (a built node
         keeps the atlas slot it was given; control: the constructors' own calls are found)
  C1     002432B0 is called from 113 direct sites in 108 functions (the page's section 9 count; section 5e says 110 callers)
  L1     the page's live example bytes decode to the S3 field layout (arithmetic only; the bytes are the 2026-09-08 live read)
"""
import hashlib, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "_index", "candidates", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
from kind7 import paths  # noqa: E402

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    return next(T.R.md.disasm(T.R.at(a, 16), a, 1))


def pin(name, a, text):
    i = ins(a)
    got = "%s %s" % (i.mnemonic, i.op_str)
    check(name, text in got, "%08X  %s" % (a, got))


def body(f):
    n = T.sizes().get(f) or T.R.ext.get(f)
    return list(T.R.md.disasm(T.R.at(f, n), f))


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")

# ---- K: the two resources the load menu requests (the page's section 5d open item)
arr, P = paths(7, 0x4D2, stop_on_miss=False)
check("K1 kind 7 id 111 (0x6F)", (P.get(0x6F) or "").endswith("Mrp_Menu\\save_load.mrp"), P.get(0x6F))
check("K2 kind 7 id 127 (0x7F)", (P.get(0x7F) or "").endswith("Tm2_Menu\\DataFace_c.tm2"), P.get(0x7F))
check("K3 control kind 7 id 0xBF = Loca.mrp (cl2 page)", (P.get(0xBF) or "").endswith("Mrp_Menu\\Loca.mrp"), P.get(0xBF))

# ---- B: bit 7 of the atlas slot flags
pin("B1 mask base: bits 5,6,7", 0x0024A733, "mov ebx, 0xe0")
pin("B1 mask adds the caller's bit k", 0x0024A73B, "bts ebx, ecx")
i = ins(0x0024A762)
check("B2 walk starts at slot 0 +0x38 (0208F5B8)", i.mnemonic == "lea" and i.address + i.size + i.operands[1].mem.disp == 0x0208F5B8,
      "%08X %s %s" % (i.address, i.mnemonic, i.op_str))
pin("B2 63 iterations", 0x0024A778, "mov r12d, 0x3f")
pin("B2 stride 0x48", 0x0024A9B1, "add r14, 0x48")
pin("B2 loop count down", 0x0024A9B5, "sub r12d, 1")
pin("B3 flags & mask", 0x0024A793, "and rcx, rax")
pin("B3 == mask", 0x0024A796, "cmp rcx, rax")
pin("B3 else skip the slot", 0x0024A799, "jne 0x24a9b1")
pin("B4 image header read (H = slot +0x20)", 0x0024A7A8, "mov rdi, qword ptr [r14 - 0x18]")
pin("B4 width u16 H+0x14", 0x0024A7BF, "movzx r15d, word ptr [rdi + 0x14]")
pin("B4 height u16 H+0x16", 0x0024A7CA, "movzx ebx, word ptr [rdi + 0x16]")
pin("B4 transfer builder", 0x0024A84A, "call 0x24af50")
pin("B4 base starts at 0x3520", 0x0024A728, "mov dword ptr [rsp + 0xc8], 0x3520")
pin("B5 packed descriptor stored at slot +0x30", 0x0024A99C, "mov qword ptr [r14 - 8], rcx")
# callers and their k
calls = T.scan()["calls"].get(0x0024A710, set())
ks = {}
for f, site in sorted(calls):
    back = [x for x in body(f) if x.address < site][-6:]
    k = None
    for x in back:
        if x.op_str.startswith("ecx, ") and x.mnemonic == "mov":
            k = x.op_str.split(", ")[1]
        if x.mnemonic == "xor" and x.op_str == "ecx, ecx":
            k = "0"
    ks["%08X" % site] = k
check("B6 0024A710 has 8 direct call sites", len(calls) == 8, str(sorted("%08X" % s for _, s in calls)))
check("B6 every site passes k in {0,1,2}", all(v in ("0", "1", "2") for v in ks.values()), str(ks))

# B7: the or/and 0x80 writers act on a slot found by name
lo, hi = 0x0027F5D0, 0x002D7600
w = []
for f, n in sorted(T.sizes().items()):
    if not lo <= f < hi:
        continue
    seq = list(T.R.md.disasm(T.R.at(f, n), f))
    for j, x in enumerate(seq):
        if x.op_str in ("dword ptr [rax + 0x38], 0x80", "dword ptr [rax + 0x38], 0xffffff7f") and x.mnemonic in ("or", "and"):
            prev = [y for y in seq[max(0, j - 6):j] if y.mnemonic == "call"]  # 00280895 has a null test between
            w.append((x.address, x.mnemonic, prev[-1].op_str if prev else None))
check("B7 writers found (control: the request router's 0027F7DA)", any(a == 0x0027F7DA for a, _, _ in w), "%d sites" % len(w))
check("B7 each writer follows a 0024A5A0 call", all(c == "0x24a5a0" for _, _, c in w),
      str([("%08X" % a, m, c) for a, m, c in w if c != "0x24a5a0"]))
pin("B8 0024A5A0 skips free slots (bit 5)", 0x0024A5B0, "test byte ptr [r9 + 0x38], 0x20")
pin("B8 miss returns 0 (a null slot)", 0x0024A5E4, "xor eax, eax")
pin("B8 hit returns the slot pointer", 0x0024A5E7, "mov rax, r9")

# ---- E: the emitter reads what the layout pass wrote
pin("E1 type-2 drawer passes node +0x18 (the atlas slot) in r8", 0x002437B9, "mov r8, qword ptr [rdi + 0x18]")
pin("E1 into 002D9380", 0x002437C2, "call 0x2d9380")
pin("E2 emitter keeps r8 in rsi", 0x002D93CF, "mov rsi, r8")
pin("E3 emitter reads slot +0x30 (descriptor)", 0x002D944A, "mov rax, qword ptr [rsi + 0x30]")
pin("E3 emitter reads slot +0x38 format bits", 0x002D946D, "mov ecx, dword ptr [rsi + 0x38]")
pin("E3 emitter reads slot +0x30 again (format 0x14 arm)", 0x002D948D, "mov rax, qword ptr [rsi + 0x30]")

# ---- S: the sub-image record
pin("S1 types 2/9: T = atlas[+0x20] + 0x30", 0x0029F4F1, "add r8, 0x30")
pin("S1 types 2/9: records at T + u16[T+0x10]", 0x0029F500, "movzx eax, word ptr [r8 + 0x10]")
pin("S1 types 2/9: + entry*8 -> node +0x20", 0x0029F50F, "lea r8, [rcx + rdx*8]")
pin("S2 type 7: T = atlas[+0x20] + 0x30", 0x0029F176, "add r9, 0x30")
pin("S2 type 7: records at T + u16[T+0x10]", 0x0029F18D, "movzx eax, word ptr [r9 + 0x10]")
pin("S2 type 7: + entry*8", 0x0029F1B1, "lea r9, [rcx + rdx*8]")
pin("S3 u16 +0 -> +0x4C", 0x0029F206, "movzx eax, word ptr [r9 + rcx*8]")
pin("S3 u16 +2 -> +0x4E", 0x0029F20F, "movzx eax, word ptr [r9 + rcx*8 + 2]")
pin("S3 u16 +4 ...", 0x0029F219, "movzx eax, word ptr [r9 + rcx*8 + 4]")
pin("S3 ... & 0xFFF -> +0x50", 0x0029F21F, "and ax, r14w")
pin("S3 dword +4 ...", 0x0029F227, "mov eax, dword ptr [r9 + rcx*8 + 4]")
pin("S3 ... >> 12 (& 0xFFF) -> +0x52", 0x0029F22C, "shr eax, 0xc")
pin("S3 r14w = 0xFFF", 0x0029F1EE, "mov r14d, 0xfff")
pin("S4 byte 7 default opacity, types 2/9", 0x0029F531, "movzx ecx, byte ptr [r8 + rax*8 + 7]")
pin("S4 byte 7 default opacity, type 7", 0x0029F1E0, "movzx ecx, byte ptr [r9 + rax*8 + 7]")

# ---- R: who resolves an atlas name
C = T.scan()["calls"]
res = sorted({f for f, _ in C.get(0x002A0060, set())})
check("R1 002A0060 callers", res == [0x001D7150, 0x0029F130, 0x0029F4C0], str(["%08X" % f for f in res]))
drawers = (0x002435C0, 0x00243C00, 0x00243860, 0x0029ED50, 0x0029F5D0, 0x0029FBD0, 0x002A0180)
bad = [("%08X" % f, "%08X" % s_) for t in (0x002A0060, 0x0024A610) for f, s_ in C.get(t, set()) if f in drawers]
check("R1 no drawer re-resolves", not bad, str(bad))
check("R1 control: 0029F130 calls 0024A610", any(f == 0x0029F130 for f, _ in C.get(0x0024A610, set())))

# ---- C: the decoder's caller count
c = C.get(0x002432B0, set())
check("C1 002432B0 direct call sites / functions", (len(c), len({f for f, _ in c})) == (113, 108),
      "%d sites, %d functions" % (len(c), len({f for f, _ in c})))

# ---- L: the page's live example, decoded with S3's layout
b = bytes.fromhex("7A0064001CC0010B")
x, y = struct.unpack_from("<HH", b, 0)
v = struct.unpack_from("<I", b, 4)[0]
fields = (x, y, v & 0xFFF, (v >> 12) & 0xFFF, b[7])
check("L1 buttonicon code 0 record decodes", fields == (122, 100, 28, 28, 11), str(fields))

print("FAILS", FAILS)
sys.exit(1 if FAILS else 0)
