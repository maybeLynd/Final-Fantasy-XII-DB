"""UQ-218 @FEF arm: the two start-up path tables and their join (SWE2-DATA 2026-09-30), static on the certified image.

T1 = 02B64380, filled by 0040A230 (called at start-up through 00409F80, CON-195): qword[fold(stem)] = .rdata path.
T2 = [01F81160]+0x228 (the file-layer object built by 001A11B0 / 0019F620), filled by 0019FFD0:
     qword[obj + 0x228 + 8*(letter*0x500 + num)] = .rdata path, read by 001A09E0 for a path ending ".cm" (letter at
     len-8, four digits at len-7..len-4, num < 0x500, byte flag obj+0x1A1+letter).
The @FEF arm of 00409FE0: row = T1[fold(@FEF name)] (null -> fault store at 0040A135); 001D6EC0(row) = T2 lookup of
the row's own path; strstr(result, "chara\\h") -> sscanf "%d.efx" -> 003B3B10(handle, n or -1).
The file layer (001A0CF0 / 001A0E50) uses the same T2 lookup to append the companion file after the main file and
store the main length in the buffer's last dword, which is the payload offset 00409FE0 hands 003B38B0.
Prints: T1 / T2 row counts, the join, companion kinds, and whether each path is an archive entry (A17 index if given).
"""
import os, re, struct, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, BASE  # noqa: E402  (section-aware reads of the SHA-checked image)
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False


def cstr(a):
    o = off(a)
    e = d.index(b"\0", o)
    return d[o:e].decode("latin-1")


def body(start, size):
    o = off(start)
    return list(md.disasm(d[o:o + size], start))


def rip_target(ins):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", ins.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return ins.address + ins.size + (v if m.group(1) == "+" else -v)


fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


# ---- T2: 0019FFD0 ----
regs, t2 = {}, {}
for ins in body(0x0019FFD0, 0x7DA):
    if ins.mnemonic == "lea" and "rip" in ins.op_str:
        regs[ins.op_str.split(",")[0].strip()] = rip_target(ins)
    elif ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [rbx + 0x"):
        m = re.match(r"qword ptr \[rbx \+ 0x([0-9a-f]+)\], (\w+)", ins.op_str)
        if m and m.group(2) in regs:
            disp = int(m.group(1), 16)
            if 0x228 <= disp < 0x228 + 0x140000:
                idx = (disp - 0x228) // 8
                t2[(idx // 0x500, idx % 0x500)] = cstr(regs[m.group(2)])
check("T2 rows decoded from 0019FFD0", len(t2) > 0, "%d rows" % len(t2))
kinds = collections.Counter()
for (L, n), s in t2.items():
    kinds[os.path.splitext(s)[1].lower() + (" chara\\h" if "chara\\h" in s.lower() else "")] += 1
print("  T2 companion kinds:", dict(kinds))
print("  T2 sample:", [("%s%04d" % (chr(L), n), s) for (L, n), s in sorted(t2.items())[:4]])

# ---- T1: 0040A230 ----
regs, t1 = {}, {}
T1 = 0x02B64380
for ins in body(0x0040A230, 0x40AA20 - 0x40A230):
    if ins.mnemonic == "lea" and "rip" in ins.op_str:
        regs[ins.op_str.split(",")[0].strip()] = rip_target(ins)
    elif ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [rip"):
        dst = rip_target(ins)
        src = ins.op_str.split(",")[1].strip()
        if dst is not None and src in regs and T1 <= dst < T1 + 0x400000:
            t1[(dst - T1) // 8] = cstr(regs[src])
    elif ins.mnemonic == "ret":
        break
check("T1 rows decoded from 0040A230", len(t1) == 144, "%d rows (page: 144)" % len(t1))


def t2_key(path):
    """001A09E0's rule, for a path ending .cm."""
    if len(path) <= 8 or not path.lower().endswith(".cm"):
        return None
    L = ord(path[-8])
    digits = path[-7:-3]
    if not digits.isdigit():
        return None           # 001A09E0 folds any four bytes; every T1 row has four digits here (checked below)
    num = int(digits)
    return (L, num) if num < 0x500 else None


join = collections.Counter()
hnums = []
for k, p in sorted(t1.items()):
    key = t2_key(p)
    comp = t2.get(key) if key else None
    if comp is None:
        join["T1 row with no T2 companion"] += 1
    elif "chara\\h" in comp.lower():
        join["companion chara\\h%d.efx"] += 1
        m = re.search(r"chara\\h(\d+)\.efx", comp, re.I)
        hnums.append(int(m.group(1)) if m else None)
    else:
        join["companion other"] += 1
print("  T1 -> T2 join:", dict(join))
check("J every T1 row keys a T2 companion chara\\h%d.efx", join["companion chara\\h%d.efx"] == len(t1) == 144, str(dict(join)))
print("  external effect numbers:", sorted(set(hnums))[:20], "... n=%d rows, %d distinct companions" % (len(hnums), len(set(t2.values()))))
if os.path.isdir("D:/FFXII_TZA_extract/ps2data/effect_finish/jp/chara"):
    shipped = sorted(f for f in os.listdir("D:/FFXII_TZA_extract/ps2data/effect_finish/jp/chara") if f.lower().startswith("h") and f.lower().endswith(".efx"))
    named = {os.path.basename(v.replace(chr(92), "/")).lower() for v in t2.values()}
    print("  shipped chara/h*.efx: %d; named by T2: %d; shipped but not named: %s" % (len(shipped), len(named), [f for f in shipped if f.lower() not in named]))

# archive membership of every path, if the extract is present
EX = "D:/FFXII_TZA_extract"
if os.path.isdir(EX):
    def exists(p):
        q = p.replace("\\", "/")
        q = re.sub(r"^PS2Data/", "ps2data/", q, flags=re.I)
        return os.path.isfile(os.path.join(EX, q.lower())) or os.path.isfile(os.path.join(EX, q))
    miss1 = [p for p in t1.values() if not exists(p)]
    miss2 = [p for p in t2.values() if not exists(p)]
    print("  extract membership: T1 %d/%d, T2 %d/%d" % (len(t1) - len(miss1), len(t1), len(t2) - len(miss2), len(t2)))
    check("X every T1 model and T2 companion is a shipped file", not miss1 and not miss2)
    if miss2[:3]:
        print("  T2 not in extract (sample):", miss2[:3])

EXPECT = {
    0x0040A11C: "lea rsi, [rip + 0x275a25d]",            # T1 = 02B64380
    0x0040A135: "mov dword ptr [0], esi",                # null row -> fault store
    0x0040A16F: "mov edx, dword ptr [rax + r14 - 4]",    # the buffer's last dword = the companion's offset
    0x0040A174: "call 0x3b38b0",                         # effect instance from the appended companion
    0x0040A17F: "call 0x1d6ec0",                         # T2 lookup of the row's own path
    0x0040A193: "call qword ptr [rip + 0x4b886f]",       # strstr(result, "chara\h")
    0x0040A1AE: "call 0x18a330",                         # sscanf(q + 7, "%d.efx")
    0x0040A1C4: "call 0x3b3b10",                         # record n
    0x001A0A7F: "mov rax, qword ptr [r11 + rcx*8 + 0x228]",
    0x0019FFF3: "add rcx, 0x228",                        # 0019FFD0 clears the 0x140000-byte table first
    0x001A0F4E: "mov dword ptr [rax + rbp - 4], edi",    # the file layer stores the main length in the last dword
    0x003B3B2C: "mov dword ptr [r8 + 0x30], edx",        # 003B3B10: n -> effect record +0x30
}
_bad = []
for a, t in EXPECT.items():
    o = off(a); x = next(md.disasm(d[o:o + 16], a))
    if "%s %s" % (x.mnemonic, x.op_str) != t:
        _bad.append("%08X %s %s" % (a, x.mnemonic, x.op_str))
check("P the arm's instructions", not _bad, "%d sites%s" % (len(EXPECT), "" if not _bad else " - " + "; ".join(_bad)))
check("K the strings", cstr(0x00D122F0) == "chara\\h" and cstr(0x00D122F8) == "%d.efx", "%r %r" % (cstr(0x00D122F0), cstr(0x00D122F8)))
print("FAILS %d" % fails)
