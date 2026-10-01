"""DD residue batch 8 (SWE2-CONTRACT, 2026-09-30): checks behind how-a-path-is-resolved-to-bytes.md's reconciled residue.

Run: python -B b8_path_resolve.py   (FAILS 0)

  S1  the resolver 0059EE90 forces the selector to 5 when the cache is enabled (001D6B20) and 00865390(path) is true
      (0059EEE3..0059EEF1)
  S2  00865390 -> 001DB050: true when the path begins with PS2Data\\obj_finish\\in\\chara\\c10\\<name>\\ for one of the four
      names c1004, c1005, c1006, c1019 (6-byte stride, bound 0x18); strncpy through 008C2F70 and a byte compare
  S3  the log rule (selectors 3..5 silent; 0 -> [FFXII_data]; else [FFXII_data_notcache]) and route 1's selector gate
      (selector 0 never tries route 1: 0059EF38)
  S4  the cache fill after a route-2 hit (0059F1B7 -> 0059A9B0) runs only when r12b is set, and r12b is set only on the
      route-1 attempt path: 001D6B90() == 0 or selector 5 -> (001D6B70() > 0) or selector != 1; otherwise 0
  S5  route 1 receives the selector (0059EFD2 movsx edx -> 001D6D20 -> r8d of 0020C1B0)
  U1  the UTF-16 copy has no consumer: 00599250 (UTF-8 -> UTF-16, surrogate range test) writes into the alloca buffer
      [rsp+0x20] passed in rdx; its return value is overwritten at 0059F0EF; after the call the only instructions that
      form an address from rsp are the next alloca (0059F104), the new buffer (0059F107) and the epilogue
  A1  route 1's lookup anchors in 0020C1B0: lock +0x58 taken (0020C230 / 0020C23C), root +0x38 (0020C242), sentinel
      +0x28 (0020C246), node key u32 +0x20 (0020C255), lock released (0020C2B3 / 0020C2C1)
  S6  001D6B90 returns the low-memory byte 01F83441 (set by 0020C610 below 1 GiB of physical memory or at the 32 MB
      budget floor); 001D6B70 returns the FileCache singleton [01F82CF0]'s +0x88 byte
  B1  the far-end bodies: 0059EE90's callers include the Audio body 00225BA0; the Input body 0079FB10 calls 00597970,
      0059D920 and 00598100
"""
import hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


def body(f):
    return list(T.R.md.disasm(T.R.at(f, T.sizes()[f]), f))


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
sc = T.scan()

# S1
pin("S1 cache enabled?", 0x0059EEDC, "call 0x1d6b20")
pin("S1 path predicate", 0x0059EEE8, "call 0x865390")
pin("S1 selector forced to 5", 0x0059EEF1, "mov byte ptr [r15 + 0x18], 5")
pin("S1 001D6B20 asks 0020C710", 0x001D6B24, "call 0x20c710")
# S2
pin("S2 00865390 gets 001DB210's object", 0x00865399, "call 0x1db210")
pin("S2 then tail-calls 001DB050", 0x008653A9, "jmp 0x1db050")
names = [T.cstr(0x01DFCFE8 + 6 * k, 8) for k in range(4)]
check("S2 the four names", names == ["c1004", "c1005", "c1006", "c1019"], str(names))
check("S2 the folder prefix", T.cstr(0x01DFD010) == "PS2Data\\obj_finish\\in\\chara\\c10\\", repr(T.cstr(0x01DFD010)))
check("S2 the separator word", T.R.at(0x008FB2B0, 2) == b"\\\x00")
pin("S2 stride 6", 0x001DB19B, "add rdi, 6")
pin("S2 bound 0x18 (four names)", 0x001DB19F, "cmp rbp, 0x18")
pin("S2 prefix copy is strncpy (IAT 008C2F70)", 0x001DB161, "call qword ptr [rip + 0x6e7e09]")
pin("S2 match returns 1", 0x001DB1D3, "mov eax, 1")
# S3
pin("S3 selector - 3", 0x0059EEFB, "lea eax, [rcx - 3]")
pin("S3 <= 2 skips the log", 0x0059EEFE, "cmp al, 2")
pin("S3 notcache tag", 0x0059EF02, "lea rdx, [rip + 0x788a07]")
pin("S3 selector 0 takes the plain tag", 0x0059EF10, "lea rdx, [rip + 0x788a19]")
check("S3 tags", (T.cstr(0x00D27910), T.cstr(0x00D27930)) == ("[FFXII_data_notcache] %s \n", "[FFXII_data] %s \n"))
pin("S3 selector 0 never tries route 1", 0x0059EF38, "cmp byte ptr [r15 + 0x18], sil")
pin("S3 (sil is zero)", 0x0059EED4, "xor esi, esi")
# S4
pin("S4 r12b starts 0", 0x0059EED6, "xor r12b, r12b")
pin("S4 001D6B90", 0x0059EFAB, "call 0x1d6b90")
pin("S4 selector 5 test", 0x0059EFB4, "cmp byte ptr [r15 + 0x18], 5")
pin("S4 001D6B70", 0x0059EFBB, "call 0x1d6b70")
pin("S4 flag -> fill", 0x0059EFC4, "mov r12b, 1")
pin("S4 else fill unless selector 1", 0x0059EFC9, "cmp byte ptr [r15 + 0x18], 1")
pin("S4 setne", 0x0059EFCE, "setne r12b")
pin("S4 fill gate", 0x0059F1AB, "test r12b, r12b")
pin("S4 cache fill", 0x0059F1B7, "call 0x59a9b0")
w12 = [i.address for i in body(0x0059EE90) if re.match(r"(mov|xor|setne)$", i.mnemonic) and i.op_str.startswith("r12b")]
check("S4 r12b writers are exactly the three", w12 == [0x0059EED6, 0x0059EFC4, 0x0059EFCE], " ".join("%08X" % a for a in w12))
# S6: what the two helpers read
pin("S6 001D6B90 asks 0020C720", 0x001D6B94, "call 0x20c720")
pin("S6 0020C720 reads the low-memory byte 01F83441", 0x0020C720, "movzx eax, byte ptr [rip + 0x1d76d1a]")
pin("S6 setter: total physical memory under 1 GiB", 0x0020C674, "cmp rcx, 0x40000000")
pin("S6 setter: clear", 0x0020C67D, "mov byte ptr [rip + 0x1d76dbd], 0")
pin("S6 setter: budget at its 32 MB floor", 0x0020C684, "cmp rax, 0x2000000")
pin("S6 setter: set", 0x0020C68C, "mov byte ptr [rip + 0x1d76dae], 1")
pin("S6 001D6B70 takes the FileCache singleton", 0x001D6B74, "call 0x1dada0")
pin("S6 001DADA0 reads 01F82CF0", 0x001DADA0, "mov rax, qword ptr [rip + 0x1da7f49]")
pin("S6 and tests its +0x88 byte", 0x001D6B7B, "cmp byte ptr [rax + 0x88], cl")
w441 = sorted(a for g in sc["refs"] if g == 0x01F83441 for f, a, k in sc["refs"][g] if k == "W")
check("S6 the low-memory byte's only writers are in 0020C610", w441 == [0x0020C67D, 0x0020C68C], " ".join("%08X" % a for a in w441))
# S5
pin("S5 selector into route 1", 0x0059EFD2, "movsx edx, byte ptr [r15 + 0x18]")
pin("S5 route 1 entry", 0x0059EFE5, "call 0x1d6d20")
pin("S5 forwarded as r8d", 0x001D6D4F, "mov r8d, esi")
pin("S5 to the lookup", 0x001D6D55, "call 0x20c1b0")
# U1
pin("U1 buffer passed in rdx", 0x0059F0DD, "lea rdx, [rsp + 0x20]")
pin("U1 the widening call", 0x0059F0EA, "call 0x599250")
pin("U1 return value overwritten", 0x0059F0EF, "lea rax, [r14 + 0xf]")
after = [i for i in body(0x0059EE90) if i.address > 0x0059F0EA and "rsp" in i.op_str]
check("U1 rsp-based addressing after the call", [(i.address, i.mnemonic) for i in after] ==
      [(0x0059F104, "sub"), (0x0059F107, "lea"), (0x0059F1EE, "lea")],
      " ".join("%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in after))
pin("U1 converter: surrogate range", 0x005992E2, "lea ecx, [rax - 0xd800]")
# A1
for a, t in ((0x0020C230, "lea rsi, [rdi + 0x58]"), (0x0020C23C, "call 0x5cd4f0"), (0x0020C242, "mov rcx, qword ptr [rdi + 0x38]"),
             (0x0020C246, "lea r8, [rdi + 0x28]"), (0x0020C255, "cmp dword ptr [rcx + 0x20], edx"),
             (0x0020C2B3, "call 0x5cd820"), (0x0020C2C1, "call 0x5cd820")):
    pin("A1 %08X" % a, a, t)
# B1
c = sorted({f for f, _ in sc["calls"].get(0x0059EE90, ())})
check("B1 0059EE90 callers include the Audio body 00225BA0", 0x00225BA0 in c and len(c) == 6, " ".join("%08X" % x for x in c))
for t in (0x00597970, 0x0059D920, 0x00598100):
    check("B1 0079FB10 calls %08X" % t, 0x0079FB10 in {f for f, _ in sc["calls"].get(t, ())})

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
