"""msvcp140 std::basic_ios / basic_istream / basic_iostream <char> members for the boot world (OPUS, 2026-09-26), standard
semantics over the MSVC x64 layout, FAIL-CLOSED. Installed after crt_bridge_boot (which keeps its streambuf ctor / dtor,
istream ctor, read, rdbuf, vbase dtor).

Layouts (as msvcp_wide.py / crt_bridge.py): streambuf {+0 vfptr, +8 _Gfirst, +0x10 _Pfirst, +0x18 _IGfirst, +0x20 _IPfirst,
+0x28 _Gnext, +0x30 _Pnext, +0x38 _IGnext, +0x40 _IPnext, +0x48 _Gcount, +0x4C _Pcount, +0x50 _IGcount, +0x58 _IPcount,
+0x60 _Plocale}: eback = *_IGfirst, gptr = *_IGnext, egptr = gptr + *_IGcount, pptr = *_IPnext. ios_base {+0 vfptr, +8 _Stdstr,
+0x10 _Mystate, +0x14 _Except, +0x18 _Fmtfl, +0x20 _Prec, +0x28 _Wide, +0x30 _Arr, +0x38 _Calls, +0x40 _Ploc}; basic_ios {+0x48
_Mystrbuf, +0x50 _Tiestr, +0x58 _Fillch}. istream {+0 vbptr, +8 _Chcount}; iostream = istream + ostream vbptr at +0x10.

The stream buffer is the GAME's basic_stringbuf (its vtable and _Init are image code). Where the library would call one of
its virtuals, the model asks the boot driver to run the GAME's function (a guest call on a side stack) and finishes with its
result: underflow (vtable slot 6) when the get area is empty (get / peek / skipws), pbackfail (slot 4) when the inline
putback path cannot apply, overflow (slot 3) when sputc finds no room in the put area.
Formatted extraction (>> int, >> double) uses the C locale: isspace skipping when skipws, then the num_get grammar for decimal
(the stream's basefield must be dec or unset, else REFUSES) and for floating point; overflow and no-digit set failbit, reaching
the end sets eofbit. Exception masks: a state change that intersects _Except REFUSES."""
import re
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

GOOD, EOF_, FAIL, BAD = 0, 1, 2, 4


class Refuse(Exception):
    pass


class NeedGuest(Exception):
    """A model needs one call into game code: fn(args...) is run by the boot driver on a side stack; then(result) finishes
    the import and returns its rax. then() may not request a second guest call."""
    def __init__(self, fn, args, then):
        Exception.__init__(self, "guest %X" % fn)
        self.fn, self.args, self.then = fn, args, then


GUESTQ = []


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
    i4 = lambda a: struct.unpack("<i", bytes(uc.mem_read(a, 4)))[0]
    w8 = lambda a, v: uc.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))
    IAT_THUNK_SYNC = 0x8088C4
    BR_LOCKS = ()
    MP = 0x7BE00000
    uc.mem_map(MP, 0x1000, 1)
    IOS_VT, LOC = MP + 0x100, MP + 0x200

    def ios_of(this):                              # the virtual base basic_ios through the vbptr at +0 (vbtable entry +4)
        return this + i4(q(this) + 4)

    def state(io):
        return d4(io + 0x10)

    def setstate(io, add):
        st = state(io) | add
        if not q(io + 0x48):
            st |= BAD
        uc.mem_write(io + 0x10, struct.pack("<I", st))
        if st & d4(io + 0x14):
            raise Refuse("exception mask %X intersects state %X" % (d4(io + 0x14), st))

    def gptrs(sb):
        gnext_p, gcount_p = q(sb + 0x38), q(sb + 0x50)
        g = q(gnext_p) if gnext_p else 0
        n = i4(gcount_p) if gcount_p else 0
        eb = q(q(sb + 0x18)) if q(sb + 0x18) else 0
        return eb, g, g + n if g else 0, gnext_p, gcount_p

    def pptr(sb):
        p = q(sb + 0x40)
        return q(p) if p else 0

    def vslot(sb, k):
        return q(q(sb) + 8 * k)

    def need_underflow(sb, then):                   # the game's underflow (slot 6); then(c or None)
        raise NeedGuest(vslot(sb, 6), (sb,), lambda r: then(None if (r & 0xFFFFFFFF) == 0xFFFFFFFF else r & 0xFF))

    def bump_avail(sb):                             # the inline sbumpc: the char, or None when the get area is empty
        eb, g, eg, gp, cp = gptrs(sb)
        if g and g < eg:
            c = uc.mem_read(g, 1)[0]
            w8(gp, g + 1)
            uc.mem_write(cp, struct.pack("<i", i4(cp) - 1))
            return c
        return None

    def peek_avail(sb):
        eb, g, eg, gp, cp = gptrs(sb)
        if g and g < eg:
            return uc.mem_read(g, 1)[0]
        return None

    def bump(sb):                                   # for the formatted extractors: the get area only (no guest call)
        c = bump_avail(sb)
        if c is None and peek_avail(sb) is None:
            pp = pptr(sb)
            if pp and pp > gptrs(sb)[2]:
                raise Refuse("formatted extraction reached egptr with a put area beyond it")
        return c

    def peekc(sb):
        c = peek_avail(sb)
        if c is None:
            pp = pptr(sb)
            if pp and pp > gptrs(sb)[2]:
                raise Refuse("formatted extraction reached egptr with a put area beyond it")
        return c

    def ipfx(io, noskip):                           # the sentry: good state, tie not modelled (must be null), skipws
        if state(io) != GOOD:
            setstate(io, FAIL)
            return False
        if q(io + 0x50):
            raise Refuse("a tied stream would be flushed")
        if not noskip and d4(io + 0x18) & 0x1:      # skipws
            sb = q(io + 0x48)
            while True:
                c = peekc(sb)
                if c is None:
                    setstate(io, EOF_ | FAIL)
                    return False
                if c not in b" \t\n\v\f\r":
                    break
                bump(sb)
        return True

    def ios_ctor(u):                                # basic_ios() (protected): the virtual base, initialised later by init()
        io = u.reg_read(UC_X86_REG_RCX)
        w8(io, IOS_VT)
        return io

    def noop(u):
        return 0

    def iostream_ctor(u):                           # basic_iostream(streambuf *) + the most-derived flag in r8
        t, sb, md = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
        if md:
            raise Refuse("iostream built as the most-derived object (the caller sets no vbptrs)")
        if not q(t) or not q(t + 0x10):
            raise Refuse("iostream vbptrs not set by the caller")
        io = ios_of(t)
        w8(t + 8, 0)                                 # _Chcount
        w8(io + 8, 0)
        uc.mem_write(io + 0x10, struct.pack("<iii", 0 if sb else BAD, 0, 0x201))
        w8(io + 0x20, 6); w8(io + 0x28, 0); w8(io + 0x30, 0); w8(io + 0x38, 0); w8(io + 0x40, LOC)
        w8(io + 0x48, sb); w8(io + 0x50, 0)
        uc.mem_write(io + 0x58, b" ")
        return t

    def get_char(u):                                # get(char &): sbumpc, through the game's underflow when empty
        t, pc = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        io = ios_of(t)
        w8(t + 8, 0)
        if ipfx(io, True):
            sb = q(io + 0x48)

            def fin(c):
                if c is None:
                    setstate(io, EOF_ | FAIL)
                else:
                    uc.mem_write(pc, bytes([c]))
                    w8(t + 8, 1)
                return t
            c = bump_avail(sb)
            if c is None:                           # uflow = underflow, then take the char it exposed
                need_underflow(sb, lambda c2: fin(None if c2 is None else bump_avail(sb)))
            return fin(c)
        return t

    def peek(u):
        t = u.reg_read(UC_X86_REG_RCX)
        io = ios_of(t)
        w8(t + 8, 0)
        if ipfx(io, True):
            sb = q(io + 0x48)

            def fin(c):
                if c is None:
                    setstate(io, EOF_)
                    return 0xFFFFFFFF
                return c
            c = peek_avail(sb)
            if c is None:
                need_underflow(sb, fin)
            return fin(c)
        return 0xFFFFFFFF

    def putback(u):                                 # putback(char): clears eofbit, then sputbackc
        t, ch = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF
        io = ios_of(t)
        w8(t + 8, 0)
        uc.mem_write(io + 0x10, struct.pack("<I", state(io) & ~EOF_))
        if ipfx(io, True):
            sb = q(io + 0x48)
            eb, g, eg, gp, cp = gptrs(sb)
            if g and g > eb and uc.mem_read(g - 1, 1)[0] == ch:
                w8(gp, g - 1)
                uc.mem_write(cp, struct.pack("<i", i4(cp) + 1))
            else:                                   # the game's pbackfail (slot 4)
                def fin(r):
                    if (r & 0xFFFFFFFF) == 0xFFFFFFFF:
                        setstate(io, BAD)
                    return t
                raise NeedGuest(vslot(sb, 4), (sb, ch), fin)
        return t

    def scan(io, sb, ok, skipws, finish):
        """The formatted-extraction scan: skip white space (if skipws), then take the longest run accepted by ok(prefix + c).
        When the get area is empty the game's underflow is asked (a guest call) and the scan continues in its then();
        finish(token, reached_end) returns the import's rax."""
        st = {"tok": b"", "skipping": skipws}

        def step():
            while True:
                c = peek_avail(sb)
                if c is None:
                    raise NeedGuest(vslot(sb, 6), (sb,), after_underflow)
                if st["skipping"]:
                    if c in b" \t\n\v\f\r":
                        bump_avail(sb)
                        continue
                    st["skipping"] = False
                if not ok(st["tok"] + bytes([c])):
                    return finish(st["tok"], False)
                st["tok"] += bytes([c])
                bump_avail(sb)

        def after_underflow(r):
            if (r & 0xFFFFFFFF) == 0xFFFFFFFF:
                return finish(st["tok"], True)
            return step()
        return step()

    INT_RE = re.compile(rb"[+-]?[0-9]*\Z")
    FLT_RE = re.compile(rb"[+-]?([0-9]*(\.[0-9]*)?([eE]([+-][0-9]*|[0-9]*)?)?)\Z")

    def fsentry(io):                                # the formatted sentry, without the skip (scan does it)
        if state(io) != GOOD:
            setstate(io, FAIL)
            return False
        if q(io + 0x50):
            raise Refuse("a tied stream would be flushed")
        return True

    def extract_int(u):                             # operator>>(int &)
        t, p = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        io = ios_of(t)
        if d4(io + 0x18) & 0xE00 not in (0, 0x200):
            raise Refuse("basefield other than dec")
        if not fsentry(io):
            return t

        def finish(tok, end):
            st = EOF_ if end else 0
            if not re.search(rb"[0-9]", tok):
                st |= FAIL
                if end and not tok:
                    st |= FAIL
            else:
                v = int(tok)
                if not -2 ** 31 <= v < 2 ** 31:
                    st |= FAIL
                    v = 2 ** 31 - 1 if v > 0 else -2 ** 31
                uc.mem_write(p, struct.pack("<i", v))
            if st:
                setstate(io, st)
            return t
        return scan(io, q(io + 0x48), lambda s_: bool(INT_RE.match(s_)), bool(d4(io + 0x18) & 1), finish)

    def extract_double(u):                          # operator>>(double &)
        t, p = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        io = ios_of(t)
        if not fsentry(io):
            return t

        def finish(tok, end):
            st = EOF_ if end else 0
            m = re.match(rb"[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?", tok)
            if not m or m.end() != len(tok):
                st |= FAIL
                uc.mem_write(p, struct.pack("<d", 0.0))
            else:
                uc.mem_write(p, struct.pack("<d", float(tok)))
            if st:
                setstate(io, st)
            return t
        return scan(io, q(io + 0x48), lambda s_: bool(FLT_RE.match(s_)), bool(d4(io + 0x18) & 1), finish)

    def clear(u):                                   # basic_ios::clear(state, reraise)
        io, st = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0x17
        if not q(io + 0x48):
            st |= BAD
        uc.mem_write(io + 0x10, struct.pack("<I", st))
        if st & d4(io + 0x14):
            raise Refuse("exception mask set")
        return 0

    def sputc(u):                                   # streambuf::sputc(char): the put area, or the game's overflow (slot 3)
        sb, ch = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF
        np, cp = q(sb + 0x40), q(sb + 0x58)
        if np and cp and i4(cp) > 0:
            p_ = q(np)
            uc.mem_write(p_, bytes([ch]))
            w8(np, p_ + 1)
            uc.mem_write(cp, struct.pack("<i", i4(cp) - 1))
            return ch
        raise NeedGuest(vslot(sb, 3), (sb, ch), lambda r: r & 0xFFFFFFFF)

    def setstate_(u):                               # basic_ios::setstate(state, reraise)
        io, st = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0x17
        setstate(io, st)
        return 0

    def osfx(u):                                    # ostream::_Osfx: flush only under unitbuf
        t = u.reg_read(UC_X86_REG_RCX)
        io = ios_of(t)
        if state(io) == GOOD and d4(io + 0x18) & 0x2:
            raise Refuse("unitbuf flush")
        return 0

    def flush(u):                                   # ostream::flush: pubsync through the buffer's sync (slot 13)
        t = u.reg_read(UC_X86_REG_RCX)
        io = ios_of(t)
        sb = q(io + 0x48)
        if sb:
            if vslot(sb, 13) != IAT_THUNK_SYNC:
                raise Refuse("a buffer with its own sync")
        return t                                     # the base sync returns 0

    M = {"??0?$basic_ios@DU?$char_traits@D@std@@@std@@IEAA@XZ": ios_ctor,
         "?_Lock@?$basic_streambuf@DU?$char_traits@D@std@@@std@@UEAAXXZ": noop,
         "?_Unlock@?$basic_streambuf@DU?$char_traits@D@std@@@std@@UEAAXXZ": noop,
         "?sputc@?$basic_streambuf@DU?$char_traits@D@std@@@std@@QEAAHD@Z": sputc,
         "?setstate@?$basic_ios@DU?$char_traits@D@std@@@std@@QEAAXH_N@Z": setstate_,
         "?uncaught_exception@std@@YA_NXZ": lambda u: 0,
         "?_Osfx@?$basic_ostream@DU?$char_traits@D@std@@@std@@QEAAXXZ": osfx,
         "?flush@?$basic_ostream@DU?$char_traits@D@std@@@std@@QEAAAEAV12@XZ": flush,
         "??1?$basic_ios@DU?$char_traits@D@std@@@std@@UEAA@XZ": noop,
         "??1?$basic_iostream@DU?$char_traits@D@std@@@std@@UEAA@XZ": noop,
         "??1?$basic_istream@DU?$char_traits@D@std@@@std@@UEAA@XZ": noop,
         "??0?$basic_iostream@DU?$char_traits@D@std@@@std@@QEAA@PEAV?$basic_streambuf@DU?$char_traits@D@std@@@1@@Z": iostream_ctor,
         "?get@?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAAEAV12@AEAD@Z": get_char,
         "?peek@?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAHXZ": peek,
         "?putback@?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAAEAV12@D@Z": putback,
         "??5?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAAEAV01@AEAH@Z": extract_int,
         "??5?$basic_istream@DU?$char_traits@D@std@@@std@@QEAAAEAV01@AEAN@Z": extract_double,
         "?clear@?$basic_ios@DU?$char_traits@D@std@@@std@@QEAAXH_N@Z": clear}
    for nm, f in M.items():
        if nm not in IAT:
            raise RuntimeError("not imported: " + nm)
        if nm in BR_LOCKS and nm not in IAT:
            pass
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)

        def hook(u, a, n, _, f=f, nm=nm):
            try:
                r = f(u)
            except Refuse as e:
                log.append(("UNSUPPORTED", nm[:40], str(e)))
                u.emu_stop()
                return
            except NeedGuest as g:
                g.name = nm
                GUESTQ.append(g)
                u.emu_stop()
                return
            u.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
