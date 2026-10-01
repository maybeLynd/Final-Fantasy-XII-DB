"""x8_versions.py [UPSTREAM_DIR] - X-8: the image-side discriminators for the linked library versions
(FABLE, Claude Opus 5.5, 2026-09-27). Static read of the shipped exe; section-aware addressing.

  A0 addressing control: 01CCD380 / 01CCE3D8 / 01F48940 / 01CB85D0 / 00D86C00 / 00D8F690 hold the Bullet
     serializer names, the JsonBox RTTI, the SEAD vorbis error text and the two YEBIS licence strings; read as
     addresses, the 2026-09-18 narrowing's 01BAC180 / 01BAD1D8 / 01E26F40 / 01B973D0 / 00C65A00 / 00C6E490 hold
     none of them (they are the FILE OFFSETS of the same strings).
  V1 libvorbis >= 1.3.5: vorbis_book_init_decode 00882C20 has the single-entry codebook branch at 00882F50
     (n == 1 && dec_maxlength == 1 -> dec_firsttablen = 1, calloc(2, 4), both entries 1).
  V2 libvorbis < 1.3.6: _book_maptype1_quantvals 00882850 contains no div / idiv (the 1.3.6 guards
     entries/vals and LONG_MAX/(vals+1) need one). Sensitivity: the same counter finds idiv in the
     neighbouring libvorbis code 00880000-00890000.
  I1 Dear ImGui: ImGuiIO ctor 00791D80 memsets 0xB88 and stores MousePos at +0xD0, MousePosPrev at +0x310.
  I2 Dear ImGui v1.35: the context ctor 00791E70 memsets +0xFA8/0x24E0, +0x34B0/0x400, +0x38D8/0x1E0,
     stores LogAutoExpandMaxDepth = 2 at +0x38D4, and its highest store is the qword at +0x3AB8 (size 0x3AC0).
  J1 JsonBox >= 0.6: the three OutputFilter vtables 00905070 / 009050F0 / 00905170 are 0x80 apart, and
     each has 15 .text slots followed by a non-code qword (the next vtable's COL, or data after the last) (0.5's setbuf(char*, int) would
     be a 16th slot on x64).
  J2 JsonBox >= 0.5: 001FF3AE stores precision 17 (0x11) into the stream's +0x20.
  H1 CRI HCA: the decoder banner 'HCA Decoder (Float) Ver.2.05.00' at 01CBA5D1.
With UPSTREAM_DIR (holding vorbis.git, imgui.git, JsonBox.git clones), also:
  U1 vorbis 65417f3a is in v1.3.5 and not v1.3.4; e5b13789 is in v1.3.6 and not v1.3.5.
  U2 JsonBox 37de9008 (drops sync / setbuf(char*, int)) is in 0.6 and not 0.5.
  U3 imgui 91b4b8a0 is at or before v1.35 and ceb4da20 is after it (the 0x3AC0 window brackets exactly v1.35).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, subprocess, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = []
for i in range(_n):
    b = _pe + 24 + _opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
def off(v):
    for _, vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
def sec(v):
    for nm, vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + max(vs, rs): return nm
def at(v, n): o = off(v); return d[o:o + n] if o is not None else b""
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(f): return list(cs.disasm(at(f, SIZES[f]), f))
def ins(f): return ["%s %s" % (x.mnemonic, x.op_str) for x in body(f)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

pairs = [(0x01CCD380, 0x01BAC180, b"btCollisionShapeData"), (0x01CCE3D8, 0x01BAD1D8, b"btCollisionObjectFloatData"),
         (0x01F48940, 0x01E26F40, b".?AV?$OutputFilter@VSolidusEscaper"), (0x01CB85D0, 0x01B973D0, b"[sead][!!error!!]MaterialVorbis"),
         (0x00D86C00, 0x00C65A00, b"FeatureId = YEBIS_D3D11"), (0x00D8F690, 0x00C6E490, b"The YEBIS library passed over")]
check("A0 corrected addresses hold the strings; the narrowing's numbers do not (as addresses) but do (as file offsets)",
      all(at(a, len(s)) == s and at(b, len(s)) != s and d[b:b + len(s)] == s for a, b, s in pairs))

w = [x for x in body(0x00882C20) if 0x00882F50 <= x.address < 0x00882F85]
seq = ["%s %s" % (x.mnemonic, x.op_str) for x in w]
check("V1 single-entry codebook branch at 00882F50", seq[:3] == ["cmp r15d, 1", "jne 0x882f85", "cmp dword ptr [rbx + 0x44], r15d"]
      and "lea edx, [r15 + 3]" in seq and "lea ecx, [rdx - 2]" in seq and "mov dword ptr [rbx + 0x40], r15d" in seq
      and "mov dword ptr [rax + 4], r15d" in seq and "mov dword ptr [rax], r15d" in seq, str(seq[:4]))

qv = [x for x in body(0x00882850) if x.mnemonic in ("div", "idiv")]
near = sum(1 for f in SIZES if 0x00880000 <= f < 0x00890000 and SIZES[f] > 0 for x in body(f) if x.mnemonic in ("div", "idiv"))
check("V2 00882850 has no div/idiv; the counter finds them in the neighbouring code", not qv and near > 0, "(%d nearby)" % near)

io = ins(0x00791D80)
check("I1 ImGuiIO: memset 0xB88, MousePos +0xD0, MousePosPrev +0x310",
      "mov r8d, 0xb88" in io and "movsd qword ptr [rbx + 0xd0], xmm0" in io and "movsd qword ptr [rbx + 0x310], xmm0" in io)

cx = body(0x00791E70); cs_ = ["%s %s" % (x.mnemonic, x.op_str) for x in cx]
def memset_after(lea, size):
    i = cs_.index(lea) if lea in cs_ else -1
    return i >= 0 and ("mov r8d, %s" % size) in cs_[i:i + 12]
stores = [int(m.group(1), 16) for s in cs_ for m in [re.match(r"mov \w+ ptr \[rbx \+ (0x[0-9a-f]+)\], ", s)] if m]
top = max(stores); topw = [s for s in cs_ if re.match(r"mov qword ptr \[rbx \+ %s\], " % hex(top), s)]
check("I2 context: three memsets, LogAutoExpandMaxDepth, last store qword +0x3AB8 -> 0x3AC0",
      memset_after("lea rcx, [rbx + 0xfa8]", "0x24e0") and memset_after("lea rcx, [rbx + 0x34b0]", "0x400")
      and memset_after("lea rcx, [rbx + 0x38d8]", "0x1e0") and "mov dword ptr [rbx + 0x38d4], 2" in cs_
      and top == 0x3AB8 and topw, "top %s" % hex(top))

vts = [0x00905070, 0x009050F0, 0x00905170]; ok = [b - a == 0x80 for a, b in zip(vts, vts[1:])]
for v in vts:
    q = [struct.unpack_from("<Q", at(v + 8 * i, 8))[0] for i in range(16)]
    ok.append(all(sec(x) == ".text" for x in q[:15]) and sec(q[15]) != ".text")
check("J1 OutputFilter vtables: 0x80 apart, 15 .text slots then a non-code qword", all(ok), str(ok))

j2 = [x for x in body(0x001FF210) if x.address == 0x001FF3AE]
check("J2 precision(17) at 001FF3AE", bool(j2) and j2[0].op_str == "qword ptr [rcx + rsi + 0x20], 0x11", j2[0].op_str if j2 else "")

check("H1 CRI HCA decoder banner 2.05.00 at 01CBA5D1", at(0x01CBA5D1, 31) == b"HCA Decoder (Float) Ver.2.05.00")

if len(sys.argv) > 1:
    up = Path(sys.argv[1])
    def anc(repo, c, t):
        return subprocess.run(["git", "-C", str(up / repo), "merge-base", "--is-ancestor", c, t]).returncode == 0
    check("U1 vorbis 65417f3a in v1.3.5 not v1.3.4; e5b13789 in v1.3.6 not v1.3.5",
          anc("vorbis.git", "65417f3a", "v1.3.5") and not anc("vorbis.git", "65417f3a", "v1.3.4")
          and anc("vorbis.git", "e5b13789", "v1.3.6") and not anc("vorbis.git", "e5b13789", "v1.3.5"))
    check("U2 JsonBox 37de9008 in 0.6 not 0.5", anc("JsonBox.git", "37de9008", "0.6") and not anc("JsonBox.git", "37de9008", "0.5"))
    check("U3 imgui 91b4b8a0 <= v1.35 < ceb4da20", anc("imgui.git", "91b4b8a0", "v1.35") and not anc("imgui.git", "ceb4da20", "v1.35")
          and anc("imgui.git", "v1.35", "ceb4da20"))
print("FAILS", fails)
sys.exit(1 if fails else 0)
