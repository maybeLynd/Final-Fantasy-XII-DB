# EXP-102 unit-resolver-family-exec
#
# Executes the SHIPPED bytes of the resolver/accessor cluster around
# BattleStats_FindOwningBattleUnit (EXP-101's subject) under Unicorn:
#
#   0031B770  KINDSCAN  unit whose +0x698 == kind table row:
#                       cl<=0x27 else 0; rdi=[0x2EBF190]+8+cl*0x1C8;
#                       same pool scan as 0031B860 (n/g tokens)
#   0031B750  B750      ret byte[rcx+0xEA9]
#   0031B760  B760      rcx ? ret [rcx+0x30] : 0      (via 00263E30)
#   00263E30  E30       ret [rcx+0x30]
#   00263E40  E40       ret rcx + u32[rcx+0x4C] + s32(edx)
#   00263E50  E50       rcx && [rcx+0x30] ? byte[chain+0xEA9] : -1
#   0031B7E0  B7E0      byte[0x2089340]&0x10 ?
#                       (r=003588B0(rcx)) ? [r+0x30] : 0  : 0
#   0031B8C0  B8C0      (t=00263750(rcx)) ? [t+0x30] : 0
#   00263750  TIDX      ecx<=3 ? [0x209A1F0+ecx*8] : 0
#   003588B0  HDEC      handle {tag@20:11, fam@16:4, idx@0:16}:
#                       fam<5; rec=00263FF0(fam)=0x2098E10+fam*0x288;
#                       need [rec],[rec+8]!=0, idx<[rec+0x20],
#                       [rec+0x10]&1, idx<dword[elems], elems[idx]!=0,
#                       word[entry+0x16]==tag -> entry else 0
#   00263FF0  FAMIDX    ret 0x2098E10 + fam*0x288
#   0031B8E0  KIND      VALID(2,id) else -1;
#                       tab=[0x2EBF130] else -1;
#                       r=0020E600([tab+0xC]) (twice) else -1;
#                       r+id*word[tab+8] else -1;
#                       ret byte[that+7]
#   00309440  CLS       (id>>12)<=0xE ? dword[0x1EEBCF8+(id>>12)*0x58]
#                       : -1
#
# Reused real bodies (executed in earlier EXPs, kept real here):
#   00236850 COUNT, 00236820 GET            (EXP-101)
#   0020E600 RESOLVE = [0x1F83530]+arg, 00322C50 VALID (EXP-100)
#
# No scripted boundaries: every body in the chain runs from shipped bytes.
#
# Trace tokens: n count, g<i> getter, V<a>:<id>=<r> validity, R resolve,
# H hdec, f famidx, t tidx, c cls, K kindscan entry. Observables: ret,
# trace, faults.

import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_RIP, UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
IMG32  = 0x50000000          # authored-data arena
POOL   = HEAP + 0x000000     # unit pool, stride 0xF50
DECOY  = HEAP + 0x800000
STRIDE = 0xF50
MATCH  = 0x698

KINDSCAN = 0x0031B770
B750     = 0x0031B750
B760     = 0x0031B760
E30      = 0x00263E30
E40      = 0x00263E40
E50      = 0x00263E50
B7E0     = 0x0031B7E0
B8C0     = 0x0031B8C0
TIDX     = 0x00263750
HDEC     = 0x003588B0
FAMIDX   = 0x00263FF0
KIND     = 0x0031B8E0
CLS      = 0x00309440
COUNT    = 0x00236850
GET      = 0x00236820
VALID    = 0x00322C50
RESOLVE  = 0x0020E600

G_POOL   = 0x0208E688        # unit pool base
G_COUNT  = 0x0208E6A0        # unit count
G_DBASE  = 0x0208E690
G_DCOUNT = 0x0208E6A4
G_KTAB   = 0x02EBF190        # kind table (rows +8, stride 0x1C8, cl<=0x27)
G_DKTAB  = 0x02EBF198        # decoy kind table
G_FLAG   = 0x02089340        # byte flag, bit 0x10 gates B7E0
G_TIDX   = 0x0209A1F0        # 4-entry object table for TIDX
G_DTIDX  = 0x0209A1F8        # decoy slot inside that table (idx 1)
G_FAMREC = 0x02098E10        # family records, stride 0x288
G_DFTAB  = 0x02EBF130        # def table for KIND/VALID arm2
G_DDFTAB = 0x02EBF138        # decoy
G_RESB   = 0x01F83530        # resolver base global
G_DRESB  = 0x01F83538        # decoy
G_CLS    = 0x01EEBCF8        # family->class table, stride 0x58
G_EQTAB  = 0x02EBF0F8        # equipment table (VALID arm 6, unused here)

KTAB    = IMG32 + 0x20000    # kind table rows live here (+8 stride 0x1C8)
DKTAB   = IMG32 + 0x40000
ELEMS   = IMG32 + 0x60000    # handle element arrays
ENTRY   = IMG32 + 0x80000    # handle entry objects
DEFTAB  = IMG32 + 0xA0000    # def table header
DDFTAB  = IMG32 + 0xC0000
ROWBASE = IMG32 + 0xE0000    # resolved rows (RESOLVE adds arg)

HOOKS = {COUNT: "n", GET: "g", VALID: "V", RESOLVE: "R", HDEC: "H",
         FAMIDX: "f", TIDX: "t", CLS: "c", KINDSCAN: "K"}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
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


def mk_handle(tag, fam, idx):
    return ((tag & 0x7FF) << 20) | ((fam & 0xF) << 16) | (idx & 0xFFFF)


class World:
    def __init__(self, case, raw, secs):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(IMG32, 0x200000)
        gm.map(STACK, 0x100000)

        # pool globals + decoys
        gm.w(G_POOL, qw(case.get("base", POOL)))
        gm.w(G_COUNT, dw(case.get("count", 0)))
        gm.w(G_DBASE, qw(case.get("decoy_base", DECOY)))
        gm.w(G_DCOUNT, dw(case.get("decoy_count", 1)))
        for i, match in enumerate(case.get("matches", [])):
            gm.w(case.get("base", POOL) + i * STRIDE + MATCH, qw(match))

        # kind table + decoy
        gm.w(G_KTAB, qw(case.get("ktab", KTAB)))
        gm.w(G_DKTAB, qw(case.get("dktab", DKTAB)))

        # flag byte
        gm.w(G_FLAG, bytes([case.get("flag", 0) & 0xFF]))

        # TIDX 4-entry table
        for i in range(4):
            gm.w(G_TIDX + i * 8, qw(case.get("tidx", [0] * 4)[i]))

        # handle family records at G_FAMREC + fam*0x288
        for fam, rec in case.get("famrecs", {}).items():
            base = G_FAMREC + fam * 0x288
            gm.w(base + 0x00, qw(rec.get("hdr", 1)))
            gm.w(base + 0x08, qw(rec.get("elems", 0)))
            gm.w(base + 0x10, qw(rec.get("live", 1)))
            gm.w(base + 0x20, dw(rec.get("bound", 0)))
        # element arrays: [0]=count dword, [8+i*8]=entry ptr
        for arr, spec in case.get("elems", {}).items():
            gm.w(arr + 0, dw(spec.get("count", 0)))
            for i, ep in enumerate(spec.get("ptrs", [])):
                gm.w(arr + 8 + i * 8, qw(ep))
        # entry objects: tag word +0x16, result field +0x30
        for obj, spec in case.get("objs", {}).items():
            if "tag" in spec:
                gm.w(obj + 0x16, hw(spec["tag"]))
            if "f30" in spec:
                gm.w(obj + 0x30, qw(spec["f30"]))
            if "f4c" in spec:
                gm.w(obj + 0x4C, dw(spec["f4c"]))
            if "ea9" in spec:
                gm.w(obj + 0xEA9, bytes([spec["ea9"] & 0xFF]))

        # def table + decoy; field writes skipped when the header
        # pointer itself is null (the case means "no table")
        for tab, spec in ((G_DFTAB, case.get("deftab")),
                          (G_DDFTAB, case.get("ddeftab"))):
            if spec is not None:
                gm.w(tab, qw(spec.get("ptr", DEFTAB)))
        for spec, dptr in ((case.get("deftab"), DEFTAB),
                           (case.get("ddeftab"), DDFTAB)):
            if spec is None:
                continue
            p = spec.get("ptr", dptr)
            if not p:
                continue
            gm.w(p + 4, dw(spec.get("cnt", 0)))
            gm.w(p + 8, hw(spec.get("stride", 0)))
            gm.w(p + 0xC, dw(spec.get("rarg", 0)))
        # resolver base + decoy; resolved rows at ROWBASE + rarg
        gm.w(G_RESB, qw(case.get("resb", ROWBASE)))
        gm.w(G_DRESB, qw(case.get("dresb", ROWBASE + 0x10000)))
        for off, b in case.get("row_bytes", {}).items():
            gm.w(ROWBASE + off, bytes([b & 0xFF]))

        # class table (G_CLS, stride 0x58) + decoy at +8
        for fam, cls in case.get("cls", {}).items():
            gm.w(G_CLS + fam * 0x58, dw(cls))
        for fam, cls in case.get("dcls", {}).items():
            gm.w(G_CLS + 8 + fam * 0x58, dw(cls))

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in HOOKS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        gm = self.gm
        if addr == COUNT:
            self.trace.append("n")
        elif addr == GET:
            self.trace.append("g%d" % s32(rcx))
        elif addr == VALID:
            self.trace.append("V%d:%X" % (rcx & 0xFFFFFFFF, rdx & 0xFFFF))
            self._watch_ret()
        elif addr == RESOLVE:
            self.trace.append("R%x" % (rcx & 0xFFFFFFFF))
            self._watch_ret()
        elif addr == HDEC:
            self.trace.append("H%x" % (rcx & 0xFFFFFFFF))
        elif addr == FAMIDX:
            self.trace.append("f%d" % s32(rcx))
        elif addr == TIDX:
            self.trace.append("t%d" % s32(rcx))
        elif addr == CLS:
            self.trace.append("c%X" % (rcx & 0xFFFF))
            self._watch_ret()
        elif addr == KINDSCAN:
            self.trace.append("K%d" % (rcx & 0xFF))

    def _watch_ret(self):
        # capture the token index: a hooked call can nest inside this one
        # (VALID auto-detect -> CLS), so trace[-1] moves before the return
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", gm_r(self, sp, 8))[0]
        idx = len(self.trace) - 1
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            holder["fired"] = True
            self.trace[idx] += "=%d" % s32(uc_.reg_read(UC_X86_REG_RAX))

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


def gm_r(w, addr, n):
    return w.gm.r(addr, n)


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", KINDSCAN)
    uc.reg_write(UC_X86_REG_RCX,
                 case.get("rcx", 0) & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_RDX,
                 case.get("rdx", 0) & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(entry, RETQ, count=200_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF}
    return " ".join(w.trace) or "-", w.faults, w, obs


# ---- model -------------------------------------------------------------------

def uget(i, base, count):
    if i < 0 or i > count - 1:
        return 0
    return base + i * STRIDE


def model(case):
    tr, ret = [], 0
    entry = case.get("entry", KINDSCAN)
    count = s32(case.get("count", 0))
    base = case.get("base", POOL)
    matches = case.get("matches", [])

    def scan(target):
        tr.append("n")
        i = 0
        while i < count:
            tr.append("g%d" % i)
            u = uget(i, base, count)
            if u:
                if i < len(matches) and matches[i] == target:
                    return u
            i += 1
            tr.append("n")
        return 0

    def hdec(h):
        tr.append("H%x" % (h & 0xFFFFFFFF))
        if not h:
            return 0
        tag, fam, idx = (h >> 20) & 0x7FF, (h >> 16) & 0xF, h & 0xFFFF
        if fam >= 5:
            return 0
        tr.append("f%d" % fam)
        rec = case.get("famrecs", {}).get(fam)
        if not rec or not rec.get("hdr", 1) or not rec.get("elems"):
            return 0
        if idx >= rec.get("bound", 0) or not rec.get("live", 1) & 1:
            return 0
        spec = case.get("elems", {}).get(rec["elems"])
        if not spec or idx >= spec.get("count", 0):
            return 0
        ep = spec.get("ptrs", [])[idx] if idx < len(spec.get("ptrs", [])) else 0
        if not ep:
            return 0
        o = case.get("objs", {}).get(ep, {})
        return ep if o.get("tag", 0) == tag else 0

    def valid2(i):
        tr.append("V2:%X" % (i & 0xFFFF))
        dt = case.get("deftab")
        ok = 0
        if dt is not None and dt.get("ptr", DEFTAB):
            ok = 1 if 0 <= s32(i) < s32(dt.get("cnt", 0)) else 0
        tr[-1] += "=%d" % ok
        return ok

    if entry == KINDSCAN:
        cl = case.get("rcx", 0) & 0xFF
        tr.append("K%d" % cl)
        ret = 0
        if cl <= 0x27:
            ktab = case.get("ktab", KTAB)
            target = ktab + 8 + cl * 0x1C8
            if target:
                ret = scan(target)
    elif entry == B750:
        o = case.get("objs", {}).get(case.get("rcx", 0), {})
        ret = o.get("ea9", 0)
    elif entry == B760:
        rcx = case.get("rcx", 0)
        o = case.get("objs", {}).get(rcx, {})
        ret = o.get("f30", 0) if rcx else 0
    elif entry == E30:
        o = case.get("objs", {}).get(case.get("rcx", 0), {})
        ret = o.get("f30", 0)
    elif entry == E40:
        rcx = case.get("rcx", 0)
        o = case.get("objs", {}).get(rcx, {})
        ret = rcx + o.get("f4c", 0) + s32(case.get("rdx", 0))
    elif entry == E50:
        rcx = case.get("rcx", 0)
        o = case.get("objs", {}).get(rcx, {})
        chain = o.get("f30", 0)
        if rcx and chain:
            ret = case.get("objs", {}).get(chain, {}).get("ea9", 0)
        else:
            ret = 0xFFFFFFFF
    elif entry == B7E0:
        h = case.get("rcx", 0)
        if case.get("flag", 0) & 0x10:
            r = hdec(h)
            ret = case.get("objs", {}).get(r, {}).get("f30", 0) if r else 0
        else:
            ret = 0
    elif entry == B8C0:
        i = s32(case.get("rcx", 0))
        tr.append("t%d" % i)
        t = case.get("tidx", [0] * 4)[i] if 0 <= i <= 3 else 0
        ret = case.get("objs", {}).get(t, {}).get("f30", 0) if t else 0
    elif entry == TIDX:
        i = s32(case.get("rcx", 0))
        tr.append("t%d" % i)
        ret = case.get("tidx", [0] * 4)[i] if 0 <= i <= 3 else 0
    elif entry == HDEC:
        ret = hdec(case.get("rcx", 0))
    elif entry == FAMIDX:
        tr.append("f%d" % s32(case.get("rcx", 0)))
        ret = G_FAMREC + s32(case.get("rcx", 0)) * 0x288
    elif entry == KIND:
        i = s32(case.get("rcx", 0))
        ret = 0xFFFFFFFF
        if valid2(i):
            dt = case["deftab"]
            p = dt.get("ptr", DEFTAB)
            rarg, stride = dt.get("rarg", 0), dt.get("stride", 0)
            tr.append("R%x" % rarg)
            r1 = case.get("resb", ROWBASE) + rarg
            tr[-1] += "=%d" % (r1 if r1 else 0)
            if r1:
                tr.append("R%x" % rarg)
                tr[-1] += "=%d" % r1
                addr = r1 + i * stride
                if addr:
                    ret = case.get("row_bytes", {}).get(
                        addr - ROWBASE + 7, 0)
    elif entry == CLS:
        i = case.get("rcx", 0) & 0xFFFF
        tr.append("c%X" % i)
        fam = i >> 12
        if fam <= 0xE:
            ret = case.get("cls", {}).get(fam, 0)
        else:
            ret = 0xFFFFFFFF
        # direct entry: the return goes to RETQ, the watch never fires,
        # so no =<ret> lands on the token
    elif entry == VALID:
        # direct auto-detect arm: ecx=1 -> CLS -> re-dispatch jt[cls-1]
        i = case.get("rdx", 0) & 0xFFFF
        tr.append("V1:%X" % i)
        tr.append("c%X" % i)
        fam = i >> 12
        cls = case.get("cls", {}).get(fam, 0) if fam <= 0xE else -1
        tr[-1] += "=%d" % cls
        # the nested CLS watch fires (its return lands inside VALID);
        # the direct-entry V watch does not (returns to RETQ)
        ok = 0
        if cls == 2:
            dt = case.get("deftab")
            ok = 1 if (dt is not None and dt.get("ptr", DEFTAB)
                       and 0 <= s32(i) < s32(dt.get("cnt", 0))) else 0
        return " ".join(tr), {"ret": ok}, None
    return " ".join(tr) or "-", {"ret": ret}, None


# ---- cases --------------------------------------------------------------------

def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # KINDSCAN: find unit owning kind-cl's table row
    A("ks-bound-max", rcx=0x27, count=2,
      matches=[0, KTAB + 8 + 0x27 * 0x1C8])
    A("ks-bound-over", rcx=0x28, count=2, matches=[0, 0])
    A("ks-hit0", rcx=3, count=3, matches=[KTAB + 8 + 3 * 0x1C8, 0, 0])
    A("ks-hit-mid", rcx=5, count=4, matches=[0, KTAB + 8 + 5 * 0x1C8, 0, 0])
    A("ks-miss", rcx=2, count=3, matches=[0, 0, 0])
    A("ks-null-tab", rcx=1, ktab=0, count=2, matches=[0, 0])
    A("ks-dup-first", rcx=4, count=3,
      matches=[KTAB + 8 + 4 * 0x1C8, KTAB + 8 + 4 * 0x1C8, 0])
    # accessors
    A("e30-read", entry=E30, rcx=ENTRY,
      objs={ENTRY: {"f30": 0x1122334455667788}})
    A("e30-zero", entry=E30, rcx=ENTRY, objs={ENTRY: {"f30": 0}})
    A("b760-null", entry=B760, rcx=0)
    A("b760-ok", entry=B760, rcx=ENTRY, objs={ENTRY: {"f30": 0xABCD}})
    A("b750-read", entry=B750, rcx=ENTRY, objs={ENTRY: {"ea9": 0x5A}})
    A("e40-index", entry=E40, rcx=ENTRY, rdx=7,
      objs={ENTRY: {"f4c": 0x1000}})
    A("e40-neg", entry=E40, rcx=ENTRY, rdx=0xFFFFFFFC,
      objs={ENTRY: {"f4c": 0x1000}})
    A("e50-chain", entry=E50, rcx=ENTRY,
      objs={ENTRY: {"f30": ENTRY + 0x100}, ENTRY + 0x100: {"ea9": 0x33}})
    A("e50-null-obj", entry=E50, rcx=0)
    A("e50-null-chain", entry=E50, rcx=ENTRY, objs={ENTRY: {"f30": 0}})
    # TIDX + B8C0
    A("tidx-2", entry=TIDX, rcx=2,
      tidx=[ENTRY, ENTRY + 8, ENTRY + 0x10, ENTRY + 0x18])
    A("tidx-3", entry=TIDX, rcx=3,
      tidx=[ENTRY, ENTRY + 8, ENTRY + 0x10, ENTRY + 0x18])
    A("tidx-4", entry=TIDX, rcx=4,
      tidx=[ENTRY, ENTRY + 8, ENTRY + 0x10, ENTRY + 0x18])
    A("tidx-neg", entry=TIDX, rcx=0xFFFFFFFF,
      tidx=[ENTRY, ENTRY + 8, ENTRY + 0x10, ENTRY + 0x18])
    A("b8c0-hit", entry=B8C0, rcx=1, tidx=[0, ENTRY, 0, 0],
      objs={ENTRY: {"f30": 0x777}})
    A("b8c0-oob", entry=B8C0, rcx=9, tidx=[ENTRY, 0, 0, 0],
      objs={ENTRY: {"f30": 0x777}})
    A("b8c0-null-entry", entry=B8C0, rcx=0, tidx=[0, ENTRY, 0, 0])
    # HDEC handle decode
    H = mk_handle(0x55, 2, 1)
    FR = {2: {"hdr": 1, "elems": ELEMS, "live": 1, "bound": 4}}
    EL = {ELEMS: {"count": 3, "ptrs": [ENTRY, ENTRY + 0x40, ENTRY + 0x80]}}
    OB = {ENTRY + 0x40: {"tag": 0x55, "f30": 0x999}}
    A("hdec-ok", entry=HDEC, rcx=H, famrecs=FR, elems=EL, objs=OB)
    A("hdec-zero", entry=HDEC, rcx=0, famrecs=FR, elems=EL, objs=OB)
    A("hdec-fam5", entry=HDEC, rcx=mk_handle(0x55, 5, 1),
      famrecs=FR, elems=EL, objs=OB)
    A("hdec-fam8", entry=HDEC, rcx=mk_handle(0x55, 8, 1),
      famrecs={0: {"hdr": 1, "elems": ELEMS, "live": 1, "bound": 4}},
      elems=EL, objs=OB)
    A("hdec-no-array", entry=HDEC, rcx=H,
      famrecs={2: {"hdr": 1, "elems": 0, "live": 1, "bound": 4}},
      elems=EL, objs=OB)
    A("hdec-no-hdr", entry=HDEC, rcx=H,
      famrecs={2: {"hdr": 0, "elems": ELEMS, "live": 1, "bound": 4}},
      elems=EL, objs=OB)
    A("hdec-idx-bound", entry=HDEC, rcx=mk_handle(0x55, 2, 4),
      famrecs=FR, elems=EL, objs=OB)
    A("hdec-dead", entry=HDEC, rcx=H,
      famrecs={2: {"hdr": 1, "elems": ELEMS, "live": 0, "bound": 4}},
      elems=EL, objs=OB)
    A("hdec-elems-bound", entry=HDEC, rcx=mk_handle(0x55, 2, 3),
      famrecs={2: {"hdr": 1, "elems": ELEMS, "live": 1, "bound": 9}},
      elems=EL, objs=OB)
    A("hdec-null-elem", entry=HDEC, rcx=mk_handle(0x55, 2, 0),
      famrecs=FR, elems=EL, objs=OB)
    A("hdec-tag-miss", entry=HDEC, rcx=mk_handle(0x77, 2, 1),
      famrecs=FR, elems=EL, objs=OB)
    # B7E0 gated resolver
    A("b7e0-off", entry=B7E0, rcx=H, flag=0,
      famrecs=FR, elems=EL, objs=OB)
    A("b7e0-ok", entry=B7E0, rcx=H, flag=0x10,
      famrecs=FR, elems=EL, objs=OB)
    A("b7e0-dead", entry=B7E0, rcx=mk_handle(0x77, 2, 1), flag=0x10,
      famrecs=FR, elems=EL, objs=OB)
    # FAMIDX
    A("famidx-0", entry=FAMIDX, rcx=0)
    A("famidx-4", entry=FAMIDX, rcx=4)
    # KIND byte getter
    DT = {"ptr": DEFTAB, "cnt": 4, "stride": 0x20, "rarg": 0x40}
    A("kind-ok", entry=KIND, rcx=2, deftab=DT, resb=ROWBASE,
      row_bytes={0x40 + 2 * 0x20 + 7: 0x5C})
    A("kind-ok0", entry=KIND, rcx=0, deftab=DT, resb=ROWBASE,
      row_bytes={0x40 + 7: 0x21})
    A("kind-oob", entry=KIND, rcx=4, deftab=DT, resb=ROWBASE,
      row_bytes={0x40 + 4 * 0x20 + 7: 0x5C})
    A("kind-neg", entry=KIND, rcx=0xFFFFFFFF, deftab=DT, resb=ROWBASE)
    A("kind-no-tab", entry=KIND, rcx=1, deftab={"ptr": 0, "cnt": 4},
      resb=ROWBASE)
    A("kind-no-resolve", entry=KIND, rcx=1,
      deftab={"ptr": DEFTAB, "cnt": 4, "stride": 0x20, "rarg": 0},
      resb=0)
    # CLS
    A("cls-ok", entry=CLS, rcx=0x1000, cls={1: 6})
    A("cls-famE", entry=CLS, rcx=0xE000, cls={0xE: 3})
    A("cls-famF", entry=CLS, rcx=0xF000, cls={0xE: 3})
    A("cls-zero", entry=CLS, rcx=0, cls={0: 0})
    # VALID auto-detect (ecx=1): CLS -> re-dispatch arm
    A("valid-auto-arm1", entry=VALID, rcx=1, rdx=0x2002,
      cls={2: 2}, deftab={"ptr": DEFTAB, "cnt": 0x3000})
    A("valid-auto-fail", entry=VALID, rcx=1, rdx=0x2005,
      cls={2: 2}, deftab={"ptr": DEFTAB, "cnt": 4})
    return C


# ---- mutants -------------------------------------------------------------------

MUTANTS = [
    ("m-ks-bnd",   0x31B778, b"\x26",
     "kind bound 0x27 -> 0x26: kind 0x27 is refused"),
    ("m-ks-ja",    0x31B779, b"\x76",
     "kind ja -> jbe: every in-range kind is refused"),
    ("m-ks-stride",0x31B78C, b"\xc0\x01\x00\x00",
     "kind stride 0x1C8 -> 0x1C0: row address off-grid"),
    ("m-ks-add8",  0x31B788, b"\x00",
     "kind +8 -> +0: expected back-pointer shifts by 8"),
    ("m-ks-tab",   0x31B77E, b"\x16\x3a\xba\x02",
     "kind table [0x2EBF190] -> [0x2EBF198]: decoy table"),
    ("m-b760-null",0x31B763, b"\xeb",
     "B760 jne -> jmp: null rcx dereferences [0+0x30]"),
    ("m-750-off",  0x31B753, b"\xa8\x0e\x00\x00",
     "B750 +0xEA9 -> +0xEA8: reads the wrong byte"),
    ("m-e50-jne",  0x263E5D, b"\x84",
     "E50 jne -> je: a live chain reports -1"),
    ("m-7e0-flag", 0x31B7EA, b"\x20",
     "B7E0 flag bit 0x10 -> 0x20: gate never opens"),
    ("m-tidx-bnd", 0x263752, b"\x02",
     "TIDX bound 3 -> 2: index 3 refused"),
    ("m-hdec-fam", 0x3588DB, b"\x07",
     "handle family mask 0xF -> 0x7: families 8+ wrap"),
    ("m-hdec-tag", 0x358927, b"\x44",
     "tag cmovne -> cmove: matching tag returns 0"),
    ("m-kind-s8",  0x31B92C, b"\x0a",
     "KIND stride word[tab+8] -> word[tab+0xA]: wrong stride"),
    ("m-kind-p7",  0x31B937, b"\x08",
     "KIND +7 -> +8: kind byte read one late"),
    ("m-cls-shr",  0x309445, b"\x0d",
     "CLS shr 0xC -> 0xD: family split at the wrong bit"),
    ("m-resb",     0x20E605, b"\x2f\x4f\xd7\x01",
     "resolver base [0x1F83530] -> [0x1F83538]: decoy base"),
]


def main():
    raw, secs = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    results = {}
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        exp_tr, exp_obs, exp_fault = model(case)
        mem_faults = [f for f in faults if f[0] == "MEM"]
        ok = bool(tr == exp_tr and not mem_faults
                  and obs["ret"] == exp_obs["ret"])
        npass += ok
        nfail += (not ok)
        results[case["name"]] = (tr, obs, bool(mem_faults))
        if not ok:
            print("FAIL %s\n  got:  %s ret=%x fault=%s\n  want: %s ret=%x"
                  % (case["name"], tr, obs["ret"], mem_faults,
                     exp_tr, exp_obs["ret"]))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr,
                             "ok": bool(ok), "obs": obs,
                             "exp_trace": exp_tr, "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))

    fired = set()
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        fired |= w.fired
    out["bodies_fired"] = ["0x%X" % v for v in sorted(fired)]
    print("fired:", " ".join("%s@%x" % (HOOKS[v], v) for v in sorted(fired)))

    base = {c["name"]: results[c["name"]] for c in build_cases()}
    for name, va, data, why in MUTANTS:
        n_diff, diffs = 0, []
        for case in build_cases():
            c = dict(case)
            c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs)
            mem = bool([f for f in faults if f[0] == "MEM"])
            if (tr, obs, mem) != base[case["name"]]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s ret=%x" % (tr, obs["ret"])))
        killed = n_diff > 0
        print(("KILL " if killed else "SURV") + " %s  (%d divergent) %s"
              % (name, n_diff, why))
        out["mutants"].append({"name": name, "va": "0x%X" % va,
                               "killed": killed, "divergent": n_diff,
                               "why": why, "sample": diffs[:3]})
    json.dump(out, open("result.json", "w"), indent=1,
              default=lambda o: o.hex() if isinstance(o, bytes) else str(o))
    return 0 if nfail == 0 and all(m["killed"] for m in out["mutants"]) else 1


if __name__ == "__main__":
    sys.exit(main())
