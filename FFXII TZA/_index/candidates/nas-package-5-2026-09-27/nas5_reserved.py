"""nas5_reserved.py - review package 5 (DM-2's intent residue): nothing in the image but the blacklist itself separates
the reserved keys - = ] \\ , . / and both Alts from the unreserved [ ; ' (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  R1 the blacklist: 35 u32 ids at 01DF13E0, read by exactly two functions - the file validator 00196550, which scans
     [01DF13E0, 01DF146C) for every slot the file fills, and the assigner 00198A00, which loops 0x23 entries and
     refuses on a match.
  R2 the shipped defaults bind none of them: group 0 (48 codes at 01DF09C0), group 1's codeA / codeB (16 records of
     16 bytes at 01DF0A80) and group 2 (4 codes at 01DF1470) contain no reserved id. Positive control: they do
     contain codes 1 and 3, the two mouse buttons left unreserved.
  R3 the key tables treat both groups alike: the DirectInput scancode table 01F3DAB0 has a non-zero scancode for every
     one of the ten keys, and the reflection registry names all ten (Key_Minus ... Key_Right_Alt beside
     Key_LeftBracket, Key_Semicolon, Key_Apostrophe).
  R4 the injected-text table 01F3DA30 maps '-' '=' ']' '\\' ',' '.' '/' to the reserved codes 81 82 84 85 88 89 90 and
     '[' ';' to the unreserved 83 86, so typed text does not separate them either.
  R5 no call to the three keyboard/pad code pollers (0079E6A0, 0079E650, 0079D670's callers are vtable-only) loads a
     reserved id as an immediate into edx: every rel32 call site of 0079E6A0 and 0079E650 takes its code from a
     register or memory, never a literal.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
FS = sorted(SIZES)
def owner(a):
    i = bisect.bisect_right(FS, a) - 1
    return FS[i] if i >= 0 and a < FS[i] + SIZES[FS[i]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a): return [(x.address, ("%s %s" % (x.mnemonic, x.op_str)).strip()) for x in cs.disasm(d[off(a):off(a) + SIZES[a]], a)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
u32 = lambda a, k: [struct.unpack_from("<I", d, off(a) + 4 * i)[0] for i in range(k)]

RES = u32(0x1DF13E0, 35)
WANT = sorted([2, 81, 82, 84, 85, 88, 89, 90, 119, 122, 123, 125] + list(range(130, 153)))
v = dict(body(0x196550)); a = dict(body(0x198A00))
check("R1 the 35-id blacklist and its two enforcers",
      sorted(RES) == WANT and v.get(0x196566) == "lea rbx, [rip + 0x1c5ae73]" and 0x19656D + 7 + 0x1C5AEF8 == 0x1DF146C
      and v.get(0x19656D) == "lea r9, [rip + 0x1c5aef8]" and v.get(0x1965B4) == "cmp ecx, dword ptr [rax]"
      and a.get(0x198AB4) == "lea rax, [rip + 0x1c58925]" and a.get(0x198AC0) == "cmp r8d, dword ptr [rax]" and a.get(0x198ACF) == "cmp edx, 0x23")

g0 = u32(0x1DF09C0, 48); g1 = u32(0x1DF0A80, 64); g2 = u32(0x1DF1470, 4)
codes = g0 + [g1[4 * r + k] for r in range(16) for k in (2, 3)] + g2
check("R2 no shipped default binds a reserved id (control: codes 1 and 3 are bound)",
      not (set(codes) & set(RES)) and 1 in codes and 3 in codes, "defaults hold %d codes" % len(codes))

TEN = {81: "Key_Minus", 82: "Key_Equals", 84: "Key_RightBracket", 85: "Key_Backslash", 88: "Key_Comma", 89: "Key_Period",
       90: "Key_Slash", 119: "Key_Left_Alt", 122: "Key_Right_Alt", 83: "Key_LeftBracket", 86: "Key_Semicolon", 87: "Key_Apostrophe"}
dik = d[off(0x1F3DAB0):off(0x1F3DAB0) + 125]
check("R3 scancode and reflection-name tables cover reserved and unreserved keys alike",
      all(dik[c - 28] != 0 for c in TEN) and all(d.count(nm.encode() + b"\0") >= 1 for nm in TEN.values()))

asc = d[off(0x1F3DA30):off(0x1F3DA30) + 128]
check("R4 the injected-text table maps reserved and unreserved punctuation alike",
      [asc[ord(ch)] for ch in "-=]\\,./"] == [81, 82, 84, 85, 88, 89, 90] and [asc[ord(ch)] for ch in "[;"] == [83, 86])

T0, TO, TS = [(BASE + v_, ro, rs) for vs, v_, rs, ro in secs if v_ == 0x1000][0]
tb = d[TO:TO + TS]
lits, sites = [], 0
for tgt in (0x79E6A0, 0x79E650):
    for i in range(len(tb) - 5):
        if tb[i] in (0xE8, 0xE9) and T0 + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == tgt:
            s = T0 + i; f = owner(s)
            if f is None: continue
            sites += 1
            prev = [x for x in body(f) if x[0] < s][-8:]
            for _, t in prev:
                m = re.fullmatch(r"mov edx, (0x[0-9a-f]+|\d+)", t)
                if m and int(m.group(1), 0) in RES: lits.append((s, t))
check("R5 no poller call site loads a reserved id as a literal",
      sites >= 15 and lits == [], "%d call sites, reserved literals %s" % (sites, lits))
print("FAILS", fails)
sys.exit(1 if fails else 0)
