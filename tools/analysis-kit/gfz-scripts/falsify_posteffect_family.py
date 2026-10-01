"""Falsification pass 1 on the-phyre-post-effect-class-family (OPUS, 2026-09-29), from the shipping image. The class set is
decoded from MSVC RTTI here, independently of members/gen_posteffect_family.py; call counts come from a raw E8/E9 rel32 index
over the whole of .text; data references are aligned 8-byte scans over the whole image.

  P0  sizes of the eleven workers and the small base bodies
  P1  RTTI: 37 PPostProcessing classes, one complete-object locator each; PUtilityPostProcessing has 3 slots, the other 36 have 9
  P2  section 3 slot map: slot 1 overridden by 8 of the 9 (not PMaterialPostEffect), slot 2 by all 9, slot 3 by exactly six
      (PDeferredLighting, PDepthOfField, PMotionBlur, PGlow, PFXAA, PScreenSpaceReflection), 4 / 7 / 8 by nobody, slot 5 as
      section 3b's table, slot 6 as section 2's table; every Base / D3D11 / intermediate class and three of the four inert ones
      override nothing in slots 1-8, PLowResParticles only slot 5.  (GF-3's "the leaves override 0 1 2 3 6" is CON-199.)
  P3  base bodies: 0065B8F0 delegates to slot 1; 00657150 asks slot 4, then answers only for 01F2D6E0 = "Transparent";
      006571A0 answers 01F2D700 = "DeferredRender" without readiness; 00657140 is xor al, al / ret; slots 3, 4, 7, 8 as cited
  P4  CON-197: slot 1's 1280 x 720 constants sit behind a null test on ctx + 0x520 computed BEFORE the test, and 005FD050
      returns the address of one static (02CC0410) on both exits - so the fallback arm is unreachable
  P5  section 3: PAtmospherics's slot 6 returns 5 on a null fourth argument, 0x15 when not ready, refreshes via slot 2
  P6  section 3c: 00640280 has one aligned reference, at 00D5B110 = 00D5B0C0 + 0x50; the stub 00657140 has 884; 00640280,
      00640330, 006403B0 have no direct call site
  P7  CON-198: every class vtable's stamping bodies (rip-relative lea) and their in-band callers, closed upward: exactly three
      exits leave the family's code band. One is a construction - 0018CD90 (the PostProcessParamContext constructor)
      constructs a PFXAA at +0x378 through 00645DB0, which stamps 00D625D0. The other two are exception-unwind funclets,
      each asserted by the FH3 unwind map that lists it: 008965EC (0018CD90's, destroying context + 0x378 through 0018D0D0
      -> 00646770) and 0089E870 (006458A0's, map 01DACB10, -> 00646AB0)
  P8  CON-198: the game runs PFXAA's worker directly - 0065A630 is a jump to 0065A640, and its only callers, 0018FD70 and
      00191DA0, pass context + 0x378; in 00191DA0 that arm runs when +0x3E8 and +0x3E9 are set and +0x4A3 is 0; 0018D850
      configures the member (00654160, 00656B10) and only then sets +0x3E9
  P9  GF-4 sweep: 0 direct calls to each of the ten slot-6 bodies; each worker has one, except 0065A640 (its override and
      0065A630) and 0065A960 (two, both from 00659EC0); 0060B980 has 58
  P10 section 4b: per-worker pushes / submissions / finish / teardown as tabulated (24 submissions); CON-201: the state column
      under its stated definition (the four helpers) is 3 3 11 19 3 5 13 8 0 17 4 - six page cells also counted 005DC190
  P11 section 3e: 00655920 keeps the receiver in r14, compares [+0x168] with 0xB000, tests bit 4 of 02CF7738, stores +0x60
  P12 section 5 / CON-200: the selector vtables 008C6C80 {purecall, 0018D100} and 008C6C98 {0060CD10, 0018D130};
      0018D0E0 stamps 008C6C80 and has 52 direct call sites, every one from a body that itself has none
  P13 section 3d: 02D27BA0, 02D2ADF0, 02D2E040 lie past .data's raw data
"""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def VA(off):
    for _n, start, _size, raw, rawsz in SECS:
        if raw <= off < raw + rawsz:
            return start + off - raw
    return None


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


q = lambda va: struct.unpack("<Q", blob[OFF(va):OFF(va) + 8])[0]
cstr = lambda va: blob[OFF(va):OFF(va) + 64].split(b"\0")[0].decode("latin-1")
fs = []
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            fs.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
fs.sort(); sizes = dict(fs); starts = [a for a, _ in fs]


def owner(va):
    j = bisect.bisect_right(starts, va) - 1
    return fs[j][0] if j >= 0 and va < fs[j][0] + fs[j][1] else None


def body(fa):
    return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}


def refs8(v):
    pat = struct.pack("<Q", v); out = []; i = blob.find(pat)
    while i >= 0:
        if i % 8 == 0:
            out.append(VA(i))
        i = blob.find(pat, i + 1)
    return out


# the raw rel32 index over the whole of .text
tx = [s for s in SECS if s[0] == ".text"][0]
T0, TR, TN = tx[1], tx[3], tx[4]
calls = collections.Counter(); callers = collections.defaultdict(list)
for m in re.finditer(rb"[\xe8\xe9]", blob[TR:TR + TN - 4]):
    i = m.start()
    tgt = T0 + i + 5 + struct.unpack("<i", blob[TR + i + 1:TR + i + 5])[0]
    calls[tgt] += 1; callers[tgt].append(T0 + i)

# P0
SZ = {0x00658470: 885, 0x006587F0: 930, 0x00659EC0: 1889, 0x0065A960: 2307, 0x00658BA0: 1241, 0x0065A640: 790, 0x00652940: 326,
      0x00659080: 2575, 0x00659A90: 391, 0x00659C20: 659, 0x0065BA00: 1658, 0x0065B8F0: 48, 0x006571C0: 27, 0x00653CD0: 4,
      0x00653B20: 4, 0x00657680: 10, 0x00657140: 3}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("P0", not bad and sum(sizes[a] for a in list(SZ)[:11]) == 13651, "sizes %s; the eleven sum to 13,651" % (bad or "all as cited"))

# P1: RTTI decoded here
tds = {VA(m.start()) - 0x10: m.group(1).decode() for m in re.finditer(rb"\.\?AV([A-Za-z0-9_]+)@PPostProcessing@Phyre@@\0", blob)}
rd = [s for s in SECS if s[0] == ".rdata"][0]
cols = {}
for off in range(rd[3], rd[3] + rd[4] - 24, 4):
    sig, o, _cd, td, _ch, me = struct.unpack("<6I", blob[off:off + 24])
    if sig == 1 and o == 0 and me == VA(off) - BASE and td + BASE in tds:
        cols[VA(off)] = tds[td + BASE]
vt = {}
for colva, name in cols.items():
    r = refs8(colva)
    if len(r) == 1:
        vt[name] = r[0] + 8
colptr = set(v - 8 for v in vt.values())
nslots = {}
for n, v in vt.items():
    k = 0
    while v + 8 * k not in colptr and k < 16 and T0 <= q(v + 8 * k) < T0 + tx[2]:
        k += 1
    nslots[n] = k
check("P1", len(tds) == 37 and len(cols) == 37 and len(vt) == 37 and nslots.get("PUtilityPostProcessing") == 3
      and sum(1 for n in vt if nslots[n] == 9) == 36,
      "%d type descriptors, %d locators, %d vtables; slot counts %s" % (len(tds), len(cols), len(vt), dict(collections.Counter(nslots.values()))))

# P2
S = {n: [q(vt[n] + 8 * k) for k in range(9)] for n in vt if n != "PUtilityPostProcessing"}
base = S["PPostEffectBase"]
NINE = {"PAtmospherics": 0x0065B270, "PCelShading": 0x0065B340, "PDeferredLighting": 0x0065B400, "PDepthOfField": 0x0065B4C0,
        "PFXAA": 0x0065B590, "PGlow": 0x0065B650, "PMaterialPostEffect": 0x0065B750, "PMotionBlur": 0x0065B820,
        "PScreenSpaceReflection": 0x0065B920}
over = {n: [k for k in range(1, 9) if S[n][k] != base[k]] for n in S if n != "PPostEffectBase"}
slot3 = sorted(n for n in over if 3 in over[n])
quiet = sorted(n for n in over if n not in NINE and over[n] and n != "PLowResParticles")
s5 = {n: S[n][5] for n in S if S[n][5] != base[5]}
ok = (base[1:] == [0x00655DC0, 0x006575E0, 0x00657680, 0x006571C0, 0x00657150, 0x0065B8F0, 0x00653CD0, 0x00653B20]
      and sorted(n for n in over if 1 in over[n]) == sorted(set(NINE) - {"PMaterialPostEffect"})
      and sorted(n for n in over if 2 in over[n]) == sorted(NINE)
      and slot3 == sorted(["PDeferredLighting", "PDepthOfField", "PMotionBlur", "PGlow", "PFXAA", "PScreenSpaceReflection"])
      and not any(k in over[n] for n in over for k in (4, 7, 8))
      and s5 == {"PDeferredLighting": 0x00657140, "PLowResParticles": 0x00657140, "PScreenSpaceReflection": 0x006571A0}
      and {n: S[n][6] for n in S if S[n][6] != base[6]} == NINE and not quiet and over["PLowResParticles"] == [5]
      and over["PAtmospherics"] == [1, 2, 6] and over["PCelShading"] == [1, 2, 6] and over["PMaterialPostEffect"] == [2, 6]
      and len(set(S[n][0] for n in S)) == 36 and all(S[n][0] != base[0] for n in over))
check("P2", ok, "slot 3 overridden by %d: %s; PAtmospherics and PCelShading override 1 2 6 only; every slot 0 distinct" % (len(slot3), ", ".join(slot3)))

# P3
b = body(0x0065B8F0)
v5, v5s, st = body(0x00657150), body(0x006571A0), body(0x00657140)
ok = (b.get(0x0065B8F4) == "cmp byte ptr [rcx + 0x40], 0" and b.get(0x0065B8FF) == "mov r8d, dword ptr [r9 + 0x2c]"
      and b.get(0x0065B903) == "mov edx, dword ptr [r9 + 0x28]" and b.get(0x0065B912) == "call qword ptr [rax + 8]"
      and v5.get(0x00657164) == "call qword ptr [rax + 0x20]" and v5.get(0x00657180) == "lea rdx, [rip + 0x18d6559]"
      and 0x00657187 + 0x18D6559 == 0x01F2D6E0 and cstr(q(0x01F2D6E0)) == "Transparent"
      and v5s.get(0x006571A6) == "lea r8, [rip + 0x18d6553]" and 0x006571AD + 0x18D6553 == 0x01F2D700
      and cstr(q(0x01F2D700)) == "DeferredRender" and not any("call" in t for t in v5s.values())
      and list(st.values()) == ["xor al, al", "ret"]
      and body(0x00657680) == {0x00657680: "mov dword ptr [rcx + 0x44], edx", 0x00657683: "xor eax, eax",
                               0x00657685: "mov dword ptr [rcx + 0x48], r8d", 0x00657689: "ret"}
      and body(0x00653CD0)[0x00653CD0] == "mov eax, dword ptr [rcx + 0x44]" and body(0x00653B20)[0x00653B20] == "mov eax, dword ptr [rcx + 0x48]"
      and body(0x006571C0).get(0x006571CF) == "cmp byte ptr [rcx + 0x41], 0")
check("P3", ok, "base render -> slot 1 with the +0x28/+0x2C pair; slot 5 Transparent after slot 4; SSR DeferredRender; the stub")

# P4
c1, g = body(0x00655DC0), body(0x005FD050)
stat = {a + 7 + int(t.split("0x")[-1].rstrip("]"), 16) for a, t in g.items() if t.startswith("lea r") and "rip + 0x26c33" in t}
ok = (c1.get(0x00655DD7) == "call 0x5fd050" and c1.get(0x00655DDC) == "add rax, 0x520" and c1.get(0x00655DE6) == "test rax, rax"
      and c1.get(0x00655DF0) == "mov edi, 0x500" and c1.get(0x00655E03) == "mov ebx, 0x2d0"
      and c1.get(0x00655E15) == "mov byte ptr [rsi + 0x40], 1"
      and g.get(0x005FD0BF) == "mov rax, rbx" and g.get(0x005FD0C4) == "lea rax, [rip + 0x26c3345]" and stat == {0x02CC0410})
check("P4", ok, "005FD050 returns 02CC0410 on both exits; 00655DC0 tests ctx + 0x520, never null: the 1280 x 720 arm is unreachable")

# P5
a6 = body(0x0065B270)
check("P5", a6.get(0x0065B2BA) == "lea eax, [rdi + 5]" and a6.get(0x0065B2E8) == "call qword ptr [rax + 0x10]"
      and a6.get(0x0065B310) == "call 0x658470" and a6.get(0x0065B317) == "mov eax, 0x15",
      "5 on a null fourth argument; slot 2 on a stale triple; the worker; 0x15 when not ready")

# P6
r = refs8(0x00640280)
check("P6", r == [0x00D5B110] and 0x00D5B110 - 0x00D5B0C0 == 0x50 and len(refs8(0x00657140)) == 884
      and calls[0x00640280] == calls[0x00640330] == calls[0x006403B0] == 0,
      "00640280: one reference, at 00D5B0C0 + 0x50; stub 00657140: %d references; no direct calls" % len(refs8(0x00657140)))

# P7: vtable stamping bodies (rip-relative lea of the vtable), closed upward inside the family band
leas = collections.defaultdict(set); vset = {v: n for n, v in vt.items()}
for m in re.finditer(rb"(?=[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d])", blob[TR:TR + TN - 7]):
    i = m.start()
    tgt = T0 + i + 7 + struct.unpack("<i", blob[TR + i + 3:TR + i + 7])[0]
    if tgt in vset:
        leas[vset[tgt]].add(owner(T0 + i))
stampers = set(x for n in leas if n != "PUtilityPostProcessing" for x in leas[n])
inb = lambda a: a is not None and 0x0063E000 <= a < 0x00648200
seen, fr, exits = set(stampers), list(stampers), set()
while fr:
    x = fr.pop()
    for c in callers[x]:
        o = owner(c)
        if not inb(o):
            exits.add((o, c, x))
        elif o not in seen:
            seen.add(o); fr.append(o)
ctor = body(0x0018CD90); fx = body(0x00645DB0)
ok = (all(leas.get(n) for n in vt) and None not in stampers and all(inb(x) for x in stampers)
      and exits == {(0x0018CD90, 0x0018CFD5, 0x00645DB0), (0x0018D0D0, 0x0018D0D0, 0x00646770), (0x0089E870, 0x0089E877, 0x00646AB0)}
      and leas["PFXAA"] >= {0x00645DB0} and fx.get(0x00645DB9) == "call 0x6461b0" and fx.get(0x00645DD0) == "lea rax, [rip + 0x71c7f9]"
      and 0x00645DD7 + 0x71C7F9 == vt["PFXAA"] and fx.get(0x00645DD7) == "mov qword ptr [rbx], rax"
      and ctor.get(0x0018CFCE) == "lea rcx, [rbx + 0x378]" and ctor.get(0x0018CFD5) == "call 0x645db0"
      and body(0x0018D0D0) == {0x0018D0D0: "jmp 0x646770"} and body(0x0089E870).get(0x0089E877) == "jmp 0x646ab0"
      and calls[0x0018CD90] == 3 and calls[0x0089E870] == 0)
# Narrowed 2026-09-30 (SWE2-AUDIT-SPEC's batch-9 review): assert each exit's owner. One exit is a construction; the
# other two are exception-unwind funclets, found by the C++ EH (FH3) unwind maps that list them as actions.
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])


def eh_owner(funclet):
    """The function whose FH3 unwind map lists `funclet` as an action: (function, map address)."""
    want = funclet - BASE
    for rf in pe.DIRECTORY_ENTRY_EXCEPTION:
        e = rf.struct
        if e.UnwindData & 1:
            continue
        try:
            hdr = pe.get_data(e.UnwindData, 4)
            if not (hdr[0] >> 3) & 3:
                continue
            off = e.UnwindData + 4 + 2 * ((hdr[2] + 1) & ~1)
            fi = struct.unpack("<I", pe.get_data(off + 4, 4))[0]
            magic, maxs, um = struct.unpack("<III", pe.get_data(fi, 12))
        except Exception:
            continue
        if magic & 0xFFFFFFF0 != 0x19930520:
            continue
        for k in range(maxs):
            if struct.unpack("<I", pe.get_data(um + 8 * k + 4, 4))[0] == want:
                return BASE + e.BeginAddress, BASE + um
    return None, None


f1 = body(0x008965EC)
own1, map1 = eh_owner(0x008965EC)
own2, map2 = eh_owner(0x0089E870)
funclets = (f1.get(0x008965EC) == "mov rcx, qword ptr [rdx + 0x40]" and f1.get(0x008965F3) == "add rcx, 0x378"
            and f1.get(0x008965FA) == "jmp 0x18d0d0" and own1 == 0x0018CD90 and own2 == 0x006458A0 and map2 == 0x01DACB10)
check("P7", ok and funclets, "%d stamping bodies, all in band; exits from the band: %s. Owners: 0018CFD5 is the construction "
      "(0018CD90 -> 00645DB0, the PFXAA at context + 0x378); 0018D0D0 is reached from 008965EC, an unwind action of %s "
      "(map %s) that destroys context + 0x378 (-> 00646770, the PFXAABase destructor chain); 0089E870 is an unwind action of "
      "%s (map %s), PDeferredLightingBase's installer (-> 00646AB0, PPostEffectBase)" % (
          len(stampers), ", ".join("%08X@%08X->%08X" % e for e in sorted(exits)),
          "%08X" % own1 if own1 else None, "%08X" % map1 if map1 else None,
          "%08X" % own2 if own2 else None, "%08X" % map2 if map2 else None))

# P8
th, a, f, s = body(0x0065A630), body(0x00191DA0), body(0x0018FD70), body(0x0018D850)
# the override's own call site is found, not assumed
ov = [c for c in callers[0x0065A640] if owner(c) == 0x0065B590]
ok = (th.get(0x0065A639) == "jmp 0x65a640" and sorted(callers[0x0065A630]) == [0x0018FDA8, 0x00191E38]
            and f.get(0x0018FD9C) == "add rcx, 0x378" and a.get(0x00191E2C) == "add rcx, 0x378"
            and a.get(0x00191DAF) == "cmp byte ptr [rcx + 0x3e8], 0" and a.get(0x00191DC5) == "cmp byte ptr [rcx + 0x3e9], 0"
            and a.get(0x00191DD2) == "cmp byte ptr [rcx + 0x4a3], 0" and a.get(0x00191DD9) == "je 0x191e10"
            and s.get(0x0018E1AD) == "lea rdi, [rbx + 0x378]" and s.get(0x0018E1BA) == "call 0x654160"
            and s.get(0x0018E1C8) == "call 0x656b10" and s.get(0x0018E1CD) == "mov byte ptr [rbx + 0x3e9], 1"
            and s.get(0x0018E178) == "je 0x18e1d4" and len(ov) == 1 and len(callers[0x0065A640]) == 2)
check("P8", ok, "0065A630 -> 0065A640 from 0018FD70 and 00191DA0 on context + 0x378; 00191DA0 takes it when +0x4A3 == 0; "
      "0018D850 configures, then sets +0x3E9")

# P9
SIX = [0x0065B8F0] + sorted(NINE.values())
W = [0x00658470, 0x006587F0, 0x00659EC0, 0x0065A960, 0x00658BA0, 0x0065A640, 0x00652940, 0x00659080, 0x00659A90, 0x00659C20, 0x0065BA00]
wc = {w: calls[w] for w in W}
check("P9", all(calls[x] == 0 for x in SIX) and all(wc[w] == (2 if w in (0x0065A640, 0x0065A960) else 1) for w in W)
      and set(owner(c) for c in callers[0x0065A960]) == {0x00659EC0} and calls[0x0060B980] == 58,
      "slot-6 bodies 0 each; workers %s; 0060B980 %d" % (" ".join("%d" % wc[w] for w in W), calls[0x0060B980]))

# P10
# the state column under its own definition (the four helpers); the page's column is CON-201 - six of its cells also count 005DC190
TAB = {0x00658470: (4, 3, 1, 1, 1), 0x006587F0: (1, 3, 1, 1, 1), 0x00658BA0: (2, 11, 3, 3, 9), 0x00659080: (5, 19, 5, 5, 9),
       0x00659A90: (2, 3, 1, 1, 1), 0x00659C20: (2, 5, 1, 1, 2), 0x00659EC0: (6, 13, 2, 3, 7), 0x0065A640: (2, 8, 2, 2, 4),
       0x0065A960: (0, 0, 3, 0, 0), 0x0065BA00: (8, 17, 4, 4, 5), 0x00652940: (1, 4, 1, 1, 2)}
PAGE_STATE = {0x00658470: 4, 0x006587F0: 4, 0x00659A90: 4, 0x00659C20: 6, 0x0065BA00: 21, 0x00652940: 5}
STATE = {0x0060D4F0, 0x0060DB50, 0x005FEFD0, 0x0060CD70}
got = {}
for w in TAB:
    tg = [int(t.split()[1], 16) for t in body(w).values() if t.startswith("call 0x")]
    got[w] = (tg.count(0x001B81B0), sum(1 for t in tg if t in STATE), tg.count(0x0060B980), tg.count(0x00600A60), tg.count(0x0016D6A0))
diff = {("%08X" % w): got[w] for w in TAB if got[w] != TAB[w]}
with5 = all(got[w][1] + [t for t in body(w).values() if t == "call 0x5dc190"].__len__() == PAGE_STATE[w] for w in PAGE_STATE)
check("P10", not diff and with5 and sum(v[2] for v in got.values()) == 24,
      "per-worker counts %s; 24 submissions; the six page cells that differ equal four helpers + 005DC190" % (diff or "as measured"))

# P11
e = body(0x00655920)
check("P11", e.get(0x00655941) == "mov r14, rcx" and e.get(0x0065598E) == "cmp dword ptr [rax + 0x168], 0xb000"
      and e.get(0x0065599A) == "mov eax, dword ptr [rip + 0x26a1d98]" and 0x006559A0 + 0x26A1D98 == 0x02CF7738
      and e.get(0x006559A0) == "shr eax, 4" and e.get(0x006559B0) == "mov byte ptr [r14 + 0x60], al",
      "+0x60 = ([+0x168] >= 0xB000) and bit 4 of 02CF7738")

# P12
z = body(0x0018D0E0)
cz = set(owner(c) for c in callers[0x0018D0E0])
check("P12", q(0x008C6C88) == 0x0018D100 and q(0x008C6C98) == 0x0060CD10 and q(0x008C6CA0) == 0x0018D130
      and z.get(0x0018D0E0) == "lea rax, [rip + 0x739b99]" and 0x0018D0E7 + 0x739B99 == 0x008C6C80
      and calls[0x0018D0E0] == 52 and not refs8(0x0018D0E0) and all(c is not None and calls[c] == 0 for c in cz),
      "0018D0E0 stamps 008C6C80; %d direct call sites, from %d bodies none of which has a direct call site" % (calls[0x0018D0E0], len(cz)))

# P13
dd = [s for s in SECS if s[0] == ".data"][0]
check("P13", all(dd[1] + dd[4] <= a < dd[1] + dd[2] for a in (0x02D27BA0, 0x02D2ADF0, 0x02D2E040)),
      "the three default buffers lie in .data past its raw data (%08X)" % (dd[1] + dd[4]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
