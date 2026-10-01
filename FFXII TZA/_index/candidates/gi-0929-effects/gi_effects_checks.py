"""gi_effects_checks.py (_index/candidates/gi-0929-effects/) - static regressions for the GI-8..GI-11 effect-element answers (FABLE, 2026-09-29).

Each check re-derives from the shipping image one fact the pages now state, and fails on the reading it corrects.
Runs from any cwd; exit status 1 if any check fails. Needs capstone.

  K1  the "step" is the element's birth: base step 002F2D60 zeroes the age +0x3C/+0x40 and the update count +0x48
      (rejects "the per-frame step")
  K2  00454890 is not an instruction start inside 00454480 and not a function (rejects it as a 0x80-0x97 tail)
  K3  0x73/0x74 update tails are 0052E270/0052F400; 0054C6B0/0054E040 have one raw caller each, in the births
      (rejects 0054C6B0/0054E040 as the update tails)
  K4  0045F600 is called by the 0x67/0x6B births only; 0x67's update calls 004607C0 (rejects 0045F600 as 0x67's tail)
  K5  00377190 (the state-element registry) has exactly four raw callers, the births of 0x40/0x41/0xD0/0x42; the
      registry walker 00377230 is called from MainLoop_Draw / MainLoop_UpdateAndRenderFrame and calls the four apply
      bodies 004640A0 / 00464BD0 / 0047BD30 / 00465690
  K6  0xD0's seventh method 00465120 calls the restore 00465510 and ends by tail-jumping the registry release
      00377360 (rejects "the payload is the seventh method")
  K7  0x40's seventh 00464050 releases the light handle +0x244 through 003ABCA0 and the registry handle +0x24C through
      00377360 (two handles)
  K8  the only writers of [reg+0x298] among the element method bodies 00440000-00500000 are the four heavy births and
      the two thin births 00455D70/004566E0 (which store 0): 0x8D/0x8E always draw resource 0. (The one other writer
      up to 00560000, 0051BC70 at 0051C185, is RenderResourceRoot's phase-2 model pass - reached only by the jmp at
      0041E4EF - and not an effect element; checked too.)
  K9  no cull call (005002E0) in the tails 00523380 (0x68), 00524320 (0x69), 005263F0 (0x6A), 0054C440, 0054DD30
      (0x73/0x74 movers); a positive control tail (0045C450) has one
  K10 dispatch-table facts from effect-type-methods.tsv: 0x89's step is 004524C0, 0x8A's 00453110; 0x86/0x87 share
      update 00450480 with 0x80; 0x97 shares step 00455390 / update 0045B260 with 0x8C
  K11 0x04's walk 004453D0 builds three rings: sinf/cosf of +0x248 and the ring loop bound 2 (r15 <= 2)
  K13 the step dispatcher's only driver, 00441B30, calls it (00441E71) on an element it has just taken off the
      owner's free list +0x120 (00441BEC-00441C0D) and linked into the active list: the step runs on a fresh element
  K14 setup table (005004C0, effect-type-methods.tsv): 0x67 -> 0053A5D0, 0xA0 -> 0053A6F0, 0xA1 -> 0053A790,
      0xA2 -> 0053A840, and 0x68 has no main-range setup (rejects the 0x65 / 0x66 / 0x67 / 0x68 labels)
  K15 0x91's birth 00459420 calls 0020E610 and never 0020E600 (replaced, not added); 0x92's 0045A050 calls 0020E600
  K16 0xAB's builder 0054B3E0 (one raw caller, 0052CB4D): stages 02AEC4B0 (004CF490's template) once and copies
      02AE9BC0 (004DA8A0's template) twice; the default A+D values 0x42 / 0x1001 / 0x45; per-slot stride 0x110 and block
      sizes 0x2D0 (first set slot) / 0x2E0 (further), matching the measurer 0054B3A0's 0x4F0 base
  K18 the authored-type census data (Effect-File-Formats/members/type_census.tsv, written by type_census.py there):
      55 types (the earlier table has 53), 0x04 = 173 and 0xA3 = 447 chunks, 48,868 records, and none of the ten
      unauthored types (rejects the "53 distinct values / 31,635 records" population)
  K17 0xD0's blend block is consumed: 00465CD0 stores +0x4A8; 0041F270 copies +0x4A8/+0x4AC/+0x4B0 to the model
      instance +0x248/+0x24C/+0x250; the instance draw setup 004FD4B0 multiplies the ambient alpha by +0x248 under
      +0x244 bit 0 and reads +0x24C / +0x250 into its render command
  K12 0x41's selection keeps the DARKEST record: 003B4310 compares luminance with comiss/jbe against a running
      minimum initialised to 2.0"""
import struct, sys, os, csv
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
HERE = os.path.dirname(os.path.abspath(__file__))
MEMBERS = os.environ.get("GI_EFFECTS_MEMBERS",   # override only to test staged member files before they are published
                         r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\17-Presentation-Rendering\Effect-File-Formats\members")
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0"), struct.unpack_from("<I", d, o + 12)[0],
                 struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0]))


def off(a):
    r = a - BASE
    for _n, va, vs, ro in secs:
        if va <= r < va + vs:
            return ro + (r - va)


funcs = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass
md = Cs(CS_ARCH_X86, CS_MODE_64)


def ins(fn):
    return list(md.disasm(d[off(fn):off(fn) + funcs[fn]], fn))


def at(fn, a):
    for x in ins(fn):
        if x.address == a:
            return (x.mnemonic + " " + x.op_str).strip()
    return None


text = [s for s in secs if s[0] == b".text"][0]
_raw = None


def raw_callers(target):
    """every E8/E9 rel32 in .text whose target is `target` (includes unlisted code)"""
    global _raw
    if _raw is None:
        _raw = {}
        _n, va, vs, ro = text
        blob = d[ro:ro + vs]
        for i in range(len(blob) - 5):
            if blob[i] in (0xE8, 0xE9):
                src = BASE + va + i
                t = (src + 5 + struct.unpack_from("<i", blob, i + 1)[0]) & 0xFFFFFFFF
                _raw.setdefault(t, []).append(src)
    return _raw.get(target, [])


def containing(a):
    best = None
    for f, s in funcs.items():
        if f <= a < f + s and (best is None or f > best):
            best = f
    return best


def calls(fn):
    return [(x.address, int(x.op_str, 16)) for x in ins(fn)
            if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")]


results = []


def check(name, ok, detail):
    results.append((name, ok))
    print("%s %s  %s" % (name, "PASS" if ok else "FAIL", detail))


# K1
a1, a2, a3 = at(0x2F2D60, 0x2F30DA), at(0x2F2D60, 0x2F30DE), at(0x2F2D60, 0x2F3128)
zero = at(0x2F2D60, 0x2F2DB6)
check("K1", a1 == "mov qword ptr [rbx + 0x40], r14" and a2 == "mov dword ptr [rbx + 0x3c], r14d"
      and a3 == "mov dword ptr [rbx + 0x48], r14d" and zero is not None and "r14d, r14d" in zero,
      "002F2DB6 %r; 002F30DA %r; 002F30DE %r; 002F3128 %r" % (zero, a1, a2, a3))
# K2
starts = {x.address for x in ins(0x454480)}
check("K2", 0x454890 not in starts and 0x454890 not in funcs and 0x45488D in starts and 0x454895 in starts
      and not raw_callers(0x454890),
      "0045488D %r; 00454890 instruction start %s; function %s"
      % (at(0x454480, 0x45488D), 0x454890 in starts, 0x454890 in funcs))
# K3
k3 = (at(0x52D370, 0x52D396) == "call 0x52e270" and at(0x52E3F0, 0x52E416) == "call 0x52f400"
      and raw_callers(0x54C6B0) == [0x52D82C] and raw_callers(0x54E040) == [0x52E9A2])
check("K3", k3, "0052D396 %r; 0052E416 %r; callers 0054C6B0 %s, 0054E040 %s"
      % (at(0x52D370, 0x52D396), at(0x52E3F0, 0x52E416),
         ["%08X" % c for c in raw_callers(0x54C6B0)], ["%08X" % c for c in raw_callers(0x54E040)]))
# K4
c4 = sorted(containing(c) for c in raw_callers(0x45F600))
check("K4", c4 == [0x45FD50, 0x529200] and at(0x45FD10, 0x45FD36) == "call 0x4607c0",
      "0045F600 callers in %s; 0045FD36 %r" % (["%08X" % c for c in c4], at(0x45FD10, 0x45FD36)))
# K5
c5 = sorted(containing(c) for c in raw_callers(0x377190))
w5 = sorted(containing(c) for c in raw_callers(0x377230))
t5 = {t for _a, t in calls(0x377230)}
check("K5", c5 == sorted([0x463FF0, 0x464B30, 0x464F20, 0x47BE20]) and w5 == sorted([0x22B0B0, 0x22B8C0])
      and {0x4640A0, 0x464BD0, 0x47BD30, 0x465690} <= t5,
      "00377190 callers in %s; 00377230 callers in %s" % (["%08X" % c for c in c5], ["%08X" % c for c in w5]))
# K6
c6 = calls(0x465120)
check("K6", any(t == 0x465510 for _a, t in c6) and c6[-1] == (0x4654DE, 0x377360)
      and at(0x377230, 0x3772EA) == "call 0x465690",
      "00465120 last %s; 003772EA %r" % (("%08X>%08X" % c6[-1]) if c6 else None, at(0x377230, 0x3772EA)))
# K7
check("K7", at(0x464050, 0x464059) == "mov ecx, dword ptr [rcx + 0x244]" and at(0x464050, 0x464063) == "call 0x3abca0"
      and at(0x464050, 0x464072) == "mov ecx, dword ptr [rbx + 0x24c]" and at(0x464050, 0x46407D) == "jmp 0x377360",
      "00464059 %r; 00464072 %r" % (at(0x464050, 0x464059), at(0x464050, 0x464072)))
# K8
w8 = []
for f, s in funcs.items():
    if 0x440000 <= f < 0x500000:
        for x in ins(f):
            if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [r") and "+ 0x298]," in x.op_str \
                    and "rsp" not in x.op_str:
                w8.append((x.address, f))
wf = sorted({f for _a, f in w8})
k8 = (wf == sorted([0x455390, 0x455D70, 0x4566E0, 0x457E10, 0x459420, 0x45A050])
      and at(0x455D70, 0x455DA0) == "mov dword ptr [rbx + 0x298], 0"
      and at(0x4566E0, 0x456710) == "mov dword ptr [rbx + 0x298], 0")
k8b = raw_callers(0x51BC70) == [0x41E4EF] and at(0x51BC70, 0x51C185) == "mov dword ptr [rbp + 0x298], 0x20"
check("K8", k8 and k8b, "writers of +0x298 in %s (%d stores); 0051BC70 referrers %s"
      % (["%08X" % f for f in wf], len(w8), ["%08X" % c for c in raw_callers(0x51BC70)]))
# K9
nocull = {f: sum(1 for _a, t in calls(f) if t == 0x5002E0) for f in (0x523380, 0x524320, 0x5263F0, 0x54C440, 0x54DD30)}
ctrl = sum(1 for _a, t in calls(0x45C450) if t == 0x5002E0)
check("K9", all(v == 0 for v in nocull.values()) and ctrl == 1,
      "cull calls %s; control 0045C450 %d" % ({"%08X" % k: v for k, v in nocull.items()}, ctrl))
# K10
rows = {}
for r in csv.reader(open(os.path.join(MEMBERS, "effect-type-methods.tsv")), delimiter="\t"):
    if r and r[0].startswith("0x"):
        rows[int(r[0], 16)] = r
k10 = (rows[0x89][1] == "004524C0" and rows[0x8A][1] == "00453110" and rows[0x86][2] == rows[0x87][2] == rows[0x80][2]
       == "00450480" and rows[0x97][1] == rows[0x8C][1] == "00455390" and rows[0x97][2] == "0045B260")
check("K10", k10, "0x89 step %s, 0x8A step %s, 0x86/0x87 update %s/%s, 0x97 step/update %s/%s"
      % (rows[0x89][1], rows[0x8A][1], rows[0x86][2], rows[0x87][2], rows[0x97][1], rows[0x97][2]))
# K11
k11 = (at(0x4453D0, 0x445560) == "movss xmm6, dword ptr [rdi + 0x248]" and at(0x4453D0, 0x44556B) == "call 0x861f0e"
       and at(0x4453D0, 0x445593) == "call 0x861f08" and at(0x4453D0, 0x445661) == "cmp r15, 2")
check("K11", k11, "00445560 %r; 00445661 %r" % (at(0x4453D0, 0x445560), at(0x4453D0, 0x445661)))
# K12
k12 = (at(0x3B4310, 0x3B46BE) == "comiss xmm13, xmm2" and at(0x3B4310, 0x3B46C2) == "jbe 0x3b46cb"
       and at(0x3B4310, 0x3B4330) == "movss xmm13, dword ptr [rip + 0x19378cf]")
check("K12", k12, "003B46BE %r; 003B46C2 %r" % (at(0x3B4310, 0x3B46BE), at(0x3B4310, 0x3B46C2)))
# K16
k16 = (at(0x54B3E0, 0x54B40A) == "lea r9, [rip + 0x25a109f]" and at(0x54B3E0, 0x54B5A6) == "movaps xmm1, xmmword ptr [rip + 0x259e613]"
       and at(0x54B3E0, 0x54B66D) == "movaps xmm0, xmmword ptr [rip + 0x259e54c]"
       and at(0x54B3E0, 0x54B72F) == "mov qword ptr [rbp + 0x50], 0x42" and at(0x54B3E0, 0x54B737) == "mov qword ptr [rbp + 0x60], 0x1001"
       and at(0x54B3E0, 0x54B73F) == "mov qword ptr [rbp + 0x70], 0x45"
       and at(0x54B3E0, 0x54BBAD) == "mov r10d, 0x2d0" and at(0x54B3E0, 0x54BC3D) == "mov r10d, 0x2e0"
       and at(0x54B3E0, 0x54BCEA) == "add rdx, 0x110" and at(0x54B3A0, 0x54B3A3) == "mov eax, 0x4f0"
       and raw_callers(0x54B3E0) == [0x52CB4D])
check("K16", k16, "0054B40A %r (-> 02AEC4B0); 0054B5A6 / 0054B66D load 02AE9BC0 twice; slot stride 0x110; sizes 0x2D0 / 0x2E0"
      % at(0x54B3E0, 0x54B40A))
# K17
k17 = (at(0x41F270, 0x41F2B2) == "mov eax, dword ptr [rbx + 0x4a8]" and at(0x41F270, 0x41F2B8) == "mov dword ptr [r9 + 0x248], eax"
       and at(0x41F270, 0x41F2C5) == "mov dword ptr [r9 + 0x24c], eax" and at(0x41F270, 0x41F2D2) == "mov dword ptr [r9 + 0x250], eax"
       and at(0x4FD4B0, 0x4FD620) == "test byte ptr [rdi + 0x244], 1" and at(0x4FD4B0, 0x4FD629) == "mulss xmm2, dword ptr [rdi + 0x248]"
       and at(0x4FD4B0, 0x4FDB28) == "movss xmm6, dword ptr [rdi + 0x24c]" and at(0x4FD4B0, 0x4FDB1C) == "mov eax, dword ptr [rdi + 0x250]"
       and at(0x465CD0, 0x465DED) == "movss dword ptr [rdx + 0x4a8], xmm0")
check("K17", k17, "0041F2B8 %r; 004FD629 %r" % (at(0x41F270, 0x41F2B8), at(0x4FD4B0, 0x4FD629)))
# K18
cen = {r["type"]: r for r in csv.DictReader(open(os.path.join(MEMBERS, "type_census.tsv")), delimiter="\t")}
old = {r["type"] for r in csv.DictReader(open(os.path.join(MEMBERS, "effect-type-authored-usage.tsv")), delimiter="\t")}
k18 = (len(cen) == 55 and len(old) == 53 and cen["0x04"]["chunks"] == "173" and cen["0xA3"]["chunks"] == "447"
       and not any(t in cen for t in ("0x03", "0x07", "0x08", "0x70", "0x81", "0x8A", "0x97", "0xA0", "0xA4", "0xA9"))
       and set(cen) - old == {"0x04", "0xA3"} and sum(int(r["chunks"]) for r in cen.values()) == 48868)
check("K18", k18, "type_census.tsv: %d types (earlier table %d), 0x04 %s, 0xA3 %s, total %d"
      % (len(cen), len(old), cen.get("0x04", {}).get("chunks"), cen.get("0xA3", {}).get("chunks"),
         sum(int(r["chunks"]) for r in cen.values())))
# K13
k13 = (at(0x441B30, 0x441BEC) == "mov rdi, qword ptr [rbx + 0x120]" and at(0x441B30, 0x441C0D) == "mov qword ptr [rbx + 0x120], rax"
       and at(0x441B30, 0x441E71) == "call 0x2f3bc0"
       and sorted(containing(c) for c in raw_callers(0x2F3BC0)) == [0x441B30])
check("K13", k13, "00441BEC %r; 00441C0D %r; 00441E71 %r" % (at(0x441B30, 0x441BEC), at(0x441B30, 0x441C0D),
                                                         at(0x441B30, 0x441E71)))
# K14
k14 = (rows[0x67][4] == "0053A5D0" and rows[0xA0][4] == "0053A6F0" and rows[0xA1][4] == "0053A790"
       and rows[0xA2][4] == "0053A840" and rows[0x68][4] == "default" and rows[0x65][4] == "0053A1E0"
       and rows[0x66][4] == "0053A3B0")
check("K14", k14, "setups 0x65 %s 0x66 %s 0x67 %s 0x68 %s 0xA0 %s 0xA1 %s 0xA2 %s" % tuple(
    rows[t][4] for t in (0x65, 0x66, 0x67, 0x68, 0xA0, 0xA1, 0xA2)))
# K15
t91 = [t for _a, t in calls(0x459420)]; t92 = [t for _a, t in calls(0x45A050)]
check("K15", 0x20E610 in t91 and 0x20E600 not in t91 and 0x20E600 in t92 and 0x20E610 not in t92,
      "00459420 calls 0020E610 x%d, 0020E600 x%d" % (t91.count(0x20E610), t91.count(0x20E600)))
fails = [n for n, ok in results if not ok]
print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
