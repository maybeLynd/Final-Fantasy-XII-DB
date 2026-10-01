#!/usr/bin/env python3
"""EXP-099 field-music-selection-exec - 003EAA70 executed with its single
scripted callee real: FieldData_GetVariable0 00265270. The pilot
(diff_field_music_selection.py) ran the subject with the callee stubbed
as `mov eax,imm; ret`; here the callee's two gates run from shipped
bytes, so a dead actor / null varblock produce progress 0 flowing
through the real ladder rather than a hand-fed value.

    003EAA70  subject   REAL - ebx = arg; r11w = callee result;
              tab=[0x2B5E0D0]; [tab+4] < arg -> -1; page = sar(arg,7)
              (biased signed div); page ptr = movsxd [tab+8+4*page],
              null -> -1. Run-chain walk on 4-byte headers
              {u16 start|len<<11, u8 nEntries, u8 default}:
              start > arg -> -1; arg < start+len -> ladder; else
              rax += 4 + 3*nEntries. Ladder: r9d = default, then per
              3-byte entry {u16 thr, u8 val}: movsx r11d,r11w; if
              progress <= thr stop; else r9d = val; last threshold
              passed wins. r9==0 -> -1.
    00265270  callee    REAL - test byte[0x2098E20],1 -> 0;
              rax=[0x2098E58]; null -> 0; else movzx eax, word[rax].

Trace: m=subject entry, V=callee entry. Observables: eax return
(music id or -1), plus trace.

NOT EXERCISED (disclosed): the loader that fills 0x2B5E0D0
(musicctrl.bin via 0051ED10), the four callers, no live process.
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

SUBJ   = 0x003EAA70          # music-selection ladder (subject)
VARFN  = 0x00265270          # FieldData_GetVariable0 (was scripted)

G_LIVE   = 0x2098E20         # liveness byte, bit0
G_VARPTR = 0x2098E58         # -> varblock; u16 progress at +0
G_TABLE  = 0x2B5E0D0         # -> table; bound +4; page ptrs +8+4*page

VARB   = HEAP + 0x000000     # varblock (u16 progress at +0)
TAB    = HEAP + 0x100000     # table: bound +4, page s32 ptrs at +8
PAGE   = HEAP + 0x200000     # page arena, 0x1000 per page index

CALLS = {SUBJ: "m", VARFN: "V"}

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

def run_hdr(start, length, entries, default):
    """4-byte run header + entries [(thr, val), ...]"""
    b = struct.pack("<HBB", (start & 0x7FF) | (length << 11),
                    len(entries), default)
    for thr, val in entries:
        b += struct.pack("<HB", thr & 0xFFFF, val & 0xFF)
    return b

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

        # callee gates: liveness bit0, varblock ptr, u16 progress
        gm.w(G_LIVE, bytes([case.get("live", 1)]))
        gm.w(G_VARPTR, qw(0 if case.get("var_null") else VARB))
        gm.w(VARB, struct.pack("<H", case.get("progress", 0) & 0xFFFF))

        # table: bound dword, s32 absolute page pointers
        gm.w(G_TABLE, qw(TAB))
        gm.w(TAB + 4, dw(case.get("bound", 0x7FF)))
        for pi, runs in case.get("pages", {}).items():
            if runs is None:
                continue  # null page pointer
            pp = PAGE + pi * 0x1000
            gm.w(TAB + 8 + pi * 4, dw(pp))
            off = 0
            for r in runs:
                gm.w(pp + off, r)
                off += len(r)

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
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, case.get("arg", 0))
    try:
        uc.emu_start(SUBJ, RETQ, count=200_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    ret = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    if ret & 0x80000000: ret -= 0x100000000
    return " ".join(w.trace) or "-", w.faults, w, {"ret": ret}

# ---- cases -------------------------------------------------------------------

def build_cases():
    C = []
    def A(name, trace, ret, **kw):
        C.append(dict(kw, name=name, want_trace=trace, want_ret=ret))

    # one run covering arg 5: start0 len10, default 7, entry thr0 -> 9
    R1 = run_hdr(0, 10, [(0, 9)], 7)
    P0 = {0: [R1]}
    # progress 0 == thr 0 -> jle stops -> default 7 (dead/null both = 0)
    A("base",        "m V", 7, arg=5, pages=P0, progress=0)
    A("dead-actor",  "m V", 7, arg=5, pages=P0, live=0, progress=50)
    A("varblock-null","m V", 7, arg=5, pages=P0, var_null=True, progress=50)
    # bound: arg > [tab+4] -> -1 before any page read; arg==bound proceeds
    A("arg-over-bound", "m V", -1, arg=6, bound=5, pages=P0)
    A("arg-eq-bound",   "m V", 7, arg=5, bound=5, pages=P0)
    # null page pointer -> -1
    A("page-null",   "m V", -1, arg=5, pages={0: None})
    # run gap: arg lands between runs -> next start > arg -> -1
    A("run-gap",     "m V", -1, arg=20, pages={0: [
        run_hdr(0, 10, [(0, 9)], 7), run_hdr(30, 10, [(0, 4)], 3)]})
    # threshold ladder: progress vs {thr:val}
    RUN_TH = run_hdr(0, 31, [(10, 9), (50, 0x21), (100, 0x33)], 7)
    A("thr-default", "m V", 7,     arg=5, pages={0: [RUN_TH]}, progress=5)
    A("thr-eq",      "m V", 7,     arg=5, pages={0: [RUN_TH]}, progress=10)
    A("thr-first",   "m V", 9,     arg=5, pages={0: [RUN_TH]}, progress=11)
    A("thr-mid",     "m V", 0x21,  arg=5, pages={0: [RUN_TH]}, progress=60)
    A("thr-last",    "m V", 0x33,  arg=5, pages={0: [RUN_TH]}, progress=0x7FFF)
    # negative progress (u16 0xFFFF -> s16 -1): never passes a threshold
    A("neg-progress","m V", 7,     arg=5, pages={0: [RUN_TH]}, progress=0xFFFF)
    A("neg-prog-8000","m V", 7,    arg=5, pages={0: [RUN_TH]}, progress=0x8000)
    # second run via stride advance: arg 40 in run2 {start30 len20}
    A("run-second",  "m V", 3, arg=40, pages={0: [
        run_hdr(0, 10, [(0, 9)], 7), run_hdr(30, 20, [(0, 4)], 3)]})
    # run upper bound is INCLUSIVE: arg == start+len still matches run1
    A("run-boundary","m V", 8, arg=30, pages={0: [
        run_hdr(0, 30, [(0, 9)], 8), run_hdr(30, 20, [(0, 4)], 3)]})
    # arg one past the bound advances to run2
    A("run-after",   "m V", 3, arg=31, pages={0: [
        run_hdr(0, 30, [(0, 9)], 8), run_hdr(30, 20, [(0, 4)], 3)]})
    # page 1: arg 200 -> page index 1, progress 50 passes thr 0 -> 0x12
    A("page1",       "m V", 0x12, arg=200, progress=50,
      pages={1: [run_hdr(200, 20, [(0, 0x12)], 5)]})
    # ladder result 0 maps to -1
    A("zero-result", "m V", -1, arg=5,
      pages={0: [run_hdr(0, 10, [(0, 0)], 7)]}, progress=50)
    # run with n=0 entries: default byte answers directly
    A("empty-run",   "m V", 4, arg=5,
      pages={0: [run_hdr(0, 10, [], 4)]}, progress=0x7FFF)
    # arg at run start boundary: start==arg proceeds (ja not taken);
    # run1 len 29 makes arg=30 fall through to run2 first
    A("start-eq-arg","m V", 7, arg=30, pages={0: [
        run_hdr(0, 29, [(0, 9)], 8), run_hdr(30, 20, [(0, 4)], 7)]})
    # run start >= 0x400: the 11-bit field carries it (kills m-start-mask)
    A("start-high",  "m V", 0x55, arg=0x405,
      pages={8: [run_hdr(0x400, 31, [(0, 0x44)], 0x55)]})
    return C

# ---- mutants -----------------------------------------------------------------

MUTANTS = [
    ("m-bound-jl",  0x3EAA8C, b"\x7e",
     "bound check jl->jle: arg==bound refuses"),
    ("m-page-sar",  0x3EAA98, b"\x06",
     "page index sar 7 -> sar 6: wrong page granularity"),
    ("m-start-mask", 0x3EAABE, b"\x03",
     "run start mask 0x7FF -> 0x3FF: start mis-reads"),
    ("m-start-ja",  0x3EAAC3, b"\x73",
     "run start ja->jae: arg==start refuses"),
    ("m-run-jae",   0x3EAAC9, b"\x72",
     "run in-range jae->jb: matching arg walks past -> -1"),
    ("m-stride",    0x3EAAD2, b"\x12",
     "advance lea scale x2 -> x1: wrong next-header offset"),
    ("m-thr-jle",   0x3EAB2F, b"\x7c",
     "threshold jle->jl: equal threshold takes the entry"),
    ("m-movsx",     0x3EAB12, b"\xb7",
     "movsx r11d,r11w -> movzx: negative progress goes positive"),
    ("m-cmove",     0x3EAB49, b"\x45",
     "cmove->cmovne: result 0 returns 0 instead of -1"),
    ("m-live-bit",  0x265276, b"\x02",
     "liveness test bit0 -> bit2: live actor reads as dead"),
]

def main():
    raw, secs = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        ok = (tr == case["want_trace"] and obs["ret"] == case["want_ret"]
              and not [f for f in faults if f[0] == "MEM"])
        npass += ok; nfail += (not ok)
        if not ok:
            print("FAIL %s\n  got:  %s ret=%d\n  want: %s ret=%d\n  faults=%s"
                  % (case["name"], tr, obs["ret"],
                     case["want_trace"], case["want_ret"], faults))
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

    base = {c["name"]: (c["trace"], c["obs"]["ret"]) for c in out["cases"]}
    for name, va, data, why in MUTANTS:
        n_diff = 0; diffs = []
        for case in build_cases():
            c = dict(case); c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs)
            if (tr, obs["ret"]) != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s ret=%d" % (tr, obs["ret"])))
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
