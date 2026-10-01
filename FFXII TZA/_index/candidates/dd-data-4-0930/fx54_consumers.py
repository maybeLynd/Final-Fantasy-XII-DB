"""Kind-0x54 effect mesh records: what the two vertex-prep consumers do with the +0x24 / +0x28 / +0x2C arrays
(SWE2-DATA 2026-09-30), static.

  V1 00435050 (single record): +0x24 (count +0x16) is block-copied 16 bytes per entry (shl 4) into the staging buffer,
     +0x2C (count +0x18) block-copied 8 bytes per entry (shl 3), +0x28 (count +0x18) goes through a byte kernel
     with the element's +0x40 block; the block copy is the CRT memcpy import.
  V2 00434CD0 (two records, factor xmm7): +0x28 is blended per byte channel and then passed through the same byte
     kernel; +0x2C is blended by a float-pair helper unless element +0x1F1 bit 5 selects a copy of the target record's
     pairs; +0x24 is blended by a third helper unless element +0x1F1 bit 6 selects a copy.
  V3 that third helper (00432030) is a normalised lerp: per entry it forms x*t' + x0 style blends of three floats,
     sums their squares, takes the square root through the CRT sqrtf import, divides one by it (a zero length keeps
     a constant) and scales the three components before storing the 16-byte entry. So the consumer treats +0x24 as
     unit direction vectors: the renormalisation is what a normal needs after interpolation.
Control C1: the same scanner reads the position array +0x20 in both consumers (the census page's control array).
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in dis(fn)}


def import_name(thunk):
    x = dis(thunk)[0]
    disp = int(x.op_str.split("+ 0x")[1].rstrip("]"), 16)
    iat = x.address + x.size + disp
    rva = struct.unpack_from("<Q", d, off(iat))[0]
    if rva >> 63:
        return "ordinal"
    a = 0x120000 + rva + 2
    o = off(a)
    return d[o:d.index(b"\0", o)].decode()


memcpy, sqrtf = import_name(0x00861EBA), import_name(0x00861F14)
print("   00861EBA -> %s ; 00861F14 -> %s" % (memcpy, sqrtf))
a = ins(0x00435050)
check("V1 00435050: +0x24 copied 16 B/entry, +0x2C 8 B/entry through memcpy; +0x28 to the byte kernel with element +0x40",
      memcpy == "memcpy"
      and a[0x004351D3].op_str == "ecx, dword ptr [rsi + 0x24]" and a[0x004351E5].op_str == "r8, 4"
      and a[0x004351EC].op_str == "0x861eba"
      and a[0x004351B5].op_str == "ecx, dword ptr [rsi + 0x2c]" and a[0x004351C7].op_str == "r8, 3"
      and a[0x004351CE].op_str == "0x861eba"
      and a[0x00435197].op_str == "ecx, dword ptr [rsi + 0x28]" and a[0x004351A6].op_str == "rdx, [r15 + 0x40]"
      and a[0x004351B0].op_str == "0x432300")
b = ins(0x00434CD0)
check("V2 00434CD0: +0x28 blended then byte kernel; +0x2C blend unless +0x1F1 bit 5; +0x24 blend unless bit 6",
      b[0x00434F09].op_str == "ecx, dword ptr [r13 + 0x28]" and b[0x00434F33].op_str == "0x433830"
      and b[0x00434F47].op_str == "0x432300"
      and b[0x00434F4C].op_str == "byte ptr [r14 + 0x1f1], 0x20" and b[0x00434F74].op_str == "0x861eba"
      and b[0x00434FAA].op_str == "0x4344c0"
      and b[0x00434FAF].op_str == "byte ptr [r14 + 0x1f1], 0x40" and b[0x00434FD7].op_str == "0x861eba"
      and b[0x00434FDE].op_str == "ecx, dword ptr [r13 + 0x24]" and b[0x0043500D].op_str == "0x432030")
n = ins(0x00432030)
check("V3 00432030: squares summed, sqrtf, 1/len (zero guarded), xyz scaled - a normalised lerp",
      sqrtf == "sqrtf"
      and n[0x0043219D].mnemonic == "mulss" and n[0x004321AE].mnemonic == "mulss" and n[0x004321B7].mnemonic == "mulss"
      and n[0x00432236].op_str == "0x861f14" and n[0x0043223B].op_str == "xmm0, xmm12"
      and n[0x00432249].op_str == "xmm6, xmm0"
      and n[0x0043225F].op_str == "xmm7, xmm6" and n[0x00432263].op_str == "xmm8, xmm6"
      and n[0x00432270].op_str == "xmm9, xmm6" and n[0x0043229D].op_str == "xmmword ptr [rax - 0x10], xmm0")
check("C1 control: both consumers read the position array +0x20",
      a[0x00435108].op_str == "ecx, dword ptr [rsi + 0x20]" and b[0x00434DB2].op_str == "ecx, dword ptr [r13 + 0x20]")
print("RESULT the consumers copy or blend +0x24 / +0x28 / +0x2C per entry; the +0x24 blend renormalises to unit length "
      "(normals), +0x28 goes through a per-byte kernel with the element's +0x40 block, +0x2C is copied or blended as "
      "float pairs")
print("FAILS %d" % FAILS)
