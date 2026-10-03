"""S-27: execute BattleFormula_BuildPeriodicStatusResult (00385DF0) and its five stages as shipped code, attribute every memory
write to the stage that made it, and test CONTRACT-periodic-tick.md's section 3 ownership matrix, I-2..I-7, section 9's Regen
draw and section 12's reproduction statement (OPUS, 2026-09-25, block 310).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Whole SHA-asserted image mapped. NO application stub. ALLOWED = the
builder's static closure (21 functions) + the MT19937 body behind the 00379CD0 thunk (00863BF0 and its seed / regenerate
helpers 00866D60 / 00866B90); entering anything else fails a case. ONE IMPORT BRIDGE: memset (thunk 00861EC0 -> IAT
008C2A60, VCRUNTIME140!memset), used by stage 1.
Fixtures (planted data only): the stats block (rcx; status words +0x3C / +0x64 and +0x68 / +0x78, duration +0xBC, beat
+0x13C, effect-slot timers +0x17C, +0x1C2 the Regen divisor), the two authored tables behind [02EBF118] (status rows:
+9 beat factor) and [02EBF040] (effect rows: +6 slot byte), each {+4 count, +8 u16 stride, +0xC encoded rows}; the decode
base q[01F83530] = 0; the frame base [01DFE0B4]. The generator is the image's own, lazily seeded by the shipped code.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RAX

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, WORLD, BRIDGE = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
STATS, RESULT, STBL, SROWS, ETBL, EROWS = WORLD, WORLD + 0x2000, WORLD + 0x3000, WORLD + 0x3100, WORLD + 0x4000, WORLD + 0x4100
RSIZE, GUARD = 0x148, 0x40
BUILDER = 0x385DF0
STAGES = {0x3848E0: 1, 0x386C70: 2, 0x385570: 3, 0x385CA0: 4, 0x386860: 5}
G_STATUS_TBL, G_EFFECT_TBL, G_DECODE, G_FRAMELIMIT = 0x2EBF118, 0x2EBF040, 0x1F83530, 0x1DFE0B4
IAT_MEMSET = 0x8C2A60
RNG_RET = 0x386D2C                                     # the instruction after Regen's call 00379CD0

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


ALLOWED = closure(BUILDER) | closure(0x863BF0) | {0x863BF0, 0x866D60, 0x866B90}
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40

uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
uc.mem_map(STACK, STACK_SZ)
uc.mem_map(RET, 0x1000)
uc.mem_map(WORLD, 0x10000)
uc.mem_map(BRIDGE, 0x1000)
uc.mem_write(RET, bytes([0xF4]))
uc.mem_write(BRIDGE, bytes([0xC3]))
uc.mem_write(IAT_MEMSET, struct.pack("<Q", BRIDGE))
state = {"bad": [], "faults": [], "stage": 0, "order": [], "writes": [], "rng": [], "memset": []}


def on_code(u, a, n, _):
    if a == BRIDGE:
        d, v, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF, u.reg_read(UC_X86_REG_R8)
        state["memset"].append([state["stage"], d, v, c])
        for i in range(c):                     # attribute the fill to the calling stage, byte by byte
            state["writes"].append((state["stage"], d + i, 1))
        u.mem_write(d, bytes([v]) * c)
        u.reg_write(UC_X86_REG_RAX, d)
        return
    if a in STAGES:
        state["stage"] = STAGES[a]
        state["order"].append(STAGES[a])
    if a == RNG_RET:
        state["rng"].append(u.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF)
    if a in FSTARTS and a not in ALLOWED:
        state["bad"].append("%08X" % a)
        u.emu_stop()


def on_write(u, ac, a, n, v, _):
    if not (STACK <= a < STACK + STACK_SZ):
        state["writes"].append((state["stage"], a, n))


def on_bad(u, ac, a, n, v, _):
    state["faults"].append("%08X" % a)
    return False


uc.hook_add(UC_HOOK_CODE, on_code)
uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)


def world(frame=1, w3c=0, w64=0, w68=b"", beat=None, dur=None, slots=None, regen_div=7, srows=None, erows=None, ecount=0):
    uc.mem_write(WORLD, bytes(0x10000))
    s = bytearray(0x800)
    struct.pack_into("<II", s, 0x3C, w3c, 0)
    struct.pack_into("<I", s, 0x64, w64)
    s[0x68:0x68 + len(w68)] = w68
    for k, v in (dur or {}).items():
        struct.pack_into("<i", s, 0xBC + 4 * k, v)
    for k, v in (beat or {}).items():
        struct.pack_into("<h", s, 0x13C + 2 * k, v)
    for k, v in (slots or {}).items():
        struct.pack_into("<h", s, 0x17C + 2 * k, v)
    s[0x1C2] = regen_div
    struct.pack_into("<i", s, 0x24, 1000)             # a max-HP-like value for the poison arm
    struct.pack_into("<i", s, 0x48, 500)
    uc.mem_write(STATS, bytes(s))
    uc.mem_write(RESULT, b"\xCC" * (RSIZE + GUARD))
    # status table [02EBF118]: stride 0x10, rows with +9 beat factor
    uc.mem_write(STBL, struct.pack("<IIHHI", 0, 32, 0x10, 0, SROWS))
    rows = bytearray(0x10 * 32)
    for k, v in (srows or {}).items():
        rows[0x10 * k + 9] = v
    uc.mem_write(SROWS, bytes(rows))
    uc.mem_write(ETBL, struct.pack("<IIHHI", 0, ecount, 0x10, 0, EROWS))
    er = bytearray([0xFF] * (0x10 * 128))
    for k, v in (erows or {}).items():
        er[0x10 * k + 6] = v
    uc.mem_write(EROWS, bytes(er))
    uc.mem_write(G_STATUS_TBL, struct.pack("<Q", STBL))
    uc.mem_write(G_EFFECT_TBL, struct.pack("<Q", ETBL))
    uc.mem_write(G_DECODE, struct.pack("<Q", 0))
    uc.mem_write(G_FRAMELIMIT, struct.pack("<i", frame))


def run():
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, STATS)
    uc.reg_write(UC_X86_REG_RDX, RESULT)
    state.update(bad=[], faults=[], stage=0, order=[], writes=[], rng=[], memset=[])
    try:
        uc.emu_start(BUILDER, RET, count=2000000)
    except UcError as e:
        state["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not state["bad"] and not state["faults"]


def ranges(offs):
    offs = sorted(set(offs))
    out, i = [], 0
    while i < len(offs):
        j = i
        while j + 1 < len(offs) and offs[j + 1] == offs[j] + 1:
            j += 1
        out.append("+%X" % offs[i] if i == j else "+%X..+%X" % (offs[i], offs[j]))
        i = j + 1
    return out


def ownership():
    own = {k: {"result": set(), "stats": set(), "other": set()} for k in range(0, 6)}
    for st, a, n in state["writes"]:
        for b in range(a, a + n):
            if RESULT <= b < RESULT + RSIZE + GUARD:
                own[st]["result"].add(b - RESULT)
            elif STATS <= b < STATS + 0x800:
                own[st]["stats"].add(b - STATS)
            else:
                own[st]["other"].add(b)
    return own


def rd(fmt, a):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


# independent MT19937 (init_genrand(5489), genrand_int32) for the Regen check
class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xFFFFFFFF
        self.i = 624

    def next(self):
        if self.i >= 624:
            for k in range(624):
                y = (self.mt[k] & 0x80000000) | (self.mt[(k + 1) % 624] & 0x7FFFFFFF)
                self.mt[k] = self.mt[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
            self.i = 0
        y = self.mt[self.i]
        self.i += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y & 0xFFFFFFFF


mt = MT(5489)
results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-36s %s  %s" % (name, "PASS" if ok else "FAIL", {k: v for k, v in kw.items() if k in ("note",)}))


# A. no statuses: the order, and the ownership matrix of an empty tick
world()
ok = run()
own = ownership()
matrix = {str(k): {"result": ranges(v["result"]), "stats": ranges(v["stats"]), "other": ["%08X" % x for x in sorted(v["other"])][:8]}
          for k, v in own.items() if any(v.values())}
st1 = own[1]["result"]
i3_claim = {0x2C, 0x2D, 0x2E, 0x2F, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x13C, 0x13D, 0x13E, 0x13F}
record("A_order_and_empty_ownership", ok and state["order"] == [1, 2, 3, 4, 5] and not any(own[k]["stats"] for k in own),
       order=state["order"], ownership=matrix, stage1_memset=[[m[0], "%08X" % m[1], m[2], hex(m[3])] for m in state["memset"]],
       stage1_writes_outside_I3_list=len(st1 - i3_claim),
       note="order %s; stats written by any stage: %s; stage 1 writes %d result bytes (I-3 names 4 fields)" % (
           state["order"], any(own[k]["stats"] for k in own), len(st1)))

# B. stage 3, the effect-slot family: statuses 3 / 9 / 20 / 30 in the +0x68 word, rows' +6 slots 0 / 1 / 2 / 0xFF
w68 = bytearray(16)
for b in (3, 9, 20, 30):
    w68[b >> 3] |= 1 << (b & 7)
world(w68=bytes(w68), slots={0: 5, 1: 1, 2: 0, 3: 7}, erows={3: 0, 9: 1, 20: 2, 30: 0xFF}, ecount=64)
stats_before = bytes(uc.mem_read(STATS, 0x800))
ok = run()
own = ownership()
res42 = rd("<8h", RESULT + 0x42)
list3e = list(uc.mem_read(RESULT + 0x3E, 4))
b_ok = (ok and res42[0] == 4 and res42[1] == 0 and res42[2] == -1 and res42[3] == -1 and list3e[0] == 9 and list3e[1:] == [0xFF] * 3
        and bytes(uc.mem_read(STATS, 0x800)) == stats_before and not own[3]["stats"])
record("B_stage3_effect_slots", b_ok, result_42=list(res42), result_3E=list3e, stage3_result_writes=ranges(own[3]["result"]),
       stats_changed=bytes(uc.mem_read(STATS, 0x800)) != stats_before,
       note="slot 0: 5 -> 4; slot 1: 1 -> 0 and id 9 listed; slot 2 (0) skipped; 0xFF never; the stats +0x17C are NOT written")

# C. five simultaneous expiries: the +0x3E list has four bytes before +0x42
w68 = bytearray(16)
ids = (1, 2, 4, 5, 6)
for b in ids:
    w68[b >> 3] |= 1 << (b & 7)
world(w68=bytes(w68), slots={k: 1 for k in range(5)}, erows={b: i for i, b in enumerate(ids)}, ecount=64)
ok = run()
tail = list(uc.mem_read(RESULT + 0x3E, 16))
res42 = rd("<8h", RESULT + 0x42)
record("C_five_expiries_list_bound", ok, result_3E_to_4D=tail, result_42_slots=list(res42), stage3_writes=ranges(ownership()[3]["result"]),
       note="observed, not asserted: ids 1,2,4,5,6 expire in one tick; the fifth id byte is written at +0x42 and the slot-0 "
            "timer write that follows lands on +0x42..+0x43")

# D. stage 2, the status-word family: a beat above 10 counts down by 10 into the RESULT; Regen (0x19) at beat <= 10 draws
checks = {}
world(w3c=1 << 0x19, beat={0x19: 25}, srows={0x19: 4}, frame=1)
ok = run()
checks["beat_25_minus_10"] = [ok, rd("<h", RESULT + 0xDC + 2 * 0x19)[0], rd("<h", STATS + 0x13C + 2 * 0x19)[0], state["rng"]]
d1 = ok and checks["beat_25_minus_10"][1] == 15 and checks["beat_25_minus_10"][2] == 25 and not state["rng"]
regen = []
for frame in (1, 2):
    for div in (7, 1, 250):
        world(w3c=1 << 0x19, beat={0x19: 10}, srows={0x19: 4}, frame=frame, regen_div=div)
        ok = run()
        acc = rd("<i", RESULT + 0x24)[0]
        flags = rd("<I", RESULT + 0x2C)[0]
        newbeat = rd("<h", RESULT + 0xDC + 2 * 0x19)[0]
        want_r = mt.next()
        regen.append({"frame": frame, "div": div, "ok": ok, "rng": state["rng"], "mt_expected": want_r, "acc_24": acc,
                      "expected_heal": (want_r % div) + 1, "flags_2C": hex(flags), "new_beat": newbeat, "expected_beat": 4 * frame * 30})
d2 = all(r["ok"] and r["rng"] == [r["mt_expected"]] and r["acc_24"] == r["expected_heal"] and (int(r["flags_2C"], 16) & 0x500) == 0x500
         and r["new_beat"] == r["expected_beat"] for r in regen)
record("D_stage2_beat_and_regen", d1 and d2, beat_countdown=checks, regen=regen,
       note="beat -10 per tick into result+0xDC+2s (stats untouched); Regen heal = (MT19937(5489) draw mod byte[+0x1C2]) + 1, "
            "ADDED; new beat = row+9 x frame base x 30")

# F. stage 4, the global drain modes: [022C314C] mode bits, the field clock [0208D45C], interval = frame base x 30 / 3
G_MODES, G_CLOCK = 0x22C314C, 0x208D45C
f_rows = []
for frame, clock in ((1, 20), (1, 25), (2, 30), (2, 40)):
    for hp, mp in ((1000, 300), (60, 30)):
        world(frame=frame)
        uc.mem_write(STATS + 0x24, struct.pack("<i", hp))
        uc.mem_write(STATS + 0x28, struct.pack("<h", mp))
        uc.mem_write(G_MODES, struct.pack("<I", 3))
        uc.mem_write(G_CLOCK, struct.pack("<I", clock))
        ok = run()
        own4 = ranges(ownership()[4]["result"])
        fires = clock % (frame * 30 // 3) == 0
        acc, mpd, flags = rd("<i", RESULT + 0x24)[0], rd("<h", RESULT + 0x2A)[0], rd("<I", RESULT + 0x2C)[0]
        want_acc = (-(hp // 100) if hp >= 100 else -1) if fires else 0
        want_mp = (-(mp // 50) if mp >= 50 else -1) if fires else 0
        f_rows.append({"frame": frame, "clock": clock, "hp_src": hp, "mp_src": mp, "ok": ok, "fires": fires, "acc_24": acc,
                       "want_24": want_acc, "mp_2A": mpd, "want_2A": want_mp, "flags_2C": hex(flags), "stage4_writes": own4})
f_ok = all(r["ok"] and r["acc_24"] == r["want_24"] and r["mp_2A"] == r["want_2A"] and (bool(r["stage4_writes"]) == r["fires"]) for r in f_rows)
record("F_stage4_drain_modes", f_ok, rows=f_rows,
       note="fires only when the clock is a multiple of frame x 10; HP arm -(src/100) or -1 below 100; MP arm -(MP/50) or -1 below "
            "50: both NEGATIVE in the record")
restore_world_after_F = True

# E. no stage calls another (I-5): the functions entered per stage never include another stage's entry out of order
record("E_I5_no_stage_calls_another", results["A_order_and_empty_ownership"]["order"] == [1, 2, 3, 4, 5], note="each stage entered once, in order")

json.dump({"pass": sum(1 for v in results.values() if v["pass_"]), "total": len(results), "ok": allok, "allowed_functions": len(ALLOWED),
           "results": results}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, default=str)
print("%d/%d pass (allowed %d functions)" % (sum(1 for v in results.values() if v["pass_"]), len(results), len(ALLOWED)))


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
