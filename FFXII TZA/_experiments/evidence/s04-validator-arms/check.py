# S-04 validator-arms — FABLE-REQ-ORACLE-S04-VALIDATOR-ALL-THIRTY-TWO-
# CLASS-ARMS. 00322C50 BattleEncodedId_IsValidForClass(ecx=cls,
# edx=id) executed native under Unicorn for EVERY class 1..32 with
# four boundary probes each (LOW-1, LOW, HIGH, HIGH+1) plus a signed
# negative probe. LOW/HIGH are recorded from live registers at the
# shared tail 0032302E (cmp ebx,edx / lea eax,[rcx-1]), not derived.
#
#   Dispatch: a=cls-1; a>0x1F -> 0. jtab 00323054 -> arm -> tail.
#   Tail 0032302A/2C/2E: edx=LOW (per arm), ecx=HIGH+1; signed jl/jg
#   -> accept iff LOW <= id <= HIGH, INCLUSIVE SIGNED.
#   Arm kinds: plain descriptor arms (LOW=0, ecx=d[desc+4]);
#   bias arms (edx=(cls-5)*0x1000, ecx=d[desc+4]+bias, desc==0 ->
#   ecx=bias => empty); cls13 = FOUR descriptors summed (each
#   missing contributes 0); constants cls19 [0xE000,0xEFFE],
#   cls22 [0,3], cls23 [0,8]; cls1 = two-level: id16>>12 indexes a
#   shipped 15-record table 0x1EEBCF8 (stride 0x58, d[+0]=subclass
#   n+5) then re-dispatches under the SAME id.
#   Descriptor cells live in .data BSS (ship as zero) -> planted
#   fixtures; counts are runtime data, the planted values are
#   synthetic and disclosed as such.
#
# Every case records: arm address executed, observed LOW/HIGH at
# the tail, and the eax verdict. NATIVE-REPLAY over shipped bytes;
# descriptor buffers are MODEL-PROVEN fixtures.

import hashlib
import json
import struct
import sys

import capstone
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x30A0000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

VALID = 0x322C50
JTAB = 0x323054
TAIL = 0x32302E                 # cmp ebx,edx — LOW in edx, HIGH+1 rcx
MAPPER_RET = 0x322C86           # insn after call 00309440
NIBTBL = 0x1EEBCF8              # 15 recs x 0x58; d[+0]=subclass

RESULT = __file__.rsplit("\\", 1)[0] + "\\result.json"
N = 0x40                        # planted descriptor count


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)


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
        self.uc = uc

    def map(self, addr, size):
        self.uc.mem_map(addr, (size + 0xFFF) & ~0xFFF)

    def w(self, addr, data):
        self.uc.mem_write(addr, data)

    def r(self, addr, n):
        return bytes(self.uc.mem_read(addr, n))

    def qw(self, a): return struct.unpack("<Q", self.r(a, 8))[0]
    def dw(self, a): return struct.unpack("<I", self.r(a, 4))[0]


# kind, LOW bias, expected number of rip-relative descriptor loads
# in the arm body (asserted at init; the cells themselves are
# computed from the shipped instructions, never hand-derived).
ARMS = {
    2:  ("desc", 0, 1),  3:  ("desc", 0, 1),  4:  ("desc", 0, 1),
    5:  ("desc", 0, 1),  6:  ("bias", 0x1000, 1),
    7:  ("bias", 0x2000, 1), 8:  ("bias", 0x3000, 1),
    9:  ("bias", 0x4000, 1), 10: ("bias", 0x5000, 1),
    11: ("bias", 0x6000, 1), 12: ("bias", 0x7000, 1),
    13: ("sum4", 0x8000, 4), 14: ("bias", 0x9000, 1),
    15: ("bias", 0xA000, 1), 16: ("bias", 0xB000, 1),
    17: ("bias", 0xC000, 1), 18: ("bias", 0xD000, 1),
    19: ("const", 0xE000, 0),
    20: ("desc", 0, 1), 21: ("desc", 0, 1),
    22: ("const", 0, 0), 23: ("const", 0, 0),
    24: ("desc", 0, 1), 25: ("desc", 0, 1), 26: ("desc", 0, 1),
    27: ("desc", 0, 1), 28: ("desc", 0, 1), 29: ("desc", 0, 1),
    30: ("bias", 0xA000, 1),            # alias of cls15 arm
    31: ("bias", 0xA000, 1),            # alias of cls15 arm
    32: ("desc", 0, 1),                 # alias of cls25 arm
}
CONST_HI = {19: 0xEFFE, 22: 3, 23: 8}


class World:
    def __init__(self, raw, secs):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        self.bounds = []
        self.arms_hit = []
        self.subclass = []
        self.faults = []
        self.arm_set = set()
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", hex(uc.reg_read(UC_X86_REG_RIP))))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("bad", hex(addr),
                            hex(uc.reg_read(UC_X86_REG_RIP))))
        uc.emu_stop()
        return False

    def on_code(self, uc, addr, size, _):
        if addr in self.arm_set:
            self.arms_hit.append(hex(addr))
        if addr == TAIL:
            self.bounds.append((uc.reg_read(UC_X86_REG_EDX),
                                uc.reg_read(UC_X86_REG_ECX)))
        if addr == MAPPER_RET:
            self.subclass.append(uc.reg_read(UC_X86_REG_EAX))

    def probe(self, cls, idv):
        """One validator run; (verdict, arm-hits, tail-bounds,
        mapper-subclass)."""
        self.bounds.clear()
        self.arms_hit.clear()
        self.subclass.clear()
        uc = self.uc
        uc.reg_write(UC_X86_REG_RSP, STACK + 0x80000)
        self.gm.w(STACK + 0x80000, qw(RETQ))
        uc.reg_write(UC_X86_REG_ECX, cls & 0xFFFFFFFF)
        uc.reg_write(UC_X86_REG_EDX, idv & 0xFFFFFFFF)
        try:
            uc.emu_start(VALID, RETQ)
        except UcError as e:
            self.faults.append(("exc", str(e)))
        return (uc.reg_read(UC_X86_REG_EAX),
                dict(arm=self.arms_hit[:],
                     tail=[{"low": l, "high1": h}
                           for l, h in self.bounds],
                     sub=self.subclass[:]))


def sgn(v):
    return v - 0x100000000 if v & 0x80000000 else v


def main():
    raw, secs = load_image()
    w = World(raw, secs)
    jtab = [w.gm.dw(JTAB + k * 4) + IMG_LO for k in range(32)]
    w.arm_set = set(jtab) | {0x322C7E}

    # ---- compute descriptor cells from the shipped rip-relative --
    # loads in each arm body; count must match ARMS's expectation.
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    CELLS = {}
    for cls, (kind, bias, nexp) in ARMS.items():
        arm = jtab[cls - 1]
        found = []
        for i in md.disasm(w.gm.r(arm, 0x90), arm):
            if i.address >= TAIL:
                break
            # arm ends at the shared-tail jump; internal short
            # jumps (cls13) stay inside the scan
            if i.mnemonic == "jmp" and \
                    ("0x32302" in i.op_str or i.op_str == "rcx"):
                break
            if i.mnemonic == "mov" and "qword ptr [rip" in i.op_str:
                disp = int(i.op_str.rsplit("0x", 1)[1].rstrip("]"), 16)
                found.append(i.address + i.size + disp)
        assert len(found) == nexp, \
            "cls%d: %d rip-loads, expected %d" % (cls, len(found), nexp)
        CELLS[cls] = found

    results, fails = {}, []

    def plant(cls, counts):
        for i, cell in enumerate(CELLS[cls]):
            buf = HEAP + 0x8000 + (cell & 0xFFF) * 0x40
            w.gm.w(buf, b"\x77" * 0x20)
            w.gm.w(buf + 4, dw(counts[i] if i < len(counts) else 0))
            w.gm.w(cell, qw(buf))

    def unplant(cls):
        for cell in CELLS[cls]:
            w.gm.w(cell, qw(0))

    # ================= classes 2..32 =============================
    for cls in range(2, 33):
        kind, bias, nexp = ARMS[cls]
        rec = {"arm": hex(jtab[cls - 1]), "kind": kind,
               "cells": [hex(c) for c in CELLS[cls]], "probes": []}
        if kind == "const":
            lo, hi = bias, CONST_HI[cls]
            for i in (lo - 1, lo, hi, hi + 1, -1):
                v, o = w.probe(cls, i)
                rec["probes"].append(
                    {"id": hex(i), "v": v, "obs": o})
            rec["bounds"] = [lo, hi]
            if [p["v"] for p in rec["probes"]] != [0, 1, 1, 0, 0]:
                fails.append((cls, "const", rec["probes"]))
        else:
            lo = bias
            # baseline — shipped state: descriptor cells are BSS
            # zeros -> the arm must reject even a mid-range id
            mid = lo + 0x10
            v, o = w.probe(cls, mid)
            rec["unplanted"] = {"id": hex(mid), "v": v, "obs": o}
            if v != 0:
                fails.append((cls, "unplanted-accepted", rec))
            # planted descriptor(s)
            counts = [3, 5, 7, 11] if kind == "sum4" else [N]
            plant(cls, counts)
            hi = lo + sum(counts) - 1
            for i in (lo - 1, lo, hi, hi + 1, -1):
                v, o = w.probe(cls, i)
                rec["probes"].append(
                    {"id": hex(i), "v": v, "obs": o})
            rec["bounds"] = [lo, hi]
            rec["count"] = sum(counts)
            if [p["v"] for p in rec["probes"]] != [0, 1, 1, 0, 0]:
                fails.append((cls, "range", rec["probes"]))
            # sum4 partial: one descriptor null contributes 0
            if kind == "sum4":
                w.gm.w(CELLS[cls][0], qw(0))
                hi2 = lo + (5 + 7 + 11) - 1
                v1, _ = w.probe(cls, hi2)
                v2, _ = w.probe(cls, hi2 + 1)
                rec["partial"] = {"sum": 23, "v_at_hi": v1,
                                  "v_at_hi1": v2}
                if not (v1 == 1 and v2 == 0):
                    fails.append((cls, "sum4-partial", rec))
            unplant(cls)
        results[str(cls)] = rec

    # ================= class 1: two-level dispatch ===============
    nib = [w.gm.dw(NIBTBL + n * 0x58) for n in range(16)]
    # plant every descriptor so each subclass arm is live
    for i, cell in enumerate(sorted({c for cs in CELLS.values()
                                     for c in cs})):
        buf = HEAP + 0x40000 + i * 0x100
        w.gm.w(buf, b"\x77" * 0x20)
        w.gm.w(buf + 4, dw(N))
        w.gm.w(cell, qw(buf))
    c1 = {"mapper_table": {"%X" % n: s for n, s in
                           enumerate(nib) if n < 15},
          "note": "id16>>12 -> d[1EEBCF8+n*0x58] = subclass "
                  "(ships n+5); full id then validated under "
                  "that arm; obs.arm records the arm hit",
          "cases": []}
    for n in range(15):
        s = nib[n]
        kind, bias, nexp = ARMS[s]
        if kind == "const":
            lo, hi = bias, CONST_HI[s]
        elif kind == "sum4":
            lo, hi = bias, bias + 4 * N - 1
        else:
            lo, hi = bias, bias + N - 1
        case = {"nibble": "%X" % n, "sub": s,
                "bounds": [lo, hi], "probes": []}
        for i in (lo - 1, lo, hi, hi + 1):
            v, o = w.probe(1, i)
            case["probes"].append({"id": hex(i), "v": v, "obs": o})
        c1["cases"].append(case)
        if [p["v"] for p in case["probes"]] != [0, 1, 1, 0]:
            fails.append(("cls1-n%X" % n, "range",
                          case["probes"]))
    for tag, i in (("F-nibble", 0xF000), ("hi-id", 0x11000),
                   ("neg", -1)):
        v, o = w.probe(1, i)
        c1["cases"].append({"nibble": tag, "probes":
                            [{"id": hex(i), "v": v, "obs": o}]})
    results["1"] = c1
    # undo the bulk plant for edge probes
    for cs in CELLS.values():
        for cell in cs:
            w.gm.w(cell, qw(0))

    results["edge"] = {
        "cls0":  {"v": w.probe(0, 0)[0]},
        "cls33": {"v": w.probe(33, 0)[0]}}

    summary = {"cases": sum(len(r.get("probes", r.get("cases", [])))
                            if isinstance(r, dict) else 0
                            for r in results.values()),
               "failures": fails,
               "faults": w.faults[:10]}
    with open(RESULT, "w") as f:
        json.dump({"summary": summary, "results": results,
                   "jtab": [hex(a) for a in jtab]}, f,
                  indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
