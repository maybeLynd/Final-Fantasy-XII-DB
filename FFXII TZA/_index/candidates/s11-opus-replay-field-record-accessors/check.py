"""S-11: execute the seven field-record accessors (CONTRACT-field-record-accessors.md) as shipped code over the shipped
navimapdata.bin, for every field id, and compare each result with a direct decode of the file (OPUS, 2026-09-25, block 304).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped; NOTHING stubbed; any entry into
a function outside ALLOWED fails. Fixtures: [02ADD100] = the shipped navimapdata.bin (loaded verbatim; SHA-256 recorded) or
0 for the null-table case; the context payload 0x2164480 (+0x1044 = active field id for the implicit accessors) is the
image's own .bss, zero elsewhere (no save override). Decode used for comparison (contract section 2): record i is 3 bytes at
table + 8 + 3*i; u16 = bytes 0..1, byte = byte 2; count = dword [table + 4].
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RAX, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
NAV = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\bin\navimapdata.bin"
IMG, PAYLOAD = 0x120000, 0x2164480
STACK, STACK_SZ, RET, TAB = 0x70000000, 0x100000, 0x71000000, 0x72000000
ACC = {"bit15_implicit": 0x377C20, "bit15": 0x377480, "bit14": 0x377A40, "bits12_13_implicit": 0x377BA0,
       "bits0_11": 0x3779F0, "byte2_bit0_implicit": 0x377700, "byte2_bits4_7_implicit": 0x377C70, "thunk_00320160": 0x320160}
ALLOWED = set(ACC.values()) | {0x3148F0, 0x2EF2B0, 0x2EF640, 0x314AA0, 0x314AC0, 0x314A60}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
if not os.path.isfile(NAV):
    NAV = NAV.replace("\\in\\", "\\us\\")
nav = open(NAV, "rb").read()
count = struct.unpack_from("<I", nav, 4)[0]
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(TAB, (len(nav) + 0xFFFF) & ~0xFFF)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(TAB, nav)
state = {"bad": [], "faults": []}


def on_code(u, a, n, _):
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def call(entry, fid, table=TAB):
    uc.mem_write(0x2ADD100, struct.pack("<Q", table))
    uc.mem_write(PAYLOAD + 0x1044, struct.pack("<i", fid))
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, fid & 0xFFFFFFFFFFFFFFFF)
    state["bad"], state["faults"] = [], []
    try:
        uc.emu_start(entry, RET, count=20000)
    except UcError as e:
        state["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    return struct.unpack("<i", struct.pack("<I", uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF))[0], ok


IMPLICIT = {"bit15_implicit", "bits12_13_implicit", "byte2_bit0_implicit", "byte2_bits4_7_implicit", "thunk_00320160"}


def decode(name, fid, gate=0):
    """Expected value from the file per contract section 2, with two measured refinements (block 304):
    (a) the implicit accessors take the id through 003148F0, which clamps a negative id to 0 (cmovs at 00314903);
    (b) 00377700's reject path zeroes the byte, and its inverted test (not / test al,1) turns that into 1, so a null table
        or an out-of-range id reads 1 - unless the save gate [payload+0x1062] bit 0 is set, which forces 0."""
    if name in IMPLICIT and fid < 0:
        fid = 0
    if name == "byte2_bit0_implicit":
        if gate & 1:
            return 0
        if not (0 <= fid < count):
            return 1
    if not (0 <= fid < count):
        return -1 if name == "bits0_11" else 0
    w = struct.unpack_from("<H", nav, 8 + 3 * fid)[0]
    b = nav[8 + 3 * fid + 2]
    return {"bit15_implicit": w >> 15, "bit15": w >> 15, "bit14": (w >> 14) & 1, "bits12_13_implicit": (w >> 12) & 3,
            "thunk_00320160": (w >> 12) & 3, "bits0_11": (-1 if (w & 0xFFF) == 0xFFF else w & 0xFFF),
            "byte2_bit0_implicit": 1 - (b & 1), "byte2_bits4_7_implicit": b >> 4}[name]


results = {}
allok = True
ids = list(range(count)) + [count, count + 1, 0x7FFFFFFF, -1, -5]
for name, entry in ACC.items():
    mism, notret, hist = [], [], {}
    for fid in ids:
        got, ok = call(entry, fid)
        if not ok:
            notret.append(fid)
        exp = decode(name, fid)
        if got != exp:
            mism.append([fid, got, exp])
        if 0 <= fid < count:
            hist[got] = hist.get(got, 0) + 1
    null_got, null_ok = call(entry, 0, table=0)
    null_exp = -1 if name == "bits0_11" else (1 if name == "byte2_bit0_implicit" else 0)
    ok = not mism and not notret and null_ok and null_got == null_exp
    allok &= ok
    results[name] = {"entry": "%08X" % entry, "pass": ok, "ids_tested": len(ids), "mismatches": mism[:20], "n_mismatch": len(mism),
                     "not_returned": notret[:10], "null_table": [null_got, null_ok], "value_histogram": {str(k): v for k, v in sorted(hist.items())}}
    print("%-24s %s  mismatches=%d  null=%s  histogram=%s" % (name, "PASS" if ok else "FAIL", len(mism), null_got, dict(sorted(hist.items()))))

# save gate: [payload+0x1062] bit 0 set -> 00377700 returns 0 for every id
uc.mem_write(PAYLOAD + 0x1062, bytes([1]))
gmis = [fid for fid in ids if call(0x377700, fid)[0] != decode("byte2_bit0_implicit", fid, gate=1)]
uc.mem_write(PAYLOAD + 0x1062, bytes([0]))
results["byte2_bit0_save_gate"] = {"entry": "00377700", "pass": not gmis, "mismatches": gmis[:10]}
allok &= not gmis
print("%-24s %s  mismatches=%d" % ("byte2_bit0_save_gate", "PASS" if not gmis else "FAIL", len(gmis)))

json.dump({"pass": sum(1 for v in results.values() if v["pass"]), "total": len(results), "ok": allok, "records": count,
           "navimapdata": NAV, "navimapdata_sha256": hashlib.sha256(nav).hexdigest(), "results": results},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
print("%d/%d pass over %d records" % (sum(1 for v in results.values() if v["pass"]), len(results), count))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
