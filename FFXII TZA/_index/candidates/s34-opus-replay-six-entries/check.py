"""S-34: execute the six entries of CONTRACT-persistent-flag-banks.md that sec. 17's differential does not cover, as shipped
code over the shipped data files, and compare each result with a direct decode of the files per the contract
(OPUS, 2026-09-25, block 306).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped; NO application stub; any entry into
a function outside ALLOWED fails the case. ONE IMPORT BRIDGE: 002EF2D0's memset goes through the thunk 00861EC0 -> IAT
slot 008C2A60 = VCRUNTIME140!memset (PE import directory); the slot is pointed at a bridge that performs memset(rcx, dl, r8)
and returns rcx. Only the reset case reaches it. The six entries: 0032A8A0 (authored gate), 00377970 (threshold schedule), 00379160
(new-game list), 002EF2D0 (reset + list), 00377440 (event-memory predicate), 002EF2B0 (payload base). Their whole static
reach is also real: 002EF640, 00265270 (FieldData_GetVariable0), 0032AB60 (SetPrimary) and the import thunk 00861EC0.
Fixtures (planted data only):
  [02ADD0C8] -> shipped mapjumpgroupflagrom.bin ('FLAGROM1', the MJGP_ROM table)     or 0
  [02ADD0D0] -> shipped mapjumpgroupinit.bin    ('FLAGDEF1')                           or 0
  [02ADD0A8] -> shipped eventmemorylist.bin     ('EVMEMLST')                           or 0
  [02098E20] bit 0 and [02098E58] -> a u16 progress word (00265270's two reads)
  the payload at 0x02164480 (the image's own .bss, located by 002EF640) filled per case.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import random
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RAX, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
DATA = r"D:\FFXII_TZA_extract\ps2data\image\ff12"
FILES = {"flagrom": DATA + r"\in\bin\mapjumpgroupflagrom.bin", "init": DATA + r"\in\bin\mapjumpgroupinit.bin",
         "evmem": DATA + r"\common\eventmemorylist.bin"}
IMG, PAYLOAD, PSIZE = 0x120000, 0x2164480, 0x1538
G_FLAGROM, G_INIT, G_EVMEM, G_VARFLAG, G_VARPTR = 0x2ADD0C8, 0x2ADD0D0, 0x2ADD0A8, 0x2098E20, 0x2098E58
STACK, STACK_SZ, RET, DATAPAGE, VARW, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x73000000, 0x74000000
IAT_MEMSET = 0x8C2A60
E = {"gate": 0x32A8A0, "schedule": 0x377970, "newgame_list": 0x379160, "reset": 0x2EF2D0, "evmem_absent": 0x377440,
     "payload_base": 0x2EF2B0}
ALLOWED = set(E.values()) | {0x2EF640, 0x265270, 0x32AB60, 0x861EC0}

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
blob = {k: open(p, "rb").read() for k, p in FILES.items()}
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
uc.mem_map(DATAPAGE, 0x10000)
uc.mem_map(VARW, 0x1000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_map(BRIDGE, 0x1000)
uc.mem_write(BRIDGE, bytes([0xC3]))
uc.mem_write(IAT_MEMSET, struct.pack("<Q", BRIDGE))
ADDR = {}
cur = DATAPAGE
for k in ("flagrom", "init", "evmem"):
    ADDR[k] = cur
    uc.mem_write(cur, blob[k])
    cur += (len(blob[k]) + 0xFFF) & ~0xFFF
state = {"bad": [], "faults": [], "entered": set(), "bridge": []}


def on_code(u, a, n, _):
    if a == BRIDGE:
        dst, val, cnt = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF, u.reg_read(UC_X86_REG_R8)
        u.mem_write(dst, bytes([val]) * cnt)
        u.reg_write(UC_X86_REG_RAX, dst)
        state["bridge"].append(["%08X" % dst, val, cnt])
        return
    if a in FSTARTS:
        state["entered"].add(a)
        if a not in ALLOWED:
            state["bad"].append("%08X" % a)
            u.emu_stop()


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def setup(flagrom=True, init=True, evmem=True, progress=None):
    uc.mem_write(G_FLAGROM, struct.pack("<Q", ADDR["flagrom"] if flagrom else 0))
    uc.mem_write(G_INIT, struct.pack("<Q", ADDR["init"] if init else 0))
    uc.mem_write(G_EVMEM, struct.pack("<Q", ADDR["evmem"] if evmem else 0))
    if progress is None:
        uc.mem_write(G_VARFLAG, bytes([0]))
    else:
        uc.mem_write(G_VARFLAG, bytes([1]))
        uc.mem_write(G_VARPTR, struct.pack("<Q", VARW))
        uc.mem_write(VARW, struct.pack("<H", progress & 0xFFFF))


def call(entry, rcx=0, rdx=0):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
    state["bad"], state["faults"], state["entered"], state["bridge"] = [], [], set(), []
    try:
        uc.emu_start(entry, RET, count=2000000)
    except UcError as e:
        state["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]
    return uc.reg_read(UC_X86_REG_RAX), ok


def payload():
    return bytes(uc.mem_read(PAYLOAD, PSIZE))


def set_payload(b):
    uc.mem_write(PAYLOAD, b)


# ---- the decode (contract sec. 7, 8, 12; files parsed with the readers' layout: u16 count at +8, u16 entries from +0x0A) ----
def u16s(b):
    n = struct.unpack_from("<H", b, 8)[0]
    return [struct.unpack_from("<H", b, 0xA + 2 * i)[0] for i in range(n)]


FR = blob["flagrom"]
FR_N = struct.unpack_from("<H", FR, 8)[0]


def schedule(idx, progress, gated=True):
    """sec. 7: parity of thresholds passed, bit 15 ends the list; offset 0 = no schedule; idx >= count -> false."""
    if not (0 <= idx < FR_N):
        return 0
    o = struct.unpack_from("<H", FR, 0xA + 2 * idx)[0]
    if o == 0:
        return 0
    p = struct.unpack("<h", struct.pack("<H", progress & 0xFFFF))[0] if gated else 0
    ans = 0
    while True:
        e = struct.unpack_from("<H", FR, o)[0]
        o += 2
        if p < (e & 0x7FFF):
            return ans
        ans ^= 1
        if e & 0x8000:
            return ans


def gate(v, pl, progress):
    """sec. 12: idx = v & 0x3FFF; bit 14 -> schedule(idx); else 0 -> 1, 1 -> 0, idx < 0x200 -> Primary bit, else 0."""
    idx = v & 0x3FFF
    if v & 0x4000:
        return schedule(idx, progress)
    if idx == 0:
        return 1
    if idx == 1 or idx >= 0x200:
        return 0
    return (pl[0x14F4 + (idx >> 3)] >> (idx & 7)) & 1


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", {k: v for k, v in kw.items() if k in ("n", "mismatches", "note")}))


# 1. payload base
got, ok = call(E["payload_base"])
record("payload_base_002EF2B0", ok and got == PAYLOAD, n=1, got="%08X" % got, expect="%08X" % PAYLOAD)

# 2. schedule 00377970: every index (incl. count, count+1, 0x3FFF) x progress at every threshold +-1, 0, extremes; ungated
thresholds = set()
for i in range(FR_N):
    o = struct.unpack_from("<H", FR, 0xA + 2 * i)[0]
    while o:
        e = struct.unpack_from("<H", FR, o)[0]
        thresholds.add(e & 0x7FFF)
        o += 2
        if e & 0x8000:
            break
progs = sorted({0, 1, 0x7FFF, 0x8000, 0xFFFF} | {t + d for t in thresholds for d in (-1, 0, 1) if 0 <= t + d <= 0xFFFF})
mism, n, notret, zero_off = [], 0, [], []
for idx in list(range(FR_N)) + [FR_N, FR_N + 1, 0x3FFF]:
    if idx < FR_N and struct.unpack_from("<H", FR, 0xA + 2 * idx)[0] == 0:
        zero_off.append(idx)
    for p in progs:
        setup(progress=p)
        got, ok = call(E["schedule"], idx)
        n += 1
        if not ok:
            notret.append([idx, p])
        if (got & 0xFFFFFFFF) != schedule(idx, p):
            mism.append([idx, p, got & 0xFFFFFFFF, schedule(idx, p)])
setup(progress=None)
ungated = [idx for idx in range(FR_N) if (call(E["schedule"], idx)[0] & 0xFFFFFFFF) != schedule(idx, 0, gated=False)]
setup(flagrom=False, progress=0x7FFF)
nullt = [idx for idx in (0, 1, 5) if call(E["schedule"], idx) != (0, True)]
record("schedule_00377970", not mism and not notret and not ungated and not nullt, n=n, mismatches=len(mism),
       detail=mism[:20], not_returned=notret[:10], progress_values=len(progs), distinct_thresholds=len(thresholds),
       zero_offset_indexes=zero_off, ungated_mismatch=ungated[:10], null_table_mismatch=nullt,
       note="count=%d; ungated ([02098E20] bit0 clear) reads progress 0" % FR_N)

# 2b. schedule, negative index (a direct caller; the gate never passes one): observed, not decoded by the contract
setup(progress=0x7FFF)
neg = {}
for idx in (-1, -2, -5):
    got, ok = call(E["schedule"], idx)
    neg[str(idx)] = [got & 0xFFFFFFFF, ok, state["faults"][:2]]
results["schedule_negative_index_observed"] = {"observed": neg, "note": "00377970 bounds with cmp ecx,eax / jge (signed), then movsxd: "
                                               "a negative index reads the u16 at table+0x0A+2*idx, i.e. the header"}
print("schedule_negative_index_observed   ", neg)

# 3. gate 0032A8A0: all 65,536 u16 encodings, two Primary payloads, two progress values; plus the 32-bit upper half ignored
rng = random.Random(0x34)
mism, n, notret = [], 0, []
for pv in (0x0000, 0x7FFF):
    for fill in ("random", "ones"):
        pl = bytearray(PSIZE)
        pl[0x14F4:0x1534] = bytes(rng.randrange(256) for _ in range(64)) if fill == "random" else b"\xFF" * 64
        set_payload(bytes(pl))
        setup(progress=pv)
        for v in range(0x10000):
            got, ok = call(E["gate"], v)
            n += 1
            if not ok:
                notret.append(v)
            if (got & 0xFFFFFFFF) != gate(v, pl, pv):
                mism.append([v, pv, fill, got & 0xFFFFFFFF, gate(v, pl, pv)])
        if pv == 0x7FFF and fill == "random":
            upper = [v for v in (0x0054, 0x400B, 0x0107, 0x4004) if (call(E["gate"], 0xABCD0000 | v)[0] & 0xFFFFFFFF) != gate(v, pl, pv)]
sites = [0x4004, 0x4006, 0x4007, 0x4008, 0x4009, 0x400A, 0x400B, 0x400C, 0x400D, 0x4010, 0x4011, 0x4067, 0xFFFF,
         0x0001, 0x0002, 0x0054, 0x005E, 0x006F, 0x0107]
setup(progress=0x7FFF)
site_vals = {"%04X" % v: call(E["gate"], v)[0] & 0xFFFFFFFF for v in sites}
record("gate_0032A8A0", not mism and not notret and not upper and site_vals["FFFF"] == 0, n=n, mismatches=len(mism),
       detail=mism[:20], not_returned=notret[:10], upper_half_ignored=not upper, call_site_ids_at_progress_7FFF=site_vals,
       note="gate(0xFFFF) = %d" % site_vals["FFFF"])

# 4. new-game list 00379160 over the shipped mapjumpgroupinit.bin, zero payload
ids = u16s(blob["init"])
set_payload(bytes(PSIZE))
setup()
got, ok = call(E["newgame_list"])
pl = payload()
exp = bytearray(PSIZE)
for i in ids:
    if 2 <= i <= 0x1FF:
        exp[0x14F4 + (i >> 3)] |= 1 << (i & 7)
changed = [o for o in range(PSIZE) if pl[o] != exp[o]]
set_bits = sorted(i for i in range(0x200) if (pl[0x14F4 + (i >> 3)] >> (i & 7)) & 1)
set_payload(bytes(PSIZE))
setup(init=False)
null_ok = call(E["newgame_list"])[1] and payload() == bytes(PSIZE)
record("newgame_list_00379160", ok and not changed and null_ok, n=len(ids), mismatches=len(changed),
       list_count=len(ids), list_first_entry="%04X" % ids[0], primary_bits_set=len(set_bits),
       bits_set=["%04X" % b for b in set_bits], bytes_outside_primary_written=[o for o in range(PSIZE) if pl[o] and not 0x14F4 <= o < 0x1534],
       null_table_writes_nothing=null_ok,
       note="%d list entries, %d Primary bits set" % (len(ids), len(set_bits)))

# 5. reset 002EF2D0: payload and 16 guard bytes each side filled with 0xA5
uc.mem_write(PAYLOAD - 16, b"\xA5" * (PSIZE + 32))
setup()
got, ok = call(E["reset"])
after = bytes(uc.mem_read(PAYLOAD - 16, PSIZE + 32))
body = after[16:16 + PSIZE]
guards_ok = after[:16] == b"\xA5" * 16 and after[16 + PSIZE:] == b"\xA5" * 16
body_ok = body == bytes(exp)
record("reset_002EF2D0", ok and guards_ok and body_ok, n=1, mismatches=0 if body_ok else sum(1 for a, b in zip(body, exp) if a != b),
       guard_bytes_untouched=guards_ok, body_equals_zero_plus_list=body_ok, functions_entered=sorted("%08X" % a for a in state["entered"]),
       memset_bridge_calls=state["bridge"],
       note="memset size 0x1538 bounded by the guards; tail jump applies the list")

# 6. event-memory predicate 00377440: all u16 ids, a set of 32-bit ids, null table
lst = set(u16s(blob["evmem"]))
setup()
mism, n = [], 0
for v in list(range(0x10000)) + [0x10000, 0x10031, 0x7FFFFFFF, -1, -0x10000 + 0x31]:
    got, ok = call(E["evmem_absent"], v)
    n += 1
    expv = 0 if (0 <= v <= 0xFFFF and v in lst) else 1
    if not ok or (got & 0xFFFFFFFF) != expv:
        mism.append([v, got & 0xFFFFFFFF, expv, ok])
setup(evmem=False)
null_vals = [call(E["evmem_absent"], v)[0] & 0xFFFFFFFF for v in (0, 0x31, 5)]
present = sorted("%04X" % v for v in lst)
record("evmem_absent_00377440", not mism and null_vals == [1, 1, 1], n=n, mismatches=len(mism), detail=mism[:20],
       listed_ids=present, null_table_returns=null_vals,
       note="0 when listed (inverted), 1 otherwise; the 32-bit id is compared whole")

json.dump({"pass": sum(1 for k, v in results.items() if v.get("pass_")), "total": sum(1 for v in results.values() if "pass_" in v),
           "ok": allok, "files": {k: {"path": p, "sha256": hashlib.sha256(blob[k]).hexdigest(), "bytes": len(blob[k])} for k, p in FILES.items()},
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1)
print("%d/%d pass" % (sum(1 for v in results.values() if v.get("pass_")), sum(1 for v in results.values() if "pass_" in v)))
