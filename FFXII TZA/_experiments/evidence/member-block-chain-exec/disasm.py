"""Linear disasm of the shipped EXE at canonical (base-inclusive) VAs.

usage: disasm.py <hex-addr> <count>
"""
import struct
import sys
import capstone

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
IMG_LO = 0x120000

raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va, vs, ra, rs))
    off += 40


def read_va(va, n):
    """va is canonical (base-inclusive). Returns bytes."""
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva < sva + vs:
            ro = ra + (rva - sva)
            return raw[ro:ro + n]
    return b""


def main():
    addr = int(sys.argv[1], 16)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    if addr < IMG_LO:
        addr += IMG_LO  # accept base-less addrs too
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    buf = read_va(addr, max(n * 8, 0x400))
    for i, ins in enumerate(md.disasm(buf, addr)):
        if i >= n:
            break
        print("  %08X  %-22s %s" % (ins.address,
              ins.bytes.hex(), ins.mnemonic + " " + ins.op_str))


if __name__ == "__main__":
    main()
