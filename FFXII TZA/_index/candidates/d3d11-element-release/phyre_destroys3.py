"""phyre_destroys3.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Seven more Phyre destroy cells
('descriptor destroy slot +0x58, form not reduced') read; two of them settle unregistered spans.

  E  PShadowCaster embeds a PSamplerStateD3D11 at +0x58 (0x58..0x7F). Construct: 006C0EB0 (reached from descriptor slot 10
     006C0860) calls 00615CD0 on +0x58 - the same body as PSamplerStateD3D11's own slot-10 constructor 006135E0 (005DC400, then
     +0x20 = 0) - and then, while the sampler's m_flags (+0x1C) bit 7 is clear, sets m_minFilter / m_magFilter = 1, m_wrapS /
     m_wrapT = 2 and m_flags bit 6. Destroy: 006C0B50 calls 006167C0 on +0x58 - the same body as PSamplerStateD3D11's destroy
     006132E0 (release +0x20, clear m_flags bit 7, 0016D6A0) - then frees m_splits' array (+0x18, count +0x10) unless bit 31
  L  PLODGroup 006C4B70: 006C5200 on m_levels (+0x50) - count at +0, array at +8, each 0x38-byte PLODLevel destroyed by 006C5320,
     then the array freed - and then frees the heap array at +0x28 (count +0x20) through 00584730 unless the count's bit 31 is set,
     nulling both. So the gap +0x20..+0x2F is a counted array like the D3D11 element arrays; its elements are not read
  D  the other five: POctreeData 008775E0 unlinks m_next / m_prev (+0x20 / +0x28), self-links them and nulls m_octree;
     PScriptableComponent 0063FC60 calls vtable slot 0 of the object at (argument - 8) with edx = 0 (null-safe);
  A  (2026-09-28 correction) 00639A60 hands the construct slot +0x50 the bare buffer and the destroy slot +0x58 buffer + [desc+0xF8]
     (00639B15 / 00639B19, 00639B20, 00639B78, 00639B9A), so the -8 undoes that adjustment: the object starts at argument - 8 and
     the store's rows are object-relative (PAnimationController's construct 005A1230 writes its vtable at the buffer's +0). It was
     first read as "the instance is the +0x08 sub-object of a polymorphic object", which misplaces the store's coordinates; PTriggerReceiverComponent 006CDD30 frees [+0x40] and [+0x28] through 00584730 unless
     the pointer's bit 0 is set, then the PComponent destructor 006AAA50; PInstancesComponent 006ADC20 frees the instances array
     (+0x20, count +0x18) unless bit 31, then 006AAA50; PBlendableAnimationSource 005A1110 stores 00D312F0 - the vtable whose RTTI
     is PAnimation::PAnimationHierarchyNode - into +0x10, +0x38 and +0x58, the three inline controllers
  S  REGRESSION: the seven cells are reduced, the two spans re-cut, PShadowCaster's constructor cell filled (FAILS before)
Usage: python phyre_destroys3.py [--patch]
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
def ops(a, k): return [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + 0x60], a) if x.mnemonic != "nop"][:k]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
same_ctor = ops(0x615CD9, 3) == [("call", "0x5dc400"), ("mov", "rax, rbx"), ("mov", "qword ptr [rbx + 0x20], 0")] and A([(0x613603, ("call", "0x5dc400")), (0x613608, ("mov", "qword ptr [rbx + 0x20], 0"))])
same_dtor = (A([(0x6167D2, ("mov", "rcx, qword ptr [rcx + 0x20]")), (0x6167DE, ("call", "qword ptr [rax + 0x10]")), (0x6167EA, ("and", "dword ptr [rbx + 0x1c], 0xffffff7f")), (0x6167F9, ("jmp", "0x16d6a0"))])
             and A([(0x6132F2, ("mov", "rcx, qword ptr [rdx + 0x20]")), (0x6132FE, ("call", "qword ptr [rax + 0x10]")), (0x613309, ("and", "dword ptr [rbx + 0x1c], 0xffffff7f")), (0x613313, ("call", "0x16d6a0"))]))
slot = struct.unpack_from("<Q", d, off(0xD50140) - 8)[0] == 0x6135E0 and struct.unpack_from("<Q", d, off(0xD50140))[0] == 0x6132E0
e = (same_ctor and same_dtor and slot and A([(0x6C087F, ("call", "0x6c0eb0")), (0x6C0EE9, ("lea", "rbx, [rdi + 0x58]")), (0x6C0EF5, ("call", "0x615cd0")),
                                             (0x6C0F04, ("mov", "byte ptr [rbx], 1")), (0x6C0F11, ("mov", "byte ptr [rbx + 1], 1")), (0x6C0F1F, ("mov", "byte ptr [rbx + 2], 2")),
                                             (0x6C0F2D, ("mov", "byte ptr [rbx + 3], 2")), (0x6C0F3D, ("or", "ecx, 0x40")),
                                             (0x6C0B62, ("lea", "rcx, [rdx + 0x58]")), (0x6C0B66, ("call", "0x6167c0")), (0x6C0B78, ("mov", "rcx, qword ptr [rbx + 0x18]")), (0x6C0B81, ("call", "0x584730"))]))
check("E", e, "PShadowCaster +0x58 is built by the sampler's constructor body and destroyed by its destructor body")
l = A([(0x6C4B82, ("lea", "rcx, [rdx + 0x50]")), (0x6C4B86, ("call", "0x6c5200")), (0x6C4B8C, ("mov", "ecx, dword ptr [rbx + 0x20]")), (0x6C4B9E, ("cmp", "ecx, 1")),
       (0x6C4BA3, ("mov", "rcx, qword ptr [rbx + 0x28]")), (0x6C4BAC, ("call", "0x584730")), (0x6C4BB3, ("mov", "qword ptr [rbx + 0x28], rax")), (0x6C4BB7, ("mov", "dword ptr [rbx + 0x20], eax")),
       (0x6C5221, ("mov", "edx, dword ptr [rcx]")), (0x6C5232, ("mov", "rbp, qword ptr [rcx + 8]")), (0x6C5247, ("call", "0x6c5320")), (0x6C524D, ("add", "rbx, 0x38")), (0x6C525A, ("call", "0x584730"))])
check("L", l, "PLODGroup: m_levels destroyed at stride 0x38, then the +0x28 array (count +0x20) freed")
vt = 0xD312F0; col = struct.unpack_from("<Q", d, off(vt - 8))[0]; td = struct.unpack_from("<I", d, off(col) + 12)[0] + B
rt = d[off(td) + 16:off(td) + 80].split(b"\0")[0] == b".?AVPAnimationHierarchyNode@PAnimation@Phyre@@"
dd = (A([(0x8775E0, ("mov", "rax, qword ptr [rdx + 0x20]")), (0x8775E4, ("mov", "rcx, qword ptr [rdx + 0x28]")), (0x8775E8, ("mov", "qword ptr [rcx + 0x20], rax")),
         (0x8775EC, ("mov", "qword ptr [rax + 0x28], rcx")), (0x8775F2, ("mov", "qword ptr [rdx + 0x20], rdx")), (0x8775F6, ("mov", "qword ptr [rdx + 0x28], rdx")), (0x8775FA, ("mov", "qword ptr [rdx], 0"))])
      and A([(0x63FC66, ("lea", "rcx, [rdx - 8]")), (0x63FC6D, ("cmove", "rcx, rax")), (0x63FC71, ("xor", "edx, edx")), (0x63FC76, ("call", "qword ptr [rax]"))])
      and A([(0x6CDD42, ("mov", "rcx, qword ptr [rdx + 0x40]")), (0x6CDD53, ("call", "0x584730")), (0x6CDD59, ("mov", "rcx, qword ptr [rbx + 0x28]")), (0x6CDD6A, ("call", "0x584730")), (0x6CDD73, ("call", "0x6aaa50"))])
      and A([(0x6ADC32, ("mov", "eax, dword ptr [rdx + 0x18]")), (0x6ADC3E, ("mov", "rcx, qword ptr [rdx + 0x20]")), (0x6ADC47, ("call", "0x584730")), (0x6ADC58, ("call", "0x6aaa50"))])
      and at(0x5A111C)[2] == vt and A([(0x5A1123, ("mov", "qword ptr [rdx + 0x58], rax")), (0x5A1127, ("mov", "qword ptr [rdx + 0x38], rax")), (0x5A112B, ("mov", "qword ptr [rdx + 0x10], rax"))]) and rt)
def rtti(v):
    col_ = struct.unpack_from("<Q", d, off(v - 8))[0]; td_ = struct.unpack_from("<I", d, off(col_) + 12)[0] + B
    return d[off(td_) + 16:off(td_) + 90].split(b"\0")[0]
aa = (A([(0x639B15, ("lea", "r15, [rsi + rdx]")), (0x639B19, ("add", "rsi, qword ptr [rdi + 0xc0]")), (0x639B20, ("call", "qword ptr [rax + 0x50]")),
          (0x639B72, ("mov", "rdx, rsi")), (0x639B78, ("call", "qword ptr [rax + 0x58]")), (0x639B94, ("mov", "rdx, r15")), (0x639B9A, ("call", "qword ptr [rax + 0x58]")),
          (0x639AA7, ("mov", "esi, dword ptr [rdi + 0xf8]")), (0x639AFA, ("mov", "rdx, qword ptr [rdi + 0xc8]"))])
      and at(0x5A1237)[2] == 0xD314E0 and A([(0x5A1245, ("mov", "qword ptr [rdx], rax"))]) and rtti(0xD314E0) == b".?AVPAnimationController@PAnimation@Phyre@@")
check("A", aa, "00639A60: construct gets the buffer, destroy gets buffer + [desc+0xF8]; PAnimationController's construct writes its own vtable at the buffer's +0")
check("D", dd, "POctreeData, PScriptableComponent, PTriggerReceiverComponent, PInstancesComponent, PBlendableAnimationSource bodies")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/d3d11-element-release/phyre_destroys3.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
def cells(l): return l.rstrip("\r\n").split("\t")
def ev(was, tag): return "RE-CUT 2026-09-28 (OPUS, %s %s). was %s. %s" % (REC, tag, was, EXE)
def cut(t, rd, was):
    if t == "PShadowCaster":
        return [[t, "0x0054", "4", "unobservedSpan0054", "u8[4]", "four bytes after m_zbias; not written by the constructor 006C0EB0 or read by the destroy; declared gap span - no Phyre reflection member registration covers it", rd, "UNKNOWN", ev(was, "E")],
                [t, "0x0058", "40", "samplerState", "PSamplerStateD3D11", "an embedded PSamplerStateD3D11: the constructor 006C0EB0 builds it with 00615CD0 (PSamplerStateD3D11's slot-10 constructor body) and sets its filters to 1, wraps to 2 and m_flags bit 6 while bit 7 is clear; the destroy 006C0B50 destroys it with 006167C0 (PSamplerStateD3D11's destroy body)", "TYPE RESOLVED", "PROVEN", ev(was, "E")]]
    return [[t, "0x0020", "4", "arrayCount20", "uint32", "the element count of the array cell at +0x28 (bit 31 set keeps the array): the destroy 006C4B70 frees the array through 00584730 when bit 31 is clear and the count is above 1, then zeroes this", "TYPE RESOLVED", "PROVEN", ev(was, "L")],
            [t, "0x0024", "4", "unobservedSpan0024", "u8[4]", "four bytes after the count; not read by the destroy; declared gap span - no Phyre reflection member registration covers it", rd, "UNKNOWN", ev(was, "L")],
            [t, "0x0028", "8", "array28", "void*", "the array cell the count at +0x20 describes: the destroy 006C4B70 frees it through 00584730 only when the count is above 1 and bit 31 is clear, then nulls it. With a count of 1 it is not freed - the pattern of the D3D11 element arrays, whose single element sits inline in this cell - so it holds a heap pointer or one inline 8-byte element; the elements are not read here", "TYPE RESOLVED", "PROVEN", ev(was, "L")]]
SPAN = {("PShadowCaster", "0x0054", "44"), ("PLODGroup", "0x0020", "16")}
DT = {"PShadowCaster": "006C0B50: destroys the embedded PSamplerStateD3D11 at +0x58 with 006167C0, then frees m_splits' array (+0x18, count +0x10) unless bit 31 is set (E)",
      "PLODGroup": "006C4B70: 006C5200 destroys m_levels (+0x50; each 0x38-byte PLODLevel through 006C5320, then the array), then frees the +0x28 array (count +0x20) unless bit 31 is set (L)",
      "POctreeData": "008775E0: unlinks m_next / m_prev (+0x20 / +0x28) from their neighbours, self-links them and nulls m_octree (D)",
      "PScriptableComponent": "0063FC60: calls vtable slot 0 of the object at (argument - 8) with edx = 0 (skipped for a null argument). The destroy slot is handed the object plus the descriptor's signed +0xF8 adjustment - 00639A60 passes buffer + [desc+0xF8] to +0x58 and the bare buffer to +0x50 - and this thunk undoes an adjustment of 8, so the object whose rows the store gives starts 8 bytes before the argument (corrected 2026-09-28: first read as the instance being the +0x08 sub-object of a polymorphic object). What slot 0 does is not read here (D A)",
      "PTriggerReceiverComponent": "006CDD30: frees [+0x40] (m_exitHandler) and [+0x28] (m_entryHandler) through 00584730 unless the pointer's bit 0 is set, then the PComponent destructor 006AAA50 (D)",
      "PInstancesComponent": "006ADC20: frees the instances array (+0x20, count +0x18) unless bit 31 is set, then the PComponent destructor 006AAA50 (D)",
      "PBlendableAnimationSource": "005A1110: stores 00D312F0 (RTTI PAnimation::PAnimationHierarchyNode) into +0x10, +0x38 and +0x58 - the vtable slots of the three inline controllers - and returns (D)"}
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if (c[0], c[1], c[2]) in SPAN and c[3].startswith("unobservedSpan"):
            out += ["\t".join(r) + e for r in cut(c[0], c[6], "%s %s (%s)" % (c[3], c[4], c[5][:200]))]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        OLDT = "the instance is the +0x08 sub-object of a polymorphic object; what slot 0 does is not read here (D)"
        if c[0] == "PScriptableComponent" and OLDT in c[6]:   # the 2026-09-28 correction (A) of the first publication's wording
            i0 = c[6].index("0063FC60: calls vtable slot 0"); j0 = c[6].index(" - READ 2026-09-28", i0)
            c[6] = c[6][:i0] + DT["PScriptableComponent"] + c[6][j0:]
        if c[0] in DT and c[6].endswith("descriptor destroy slot +0x58, form not reduced"):
            c[6] = "~~%s~~ %s - READ 2026-09-28 (OPUS, %s)" % (c[6], DT[c[0]], REC)
        if c[0] == "PShadowCaster" and c[5] == "":
            c[5] = "006C0EB0 (reached from descriptor slot 10 006C0860; OPUS %s E): +0x00 = 0, +0x08 = 01F2EDC8, +0x10 = 0, +0x18 = 0, +0x50 = 0x3727C5AC, then the embedded PSamplerStateD3D11 at +0x58 through 00615CD0 with its filters and wraps set" % REC
        tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines()]
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
have = {(r[0], int(r[1], 16)): r for r in F if r[0] in ("PShadowCaster", "PLODGroup")}
ok = (have.get(("PShadowCaster", 0x58), [0, 0, 0, "", ""])[4] == "PSamplerStateD3D11" and have[("PShadowCaster", 0x58)][2] == str(int(T["PSamplerStateD3D11"][1], 16))
      and have.get(("PLODGroup", 0x28), [0, 0, 0, ""])[3] == "array28"
      and all(sum(int(r[2]) for k, r in have.items() if k[0] == t) == int(T[t][1], 16) for t in ("PShadowCaster", "PLODGroup"))
      and all(REC in T[t][6] for t in DT) and REC in T["PShadowCaster"][5])
check("Q", all(DT[t] in T[t][6] for t in DT), "the --patch generator's destroy text equals the store cell for all seven types (a row-only amendment fails)")
check("S", ok, "seven destroy cells reduced; PShadowCaster +0x58 typed PSamplerStateD3D11 at its width; PLODGroup +0x20 re-cut; tiling kept")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
