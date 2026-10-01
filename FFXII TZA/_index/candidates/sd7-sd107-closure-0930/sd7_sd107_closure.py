"""sd7_sd107_closure.py - close the residue of SD-7 and SD-107 that SWE2-ORACLE narrowed (SWE2-STRUCT, 2026-09-30).
Static, the certified image, through Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py. Nothing is
executed and nothing is live. structflow.py is unchanged by this record.

SD-7  (who calls GameApplication slot 15, 0017D1A0, the setter of the input manager's +0x39 poll gate):
  ORACLE left 34 of the 192 `call/jmp [vtable+0x78]` dispatch sites untyped. This checker types the object each of
  those 34 dispatches on to a concrete non-application class or domain, and adds the two dispatch forms ORACLE's
  vtable census did not carry (a call through a register, and a call through a rip slot). The residue partitions into:
    R1 render context   the object is the Phyre immediate-geometry render context = PrimitiveRendererD3D11 (45 slots,
                        +0x78 = slot 15 = 006CAB80); its sibling Gi/DynGeoFont draw methods dispatch the SAME object
                        at slots >= 31 (E4). Five draw methods, plus the global 01FC35F8 (0020FF10 x2) which holds
                        that context (written only by 00210320 from the rdx of GiVmax's slot-1 draw 001DB3D0).
    R2 Steam            001F3AE0's [rbx] is a Steam client interface vtable (001F3E10 -> SteamInternal_CreateInterface
                        008C3188; the strings are SteamClient017 / SteamUtils009 ...).
    R3 Bullet           btCompoundShape (008330A0's second site, same rbx), btBvhTriangleMeshShape (008420F0 x2,
                        00837680's this), a btConvexShape support pair (00831380, caller 0084CB30 loads two
                        btCollisionShape at +0x30/+0x38), and a btDiscreteDynamicsWorld's debug drawer (00855B80).
    R4 PPFX             the base is loaded at a field of a PPFX-middleware object (functions in 006F0000..0079000);
                        where the dispatched object is typable its vtable is a PPFX GPU interface (IGPUEffect +0x78 =
                        789CD0, IGPUDevice +0x78 = 724C10). 20 sites.
    R5 typed handle     007AB5C0's object is a resolved resource handle (007AB1E0 checks handle types 2/8/9 and
                        indexes the registries 02EAD5xx).
  The two extra forms: no register-target call in the image loads its target from [reg+0x78] (S6), and no rip-target
  call does either - the rip calls are import thunks (S7). So slot 15 can be reached only through a [vtable+0x78]
  dispatch on a GameApplication object, and no such object exists: SD-7 is CLOSED. The +0x39 gate is set only by the
  other setter 001989D0.

SD-107  (does anything instantiate text-element kind 1, whose emitter 002AA800 skips the control-code engine):
  ORACLE left 74 register-sourced +0xA3 stores open. This checker separates them by store width and types the base:
    T1  exactly two of the 74 are BYTE stores at +0xA3 (0077FFE0@00780079, 00780590@00780729). Both are PPFX effect
        objects (0077-0078 range) that write +0xA0,+0xA1,+0xA2,+0xA3 as one 4-byte tuple - a colour/vector channel,
        not a text-element kind (a text element's builder 002B3C30 writes the kind as a lone byte and puts floats at
        +0x04 = 23.0, +0x0C = 1.0, +0x48).
    T2  the other 72 are DWORD/QWORD stores at +0xA0: they cover +0xA3 only as a field's top byte, so they can set
        +0xA3 = 1 only inside a 0x01xxxxxx value. Their bases are non-text-element: 7+ store through a polymorphic
        `this` (a vtable at +0, where a text element holds a float), and the Gi* group (0020E6C0 / 00863850 /
        00864330 / 00864860) writes a render scratch buffer as a contiguous +0x70..+0xA4 dword block.
  No traced store lands on a text-element base, so kind 1 is still never instantiated.

Controls:
  K1  the two ORACLE records exist and their `.out` files list 34 (SD-7) and 74 (SD-107) residue rows.
  K2  E4 control: a sibling draw method (00863850, GiColorRect) dispatches its render context at slot >= 31 (+0x138),
      the property that excludes the render context from GameApplication (31 slots).
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, SC = T.R, V.SZ, T.scan()
CAND = os.path.abspath(os.path.join(HERE, ".."))
SD7_OUT = os.path.join(CAND, "sd7-stored-app-pointer-0930", "sd7_app_pointer_sites.out")
SD107_OUT = os.path.join(CAND, "sd107-register-stores-0930", "sd107_register_stores.out")
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, " ".join(i.op_str.split()))).strip()


def has(pairs):
    bad = [("%08X" % a, txt(a)) for a, s in pairs if txt(a) != s]
    return not bad, bad


def slot(vt, k):
    return struct.unpack("<Q", R.at(vt + 8 * k, 8))[0]


def nslots(vt):
    n = 0
    while slot(vt, n) in SZ:
        if n and T.rtti_class(vt + 8 * n):
            break
        n += 1
    return n


# ---------------------------------------------------------------------------
# SD-7
# ---------------------------------------------------------------------------
print("=== SD-7: who calls GameApplication slot 15 (0017D1A0)? ===")

resid = [ln.split()[1:3] for ln in open(SD7_OUT) if ln.strip().startswith("RESIDUE")]
resid = [(int(f, 16), int(a, 16)) for f, a in resid]
check("K1", os.path.isdir(os.path.join(CAND, "sd7-stored-app-pointer-0930")) and len(resid) == 34,
      "ORACLE record sd7-stored-app-pointer-0930 lists %d residue dispatch sites (34)" % len(resid))

# R1 render context. PrimitiveRendererD3D11 is the object at the +0x78 dispatch; it has 45 slots so +0x78 = slot 15.
D3D11 = 0x00D86960
ok_r1 = (T.rtti_class(D3D11) == "PrimitiveRendererD3D11" and nslots(D3D11) >= 40 and slot(D3D11, 15) == 0x006CAB80)
# the five residue draw methods and the global carrier
R1 = {0x002143E0, 0x00214540, 0x00862D40, 0x00862EC0, 0x008651A0, 0x0020FF10}
ok_r1_sites = R1 <= {f for f, _ in resid}
check("S1", ok_r1 and ok_r1_sites,
      "render context = PrimitiveRendererD3D11 (%d slots, +0x78 = slot 15 = %08X); its draw methods are the residue"
      % (nslots(D3D11), slot(D3D11, 15)))

# K2 / E4 control: GiColorRect's draw 00863850 dispatches the SAME render context at slot >= 31 (+0x138)
ok_k2, bad = has([(0x00862DF9, "call qword ptr [r10 + 0x78]")])
# 00863850 reaches a +0x138 dispatch (slot 39) on its rdx; confirm such a dispatch exists in its body
big = False
for i in R.md.disasm(R.at(0x00863850, SZ.get(0x00863850, 0x400)), 0x00863850):
    if i.mnemonic in ("call", "jmp") and re.search(r"\+ 0x1[0-9a-f][0-9a-f]\]$", i.op_str):
        big = True
        break
check("K2", ok_k2 and big,
      "E4 control: the sibling draw 00863850 dispatches its render context at a slot >= 31 (+0x1xx), so the context is "
      "not a GameApplication (31 slots) %s" % (bad or ""))

# the global 01FC35F8 (0020FF10's base) holds the render context: written only by 00210320 from rdx, and 00210320 is
# called from GiVmax's slot-1 draw 001DB3D0 (001DB4AC), whose rdx/rsi is the render context.
givmax = [c for s in T.qword_sites(0x001DB3D0) for vt, c in [T.vtable_start(s)] if c]
ok_glob, bad = has([(0x0021037B, "mov qword ptr [rip + 0x1db3276], rdx"), (0x001DB4AC, "call 0x210320")])
stores = sorted((f, a) for f, a, kind in SC["refs"].get(0x01FC35F8, ()) if kind == "W")
check("S2", ok_glob and stores == [(0x00210320, 0x0021037B)] and "GiVmax" in givmax,
      "the 0020FF10 global 01FC35F8 holds the render context: its only writer 00210320 stores rdx, and 00210320 is "
      "called from GiVmax's slot-1 draw 001DB3D0 %s" % (bad or ""))

# R2 Steam. 001F3AE0's [rbx] is a Steam client-interface vtable; its allocator 001F3E10 calls SteamInternal_CreateInterface.
import pefile  # noqa: E402
pe = pefile.PE(R.b.EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
steam = None
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for i in e.imports:
        if i.address == 0x008C3188:
            steam = i.name
ok_steam, bad = has([(0x001F3BFC, "call qword ptr [rax + 0x78]"), (0x001F3AF2, "call qword ptr [rip + 0x6cf6a0]")])
check("S3", ok_steam and steam == b"SteamInternal_CreateInterface" and T.cstr(0x00903538) == "SteamClient017"
      and 0x001F3AE0 in {f for f, _ in resid},
      "001F3AE0's object is a Steam client interface (001F3E10 -> %s; string SteamClient017)" % (steam.decode() if steam else None))

# R3 Bullet. The second 008330A0 site is the same btCompoundShape; 008420F0 x2 is btBvhTriangleMeshShape (00837680's
# this); 00855B80 dispatches a btDiscreteDynamicsWorld's debug drawer; 00831380's rdi is a btConvexShape support pair.
ok_bt, bad = has([(0x0083323E, "call qword ptr [rax + 0x78]"), (0x00833235, "call qword ptr [rax + 0x78]"),
                  (0x0084CE5C, "call 0x831380"), (0x0084CD6E, "mov rcx, qword ptr [rbx + 0x30]"),
                  (0x0084CE61, "mov rcx, qword ptr [rbx + 0x38]")])
bt_world = slot(0x01CCF5E0, 4) == 0x00857820 and T.rtti_class(0x01CCF5E0) == "btDiscreteDynamicsWorld"
bt_cvx = T.rtti_class(0x01CCD440) == "btConvexShape" and nslots(0x01CCD440) == 20
check("S4", ok_bt and bt_world and bt_cvx and {0x00831380, 0x008330A0, 0x008420F0, 0x00855B80} <= {f for f, _ in resid},
      "Bullet group: 008330A0's 2nd site is the same btCompoundShape; 00831380's rdi is a btConvexShape support pair "
      "(0084CB30 passes [rbx+0x30]/[rbx+0x38]); 00855B80 drives a btDiscreteDynamicsWorld's debug drawer %s" % (bad or ""))

# R4 PPFX. The dispatched object's vtable, where typable, is a PPFX GPU interface. Pin the slot-15 entries.
ppfx = (slot(0x00DAF1B8, 15) == 0x00789CD0 and T.rtti_class(0x00DAF1B8) == "PPFX::IGPUEffect"
        and slot(0x00D9EA30, 15) == 0x00724C10 and T.rtti_class(0x00D9EA30) == "PPFX::IGPUDevice")
PPFX = {0x006F8740, 0x0070CF00, 0x0070CFA0, 0x00736D60, 0x007370A0, 0x00738840, 0x0073BD30, 0x0073D370, 0x0073DFA0,
        0x0073EA00, 0x0073F290, 0x007407E0, 0x0075D4E0, 0x0075DA10, 0x0077FFE0, 0x0078EAF0}
ppfx_range = all(0x006F0000 <= f < 0x00790000 for f in PPFX)
check("S5", ppfx and ppfx_range and PPFX <= {f for f, _ in resid},
      "PPFX group: dispatched objects are PPFX GPU interfaces (IGPUEffect +0x78 = %08X, IGPUDevice +0x78 = %08X); all "
      "%d holder functions lie in the PPFX range 006F0000-0079000" % (slot(0x00DAF1B8, 15), slot(0x00D9EA30, 15), len(PPFX)))

# R5 typed handle. 007AB5C0's object is a resolved resource handle (007AB1E0 checks handle types 2/8/9).
ok_h, bad = has([(0x007AB9E8, "call qword ptr [rdx + 0x78]"), (0x007AB1E4, "cmp cl, 2"),
                 (0x007AB1FD, "cmp cl, 8"), (0x007AB216, "cmp cl, 9")])
check("S6", ok_h and 0x007AB5C0 in {f for f, _ in resid},
      "007AB5C0's object is a resolved resource handle (007AB1E0 checks handle types 2/8/9 and indexes 02EAD5xx) %s" % (bad or ""))

# the register-call form: a `call/jmp reg` reaches slot 15 only if reg was loaded by `mov reg, [X + 0x78]`. (The
# rip-call form is covered by S8: a `call [rip -> slot]` reaches 0017D1A0 only if that slot holds it, and the only
# image qword equal to 0017D1A0 is its vtable entry.)
reg_from_78 = 0
n_reg = 0
for f in SZ:
    ins, idx, _ = V.body(f)
    for k, i in enumerate(ins):
        if i.mnemonic in ("call", "jmp") and re.fullmatch(r"r\w+", i.op_str):
            n_reg += 1
            fam = V.canon(i.op_str)
            for j in range(k - 1, max(-1, k - 30), -1):
                if fam in V.writes(ins[j]):
                    if ins[j].mnemonic == "mov" and re.search(r"qword ptr \[\w+ \+ 0x78\]$", ins[j].op_str):
                        reg_from_78 += 1
                    break
check("S7", reg_from_78 == 0 and n_reg > 500,
      "no register-target call (%d scanned) loads its target from [reg+0x78]; so with the memory form (S8) slot 15 is "
      "reachable only through a [vtable+0x78] dispatch" % n_reg)

# OPUS's frame: no direct caller of slot 15, and the only image qword naming it is its own vtable entry
direct = SC["calls"].get(0x0017D1A0) or ()
qsites = T.qword_sites(0x0017D1A0)
check("S8", len(direct) == 0 and qsites == [0x008C57D8] and slot(0x008C5760, 15) == 0x0017D1A0,
      "0017D1A0 has no direct call/jmp and the only image qword naming it is its own vtable slot (008C57D8); with all "
      "34 residue objects typed non-application, slot 15 is called nowhere - the +0x39 gate is set only by 001989D0")

# ---------------------------------------------------------------------------
# SD-107
# ---------------------------------------------------------------------------
print("=== SD-107: is text-element kind 1 ever instantiated? ===")

open74 = []
for ln in open(SD107_OUT):
    m = re.match(r"\s+S7 open\s+([0-9A-F]{8}) ([0-9A-F]{8}) (byte|word|dword|qword)\s+\[(\w+)\+(0x[0-9a-f]+)\]", ln)
    if m:
        open74.append((int(m.group(1), 16), int(m.group(2), 16), m.group(3), m.group(4), int(m.group(5), 16)))
check("K3", os.path.isdir(os.path.join(CAND, "sd107-register-stores-0930")) and len(open74) == 74,
      "ORACLE record sd107-register-stores-0930 lists %d open register stores (74)" % len(open74))

# T1: exactly two are BYTE stores directly at +0xA3; both are PPFX effect objects writing a 4-byte tuple.
byte_a3 = sorted((f, a) for f, a, wd, base, d in open74 if wd == "byte" and d == 0xA3)
check("T1a", byte_a3 == [(0x0077FFE0, 0x00780079), (0x00780590, 0x00780729)],
      "exactly two of the 74 write the kind byte directly (byte at +0xA3): %s"
      % " ".join("%08X@%08X" % x for x in byte_a3))

# both write +0xA0,+0xA1,+0xA2,+0xA3 as one 4-byte tuple (a colour/vector channel), in the PPFX range
ok_tuple = True
for f, a in byte_a3:
    ins = list(R.md.disasm(R.at(f, SZ[f]), f))
    base = re.match(r"byte ptr \[(\w+) \+ 0xa3\]", next(i for i in ins if i.address == a).op_str).group(1)
    disps = {int(m, 16) for i in ins for m in re.findall(r"byte ptr \[%s \+ (0xa[0-3])\]" % base, i.op_str)}
    ok_tuple = ok_tuple and {0xA0, 0xA1, 0xA2, 0xA3} <= disps and 0x0077 <= (f >> 16) <= 0x0078
check("T1b", ok_tuple,
      "both byte-+0xA3 writers store +0xA0..+0xA3 as one 4-byte tuple on a PPFX effect object (range 0077-0078), not a "
      "text-element kind (the builder 002B3C30 writes the kind as a lone byte and floats at +0x04/+0x0C/+0x48)")

# the text-element builder's layout, for contrast (a base with these can be a text element; no open store's base has it)
ok_builder, bad = has([(0x002B3C40, "mov byte ptr [rcx + 0xa3], 0"), (0x002B3D35, "mov dword ptr [rbx + 4], 0x41b80000"),
                       (0x002B3D41, "mov dword ptr [rbx + 0xc], 0x3f800000"), (0x002B3CF3, "movss dword ptr [rbx + 0x48], xmm1")])
check("T2", ok_builder,
      "the text element's builder 002B3C30 writes the kind as a lone byte at +0xA3 and floats 23.0/1.0 at +0x04/+0x0C "
      "and a float at +0x48 - the layout none of the 74 open bases carries %s" % (bad or ""))

# T3: the other 72 are DWORD/QWORD stores at +0xA0 (cover +0xA3 only as a top byte)
rest = [(f, a, wd, d) for f, a, wd, base, d in open74 if (wd, d) != ("byte", 0xA3)]
check("T3", len(rest) == 72 and all(wd in ("dword", "qword") and d == 0xA0 for f, a, wd, d in rest),
      "the other 72 are dword/qword stores at +0xA0: they reach +0xA3 only as a field's top byte (need a 0x01xxxxxx "
      "value), never a lone kind byte")

Q = collections.defaultdict(list)
for sec in pe.sections:
    data = sec.get_data()
    for off in range(0, len(data) - 7, 8):
        v = struct.unpack_from("<Q", data, off)[0]
        if v in SZ:
            Q[v].append(pe.OPTIONAL_HEADER.ImageBase + sec.VirtualAddress + off)


def classes(fn):
    return sorted({c for s in Q.get(fn, ()) for _, c in [T.vtable_start(s)] if c})


# T4: none of the 74 open-store functions is building a text element - none contains the builder's signature write of
# 23.0f (0x41b80000) to a base's +0x04, nor a lone-immediate kind store `mov byte [base + 0xa3], imm`.
textish = []
for f in {x[0] for x in open74}:
    for i in R.md.disasm(R.at(f, SZ[f]), f):
        if (i.mnemonic == "mov" and re.search(r"dword ptr \[\w+ \+ 4\], 0x41b80000$", i.op_str)) or \
           (i.mnemonic == "mov" and re.match(r"byte ptr \[\w+ \+ 0xa3\], 0x?[0-9a-f]+$", i.op_str)):
            textish.append((f, i.address))
check("T4", textish == [],
      "none of the 74 open-store functions builds a text element (no 23.0f write to +0x04, no immediate kind store at "
      "+0xA3): %d such writes found" % len(textish))

# T5: the Gi* render group writes a render scratch buffer (rdx), and the store functions are Gi draw methods by RTTI
GI = {0x0020E6C0, 0x00863850, 0x00864330, 0x00864860}
gi_named = {f: (classes(f)[0] if classes(f) else None) for f in GI}
check("T5", GI <= {f for f, _, _, _, _ in open74} and all(gi_named[f] and gi_named[f].startswith("Gi") for f in GI),
      "the Gi* group writes [rdx+0xA0] into a render scratch buffer: %s"
      % ", ".join("%08X=%s" % (f, gi_named[f]) for f in sorted(GI)))

print("FAILS %d" % fails)
