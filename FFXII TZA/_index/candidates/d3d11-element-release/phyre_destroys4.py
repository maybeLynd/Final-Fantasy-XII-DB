"""phyre_destroys4.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The last four Phyre destroy cells
('descriptor destroy slot +0x58, form not reduced') - the physics classes - and a transfer gap they expose.

  R  PPhysicsRigidBodyBullet +0x118 / +0x120 are the Bullet objects the materializer 0069FB10 builds (the page
     23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md already records them):
     +0x120 gets a 0x80-byte object constructed by 00832390, whose vtable's RTTI is btCompoundShape (0069FBA5..0069FBC9);
     +0x118 gets a 0x2C0-byte object constructed by 00852DB0, whose vtable's RTTI is btRigidBody (006A01A1..006A01C9). The store
     still carried them as 'unobservedSpan0118 u8[16] ... nothing is known'
  D  the destroys:
       PPhysicsRigidBodyBullet 00689FC0: calls +0x118's vtable slot 1 with edx = 1 and +0x120's slot 0 with edx = 1 (the MSVC
         deleting-destructor call shape), nulls +0x120, +0x118 and +0xC8, then 00691D40
       PPhysicsCharacterControllerBullet 00687F30: 006A27C0, then frees [+0x118] through 00584730 unless the pointer's bit 0 is set
       PPhysicsCharacterController 006890D0: 006A4670 on [+0xD8] when set, then the same two steps
       PPhysicsWorld 00688000: 006A49A0, 006A4710, then 00691DF0
  S  REGRESSION: the span is re-cut and the four cells reduced (FAILS before)
Usage: python phyre_destroys4.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
A = lambda pairs: all(at(a)[:2] == v for a, v in pairs)
def rtti(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]; td = struct.unpack_from("<I", d, off(col) + 12)[0] + B
    return d[off(td) + 16:off(td) + 90].split(b"\0")[0]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
r = (A([(0x69FBA5, ("lea", "edx, [rsi + 0x10]")), (0x69FBA8, ("lea", "ecx, [rdx + 0x70]")), (0x69FBAB, ("call", "0x85e680")), (0x69FBBF, ("call", "0x832390")),
        (0x69FBC9, ("mov", "qword ptr [rdi + 0x120], rax")), (0x6A01A1, ("mov", "edx, 0x10")), (0x6A01A6, ("mov", "ecx, 0x2c0")), (0x6A01AB, ("call", "0x85e680")),
        (0x6A01C1, ("call", "0x852db0")), (0x6A01C6, ("mov", "rsi, rax")), (0x6A01C9, ("mov", "qword ptr [rdi + 0x118], rsi"))])
     and rtti(at(0x8323B1)[2]) == b".?AVbtCompoundShape@@" and rtti(at(0x852DD4)[2]) == b".?AVbtRigidBody@@")
check("R", r, "+0x120 <- 0x80-byte btCompoundShape (00832390); +0x118 <- 0x2C0-byte btRigidBody (00852DB0)")
dd = (A([(0x689FD2, ("mov", "rcx, qword ptr [rdx + 0x118]")), (0x689FE1, ("mov", "edx, 1")), (0x689FE6, ("call", "qword ptr [rax + 8]")),
         (0x689FE9, ("mov", "rcx, qword ptr [rbx + 0x120]")), (0x689FF8, ("mov", "edx, 1")), (0x689FFD, ("call", "qword ptr [rax]")),
         (0x68A001, ("mov", "qword ptr [rbx + 0x120], rax")), (0x68A008, ("mov", "qword ptr [rbx + 0x118], rax")), (0x68A00F, ("mov", "qword ptr [rbx + 0xc8], rax")),
         (0x68A019, ("call", "0x691d40"))])
      and A([(0x687F45, ("call", "0x6a27c0")), (0x687F4B, ("mov", "rcx, qword ptr [rbx + 0x118]")), (0x687F5F, ("call", "0x584730"))])
      and A([(0x6890E2, ("mov", "rcx, qword ptr [rdx + 0xd8]")), (0x6890EE, ("call", "0x6a4670")), (0x6890F7, ("call", "0x6a27c0")),
             (0x6890FD, ("mov", "rcx, qword ptr [rbx + 0x118]")), (0x689111, ("call", "0x584730"))])
      and A([(0x688015, ("call", "0x6a49a0")), (0x68801D, ("call", "0x6a4710")), (0x688025, ("call", "0x691df0"))]))
check("D", dd, "the four physics destroys")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/phyre_destroys4.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PAGE = "23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was): return "RE-CUT 2026-09-28 (OPUS, %s R D; the page %s already recorded both). was %s. %s" % (REC, PAGE, was, EXE)
def cut(t, was):
    return [[t, "0x0118", "8", "rigidBody", "void*", "the Bullet btRigidBody this body materializes into: 0069FB10 allocates 0x2C0 bytes and constructs it with 00852DB0 (vtable RTTI btRigidBody), storing it here at 006A01C9; non-null means already materialized. The destroy 00689FC0 calls its vtable slot 1 with edx = 1 and nulls it", "TYPE RESOLVED", "PROVEN", ev(was)],
            [t, "0x0120", "8", "compoundShape", "void*", "the Bullet btCompoundShape built for the body: 0069FB10 allocates 0x80 bytes and constructs it with 00832390 (vtable RTTI btCompoundShape), storing it here at 0069FBC9. The destroy 00689FC0 calls its vtable slot 0 with edx = 1 and nulls it", "TYPE RESOLVED", "PROVEN", ev(was)]]
DT = {"PPhysicsRigidBodyBullet": "00689FC0: calls the btRigidBody's (+0x118) vtable slot 1 and the btCompoundShape's (+0x120) slot 0, each with edx = 1 (the MSVC deleting-destructor call shape), nulls +0x120, +0x118 and +0xC8, then 00691D40",
      "PPhysicsCharacterControllerBullet": "00687F30: 006A27C0, then frees [+0x118] through 00584730 unless the pointer's bit 0 is set",
      "PPhysicsCharacterController": "006890D0: 006A4670 on [+0xD8] when it is set, then 006A27C0 and the [+0x118] free as in PPhysicsCharacterControllerBullet",
      "PPhysicsWorld": "00688000: 006A49A0, 006A4710, then 00691DF0 (each on the world; not reduced further here)"}
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) == ("PPhysicsRigidBodyBullet", "0x0118", "16") and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] in DT and c[6].endswith("descriptor destroy slot +0x58, form not reduced"):
            c[6] = "~~%s~~ %s - READ 2026-09-28 (OPUS, %s D)" % (c[6], DT[c[0]], REC); tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
have = {int(r[1], 16): r for r in F if r[0] == "PPhysicsRigidBodyBullet"}
ok = (have.get(0x118, [0, 0, 0, ""])[3] == "rigidBody" and have.get(0x120, [0, 0, 0, ""])[3] == "compoundShape"
      and sum(int(r[2]) for r in have.values()) == int(T["PPhysicsRigidBodyBullet"][1], 16) and all(REC in T[t][6] for t in DT))
check("S", ok, "PPhysicsRigidBodyBullet +0x118 / +0x120 re-cut, tiling kept; four destroy cells reduced")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
