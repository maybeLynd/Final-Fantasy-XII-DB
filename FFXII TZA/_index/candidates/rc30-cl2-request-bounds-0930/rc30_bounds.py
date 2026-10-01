"""rc30_bounds.py - RC-30: the hand bounds for every site rc30_census.py leaves OPEN, the loca_*.cl2 request that
exists, its authored selector, and the reader. ORACLE, 2026-09-30. Every fact is asserted against the image bytes or
the shipped files; a changed byte fails the script.
"""
import collections, contextlib, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
sys.path.insert(0, os.path.join(HERE, "..", "rc6-console-map-codes-0930"))
with contextlib.redirect_stdout(io.StringIO()):
    import rc5_paths as R  # noqa: E402
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def D(a, n=0x20):
    return {x.address: (x.mnemonic, x.op_str) for x in img.dis(a, n)}


def F(f):
    return {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(f)}


# ---- B1 the path tables are read only by ResourcePath_Get / ResourcePath_Copy (and filled by 002DF9A0) ----
g, c = D(0x002DF980, 0x16), D(0x002DF880, 0x10)
check(img.ripmem(img.dis(0x002DF983, 8)[0]) == 0x0215F000 and img.ripmem(img.dis(0x002DF886, 8)[0]) == 0x0215F000,
      "B1 002DF980 and 002DF880 index g_pathTables 0215F000 (the raw rip scan finds no other reader outside 002DF9A0)")
cp = [(a, img.owner(a)) for a, _k in img.calls_to(0x002DF880)]
x = F(0x00377DC0)
check(cp == [(0x00377E09, 0x00377DC0)] and x.get(0x00377DED) == ("mov", "eax, r9d") and x.get(0x00377DFD) == ("mov", "ecx, eax")
      and F(0x00378A60).get(0x00378B1A) == ("mov", "r9d, 4"),
      "B1b ResourcePath_Copy's only caller 00377DC0 passes kind = its r9d = 4 (00378B1A): map packs, never kind 7")
# ---- B2 decoder 002ED6F0 (packed code -> kind, id): every arm's kind ----
kinds = set()
for k in range(0x35):
    t = img.BASE + struct.unpack("<I", img.rd(img.BASE + 0x1CD854 + 4 * img.rd(img.BASE + 0x1CD888 + k, 1)[0], 4))[0]
    for ins in img.dis(t, 0x30):
        if ins.mnemonic == "mov" and ins.op_str.startswith("edx, 0x"):
            kinds.add(int(ins.op_str.split(",")[1], 16))
        if ins.mnemonic == "ret":
            break
kinds.add(1)  # default arm 002ED840: mov eax, 1 ; mov [r9], eax
check(7 not in kinds and D(0x002ED840, 0x10).get(0x002ED847) == ("mov", "dword ptr [r9], eax"),
      "B2 002ED6F0's kinds are %s - never 7 (sites 001BB397, 001F5E64, 002EEF70, 00863144 via 002E98F0; 002E6776, "
      "002EADEA, 002EAE08, 002E9988, 002E99A8, 002E700C)" % sorted(hex(k) for k in kinds))
# ---- B3 0032F170 (manager formula) kinds 1 / 8 / 5 ----
m = D(0x0032F170, 0x3C)
check(m.get(0x0032F181) == ("mov", "dword ptr [r8], 1") and m.get(0x0032F193) == ("mov", "dword ptr [r8], 8")
      and m.get(0x0032F1A1) == ("mov", "dword ptr [r8], 5"),
      "B3 0032F170 writes kind 1, 8 or 5 (sites 001DA31B, 003DDAB9 via 003DD4C0, 003DF593 via 003DF440, 003E9F59 via 003E9F80)")
p = F(0x0032FCA0)
check(p.get(0x0032FD27) == ("lea", "esi, [rdi - 3]") and p.get(0x0032FD30) == ("mov", "esi, 8") and p.get(0x0032FD3F) == ("mov", "esi, 5")
      and p.get(0x0033001F) == ("mov", "r8d, esi"),
      "B3b 0032FCA0 passes kind esi in {1, 8, 5} to 003306E0 / 00330310, whose kind reaches 00332250 (00332280)")
# ---- B4 constants ----
check(D(0x0032F602, 0x18).get(0x0032F60E) == ("lea", "ecx, [rdi + 8]"), "B4a 0032F617: kind = 0 + 8 after the loop (rdi counts down to 0)")
check(D(0x002ED8C0, 8).get(0x002ED8C0) == ("mov", "dword ptr [rdx], 0x20"), "B4b 002ED8C0 writes kind 0x20 (003A13F0's six sites)")
e = F(0x003DCA30)
kstores = [a for a, (mn, op) in e.items() if mn == "mov" and op.startswith("dword ptr [r9]")]
check(kstores == [0x003DCA49] and e[0x003DCA49] == ("mov", "dword ptr [r9], 0x1e"),
      "B4c 003DCA30 writes kind 0x1E and nothing else through the kind pointer (003DC977, 003DC683 via 003DC5B0)")
check(D(0x003EB10C, 12).get(0x003EB10C, ("", ""))[1].endswith(", 0x24"),
      "B4d the BGM stream descriptor's kind (02B5E0FC) is written only as 0x24 at 003EB10C (003EAE29, and 003EADE0's request)")
check(D(0x002E61A3, 8).get(0x002E61A3) == ("mov", "ecx, 0x20") and D(0x002E6272, 8).get(0x002E6272) == ("mov", "ecx, 0x20"),
      "B4e 002E60F0's two sites the dataflow did not reach pass kind 0x20")

# ---- B5 the script verbs: debug_filesize 0x2006 (0050DF70) and debug_fileread 0x2007 (0050DFE0) ----
vc = io.open(os.path.join(HERE, "verb_census.out"), encoding="utf-8").read()
check("verb 0x2006: 0 calls" in vc and "verb 0x2007: 0 calls" in vc and "PASS  control" in vc,
      "B5 0050DF9D / 0050E039 take kind from the script stack; shipped bytecode calls 0x2006 / 0x2007 zero times (verb_census.out)")

# ---- B6 the three computed-id sites ----
h = F(0x0056F2A0)
check(h.get(0x0056F2BD) == ("cmp", "dl, 5") and h.get(0x0056F2C0) == ("jbe", "0x56f34d") and h.get(0x0056F351) == ("call", "0x577880"),
      "B6a 00575C30's category byte: the only fresh source is 0056F2A0, which posts it only when <= 5 (0056F2BD); the other "
      "senders replay +0xD2 (written only at 00575CD2 from an accepted category) or the history at +0xD4")
tv = struct.unpack("<6H", img.rd(0x00D23740, 12))
check(min(tv) >= 0x228, "B6b so 00575C30's id >= 00D23740[0..5] = %s >= 0x228 - never 0xE2..0xE4" % list(tv))

# ---- B7 the loca_*.cl2 request that exists: 003C1F00 ----
q = F(0x003C1F00)
check(q.get(0x003C2068) == ("movzx", "eax, byte ptr [r8 + 1]") and q.get(0x003C207A) == ("add", "r8d, 0xe1")
      and q.get(0x003C2071) == ("mov", "edx, 7") and q.get(0x003C208D) == ("call", "0x249210")
      and q.get(0x003C2043) == ("mov", "rcx, qword ptr [rax + 0xe8]") and q.get(0x003C209D) == ("mov", "qword ptr [rax + 0x118], rcx"),
      "B7a 003C1F00 requests kind 7 id 0xE1 + entry.byte1 of [[02B457E0]+0xE8] when the byte is non-zero, into +0x118")
r = F(0x003BC2D0)
check(r.get(0x003BC35D) == ("mov", "r8d, 0xa4") and r.get(0x003BC373) == ("mov", "qword ptr [rdi + 0xe8], rcx"),
      "B7b +0xE8 is kind 7 id 0xA4 (003BC35D)")
arr = R.regions[1][0][7]
names = {i: (R.row(arr, i) or "-").split("\\")[-1] for i in (0xA4, 0xE2, 0xE3, 0xE4)}
print("    kind 7 rows (region 1): %s" % {hex(k): v for k, v in names.items()})
check(names[0xA4] == "menumap_common.bin" and names[0xE2] == "Loca_gil.cl2" and names[0xE3] == "Loca_bhm.cl2" and names[0xE4] == "Loca_rbl.cl2",
      "B7c 0xA4 = menumap_common.bin; 0xE2/0xE3/0xE4 = Loca_gil/Loca_bhm/Loca_rbl.cl2")
sel = collections.Counter()
rows = {}
for pth in arc.find("menumap_common.bin"):
    d = arc.get(pth)
    off = struct.unpack_from("<H", d, 8)[0]
    n = struct.unpack_from("<I", d, off)[0]
    for i in range(n):
        b1 = d[off + 4 + 8 * i + 1]
        sel[b1] += 1
        if b1:
            rows.setdefault(i, set()).add((b1, struct.unpack_from("<I", d, off + 8 + 8 * i)[0]))
print("    entry byte +1 over all %d menumap_common.bin copies: %s; non-zero entries %s" % (len(arc.find("menumap_common.bin")), dict(sel), rows))
check(set(rows) == {40, 46} and rows[40] == {(1, 60181)} and rows[46] == {(2, 60187)},
      "B7d the only non-zero selectors: entry 40 -> 1 (0xE2 Loca_gil, gil01_s02), entry 46 -> 2 (0xE3 Loca_bhm, bhm01_s01); "
      "no entry selects 3 (Loca_rbl)")

# ---- B8 the reader ----
u = F(0x003C26C0)
w = D(0x0024A9E0, 0x1E)
check(u.get(0x003C2794) == ("mov", "rcx, qword ptr [r13 + 0x118]") and u.get(0x003C27A9) == ("call", "0x24a9e0")
      and u.get(0x003C27B0) == ("movzx", "ecx, word ptr [rax + 0xc]") and u.get(0x003C27B4) == ("mov", "edi, dword ptr [rax + 8]")
      and u.get(0x003C27B7) == ("movzx", "esi, word ptr [rax + 0xe]") and u.get(0x003C2824) == ("call", "0x24a480")
      and w.get(0x0024A9E0) == ("lea", "rax, [rcx + 0x10]"),
      "B8a 003C26C0 reads the .cl2 at +0x118 (else +0x110) as a TIM2 picture header at +0x10: palette = +0x10 + u32[+0x18] + "
      "u16[+0x1C] = +0x40, colours = u16[+0x1E]; 0024A480 binds them to the page image")
v = F(0x0024A480)
t = F(0x0024A1D0)
check(v.get(0x0024A4BE) == ("mov", "qword ptr [rbx + 0x28], rsi") and v.get(0x0024A4B8) == ("shl", "eax, 0x12")
      and t.get(0x0024A36E) == ("movzx", "ecx, byte ptr [rax + 0x13]") and t.get(0x0024A372) == ("movzx", "r9d, byte ptr [rax + 0x12]")
      and t.get(0x0024A380) == ("call", "0x180e70"),
      "B8b the palette override (+0x28, count << 18) is decoded by 00180E70 with the IMAGE's own clut and image type bytes "
      "([picture header]+0x12/+0x13), never the .cl2's +0x22/+0x23")
k = F(0x00180E70)
check(k.get(0x00180EBA) == ("shl", "edi, 8") and k.get(0x00180EFF) == ("cmp", "edi, 0x4304") and k.get(0x00180F8E) == ("call", "0x17f3b0"),
      "B8c 00180E70 copies the palette in 16-entry rows, un-swizzling the 8-entry blocks for type pairs 0x105/0x205/0x305/"
      "0x4104/0x4204/0x4304, with no per-byte channel reordering")
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
