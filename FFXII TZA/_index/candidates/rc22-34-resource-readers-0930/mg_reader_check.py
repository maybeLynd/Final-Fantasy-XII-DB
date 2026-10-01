"""RC-32 / RC-33 / RC-34: the readers of a loaded worldmap/meshdata.mg, checked against the image and both shipped files.

A. Reader instructions: every cited instruction must decode to the stated form (a known-answer control per site).
B. Raw E8/E9 sweep of .text (function-list independent) for the consumers of a sub-mesh pointer; the known call
   sites are the positive control, and any extra site is printed and FAILs (the reader set would be incomplete).
C. Both shipped .mg files parsed under the reader model (directory -> sub-mesh headers -> slots / vertices / indices).
D. RC-34: the name -> texture chain (00D23270 table, the loader's 00D231C0 table and kind-7 ids 0xAA+i).
Prints FAILS N."""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, ins_at, text_range, u64, u32, cstr, names

FAILS = 0


def check(ok, msg):
    global FAILS
    print(("PASS " if ok else "FAIL ") + msg)
    FAILS += 0 if ok else 1


# ---------------------------------------------------------------- A. reader instructions
SITES = [
    # file directory: sub-mesh i = buf + s32[buf + 8*i]  (only the even dwords are offsets)
    (0x00274783, "mov eax, dword ptr [rcx + rax*8]"),
    (0x00274786, "add rax, rcx"),
    # 00563110 (world-map bind): sub0 = entry 0, sub1 = entry 1
    (0x0056312D, "xor edx, edx"),
    (0x0056313C, "mov edx, 1"),
    # slot j = sub + s32[sub+0x10] + j*0x20; slot count s32[sub+0x14]
    (0x00555A50, "movsxd rax, dword ptr [rcx + 0x10]"),
    (0x00555A57, "shl r8, 5"),
    (0x00563160, "cmp dword ptr [rax + 0x14], edi"),
    # bind: name matched against the 00D23270 {psd name, texture name} table, registry lookup, stored over slot+0
    (0x0056314D, "lea r14, [rip + 0x7c011c]"),
    (0x005631BB, "mov rcx, qword ptr [r14 + r11*8 + 8]"),
    (0x005631C5, "call 0x24a5a0"),
    (0x005631CA, "mov qword ptr [rbx], rax"),
    # 0024A5A0: 64 x 0x48 registry at 0208F580, live flag 0x20 at +0x38, name at +0
    (0x0024A5A3, "lea r9, [rip + 0x1e44fd6]"),
    (0x0024A5B0, "test byte ptr [r9 + 0x38], 0x20"),
    (0x0024A5DA, "add r9, 0x48"),
    (0x0024A5DE, "cmp r10d, 0x40"),
    # 002493D0: request + claim a registry slot under the caller's name (0024A4E0 = the only name writer)
    (0x002493EF, "call 0x24a4e0"),
    (0x002493FB, "mov qword ptr [rbx + 0x18], rax"),      # request+0x18 = the named slot
    (0x002493F4, "lea rcx, [rip + 0x275]"),               # request+0x10 = completion callback 00249670
    (0x00249674, "mov rcx, qword ptr [rcx + 0x18]"),      # 00249670: 0024A1D0(slot, loaded buffer)
    (0x00249678, "jmp 0x24a1d0"),
    # 00562F90: meshdata.mg = kind 7 id 0xA8, buffer at obj+0x10; textures kind 7 id 0xAA+i named from 00D231C0
    (0x00562FB6, "mov r8d, 0xa8"),
    (0x00562FDA, "mov qword ptr [r14 + 0x10], r8"),
    (0x00562FCB, "lea rsi, [rip + 0x7c01ee]"),
    (0x00563000, "lea r8d, [rbx + 0xaa]"),
    (0x0056301F, "call 0x2493d0"),
    # sub0 drawer 005556A0 (via 00562F30 = mov rcx,[rcx]; jmp): vertices s32[sub+8], count s32[sub+0xC]
    (0x00562F30, "mov rcx, qword ptr [rcx]"),
    (0x0055576D, "mov eax, dword ptr [rbp + 0xc]"),
    (0x0055577A, "movsxd rdx, dword ptr [rbp + 8]"),
    (0x005557F9, "movsxd rsi, dword ptr [rbp + 8]"),
    (0x00555808, "cmp dword ptr [rbp + 0x14], r14d"),
    (0x00555830, "movsxd rdi, dword ptr [rbp + 0x10]"),
    (0x00555884, "mov r8, qword ptr [rdi]"),          # the texture bound over slot+0
    (0x0055588C, "mov rax, qword ptr [r8 + 0x20]"),
    (0x00555898, "movzx ebx, word ptr [rax + 0x14]"),   # texture width
    (0x0055589C, "movzx ebp, word ptr [rax + 0x16]"),   # texture height
    (0x005558BE, "mov r14d, 4"),                        # four vertices per slot
    (0x00555900, "mulss xmm0, dword ptr [rsi]"),        # s * width
    (0x0055590B, "mulss xmm1, dword ptr [rsi + 4]"),    # t * height
    (0x00555910, "add rsi, 0x20"),                      # 0x20-byte vertex, never reset per slot
    (0x005558F0, "movsx eax, word ptr [rdi + 0x18]"),   # slot colour s16[4]
    (0x0055593C, "movsx eax, word ptr [rdi + 0x1e]"),
    (0x00555858, "call 0x181870"),
    # sub1 drawer 00555400 -> 00555D10 per slot
    (0x00555660, "movsxd rdx, dword ptr [rdi + 0x10]"),
    (0x00555681, "cmp ebx, dword ptr [rdi + 0x14]"),
    (0x00555D5E, "movsxd r13, dword ptr [rcx + 8]"),    # vertex base
    (0x00555D64, "movsxd rax, dword ptr [rcx]"),        # index base
    (0x00555D6A, "movsxd rdx, dword ptr [rdx + 0x10]"), # slot index start
    (0x00555D77, "lea r14, [rcx + rdx*2]"),
    (0x00555D7B, "cmp dword ptr [r15 + 0x14], esi"),    # slot index count
    (0x00555DB2, "cmp esi, 0x20"),                      # 32-vertex batches
    (0x00555DF3, "cmp ax, bx"),                         # bit 15 = restart
    (0x00555E38, "and ebx, 0x7fff"),
    (0x00555E3E, "shl rbx, 5"),
    (0x00555E68, "movd xmm0, dword ptr [rbx]"),         # s32 colour
    (0x00555E71, "cvtdq2ps xmm0, xmm0"),
    (0x00555E53, "lea r8, [rbx + 0x10]"),               # position vec4
    (0x00555B96, "movabs rcx, 0x3000000000008000"),     # GIF tag, NREG 3
    (0x00555BA6, "mov qword ptr [r10 + 8], 0x412"),     # REGS ST, RGBAQ, XYZ2
    (0x00555BB7, "movsx eax, word ptr [r8 + 0x18]"),    # slot colour
    (0x005562E8, "mov qword ptr [rcx], 0xa"),           # PRIM line strip (flag off)
    (0x005562F3, "mov eax, 0x4c"),                      # PRIM tri strip, gouraud, alpha
    (0x005562F8, "mov r8d, 0x5c"),                      # + texture
    (0x00556311, "mov qword ptr [rax + 8], 0"),         # A+D address 0 = PRIM
    # who draws what
    (0x00562F70, "mov rdx, qword ptr [rcx + 8]"),       # 00562F40: sub1
    (0x00562F74, "mov rcx, qword ptr [rcx + 0x20]"),    #           texture = obj+0x20 (w_shade_p)
    (0x0055A91C, "mov rcx, qword ptr [rdi + 0xc8]"),    # license board: raw buffer
    (0x0055A923, "mov edx, 1"),                         #   entry 1 = sub1
    (0x0055A954, "xor ecx, ecx"),                       #   no texture
]
print("== A. reader instructions")
for a, want in SITES:
    x = ins_at(a)
    got = f"{x.mnemonic} {x.op_str}" if x else None
    check(got == want, f"{a:08X} {want}" + ("" if got == want else f"   (decoded: {got})"))

# ---------------------------------------------------------------- B. raw call sweep
print("== B. raw E8/E9 sites of the sub-mesh consumers (.text, function-list independent)")
t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
EXPECT = {
    0x00274780: {0x0055A928, 0x00563133, 0x00563144},
    0x00555A50: {0x0056316A, 0x005631E8},
    0x00555400: {0x0055A967, 0x00562F78},
    0x00555D10: {0x0055567A},
    0x005556A0: {0x00562F33},
    0x00562F30: {0x005527D2},
    0x00562F40: {0x005536B7},
    0x00563110: {0x00552362},
    0x00562F90: {0x005505D0},
}
found = {t: set() for t in EXPECT}
for p in range(len(blob) - 5):
    if blob[p] in (0xE8, 0xE9):
        tgt = t0 + p + 5 + struct.unpack_from("<i", blob, p + 1)[0]
        if tgt in found:
            x = ins_at(t0 + p)
            if x is not None and x.size == 5 and x.mnemonic in ("call", "jmp"):
                found[tgt].add(t0 + p)
for t, want in EXPECT.items():
    extra = found[t] - want
    miss = want - found[t]
    check(not miss and not extra, f"{t:08X} {names.get(t, '')}: sites {sorted('%08X' % s for s in found[t])}"
          + (f" missing {sorted('%08X' % s for s in miss)}" if miss else "")
          + (f" EXTRA {sorted('%08X' % s for s in extra)}" if extra else ""))
# rip references to the bind table: only 00563110
refs = []
for p in range(len(blob) - 4):
    disp = struct.unpack_from("<i", blob, p)[0]
    for k in (0, 1, 2, 4):
        tg = t0 + p + 4 + k + disp
        if 0x00D23270 <= tg < 0x00D232D8:
            for back in range(7, 0, -1):
                x = ins_at(t0 + p - back)
                if x is not None and x.address + x.size == t0 + p + 4 + k and "rip" in x.op_str:
                    refs.append((x.address, tg)); break
check(sorted(refs) == [(0x0056314D, 0x00D23270), (0x00563157, 0x00D232D0)],
      "rip references into the 00D23270 bind table: " + ", ".join("%08X->%08X" % r for r in sorted(refs)))
# indirect reach: rip references (lea of a function pointer) and raw qwords anywhere in the file equal to a consumer
# entry. Control: the license-board widget procedure 0055A8A0 is installed by lea at 0055A84B.
TARGETS = set(EXPECT) | {0x0055A8A0}
fprefs = {t: [] for t in TARGETS}
for p in range(len(blob) - 4):
    disp = struct.unpack_from("<i", blob, p)[0]
    for k in (0, 1, 2, 4):
        tg = t0 + p + 4 + k + disp
        if tg in fprefs:
            for back in range(7, 0, -1):
                x = ins_at(t0 + p - back)
                if x is not None and x.address + x.size == t0 + p + 4 + k and "rip" in x.op_str:
                    fprefs[tg].append(x.address); break
qrefs = {t: [] for t in TARGETS}
for p in range(0, len(d) - 8, 8):
    q = struct.unpack_from("<Q", d, p)[0]
    if q in qrefs:
        qrefs[q].append(p)
check(fprefs[0x0055A8A0] == [0x0055A84B], "control: 0055A8A0 has its installer lea at 0055A84B (found %s)"
      % ["%08X" % a for a in fprefs[0x0055A8A0]])
for t in sorted(EXPECT):
    check(not fprefs[t] and not qrefs[t], f"{t:08X}: no rip reference, no aligned data qword (indirect reach none): "
          f"rip {['%08X' % a for a in fprefs[t]]} qword@fileoff {['%X' % a for a in qrefs[t]]}")

# ---------------------------------------------------------------- C. the shipped files
print("== C. both shipped meshdata.mg under the reader model")
ROOT = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
files = [f"{ROOT}/{l}/worldmap/meshdata.mg" for l in ("in", "ch")]
blobs = [open(f, "rb").read() for f in files]
check(blobs[0] == blobs[1], "in and ch copies byte-identical (%d B)" % len(blobs[0]))
b = blobs[0]
n = len(b)
dirent = [struct.unpack_from("<II", b, 8 * i) for i in range(2)]
check(dirent == [(0x10, 0x2C0), (0x2D0, 0x3280)], f"directory {{offset,size}} x2 = {[(hex(o), hex(s)) for o, s in dirent]}")
check(dirent[0][0] + dirent[0][1] == dirent[1][0] and dirent[1][0] + dirent[1][1] == n,
      "the two sub-meshes tile the file exactly (0x10+0x2C0 = 0x2D0, 0x2D0+0x3280 = EOF)")
subs = []
for i, (so, ss) in enumerate(dirent):
    h = struct.unpack_from("<6i", b, so)
    idx_off, idx_n, vtx_off, vtx_n, slot_off, slot_n = h
    pad = b[so + 0x18:so + slot_off]
    print(f"   sub{i} @0x{so:X}: idxOff 0x{idx_off:X} idxCount {idx_n}  vtxOff 0x{vtx_off:X} vtxCount {vtx_n}  "
          f"slotOff 0x{slot_off:X} slotCount {slot_n}")
    check(pad == b"\0" * len(pad), f"sub{i} header 0x18 B + {len(pad)} zero bytes before the slots")
    check(slot_off + 0x20 * slot_n <= vtx_off, f"sub{i} slots end (0x{slot_off + 0x20 * slot_n:X}) <= vertices (0x{vtx_off:X})")
    check(vtx_off + 0x20 * vtx_n == idx_off, f"sub{i} vertices ({vtx_n} x 0x20) end exactly at the index stream")
    check(idx_off + 2 * idx_n <= ss and ss - (idx_off + 2 * idx_n) < 16,
          f"sub{i} index stream ({idx_n} x u16) ends {ss - (idx_off + 2 * idx_n)} B before the sub-mesh end")
    subs.append((so, h))
# slots
for i, (so, h) in enumerate(subs):
    idx_off, idx_n, vtx_off, vtx_n, slot_off, slot_n = h
    for j in range(slot_n):
        s = so + slot_off + 0x20 * j
        name = b[s:s + 16].split(b"\0")[0].decode("latin-1")
        start, cnt = struct.unpack_from("<ii", b, s + 0x10)
        col = struct.unpack_from("<4h", b, s + 0x18)
        print(f"   sub{i} slot{j}: name {name!r:12} indexStart {start:4} indexCount {cnt:4} colour {col}")
        check(start + cnt <= idx_n, f"sub{i} slot{j} index range inside the stream")
# sub0: vertices {s,t,1,1 floats}{x,y,z,w floats}; the drawer's fixed order vs the index stream
so, h = subs[0]
v = [struct.unpack_from("<8f", b, so + h[2] + 0x20 * k) for k in range(h[3])]
check(all(x[2] == 1.0 and x[3] == 1.0 and x[7] == 1.0 and x[5] == 0.0 for x in v),
      "sub0: every vertex = (s, t, 1, 1)(x, 0, z, 1) floats")
check(all(0.0 <= x[0] <= 1.0 and 0.0 <= x[1] <= 1.0 for x in v), "sub0: s, t in [0, 1] (scaled by the texture size)")
idx0 = struct.unpack_from(f"<{h[1]}H", b, so + h[0])
same = True
for j in range(4):
    strip = [w & 0x7FFF for w in idx0[4 * j:4 * j + 4]]
    tri_a = {frozenset(strip[k:k + 3]) for k in range(2)}
    drawn = [4 * j + 3, 4 * j, 4 * j + 1, 4 * j + 2]        # 005556A0 emission order: k3, k0, k1, k2
    tri_b = {frozenset(drawn[k:k + 3]) for k in range(2)}
    same &= tri_a == tri_b and idx0[4 * j] & 0x8000 and not any(w & 0x8000 for w in idx0[4 * j + 1:4 * j + 4])
check(bool(same), "sub0: each slot's index strip (restart flag on its first index) covers the same two triangles "
      "as 005556A0's fixed k3,k0,k1,k2 emission")
xs = sorted({round(x[4], 3) for x in v}); zs = sorted({round(x[6], 3) for x in v})
print(f"   sub0 x values {xs}  z values {zs}")
# sub1: s32 colours + position; index flags
so, h = subs[1]
vtx = [struct.unpack_from("<4i4f", b, so + h[2] + 0x20 * k) for k in range(h[3])]
check(all(0 <= c <= 0xFF for x in vtx for c in x[:4]), "sub1: vertex +0x00..+0x0C are small s32 colour values")
check(all(x[5] == 0.0 and x[7] == 1.0 for x in vtx), "sub1: position (x, 0, z, 1)")
idx1 = struct.unpack_from(f"<{h[1]}H", b, so + h[0])
check(max(w & 0x7FFF for w in idx1) < h[3], f"sub1: every index & 0x7FFF < vertexCount {h[3]}")
restarts = sum(1 for w in idx1 if w & 0x8000)
check(idx1[0] & 0x8000 != 0, "sub1: the stream opens with a restart")
print(f"   sub1: {len(idx1)} indices, {restarts} strips (bit-15 restarts)")
cols = sorted({x[:4] for x in vtx})
print(f"   sub1 distinct vertex colours: {len(cols)}; first {cols[:3]}")
# control: the old reading must fail under the reader model
check(struct.unpack_from("<I", b, 4)[0] + 0x10 == 0x2D0, "control: +0x04 (0x2C0) is sub0's SIZE, not an offset to "
      "an index table (0x10 + 0x2C0 = sub1's offset)")

# ---------------------------------------------------------------- D. RC-34 name -> texture
print("== D. RC-34: slot name -> texture")
bind = []
for k in range(6):
    a = u64(0x00D23270 + 16 * k); t = u64(0x00D23278 + 16 * k)
    bind.append((cstr(a), cstr(t)))
print("   00D23270:", bind)
check(bind[:4] == [(f"main{i}.psd", f"w_main{i}") for i in range(4)] and bind[4] == ("upper", "w_shade_p")
      and bind[5] == ("linetex", "w_line01"), "bind table = main0..3.psd -> w_main0..3, upper -> w_shade_p, linetex -> w_line01")
check(u64(0x00D232D0) == 0xA6, "table end sentinel 00D232D0 is the next datum (the loop bound, not a 7th row)")
load = [(cstr(u64(0x00D231C0 + 16 * i)), u32(0x00D231C8 + 16 * i)) for i in range(11)]
print("   00D231C0:", load)
import kind7
arr, ps = kind7.paths(7, limit=0x5E1, stop_on_miss=False)
for i in range(1, 5):
    nm = load[i][0]
    pth = ps.get(0xAA + i, "")
    check(nm == f"w_main{i - 1}" and pth.lower().endswith(f"tm2_menu\\w_main{i - 1}.tm2"),
          f"loader row {i}: name {nm} -> kind 7 id 0x{0xAA + i:X} -> {pth}")
    shipped = os.path.exists(f"{ROOT}/in/tm2_menu/w_main{i - 1}.tm2")
    check(shipped, f"shipped: in/tm2_menu/w_main{i - 1}.tm2")
check(ps.get(0xA8, "").lower().endswith("worldmap\\meshdata.mg"), "control: kind 7 id 0xA8 -> " + ps.get(0xA8, ""))
check(load[0][0] == "w_shade_p" and ps.get(0xAA, "").lower().endswith("w_shade_p.tm2"),
      "sub1's world-map texture obj+0x20 = loader row 0 = w_shade_p (id 0xAA)")
print(f"FAILS {FAILS}")
