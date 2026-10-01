"""SWE2-AUDIT-SEM, independent static checks on SWE2-DATA's DD owner read batch 2 (959a77e13): does the database, BEFORE
the commit, already answer parts of SD-60, SD-61, SD-62, SD-66 and SD-67, and do the bytes support the rows' stated
limits?  Static reads of the certified image through retool.py; page texts read from git at 959a77e13^ (the parent).
Prints PASS/FAIL per check with a control; exit 1 on any FAIL.  Run from anywhere: python -B dd2_sem.py"""
import os, re, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402
R = T.R
PARENT = "959a77e13^"
DBP = "Database/FFXII TZA/"
fails = 0
def check(name, ok, detail=""):
    global fails
    fails += 0 if ok else 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (" - " + str(detail)) if detail != "" else ""))
def page(p):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s%s" % (PARENT, DBP, p)], capture_output=True).stdout.decode("utf-8", "replace")
def q(a):
    return struct.unpack("<Q", R.at(a, 8))[0]
SZ = T.sizes()
def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))
def rip(i):
    for op in i.operands:
        if op.type == 3 and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
C = T.scan()

print("== SD-60: what execute does with the GiBeginEff command, and whether the database already reads it")
ex = q(0x01CCFB78 + 8)
check("V1 GiBeginEff vtable 01CCFB78: slot 0 = 00864F30 (prepare), slot 1 = 00864E90 (execute)",
      q(0x01CCFB78) == 0x00864F30 and ex == 0x00864E90, "%08X %08X" % (q(0x01CCFB78), ex))
b = body(0x00864E90); txt = [(i.address, i.mnemonic, i.op_str) for i in b]
k = [n for n, t in enumerate(txt) if t[1] == "call" and t[2] == "0x210520"]
pre = " | ".join(t[2] for t in txt[k[0] - 3:k[0]]) if k else ""
check("V2 execute calls 00210520 with rcx = cmd+8, xmm1 = cmd+0x88, xmm2 = cmd+0x8C",
      bool(k) and "rcx, [rbx + 8]" in pre and "xmm1, dword ptr [rbx + 0x88]" in pre and "xmm2, dword ptr [rbx + 0x8c]" in pre, pre)
k30 = [n for n, t in enumerate(txt) if t[1] == "call" and t[2] == "qword ptr [rax + 0x30]"]
check("V3 execute passes rdx = cmd+0x48 to the device's vtable +0x30", bool(k30) and txt[k30[0] - 2][2] == "rdx, [rbx + 0x48]")
w = {rip(i): i.address for i in body(0x00210520) if rip(i) and i.operands[0].type == 3}
check("V4 00210520 stores the 64-byte block to 01FD3620..01FD365F and the floats to 01FD3660 (xmm1) / 01FD3664 (xmm2)",
      set(w) == {0x01FD3620, 0x01FD3630, 0x01FD3640, 0x01FD3650, 0x01FD3660, 0x01FD3664}, sorted("%08X" % x for x in w))
rd = sorted((f, a, kd) for g in range(0x01FD3620, 0x01FD3668) for (f, a, kd) in C["refs"].get(g, ()) if f != 0x00210520)
check("V5 readers of those globals exist: 0020EA50 takes the matrix 01FD3620, 00210230 reads 01FD3660 / 01FD3664",
      {(0x0020EA50, "lea"), (0x00210230, "R")} <= {(f, kd) for f, a, kd in rd}, ["%08X@%08X(%s)" % x for x in rd])
vif = page("17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md")
check("V6 at the parent, the VIF1/VU1 page already names them: the matrix at 01FD3620 and the Z bounds 01FD3664 / 01FD3660",
      "multiplies by the matrix at `01FD3620`" in vif and "upper float at `01FD3664`" in vif and "lower at\n       `01FD3660`" in vif)
dev = q(0x00D86960 + 0x30)
db = body(dev)
st = [i for i in db if i.mnemonic == "mov" and i.op_str.startswith("dword ptr [rcx +")]
check("V7 device vtable 00D86960 (PrimitiveRendererD3D11, BG-11 / Gi page 20e) slot +0x30 = 006CAF40: 16 dword copies to +0x10..+0x4C, then byte +0x208F3 = 1",
      dev == 0x006CAF40 and len(st) == 16 and any("0x208f3], 1" in i.op_str for i in db), "%08X, %d stores" % (dev, len(st)))
dyn = page("16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md"); gi = page("17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md")
check("V8 at the parent, the dyngeo page reads slot 6 006CAF40 and the Gi page maps +0x030 -> 006CAF40 and names the device",
      "`006CAF40` copies 16 dwords to `+0x10` and sets dirty `+0x208F3`" in dyn and "+0x030 006CAF40" in gi and "PrimitiveRendererD3D11" in gi)
check("C1 control: 00210520's store census is not empty-by-construction (the scan finds 00210520 writing 01FD3620)",
      any(f == 0x00210520 and kd == "W" for f, a, kd in C["refs"].get(0x01FD3620, ())))

print("== SD-61: PAnnotation +0x18 / +0x20 / +0x28")
ct = body(0x006B66C0)
check("A1 006B66C0 stores rdx -> +0x18, r8 -> +0x20, r9d -> +0x28",
      {"qword ptr [rcx + 0x18], rdx", "qword ptr [rcx + 0x20], r8", "dword ptr [rcx + 0x28], r9d"} <= {i.op_str for i in ct if i.mnemonic == "mov"})
lk = body(0x006B67F0)
check("A2 006B67F0 (BL-5's find-by-key) reads +0x18 and compares it with its rdx key", any(i.op_str == "qword ptr [rax + 0x18], rdx" and i.mnemonic == "cmp" for i in lk))
sites = sorted(a for f, a in C["calls"].get(0x006B66C0, ()))
formed = {"rdx": 0, "r8": 0, "r9": 0}; allthree = 0
for s in sites:
    f = T.func_of(s, SZ); ins = body(f); n = [j for j, i in enumerate(ins) if i.address == s][0]
    win = ins[max(0, n - 12):n]; got = set()
    for i in win:
        o = i.op_str.split(",")[0].strip()
        if i.mnemonic in ("mov", "lea", "xor", "movzx", "or", "and") and o in ("rdx", "edx", "r8", "r8d", "r9", "r9d"):
            got.add({"edx": "rdx", "r8d": "r8", "r9d": "r9"}.get(o, o))
    for r in got:
        formed[r] += 1
    allthree += (len(got) == 3)
check("A3 the row says none of the 70 sites forms the arguments within 12 instructions; counted here per register",
      len(sites) == 70, "sites %d; rdx formed at %d, r8 at %d, r9 at %d; all three at %d" % (len(sites), formed["rdx"], formed["r8"], formed["r9"], allthree))
check("A4 so the row's 'none of its 70 call sites forms those arguments within the 12 instructions' does not hold", allthree > 0, allthree)
mr = page("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md")
check("A5 at the parent, BL-5 on the member-registration page names the +0x18 reader (key compare) and the WriteMask key",
      "key compare at annotation `+0x18`" in mr and "\"WriteMask\"" in mr)
check("C2 control: the per-site window sees the first site's key lea 02CF8570 at 005B4FE3",
      any(i.address == 0x005B4FE3 and rip(i) == 0x02CF8570 for i in body(0x005B4E00)))

print("== SD-62: the two non-type elements 01F2E330 / 01F2E780")
for acc, el, guard, dtor in ((0x006373D0, 0x01F2E330, 0x02CF94EC, 0x008AF490), (0x00637440, 0x01F2E780, 0x02CF9524, 0x008AFDE0)):
    ins = body(acc); calls = [i.op_str for i in ins if i.mnemonic == "call"]
    leas = [rip(i) for i in ins if i.mnemonic == "lea"]
    check("R1 %08X returns %08X; its cold path is _Init_thread_header / atexit(%08X) / _Init_thread_footer on guard %08X, no constructor"
          % (acc, el, dtor, guard), calls == ["0x8092fc", "0x808b90", "0x80929c"] and el in leas and dtor in leas and guard in leas, calls)
cd = page("22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md")
ap = page("22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md")
check("R2 at the parent, the database already calls both registries: 006373D0's return is the class registry list head, 00637440 fetches the registry object",
      "walks the registry list (`006373D0` → `+0x10`" in cd and "`call 00637440` fetches the registry object" in ap and "| `00637440` | registry root accessor" in mr)

print("== SD-66: the attach through 02CF8580")
ins = body(0x006349B0)
k = [n for n, i in enumerate(ins) if i.address == 0x00634AA3][0]
check("D1 006349B0: rsi = lea 02CF8580, then rax = [02CF8580]; call [rax+0x40] with rcx = rsi (the object itself)",
      any(i.address == 0x006349CC and rip(i) == 0x02CF8580 and i.op_str.startswith("rsi") for i in ins)
      and rip(ins[k - 1]) == 0x02CF8580 and ins[k - 1].op_str.startswith("rax") and ins[k].op_str == "qword ptr [rax + 0x40]"
      and "rcx, rsi" in [i.op_str for i in ins[k - 5:k]])
col = q(0x00D56ED0 - 8); td = struct.unpack("<I", R.at(col + 12, 4))[0] + 0x120000
name = T.cstr(td + 16, 120)
check("D2 the object's vtable 00D56ED0 (loaded at 00163EF9) is RTTI PClassDescriptorWithoutDefaultConstructor<PClassDescriptorDynamic>: a class descriptor",
      name == ".?AV?$PClassDescriptorWithoutDefaultConstructor@VPClassDescriptorDynamic@Phyre@@@Phyre@@"
      and any(a == 0x00163EF9 for f, a, kd in C["refs"].get(0x00D56ED0, ())), name)
check("D3 at the parent, the member-registration page already says 006349B0 registers members on 'owner class descriptor 02CF8580' via [owner_vftable+0x40]",
      "owner class descriptor `02CF8580`" in mr and "`call [owner_vftable+0x40]`" in mr)

print("== SD-67: m_streamBindings")
ins = body(T.func_of(0x005E6860, SZ)); k = [n for n, i in enumerate(ins) if i.address == 0x005E6860][0]
w = {i.op_str.split(",")[0]: i.op_str.split(",")[1].strip() for i in ins[k - 10:k] if i.op_str.startswith("dword ptr [rsp +")}
check("S1 005E6860 -> 00632A10: a5 offset 0x38, a7 kind 4 (PSharray, UQ-281), a8 element size 8",
      w.get("dword ptr [rsp + 0x20]") == "0x38" and w.get("dword ptr [rsp + 0x30]") == "4" and w.get("dword ptr [rsp + 0x38]") == "8", w)
check("S2 at the parent, the member-registration page (section 20, OPUS 2026-09-26/27) already adjudicates it: native +0x38, 16 bytes, PSharray of pointers",
      "**`m_streamBindings`, the adjudicated field.** Native `+0x38`, 16 bytes, `PSharray<PMeshInstanceSegmentStreamBinding*>`" in mr)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
