"""Import bridges for the S-40 replay (OPUS, 2026-09-26), installed by name at each import's trap in block 332's world.

C runtime (ucrtbase): strtok_s, sscanf (__stdio_common_vsscanf, d/u/x/X conversions; %i, %s, %c and anything else STOP the run),
memcmp and the other string functions, each with the C library's semantics.
C++ runtime (msvcp140): the six std::basic_streambuf<char> / basic_istream<char> members the Yebis licence reader uses
(0071D9E0): construct, read -> sgetn over the get area, rdbuf(p), destroy - standard semantics over the MSVC x64 layout, and
FAIL-CLOSED: read() refuses unless the stream buffer's xsgetn / uflow / underflow slots resolve to the base-class imports, the
DLL's own vtables and locale live on a non-executable page, and an istream built as a base subobject is refused.
Every bridged call is appended to `log`."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP


def cstr(u, a, n=None):
    """The NUL-terminated string at a, read in page-bounded chunks to its terminator (n caps it for display only)."""
    out = b""
    while True:
        k = 0x1000 - (a & 0xFFF)
        b = bytes(u.mem_read(a, k))
        z = b.find(b"\0")
        if z >= 0:
            out += b[:z]
            break
        out += b
        a += k
    return out[:n] if n else out


def install(W, uc, log):
    pe = pefile.PE(W.EXE)
    IAT = {(imp.name or b"").decode(): imp.address for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]

    def strtok_s(u):                                     # (str, delim, context): the C library's strtok_s
        s, dl, ctx = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        if s == 0:
            s = q(ctx)
        if s == 0:
            return 0
        d = set(cstr(u, dl))
        b = cstr(u, s)
        i = 0
        while i < len(b) and b[i] in d:
            i += 1
        if i == len(b):
            uc.mem_write(ctx, struct.pack("<Q", s + i))
            return 0
        j = i
        while j < len(b) and b[j] not in d:
            j += 1
        if j < len(b):
            u.mem_write(s + j, b"\0")
            uc.mem_write(ctx, struct.pack("<Q", s + j + 1))
        else:
            uc.mem_write(ctx, struct.pack("<Q", s + j))
        return s + i

    def strlen(u):
        return len(cstr(u, u.reg_read(UC_X86_REG_RCX)))

    def strcmp(u):
        a, b = cstr(u, u.reg_read(UC_X86_REG_RCX)), cstr(u, u.reg_read(UC_X86_REG_RDX))
        return 0 if a == b else (0xFFFFFFFF if a < b else 1)

    def strncmp(u):
        n = u.reg_read(UC_X86_REG_R8)
        a, b = cstr(u, u.reg_read(UC_X86_REG_RCX))[:n], cstr(u, u.reg_read(UC_X86_REG_RDX))[:n]
        return 0 if a == b else (0xFFFFFFFF if a < b else 1)

    def _stricmp(u):
        a, b = cstr(u, u.reg_read(UC_X86_REG_RCX)).lower(), cstr(u, u.reg_read(UC_X86_REG_RDX)).lower()
        return 0 if a == b else (0xFFFFFFFF if a < b else 1)

    def strcpy_s(u):                                     # (dst, size, src)
        d, n, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        b = cstr(u, s)
        if len(b) + 1 > n:
            return 34
        u.mem_write(d, b + b"\0")
        return 0

    def strncpy_s(u):                                    # (dst, size, src, count)
        d, n, s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)
        b = cstr(u, s)
        if c != 0xFFFFFFFFFFFFFFFF:
            b = b[:c]
        if len(b) + 1 > n:
            return 34
        u.mem_write(d, b + b"\0")
        return 0

    def strcat_s(u):
        d, n, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        a, b = cstr(u, d), cstr(u, s)
        if len(a) + len(b) + 1 > n:
            return 34
        u.mem_write(d + len(a), b + b"\0")
        return 0

    def atoi(u):
        b = cstr(u, u.reg_read(UC_X86_REG_RCX)).strip()
        k = 0
        while k < len(b) and (b[k:k + 1].isdigit() or (k == 0 and b[k:k + 1] in b"+-")):
            k += 1
        try:
            return int(b[:k]) & 0xFFFFFFFF
        except ValueError:
            return 0

    def strrchr(u):
        s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF
        b = cstr(u, s)
        i = len(b) if c == 0 else b.rfind(bytes([c]))
        return s + i if i >= 0 else 0

    def strstr(u):
        s, t = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        i = cstr(u, s).find(cstr(u, t))
        return s + i if i >= 0 else 0

    def memcmp(u):
        a, b, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        x, y = bytes(u.mem_read(a, n)), bytes(u.mem_read(b, n))
        return 0 if x == y else (0xFFFFFFFF if x < y else 1)

    class Unsupported(Exception):
        pass

    def __stdio_common_vsscanf(u):                       # (options, buffer, count, format, locale, va): the C library's sscanf,
        buf, cnt, fmt = u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)   # for d i u x X s c
        va = q(u.reg_read(UC_X86_REG_RSP) + 0x30)                                    # conversions only; anything else stops
        s = cstr(u, buf)
        if cnt != 0xFFFFFFFFFFFFFFFF:
            s = s[:cnt]
        f = cstr(u, fmt)
        i = j = assigned = 0
        ws = b" \t\n\r\v\f"
        while j < len(f):
            c = f[j:j + 1]
            if c in (b" ", b"\t", b"\n"):
                while i < len(s) and s[i:i + 1] in ws:
                    i += 1
                j += 1
                continue
            if c != b"%":
                if i >= len(s) or s[i:i + 1] != c:
                    break
                i += 1; j += 1
                continue
            j += 1
            suppress = f[j:j + 1] == b"*"
            if suppress:
                j += 1
            width = 0
            while f[j:j + 1].isdigit():
                width = width * 10 + int(f[j:j + 1]); j += 1
            size = 4
            for m, sz in ((b"hh", 1), (b"ll", 8), (b"I64", 8), (b"h", 2), (b"l", 4)):
                if f[j:j + len(m)] == m:
                    size = sz; j += len(m)
                    break
            conv = f[j:j + 1]; j += 1
            if conv in (b"d", b"i", b"u", b"x", b"X"):
                while i < len(s) and s[i:i + 1] in ws:
                    i += 1
                lim = width or 1 << 30
                k = i
                if k < len(s) and s[k:k + 1] in b"+-" and conv in (b"d", b"i"):
                    k += 1
                if conv in (b"x", b"X") and s[k:k + 2] in (b"0x", b"0X") and (not width or width >= 3):
                    k += 2                                   # C's %x accepts an optional 0x prefix
                digits = b"0123456789abcdefABCDEF" if conv in (b"x", b"X") else b"0123456789"
                if conv == b"i":
                    raise Unsupported("%i")
                while k < len(s) and k - i < lim and s[k:k + 1] in digits:
                    k += 1
                tok = s[i:k]
                if not tok or tok in (b"+", b"-"):
                    break
                v = int(tok.replace(b"0x", b"").replace(b"0X", b"") or b"0", 16) if conv in (b"x", b"X") else int(tok, 10)
                i = k
                if not suppress:
                    p = q(va); va += 8
                    u.mem_write(p, struct.pack({1: "<B", 2: "<H", 4: "<I", 8: "<Q"}[size], v & ((1 << (8 * size)) - 1)))
                    assigned += 1
            elif conv == b"s":
                raise Unsupported("%s needs a buffer-size argument under the secure CRT")
            elif conv == b"c":
                raise Unsupported("%c")
            elif conv == b"%":
                if s[i:i + 1] != b"%":
                    break
                i += 1
            else:
                raise Unsupported("%" + conv.decode("latin1"))
        return 0xFFFFFFFF if (not s and assigned == 0) else assigned

    # ---- msvcp140 std::basic_streambuf<char> / basic_istream<char> (MSVC STL, x64 layout) --------------------------------------
    # streambuf: +0 vfptr, +8 _Gfirst, +0x10 _Pfirst, +0x18 _IGfirst, +0x20 _IPfirst, +0x28 _Gnext, +0x30 _Pnext, +0x38 _IGnext,
    #   +0x40 _IPnext, +0x48 _Gcount, +0x4C _Pcount, +0x50 _IGcount, +0x58 _IPcount, +0x60 _Plocale (the offsets the image's inline
    #   setg writes at 0071DB6B-0071DB84 through _IGfirst / _IGnext / _IGcount).
    # istream (most-derived construction): +0 vbptr, +8 _Chcount, +0x10 the virtual base basic_ios: ios_base {+0 vfptr, +8 _Stdstr,
    #   +0x10 _Mystate, +0x14 _Except, +0x18 _Fmtfl, +0x20 _Prec, +0x28 _Wide, +0x30 _Arr, +0x38 _Calls, +0x40 _Ploc}, then
    #   +0x48 _Mystrbuf, +0x50 _Tiestr, +0x58 _Fillch. The image reads only the vbtable's base offset ([vbptr + 4]).
    # The DLL's own vtables / vbtable / locale objects are external data; the bridge gives them addresses on a NON-EXECUTABLE model
    # page, so any virtual call through them faults (fails closed) instead of running.
    MP = 0x7B800000
    uc.mem_map(MP, 0x10000, 1)                           # read-only: data, never code
    uc.mem_write(MP, bytes(0x10000))
    SB_VT, IOS_VT, VBT, LOC = MP + 0x100, MP + 0x200, MP + 0x300, MP + 0x400
    uc.mem_write(VBT, struct.pack("<ii", 0, 0x10))
    d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]

    def w8(a, v):
        uc.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def slot_import(obj, k):                            # the import a vtable slot resolves to (image thunk `jmp [IAT]`), else None
        t = q(q(obj) + 8 * k)
        b = bytes(uc.mem_read(t, 6))
        if b[:2] != b"\xFF\x25":
            return None
        iat = t + 6 + struct.unpack("<i", b[2:6])[0]
        return next((k2 for k2, v in IAT.items() if v == iat), None)

    def sb_ctor(u):                                     # basic_streambuf() : _Plocale(new locale), _Init()
        t = u.reg_read(UC_X86_REG_RCX)
        w8(t, SB_VT)
        for off in (8, 0x10, 0x28, 0x30):
            w8(t + off, 0)
        uc.mem_write(t + 0x48, struct.pack("<ii", 0, 0))
        for p, f in ((0x18, 8), (0x20, 0x10), (0x38, 0x28), (0x40, 0x30), (0x50, 0x48), (0x58, 0x4C)):
            w8(t + p, t + f)
        w8(t + 0x60, LOC)
        return t

    def is_ctor(u):                                     # basic_istream(streambuf *, bool isstd) [+ most-derived flag]
        t, sb, isstd, md = (u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        if not md & 0xFFFFFFFF:
            raise Unsupported("istream constructed as a base subobject")
        w8(t, VBT)
        w8(t + 8, 0)                                    # _Chcount
        io = t + 0x10
        w8(io, IOS_VT)
        w8(io + 8, 0)
        uc.mem_write(io + 0x10, struct.pack("<iii", 0 if sb else 4, 0, 0x201))   # state (badbit if no buffer), except, skipws|dec
        w8(io + 0x20, 6); w8(io + 0x28, 0); w8(io + 0x30, 0); w8(io + 0x38, 0); w8(io + 0x40, LOC)
        w8(io + 0x48, sb); w8(io + 0x50, 0)
        uc.mem_write(io + 0x58, b" ")
        return t

    def is_read(u):                                     # read(buf, n): sentry(noskip) -> rdbuf()->sgetn -> eof|fail on short
        t, buf, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        io = t + struct.unpack("<i", bytes(uc.mem_read(q(t) + 4, 4)))[0]
        state = d4(io + 0x10)
        w8(t + 8, 0)
        if state != 0 or q(io + 0x50):
            if q(io + 0x50):
                raise Unsupported("tied stream")
            uc.mem_write(io + 0x10, struct.pack("<I", state | 2))   # sentry failed: failbit
            return t
        if n <= 0:
            return t
        sb = q(io + 0x48)
        got = 0
        for k, want in ((8, "xsgetn"), (7, "uflow"), (6, "underflow")):
            nm_ = slot_import(sb, k) or ""
            if want not in nm_:
                raise Unsupported("streambuf slot %d is not the base %s" % (k, want))
        while got < n:                                  # base xsgetn over the get area; base uflow -> base underflow -> eof
            gnext, gcount = q(q(sb + 0x38)), struct.unpack("<i", bytes(uc.mem_read(q(sb + 0x50), 4)))[0]
            avail = gcount if gnext else 0
            if avail <= 0:
                break
            k = min(avail, n - got)
            uc.mem_write(buf + got, bytes(uc.mem_read(gnext, k)))
            got += k
            uc.mem_write(q(sb + 0x50), struct.pack("<i", gcount - k))
            w8(q(sb + 0x38), gnext + k)
        w8(t + 8, got)
        if got != n:
            uc.mem_write(io + 0x10, struct.pack("<I", state | 1 | 2))
        log.append(("istream::read", n, got))
        return t

    def ios_rdbuf_set(u):                               # rdbuf(streambuf *): swap, clear() -> badbit iff null
        io, sb = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        old = q(io + 0x48)
        w8(io + 0x48, sb)
        uc.mem_write(io + 0x10, struct.pack("<I", 0 if sb else 4))
        return old

    def is_vbase_dtor(u):                               # ~basic_istream + ~basic_ios/~ios_base: the model locale is not heap
        t = u.reg_read(UC_X86_REG_RCX)
        if q(t) != VBT:
            raise Unsupported("istream not built by the bridge")
        return 0

    def sb_dtor(u):
        t = u.reg_read(UC_X86_REG_RCX)
        if q(t + 0x60) != LOC:
            raise Unsupported("streambuf not built by the bridge")
        w8(t, SB_VT)
        return 0

    MSVCP = {"??0?$basic_streambuf@DU?$char_traits@D@std@@@std@@IEAA@XZ": sb_ctor,
             "??0?$basic_istream@DU?$char_traits@D@std@@@std@@QEAA@PEAV?$basic_streambuf@DU?$char_traits@D@std@@@1@_N@Z": is_ctor,
             "?read@?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAAEAV12@PEAD_J@Z": is_read,
             "?rdbuf@?$basic_ios@DU?$char_traits@D@std@@@std@@QEAAPEAV?$basic_streambuf@DU?$char_traits@D@std@@@2@PEAV32@@Z": ios_rdbuf_set,
             "??_D?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAXXZ": is_vbase_dtor,
             "??1?$basic_streambuf@DU?$char_traits@D@std@@@std@@UEAA@XZ": sb_dtor}
    missing = [k for k in MSVCP if k not in IAT]
    if missing:
        raise RuntimeError("msvcp140 names not imported: %s" % missing)

    FN = {f.__name__: f for f in (strtok_s, strlen, strcmp, strncmp, _stricmp, strcpy_s, strncpy_s, strcat_s, atoi, strrchr, strstr, memcmp,
                                  __stdio_common_vsscanf)}
    FN.update(MSVCP)
    for nm, f in FN.items():
        if nm not in IAT:
            continue
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)

        def hook(u, a, n, _, f=f, nm=nm):
            try:
                r = f(u)
            except Unsupported as e:
                log.append(("UNSUPPORTED", nm, str(e)))
                u.emu_stop()
                return
            u.reg_write(UC_X86_REG_RAX, r)
            if nm == "strtok_s":
                log.append((nm, cstr(u, r, 80) if r else None))
            elif nm == "__stdio_common_vsscanf":
                log.append((nm, cstr(u, u.reg_read(UC_X86_REG_R9), 20), r))
            else:
                log.append(nm)
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
    return IAT
