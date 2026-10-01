"""controller_pointers.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. PPhysicsCharacterControllerBullet
+0x130..+0x18F was one 96-byte span ('nothing is known beyond the extent'). Its constructor, copy, teardown and unregister code
read the first 32 bytes as four pointers with distinct ownership:

  Z  the constructor 00691120 - called by both descriptors' slot-10 constructors (00688570 at 0068858F for this class, 006895C0
     at 006895F3 for PPhysicsCharacterController; slot 10 sits beside destroy slot 00687F30 / 006890D0) - zeroes exactly +0x130 / +0x138 / +0x140 / +0x148 (00691130..00691145); the copy 00692540 copies
     exactly those four qwords (0069255C..00692586)
  O  the teardown 006A27C0 (run by both character-controller destroys):
       when +0x138 and +0x130 are set: [+0x130]'s vtable +0x78 with [+0x138], then +0x40 with 005C5310([+0x138]) = [[+0x138]+0x10]
       +0x148: vtable slot 0 with edx = 1 (the MSVC deleting-destructor call shape)
       +0x138: vtable slot 0 with edx = 0, then freed through 00584730 - destroyed in place, then its Phyre allocation freed
       +0x140: vtable slot 1 with edx = 1
       then nulls +0x148, +0x138, +0x140 - but not +0x130, which it never frees
  U  the unregister loop at 006A4790: [+0x130]'s vtable +0x78 with [+0x138] and +0x40 with [+0x140], then +0x130 = 0 (and +0xD8)
  So +0x130 is the object the controller is registered with (called, never freed: not owned); +0x138, +0x140 and +0x148 are owned.
  Which classes they are, and +0x150..+0x18F, are not established here.
  S  REGRESSION: the span is re-cut into four pointer rows and a 64-byte remainder, tiling kept (FAILS before)
Usage: python controller_pointers.py [--patch]
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
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
A = lambda pairs: all(at(a) == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
check("Z", A([(0x691130, ("mov", "qword ptr [rbx + 0x130], rax")), (0x691137, ("mov", "qword ptr [rbx + 0x138], rax")), (0x69113E, ("mov", "qword ptr [rbx + 0x140], rax")),
              (0x691145, ("mov", "qword ptr [rbx + 0x148], rax")), (0x69112E, ("xor", "eax, eax")), (0x68858F, ("call", "0x691120")), (0x6895F3, ("call", "0x691120")),
              (0x69255C, ("mov", "qword ptr [rdi + 0x130], rax")), (0x69256A, ("mov", "qword ptr [rdi + 0x138], rax")), (0x692578, ("mov", "qword ptr [rdi + 0x140], rax")),
              (0x692586, ("mov", "qword ptr [rdi + 0x148], rax"))]),
      "00691120 (called from the slot-10 constructors 00688570 / 006895C0) zeroes and 00692540 copies exactly the four qwords +0x130..+0x148")
slot = lambda i, dt, ct: struct.unpack_from("<Q", d, off(i))[0] == dt and struct.unpack_from("<Q", d, off(i) - 8)[0] == ct
check("Z2", slot(0xD70E30, 0x687F30, 0x688570) and slot(0xD71C40, 0x6890D0, 0x6895C0), "descriptor slots: destroy 00687F30 / 006890D0 beside constructors 00688570 / 006895C0")
check("O", A([(0x6A27C6, ("mov", "rdx, qword ptr [rcx + 0x138]")), (0x6A27D5, ("mov", "rcx, qword ptr [rcx + 0x130]")), (0x6A27E9, ("call", "qword ptr [rax + 0x78]")),
              (0x6A27FD, ("call", "0x5c5310")), (0x6A280C, ("call", "qword ptr [rbx + 0x40]")), (0x5C5310, ("mov", "rax, qword ptr [rcx + 0x10]")),
              (0x6A2814, ("mov", "rcx, qword ptr [rdi + 0x148]")), (0x6A2823, ("mov", "edx, 1")), (0x6A2828, ("call", "qword ptr [rax]")),
              (0x6A282A, ("mov", "rcx, qword ptr [rdi + 0x138]")), (0x6A2839, ("xor", "edx, edx")), (0x6A283B, ("call", "qword ptr [rax]")), (0x6A2844, ("call", "0x584730")),
              (0x6A2849, ("mov", "rcx, qword ptr [rdi + 0x140]")), (0x6A2858, ("mov", "edx, 1")), (0x6A285D, ("call", "qword ptr [rax + 8]")),
              (0x6A2862, ("mov", "qword ptr [rdi + 0x148], rax")), (0x6A2869, ("mov", "qword ptr [rdi + 0x138], rax")), (0x6A2870, ("mov", "qword ptr [rdi + 0x140], rax")),
              (0x687F45, ("call", "0x6a27c0")), (0x6890F7, ("call", "0x6a27c0"))]),
      "006A27C0: unregister from +0x130, delete +0x148 (slot 0, 1), destroy+free +0x138, delete +0x140 (slot 1, 1); +0x130 never freed")
check("U", A([(0x6A4790, ("mov", "rcx, qword ptr [rbx + 0x130]")), (0x6A479F, ("mov", "rdx, qword ptr [rbx + 0x138]")), (0x6A47A6, ("call", "qword ptr [rax + 0x78]")),
              (0x6A47B0, ("mov", "rdx, qword ptr [rbx + 0x140]")), (0x6A47BA, ("call", "qword ptr [rax + 0x40]")), (0x6A47BD, ("mov", "qword ptr [rbx + 0x130], rbp")),
              (0x6A47C4, ("mov", "qword ptr [rbx + 0xd8], rbp"))]),
      "the unregister loop calls +0x130's +0x78 / +0x40 with +0x138 / +0x140, then nulls +0x130")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/d3d11-element-release/controller_pointers.py"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"; T = "PPhysicsCharacterControllerBullet"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(was):
    P = ("TYPE RESOLVED", "PROVEN")
    return [[T, "0x0130", "8", "registeredWith130", "void*", "the object this controller is registered with: the teardown 006A27C0 and the unregister loop at 006A4790 call its vtable slots +0x78 (with +0x138) and +0x40 (with +0x140, or [[+0x138]+0x10]); the loop then nulls it. Never freed by the controller - not owned. Which object it is is not established", P[0], P[1], ev(was, "Z O U")],
            [T, "0x0138", "8", "ownedObject138", "void*", "owned: the teardown calls its vtable slot 0 with edx = 0 (destroy in place), then frees it through 00584730 (the Phyre allocator), and nulls it; passed to +0x130's slot +0x78 when unregistering. Its class is not established", P[0], P[1], ev(was, "Z O U")],
            [T, "0x0140", "8", "ownedObject140", "void*", "owned: the teardown calls its vtable slot 1 with edx = 1 (the MSVC deleting-destructor call shape) and nulls it; passed to +0x130's slot +0x40 when unregistering. Its class is not established", P[0], P[1], ev(was, "Z O U")],
            [T, "0x0148", "8", "ownedObject148", "void*", "owned: the teardown calls its vtable slot 0 with edx = 1 (the MSVC deleting-destructor call shape) and nulls it. Its class is not established", P[0], P[1], ev(was, "Z O")],
            [T, "0x0150", "64", "unobservedSpan0150", "u8[64]", "the class's last 64 bytes; not touched by the constructor path, copy, teardown or unregister loop read here, and the Phyre reflection schema recovered no member for them", "DISCOVERED", "UNKNOWN", ev(was, "Z O U")]]
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) == (T, "0x0130", "96") and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut("%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = {int(cells(l)[1], 16): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T}
ok = ([F.get(o, [0, 0, 0, ""])[3] for o in (0x130, 0x138, 0x140, 0x148, 0x150)] == ["registeredWith130", "ownedObject138", "ownedObject140", "ownedObject148", "unobservedSpan0150"]
      and sum(int(r[2]) for r in F.values()) == 0x190)
check("S", ok, "+0x130..+0x18F re-cut into four pointer rows and a 64-byte remainder; the type still tiles 0x190")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
