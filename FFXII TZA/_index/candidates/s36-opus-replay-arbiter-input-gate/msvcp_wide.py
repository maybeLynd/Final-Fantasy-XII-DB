"""msvcp140's std::basic_ios / basic_istream / basic_streambuf <wchar_t> members, standard semantics over the MSVC x64 layout,
FAIL-CLOSED: members that only run on an open file (getline, seekg, tellg) refuse and stop the run.
Layouts as in crt_bridge.py's narrow bridge: streambuf {+0 vfptr, +8 _Gfirst, +0x10 _Pfirst, +0x18 _IGfirst, +0x20 _IPfirst,
+0x28 _Gnext, +0x30 _Pnext, +0x38 _IGnext, +0x40 _IPnext, +0x48 _Gcount, +0x4C _Pcount, +0x50 _IGcount, +0x58 _IPcount,
+0x60 _Plocale}; ios_base {+0 vfptr, +8 _Stdstr, +0x10 _Mystate, +0x14 _Except, +0x18 _Fmtfl, +0x20 _Prec, +0x28 _Wide,
+0x30 _Arr, +0x38 _Calls, +0x40 _Ploc} then basic_ios {+0x48 _Mystrbuf, +0x50 _Tiestr, +0x58 _Fillch (wchar_t)};
istream {+0 vbptr, +8 _Chcount, +0x10 basic_ios}. The DLL's own vtables and locale live on a non-executable page."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9


class Unsupported(Exception):
    pass


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
    MP = 0x7B900000
    uc.mem_map(MP, 0x10000, 1)
    uc.mem_write(MP, bytes(0x10000))
    SB_VT, IOS_VT, VBT, LOC = MP + 0x100, MP + 0x200, MP + 0x300, MP + 0x400
    uc.mem_write(VBT, struct.pack("<ii", 0, 0x10))

    def w8(a, v):
        uc.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))

    def sb_init(t):
        for off in (8, 0x10, 0x28, 0x30):
            w8(t + off, 0)
        uc.mem_write(t + 0x48, struct.pack("<ii", 0, 0))
        for p, f in ((0x18, 8), (0x20, 0x10), (0x38, 0x28), (0x40, 0x30), (0x50, 0x48), (0x58, 0x4C)):
            w8(t + p, t + f)

    def sb_ctor(u):                                # basic_streambuf(): _Plocale = new locale, _Init()
        t = u.reg_read(UC_X86_REG_RCX)
        w8(t, SB_VT)
        sb_init(t)
        w8(t + 0x60, LOC)
        return t

    def sb_Init(u):                                # _Init(): the six pointer members point at the internal fields, all zero
        sb_init(u.reg_read(UC_X86_REG_RCX))
        return 0

    def sb_dtor(u):
        t = u.reg_read(UC_X86_REG_RCX)
        if q(t + 0x60) != LOC:
            raise Unsupported("streambuf not built by the bridge")
        w8(t, SB_VT)
        return 0

    def ios_ctor(u):                               # basic_ios() (protected): the virtual base, initialised later by init()
        io = u.reg_read(UC_X86_REG_RCX)
        w8(io, IOS_VT)
        return io

    def ios_dtor(u):
        return 0

    def is_ctor(u):                                # basic_istream(streambuf *, bool isstd) with the most-derived flag
        t, sb, isstd, md = (u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        io = t + 0x10
        if md & 0xFFFFFFFF:
            w8(t, VBT)
        elif q(t) == 0:
            raise Unsupported("istream as a base subobject with no vbptr")
        io = t + struct.unpack("<i", bytes(uc.mem_read(q(t) + 4, 4)))[0]
        w8(t + 8, 0)
        w8(io, IOS_VT)
        w8(io + 8, 0)
        uc.mem_write(io + 0x10, struct.pack("<iii", 0 if sb else 4, 0, 0x201))
        w8(io + 0x20, 6); w8(io + 0x28, 0); w8(io + 0x30, 0); w8(io + 0x38, 0); w8(io + 0x40, LOC)
        w8(io + 0x48, sb); w8(io + 0x50, 0)
        uc.mem_write(io + 0x58, struct.pack("<H", 0x20))
        return t

    def is_dtor(u):
        return 0

    def ios_clear(u):                              # clear(state, reraise): state |= badbit when no buffer; no exceptions set
        io, st = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0x17
        if not q(io + 0x48):
            st |= 4
        uc.mem_write(io + 0x10, struct.pack("<I", st))
        if st & d4(io + 0x14):
            raise Unsupported("an exception mask is set")
        return 0

    def ios_setstate(u):                           # setstate(state, reraise) = clear(rdstate() | state)
        io, st = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0x17
        st |= d4(io + 0x10)
        if not q(io + 0x48):
            st |= 4
        uc.mem_write(io + 0x10, struct.pack("<I", st))
        if st & d4(io + 0x14):
            raise Unsupported("an exception mask is set")
        return 0

    def fiopen(u):                                 # std::_Fiopen(const wchar_t *, openmode, prot): the file is absent -> nullptr
        a = u.reg_read(UC_X86_REG_RCX)
        b = bytes(u.mem_read(a, 520))
        name = b.decode("utf-16-le", "replace").split("\0")[0]
        log.append(("_Fiopen", name, "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)))
        return 0

    def refuse(nm):
        def f(u):
            raise Unsupported(nm + " runs only on an open file; not modelled")
        return f

    M = {"??0?$basic_streambuf@_WU?$char_traits@_W@std@@@std@@IEAA@XZ": sb_ctor,
         "?_Init@?$basic_streambuf@_WU?$char_traits@_W@std@@@std@@IEAAXXZ": sb_Init,
         "??1?$basic_streambuf@_WU?$char_traits@_W@std@@@std@@UEAA@XZ": sb_dtor,
         "??0?$basic_ios@_WU?$char_traits@_W@std@@@std@@IEAA@XZ": ios_ctor,
         "??1?$basic_ios@_WU?$char_traits@_W@std@@@std@@UEAA@XZ": ios_dtor,
         "??1?$basic_istream@_WU?$char_traits@_W@std@@@std@@UEAA@XZ": is_dtor,
         "?clear@?$basic_ios@_WU?$char_traits@_W@std@@@std@@QEAAXH_N@Z": ios_clear,
         "?setstate@?$basic_ios@_WU?$char_traits@_W@std@@@std@@QEAAXH_N@Z": ios_setstate,
         "?getline@?$basic_istream@_WU?$char_traits@_W@std@@@std@@QEAAAEAV12@PEA_W_J@Z": refuse("getline"),
         "?seekg@?$basic_istream@_WU?$char_traits@_W@std@@@std@@QEAAAEAV12@_JH@Z": refuse("seekg"),
         "?_Fiopen@std@@YAPEAU_iobuf@@PEB_WHH@Z": fiopen,
         "?tellg@?$basic_istream@_WU?$char_traits@_W@std@@@std@@QEAA?AV?$fpos@U_Mbstatet@@@2@XZ": refuse("tellg")}
    for k in IAT:
        if k.startswith("??0?$basic_istream@_WU?$char_traits@_W@std@@@std@@QEAA@PEAV?$basic_streambuf"):
            M[k] = is_ctor
    for nm, f in M.items():
        if nm not in IAT:
            raise RuntimeError("not imported: " + nm)
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)

        def hook(u, a, n, _, f=f, nm=nm):
            try:
                r = f(u)
            except Unsupported as e:
                log.append(("UNSUPPORTED", nm[:40], str(e)))
                u.emu_stop()
                return
            u.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            log.append(nm.split("@")[0][:30])
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
