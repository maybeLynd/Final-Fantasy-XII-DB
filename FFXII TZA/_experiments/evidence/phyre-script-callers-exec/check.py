# EXP-110 phyre-script-callers-exec
#
# Executes the SHIPPED bytes of the three Phyre script-execution callers
# of the lua chunk loader named in CONTRACT-lua-chunk-loader under
# Unicorn, plus the nine leaf VM-stack primitives that carry observable
# contract semantics.
#
#   00684D10  D10  (obj, state). env = q[obj+8]; buf = q[env+0x50];
#             payload = q[env+0x60] - (b[env+0x60]&1); 0 -> ret 0.
#             Pool q[0x2E41050]: if d[+0x58] < (d[+0x48]&~bit31):
#             idx=cursor++; elem=q[+0x50]+idx*0x28; CPY86(elem+8 dst,
#             elem+0x18 src, elem+0x10&~bit31 n); state = q[elem+0x20].
#             LOAD(state,buf); fail -> ret 0 (esi=0).
#             pcall(state,0,0,0); err -> errstr+LOG(d6feb0)+settop(-2)
#             -> ret 0. r13 = gettop(argstate); r15 = gettop(state);
#             PUSHLS(state,payload); type(-1)==0 -> ret 0.
#             state==argstate: IDXOP(state,i) for i=1..r13;
#             else COPY(argstate,state,1,r13). pcall(state,r13,1,0);
#             errstr fetched unconditionally; err -> LOG+settop -> ret 0.
#             state!=argstate: COPY(state,argstate,r15+1,1).
#             esi = gettop(argstate) - r13. Exit pops pool cursor iff
#             checked-out elem is still the last. ret esi.
#
#   00684F60  F60  (obj, state, idx). env = q[obj+8]; 0 -> ret 7;
#             state 0 -> ret 1. esi=9; LOAD(state, env); fail -> ret
#             esi(=9 under arg-preserving stub). PUSHP(state,env);
#             SETFLD(state,0xD701A0). esi=0; pcall(state,0,0,0);
#             err -> errstr + LOG(3,d6ffd8,err,packed q[env+0x48]) +
#             settop(-2) -> ret 0. d[obj+0x20]<0 -> LOG(3,d70010,
#             packed q[env+0x48]) -> ret 0. Else strtab = q[env+0x28];
#             packed = q[strtab+idx*8] - low bit; PUSHLS(state,packed);
#             MARSH(state,q[obj+0x10],q[obj+0x18]); pcall(state,1,0,0);
#             errstr fetched unconditionally; err -> LOG+settop -> ret 0;
#             errstr!=0 -> LOG(2,d6e970,errstr). ret 0 always on success.
#
#   00686280  C280 (obj, arg2, rtag, vario). r14=vario; 0 -> ret 0.
#             head = q[vario]; 0 -> ret 0. env=q[obj+8]; buf=q[env+0x50];
#             payload=q[env+0x60]-lowbit; 0 -> ret 0. TWO pools tried in
#             order (q[0x2E41020], q[0x2E41050]): same checkout protocol;
#             state = q[elem+0x20]; first non-null state wins (a
#             checked-out elem with null state stays checked out).
#             no state -> ret 0. LOAD(state,buf); fail -> ret 0.
#             pcall(state,0,0,0); err -> errstr+LOG+settop -> ret 0.
#             PUSHLS(state,payload); type(-1)==0 -> ret 0.
#             ITER(state,&it) seeds payload cursor. Marshal loop over
#             NULL-terminated tag array at head: per tag, cursor += 8,
#             payload = [cursor-8] sized by type; GROW(state,1) then
#             PUSHB/PUSHI/PUSHN; default tag -> DISP(tag,&cursor,state),
#             fail -> LOG(d6fee0). pcall(state,nargs+1,1,0); err ->
#             errstr+LOG+settop -> ret 0. Result tag dispatch on arg3:
#             SENT0 -> TOBOOL -> b[r14+8]; SENT1/2 -> TONUM -> b;
#             SENT3/4 -> TONUM -> w/d; SENT5/6 -> TONUM -> d;
#             SENT7/8 -> TONUM -> q; else GETA(tag,state,r14) then
#             GETB then (tag == SING|1 -> MSHL -> q[r14+8]) else
#             LOG(d6ff20). Each numeric arm pops via settop(-2).
#             Success ret 1; pool pop iff last. ret 0 on all failures.
#
# Real callees (leaf stack primitives, TValue = 0x10-byte {q val,d type}):
#   0080FD00 gettop = (q[S+0x10]-q[q[S+0x20]])/0x10-1
#   00811130 settop: edx>=0 -> target=frame+(edx+1)*0x10, nil-fill,
#             top=target(clamped); edx<0 -> top += (edx+1)*0x10
#   00810450 pushbool {v!=0, d8=1}; 00810580 pushint cvtsi2ss {f,d8=3};
#   00810640 pushnum {xmm1,d8=3}; 008105A0 pushptr {q,d8=2}
#   008113D0 tobool(idx): resolve, truthy = type!=0 && (type!=1||val!=0)
#   008119F0 type(idx): d[elem+8]&0xF, -1 on nil sentinel
#   006372A0 singleton: lea rax,[rip] (const ptr from shipped .data)
#
# Scripted boundaries: 00683C30 LOAD (arg capture + planted al),
#   00861EBA CPY86 (real memcpy semantics), 00810340 PCALL (planted ret
#   seq + declared stack effect), 00811530 ERRSTR, 005CDAA0 LOG,
#   0080FB20 PUSHLS (declared {q=ptr,d8=4} push), 00810730 IDXOP
#   (declared nil push), 00810ED0 SETFLD (declared pop), 00682AA0 COPY,
#   00682D20 MARSH, 006811B0 ITER (seeds cursor), 00681010 DISP,
#   0080F420 GROW, 006810B0/00681130 GETA/GETB (variant writers),
#   00811470 TONUM, 00636920 MSHL, 12 TLS sentinels (planted tokens).
#
import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP, \
    UC_X86_REG_RSP, UC_X86_REG_RSI, UC_X86_REG_XMM1

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

D10  = 0x00684D10
F60  = 0x00684F60
C280 = 0x00686280

# real leaves
GETTOP = 0x0080FD00
SETTOP = 0x00811130
PUSHB  = 0x00810450
PUSHI  = 0x00810580
PUSHN  = 0x00810640
PUSHP  = 0x008105A0
TOBOOL = 0x008113D0
TYPE   = 0x008119F0
SING   = 0x006372A0

# scripted
LOAD   = 0x00683C30
CPY86  = 0x00861EBA
PCALL  = 0x00810340
ERRSTR = 0x00811530
LOG    = 0x005CDAA0
PUSHLS = 0x0080FB20
IDXOP  = 0x00810730
SETFLD = 0x00810ED0
COPY   = 0x00682AA0
MARSH  = 0x00682D20
ITER   = 0x006811B0
DISP   = 0x00681010
GROW   = 0x0080F420
GETA   = 0x006810B0
GETB   = 0x00681130
TONUM  = 0x00811470
MSHL   = 0x00636920

SENTS = [0x00630490, 0x0062FF50, 0x0062FFC0, 0x00630030, 0x006300A0,
         0x00630110, 0x00630180, 0x00630420, 0x006303B0, 0x006301F0,
         0x00630260, 0x006302D0]

G_P1 = 0x02E41020
G_P2 = 0x02E41050

# fixture layout
OBJ    = HEAP + 0x000000        # rcx object
ENV    = HEAP + 0x010000        # q[obj+8]
STATE  = HEAP + 0x020000        # lua state arg
FRAME  = HEAP + 0x028000        # frame descriptor (q[0] = frame base)
STK    = HEAP + 0x030000        # TValue stack
ESTATE = HEAP + 0x040000        # pool-elem lua state
EFRAME = HEAP + 0x048000
ESTK   = HEAP + 0x050000
HDR1   = HEAP + 0x060000
HDR2   = HEAP + 0x064000
ELEM1  = HEAP + 0x068000
ELEM2  = HEAP + 0x06C000
EDST   = HEAP + 0x070000        # elem copy dst
ESRC   = HEAP + 0x078000        # elem copy src
EDST2  = HEAP + 0x080000
ESRC2  = HEAP + 0x088000
BUF    = HEAP + 0x090000        # script buffer (q[env+0x50])
PAY    = HEAP + 0x098000        # packed payload (q[env+0x60])
STRTAB = HEAP + 0x0A0000        # env string table q[env+0x28]
NAME1  = HEAP + 0x0A8000        # obj marshal args q[+0x10]/q[+0x18]
NAME2  = HEAP + 0x0A9000
ESTR   = HEAP + 0x0B0000        # errstr
TAGS   = HEAP + 0x0C0000        # vararg tag array (NULL-term)
PAYARR = HEAP + 0x0C8000        # vararg payload array
CURH   = HEAP + 0x0D0000        # cursor holder cell -> points at CUR
CUR    = HEAP + 0x0D1000        # cursor qword (walks PAYARR)
VARIO  = HEAP + 0x0E0000        # in/out variant
SENTB  = 0xB0000000             # sentinel token base (+i*0x10)
SING_TOK = 0x02CF8270           # 006372A0 lea target (shipped const)


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)


def _init_state(gm, state, frame, stk, depth, framebase=0):
    """plant a lua-ish state: q[+0x10]=top, q[+0x18]=glb, q[+0x20]=frame
    ptr whose q[0] = frame base. depth = elems already on stack."""
    fb = stk + framebase * 0x10
    gm.w(state + 0x10, qw(stk + (framebase + depth) * 0x10))
    gm.w(state + 0x18, qw(stk + 0x8000))
    gm.w(state + 0x20, qw(frame))
    gm.w(state + 0x30, qw(stk + 0x4000))     # stack limit (GROW reads)
    gm.w(state + 0x38, qw(stk))
    gm.w(frame, qw(fb))
    return fb


def _push_tv(gm, state, qv, ty):
    top = struct.unpack("<Q", gm.r(state + 0x10, 8))[0]
    gm.w(top, qw(qv))
    gm.w(top + 8, dw(ty))
    gm.w(state + 0x10, qw(top + 0x10))


def _pop_tv(gm, state, n=1):
    top = struct.unpack("<Q", gm.r(state + 0x10, 8))[0]
    gm.w(state + 0x10, qw(top - 0x10 * n))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)

        # caller object + env
        env = case.get("env", ENV)
        gm.w(OBJ + 8, qw(env))
        gm.w(OBJ + 0x10, qw(case.get("o10", NAME1)))
        gm.w(OBJ + 0x18, qw(case.get("o18", NAME2)))
        gm.w(OBJ + 0x20, dw(case.get("o20", 0)))
        if env:
            gm.w(env + 0x28, qw(case.get("strtab", STRTAB)))
            gm.w(env + 0x48, qw(case.get("e48", ESTR + 0x400)))
            gm.w(env + 0x50, qw(case.get("buf", BUF)))
            gm.w(env + 0x60, qw(case.get("pay", PAY)))
            st = case.get("strtab", STRTAB)
            for i, v in enumerate(case.get("tab", [ESTR + 0x800])):
                gm.w(st + i * 8, qw(v))

        # arg lua state + stack (depth elems planted)
        st = case.get("state", STATE)
        if st:
            fb = _init_state(gm, st, FRAME, STK,
                             case.get("depth", 0),
                             case.get("framebase", 0))
            for i, (qv, ty) in enumerate(case.get("stack", [])):
                gm.w(fb + i * 0x10, qw(qv))
                gm.w(fb + i * 0x10 + 8, dw(ty))

        # elem lua state (for pool checkouts)
        _init_state(gm, ESTATE, EFRAME, ESTK, case.get("edepth", 0))
        for i, (qv, ty) in enumerate(case.get("estack", [])):
            gm.w(ESTK + i * 0x10, qw(qv))
            gm.w(ESTK + i * 0x10 + 8, dw(ty))

        # pool headers + elems
        for g, hdr, el, dst, src, tag in (
                (G_P1, HDR1, ELEM1, EDST, ESRC, "p1"),
                (G_P2, HDR2, ELEM2, EDST2, ESRC2, "p2")):
            h = case.get(tag + "_hdr", hdr if case.get(tag, 1) else 0)
            gm.w(g, qw(h))
            if h:
                cap = case.get(tag + "_cap", 4)
                gm.w(h + 0x48, dw(cap))
                gm.w(h + 0x50, qw(case.get(tag + "_elems", el)))
                gm.w(h + 0x58, dw(case.get(tag + "_cur", 0)))
                e = case.get(tag + "_elems", el)
                nplant = min(cap & 0x7FFFFFFF, 8)
                for i in range(nplant):
                    gm.w(e + i * 0x28 + 8, qw(dst + i * 0x100))
                    gm.w(e + i * 0x28 + 0x10,
                         dw(case.get(tag + "_n", 0x20)))
                    gm.w(e + i * 0x28 + 0x18, qw(src + i * 0x100))
                    stv = case.get(tag + "_states", None)
                    gm.w(e + i * 0x28 + 0x20,
                         qw((stv[i] if stv and i < len(stv) else ESTATE)))
                    gm.w(src + i * 0x100,
                         bytes([(0xA0 + i) & 0xFF]) * 0x40)

        # vararg / out-variant (C280): q[vario] = tag-array head
        va = case.get("vario", VARIO)
        if va:
            gm.w(va, qw(case.get("tags_ptr", TAGS)))
            for i, t in enumerate(case.get("tags", [])):
                gm.w(TAGS + i * 8, qw(t))
            gm.w(TAGS + len(case.get("tags", [])) * 8, qw(0))
            gm.w(CURH, qw(PAYARR))
            for i, v in enumerate(case.get("payarr", [])):
                gm.w(PAYARR + i * 8, qw(v))
            gm.w(BUF, case.get("buf_bytes", b"CHUNK\x00"))
            gm.w(PAY, case.get("pay_bytes", b"PAYLD\x00"))
            gm.w(ESTR, case.get("estr_bytes", b"err-str\x00"))

        self.trace, self.faults, self.fired = [], [], set()
        self._stub_n = {}
        for va_, data in case.get("plants", []):
            gm.w(va_, data)
        for va_, data in case.get("patch_bytes", []):
            gm.w(va_, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (LOAD, PCALL, ERRSTR, LOG, PUSHLS, IDXOP, SETFLD,
                   COPY, MARSH, ITER, DISP, GROW, GETA, GETB, TONUM,
                   MSHL, CPY86):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in SENTS:
            uc.hook_add(UC_HOOK_CODE, self.on_sent, begin=va, end=va)
        for va in (GETTOP, SETTOP, PUSHB, PUSHI, PUSHN, PUSHP, TOBOOL,
                   TYPE):
            uc.hook_add(UC_HOOK_CODE, self.on_watch, begin=va, end=va)

    def _pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RIP, back)

    def _ret_seq(self, key, default=0):
        seq = self.case.get(key, default)
        if not isinstance(seq, (list, tuple)):
            seq = [seq]
        n = self._stub_n.get("%x" % 0, 0)
        return seq

    def on_watch(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        if addr == GETTOP:
            self.trace.append("T%x" % (rcx & 0xFFFFFFFF))
        elif addr == PUSHN:
            self.trace.append("n%x" % (rcx & 0xFFFFFFFF))
        elif addr in (SETTOP, TOBOOL, TYPE):
            tag = {SETTOP: "t", TOBOOL: "B", TYPE: "y"}[addr]
            self.trace.append("%s%x:%x" % (tag, rcx & 0xFFFFFFFF,
                                           s32(rdx)))
        else:
            tag = {PUSHB: "b", PUSHI: "i", PUSHP: "p"}[addr]
            self.trace.append("%s%x:%x" % (tag, rcx & 0xFFFFFFFF,
                                           rdx & 0xFFFFFFFF))

    def on_sent(self, uc, addr, size, _):
        i = SENTS.index(addr)
        self.trace.append("s%d" % i)
        uc.reg_write(UC_X86_REG_RAX, SENTB + i * 0x10)
        self._pop_ret()

    def _stack_args(self, uc):
        sp = uc.reg_read(UC_X86_REG_RSP)
        return struct.unpack("<II", self.gm.r(sp + 0x28, 8))

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        c = self.case
        gm = self.gm
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8 = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
        r9 = uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF
        key = "%x" % addr
        self._stub_n[key] = self._stub_n.get(key, 0) + 1
        if addr == LOAD:
            self.trace.append("L%x:%x" % (rcx & 0xFFFFFFFF,
                                          rdx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("load_ret", 1) & 0xFF)
            if "load_esi" in c:
                uc.reg_write(UC_X86_REG_RSI, c["load_esi"]
                             & 0xFFFFFFFFFFFFFFFF)
        elif addr == CPY86:
            n = r8 & 0x7FFFFFFF
            gm.w(rcx, gm.r(rdx, n))
            self.trace.append("c%x:%x:%x" % (rcx & 0xFFFFFFFF,
                                             rdx & 0xFFFFFFFF, n))
        elif addr == PCALL:
            a5, a6 = self._stack_args(uc)
            self.trace.append("P%x:%x:%x:%x" % (rcx & 0xFFFFFFFF,
                              s32(rdx), s32(r8), s32(r9)))
            seq = c.get("pcall_rets", [0])
            n = self._stub_n[key] - 1
            ret = seq[n] if n < len(seq) else seq[-1]
            uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFF)
            # declared effect: consume nargs, push nresults tagged TVs
            nargs = max(0, s32(rdx))
            nres = max(0, s32(r8))
            for _ in range(nargs):
                _pop_tv(gm, rcx)
            for i in range(nres):
                _push_tv(gm, rcx, c.get("res_q", ESTR + 0xC00) + i * 0x10,
                         c.get("res_ty", 1))
        elif addr == ERRSTR:
            self.trace.append("E%x:%x" % (rcx & 0xFFFFFFFF, s32(rdx)))
            uc.reg_write(UC_X86_REG_RAX, c.get("errstr", ESTR)
                         & 0xFFFFFFFFFFFFFFFF)
        elif addr == LOG:
            sp = uc.reg_read(UC_X86_REG_RSP)
            a5 = struct.unpack("<Q", gm.r(sp + 0x28, 8))[0]
            self.trace.append("G%x:%x:%x:%x:%x" % (
                rcx & 0xFFFFFFFF, rdx & 0xFFFFFFFF, r8 & 0xFFFFFFFF,
                r9 & 0xFFFFFFFFFFFFFFFF, a5 & 0xFFFFFFFFFFFFFFFF))
        elif addr == PUSHLS:
            self.trace.append("S%x:%x" % (rcx & 0xFFFFFFFF,
                                          rdx & 0xFFFFFFFFFFFFFFFF))
            _push_tv(gm, rcx, rdx, c.get("pushls_ty", 4))
            uc.reg_write(UC_X86_REG_RAX, rdx)
        elif addr == IDXOP:
            self.trace.append("x%x:%x" % (rcx & 0xFFFFFFFF, s32(rdx)))
            _push_tv(gm, rcx, 0, 0)
        elif addr == SETFLD:
            top = struct.unpack("<Q", gm.r(rcx + 0x10, 8))[0]
            ty = struct.unpack("<I", gm.r(top - 0x10 + 8, 4))[0]
            self.trace.append("f%x:%x:%x" % (rcx & 0xFFFFFFFF,
                              rdx & 0xFFFFFFFF, ty & 0xF))
            _pop_tv(gm, rcx)
        elif addr == COPY:
            self.trace.append("C%x:%x:%x:%x" % (rcx & 0xFFFFFFFF,
                              rdx & 0xFFFFFFFF, s32(r8), s32(r9)))
        elif addr == MARSH:
            self.trace.append("m%x:%x:%x" % (rcx & 0xFFFFFFFF,
                              rdx & 0xFFFFFFFFFFFFFFFF,
                              r8 & 0xFFFFFFFFFFFFFFFF))
        elif addr == ITER:
            self.trace.append("I%x" % (rcx & 0xFFFFFFFF))
            gm.w(rdx + 0x18, qw(CURH))
        elif addr == DISP:
            self.trace.append("D%x:%x:%x" % (rcx & 0xFFFFFFFFFFFFFFFF,
                              rdx & 0xFFFFFFFFFFFFFFFF,
                              r8 & 0xFFFFFFFFFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("disp_ret", 1) & 0xFF)
        elif addr == GROW:
            self.trace.append("g%x:%x" % (rcx & 0xFFFFFFFF, s32(rdx)))
        elif addr == GETA:
            self.trace.append("a%x:%x:%x" % (rcx & 0xFFFFFFFFFFFFFFFF,
                              rdx & 0xFFFFFFFFFFFFFFFF,
                              r8 & 0xFFFFFFFFFFFFFFFF))
            ok = c.get("geta_ret", 0)
            uc.reg_write(UC_X86_REG_RAX, ok & 0xFF)
            if ok:
                gm.w(r8, qw(c.get("geta_q", ESTR + 0xD00)))
                gm.w(r8 + 8, bytes([c.get("geta_b", 1) & 0xFF]))
        elif addr == GETB:
            self.trace.append("z%x:%x:%x" % (rcx & 0xFFFFFFFFFFFFFFFF,
                              rdx & 0xFFFFFFFFFFFFFFFF,
                              r8 & 0xFFFFFFFFFFFFFFFF))
            ok = c.get("getb_ret", 0)
            uc.reg_write(UC_X86_REG_RAX, ok & 0xFF)
            if ok:
                gm.w(r8, qw(c.get("getb_q", ESTR + 0xD40)))
                gm.w(r8 + 8, bytes([c.get("getb_b", 2) & 0xFF]))
        elif addr == TONUM:
            self.trace.append("N%x:%x" % (rcx & 0xFFFFFFFF, s32(rdx)))
            uc.reg_write(UC_X86_REG_RAX, c.get("tonum_ret", 0x1234)
                         & 0xFFFFFFFFFFFFFFFF)
        elif addr == MSHL:
            self.trace.append("h%x" % (rcx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("mshl_ret", ESTR + 0xD80)
                         & 0xFFFFFFFFFFFFFFFF)
        self._pop_ret()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


# ---- model -----------------------------------------------------------------

def _tv_img(qv=None, ty=None, d0=None):
    img = bytearray(0x10)
    if qv is not None:
        struct.pack_into("<Q", img, 0, qv & 0xFFFFFFFFFFFFFFFF)
    if d0 is not None:
        struct.pack_into("<I", img, 0, d0 & 0xFFFFFFFF)
    if ty is not None:
        struct.pack_into("<I", img, 8, ty & 0xFFFFFFFF)
    return img


class MState:
    """mirrors the fixture's lua-state stack + pool for expected obs.
    tv/etv entries are 16-byte TValue images."""
    def __init__(self, case):
        self.case = case
        self.top_d = case.get("depth", 0)
        self.etop_d = case.get("edepth", 0)
        self.tv = {i: _tv_img(qv, ty) for i, (qv, ty) in
                   enumerate(case.get("stack", []))}
        self.etv = {i: _tv_img(qv, ty) for i, (qv, ty) in
                    enumerate(case.get("estack", []))}
        self.cur1 = case.get("p1_cur", 0)
        self.cur2 = case.get("p2_cur", 0)

    def top(self, which="a"):
        return self.top_d if which == "a" else self.etop_d

    def gettop(self, which="a"):
        return (self.top_d if which == "a" else self.etop_d) - 1

    def _slot(self, which, i):
        tv = self.tv if which == "a" else self.etv
        if i not in tv:
            tv[i] = _tv_img()
        return tv[i]

    def _wslot(self, which, d0=None, q0=None, ty=None):
        """write fields into the slot AT top (stale bytes persist),
        then advance. Mirrors the leaf pushers' partial writes."""
        d = self.top_d if which == "a" else self.etop_d
        img = self._slot(which, d)
        if q0 is not None:
            struct.pack_into("<Q", img, 0, q0 & 0xFFFFFFFFFFFFFFFF)
        if d0 is not None:
            struct.pack_into("<I", img, 0, d0 & 0xFFFFFFFF)
        if ty is not None:
            struct.pack_into("<I", img, 8, ty & 0xFFFFFFFF)
        if which == "a":
            self.top_d = d + 1
        else:
            self.etop_d = d + 1

    def push(self, qv, ty, which="a"):
        """stub-style push: q0=qv, d8=ty."""
        self._wslot(which, q0=qv, ty=ty)

    def pushb(self, v, which="a"):
        self._wslot(which, d0=1 if v else 0, ty=1)

    def pushi(self, v, which="a"):
        v &= 0xFFFFFFFFFFFFFFFF
        if v & 0x8000000000000000:
            v -= 0x10000000000000000
        self._wslot(which, d0=struct.unpack("<I", struct.pack("<f",
                                  float(v)))[0], ty=3)

    def pushn(self, f64bits, which="a"):
        fv = struct.unpack("<d", struct.pack("<Q", f64bits
                                              & 0xFFFFFFFFFFFFFFFF))[0]
        self._wslot(which, d0=struct.unpack("<I", struct.pack("<f",
                                  fv))[0], ty=3)

    def pushp(self, ptr, which="a"):
        self._wslot(which, q0=ptr, ty=2)

    def pop(self, n=1, which="a"):
        """top moves down; slot bytes persist."""
        if which == "a":
            self.top_d -= n
        else:
            self.etop_d -= n

    def settop(self, edx, which="a"):
        """edx>=0: target=frame+edx+1, nil-fill(d8=0) slots [d,nd).
        edx<0: top += edx+1 (no clamp — can go below frame).
        Entries keep their bytes; only top moves."""
        tv = self.tv if which == "a" else self.etv
        d = self.top_d if which == "a" else self.etop_d
        if edx >= 0:
            nd = edx + 1
            for i in range(max(0, d), nd):
                struct.pack_into("<I", self._slot(which, i), 8, 0)
            nd2 = nd
        else:
            nd2 = d + edx + 1
        if which == "a":
            self.top_d = nd2
        else:
            self.etop_d = nd2

    def typeat(self, idx, which="a"):
        img = self.valat(idx, which)
        return struct.unpack_from("<I", img, 8)[0] & 0xF

    def valat(self, idx, which="a"):
        tv = self.tv if which == "a" else self.etv
        d = self.top_d if which == "a" else self.etop_d
        return tv.get(d + idx, _tv_img())

    def tobool(self, idx, which="a"):
        img = self.valat(idx, which)
        ty = struct.unpack_from("<I", img, 8)[0]
        if ty == 0:
            return 0
        if ty == 1 and struct.unpack_from("<I", img, 0)[0] == 0:
            return 0
        return 1

    def checkout(self, tag):
        cap = self.case.get(tag + "_cap", 4)
        cur = self.cur1 if tag == "p1" else self.cur2
        hdr_on = self.case.get(tag, 1) != 0
        if not hdr_on or cur >= (cap & 0x7FFFFFFF):
            return None
        if tag == "p1":
            self.cur1 = cur + 1
        else:
            self.cur2 = cur + 1
        return cur

    def pop_last(self, tag, idx):
        cur = self.cur1 if tag == "p1" else self.cur2
        if cur and idx == cur - 1:
            if tag == "p1":
                self.cur1 = cur - 1
            else:
                self.cur2 = cur - 1


def _m_pcall(m, state, which, tr):
    seq = m.case.get("pcall_rets", [0])
    n = getattr(m, "_pc_n", 0)
    m._pc_n = n + 1
    ret = seq[n] if n < len(seq) else seq[-1]
    # declared stub effect
    return ret


def m_d10(case):
    """expected (ret, trace) for 00684D10."""
    m = MState(case)
    tr = []
    env = case.get("env", ENV)
    pay = case.get("pay", PAY)
    if (pay & 0xFFFFFFFFFFFF) - (pay & 1) == 0:
        return 0, "-", m
    payload = (pay & 0xFFFFFFFFFFFFFFFF) - (pay & 1)
    st_arg = case.get("state", STATE)
    st = st_arg
    idx = m.checkout("p2")
    elem_used = idx is not None
    if elem_used:
        dst = EDST2 + idx * 0x100
        tr.append("c%x:%x:%x" % (dst & 0xFFFFFFFF,
                                 (ESRC2 + idx * 0x100) & 0xFFFFFFFF,
                                 case.get("p2_n", 0x20)))
        st = ESTATE
        which = "e"
    else:
        which = "a"
    tr.append("L%x:%x" % (st & 0xFFFFFFFF,
                          case.get("buf", BUF) & 0xFFFFFFFF))
    if not case.get("load_ret", 1):
        if elem_used:
            m.pop_last("p2", idx)
        return case.get("load_esi", 0), " ".join(tr), m
    tr.append("P%x:0:0:0" % (st & 0xFFFFFFFF))
    r = _m_pcall(m, st, which, tr)
    if r:
        tr.append("E%x:-1" % (st & 0xFFFFFFFF))
        tr.append("G3:%x:%x:%x:%x" % (0xD6FEB0, r & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        if elem_used:
            m.pop_last("p2", idx)
        return 0, " ".join(tr), m
    tr.append("T%x" % (st_arg & 0xFFFFFFFF))
    r13 = m.gettop("a")
    tr.append("T%x" % (st & 0xFFFFFFFF))
    r15 = m.gettop(which)
    tr.append("S%x:%x" % (st & 0xFFFFFFFF, payload & 0xFFFFFFFFFFFFFFFF))
    m.push(payload, case.get("pushls_ty", 4), which)
    tr.append("y%x:-1" % (st & 0xFFFFFFFF))
    if m.typeat(-1, which) == 0:
        if elem_used:
            m.pop_last("p2", idx)
        return 0, " ".join(tr) or "-", m
    if st == st_arg:
        for i in range(1, r13 + 1):
            tr.append("x%x:%x" % (st & 0xFFFFFFFF, i))
            m.push(0, 0, "a")
    else:
        tr.append("C%x:%x:1:%x" % (st_arg & 0xFFFFFFFF,
                                   st & 0xFFFFFFFF, r13))
    tr.append("P%x:%x:1:0" % (st & 0xFFFFFFFF, r13))
    r = _m_pcall(m, st, which, tr)
    for _ in range(max(0, r13)):
        m.pop(1, which)
    for i in range(1):
        m.push(case.get("res_q", ESTR + 0xC00) + i * 0x10,
               case.get("res_ty", 1), which)
    tr.append("E%x:-1" % (st & 0xFFFFFFFF))
    if r:
        tr.append("G3:%x:%x:%x:%x" % (0xD6FEB0, r & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        if elem_used:
            m.pop_last("p2", idx)
        return 0, " ".join(tr), m
    if st != st_arg:
        tr.append("C%x:%x:%x:1" % (st & 0xFFFFFFFF,
                                   st_arg & 0xFFFFFFFF, r15 + 1))
    tr.append("T%x" % (st_arg & 0xFFFFFFFF))
    esi = m.gettop("a") - r13
    if elem_used:
        m.pop_last("p2", idx)
    return esi & 0xFFFFFFFF, " ".join(tr), m


def m_f60(case):
    """expected (ret, trace) for 00684F60."""
    m = MState(case)
    tr = []
    env = case.get("env", ENV)
    st = case.get("state", STATE)
    if env == 0:
        return 7, "-", m
    if st == 0:
        return 1, "-", m
    tr.append("L%x:%x" % (st & 0xFFFFFFFF, env & 0xFFFFFFFF))
    if not case.get("load_ret", 1):
        return case.get("load_esi", 9), " ".join(tr), m
    tr.append("p%x:%x" % (st & 0xFFFFFFFF, env & 0xFFFFFFFF))
    m.pushp(env)
    tr.append("f%x:%x:2" % (st & 0xFFFFFFFF, 0xD701A0))
    m.pop(1)
    tr.append("P%x:0:0:0" % (st & 0xFFFFFFFF))
    seq = case.get("pcall_rets", [0])
    r = seq[0]
    if r:
        tr.append("E%x:-1" % (st & 0xFFFFFFFF))
        packed = (case.get("e48", ESTR + 0x400)
                  & 0xFFFFFFFFFFFFFFFF)
        packed -= packed & 1
        tr.append("G3:%x:%x:%x:%x" % (0xD6FFD8, r & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, packed))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2)
        return 0, " ".join(tr), m
    if s32(case.get("o20", 0)) < 0:
        packed = case.get("e48", ESTR + 0x400) & 0xFFFFFFFFFFFFFFFF
        packed -= packed & 1
        tr.append("G3:%x:%x:0:0" % (0xD70010, packed))
        return 0, " ".join(tr), m
    idx = case.get("r8", 0) & 0xFFFFFFFF
    tab = case.get("tab", [ESTR + 0x800])
    tv = tab[idx] if idx < len(tab) else 0
    packed = (tv & 0xFFFFFFFFFFFFFFFF) - (tv & 1)
    tr.append("S%x:%x" % (st & 0xFFFFFFFF, packed))
    m.push(packed, case.get("pushls_ty", 4))
    tr.append("m%x:%x:%x" % (st & 0xFFFFFFFF,
                             case.get("o10", NAME1) & 0xFFFFFFFFFFFFFFFF,
                             case.get("o18", NAME2) & 0xFFFFFFFFFFFFFFFF))
    tr.append("P%x:1:0:0" % (st & 0xFFFFFFFF))
    r2 = seq[1] if len(seq) > 1 else seq[-1]
    for _ in range(1):
        m.pop(1)
    tr.append("E%x:-1" % (st & 0xFFFFFFFF))
    if r2:
        tr.append("G3:%x:%x:%x:%x" % (0xD6FEB0, r2 & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2)
        return 0, " ".join(tr), m
    if case.get("errstr", ESTR):
        tr.append("G2:%x:%x:%x:%x" % (0xD6E970,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0, 0))
    return 0, " ".join(tr), m


def m_c280(case):
    """expected (ret, trace) for 00686280."""
    m = MState(case)
    tr = []
    va = case.get("vario", VARIO)
    if va == 0:
        return 0, "-", m
    if case.get("tags_ptr", TAGS) == 0:
        return 0, "-", m
    env = case.get("env", ENV)
    pay = case.get("pay", PAY)
    if (pay & 0xFFFFFFFFFFFFFFFF) - (pay & 1) == 0:
        return 0, "-", m
    payload = pay - (pay & 1)
    # two-pool checkout: p1 first, then p2; first non-null state wins
    st = 0
    elem_tag = elem_idx = None
    for tag in ("p1", "p2"):
        i = m.checkout(tag)
        if i is None:
            continue
        dst, src = ((EDST, ESRC) if tag == "p1" else (EDST2, ESRC2))
        tr.append("c%x:%x:%x" % ((dst + i * 0x100) & 0xFFFFFFFF,
                                 (src + i * 0x100) & 0xFFFFFFFF,
                                 case.get(tag + "_n", 0x20)))
        states = case.get(tag + "_states")
        sv = states[i] if states else ESTATE
        if sv:
            st, elem_tag, elem_idx = sv, tag, i
            break
    if st == 0:
        return 0, " ".join(tr) or "-", m
    which = "e" if st == ESTATE else "a"
    tr.append("L%x:%x" % (st & 0xFFFFFFFF,
                          case.get("buf", BUF) & 0xFFFFFFFF))
    if not case.get("load_ret", 1):
        if elem_tag:
            m.pop_last(elem_tag, elem_idx)
        return 0, " ".join(tr), m
    tr.append("P%x:0:0:0" % (st & 0xFFFFFFFF))
    seq = case.get("pcall_rets", [0])
    r = seq[0]
    if r:
        tr.append("E%x:-1" % (st & 0xFFFFFFFF))
        tr.append("G3:%x:%x:%x:%x" % (0xD6FEB0, r & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        if elem_tag:
            m.pop_last(elem_tag, elem_idx)
        return 0, " ".join(tr), m
    tr.append("S%x:%x" % (st & 0xFFFFFFFF, payload & 0xFFFFFFFFFFFFFFFF))
    m.push(payload, case.get("pushls_ty", 4), which)
    tr.append("y%x:-1" % (st & 0xFFFFFFFF))
    if m.typeat(-1, which) == 0:
        if elem_tag:
            m.pop_last(elem_tag, elem_idx)
        return 0, " ".join(tr) or "-", m
    tr.append("I%x" % (st & 0xFFFFFFFF))
    # marshal loop
    tags = case.get("tags", [])
    pays = case.get("payarr", [])
    n12 = 1
    sent_pos = {SENTB + k * 0x10: k for k in range(12)}
    for ti, tag in enumerate(tags):
        i = sent_pos.get(tag, -1)
        order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        if i < 0:
            for k in order:
                tr.append("s%d" % k)
            tr.append("D%x:%x:%x" % (tag & 0xFFFFFFFFFFFFFFFF,
                                     CURH & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF))
            if not case.get("disp_ret", 1):
                tr.append("G1:%x:%x:%x:%x" % (0xD6FEE0, n12, 0, 0))
            n12 += 1
            continue
        for k in order[:i + 1]:
            tr.append("s%d" % k)
        pay = pays[ti] if ti < len(pays) else 0
        tr.append("g%x:1" % (st & 0xFFFFFFFF))
        if i == 0:
            tr.append("b%x:%x" % (st & 0xFFFFFFFF, 1 if pay else 0))
            m.pushb(pay, which)
        elif i in (9, 10):
            tr.append("n%x" % (st & 0xFFFFFFFF))
            m.pushn(pay, which)
        else:
            tr.append("i%x:%x" % (st & 0xFFFFFFFF, pay & 0xFFFFFFFF))
            m.pushi(pay, which)
        n12 += 1
    tr.append("P%x:%x:1:0" % (st & 0xFFFFFFFF, n12))
    r2 = seq[1] if len(seq) > 1 else seq[-1]
    for _ in range(max(0, n12)):
        m.pop(1, which)
    m.push(case.get("res_q", ESTR + 0xC00), case.get("res_ty", 1), which)
    if r2:
        tr.append("E%x:-1" % (st & 0xFFFFFFFF))
        tr.append("G3:%x:%x:%x:%x" % (0xD6FEB0, r2 & 0xFFFFFFFF,
                                      case.get("errstr", ESTR)
                                      & 0xFFFFFFFFFFFFFFFF, 0))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        if elem_tag:
            m.pop_last(elem_tag, elem_idx)
        return 0, " ".join(tr) or "-", m
    # result dispatch on arg3 (rtag)
    rtag = case.get("rtag", SENTB)
    ri = -1
    for k, v in enumerate(SENTS):
        if rtag == SENTB + k * 0x10:
            ri = k
    res_out = None
    if ri == 0:
        tr.append("s0")
        tr.append("B%x:-1" % (st & 0xFFFFFFFF))
        bv = m.tobool(-1, which)
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        res_out = ("b", bv)
    elif ri in (1, 2):
        for k in range(0, ri + 1):
            tr.append("s%d" % k)
        tr.append("N%x:-1" % (st & 0xFFFFFFFF))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        res_out = ("b", case.get("tonum_ret", 0x1234) & 0xFF)
    elif ri in (3, 4):
        for k in range(0, ri + 1):
            tr.append("s%d" % k)
        tr.append("N%x:-1" % (st & 0xFFFFFFFF))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        res_out = ("d", case.get("tonum_ret", 0x1234) & 0xFFFF)
    elif ri in (5, 6):
        for k in range(0, ri + 1):
            tr.append("s%d" % k)
        tr.append("N%x:-1" % (st & 0xFFFFFFFF))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        res_out = ("d", case.get("tonum_ret", 0x1234) & 0xFFFFFFFF)
    elif ri in (7, 8):
        for k in range(0, ri + 1):
            tr.append("s%d" % k)
        tr.append("N%x:-1" % (st & 0xFFFFFFFF))
        tr.append("t%x:-2" % (st & 0xFFFFFFFF))
        m.settop(-2, which)
        res_out = ("q", case.get("tonum_ret", 0x1234)
                   & 0xFFFFFFFFFFFFFFFF)
    else:
        for k in range(9):
            tr.append("s%d" % k)
        if case.get("geta_ret", 0):
            tr.append("a%x:%x:%x" % (rtag & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF, VARIO
                                     & 0xFFFFFFFFFFFFFFFF))
            res_out = ("qa", case.get("geta_q", ESTR + 0xD00),
                       case.get("geta_b", 1))
        elif case.get("getb_ret", 0):
            tr.append("a%x:%x:%x" % (rtag & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF, VARIO
                                     & 0xFFFFFFFFFFFFFFFF))
            tr.append("z%x:%x:%x" % (rtag & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF, VARIO
                                     & 0xFFFFFFFFFFFFFFFF))
            res_out = ("qb", case.get("getb_q", ESTR + 0xD40),
                       case.get("getb_b", 2))
        else:
            tr.append("a%x:%x:%x" % (rtag & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF, VARIO
                                     & 0xFFFFFFFFFFFFFFFF))
            tr.append("z%x:%x:%x" % (rtag & 0xFFFFFFFFFFFFFFFF,
                                     st & 0xFFFFFFFF, VARIO
                                     & 0xFFFFFFFFFFFFFFFF))
            # SING leaf runs real: returns shipped const; |1 compare
            if rtag == (SING_TOK | 1):
                tr.append("h%x" % (st & 0xFFFFFFFF))
                res_out = ("q", case.get("mshl_ret", ESTR + 0xD80)
                           & 0xFFFFFFFFFFFFFFFF)
            else:
                tr.append("G1:%x:%x:%x:%x" % (0xD6FF20, va & 0xFFFFFFFFFFFFFFFF, 0, 0))
                if elem_tag:
                    m.pop_last(elem_tag, elem_idx)
                return 0, " ".join(tr) or "-", m
    if elem_tag:
        m.pop_last(elem_tag, elem_idx)
    m.res_out = res_out
    return 1, " ".join(tr), m


# ---- run + compare ---------------------------------------------------------

def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", D10)
    uc.reg_write(UC_X86_REG_RCX, case.get("obj", OBJ))
    uc.reg_write(UC_X86_REG_RDX, case.get("state", STATE)
                 & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R8, (case.get("rtag", case.get("r8", 0))
                 if entry == C280 else case.get("r8", 0))
                 & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R9, case.get("vario", VARIO)
                 & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(entry, RETQ, count=4_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))

    gm = w.gm
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF}
    st = case.get("state", STATE)
    if st:
        obs["top"] = struct.unpack("<Q", gm.r(st + 0x10, 8))[0]
        obs["stk"] = [list(gm.r(STK + i * 0x10, 0x10))
                      for i in range(case.get("obs_stk", 0))]
    obs["etop"] = struct.unpack("<Q", gm.r(ESTATE + 0x10, 8))[0]
    obs["estk"] = [list(gm.r(ESTK + i * 0x10, 0x10))
                   for i in range(case.get("obs_estk", 0))]
    for tag, g, hdr in (("p1", G_P1, HDR1), ("p2", G_P2, HDR2)):
        h = case.get(tag + "_hdr", hdr if case.get(tag, 1) else 0)
        obs[tag + "_cur"] = struct.unpack("<I", gm.r(h + 0x58, 4))[0] \
            if h else None
    if case.get("obs_copy"):
        i = case["obs_copy"]
        dst, src = ((EDST, ESRC) if case.get("obs_pool", "p2") == "p1"
                    else (EDST2, ESRC2))
        obs["copy"] = list(gm.r(dst + i * 0x100,
                                case.get("p2_n", 0x20) if
                                case.get("obs_pool", "p2") == "p2"
                                else case.get("p1_n", 0x20)))
    va = case.get("vario", VARIO)
    if va and case.get("obs_vario"):
        obs["vario_q"] = struct.unpack("<Q", gm.r(va, 8))[0]
        obs["vario_b"] = gm.r(va + 8, 1)[0]
        obs["vario_d"] = struct.unpack("<I", gm.r(va + 8, 4))[0]
        obs["vario_q8"] = struct.unpack("<Q", gm.r(va + 8, 8))[0]
    return " ".join(w.trace) or "-", w.faults, obs


def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # ---- D10 ----
    A("d10-pack0", entry=D10, pay=0)
    A("d10-nopool", entry=D10, p2=0, pcall_rets=[0], depth=0,
      obs_stk=2)
    A("d10-loadfail", entry=D10, p2=0, load_ret=0)
    A("d10-loadfail-esi", entry=D10, p2=0, load_ret=0, load_esi=0x77)
    A("d10-pcall1-fail", entry=D10, p2=0, pcall_rets=[5])
    A("d10-checkout", entry=D10, p2_cur=0, p2_n=0x20, pcall_rets=[0],
      depth=0, edepth=0, obs_copy=0, obs_estk=3)
    A("d10-checkout-full", entry=D10, p2_cur=4, p2_cap=4,
      pcall_rets=[0])
    A("d10-samebuf", entry=D10, p2=0, pcall_rets=[0], depth=3,
      stack=[(0x11, 1), (0x22, 3), (0x33, 3)])
    A("d10-diffbuf", entry=D10, p2_cur=0, pcall_rets=[0], depth=2,
      stack=[(0x11, 1), (0x22, 3)], edepth=0)
    A("d10-pcall2-fail", entry=D10, p2=0, pcall_rets=[0, 9], depth=1,
      stack=[(0x11, 1)], obs_stk=4)
    A("d10-type0", entry=D10, p2=0, pcall_rets=[0], depth=0,
      pushls_ty=0)
    A("d10-type16", entry=D10, p2=0, pcall_rets=[0], depth=0,
      pushls_ty=0x10)
    A("d10-pack3", entry=D10, p2=0, pcall_rets=[0], pay=PAY | 3)
    A("d10-cap-bit31", entry=D10, p2_cur=0, p2_cap=0x80000004,
      pcall_rets=[0], obs_copy=0)
    A("d10-cap-bit30", entry=D10, p2_cur=0, p2_cap=0x40000000,
      pcall_rets=[0], obs_copy=0)
    A("d10-checkout-idx1", entry=D10, p2_cur=1, pcall_rets=[0],
      obs_copy=1, depth=0)
    A("d10-samebuf-stk", entry=D10, p2=0, pcall_rets=[0], depth=3,
      stack=[(0x11, 1), (0x22, 3), (0x33, 3)], obs_stk=8)

    # ---- F60 ----
    A("f60-env0", entry=F60, env=0)
    A("f60-state0", entry=F60, state=0)
    A("f60-loadfail", entry=F60, load_ret=0)
    A("f60-loadfail-esi", entry=F60, load_ret=0, load_esi=0x55)
    A("f60-ok", entry=F60, pcall_rets=[0], o20=0,
      tab=[ESTR + 0x801], obs_stk=4)
    A("f60-pcall1-fail", entry=F60, pcall_rets=[7])
    A("f60-o20neg", entry=F60, pcall_rets=[0], o20=0xFFFFFFFF)
    A("f60-pcall2-fail", entry=F60, pcall_rets=[0, 11], o20=0)
    A("f60-errstr0", entry=F60, pcall_rets=[0], o20=0, errstr=0)
    A("f60-idx1", entry=F60, pcall_rets=[0], o20=0, r8=1,
      tab=[ESTR + 0x801, ESTR + 0x901])

    # ---- C280 ----
    A("c280-vario0", entry=C280, vario=0)
    A("c280-head0", entry=C280, tags_ptr=0)
    A("c280-pack0", entry=C280, pay=0)
    A("c280-nopool", entry=C280, p1=0, p2=0)
    A("c280-p1", entry=C280, p1_cur=0, p2=0, pcall_rets=[0],
      tags=[], rtag=SENTB, obs_copy=0, obs_pool="p1", obs_vario=1,
      res_ty=1, res_q=ESTR + 0xC00,
      estack=[(0x99, 1)])
    A("c280-p2-fallback", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=SENTB + 0x70, obs_vario=1, tonum_ret=0xABCD,
      estack=[(0x99, 1)])
    A("c280-p1-full-p2", entry=C280, p1_cur=4, p1_cap=4, p2_cur=0,
      pcall_rets=[0], tags=[], rtag=SENTB, obs_vario=1,
      estack=[(0x99, 1)])
    A("c280-nullstate-skip", entry=C280, p1_states=[0],
      p1_cur=0, p1_cap=4, p2_cur=0, pcall_rets=[0], tags=[],
      rtag=SENTB, obs_vario=1, estack=[(0x99, 1)])
    A("c280-loadfail", entry=C280, p1=0, p2_cur=0, load_ret=0)
    A("c280-pcall1-fail", entry=C280, p1=0, p2_cur=0,
      pcall_rets=[6])
    A("c280-marshal", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[SENTB, SENTB + 0x10, SENTB + 0x30, SENTB + 0x90],
      payarr=[1, 0x42, 0x1234, 0x3F800000],
      rtag=SENTB, obs_vario=1, estack=[(0x99, 1)], edepth=1,
      obs_estk=6)
    A("c280-marshal-unknown", entry=C280, p1=0, p2_cur=0,
      pcall_rets=[0], tags=[0xDEAD0000], payarr=[0x55],
      rtag=SENTB, obs_vario=1, estack=[(0x99, 1)])
    A("c280-pcall2-fail", entry=C280, p1=0, p2_cur=0,
      pcall_rets=[0, 8], tags=[], rtag=SENTB)
    A("c280-res-i64", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=SENTB + 0x70, obs_vario=1,
      tonum_ret=0x1122334455667788, estack=[(0x99, 1)])
    A("c280-res-geta", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=0xCAFE0000, geta_ret=1, obs_vario=1,
      estack=[(0x99, 1)])
    A("c280-res-getb", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=0xCAFE0000, getb_ret=1, obs_vario=1,
      estack=[(0x99, 1)])
    A("c280-res-unknown", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=0xCAFE0000, obs_vario=1, estack=[(0x99, 1)])
    A("c280-res-word", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=SENTB + 0x30, obs_vario=1, tonum_ret=0xBEEF1234,
      estack=[(0x99, 1)])
    A("c280-res-mshl", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=SING_TOK | 1, obs_vario=1, estack=[(0x99, 1)])
    A("c280-res-bool-nil", entry=C280, p1=0, p2_cur=0,
      pcall_rets=[0], tags=[], rtag=SENTB, obs_vario=1, res_ty=0)
    A("c280-type0", entry=C280, p1=0, p2_cur=0, pcall_rets=[0],
      tags=[], rtag=SENTB, pushls_ty=0)
    return C


def check_case(case, raw, secs):
    entry = case.get("entry", D10)
    tr, faults, obs = run_case(case, raw, secs)
    if entry == D10:
        eret, etr, m = m_d10(case)
    elif entry == F60:
        eret, etr, m = m_f60(case)
    else:
        eret, etr, m = m_c280(case)
    errs = []
    if faults:
        errs.append("faults=%s" % (faults,))
    if obs["ret"] != eret:
        errs.append("ret got=%x exp=%x" % (obs["ret"], eret))
    # trace compare (rdx local in ITER differs — normalize)
    ntr = " ".join(t for t in tr.split())
    if ntr != etr:
        errs.append("trace\n  got=%s\n  exp=%s" % (ntr, etr))
    for tag in ("p1", "p2"):
        exp_cur = m.cur1 if tag == "p1" else m.cur2
        if obs.get(tag + "_cur") is not None and \
                obs[tag + "_cur"] != exp_cur:
            errs.append("%s_cur got=%x exp=%x" %
                        (tag, obs[tag + "_cur"], exp_cur))
    # stack images + top pointers
    if case.get("obs_stk"):
        exp_top = STK + (case.get("framebase", 0) + m.top_d) * 0x10
        if obs["top"] != exp_top:
            errs.append("top got=%x exp=%x" % (obs["top"], exp_top))
        for i in range(case["obs_stk"]):
            exp_img = list(m.tv.get(i, _tv_img()))
            if obs["stk"][i] != exp_img:
                errs.append("stk[%d] got=%s exp=%s" %
                            (i, obs["stk"][i], exp_img))
    if case.get("obs_estk"):
        exp_etop = ESTK + m.etop_d * 0x10
        if obs["etop"] != exp_etop:
            errs.append("etop got=%x exp=%x" % (obs["etop"], exp_etop))
        for i in range(case["obs_estk"]):
            exp_img = list(m.etv.get(i, _tv_img()))
            if obs["estk"][i] != exp_img:
                errs.append("estk[%d] got=%s exp=%s" %
                            (i, obs["estk"][i], exp_img))
    if case.get("obs_copy") is not None and "copy" in obs:
        i = case["obs_copy"]
        n = case.get("p2_n", 0x20) if case.get("obs_pool", "p2") == "p2" \
            else case.get("p1_n", 0x20)
        exp = [(0xA0 + i) & 0xFF] * min(n, 0x40) + [0] * (n - 0x40) \
            if n > 0x40 else [(0xA0 + i) & 0xFF] * n
        if obs["copy"] != exp[:n]:
            errs.append("copy got=%s exp=%s" % (obs["copy"][:8],
                                                exp[:8]))
    if "vario_q" in obs:
        ro = getattr(m, "res_out", None)
        if ro:
            if ro[0] == "b" and obs["vario_b"] != ro[1]:
                errs.append("vario_b got=%x exp=%x" %
                            (obs["vario_b"], ro[1]))
            if ro[0] == "d" and obs["vario_d"] != ro[1]:
                errs.append("vario_d got=%x exp=%x" %
                            (obs["vario_d"], ro[1]))
            if ro[0] == "q" and obs["vario_q8"] != ro[1]:
                errs.append("vario_q8 got=%x exp=%x" %
                            (obs["vario_q8"], ro[1]))
            if ro[0] == "qa" and (obs["vario_q"] != ro[1] or
                                  obs["vario_b"] != ro[2]):
                errs.append("vario_qa got=%x/%x exp=%x/%x" %
                            (obs["vario_q"], obs["vario_b"],
                             ro[1], ro[2]))
            if ro[0] == "qb" and (obs["vario_q"] != ro[1] or
                                  obs["vario_b"] != ro[2]):
                errs.append("vario_qb got=%x/%x exp=%x/%x" %
                            (obs["vario_q"], obs["vario_b"],
                             ro[1], ro[2]))
    return errs


# ---- mutants ---------------------------------------------------------------

# (name, va, orig_byte, patch_byte, discriminating case)
MUTS = [
    # D10 — packed-payload low-bit mask width
    ("m-d10-and1",    0x684D46, 0x01, 0x03, "d10-pack3"),
    # D10 — payload-null gate (jne -> never)
    ("m-d10-pack0",   0x684D4F, 0x07, 0x00, "d10-nopool"),
    # D10 — pool capacity gate invert (jae -> jb)
    ("m-d10-jae",     0x684D75, 0x73, 0x72, "d10-checkout-full"),
    # D10 — capacity bit31 mask -> bit30
    ("m-d10-btr",     0x684D71, 0x1F, 0x1E, "d10-cap-bit30"),
    # D10 — elem stride 0x28 -> 0x18 (sib scale 4->2)
    ("m-d10-stride",  0x684D7F, 0x89, 0x49, "d10-checkout-idx1"),
    # D10 — elem state field +0x20 -> +0x18
    ("m-d10-elemst",  0x684DBE, 0x20, 0x18, "d10-diffbuf"),
    # D10 — pcall2 nargs r13d -> 0
    ("m-d10-nargs",   0x684EC5, 0x8B, 0x31, "d10-samebuf"),
    # D10 — copy-back count r15+1 -> r15
    ("m-d10-copybk",  0x684EF3, 0x01, 0x00, "d10-diffbuf"),
    # D10 — pool-pop slot cmp (rax-1 -> rax-2): no pop
    ("m-d10-poolpop", 0x684F25, 0xFF, 0xFE, "d10-checkout"),
    # D10 — result sub -> add
    ("m-d10-sub",     0x684F0F, 0x2B, 0x03, "d10-samebuf"),
    # F60 — env-null gate
    ("m-f60-envg",    0x684F81, 0x14, 0x00, "f60-ok"),
    # F60 — state-null gate
    ("m-f60-stateg",  0x684F9A, 0x14, 0x00, "f60-ok"),
    # F60 — env0 ret code 7 -> 8
    ("m-f60-ret7",    0x684F84, 0x07, 0x08, "f60-env0"),
    # F60 — state0 ret code 1 -> 2
    ("m-f60-ret1",    0x684F9D, 0x01, 0x02, "f60-state0"),
    # F60 — esi=9 -> 10 (load-fail ret)
    ("m-f60-esi9",    0x684FB8, 0x09, 0x0A, "f60-loadfail"),
    # F60 — o20<0 packed branch invert (jge -> jl)
    ("m-f60-jge",     0x685058, 0x7D, 0x7C, "f60-ok"),
    # F60 — string-table index scale 8 -> 4 (sib f1 -> b1)
    ("m-f60-sib",     0x685089, 0xF1, 0xB1, "f60-idx1"),
    # F60 — pcall2 nargs 1 -> 2
    ("m-f60-lea1n",   0x6850C1, 0x01, 0x02, "f60-ok"),
    # C280 — vario-null gate
    ("m-c280-r9g",    0x6862B1, 0x07, 0x00, "c280-p1"),
    # C280 — pool capacity gate invert (jae -> jb)
    ("m-c280-jae",    0x686325, 0x73, 0x72, "c280-p1-full-p2"),
    # C280 — pool count 2 -> 1
    ("m-c280-pools",  0x68636E, 0x02, 0x01, "c280-nullstate-skip"),
    # C280 — payload cursor stride 8 -> 16
    ("m-c280-cur8",   0x686444, 0x08, 0x10, "c280-marshal"),
    # C280 — arg counter inc -> dec
    ("m-c280-inc",    0x6865E7, 0xC4, 0xCC, "c280-marshal"),
    # C280 — SING|1 -> SING-1 (or -> sub)
    ("m-c280-or",     0x6867A5, 0x0B, 0x2B, "c280-res-mshl"),
    # C280 — pool-pop slot cmp (rcx-1 -> rcx-2)
    ("m-c280-pop",    0x6867F2, 0xFF, 0xFE, "c280-p1"),
    # C280 — result byte offset +8 -> +9
    ("m-c280-b8",     0x686680, 0x08, 0x09, "c280-p1"),
    # C280 — result word offset +8 -> +9
    ("m-c280-w8",     0x6866F0, 0x08, 0x09, "c280-res-word"),
    # C280 — result qword offset +8 -> +0x10
    ("m-c280-q8",     0x68676F, 0x08, 0x10, "c280-res-i64"),
    # GETTOP — stride sar 4 -> 3
    ("m-gt-sar",      0x80FD12, 0x04, 0x03, "d10-samebuf"),
    # GETTOP — depth bias -0x10 -> -0x20
    ("m-gt-lea",      0x80FD0E, 0xF0, 0xE0, "d10-samebuf"),
    # SETTOP — stride shl 4 -> 5 (edx<0 path)
    ("m-st-shl",      0x811172, 0x04, 0x05, "d10-pcall2-fail"),
    # PUSHB — type tag 1 -> 2
    ("m-pb-ty",       0x810462, 0x01, 0x02, "c280-marshal"),
    # PUSHI — type tag 3 -> 4
    ("m-pi-ty",       0x81058F, 0x03, 0x04, "c280-marshal"),
    # PUSHP — type tag 2 -> 3
    ("m-pp-ty",       0x8105AA, 0x02, 0x03, "f60-ok"),
    # PUSHN — top stride +0x10 -> +0x20
    ("m-pn-add",      0x810653, 0x10, 0x20, "c280-marshal"),
    # TOBOOL — nil-type gate invert (je -> jne)
    ("m-tb-nil",      0x81144F, 0x74, 0x75, "c280-res-bool-nil"),
    # TYPE — tag mask 0xF -> 0x1F
    ("m-ty-and",      0x811A68, 0x0F, 0x1F, "d10-type16"),
    # SING — singleton const +0x10
    ("m-sg-lea",      0x6372A3, 0xC9, 0xD9, "c280-res-mshl"),
]


def run_mutants(raw, secs, cases):
    byname = {c["name"]: c for c in cases}
    killed, alive, badsite = [], [], []
    for name, va, orig, patch, cname in MUTS:
        base = byname.get(cname)
        if base is None:
            badsite.append((name, "no case %s" % cname))
            continue
        tr0, f0, obs0 = run_case(base, raw, secs)
        mut = dict(base)
        mut["patch_bytes"] = list(mut.get("patch_bytes", [])) + \
            [(va, bytes([patch]))]
        tr1, f1, obs1 = run_case(mut, raw, secs)
        diff = (tr0 != tr1) or (obs0 != obs1) or bool(f1)
        if diff:
            killed.append(name)
        else:
            # verify the site byte really was orig
            raw_b = None
            for sva, vs, ra, rs in secs:
                rva = va - IMG_LO
                if sva <= rva < sva + rs:
                    raw_b = raw[ra + (rva - sva)]
            if raw_b is not None and raw_b != orig:
                badsite.append((name, "site byte %02x != orig %02x" %
                                (raw_b, orig)))
            else:
                alive.append(name)
    return killed, alive, badsite


def main():
    raw, secs = load_image()
    cases = build_cases()
    npass = nfail = 0
    fails = []
    for case in cases:
        errs = check_case(case, raw, secs)
        if errs:
            nfail += 1
            fails.append((case["name"], errs))
            print("FAIL %s" % case["name"])
            for e in errs:
                print("   %s" % e)
        else:
            npass += 1
            print("pass %s" % case["name"])
    print("== %d/%d cases passed" % (npass, npass + nfail))
    killed, alive, badsite = run_mutants(raw, secs, cases)
    print("== mutants: %d killed, %d alive, %d badsite" %
          (len(killed), len(alive), len(badsite)))
    for n in alive:
        print("   ALIVE %s" % n)
    for n, w in badsite:
        print("   BADSITE %s %s" % (n, w))
    json.dump({"cases": npass + nfail, "pass": npass,
               "fails": [f[0] for f in fails],
               "mutants": len(MUTS), "killed": len(killed),
               "alive": alive,
               "badsite": [b[0] for b in badsite]},
              open("result.json", "w"), indent=1)
    return 1 if (nfail or alive or badsite) else 0


if __name__ == "__main__":
    sys.exit(main())
