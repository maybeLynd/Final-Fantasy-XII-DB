"""gr18_edges_check.py - GR-18: can a shipped game reach the synthetic reward edge states SECTION-03 executed? (OPUS, 2026-09-30)
Static reads of the certified image plus the shipped .ard files and battle_pack.

E1  zero-count / missing reward descriptor: the install (BattleUnit_ApplyUnitDefinition 0023A570) bounds a unit row's
    +0x22 / +0x24 against the count (+4) of the tables at 02EBF148 / 02EBF140 (.ard slots 5 / 6); a missing descriptor or
    a count of 0 passes the unsigned test. Census of the 166 shipped .ard files: 1,146 unit rows in 162 files, every
    +0x22 / +0x24 inside a present, non-empty table (0 missing, 0 zero-count, 0 out of range).
E2  level-zero reward (defeated level at or below the +0x88 baseline): an enemy's level +0x1C2 and baseline +0x88 are
    written only by the grower 0030C470 (+0x1C2 byte writers: 0030C496 zero, 0030C7BB the step; 003AF80F is a global
    render block). For an enemy the grower runs at init with level 1 / baseline 1 (0023AD37) and from the script verb
    behind 002398F0 (only caller 0050F910) with level = baseline + (00328370() % (n + 1)): level - baseline >= 0 always.
    So level == baseline is the ORDINARY enemy state and below-baseline is unreachable.
E3  the 0xFF member selector: the four-slot divisor (002F8C94-002F8CE5) resolves slot i through 0031B810, which yields
    0xFF only for an empty member byte (class 0x17 admits 0..8 by constant); 002367A0(0xFF) matches identity 0xFFFF only
    after BattleEncodedId_IsValidForClass(2, 0xFF) (00322C50: class 2 = chr_data 02EBF130's count); the shipped chr_data
    has 40 rows, so 0xFF is refused and no unit is selected.
Prints PASS/FAIL per check and FAILS n last. The fourth state (a high relocation base) is a runtime fact - see README.
"""
import glob, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work"))
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


# E1
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
code = txt(0x0023A738) == "mov ecx, dword ptr [rax + 4]" and txt(0x0023A73F) == "movzx eax, word ptr [rsi + 0x22]" \
    and txt(0x0023A743) == "dec ecx" and txt(0x0023A745) == "cmp eax, ecx" and txt(0x0023A747) == "ja 0x23a63a" \
    and txt(0x0023A760) == "movzx eax, word ptr [rsi + 0x24]" and rip(0x0023A72C) == 0x02EBF148 and rip(0x0023A74D) == 0x02EBF140
files = units = 0
bad = {"missing": 0, "zero": 0, "oob": 0}
for f in sorted(glob.glob(os.path.join(WORK, "repos-3f/ard/ard/*.ard"))):
    b = open(f, "rb").read()
    tab = lambda k: None if not u32(b, 0x10 + 4 * k) else (lambda o: (o, u32(b, o + 4), u32(b, o + 8), u32(b, o + 0xC)))(u32(b, 0x10 + 4 * k))
    t2, t5, t6 = tab(2), tab(5), tab(6)
    if not t2 or not t2[1]:
        continue
    files += 1
    for i in range(t2[1]):
        r = t2[0] + t2[3] + i * t2[2]
        units += 1
        for sel, t in ((u16(b, r + 0x22), t5), (u16(b, r + 0x24), t6)):
            if t is None:
                bad["missing"] += 1
            elif t[1] == 0:
                bad["zero"] += 1
            elif sel > t[1] - 1:
                bad["oob"] += 1
check("E1", code and (files, units) == (162, 1146) and bad == {"missing": 0, "zero": 0, "oob": 0},
      "install bounds read; %d files / %d unit rows; %s" % (files, units, bad))
# E2
wr = []
for f in sorted(SZ):
    try:
        ins = list(R.md.disasm(R.at(f, SZ[f]), f))
    except Exception:
        continue
    for i in ins:
        m = re.search(r"byte ptr \[(\w+)(?: \+ \w+\*\d)? \+ (0x[0-9a-f]+)\]", i.op_str.split(",")[0])
        if m and m.group(1) not in ("rip", "rsp", "rbp") and int(m.group(2), 16) == 0x1C2 and i.mnemonic == "mov":
            wr.append((f, i.address))
g = {(f, s): (V.value_at(f, s, "rdx", 2), V.value_at(f, s, "r8", 2)) for f, s in sorted(set(c["calls"].get(0x0030C470, ())))}
ok = wr == [(0x0030C470, 0x0030C496), (0x0030C650, 0x0030C7BB), (0x003AF460, 0x003AF80F)] and txt(0x003AF460).startswith("lea rax, [rip") \
    and txt(0x0030C4B1) == "mov byte ptr [rcx + 0x88], r8b" \
    and txt(0x0023AD37) == "mov edx, 1" and txt(0x0023AD3C) == "mov r12d, edx" and txt(0x0023AD8B) == "mov r8d, r12d" \
    and sorted({f for f, _ in c["calls"].get(0x002398F0, ())}) == [0x0050F910]
ok &= txt(0x0023991D) == "call 0x328370" and txt(0x00239926) == "idiv ecx" and txt(0x0023992F) == "mov r8d, edi" \
    and txt(0x00239932) == "add edx, edi" and txt(0x00239934) == "call 0x30c470"
check("E2", ok,
      "+0x1C2 byte writers %s; enemy init level 1 / baseline 1; the script verb sets level = baseline + rand" % ["%08X" % a for _, a in wr])
# E3
B = 0x120000
cls = lambda k: B + struct.unpack("<I", R.at(B + 0x203054 + 4 * (k - 1), 4))[0]
bp = open(os.path.join(WORK, "repos-2d/vbf/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"), "rb").read()
cd = u32(bp, 0x44)
ok = txt(0x002F8C96) == "call 0x31b810" and txt(0x002F8CE2) == "cmp ebx, 4" \
    and txt(0x0031B81E) == "lea ecx, [r8 + 0x17]" and txt(0x0031B82B) == "mov al, 0xff" and cls(0x17) == 0x00322FAF \
    and txt(0x00322FAF) == "mov ecx, 9" and txt(0x002367B8) == "lea ecx, [r8 + 2]" and txt(0x002367BC) == "call 0x322c50" \
    and txt(0x002367E3) == "cmp edi, 0xff" and txt(0x002367E9) == "mov ecx, 0xffff" and cls(2) == 0x00322C9A \
    and rip(0x00322C9A) == 0x02EBF130 and bp[cd:cd + 4] == b"st2e" and u32(bp, cd + 4) == 40
check("E3", ok, "0xFF reaches 002367A0 only from an empty member byte; class 2 bounds it by chr_data's count %d, so 0xFF is refused"
      % u32(bp, cd + 4))
print("FAILS %d" % fails)
