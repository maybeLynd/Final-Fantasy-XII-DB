"""Shared loader for the S-25 probes (read-only; nothing here writes outside this folder).

Maps the shipped FFXII_TZA.exe at its canonical VAs (image base 0x120000), verifying the
certified SHA-256, and exposes byte reads for capstone and for Unicorn worlds.
"""
import hashlib
import struct

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000


def load():
    raw = open(EXE, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    assert got == SHA, "EXE hash mismatch: %s" % got
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


def read(raw, secs, va, n):
    rva = va - BASE
    for sva, vs, ra, rs in secs:
        if sva <= rva < sva + max(vs, rs):
            return raw[ra + rva - sva: ra + rva - sva + n]
    raise KeyError(hex(va))
