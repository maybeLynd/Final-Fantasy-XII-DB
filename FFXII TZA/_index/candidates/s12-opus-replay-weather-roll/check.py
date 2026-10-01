"""S-12: execute the weather ROLL 0025ACA0 (CONTRACT-weather.md) with its real probability source 002658B0, its real transition
resolver 0025ABA0 and the real gameplay MT19937 draw 00379CD0 -> 00863BF0, against an independent model of the contract's section 12
and an independent MT19937 (OPUS, 2026-09-25, block 339).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. Block 303 executed the APPLY 0026D910 and noted "the roll 0025ACA0 end to
end" as not covered. world.py (block 318/319's builder, Session) supplies the image, the IAT traps and the named bridges. No
application stub. STOP BOUNDARY (recorded, nothing substituted): 0026D910, the apply the roll tail-jumps to (block 303's subject);
the slot it receives in ecx is the roll's result. The MT is seeded by the shipped seeder 00379CF0 -> 00863D30 -> 00866D60.
Fixtures: the persisted slot byte +0x1060 of the payload 002EF2B0 returns; the script-loaded bit [02098E20] bit 0 and the script
block [02098E10] (word +0 >= 7, +0x64 the section offset, section[1..3] the three probabilities as signed bytes); the debug
override dword +0xAAC of the object 001D50D0 returns; six idle objects (the world's convention).
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
ROLL, APPLY, SEED, PAYLOAD, CONSOLE = 0x25ACA0, 0x26D910, 0x379CF0, 0x2EF2B0, 0x1D50D0
W.ALLOWED |= {0x16D6A0, APPLY, 0x863D30} | set().union(*(W.closure(f) for f in (ROLL, SEED, 0x863D30, PAYLOAD, CONSOLE)))   # 00379CF0 is `jmp 00863D30`
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
SCRIPT = 0x76300000
got = {}


def on_apply(u, a, n, _):
    got["slot"] = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_apply, begin=APPLY, end=APPLY)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def call(fn, *args):
    got.clear()
    S.call(fn, *args)
    return uc.reg_read(UC_X86_REG_RAX)


PAY = call(PAYLOAD)
CON = call(CONSOLE)


class MT:
    """MT19937, init_genrand - independent of the image."""

    def __init__(self, seed):
        self.m = [seed & 0xFFFFFFFF]
        for i in range(1, 624):
            self.m.append((1812433253 * (self.m[-1] ^ (self.m[-1] >> 30)) + i) & 0xFFFFFFFF)
        self.i = 624

    def next(self):
        if self.i >= 624:
            for k in range(624):
                y = (self.m[k] & 0x80000000) | (self.m[(k + 1) % 624] & 0x7FFFFFFF)
                self.m[k] = self.m[(k + 397) % 624] ^ (y >> 1) ^ (0x9908B0DF if y & 1 else 0)
            self.i = 0
        y = self.m[self.i]
        self.i += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        return y


def model(persisted, probs, override, loaded, mt):
    def prob(s):
        i = min(max(s - 1, 0), 2)
        return probs[i] if loaded else 0x21

    def resolve(s):
        if s == 1:
            return 2 if prob(2) > 0 else (3 if prob(3) > 0 else 1)
        if s == 3:
            return 2 if prob(2) > 0 else (1 if prob(1) > 0 else 3)
        if (mt.next() * 100) >> 32 < 50:
            return 3 if prob(3) > 0 else (1 if prob(1) > 0 else 2)
        return 1 if prob(1) > 0 else (3 if prob(3) > 0 else 2)

    s = override if override > 0 else persisted + 1
    p = prob(s)
    if p == 0:
        s = resolve(s)
    elif p < 100 and (mt.next() * 100) >> 32 >= p:
        s = resolve(s)
    return s


def setup(persisted, probs, override=0, loaded=True):
    w(PAY + 0x1060, "<b", persisted)
    w(0x2098E20, "<B", 1 if loaded else 0)
    uc.mem_write(SCRIPT, bytes(0x200))
    w(SCRIPT, "<H", 7)
    w(SCRIPT + 0x64, "<I", 0x100)
    w(SCRIPT + 0x101, "<bbb", *probs)
    w(0x2098E10, "<Q", SCRIPT)
    w(CON + 0xAAC, "<i", override)


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


SEED_VALUE = 4537
got.clear()
assert S.call(SEED, SEED_VALUE), (S.st["bad"] or S.st["faults"])[:2]
mt = MT(SEED_VALUE)
cases, bad = [], []
grid = [(0, (100, 0, 0)), (0, (0, 100, 0)), (1, (0, 0, 100)), (2, (50, 30, 20)), (1, (33, 33, 33)), (0, (0, 0, 0)), (2, (10, 90, 0)),
        (1, (-5, 40, 60)), (0, (70, 0, 30)), (2, (0, 0, 0))]
for rep in range(6):
    for persisted, probs in grid:
        setup(persisted, probs)
        call(ROLL)
        want = model(persisted, probs, 0, True, mt)
        cases.append([persisted, list(probs), got.get("slot"), want])
        if got.get("slot") != want:
            bad.append(cases[-1])
record("roll_matches_the_contract_model", not bad and len(cases) == 60, cases=cases[:12], total=len(cases), mismatches=bad[:5],
       note="60 rolls (10 persisted-slot / probability settings x 6, the MT advancing throughout): the slot 0025ACA0 hands the apply "
            "equals section 12's roll / resolve model driven by an independent MT19937 seeded like the shipped one (4537)")

ov = []
for o in (2, 3):
    setup(0, (0, 0, 0), override=o)
    call(ROLL)
    ov.append([o, got.get("slot"), model(0, (0, 0, 0), o, True, mt)])
setup(1, (0, 0, 0), loaded=False)
call(ROLL)
unl = [got.get("slot"), model(1, (0, 0, 0), 0, False, mt)]
record("override_and_unloaded_script", all(a == b for _, a, b in ov) and unl[0] == unl[1], override=ov, script_not_loaded=unl,
       note="a positive debug override (+0xAAC) replaces persisted+1 as the start slot; with the script not loaded every probability "
            "reads 33 (0x21)")

json.dump({"ok": allok, "mt_seed": SEED_VALUE, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
