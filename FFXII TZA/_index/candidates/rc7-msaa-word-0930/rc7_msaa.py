"""rc7_msaa.py - RC-7 (ORACLE, 2026-09-30).  What the MSAA setting word at 01DF0900 holds.

1. Reference census of 01DF0900..01DF0903 over every function body (memsweep.py: .pdata chain roots plus leaf bodies
   from functions.tsv): rip-relative operands of any width whose byte range overlaps the word, the image-base-relative
   form (disp 0x01CD0900 on any base register), and 8-byte pointers / 4-byte RVAs to the word anywhere in the file.
   Control: the reads 0018644D (feeding the page-cited compare 00186453) and 001865BD must be found.
2. The value sources, each checked against the decoded instruction (a mismatch is a FAIL):
   - the .data initial value;
   - 00186CD0 (from the scene constructor 00184F20): word = f([framework + 0xD3C]);
   - 007980A0 (boot): [framework + 0xD20 + 0x1C] = 001DE570(GameSetting config) - the framework field's only value store;
   - 001DE570: table 00900EE8 indexed by (config +0x20) mod 5;
   - 00187950: word = [scene + 0xDC8] when [scene + 1]; scene +0xDC8 is written by the constructor (0) and 00189520,
     whose two callers are console arms that pass 001DE570's result;
   - 2e: displacement stores to framework +0xD20..+0xD54 in every function that loads [02EA5368] or calls its getter
     must be the constructor's only (the boot store rebases to +0xD20 first, so it is checked by instruction above).
3. The render side: the three render commands built by 00186410 / 00187950 carry the word at command +8, the callback
   00189110 copies its low byte to [target + 9], and 0061FDA0 reads [[texture + 0x20] + 9] into the D3D11_TEXTURE2D_DESC
   (desc at rsp+0x48: SampleDesc.Count at +0x14 = rsp+0x5C, Quality at +0x18 = rsp+0x60) with two remaps, then calls
   device vtable +0x28 (ID3D11Device::CreateTexture2D).
Output rc7_refs.tsv (the census) and the checks on stdout."""
import io, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img, memsweep

HERE = os.path.dirname(os.path.abspath(__file__))
W = 0x01DF0900
FAILS = []


def expect(va, text):
    x = img.dis(va, 16)[0]
    got = "%s %s" % (x.mnemonic, x.op_str)
    ok = got == text
    if not ok:
        FAILS.append("%08X: expected %r got %r" % (va, text, got))
    t = img.ripmem(x)
    print("  %s %08X  %-48s%s" % ("ok  " if ok else "FAIL", va, got, ("  -> %08X" % t) if t else ""))


recs = memsweep.load()
rows = []
for r in recs:
    t = r[10]
    if t is not None and t < W + 4 and t + max(r[9], 1) > W:
        rows.append(r + ("rip",))
    elif r[5] not in (None, "rip") and r[8] <= W - img.BASE + 3 and r[8] + max(r[9], 1) > W - img.BASE:
        rows.append(r + ("image-base-relative",))
with io.open(os.path.join(HERE, "rc7_refs.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("site\tfunction\tinstruction\twidth\tform\taccess\n")
    for r in rows:
        f.write("%08X\t%08X\t%s %s\t%d\t%s\t%s\n" % (r[0], r[1], r[2], r[3], r[9], r[12], "W" if r[11] else "R"))
print("1. references to 01DF0900..03: %d (writes %d) in %s" % (len(rows), sum(1 for r in rows if r[11]),
                                                              sorted({"%08X" % r[1] for r in rows})))
for r in rows:
    print("    %08X %08X %-5s %-44s w%d %s" % (r[0], r[1], r[2], r[3], r[9], "WRITE" if r[11] else ""))
if not {0x0018644D, 0x001865BD} <= {r[0] for r in rows}:
    FAILS.append("census control")
ptrs = [m.start() for m in re.finditer(re.escape(struct.pack("<Q", W)), img.blob)]
rvas = [m.start() for m in re.finditer(re.escape(struct.pack("<I", W - img.BASE)), img.blob)]
print("   8-byte pointers to the word in the file: %d; 4-byte RVAs: %d" % (len(ptrs), len(rvas)))
print("   .data initial value:", img.u32(W))
if img.u32(W) != 4:
    FAILS.append("initial value")

print("2a. 00186CD0 (scene constructor 00184F20 -> 00186CD0, 00185056):")
for va, t in ((0x00186D2B, "mov eax, dword ptr [rip + 0x1c69bcf]"), (0x00186D31, "mov dword ptr [rip + 0x2b3134d], eax"),
              (0x00186D37, "call 0x796e20"), (0x00186D3C, "mov ebp, dword ptr [rax + 0xd3c]"), (0x00186D50, "test ebp, ebp"),
              (0x00186D52, "je 0x186d70"), (0x00186D54, "cmp ebp, 1"), (0x00186D57, "mov byte ptr [rsi + 0xdba], 1"),
              (0x00186D5E, "cmove ebp, r12d"), (0x00186D68, "mov dword ptr [rip + 0x1c69b92], ebp"),
              (0x00186D70, "mov byte ptr [rsi + 0xdba], r12b"), (0x00186D81, "mov dword ptr [rip + 0x1c69b78], r12d")):
    expect(va, t)
expect(0x00796E20, "mov rax, qword ptr [rip + 0x270e541]")
print("2b. 007980A0 (boot; called from 007A3770): framework +0xD20 base, +0x1C = +0xD3C")
for va, t in ((0x00798545, "mov rdi, qword ptr [rip + 0x270ce1c]"), (0x0079854C, "add rdi, 0xd20"),
              (0x00798563, "mov rcx, qword ptr [rip + 0x17ea7b6]"), (0x0079856A, "call 0x1de570"),
              (0x0079856F, "mov dword ptr [rdi + 0x1c], eax")):
    expect(va, t)
print("   callers of 007980A0:", ["%08X" % a for a, k in img.calls_to(0x007980A0)])
print("2c. 001DE570: count = table[(cfg+0x20) mod 5]")
for va, t in ((0x001DE570, "mov r8d, dword ptr [rcx + 0x20]"), (0x001DE574, "mov eax, 0xcccccccd"),
              (0x001DE58C, "mov eax, dword ptr [rcx + r8*4]")):
    expect(va, t)
tbl = struct.unpack("<5i", img.rd(0x00900EE8, 20))
print("   table 00900EE8 =", tbl)
if tbl != (1, 2, 4, 8, 9):
    FAILS.append("table")
print("   callers of 001DE570:", ["%08X in %08X" % (a, img.owner(a)) for a, k in img.calls_to(0x001DE570)])
print("2d. 00187950 and the scene field +0xDC8")
for va, t in ((0x00187A6D, "cmp byte ptr [r14 + 1], r12b"), (0x00187A73, "mov eax, dword ptr [r14 + 0xdc8]"),
              (0x00187A7A, "mov dword ptr [rip + 0x1c68e80], eax"), (0x00189520, "mov byte ptr [rcx + 1], 1"),
              (0x00189524, "mov dword ptr [rcx + 0xdc8], edx"), (0x00184F54, "xor esi, esi"),
              (0x00185046, "mov dword ptr [rdi + 0xdc8], esi"), (0x001D4A6F, "call 0x1de570"), (0x001D4A80, "call 0x189520"),
              (0x001D51C1, "call 0x1de570"), (0x001D51D2, "call 0x189520")):
    expect(va, t)
dc8 = [r for r in recs if r[11] and r[5] not in (None, "rip") and r[8] <= 0xDC8 < r[8] + r[9] and r[8] > 0xDC8 - 8]
print("   every write covering a +0xDC8 field image-wide: %s" % ["%08X/%08X %s %s" % (r[0], r[1], r[2], r[3]) for r in dc8])
print("   callers of 00189520:", ["%08X in %08X" % (a, img.owner(a)) for a, k in img.calls_to(0x00189520)])
fw_fns = {r[1] for r in recs if r[10] == 0x02EA5368}
fw_fns |= {img.owner(a) for g in (0x00796E20, 0x00796E30) for a, k in img.calls_to(g)}
fw_st = [r for r in recs if r[11] and r[1] in fw_fns and r[5] not in (None, "rip", "rsp") and 0xD20 <= r[8] <= 0xD54]
print("2e. displacement stores to +0xD20..+0xD54 in the %d functions that load [02EA5368] or call its getter:" % len(fw_fns))
for r in fw_st:
    print("    %08X %08X %s %s" % (r[0], r[1], r[2], r[3]))
if {r[1] for r in fw_st} != {0x00792350}:
    FAILS.append("framework field store search")
print("3. render side")
for va, t in ((0x001864C3, "mov ecx, dword ptr [rip + 0x1c6a437]"), (0x001864C9, "mov dword ptr [rax + 8], ecx"),
              (0x001864B3, "lea rdx, [rip + 0x2c56]"), (0x00189110, "mov rax, qword ptr [rcx + 0x10]"),
              (0x00189114, "mov rcx, qword ptr [rax]"), (0x00189117, "movzx eax, byte ptr [rax + 8]"),
              (0x0018911B, "mov byte ptr [rcx + 9], al"), (0x0061FEB0, "mov rcx, qword ptr [rbx + 0x20]"),
              (0x0061FEC1, "movzx eax, byte ptr [rcx + 9]"), (0x0061FECC, "mov dword ptr [rsp + 0x5c], eax"),
              (0x0061FED0, "cmp eax, 7"), (0x0061FED5, "mov dword ptr [rsp + 0x5c], 4"), (0x0061FEDD, "mov dword ptr [rsp + 0x60], 0x10"),
              (0x0061FEE7, "cmp eax, 9"), (0x0061FEEC, "mov dword ptr [rsp + 0x5c], 8"), (0x0061FEF4, "mov dword ptr [rsp + 0x60], 0x10"),
              (0x0061FEFE, "cmp eax, 1"), (0x0061FF01, "jbe 0x61ff2c"), (0x0061FE7A, "mov dword ptr [rsp + 0x48], r12d"),
              (0x006200CF, "lea rdx, [rsp + 0x48]"), (0x006200E5, "call qword ptr [rax + 0x28]")):
    expect(va, t)
print("   the image's anti-aliasing label list at 01DF0270 (no code or data reference to it was found):",
      [img.rd(struct.unpack("<Q", img.rd(0x01DF0270 + 8 * k, 8))[0], 12).split(b"\0")[0].decode() for k in range(7)])
print("FAILS", len(FAILS), FAILS)
