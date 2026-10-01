"""Bind the SHIPPED battle_pack.bin into a world.py Session by shipped code (OPUS, block 332; the method of blocks 324/326/328).

battle_pack.bin (us) is copied raw to B; 003846F0(&[0208E680], blob, 0) - the delivery stub 00238850's first call - relocates the
directory; then every binding call 00236C30 makes is made again with the same arguments, read from its own instruction stream
(003845F0 / 003846F0 slot binds, the inner binders 00238160 / 00238660 / 003847B0, and 00237FC0's first call). Not made: 00238880
and the tail of 00237FC0, which allocate from engine heap 6 (its allocator halts unbuilt). The codec base stays at the image's 0.
"""
import hashlib
import os
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

PACK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data",
                    "image", "ff12", "test_battle", "us", "binaryfile", "battle_pack.bin")
PACK_SHA = "d1bb89aac759cfcd4eb181715d9e88afb78d62a9a3fcffa6242f365f182cbc98"
B = 0x76100000
BINDERS = (0x3846F0, 0x3845F0, 0x238160, 0x238660, 0x3847B0)


def allowed(W):
    return set().union(*(W.closure(f) for f in BINDERS))


def _file_off(raw, va):
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    n = struct.unpack_from("<H", raw, pe + 6)[0]
    o = pe + 24 + struct.unpack_from("<H", raw, pe + 20)[0]
    for _ in range(n):
        vs, sva, rs, ra = struct.unpack_from("<IIII", raw, o + 8)
        if sva + 0x120000 <= va < sva + 0x120000 + rs:
            return ra + va - sva - 0x120000
        o += 40


def bind(W, S):
    """Returns (made, skipped): the calls re-made and the ones not made."""
    uc = S.uc
    pack = open(PACK, "rb").read()
    assert hashlib.sha256(pack).hexdigest() == PACK_SHA
    uc.mem_write(B, pack)
    assert S.call(0x3846F0, 0x208E680, B, 0)
    d = lambda off: struct.unpack("<I", bytes(uc.mem_read(B + off, 4)))[0]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    k = _file_off(W.raw, 0x236C70)
    slot = off = None
    r8 = 0
    made, skipped = [], []
    for ins in md.disasm(W.raw[k:k + 0x3D0], 0x236C70):
        m = re.search(r"rip \+ (0x[0-9a-f]+)", ins.op_str)
        if ins.mnemonic == "lea" and ins.op_str.startswith("rcx") and m:
            slot = ins.address + ins.size + int(m.group(1), 16)
        mm = re.search(r"\[r[ac]x \+ (0x[0-9a-f]+)\]", ins.op_str)
        if ins.mnemonic in ("movsxd", "mov") and ins.op_str.startswith(("rdx", "ecx")) and mm:
            off = int(mm.group(1), 16)
        if ins.mnemonic == "xor" and ins.op_str == "r8d, r8d":
            r8 = 0
        if ins.mnemonic == "mov" and ins.op_str.startswith("r8d, "):
            r8 = int(ins.op_str.split(", ")[1], 16)
        if ins.mnemonic == "call":
            fn = int(ins.op_str, 16)
            if fn in (0x3845F0, 0x3846F0):
                assert S.call(fn, slot, d(off), r8)
                made.append("%08X <- +%X" % (slot, off))
            elif fn in (0x238160, 0x238660, 0x3847B0):
                assert S.call(fn, d(off))
                made.append("%X(+%X)" % (fn, off))
            elif fn == 0x237FC0:
                assert S.call(0x3845F0, 0x2EBF138, d(off))
                made.append("02EBF138 <- +%X (00237FC0's first call)" % off)
                skipped.append("00237FC0 tail (heap 6)")
            else:
                skipped.append("%X (heap 6)" % fn)
            slot = off = None
        if ins.mnemonic == "ret":
            break
    return made, skipped
