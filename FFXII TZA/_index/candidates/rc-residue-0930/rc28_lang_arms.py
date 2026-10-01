"""RC-28 leftover 1: which language index selects which kind-7 path arm (SWE2-DATA 2026-09-30), static.

002DF9A0(lang) builds the path directory 0215F000[kind]. It switches on lang - 1 (0..0xA) through the jump table at
image base + 0x1C04B0 (002DFBB3 cmp eax, 0xA; out of range -> the default arm 002DFF32). The language name table
01E88B00[lang] (read at 002E03F5 for the sprintf of the per-language directory) names each index:
0 JP, 1 US, 2 FR, 3 DE, 4 IT, 5 ES, 6 UK, 7 KR, 8 CH, 9 ASIA, 10 IN, 11 CN.
For every lang 0..11 this script follows the builder from its entry through the switch arm and every unconditional jmp
to the ret, keeping the last value stored to each directory slot (lea reg,[rip+X]; mov [rip+slot], reg), and reports
the kind-7 array (slot 0215F038) with the files it names for fontpack_fs.bin (id 0xD2) and the six .btm (0xDA..0xDF).
Controls: C1 the jump table decodes to 11 arms inside 002DF9A0; C2 the name table spells the twelve languages;
C3 the default path (lang 0) reaches the common tail 002DFF7F.
"""
import os, re, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis, u64, cstr, funcs  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


FN = 0x002DF9A0
body = dis(FN)
at = {x.address: i for i, x in enumerate(body)}
JT = 0x120000 + 0x1C04B0
arms = [0x120000 + struct.unpack_from("<I", d, off(JT + 4 * i))[0] for i in range(11)]
check("C1 the switch table's 11 arms lie inside 002DF9A0", all(FN <= a < FN + funcs[FN] for a in arms),
      " ".join("%08X" % a for a in arms))
LANG = [cstr(u64(0x01E88B00 + 8 * i)) for i in range(12)]
check("C2 the language name table reads JP US FR DE IT ES UK KR CH ASIA IN CN",
      LANG == ["JP", "US", "FR", "DE", "IT", "ES", "UK", "KR", "CH", "ASIA", "IN", "CN"], " ".join(map(str, LANG)))


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


def run(lang):
    slots, regs = {}, {}
    i = 0
    switched = False
    steps = 0
    tail_seen = False
    while i < len(body) and steps < 5000:
        steps += 1
        x = body[i]
        if x.address == 0x002DFF7F:
            tail_seen = True
        if x.address == 0x002DFBC9:   # jmp rcx (the switch)
            k = lang - 1
            tgt = arms[k] if 0 <= k <= 10 else 0x002DFF32
            i = at[tgt]; switched = True; continue
        if x.address == 0x002DFBB6:   # ja default
            if not (0 <= lang - 1 <= 10):
                i = at[0x002DFF32]; continue
            i += 1; continue
        t = rip_t(x)
        if x.mnemonic == "lea" and t is not None:
            regs[x.op_str.split(",")[0]] = t
        elif x.mnemonic == "mov" and t is not None and x.op_str.startswith("qword ptr [rip"):
            reg = x.op_str.rsplit(", ", 1)[1]
            if 0x0215F000 <= t < 0x0215F200 and reg in regs:
                slots[(t - 0x0215F000) // 8] = regs[reg]
        if x.mnemonic == "jmp" and x.op_str.startswith("0x"):
            i = at[int(x.op_str, 16)]; continue
        if x.mnemonic.startswith("j") and x.mnemonic != "jmp":
            i += 1; continue       # conditional branches fall through (none guards the directory stores)
        if x.mnemonic == "ret":
            break
        i += 1
    return slots, switched, tail_seen


rows = []
for lang in range(12):
    slots, sw, tail = run(lang)
    arr = slots.get(7)
    def nm(i):
        p = u64(arr + 8 * i) if arr else None
        s = cstr(p, 260) if p else None
        return s if s else "NULL"
    fp = nm(0xD2)
    btm = [nm(i) for i in range(0xDA, 0xE0)]
    dirs = sorted({s.split(chr(92))[4] for s in [fp] + btm if s != "NULL"})
    rows.append((lang, LANG[lang], arr, fp, btm, tail))
    print("   lang %2d %-4s kind-7 array %s  fontpack_fs: %s" % (lang, LANG[lang], "%08X" % arr if arr else "-",
          fp.split(chr(92))[4] if fp != "NULL" else "NULL"))
    print("        btm dirs: %s" % " ".join(s.split(chr(92))[4] if s != "NULL" else "NULL" for s in btm))
check("C3 the default path (lang 0, JP) reaches the common tail 002DFF7F", rows[0][5])
print("FAILS %d" % FAILS)
