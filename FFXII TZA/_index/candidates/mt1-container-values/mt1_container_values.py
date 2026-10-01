"""mt1_container_values.py - MT-1: which container each MSVC _Tree instantiation is (FABLE, Claude Opus 5.5,
2026-09-26; first read by a delegated read-only pass, every cited instruction re-checked here).

  A1 the three maps in YEBIS's global state block are find-or-create caches over the PPFX GPU device's "Ref" creators.
     - +0xA8: the descent 0070D270 loads [rcx+0xA8] (0070D276). A miss calls 006F1E00 (0070D2F4), which calls device
       slot 66 ([r10+0x210], 006F1ED4) and inserts into [rbp+0xA8] (006F1F0C). The value is latched at +0xD8 (0070D325).
     - +0xB8: 0070DC90 loads [rcx+0xB8] (0070DC96). A miss calls 006F2240 (0070DD06), which calls slot 62
       ([r10+0x1F0], 006F2302) and inserts into [rcx+0xB8] (006F2285, 006F2336). The value is latched at +0xF0 (0070DD14).
     - +0xC8: the creator 006F1F60 calls slot 60 ([rax+0x1E0], 006F2015).
  A2 the device. Both creators read [block+0x20] (006F1E0E, 006F224F). The block's initialiser 006FF900 stores it at
     0070012F from 00727050 (0070012A). 00727050 reaches 007243E0 (007270A1), which installs vtable 00D9EA30
     (007243F4). That vtable's RTTI names PPFX::IGPUDevice.
  A3 the slots. Vtable slots 60, 62 and 66 are 00725E40, 00725FF0 and 00726700. Each body lea's its log tag: "Ref2D"
     (00725F09), "Ref3D" (007260B7), "RefRT" (007267CC). Each calls one constructor chain:
     - slot 60 builds an IGPUTexture: 007876E0 tail-jumps to 007875F0, which installs 00DADBF0 at 0078767A;
     - slot 62 builds an IGPUVolumeTexture: 00787B80, then 00787A90, which installs 00DADD50 at 00787B1A;
     - slot 66 builds an IGPUSurface: 00785A10, which tail-jumps to 007857D0 (it allocates, then calls 00785A60),
       and 00785A60 installs 00DAD3A8 at 00785A86.
     The chain is followed through direct call and jmp edges. The class names come from the RTTI of each installed
     vtable.
  A4 the +0xB8 map's entry wrapper 006DC9A0 has no static reference. There is no E8/E9 rel32 in .text, no 8-byte VA and
     no 4-byte RVA in the file. Control: the same search finds the +0xA8 wrapper 006DD570's one call (006CC01A).
  B1 instantiation B is a map<string, string>, the parsed YEBIS licence.
     - 0071D170 looks up named fields ("FeatureId", "BeginYear", ..., "MacAddress", "License") through 0071F000
       (0071D40A), and tests the result as an MSVC std::string (0071D40F cmp [rax+0x18], 0x10).
     - The payload destructor 0071EE70 frees two std::strings, at pair +0x20 and pair +0x00.
     - 0x20 header + 0x20 key + 0x20 value = the 0x60 node.
  C2 instantiation C, the PFramework static tree at 02EA5550 (MT-2), holds one 8-byte element per node. Its head is
     allocated by 00799B20 with 0x28 bytes (00799B32), the 0x20 header plus 8. Its tidy and subtree destroyer call
     only each other and free, so the element is trivially destroyed.
  C3 nothing fills or searches C. Image-wide, every rip-relative operand into 02EA5550..02EA555F sits in the static
     constructor 00169270 or the atexit destructor 008B7940. Its rotations and erase are called only by its own erase
     and tidy, which only the destructor reaches. Control: the same sweep finds hundreds of sites for the YEBIS block
     global 02EA0B70. So C's element type cannot be read from any use; the shipped code never uses the container.
  X1 correction: 006FF900 is the block's initialiser, not its teardown. 006DE950 allocates the 0xD40 block
     (006DE9E1), constructs it (006DE9F3), publishes it at 02EA0B70 (006DE9FB), then calls 006FF900 on it
     (006DEA1C/006DEA1F) and sign-tests the status (006DEA28). 006FF900 creates the device (A2).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size=16): return list(cs.disasm(d[off(a):off(a) + size], a))
def at(a):
    x = ins(a)[0]; return "%s %s" % (x.mnemonic, x.op_str)
def target(a):
    x = ins(a)[0]; m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return a + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
def cstr(v):
    o = off(v); return d[o:d.find(b"\0", o)].decode("latin-1")
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def rtti(vt):
    td = BASE + struct.unpack_from("<IIII", d, off(q(vt - 8)))[3]; return cstr(td + 16)
def calls(a, size): return {x.op_str for x in ins(a, size) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")}
def reaches(a, t, depth=3, size=0x100):
    """t is reached from a through direct call/jmp edges within `depth` hops."""
    front = {a}
    for _ in range(depth):
        front = {int(c, 16) for f in front for c in calls(f, size)}
        if t in front: return True
    return False
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
E = {0x70D276: "mov r10, qword ptr [rcx + 0xa8]", 0x70D2F4: "call 0x6f1e00", 0x6F1ED4: "call qword ptr [r10 + 0x210]",
     0x6F1F0C: "lea rcx, [rbp + 0xa8]", 0x70D325: "mov qword ptr [rbx + 0xd8], rcx",
     0x70DC96: "mov r10, qword ptr [rcx + 0xb8]", 0x70DD06: "call 0x6f2240", 0x6F2302: "call qword ptr [r10 + 0x1f0]",
     0x6F2285: "lea rdi, [rcx + 0xb8]", 0x6F2336: "mov rcx, rdi", 0x70DD14: "mov qword ptr [rbx + 0xf0], rcx",
     0x6F2015: "call qword ptr [rax + 0x1e0]"}
bad = {"%08X" % a: at(a) for a, s in E.items() if at(a) != s}
check("A1 +0xA8 -> slot 66 (0x210), +0xB8 -> slot 62 (0x1F0), +0xC8 -> slot 60 (0x1E0); inserts and latches", not bad, str(bad))
check("A2 [block+0x20] is set by the initialiser from 00727050, whose chain installs the PPFX::IGPUDevice vtable",
      at(0x6F1E0E) == "cmp qword ptr [rcx + 0x20], 0" and at(0x6F224F) == "mov r11, qword ptr [rcx + 0x20]"
      and at(0x70012A) == "call 0x727050" and at(0x70012F) == "mov qword ptr [rsi + 0x20], rax"
      and at(0x6FF981) == "mov rsi, rcx" and at(0x7270A1) == "call 0x7243e0" and target(0x7243F4) == 0xD9EA30
      and rtti(0xD9EA30) == ".?AVIGPUDevice@PPFX@@", rtti(0xD9EA30))
VT = 0xD9EA30
slots = {60: (0x725E40, 0x725F09, "Ref2D", 0x7876E0, 0x7875F0, 0x78767A, ".?AVIGPUTexture@PPFX@@"),
         62: (0x725FF0, 0x7260B7, "Ref3D", 0x787B80, 0x787A90, 0x787B1A, ".?AVIGPUVolumeTexture@PPFX@@"),
         66: (0x726700, 0x7267CC, "RefRT", 0x785A10, 0x785A60, 0x785A86, ".?AVIGPUSurface@PPFX@@")}
res = {}
for s, (body, tag, name, c1, c2, inst, cls) in slots.items():
    chain = hex(c1) in calls(body, 0x200) and reaches(c1, c2)
    res[s] = (q(VT + 8 * s) == body, cstr(target(tag)) == name, chain, rtti(target(inst)) == cls, rtti(target(inst)))
check("A3 slots 60/62/66 = Ref2D/Ref3D/RefRT, building IGPUTexture / IGPUVolumeTexture / IGPUSurface",
      all(all(v[:4]) for v in res.values()), str({k: v for k, v in res.items()}))
def rel_refs(t):
    hits = []; tb = [(BASE + va, rs, ro) for vs, va, rs, ro in secs][0]
    for op in (b"\xE8", b"\xE9"):
        k = d.find(op, tb[2])
        while 0 <= k < tb[2] + tb[1] - 5:
            a = tb[0] + k - tb[2]
            if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == t:
                x = ins(a)
                if x and x[0].address == a and x[0].size == 5: hits.append(a)
            k = d.find(op, k + 1)
    return hits
def abs_refs(t): return d.count(struct.pack("<Q", t)) + d.count(struct.pack("<I", t - BASE))
R0, R1 = rel_refs(0x6DC9A0), rel_refs(0x6DD570)
check("A4 the +0xB8 wrapper 006DC9A0 has no E8/E9, VA or RVA reference; control: 006DD570's call at 006CC01A is found",
      at(0x6DC9A7) == "jmp 0x70dc90" and R0 == [] and abs_refs(0x6DC9A0) == 0 and R1 == [0x6CC01A],
      "006DC9A0 rel %s abs %d; 006DD570 rel %s" % (R0, abs_refs(0x6DC9A0), ["%08X" % a for a in R1]))
leas = []
for x in ins(0x71D170, 2140):
    m = re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str)
    if x.mnemonic == "lea" and m:
        t = x.address + x.size + int(m.group(1), 16); o = off(t)
        if o and 0xD9B000 <= t < 0xD9C000: leas.append(cstr(t))
want = ["FeatureId", "BeginYear", "BeginMonth", "BeginDay", "EndYear", "EndMonth", "EndDay", "MacAddress", "License"]
check("B1 0071D170 looks up the licence fields by name and tests the result as a std::string",
      all(w in leas for w in want) and at(0x71D40A) == "call 0x71f000" and at(0x71D40F) == "cmp qword ptr [rax + 0x18], 0x10",
      str([w for w in want if w not in leas]))
D = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(0x71EE70, 0x80)}
check("B1 the payload destructor 0071EE70 frees two std::strings, at +0x20 and +0x00 (capacity +0x18, reset to 0xF)",
      D.get(0x71EE99) == "mov qword ptr [rdi + 0x18], 0xf" and D.get(0x71EECE) == "mov qword ptr [rbx + 0x18], 0xf"
      and D.get(0x71EE7E) == "lea rdi, [rcx + 0x20]" and D.get(0x71EE82) == "mov rbx, rcx")
check("X1 006FF900 runs on the freshly constructed and published block, and its status is sign-tested",
      at(0x6DE9E1) == "call 0x6da880" and at(0x6DE9F3) == "call 0x6ff5d0" and target(0x6DE9FB) == 0x2EA0B70
      and at(0x6DEA1C) == "mov rcx, rbx" and at(0x6DEA1F) == "call 0x6ff900" and at(0x6DEA28) == "jns 0x6dea6c")
A = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(0x799B20, 0x53)}
check("C2 instantiation C's node is 0x28 bytes: the static constructor 00169270 builds its head with 00799B20, which allocates 0x28",
      at(0x169297) == "call 0x799b20" and A.get(0x799B32) == "mov ecx, 0x28" and A.get(0x799B37) == "call 0x210ec0"
      and A.get(0x799B68) == "mov word ptr [rax + 0x18], 0x101")
check("C2 C's tidy and subtree destroyer free nodes without destroying a payload (their only callees: each other and free)",
      calls(0x79B0D0, 0x7E) == {"0x799b80", "0x210eb0"} and calls(0x799B80, 0x50) == {"0x799b80", "0x210eb0"})
def rip_sweep(lo, hi):
    """image-wide: every instruction in .text whose rip-relative operand lands in [lo, hi). Candidates are found by
    their disp32 for every trailing-immediate width, then decoded from each possible start and kept only if the
    decoded instruction ends where the candidate says and targets the range."""
    tb, trs, tro = [(BASE + va, rs, ro) for vs, va, rs, ro in secs][0]; hits = set()
    for k in range(tro, tro + trs - 4):
        disp = struct.unpack_from("<i", d, k)[0]
        for x in (0, 1, 2, 4):
            t = tb + (k - tro) + 4 + x + disp
            if lo <= t < hi:
                for s in range(k - 7, k):
                    a = tb + (s - tro); L = ins(a, 16)
                    if L and L[0].address == a and a + L[0].size == tb + (k - tro) + 4 + x and "rip" in L[0].op_str:
                        m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", L[0].op_str)
                        if m and lo <= a + L[0].size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) < hi: hits.add(a)
    return sorted(hits)
H = rip_sweep(0x2EA5550, 0x2EA5560); K = rip_sweep(0x2EA0B70, 0x2EA0B78)
own = [a for a in H if not (0x169270 <= a < 0x1692B3 or 0x8B7940 <= a < 0x8B79A0)]
check("C3 image-wide, only C's static constructor and its atexit destructor address the tree; control: the YEBIS block global has many",
      H and own == [] and len(K) >= 60, "candidate decodes: C %d (outside ctor/dtor %s); YEBIS block %d" % (len(H), ["%08X" % a for a in own], len(K)))
fam = {0x799BD0: (0x79BA10, 0x79BA10 + 978), 0x799C30: (0x79BA10, 0x79BA10 + 978), 0x79BA10: (0x79B930, 0x79B930 + 218),
       0x79B930: (0x8B7940, 0x8B79A0), 0x79B0D0: (0x79B930, 0x79B930 + 218), 0x799B80: (0x799B80, 0x799B80 + 0x50)}
stray = {"%08X" % f: ["%08X" % a for a in rel_refs(f) if not (lo <= a < hi) and not (0x79B0D0 <= a < 0x79B14E and f == 0x799B80)]
         for f, (lo, hi) in fam.items()}
check("C3 C's rotations, erase, erase-range, tidy and destroyer are called only inside the family and from the destructor",
      all(v == [] for v in stray.values()) and all(rel_refs(f) for f in fam), str(stray))
print("FAILS", fails)
sys.exit(1 if fails else 0)
