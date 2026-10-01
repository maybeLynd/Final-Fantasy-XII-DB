"""A faithful subset of the MSVC UCRT __stdio_common_vs*printf* family over an emulated va_list (x64: 8-byte slots,
floats passed as doubles). Supports flags -+ 0#, width, .precision (incl. *), length h hh l ll I64 z, and d i u x X o c s f F e E g G p %."""
import re
import struct

SPEC = re.compile(rb"%([-+ 0#]*)(\*|\d+)?(?:\.(\*|\d+))?(hh|h|ll|l|I64|I32|z|j|t|L)?([diouxXcsfFeEgGp%])")


def cstr(uc, a, limit=4096):
    b = bytes(uc.mem_read(a, limit))
    return b[:b.index(b"\0")] if b"\0" in b else b


def format_va(uc, fmt, va):
    out, pos, i = b"", 0, 0

    def nxt():
        nonlocal i
        v = struct.unpack("<Q", bytes(uc.mem_read(va + 8 * i, 8)))[0]
        i += 1
        return v
    for m in SPEC.finditer(fmt):
        out += fmt[pos:m.start()]
        pos = m.end()
        flags, width, prec, length, conv = m.groups()
        if conv == b"%":
            out += b"%"
            continue
        w = nxt() & 0xFFFFFFFF if width == b"*" else (int(width) if width else None)
        p = nxt() & 0xFFFFFFFF if prec == b"*" else (int(prec) if prec is not None else None)
        pyflags = flags.decode()
        if conv in b"di":
            v = nxt()
            bits = 64 if length in (b"ll", b"I64", b"z", b"j", b"t") else (16 if length == b"h" else (8 if length == b"hh" else 32))
            v &= (1 << bits) - 1
            if v >> (bits - 1):
                v -= 1 << bits
            s = ("%" + pyflags + (str(w) if w else "") + ("." + str(p) if p is not None else "") + "d") % v
        elif conv in b"uxXo":
            v = nxt()
            bits = 64 if length in (b"ll", b"I64", b"z", b"j", b"t") else (16 if length == b"h" else (8 if length == b"hh" else 32))
            v &= (1 << bits) - 1
            c = {"u": "d"}.get(conv.decode(), conv.decode())
            s = ("%" + pyflags + (str(w) if w else "") + ("." + str(p) if p is not None else "") + c) % v
        elif conv == b"c":
            s = chr(nxt() & 0xFF)
            s = s.rjust(w) if w and "-" not in pyflags else (s.ljust(w) if w else s)
        elif conv == b"s":
            a = nxt()
            t = cstr(uc, a).decode("latin-1") if a else "(null)"
            if p is not None:
                t = t[:p]
            s = t.rjust(w) if w and "-" not in pyflags else (t.ljust(w) if w else t)
        elif conv == b"p":
            s = "%016X" % nxt()
        else:
            d = struct.unpack("<d", struct.pack("<Q", nxt()))[0]
            s = ("%" + pyflags + (str(w) if w else "") + ("." + str(p) if p is not None else "") + conv.decode()) % d
        out += s.encode("latin-1")
    out += fmt[pos:]
    return out
