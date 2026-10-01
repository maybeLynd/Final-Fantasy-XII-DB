#!/usr/bin/env python3
"""disasm_fn.py - disassemble a function and RESOLVE every RIP-relative target with the tool.

The project's standing rule is that a RIP-relative target is computed by a tool and never by
hand, and every block that needed one has so far written the arithmetic inline. This is that
arithmetic, once.

What it adds over a plain disassembly
-------------------------------------
* every `[rip + disp]` operand is annotated with its absolute target;
* a target that lands in a read-only section is decoded as a **C string** when it looks like one,
  because a constructor's strings are usually what names it;
* a target that lands in `.rdata` and is followed by a plausible pointer is reported as a
  possible **vtable**, and the 8 bytes before it are printed -- MSVC puts the RTTI complete-object
  locator at `vtable - 8`, which is how the input name registry was named;
* `call` and `jmp` targets are printed as function addresses so a caller graph can be read off.

**It reads the shipped executable, never a decompiler's output.** The GFZ can be wrong; the bytes
cannot.
"""
import argparse
import struct
import sys
import kit_paths as KP  # noqa: E402
import os

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP
except ImportError:
    sys.stderr.write("disasm_fn: needs capstone (pip install capstone)\n")
    raise SystemExit(2)

DEFAULT_EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")


class Image(object):
    def __init__(self, path):
        d = open(path, "rb").read()
        self.d = d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        optsz = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
        self.secs = []
        off = pe + 24 + optsz
        for _ in range(nsec):
            name = d[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
            vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
            self.secs.append((name, va, vs, ra, rs))
            off += 40

    def section(self, va):
        r = va - self.base
        for name, sva, vs, ra, rs in self.secs:
            if sva <= r < sva + max(vs, rs):
                return name
        return None

    def read(self, va, n):
        """Bytes at va, or None. **Bounded by SizeOfRawData**, never the virtual size -- past it
        the file holds whatever the next section starts with, and this project has already been
        burned once reading a BSS 'default' out of the following section."""
        r = va - self.base
        for _name, sva, vs, ra, rs in self.secs:
            if sva <= r < sva + max(vs, rs):
                o = r - sva
                if o >= rs:
                    return None                      # in the virtual span, past the raw data
                return self.d[ra + o: ra + o + n]
        return None

    def cstring(self, va, limit=96):
        b = self.read(va, limit)
        if not b:
            return None
        z = b.find(b"\0")
        if z <= 0:
            return None
        s = b[:z]
        if not all(32 <= c < 127 or c in (9,) for c in s):
            return None
        return s.decode("ascii")

    def qword(self, va):
        b = self.read(va, 8)
        return struct.unpack("<Q", b)[0] if b and len(b) == 8 else None


def annotate(img, va):
    """-> a short note about what lives at va, or ''."""
    sec = img.section(va)
    if sec is None:
        return "unmapped"
    s = img.cstring(va)
    if s is not None and len(s) >= 3:
        return '%s  "%s"' % (sec, s)
    # a possible vtable: a pointer that lands in .text, with an RTTI locator 8 bytes before
    q = img.qword(va)
    if q and img.section(q) == ".text":
        loc = img.qword(va - 8)
        extra = ""
        if loc and img.section(loc) is not None:
            extra = "  RTTI locator -> %08X" % loc
        return "%s  possible VTABLE, [0]=%08X%s" % (sec, q, extra)
    if q is not None:
        return "%s  qword=%016X" % (sec, q)
    return sec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("addr", type=lambda x: int(x, 16))
    ap.add_argument("length", type=lambda x: int(x, 0))
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--calls-only", action="store_true")
    a = ap.parse_args()

    img = Image(a.exe)
    code = img.read(a.addr, a.length)
    if code is None or len(code) < a.length:
        raise SystemExit("could not read %d bytes at %08X" % (a.length, a.addr))

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for ins in md.disasm(code, a.addr):
        note = ""
        for op in ins.operands:
            if op.type == X86_OP_MEM and op.value.mem.base == X86_REG_RIP:
                tgt = ins.address + ins.size + op.value.mem.disp
                note = "  ; %08X  %s" % (tgt, annotate(img, tgt))
        if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
            tgt = int(ins.op_str, 16)
            note = "  ; -> %08X" % tgt
        if a.calls_only and not note:
            continue
        print("%08X  %-30s %s%s" % (ins.address, ins.bytes.hex(),
                                    ins.mnemonic + " " + ins.op_str, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
