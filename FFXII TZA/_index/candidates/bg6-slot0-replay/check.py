"""BG-6 slot-0 surrogate replay (SWE2-ORACLE, 2026-10-02).

Executes PrimitiveRendererD3D11 vtable slot 0, `006CA760`, under Unicorn
against a synthetic device object. The static row is already ANSWERED
(`d[dev+0x18860]` has exactly two image-wide touches — the read here and
the clear here — so slot 0 always returns the same 0x7FE0 staging block
and zeroes the index). This surrogate adds an executed confirmation and
checks the *counterfactual* the static answer implies: if the index cell
were nonzero, the function honors it (imul by 0x7FE0) — i.e. "always 0"
is a population fact, not a function constant.

NATIVE-REPLAY evidence; the device object is a synthetic fixture
(disclosed), live_game: false.
"""
import hashlib, json, os, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RAX, UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO = 0x120000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

F = 0x006CA760
IDX, BLK, PUB = 0x18860, 0x10880, 0xB8
STRIDE = 0x7FE0


def load():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs = []
    off = pe + 24 + optsz
    for i in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8 + i * 40)
        secs.append((va + IMG_LO, max(vs, rs), ra, rs))
    return raw, secs


def run(idx):
    raw, secs = load()
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for va, sz, ra, rs in secs:
        lo, hi = va & ~0xFFF, (va + sz + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        if rs:
            uc.mem_write(va, raw[ra:ra + rs])
    uc.mem_map(HEAP, 0x20000)
    uc.mem_map(STACK - 0x100000, 0x200000)
    uc.mem_map(RETQ, 0x1000)
    uc.mem_write(RETQ, b"\xF4")  # hlt sentinel
    dev = HEAP
    uc.mem_write(dev + IDX, struct.pack("<I", idx))
    uc.reg_write(UC_X86_REG_RCX, dev)
    uc.reg_write(UC_X86_REG_RSP, STACK - 0x100)
    uc.mem_write(STACK - 0x100, struct.pack("<Q", RETQ))
    uc.emu_start(F, RETQ, timeout=10_000_000)
    ret = uc.reg_read(UC_X86_REG_RAX)
    idx_after = struct.unpack("<I", uc.mem_read(dev + IDX, 4))[0]
    pub = struct.unpack("<Q", uc.mem_read(dev + PUB, 8))[0]
    return dict(idx_in=idx, ret=ret - dev, idx_after=idx_after,
                pub=pub - dev)


def main():
    cases = []
    for idx in (0, 1, 3):
        r = run(idx)
        r["expect_ret"] = BLK + idx * STRIDE
        r["pass"] = (r["ret"] == r["expect_ret"] and r["idx_after"] == 0
                     and r["pub"] == r["ret"])
        cases.append(r)
    md5 = hashlib.md5(json.dumps(cases, sort_keys=True).encode()).hexdigest()
    out = dict(subject="006CA760 (PrimitiveRendererD3D11 slot 0)",
               exe_sha=SHA, cases=cases, md5=md5,
               live_game=False,
               note="synthetic device object; NATIVE-REPLAY class only")
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "result.json"), "w"), indent=2)
    for c in cases:
        print("PASS" if c["pass"] else "FAIL",
              f"idx={c['idx_in']} ret=+{c['ret']:#x} "
              f"idx_after={c['idx_after']} pub=+{c['pub']:#x}")
    print("md5", md5)
    sys.exit(0 if all(c["pass"] for c in cases) else 1)


if __name__ == "__main__":
    main()
