"""HM-1: who writes an element row's +0x08 parentSlot, and where the parent comes from (OPUS, 2026-09-27). Control. Static.

The earlier pass (hm1_parent_skeleton.py) found only -1 writers of RenderStrideC0Element +0x08. The positive writers
exist and are reached only from the character-render-record attach step:
  A1 two attach bodies store the PARENT row's +0x04 slot into the child's +0x08: 00370180 (0037020D) and 00373160
     (003731E9). With a joint (r8 != -1) they store it as the child's +0x14 word; without one they store the child's
     +0x04 into the parent's +0x10
  A2 00370180's only rel32 caller is the bank wrapper 0046E590; 00373160's only rel32 reference is the conditional
     tail jump in 00370390 (taken when the child row's +0x9C == 2), whose only caller is the bank wrapper 0046E640.
     Both wrappers resolve (child, parent) through 002ED570 on the same bank and then write +0x0C = 0020E620(row at
     +0x08) - so the +0x0C writer list has FIVE members, not the three the field row named
  A3 the wrappers are reached from the render-record attach helpers: 0046E590 only from 004218A0 (joint by NAME,
     00372760), 0046E640 from 004215A0 and 004219C0 (joint by CODE) and from 004211B0 (joint index given). Each takes
     the parent record as rcx and passes the parent's and the child's +0x18 element slots as (child, parent).
     004211B0 is the one route that does not start at +0x3CE: its callers are 0041F010 (from 004215A0's 0x10A and
     0x0F arms and from 00424D80) and 0041EDE0 (from 00429760)
  A4 RenderRecords_ProcessDirtyState 00427DE0 drives both: 0042F6C0 and 0042F880 read the child record's +0x3CE u16,
     index the 0x740-byte record pool [022C6F28] with it (an inactive record, +0x284 == 0, counts as none) and call
     004218A0(parent, child + 0x3D4, child) / 004215A0(parent, child.+0x3CC, child)
  A5 +0x3CC is the attach-point CODE, not a link index: 004215A0 dispatches on it (0x7FFF whole model, 0x10A, 0x102 ->
     2, 0x103 -> 3, below 0x100 through 003E5AD0, other values through 00422380), and no pool index is formed from it
  A6 the only u16 stores to +0x3CC / +0x3CE in .text are 0042F310 and 0042F3B0(child, parent, code, ...): both store
     (parent, code) and set +0x290 bit 19, the dirty bit 0042F6C0 / 0042F880 clear. Their rel32 callers are listed
Not claimed: which actors a shipped script or battle routine attaches, so which parent the hc1006_03 row gets; bulk
(memset / copy) initialisation of +0x3CC..+0x3CF; what each attach code names.
"""
import re, struct, sys, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def D(f): return list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(f)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
CODE = [s for s in SECS if s[0] & 0x20000000]
def refs(t):
    """every rel32 call / jmp / jcc whose target is t: (site, kind)"""
    out = []
    for ch, vs, va, rs, ro in CODE:
        for p in range(ro, ro + rs - 6):
            if d[p] in (0xE8, 0xE9) and BASE + va + p - ro + 5 + struct.unpack_from("<i", d, p + 1)[0] == t:
                out.append((BASE + va + p - ro, "call" if d[p] == 0xE8 else "jmp"))
            elif d[p] == 0x0F and 0x80 <= d[p + 1] <= 0x8F and BASE + va + p - ro + 6 + struct.unpack_from("<i", d, p + 2)[0] == t:
                out.append((BASE + va + p - ro, "jcc"))
    return out
def callers(t): return {owner(s) for s, k in refs(t) if k == "call"}

a, b = I(0x370180), I(0x373160)
check("A1 both attach bodies store the parent row's +0x04 into the child's +0x08; joint -> child +0x14, none -> parent +0x10",
      a.get(0x370209) == "mov ecx, dword ptr [r15 + 4]" and a.get(0x37020D) == "mov dword ptr [r14 + 8], ecx"
      and a.get(0x37021C) == "mov word ptr [r14 + 0x14], r13w" and a.get(0x370223) == "mov eax, dword ptr [r14 + 4]"
      and a.get(0x370227) == "mov dword ptr [r15 + 0x10], eax"
      and b.get(0x3731E5) == "mov ecx, dword ptr [r15 + 4]" and b.get(0x3731E9) == "mov dword ptr [rbp + 8], ecx"
      and b.get(0x3731F7) == "mov word ptr [rbp + 0x14], r13w" and b.get(0x3731FE) == "mov eax, dword ptr [rbp + 4]"
      and b.get(0x373201) == "mov dword ptr [r15 + 0x10], eax")

r1, r2 = refs(0x370180), refs(0x373160)
g = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x370390):off(0x370390) + 14], 0x370390)}
w1, w2 = I(0x46E590), I(0x46E640)
wr = lambda W, c, s: (W.get(c) == "call " + hex(s) and any(v == "mov dword ptr [rbx + 0xc], eax" for v in W.values())
                      and any(v == "mov edx, dword ptr [rbx + 8]" for v in W.values()) and "call 0x20e620" in W.values())
check("A2 00370180 <- 0046E590 only; 00373160 <- the tail jcc in 00370390 only (row +0x9C == 2) <- 0046E640 only; both"
      " wrappers then write +0x0C = encode(row at +0x08)",
      [(owner(s), k) for s, k in r1] == [(0x46E590, "call")] and [(s, k) for s, k in r2] == [(0x370397, "jcc")]
      and g.get(0x370390) == "cmp dword ptr [rcx + 0x9c], 2" and callers(0x370390) == {0x46E640}
      and wr(w1, 0x46E5EB, 0x370180) and wr(w2, 0x46E69B, 0x370390),
      "refs %s / %s" % ([("%08X" % s, k) for s, k in r1], [("%08X" % s, k) for s, k in r2]))

N, C, Q, R = I(0x4218A0), I(0x4215A0), I(0x4219C0), I(0x4211B0)
check("A3 0046E590 <- 004218A0 (joint by name, 00372760); 0046E640 <- 004215A0, 004219C0 and 004211B0; the parent"
      " record is rcx and the element slots go as (child, parent); 004211B0 <- 0041EDE0 and 0041F010",
      callers(0x46E590) == {0x4218A0} and callers(0x46E640) == {0x4211B0, 0x4215A0, 0x4219C0}
      and N.get(0x4218CC) == "mov esi, dword ptr [rbx + 0x18]" and N.get(0x4218BB) == "mov rbx, r8"
      and N.get(0x421906) == "mov esi, dword ptr [r14 + 0x18]" and N.get(0x4218BE) == "mov r14, rcx"
      and N.get(0x42196C) == "call 0x372760" and N.get(0x42197B) == "mov r8d, dword ptr [rsi + 4]"
      and N.get(0x421982) == "mov edx, dword ptr [rbp + 4]" and N.get(0x421989) == "call 0x46e590"
      and C.get(0x42174D) == "mov r8d, dword ptr [rbx + 4]" and C.get(0x421754) == "mov edx, dword ptr [r14 + 4]"
      and C.get(0x42175C) == "call 0x46e640" and Q.get(0x421AC1) == "call 0x46e640"
      and R.get(0x4211C3) == "mov edi, dword ptr [rdx + 0x18]" and R.get(0x421200) == "mov esi, dword ptr [r14 + 0x18]"
      and R.get(0x4211D1) == "mov r14, rcx" and R.get(0x42124B) == "mov edx, dword ptr [rdi + 4]"
      and R.get(0x421244) == "mov r8d, dword ptr [rbx + 4]" and R.get(0x421255) == "call 0x46e640"
      and callers(0x4211B0) == {0x41EDE0, 0x41F010},
      str(sorted("%08X" % f for f in callers(0x46E640))))

P6, P8 = I(0x42F6C0), I(0x42F880)
check("A4 0042F6C0 / 0042F880 (from 00427DE0) take the parent from the child's +0x3CE (pool 0x740, +0x284 == 0 -> none)"
      " and call 004218A0(parent, child+0x3D4, child) / 004215A0(parent, child.+0x3CC, child)",
      P6.get(0x42F6C6) == "movzx eax, word ptr [rcx + 0x3ce]" and P6.get(0x42F6EA) == "imul rdi, rax, 0x740"
      and P6.get(0x42F6F8) == "cmp dword ptr [rdi + 0x284], ebp" and P6.get(0x42F7DD) == "lea rdx, [rsi + 0x3d4]"
      and P6.get(0x42F7E4) == "mov rcx, rdi" and P6.get(0x42F7DA) == "mov r8, rsi" and P6.get(0x42F7E7) == "call 0x4218a0"
      and P8.get(0x42F889) == "movzx eax, word ptr [rcx + 0x3ce]" and P8.get(0x42F8AB) == "imul rdi, rax, 0x740"
      and P8.get(0x42FA1C) == "movzx edx, word ptr [rsi + 0x3cc]" and P8.get(0x42FA23) == "mov r8, rsi"
      and P8.get(0x42FA26) == "mov rcx, rdi" and P8.get(0x42FA29) == "call 0x4215a0"
      and callers(0x42F6C0) == {0x427DE0} and callers(0x42F880) == {0x427DE0})

codecmp = sorted(int(m, 16) for v in C.values() for m in re.findall(r"^mov eax, (0x[0-9a-f]+)$", v))
pool3cc = [v for v in P8.values() if "0x3cc" in v and "imul" in v]
check("A5 REGRESSION against 'sibling link word': +0x3CC is the code 004215A0 dispatches on (0x7FFF, 0x10A, 0x102, 0x103,"
      " 0x100 bound), never scaled into the record pool",
      C.get(0x4215C6) == "movzx ebp, dx" and C.get(0x421658) == "cmp bp, ax" and C.get(0x42173E) == "call 0x3e5ad0"
      and C.get(0x42176D) == "call 0x422380" and codecmp == [0x100, 0x102, 0x103, 0x10A, 0x7FFF] and not pool3cc
      and "imul" not in P8.get(0x42FA1C, "") and P8.get(0x42F95B) == "cmp word ptr [rsi + 0x3cc], ax", str(codecmp))

stores = []
for ch, vs, va, rs, ro in CODE:
    for f in keys:
        if BASE + va <= f < BASE + va + vs and off(f) is not None:
            for x in cs.disasm(d[off(f):off(f) + sizes[f]], f):
                s = "%s %s" % (x.mnemonic, x.op_str)
                if re.match(r"mov word ptr \[r(?!sp|ip)\w+ \+ 0x3c[ce]\], ", s): stores.append((f, x.address, s))
S1, S3 = I(0x42F310), I(0x42F3B0)
cl = sorted({owner(s) for f in (0x42F310, 0x42F3B0) for s, k in refs(f) if k in ("call", "jmp")} - {None})
check("A6 the only u16 stores to +0x3CC / +0x3CE are 0042F310 and 0042F3B0; both set +0x290 bit 19, the bit the"
      " dirty-state attach clears",
      sorted({f for f, a_, s in stores}) == [0x42F310, 0x42F3B0] and len(stores) == 4
      and S1.get(0x42F382) == "mov word ptr [rcx + 0x3ce], dx" and S1.get(0x42F389) == "mov word ptr [rcx + 0x3cc], r8w"
      and S1.get(0x42F39C) == "bts eax, 0x13" and S3.get(0x42F4A0) == "bts eax, 0x13"
      and P8.get(0x42FABE) == "and dword ptr [rsi + 0x290], 0xfff7ffff",
      "stores %d; callers of the two setters %s" % (len(stores), ["%08X" % f for f in cl]))

L0, E4, K8, K3 = I(0x36FFF0), I(0x46E4D0), I(0x372820), I(0x3703A0)
def rip(ins, a):
    """the absolute target of the rip-relative operand of the instruction at a"""
    x = next(cs.disasm(d[off(a):off(a) + 16], a, 1))
    m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", ins)
    return a + x.size + int(m.group(1), 16)
name = d[off(0x37001E + 7 + 0x9A1083):off(0x37001E + 7 + 0x9A1083) + 40].split(b"\0")[0]
check("A8 0036FFF0 loads SkeletonMapping.bin into the table at 02AD9E30 (count at 02AD9E38): 0x30-byte entries, a 32-byte"
      " name copied first, +0x20 value count, +0x28 the int32 values",
      name == b"./PS2Data/add_motion/SkeletonMapping.bin" and rip(L0[0x3700A1], 0x3700A1) == 0x2AD9E30
      and rip(L0[0x370086], 0x370086) == 0x2AD9E38 and L0.get(0x3700C3) == "mov r8d, 0x20" and L0.get(0x3700CC) == "lea rcx, [rcx + rcx*2]"
      and L0.get(0x3700F6) == "mov dword ptr [rsi + rax + 0x20], ecx" and L0.get(0x370112) == "mov qword ptr [rsi + rcx + 0x28], rax",
      name.decode())
check("A9 the element's +0x20 is its 32-byte NAME and +0xB0 its SkeletonMapping index: the create path 0046E4D0 runs the"
      " constructor then 00372820(element, ..., name); 00372820 copies 32 bytes to +0x20, sets +0xB0 to -1 and then to"
      " the entry whose name equals it; 003703A0 takes the mapped path only when +0xB0 != -1 and indexes the table by it",
      E4.get(0x46E515) == "call 0x3721e0" and E4.get(0x46E521) == "mov r9, rbp" and E4.get(0x46E554) == "mov rcx, rbx"
      and E4.get(0x46E557) == "call 0x372820" and callers(0x372820) == {0x46E4D0}
      and K8.get(0x372842) == "mov rdi, r9" and K8.get(0x37288C) == "movups xmm0, xmmword ptr [rdi]"
      and K8.get(0x37288F) == "lea r11, [rsi + 0x20]" and K8.get(0x37289D) == "movups xmmword ptr [r11], xmm0"
      and K8.get(0x3728AF) == "movups xmmword ptr [r11 + 0x10], xmm1" and K8.get(0x3728A8) == "mov dword ptr [rsi + 0xb0], r13d"
      and rip(K8[0x3728CE], 0x3728CE) == 0x2AD9E30 and K8.get(0x3728E3) == "movzx ecx, byte ptr [rax + r8]"
      and K8.get(0x3728F7) == "mov dword ptr [rsi + 0xb0], r9d"
      and K3.get(0x370647) == "cmp dword ptr [r14 + 0xb0], -1" and K3.get(0x37065D) == "movsxd rax, dword ptr [r14 + 0xb0]"
      and rip(K3[0x370673], 0x370673) == 0x2AD9E30)

rows = {}
import os
for l in open(os.environ.get("FIELDS_PATH") or ROOT / "Database/FFXII TZA/_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and (c[0], c[1]) in (("CharacterRenderRecord", "0x3CC"), ("CharacterRenderRecord", "0x3CE"), ("RenderStrideC0Element", "0x00C"),
                                        ("RenderStrideC0Element", "0x020"), ("RenderStrideC0Element", "0x0B0")):
        rows[(c[0], c[1])] = c
cc, ce, e0c = rows.get(("CharacterRenderRecord", "0x3CC")), rows.get(("CharacterRenderRecord", "0x3CE")), rows.get(("RenderStrideC0Element", "0x00C"))
check("A7 STORE REGRESSION: +0x3CC is not stored as a link / index word, +0x3CE names the parent, and the element's +0x0C"
      " writer list carries all five writers",
      cc is not None and "link" not in cc[3].lower() and "index" not in cc[3].lower() and "sibling link" not in cc[5]
      and ce is not None and "parent" in ce[3].lower()
      and e0c is not None and all(w in e0c[5] for w in ("0046E300", "0046E370", "0046E420", "0046E590", "0046E640")),
      "%s / %s" % (cc and cc[3], ce and ce[3]))
e20, eb0 = rows.get(("RenderStrideC0Element", "0x020")), rows.get(("RenderStrideC0Element", "0x0B0"))
check("A10 STORE REGRESSION against 'unobserved': the element's +0x20 is stored as a char[32] name, +0xB0 as the"
      " SkeletonMapping index",
      e20 is not None and e20[4] == "char[32]" and "unobserved" not in e20[3].lower()
      and eb0 is not None and "skeletonmapping" in eb0[3].lower(), "%s / %s" % (e20 and e20[3], eb0 and eb0[3]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
