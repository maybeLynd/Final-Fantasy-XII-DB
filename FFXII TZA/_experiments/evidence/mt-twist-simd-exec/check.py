#!/usr/bin/env python
# EXP-111 — mt-twist-simd-exec: isolated original-code execution of the
# shipped MT19937 twist 00866B90 under BOTH arms of its CPU-feature gate.
#
#   00866B90  sub rsp,0x28 ; xor ecx,ecx
#             cmp d[0x1F44858],2 ; jl 00866C89     <- feature gate
#   SIMD arm 00866BA3..00866C88: vector loop rax 0x2EB3EA4..0x2EB4224
#             step 0x20 (8 elems/iter, 28 iters = 0xE0 elems):
#               y = (s[i]&xmm3_upmask) | (s[i+1]&xmm4_lomask)
#               s[i] = s[i+397] ^ (y>>1) ^ ((s[i+1]&1)*0x9908B0DF)
#             ecx = 0xE0 on exit
#   scalar1  00866C89..: r8 = state+ecx*4 .. 0x2EB3BFC  (i in [ecx,0xE3))
#             s[i] = s[i+397] ^ twist(s[i],s[i+1])
#   scalar2  00866CE2..: rax 0x2EB3BFC .. 0x2EB422C    (i in [0xE3,0x26F))
#             s[i] = s[i-227] ^ twist(s[i],s[i+1])
#   tail     s[623] = s[396] ^ twist(s[623],s[0]); mti[0x2EB4230] = 0
#
# Shipped image plants d[0x1F44858]=1 -> the SIMD arm is NEVER entered
# (contract claim-table row: UNKNOWN). This harness plants the dword
# per case and compares the full 624-dword post-twist state plus the
# mti reset against (a) the other arm's native run and (b) an
# independent Python MT19937 twist.
#
# ZERO scripted boundaries — the body is a leaf.

import ctypes, hashlib, json, random, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_MEM_UNMAPPED, UC_MODE_64, \
    UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RSP, \
    UC_X86_REG_XMM6, UC_X86_REG_XMM7

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

STACK  = 0x61000000
RETQ   = 0x62000000

TWIST  = 0x00866B90
FEATD  = 0x01F44858            # CPU-feature dword (image plants 1)
STATE  = 0x02EB3870            # MT state array, 624 dwords
MTI    = 0x02EB4230            # twist-count cell (reset to 0)
N      = 624
MAGIC  = 0x9908B0DF

MASK_LO = 0x7FFFFFFF           # xmm4 lane mask (low 31 bits)
MASK_HI = 0x80000000           # xmm3 lane mask (sign bit)
MASK_Y  = 0x7FFFFFFE           # scalar 'and edx' mask


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


def py_twist(s):
    """Independent MT19937 twist (N=624, M=397)."""
    s = list(s)
    for i in range(N - 397):
        y = (s[i] & MASK_HI) | (s[i + 1] & MASK_LO)
        s[i] = s[i + 397] ^ (y >> 1) ^ (MAGIC if y & 1 else 0)
    for i in range(N - 397, N - 1):
        y = (s[i] & MASK_HI) | (s[i + 1] & MASK_LO)
        s[i] = s[i - 227] ^ (y >> 1) ^ (MAGIC if y & 1 else 0)
    y = (s[N - 1] & MASK_HI) | (s[0] & MASK_LO)
    s[N - 1] = s[396] ^ (y >> 1) ^ (MAGIC if y & 1 else 0)
    return s


def run_twist(state_words, feat, raw, secs, patch=()):
    """Execute the shipped 00866B90 on a planted state; return
    (faults, final_state, mti)."""
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    gm = GuestMem(uc)
    gm.map(IMG_LO, IMG_HI - IMG_LO)
    for sva, vs, ra, rs in secs:
        if vs and rs:
            gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
    gm.map(STACK, 0x100000)
    gm.map(RETQ, 0x1000)
    gm.w(RETQ, b"\xc3" + b"\xcc" * 0xFF)
    faults = []
    uc.hook_add(UC_HOOK_MEM_UNMAPPED,
                lambda u, a, ad, sz, v, c: faults.append(
                    "mem %x addr=%x" % (a, ad)) or False)
    gm.w(FEATD, dw(feat))
    gm.w(STATE, b"".join(dw(x) for x in state_words))
    gm.w(MTI, dw(0xDEADBEEF))
    for va, data in patch:
        gm.w(va, data)
    uc.reg_write(UC_X86_REG_RSP, STACK + 0x8000)
    uc.reg_write(UC_X86_REG_RIP, TWIST)
    uc.mem_write(STACK + 0x8000, struct.pack("<Q", RETQ))
    uc.reg_write(UC_X86_REG_XMM6,
                 (0xC6C6C6C6C6C6C6C6 << 64) | 0x6C6C6C6C6C6C6C6C)
    uc.reg_write(UC_X86_REG_XMM7,
                 (0xC7C7C7C7C7C7C7C7 << 64) | 0x7C7C7C7C7C7C7C7C)
    try:
        uc.emu_start(TWIST, RETQ, count=20000)
    except Exception as e:
        faults.append("emu %s" % e)
    out = list(struct.unpack("<%dI" % N, gm.r(STATE, N * 4)))
    mti = struct.unpack("<I", gm.r(MTI, 4))[0]
    canary = gm.r(STACK + 0x8000 - 0x28, 0x20)
    return faults, out, mti, canary


def build_states():
    rng = random.Random(0x12E2)
    S = {}
    S["zeros"] = [0] * N
    S["ones"] = [0xFFFFFFFF] * N
    S["inc"] = [(i * 0x9E3779B9) & 0xFFFFFFFF for i in range(N)]
    S["rand"] = [rng.getrandbits(32) for _ in range(N)]
    S["lsb-alt"] = [i & 1 for i in range(N)]          # only bit0 varies
    S["hi-only"] = [(0x80000000 if i % 3 == 0 else 0) for i in range(N)]
    S["edge-mix"] = [0x80000001, 0x00000001, 0x7FFFFFFF,
                     0x80000000] * (N // 4)
    S["std-seed"] = [19650218 + i for i in range(N)]  # canonical-ish
    return S


def main():
    raw, secs = load_image()
    states = build_states()
    npass = nfail = 0
    fails = []
    for name, s in states.items():
        ref = py_twist(s)
        f1, out1, mti1, _ = run_twist(s, 1, raw, secs)
        f2, out2, mti2, _ = run_twist(s, 2, raw, secs)
        errs = []
        if f1 or f2:
            errs.append("faults scalar=%s simd=%s" % (f1, f2))
        if out1 != ref:
            d = [i for i in range(N) if out1[i] != ref[i]]
            errs.append("scalar mismatched model at %d elems e.g. %s" %
                        (len(d), d[:5]))
        if out2 != ref:
            d = [i for i in range(N) if out2[i] != ref[i]]
            errs.append("simd mismatched model at %d elems e.g. %s" %
                        (len(d), d[:5]))
        if out1 != out2:
            d = [i for i in range(N) if out1[i] != out2[i]]
            errs.append("scalar!=simd at %d elems e.g. %s" %
                        (len(d), d[:5]))
        if mti1 != 0 or mti2 != 0:
            errs.append("mti scalar=%x simd=%x exp=0" % (mti1, mti2))
        if errs:
            nfail += 1
            fails.append((name, errs))
            print("FAIL %s" % name)
            for e in errs:
                print("   %s" % e)
        else:
            npass += 1
            print("pass %s" % name)
    print("== %d/%d state cases passed" % (npass, npass + nfail))
    killed, alive, badsite = run_mutants(states["rand"], raw, secs)
    print("== mutants: %d killed, %d alive, %d badsite" %
          (len(killed), len(alive), len(badsite)))
    for n in alive:
        print("   ALIVE %s" % n)
    for n, w in badsite:
        print("   BADSITE %s %s" % (n, w))
    json.dump({"cases": npass + nfail, "pass": npass,
               "fails": [f[0] for f in fails],
               "mutants": len(MUTS), "killed": len(killed),
               "alive": alive,
               "badsite": [b[0] for b in badsite]},
              open("result.json", "w"), indent=1)
    return 1 if (nfail or alive or badsite) else 0


# ---- mutants ---------------------------------------------------------------
# (name, va, orig_byte, patch_byte, arm: 0=scalar flag=1, 2=simd flag=2,
#  9=gate both)
MUTS = [
    # gate: jl -> jge (inverts which arm runs)
    ("m-gate",      0x866B9E, 0x8C, 0x8D, 0),
    # SIMD: elements-per-iter counter 0xE0 -> 0xE1 (tail seed shifts)
    ("m-simd-ecx",  0x866BC5, 0xE0, 0xE1, 2),
    # SIMD: upper mask const sign bit -> 0
    ("m-simd-hi",   0x1CCFE03, 0x80, 0x00, 2),
    # SIMD: lower mask const -> &0x7FFFFF
    ("m-simd-lo",   0x1CCFDF0, 0xFE, 0xFC, 2),
    # SIMD: magic const low byte
    ("m-simd-mag",  0x1CCFE10, 0xDF, 0xDE, 2),
    # SIMD: odd-element mask xmm7 = 1 -> 0 (kills the magic term)
    ("m-simd-odd",  0x1CEBCD0, 0x01, 0x00, 2),
    # SIMD: write target -0x634 -> -0x630
    ("m-simd-dst",  0x866C2D, 0xCC, 0xD0, 2),
    # SIMD: lane stride add 0x20 -> 0x10
    ("m-simd-adv",  0x866C76, 0x20, 0x10, 2),
    # SIMD: s[i+397] read offset [rax] -> [rax+8]
    ("m-simd-src",  0x866C17, 0x00, 0x08, 2),
    # scalar1: lomask 0x7FFFFFFE -> 0x7FFFFFFF
    ("m-sc1-mask",  0x866CBE, 0xFE, 0xFC, 0),
    # scalar1: magic imm
    ("m-sc1-mag",   0x866CC4, 0xDF, 0xDE, 0),
    # scalar1: s[i+397] offset +0x634 -> +0x638
    ("m-sc1-m",     0x866CD2, 0x34, 0x38, 0),
    # scalar1: loop bound r8<rax via jl -> never
    ("m-sc1-loop",  0x866CE0, 0x7C, 0xEB, 0),
    # scalar1: odd test &1 -> &2
    ("m-sc1-odd",   0x866CBB, 0x01, 0x02, 0),
    # scalar2: s[i-227] offset -0x38C -> -0x390
    ("m-sc2-m",     0x866D0E, 0x74, 0x70, 0),
    # scalar2: loop bound jl -> never
    ("m-sc2-loop",  0x866D1B, 0x7C, 0xEB, 0),
    # tail: s[0] read -> s[1]
    ("m-tail-s0",   0x866D25, 0x47, 0x4B, 0),
    # tail: lsb magic imul const
    ("m-tail-mag",  0x866D46, 0xDF, 0xDE, 0),
    # tail: mti reset value 0 -> 1
    ("m-tail-mti",  0x866D38, 0x00, 0x01, 0),
    # scalar1: shr edx,1 -> shr edx,2
    ("m-sc1-shr",   0x866CCC, 0xEA, 0xEB, 0),
]


def run_mutants(seed_state, raw, secs):
    killed, alive, badsite = [], [], []
    # baselines for both arms on the same state
    _, base1, mti1, can1 = run_twist(seed_state, 1, raw, secs)
    _, base2, mti2, can2 = run_twist(seed_state, 2, raw, secs)
    for name, va, orig, patch, arm in MUTS:
        raw_b = None
        for sva, vs, ra, rs in secs:
            rva = va - IMG_LO
            if sva <= rva < sva + rs:
                raw_b = raw[ra + (rva - sva)]
        if raw_b is not None and raw_b != orig:
            badsite.append((name, "site byte %02x != orig %02x" %
                            (raw_b, orig)))
            continue
        fl = 1 if arm == 0 else 2
        f, out, mti, can = run_twist(seed_state, fl, raw, secs,
                                patch=[(va, bytes([patch]))])
        base = base1 if arm == 0 else base2
        base_mti = mti1 if arm == 0 else mti2
        base_can = can1 if arm == 0 else can2
        if f or out != base or mti != base_mti or can != base_can:
            killed.append(name)
        else:
            alive.append(name)
    return killed, alive, badsite


if __name__ == "__main__":
    sys.exit(main())
