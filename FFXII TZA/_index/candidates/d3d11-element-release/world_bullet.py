"""world_bullet.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. PPhysicsWorldBullet +0x60..+0xE7 was one
136-byte span ('nothing is known beyond the extent'). The world's Bullet creator 006A0310 and its teardown 006A5B10 / destructor
00691DF0 read most of it:

  C  006A0310 builds the Bullet world, by vtable RTTI. Its callers pass the world: 0069F10C (right after the rigid-body
     materializer 0069FB10, when [world+0x60] is still null) and 00698CB4; it refuses when +0x60 or +0x68 is already set:
       +0x68 <- 00838600 on a 0xB0-byte 0085E680 allocation, RTTI btAxisSweep3 (006A036E..006A03FB)
       +0x70 <- an 8-byte 00210EC0 allocation whose vtable is btGhostPairCallback's (006A040E..006A042C); then registered through
             +0x68's vtable +0x48 and the result's +0x70 (006A0435..006A0449)
       +0x60 <- 00854980 on a 0x180-byte 0017D260 allocation, RTTI btDiscreteDynamicsWorld, given +0x68 as its broadphase
             (006A045B..006A0492)
       +0xB8 <- +0x08 of the static 02E4AFF0 that 0069E6F0 returns (006A04FA / 006A0501), which then sizes the +0x98 and +0xA8
             arrays (006A5450 at 006A050E, edx = +0xB8 for the second)
  G  0069E6F0 is a thread-safe static getter: it returns 02E4AFF0, built once by 00691240 under the guard 02E4B090 (atexit
     008B3BE0); 006A0310 also passes that static's +0x18 / +0x20 / +0x28 to 00854980. Its type is not in the store. (Corrected
     2026-09-28: the first publication, 1f76f608e, called it 'the world description' - an unverified label.)
  T  006A5B10: +0x60 destroyed in place (vtable slot 0, edx 0) then freed through 00584730; +0x68 and +0x70 deleted (slot 0, edx
     1, the MSVC deleting-destructor call shape); the +0x98 / +0xA0 and +0xA8 / +0xB0 arrays freed unless bit 31 of the count
  D  00691DF0 (the class destructor): 006A5B10, then the +0xD0 / +0xD8, +0xC0 / +0xC8, +0xA8 / +0xB0, +0x98 / +0xA0 arrays freed
     unless bit 31, each pair nulled
  Not read here: +0x78..+0x97, the four dwords after the counts, +0xBC, +0xE0..+0xE7, and the arrays' elements.
  Q  the generator equals the store for every re-cut row;  W  no row keeps the unverified 'world description' label (FAILS on
     1f76f608e)
  S  REGRESSION: the span is re-cut, tiling kept (FAILS before)
Usage: python world_bullet.py [--patch]
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
def ctor_rtti(f, k=40):
    for x in list(cs.disasm(d[off(f):off(f) + 0x200], f))[:k]:
        m = re.search(r"rip \+ (0x[0-9a-f]+)", x.op_str)
        if m and x.mnemonic == "lea":
            try:
                r = rtti(x.address + x.size + int(m.group(1), 16))
                if r.startswith(b".?AV"): return r
            except Exception: pass
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
c = (A([(0x6A032A, ("cmp", "qword ptr [rcx + 0x60], 0")), (0x6A0335, ("cmp", "qword ptr [rcx + 0x68], 0")), (0x69F102, ("cmp", "qword ptr [rdi + 0x60], 0")), (0x69F10C, ("call", "0x6a0310")), (0x698CB4, ("call", "0x6a0310")), (0x6A036E, ("mov", "ecx, 0xb0")), (0x6A0373, ("call", "0x85e680")), (0x6A03F5, ("call", "0x838600")), (0x6A03FB, ("mov", "qword ptr [rbx + 0x68], rax")),
        (0x6A040E, ("mov", "ecx, 8")), (0x6A0413, ("call", "0x210ec0")), (0x6A0429, ("mov", "qword ptr [rax], rcx")), (0x6A042C, ("mov", "qword ptr [rbx + 0x70], rax")),
        (0x6A043C, ("call", "qword ptr [rax + 0x48]")), (0x6A0442, ("mov", "rdx, qword ptr [rbx + 0x70]")), (0x6A0449, ("call", "qword ptr [r8 + 0x70]")),
        (0x6A045B, ("mov", "ecx, 0x180")), (0x6A0460, ("call", "0x17d260")), (0x6A0481, ("mov", "r8, qword ptr [rbx + 0x68]")), (0x6A048C, ("call", "0x854980")),
        (0x6A0492, ("mov", "qword ptr [rbx + 0x60], rax")), (0x6A04FA, ("mov", "edx, dword ptr [rdi + 8]")), (0x6A0501, ("mov", "dword ptr [rbx + 0xb8], edx")),
        (0x6A0507, ("lea", "rcx, [rbx + 0x98]")), (0x6A050E, ("call", "0x6a5450")), (0x6A0513, ("lea", "rcx, [rbx + 0xa8]")), (0x6A051A, ("mov", "edx, dword ptr [rbx + 0xb8]"))])
     and rtti(at(0x6A0422)[2]) == b".?AVbtGhostPairCallback@@" and ctor_rtti(0x838600) == b".?AVbtAxisSweep3@@" and ctor_rtti(0x854980) == b".?AVbtDiscreteDynamicsWorld@@")
g = (at(0x69E737)[:2] == ("lea", "rbx, [rip + 0x27ac8b2]") and at(0x69E737)[2] == 0x2E4AFF0 and at(0x69E741)[:2] == ("call", "0x691240")
     and at(0x69E764)[2] == 0x2E4AFF0 and at(0x69E72E)[2] == 0x2E4B090 and at(0x6A0340)[:2] == ("call", "0x69e6f0") and at(0x6A0345)[:2] == ("mov", "rdi, rax")
     and A([(0x6A0474, ("mov", "rcx, qword ptr [rdi + 0x18]")), (0x6A047D, ("mov", "r9, qword ptr [rdi + 0x28]")), (0x6A0485, ("mov", "rdx, qword ptr [rdi + 0x20]"))]))
check("G", g, "0069E6F0 returns the static 02E4AFF0 (00691240 under guard 02E4B090); its +0x08 / +0x18 / +0x20 / +0x28 feed 006A0310")
check("C", c, "006A0310: +0x68 btAxisSweep3, +0x70 btGhostPairCallback, +0x60 btDiscreteDynamicsWorld, +0xB8 the array size")
t = A([(0x6A5B1F, ("mov", "rcx, qword ptr [rcx + 0x60]")), (0x6A5B2B, ("xor", "edx, edx")), (0x6A5B2D, ("call", "qword ptr [rax]")), (0x6A5B33, ("call", "0x584730")),
       (0x6A5B3C, ("mov", "rcx, qword ptr [rbx + 0x68]")), (0x6A5B48, ("mov", "edx, 1")), (0x6A5B4D, ("call", "qword ptr [rax]")),
       (0x6A5B4F, ("mov", "rcx, qword ptr [rbx + 0x70]")), (0x6A5B5F, ("mov", "edx, 1")), (0x6A5B64, ("call", "qword ptr [rax]")),
       (0x6A5B6A, ("mov", "eax, dword ptr [rbx + 0x98]")), (0x6A5B74, ("mov", "rcx, qword ptr [rbx + 0xa0]")), (0x6A5B89, ("call", "0x584730")),
       (0x6A5B9B, ("mov", "eax, dword ptr [rbx + 0xa8]")), (0x6A5BA5, ("mov", "rcx, qword ptr [rbx + 0xb0]")), (0x6A5BBA, ("call", "0x584730"))])
check("T", t, "006A5B10: destroy+free +0x60, delete +0x68 / +0x70, free the +0xA0 / +0xB0 arrays")
dd = A([(0x691E07, ("call", "0x6a5b10")), (0x691E0D, ("mov", "eax, dword ptr [rbx + 0xd0]")), (0x691E1C, ("mov", "rcx, qword ptr [rbx + 0xd8]")),
        (0x691E3D, ("mov", "eax, dword ptr [rbx + 0xc0]")), (0x691E4C, ("mov", "rcx, qword ptr [rbx + 0xc8]")),
        (0x691E6B, ("mov", "eax, dword ptr [rbx + 0xa8]")), (0x691E7A, ("mov", "rcx, qword ptr [rbx + 0xb0]")),
        (0x691E99, ("mov", "eax, dword ptr [rbx + 0x98]")), (0x691EA8, ("mov", "rcx, qword ptr [rbx + 0xa0]"))])
check("D", dd, "00691DF0: 006A5B10, then the four counted arrays")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/d3d11-element-release/world_bullet.py"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"; TN = "PPhysicsWorldBullet"
def cells(l): return l.rstrip("\r\n").split("\t")
def cut(was):
    ev = lambda tag: "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
    P = ("TYPE RESOLVED", "PROVEN"); U = ("DISCOVERED", "UNKNOWN")
    R = [[TN, "0x0060", "8", "dynamicsWorld", "void*", "the Bullet btDiscreteDynamicsWorld: 006A0310 constructs it with 00854980 (vtable RTTI btDiscreteDynamicsWorld) on a 0x180-byte 0017D260 allocation, passing +0x68 as its broadphase; 006A5B10 destroys it in place (vtable slot 0, edx 0) and frees it through 00584730", P[0], P[1], ev("C T")],
         [TN, "0x0068", "8", "broadphase", "void*", "the Bullet btAxisSweep3 broadphase: 006A0310 constructs it with 00838600 (vtable RTTI btAxisSweep3) on a 0xB0-byte 0085E680 allocation; 006A5B10 deletes it (vtable slot 0, edx 1)", P[0], P[1], ev("C T")],
         [TN, "0x0070", "8", "ghostPairCallback", "void*", "a btGhostPairCallback (an 8-byte 00210EC0 allocation holding only that vtable, by RTTI) that 006A0310 registers through the broadphase (+0x68's vtable +0x48, then the result's +0x70); 006A5B10 deletes it (vtable slot 0, edx 1)", P[0], P[1], ev("C T")],
         [TN, "0x0078", "32", "unobservedSpan0078", "u8[32]", "not read by the creator, teardown or destructor read here", U[0], U[1], ev("C T D")]]
    for c0, a0 in ((0x98, 0xA0), (0xA8, 0xB0)):
        R += [[TN, "0x%04X" % c0, "4", "arrayCount%02X" % c0, "uint32", "the element count of the array at +0x%02X (bit 31 set keeps it): 006A0310 sizes it from +0xB8 through 006A5450; 006A5B10 and 00691DF0 free the array through 00584730 unless bit 31 is set, and zero this" % a0, P[0], P[1], ev("C T D")],
              [TN, "0x%04X" % (c0 + 4), "4", "unobservedSpan%04X" % (c0 + 4), "u8[4]", "four bytes after the count; not read here", U[0], U[1], ev("T D")],
              [TN, "0x%04X" % a0, "8", "array%02X" % a0, "void*", "a heap array freed through 00584730 by 006A5B10 and 00691DF0 (count at +0x%02X) and nulled; its elements are not read here" % c0, P[0], P[1], ev("T D")]]
    R += [[TN, "0x00B8", "4", "arraySizeB8", "uint32", "the size 006A0310 copies from +0x08 of the static 02E4AFF0 that 0069E6F0 returns (006A0501), and sizes the +0x98 and +0xA8 arrays with (006A5450). What that static is is not established", P[0], P[1], ev("C")],
          [TN, "0x00BC", "4", "unobservedSpan00BC", "u8[4]", "four bytes after the size; not read here", U[0], U[1], ev("C")]]
    for c0, a0 in ((0xC0, 0xC8), (0xD0, 0xD8)):
        R += [[TN, "0x%04X" % c0, "4", "arrayCount%02X" % c0, "uint32", "the element count of the array at +0x%02X (bit 31 set keeps it): 00691DF0 frees the array through 00584730 unless bit 31 is set, and zeroes this" % a0, P[0], P[1], ev("D")],
              [TN, "0x%04X" % (c0 + 4), "4", "unobservedSpan%04X" % (c0 + 4), "u8[4]", "four bytes after the count; not read here", U[0], U[1], ev("D")],
              [TN, "0x%04X" % a0, "8", "array%02X" % a0, "void*", "a heap array freed through 00584730 by 00691DF0 (count at +0x%02X) and nulled; its elements are not read here" % c0, P[0], P[1], ev("D")]]
    R += [[TN, "0x00E0", "8", "unobservedSpan00E0", "u8[8]", "the class's last eight bytes; not read here", U[0], U[1], ev("C T D")]]
    return R
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c_ = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c_[0], c_[1], c_[2]) == (TN, "0x0060", "136") and c_[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut("%s %s (%s)" % (c_[3], c_[4], c_[5][:200]))]; continue
        if c_[0] == TN and c_[1] == "0x00B8" and "world description" in c_[5]:
            new = {r[1]: r for r in cut("")}["0x00B8"]; c_[5] = new[5]
            c_[8] += " || LABEL CORRECTED 2026-09-28 (OPUS, %s G): 'the world description' was unverified; the source is the static 02E4AFF0 that 0069E6F0 returns" % REC
            l = "	".join(c_) + e
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = {int(cells(l)[1], 16): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == TN}
ok = ([F.get(o, [0, 0, 0, ""])[3] for o in (0x60, 0x68, 0x70, 0xA0, 0xB8, 0xD8)] == ["dynamicsWorld", "broadphase", "ghostPairCallback", "arrayA0", "arraySizeB8", "arrayD8"]
      and sum(int(r[2]) for r in F.values()) == 0xE8)
gen = {r[1]: r for r in cut("")}
check("Q", all(o in F and F[o][3:6] == gen["0x%04X" % o][3:6] for o in (int(k, 16) for k in gen)),
      "the --patch generator equals the store (name, ctype, meaning) for every re-cut row - an amendment made to the rows and not here fails")
check("W", all("world description" not in r[5] for r in F.values()), "no row calls the 02E4AFF0 static a world description")
check("S", ok, "+0x60..+0xE7 re-cut; the type still tiles 0xE8")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
