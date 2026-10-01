#!/usr/bin/env python3
"""EXP-098 battle-mode-composition-exec - the battle-runtime-mode ladder
0030D9A0 executed with its whole callee chain real: the predicate
00377C20, the index getter 003148F0, and its context chain
002EF2B0 -> 002EF640. NOTHING is scripted - the pilot
(diff_battle_mode.py) ran the ladder and the predicate separately with
each other stubbed ("a scripted callee is not a proved one"); this runs
the composition.

    0030D9A0  ladder    REAL - flags = [[0x2EBF190]+0x5B04]; test cl,8->5;
              test cl,4->4; call 00377C20 -> nonzero:3; reload flags;
              test cl,2->2; else return cl&1 (0/1). Priority 8>4>pred>2>1.
    00377C20  predicate REAL - idx = 003148F0(); tab=[0x2ADD100]; null->0;
              idx>=[tab+4]->0; packed = tab[3*idx+9]<<8 | tab[3*idx+8];
              ret packed>>15.
    003148F0  index     REAL - ctx = 002EF2B0(); eax=[ctx+0x1044];
              cmovs clamps negative to 0.
    002EF2B0  ctx       REAL - ret 002EF640() + 0x200  (=> 0x2164480).
    002EF640  base      REAL - ret 0x2164280 (constant).

    => the active-field index is dword [0x21654C4] (real .data/BSS cell,
       planted per case), the field-record table pointer is [0x2ADD100]
       with count at +4 and 3-byte rows at +8.

Trace: d=ladder entry, P=predicate, I=index getter, C=ctx, G=base.
Early-return modes (5,4) must NOT fire P; modes 3/2/1/0 must.

NOT EXERCISED (disclosed): the four mode setters, the save round trip,
the 21 consumers, no live process.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

LADDER = 0x0030D9A0          # battle-mode ladder (subject)
PRED   = 0x00377C20          # field-bit15 predicate
IDXFN  = 0x003148F0          # active field index
CTXFN  = 0x002EF2B0          # ctx getter (+0x200)
BASEFN = 0x002EF640          # base 0x2164280

G_STATE  = 0x2EBF190         # state pointer cell
G_TABLE  = 0x2ADD100         # field-record table pointer cell
IDX_CELL = 0x21654C4         # [0x2164280+0x200+0x1044] active field index

STATE  = HEAP + 0x000000     # state block (flags dword at +0x5B04)
TAB    = HEAP + 0x100000     # field-record table (count +4, rows +8 stride 3)

CALLS = {LADDER: "d", PRED: "P", IDXFN: "I", CTXFN: "C", BASEFN: "G"}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)

def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs

class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def q(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]
    def d(self, addr):
        return struct.unpack("<I", self.r(addr, 4))[0]

class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x400000), (STACK, 0x100000), (RETQ, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")

        # state block: [0x2EBF190] -> STATE, flags dword at +0x5B04
        gm.w(G_STATE, qw(STATE))
        gm.w(STATE + 0x5B04, dw(case.get("flags", 0)))

        # index chain: [0x21654C4] = active field index (real BSS cell)
        gm.w(IDX_CELL, dw(case.get("idx", 0)))
        # decoy cells for the m-add200 mutant: [0x21642C4] carries a
        # different index so a wrong +0x200 add reads the wrong index
        gm.w(0x2164280 + 0x100 + 0x1044, dw(case.get("decoy_idx", 7)))

        # field-record table: [0x2ADD100] -> TAB (or 0); count at +4;
        # rows at +8, stride 3; bit15 of the u16 at row+0 is the flag
        # (bytes tab[3i+8]=lo, tab[3i+9]=hi per the body).
        if case.get("tab_null"):
            gm.w(G_TABLE, qw(0))
        else:
            gm.w(G_TABLE, qw(TAB))
            rows = case.get("rows", [])
            gm.w(TAB + 4, dw(case.get("count", len(rows))))
            for i, v in enumerate(rows):
                gm.w(TAB + 8 + i * 3, bytes([v & 0xFF, (v >> 8) & 0xFF, 0]))

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        self.trace.append(CALLS[addr])

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    try:
        uc.emu_start(LADDER, RETQ, count=100_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    ret = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    obs = {"mode": ret, "flags_after": gm.d(STATE + 0x5B04)}
    return " ".join(w.trace) or "-", w.faults, w, obs

# ---- cases -------------------------------------------------------------------

def build_cases():
    C = []
    def A(name, trace, mode, **kw):
        C.append(dict(kw, name=name, want_trace=trace, want_mode=mode))

    FULL = "d P I C G"
    # early returns - the predicate chain must NOT fire
    A("m5-bit3",     "d", 5, flags=0x8)
    A("m5-priority", "d", 5, flags=0xF)            # 8 outranks 4/2/1
    A("m4-bit2",     "d", 4, flags=0x4)
    A("m4-over-low", "d", 4, flags=0x6)            # 4 outranks 2+1
    # predicate consulted - bit15 of the indexed row decides mode 3
    A("m3-pred",     FULL, 3, flags=0, idx=0, rows=[0x8000, 0])
    A("m3-over-low", FULL, 3, flags=0x3, idx=0, rows=[0x8000])
    A("m2-bit1",     FULL, 2, flags=0x2, idx=0, rows=[0])
    A("m1-bit0",     FULL, 1, flags=0x1, idx=0, rows=[0])
    A("m0-none",     FULL, 0, flags=0, idx=0, rows=[0])
    # bit14 set, bit15 clear: the shift selects bit15, not "any high bit"
    A("row-bit14",   FULL, 0, flags=0, idx=0, rows=[0x4000])
    # index chain: negative clamps to 0 via cmovs
    A("idx-neg-clamp",   FULL, 3, flags=0, idx=-1, rows=[0x8000])
    A("idx-neg-clear",   FULL, 0, flags=0, idx=-1, rows=[0])
    # count bound: idx == count refuses, count-1 is the last valid row
    A("idx-eq-count",    FULL, 0, flags=0, idx=2, count=2, rows=[0x8000, 0x8000])
    A("idx-last",        FULL, 3, flags=0, idx=1, count=2, rows=[0, 0x8000])
    A("idx-over",        FULL, 0, flags=0, idx=9, count=2, rows=[0x8000, 0x8000])
    # null table refuses before indexing
    A("tab-null",        FULL, 0, flags=0, idx=0, tab_null=True)
    # high flag bits are ignored
    A("flags-high",      FULL, 0, flags=0x100, idx=0, rows=[0])
    A("flags-high-m5",   "d", 5, flags=0x108)
    # mid-index row select: idx picks its own row, not row 0
    A("idx-select",      FULL, 3, flags=0, idx=2, count=3, rows=[0, 0, 0x8000])
    return C

# ---- mutants -----------------------------------------------------------------

MUTANTS = [
    ("m-mode5",   0x30D9B7, b"\x06",
     "mode-5 arm mov eax,5 -> 6: wrong mode returned"),
    ("m-test4",   0x30D9C2, b"\x02",
     "test cl,4 -> test cl,2: bit4 falls through, bit2 answers 4"),
    ("m-predcall", 0x30D9CF, b"\x90" * 5,
     "call 00377C20 removed: stale eax -> mode 3 always taken"),
    ("m-tabnull", 0x377C30, b"\x45\x31\xc0",
     "test r8,r8 -> xor r8d,r8d: table always reads as null"),
    ("m-jae",     0x377C39, b"\x72",
     "count bound jae -> jb: in-range refuses, out-of-range indexes"),
    ("m-shr",     0x377C57, b"\x0e",
     "packed>>15 -> >>14: bit14 answers instead of bit15"),
    ("m-cmovs",   0x314903, b"\x90" * 3,
     "cmovs removed: negative index not clamped, refuses at bound"),
    ("m-add200",  0x2EF2BB, b"\x00\x01",
     "ctx +0x200 -> +0x100: index read from the wrong cell"),
    ("m-and1",    0x30DA03, b"\x02",
     "and eax,1 -> and eax,2: mode 0/1 answers from bit1"),
    ("m-test8",   0x30D9B3, b"\x04",
     "test cl,8 -> test cl,4: bit8 flag falls to the bit4 arm"),
]

def main():
    raw, secs = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        ok = (tr == case["want_trace"] and obs["mode"] == case["want_mode"]
              and not [f for f in faults if f[0] == "MEM"])
        npass += ok; nfail += (not ok)
        if not ok:
            print("FAIL %s\n  got:  %s mode=%d\n  want: %s mode=%d\n  faults=%s"
                  % (case["name"], tr, obs["mode"],
                     case["want_trace"], case["want_mode"], faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr, "ok": bool(ok),
                             "obs": obs, "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))
    fired = set()
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        fired |= w.fired
    out["bodies_fired"] = ["0x%X" % v for v in sorted(fired)]
    print("fired:", " ".join("%s@%x" % (CALLS[v], v) for v in sorted(fired)))

    base = {c["name"]: (c["trace"], c["obs"]["mode"]) for c in out["cases"]}
    for name, va, data, why in MUTANTS:
        n_diff = 0; diffs = []
        for case in build_cases():
            c = dict(case); c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs)
            if (tr, obs["mode"]) != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s mode=%d" % (tr, obs["mode"])))
        killed = n_diff > 0
        print(("KILL " if killed else "SURV") + " %s  (%d divergent) %s"
              % (name, n_diff, why))
        out["mutants"].append({"name": name, "va": "0x%X" % va,
                               "killed": killed, "divergent": n_diff,
                               "why": why, "sample": diffs[:3]})
    json.dump(out, open("result.json", "w"), indent=1,
              default=lambda o: o.hex() if isinstance(o, bytes) else str(o))
    return 0 if nfail == 0 and all(m["killed"] for m in out["mutants"]) else 1

if __name__ == "__main__":
    sys.exit(main())
