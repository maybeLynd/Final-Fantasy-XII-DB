# EXP-141 loot-pool-exec — isolated original-code run (ASTRA-TRANSFER-
# ORACLE-S33-LOOT-POOL; original request OPUS-REQ-ASTRA-S33-LOOT-POOL-
# ISOLATED-RUN). Executes the five world-loot pool ops plus their real
# callees under Unicorn; a Python model mirrors site-for-site.
#
#   INIT    00319B10 — unrolled pool init: per node q[+4]=0 (state+stamp
#            merged), q[+10]=0 prev, q[+18]=0 next, d[+58]=0 handle,
#            d[+0]=slotIndex 0..9; q[HEAD]=q[TAIL]=0; tail-jmp FB250.
#   FB250   002FB250 — ten byte stores: b[PRES_T + i*0x20] = 0.
#   CREATE  00319CA0 — scan slots 0..9 for state==0 (cmp d[rbx+4],ebp;
#            add rbx,0x60; cmp eax,0xA; jl). All busy -> evict head:
#            unlink, PRES(handle,op5,&uninit frame+0x20), FB2A0(slot),
#            zero state/stamp/next/prev/handle — then the SAME node is
#            appended at TAIL (FIFO). Copies 56B drop buffer (3 movups
#            + 1 movsd), d[+4]=1, builds payload {pos.xyz, 1.0f, rare,
#            tblval} at frame+0x20, calls RARE(drops), then
#            PRES(ecx=0,op1,&payload) — handle = eax. If d[GGATE]>0
#            (signed) calls GATE0 (a shipped `ret 0` no-op).
#   TICK    00319600 — cookie-guarded. head==0 -> out. Per node:
#            state==1 -> EFE0(handle)->FA730 (flag b[obj+0x272]&1, then
#            walk intrusive list q[mgr+0x57E0+0x2490] via +0x278 for the
#            node==object — the +0x58 "handle" IS a truncated pointer,
#            UQ-137's mechanism confirmed on bytes); ret==2 -> stamp=
#            clock, state=2, EFC0->FA6E0->CPY16 publishes object+0..0xF
#            to frame, FB2D0(slot,&pos) writes presence +0x10/flag.
#            state 2..6 -> step=cvtt(-30f*scalar); fire when clock >=
#            stamp - step*(0x3C-(7-state)); on fire state++ BEFORE the
#            call and PRES(handle,op2,&(7-oldstate)).
#            state==7 -> fire when clock >= stamp - step*0x3C (=+1800
#            at scalar 1.0): unlink, PRES(handle,op4,&uninit frame+0x20),
#            FB2A0(slot), zero — THEN advance reads [rbx+0x18]==0, so a
#            despawn ENDS the walk (one retire per tick). state 0 or >7:
#            skipped (jle / jne).
#   COLLECT 00319920 — 7-entry grant loop: ax=w[node+0x20+8k] != 0xFFFF
#            -> INV(id, d[+4] qty, 1); inc d[CNT]; unlink; payload slot
#            <- edx arg; PRES(handle,op3,&payload); FB2A0(slot); zero.
#   REMOVE  003197B0 — unlink; payload <- edx; PRES(handle,op3); FB2A0;
#            zero. No grant, no counter.
#   CWRAP   00319A00 — rcx = POOL + movsxd(ecx)*0x60; jmp COLLECT.
#   RWRAP   00319830 — same -> REMOVE. No bounds check.
#   PRES    0028F000 — dispatcher: mgr=q[MGR_G] null -> 0; op 1..6 via
#            jtab 0x28F09C. op1->0x28F034: r9d=pl[0x14], r8d=pl[0x10],
#            rdx=pl, rcx=mgr+0x57E0, tail L160. op2->0x28F050: edx=
#            d[pl], rcx=handle, call LA10, ret handle. op3->0x28F063:
#            edx=d[pl], call L820, ret handle. op4/5->0x28F076: edx=0,
#            call L820, ret 0 — ops 4 and 5 share ONE target, the
#            payload slot is never read. op6->0x28F088: rcx=mgr+0x57E0,
#            call L900, ret 0.
#   RARE    00319A20 — per drop entry (stride 8, id w[+0]): skip
#            id==0xFFFF or (id&0xF000)!=0x1000; else row = itemdesc-
#            encoded: ecx = decodelo + w[itd+8]*(id-0x1000); tier =
#            TIER(row) = remap(b[row+9]) -> 1..9 (0 if class>0x1A);
#            tier 1..5 -> return 0 EARLY; tier 6 -> r=1; else r stays.
#            Returns 0/1/2 -> payload+0x10 (rarity/glow).
#   TIER    0031E9F0 — b[rcx+9] >0x1A -> 0; else btab 0x31EA74 ->
#            jtab 0x31EA50 -> ret slot+1.
#   DECODE  0020E600 — rax = ecx + q[0x1F83530].
#   EFE0    0028EFE0 — edx=handle; rcx=q[MGR_G]+0x57E0; jmp FA730.
#            NO null-manager test — null mgr + flagged object faults
#            at q[0x7C70].
#   EFC0    0028EFC0 — r8=rdx out; edx=handle; rcx=mgr+0x57E0; jmp
#            FA6E0.
#   FA730   003FA730 — ret 0 if !(b[obj+0x272]&1); walk list
#            q[rcx+0x2490] by q[+0x278]; match (elem==obj) -> ret
#            d[obj+0x260]; exhausted -> 0.
#   FA6E0   003FA6E0 — same walk; match -> CPY16(out, obj) 16B, ret 1.
#   CPY16   00202C90 — movups [rdx]->[rcx].
#   FB2A0   002FB2A0 — ecx>9 (unsigned) -> -1; else b[PRES_T+ecx*0x20]
#            =0, ret 1.
#   FB2D0   002FB2D0 — ecx>9 -> -1; b[entry]==1 -> -2 NO WRITE; else
#            entry+0x10 <- 16B from rdx, flag=1, ret 1.
#   GATE0   0016D6A0 — shipped `ret 0` (the create counter-gated call
#            is a no-op in this build).
#   CHKCK   00808C40 — real __security_check_cookie vs q[0x1F44830].
#
# Scripted boundaries (disclosed): five host trampolines intercept the
# leaf entries — no image bytes patched; the native `call`/`jmp`
# executes, the hook supplies the body and returns:
#   L160 003FA160 pres op1 leaf — records r8/r9 + 16B payload, returns
#        the scripted handle (default = the planted object OBJ, so the
#        tick ready-query resolves end-to-end).
#   LA10 003FAA10 pres op2 leaf — records rcx/edx.
#   L820 003FA820 pres op3/4/5 leaf — records rcx/edx (edx provably 0
#        for op4/5 by the dispatcher's xor, not by stack content).
#   L900 003FA900 pres op6 leaf — records rcx.
#   INV  00300B80 inventory grant — records id/qty/r8.
#
# Fixture (planted, disclosed): all pool/list/presence/clock/counter/
# manager/item-descriptor globals are BSS (ship 0) or planted cells;
# MGR/OBJ/drop/position buffers live on the guest heap. Ops 4/5 receive
# a harness-clean (zeroed) stack slot — disclosed; the boundary that
# matters (dispatcher never reads it) is proven by the leaf edx=0.
# patch_bytes overrides of .rdata scalars (SCAL_C, TBLZ) are disclosed
# fixture edits, not shipped-behavior claims. Everything fixture-
# planted is MODEL-PROVEN, not replay authority.
#
# Native and model must agree on trace/rets/faults/watched memory.

import ctypes
import hashlib
import json
import struct
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_HOOK_INTR, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RSP, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

INIT    = 0x00319B10
CREATE  = 0x00319CA0
TICK    = 0x00319600
COLLECT = 0x00319920
REMOVE  = 0x003197B0
CWRAP   = 0x00319A00
RWRAP   = 0x00319830
FB250   = 0x002FB250
FB2A0   = 0x002FB2A0
FB2D0   = 0x002FB2D0
EFE0    = 0x0028EFE0
EFC0    = 0x0028EFC0
FA730   = 0x003FA730
FA6E0   = 0x003FA6E0
CPY16   = 0x00202C90
RARE    = 0x00319A20
DECODE  = 0x0020E600
TIER    = 0x0031E9F0
PRES    = 0x0028F000
GATE0   = 0x0016D6A0
CHKCK   = 0x00808C40

L160 = 0x003FA160                 # stub: presentation op1 leaf
LA10 = 0x003FAA10                 # stub: presentation op2 leaf
L820 = 0x003FA820                 # stub: presentation op3/4/5 leaf
L900 = 0x003FA900                 # stub: presentation op6 leaf
INV  = 0x00300B80                 # stub: inventory grant
STUBS = (L160, LA10, L820, L900, INV)

POOL    = 0x2EC0FA0               # ten nodes x 0x60
HEAD_G  = 0x2EC1360
TAIL_G  = 0x2EC1368
PRES_T  = 0x22BE7F0               # presence table, stride 0x20
CLOCK_G = 0x208D45C               # dword field clock
CNT_G   = 0x22C3174               # pickups collected
MGR_G   = 0x209BE80               # q: manager ptr
GIDX_G  = 0x22C3158               # dword: TBLZ index (ja 3 -> 0)
GGATE_G = 0x22C3164               # dword: >0 -> call GATE0
ITD_G   = 0x2EBF0F8               # q: item-table descriptor
BASECELL = 0x1F83530              # q: decode base
SCAL_C  = 0x1DFE0B8               # float scalar (ships 1.0f)
TBLZ    = 0x1EED3A8               # 4xdword table (ships [0,1,2,3])

MGR   = HEAP + 0x60000            # manager fixture (list at +0x7C70)
OBJ   = HEAP + 0x70000            # world object fixture (handle)
OBJ2  = HEAP + 0x70800            # second object fixture
ITD   = HEAP + 0x68000            # item-table descriptor fixture
                                  # (must clear MGR's 0x8000 span)
BASEP = HEAP + 0x30000            # decode base
IROWS = BASEP + 0x8000            # item rows in BASE pool
DROP  = HEAP + 0x90000            # drop buffer (56B)
POSP  = HEAP + 0x91000            # create position vec3


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)
def fw(f): return struct.pack("<f", f)


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


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL,
                            ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x"
                       % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data),
                       len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]


def mknode(slot, state=0, stamp=0, handle=0, drops=None):
    n = bytearray(0x60)
    n[0:4] = dw(slot)
    n[4:8] = dw(state)
    n[8:0xC] = dw(stamp)
    if drops:
        for i, (iid, qty) in enumerate(drops[:7]):
            n[0x20 + i * 8:0x22 + i * 8] = ww(iid)
            n[0x24 + i * 8:0x28 + i * 8] = dw(qty)
    n[0x58:0x5C] = dw(handle)
    return n


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    W.append((BASECELL, qw(case.get("basep", BASEP))))
    W.append((MGR_G, qw(case.get("mgr", MGR))))
    W.append((ITD_G, qw(case.get("itd", ITD))))
    W.append((CLOCK_G, dw(case.get("clock", 0))))
    W.append((CNT_G, dw(case.get("cnt", 0))))
    W.append((GIDX_G, dw(case.get("gidx", 0))))
    W.append((GGATE_G, dw(case.get("ggate", 0))))
    # item-table descriptor: w[+8]=stride, d[+0xC]=enc (decode ->
    # row base low32 = enc + BASEP_low32)
    itd = bytearray(0x20)
    itd[8:0xA] = ww(case.get("istride", 0x20))
    itd[0xC:0x10] = dw(case.get("ienc", IROWS - BASEP))
    W.append((ITD, bytes(itd)))
    # item rows: b[+9] = class byte -> tier (only 0x1xxx ids ever
    # reach a row — RARE's mask gate skips everything else)
    pool = bytearray(0x10000)
    for rid, cls in case.get("itab", {}).items():
        r = (IROWS - BASEP) + 0x20 * (rid - 0x1000)
        if 0 <= r + 9 < len(pool):
            pool[r + 9] = cls & 0xFF
    W.append((BASEP, bytes(pool)))
    # manager: intrusive object list head at +0x7C70 (mgr+0x57E0's
    # +0x2490 member)
    mgr = bytearray(0x8000)
    objects = case.get("objects", {})
    head = 0
    prev = 0
    for addr in sorted(objects):
        if objects[addr].get("onlist", True):
            if prev:
                mgr[0] = mgr[0]      # placeholder; links below
            if not head:
                head = addr
            prev = addr
    mgr[0x7C70:0x7C78] = qw(case.get("listhead", head))
    W.append((MGR, bytes(mgr)))
    for addr, o in objects.items():
        ob = bytearray(0x300)
        pos = o.get("pos", (0.0, 0.0, 0.0, 0.0))
        for i, f in enumerate(pos):
            ob[i * 4:i * 4 + 4] = fw(f)
        ob[0x260:0x264] = dw(o.get("ostate", 0))
        ob[0x272] = o.get("oflag", 0) & 0xFF
        ob[0x278:0x280] = qw(o.get("onext", 0))
        W.append((addr, bytes(ob)))
    # drop buffer (56B) and position vec3
    db = bytearray(0x40)
    for i, (iid, qty) in enumerate(case.get("drops", [])[:7]):
        db[i * 8:i * 8 + 2] = ww(iid)
        db[i * 8 + 4:i * 8 + 8] = dw(qty)
    W.append((DROP, bytes(db)))
    px, py, pz = case.get("pos", (0.0, 0.0, 0.0))
    W.append((POSP, fw(px) + fw(py) + fw(pz) + fw(0.0)))
    # the pool: seed every slot, then the list
    poolb = bytearray(0x3C0)
    pre = case.get("preinit", True)
    if case.get("dirty"):
        poolb = bytearray([0xAA] * 0x3C0)
    elif pre:
        for s in range(10):
            poolb[s * 0x60:s * 0x60 + 4] = dw(s)
    listed = case.get("list", [])        # ordered list of slot ids
    nodes = case.get("nodes", {})        # slot -> field dict
    for s, nd in nodes.items():
        n = mknode(s, nd.get("state", 0), nd.get("stamp", 0),
                   nd.get("handle", 0), nd.get("drops"))
        for i, b in enumerate(n):
            if i < 0x10 or 0x20 <= i < 0x58 or i >= 0x58:
                poolb[s * 0x60 + i] = b
        poolb[s * 0x60 + 4:s * 0x60 + 8] = dw(nd.get("state", 0))
        poolb[s * 0x60 + 8:s * 0x60 + 0xC] = dw(nd.get("stamp", 0))
        poolb[s * 0x60:s * 0x60 + 4] = dw(s)
    # overwrite any explicitly-raw node
    for s, rawn in case.get("rawnodes", {}).items():
        poolb[s * 0x60:(s + 1) * 0x60] = rawn[:0x60]
    # link the listed nodes (prev/next); unlisted keep 0
    for j, s in enumerate(listed):
        pv = POOL + listed[j - 1] * 0x60 if j else 0
        nx = POOL + listed[j + 1] * 0x60 if j + 1 < len(listed) else 0
        poolb[s * 0x60 + 0x10:s * 0x60 + 0x18] = qw(pv)
        poolb[s * 0x60 + 0x18:s * 0x60 + 0x20] = qw(nx)
    W.append((POOL, bytes(poolb)))
    W.append((HEAD_G, qw(POOL + listed[0] * 0x60 if listed else
                         case.get("head", 0))))
    W.append((TAIL_G, qw(POOL + listed[-1] * 0x60 if listed else
                         case.get("tail", 0))))
    # presence table
    pres = bytearray(0x140)
    for s, (flag, pos4) in case.get("pres", {}).items():
        pres[s * 0x20] = flag & 0xFF
        for i, f in enumerate(pos4):
            pres[s * 0x20 + 0x10 + i * 4:s * 0x20 + 0x14 + i * 4] = fw(f)
    W.append((PRES_T, bytes(pres)))
    return W


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, addr, size))
        uc.emu_stop()
        return True

    def on_code(self, uc, addr, size, _):
        if addr == GATE0:
            # shipped `ret 0` — record the call boundary but let the
            # real bytes execute
            self.trace.append("gate0")
            return
        if addr not in STUBS:
            return
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        r9 = uc.reg_read(UC_X86_REG_R9)
        if addr == L160:
            try:
                pl = self.gm.r(rdx, 16).hex()
            except KeyError:
                pl = "unmapped"
            self.trace.append("pres1:%x:%x:%s" % (r8, r9, pl))
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("op1ret", OBJ))
        elif addr == LA10:
            self.trace.append("pres2:%x:%x" % (rcx, rdx))
            uc.reg_write(UC_X86_REG_RAX, rcx)
        elif addr == L820:
            self.trace.append("pres345:%x:%x" % (rcx, rdx))
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif addr == L900:
            self.trace.append("pres6:%x" % rcx)
            uc.reg_write(UC_X86_REG_RAX, 0)
        elif addr == INV:
            self.trace.append("inv:%x:%x:%x" % (rcx, rdx, r8))
            uc.reg_write(UC_X86_REG_RAX, 0)
        self._ret(uc)

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        try:
            uc.emu_start(entry, RETQ, count=300000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for step in self.case.get("steps", []):
            entry, rcx = step[0], step[1]
            rdx = step[2] if len(step) > 2 else 0
            r8 = step[3] if len(step) > 3 else 0
            r9 = step[4] if len(step) > 4 else 0
            self.run_one(entry, rcx, rdx, r8, r9)

    def obs(self):
        mem = {}
        for addr, n in self.case.get("watch", []):
            try:
                mem["%x" % addr] = self.gm.r(addr, n).hex()
            except KeyError:
                mem["%x" % addr] = None
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------

RANGES = ((HEAP, HEAP + 0x100000), (IMG_LO, IMG_HI),
          (STACK, STACK + 0x100000))


def f32(v):
    return struct.unpack("<f", struct.pack("<f", v))[0]


def cvtt(v):
    return int(v) & 0xFFFFFFFF    # truncate toward zero (matches
                                # cvttss2si for in-range floats)


class Model:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.fault_end = RETQ
        self._rax = 0
        self._fault_rax = 0

    # memory
    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            try:
                return img_rd(self.raw, self.secs, a, 1)[0]
            except KeyError:
                return 0
        return 0
    def mw(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a):
        return self.md(a) | (self.md(a + 4) << 32)
    def sb(self, a, v):
        self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def sd(self, a, v):
        for i in range(4):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def sq(self, a, v):
        for i in range(8):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)
    def sf(self, a, f):
        for i, b in enumerate(fw(f)):
            self.sb(a + i, b)

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in RANGES)

    def _rd(self, a, n, site, raxv=None):
        """ordered read: records ('memr', a, n) + fault_end on
        unmapped and returns None. fault residue = the tracked rax
        (cookie^rsp, last call return, or list cursor) unless the
        caller supplies a better value."""
        if not self.mapped(a):
            self.faults.append(("memr", a & 0xFFFFFFFFFFFFFFFF, n))
            self.fault_end = site
            self._fault_rax = self._rax if raxv is None else raxv
            return None
        if n == 1:
            return self.mb(a)
        if n == 2:
            return self.mw(a)
        if n == 4:
            return self.md(a)
        return self.mq(a)

    def s32(self, v):
        v &= 0xFFFFFFFF
        return v - 0x100000000 if v & 0x80000000 else v

    # ---------- scripted boundaries ----------
    def stub_l160(self, rcx, rdx, r8d, r9d):
        pl = "".join("%02x" % self.mb(rdx + i) for i in range(16)) \
            if self.mapped(rdx) and self.mapped(rdx + 15) \
            else "unmapped"
        self.trace.append("pres1:%x:%x:%s" % (r8d, r9d, pl))
        return self.case.get("op1ret", OBJ)

    def stub_la10(self, rcx, rdx):
        self.trace.append("pres2:%x:%x" % (rcx, rdx))
        return rcx

    def stub_l820(self, rcx, rdx):
        self.trace.append("pres345:%x:%x" % (rcx, rdx))
        return 0

    def stub_l900(self, rcx):
        self.trace.append("pres6:%x" % rcx)
        return 0

    def stub_inv(self, rcx, rdx, r8):
        self.trace.append("inv:%x:%x:%x" % (rcx, rdx, r8))
        return 0

    # ---------- bodies ----------
    def decode(self, i):
        """0020E600 — rax = ecx + q[0x1F83530]."""
        self._rax = (i + self.mq(BASECELL)) & 0xFFFFFFFFFFFFFFFF
        return self._rax

    def tier(self, row):
        """0031E9F0 — b[row+9] >0x1A -> 0; else btab -> jtab ->
        ret slot+1."""
        k = self._rd(row + 9, 1, 0x31E9F0)
        if k is None:
            return None
        if k > 0x1A:
            self._rax = 0
            return 0
        slot = self.mb(0x31EA74 + k)
        if slot > 8:
            self.faults.append(("unmodeled-tier-slot", slot, 0))
            return None
        # jtab arms are compiler-interleaved, not sequential:
        # slot 0..8 -> ret 1,2,3,4,6,7,8,9,5 (verified on bytes)
        ret = (1, 2, 3, 4, 6, 7, 8, 9, 5)[slot]
        self._rax = ret
        return ret

    def rare(self, drops):
        """00319A20 — qualifying ids (0xFFFF skip, (id&F000)==0x1000)
        classify via TIER; tier 1..5 -> ret 0 early; tier 6 -> r=1;
        default 2."""
        rsi = self.mq(ITD_G)
        r = 2
        for i in range(7):
            bx = self._rd(drops + i * 8, 2, 0x319A60)
            if bx is None:
                return None
            if bx == 0xFFFF or (bx & 0xF000) != 0x1000:
                continue
            if rsi:
                p = self.decode(self.md(rsi + 0xC))
                if p:
                    rsi = self.mq(ITD_G)
                    ecx = (self.mw(rsi + 8) * ((bx - 0x1000) & 0xFFFFFFFF)
                           + (self.decode(self.md(rsi + 0xC)) & 0xFFFFFFFF)
                           ) & 0xFFFFFFFF
                else:
                    ecx = 0
            else:
                ecx = 0
            t = self.tier(ecx)
            if t is None:
                return None
            if t <= 0:
                continue
            if t <= 5:
                self._rax = 0
                return 0
            if t == 6:
                r = 1
        self._rax = r
        return r

    def fb250(self):
        """002FB250 — zero the flag byte of all ten presence slots."""
        for i in range(10):
            self.sb(PRES_T + i * 0x20, 0)

    def fb2a0(self, slot):
        """002FB2A0 — presence clear; ecx>9 (unsigned) -> -1."""
        if (slot & 0xFFFFFFFF) > 9:
            self._rax = 0xFFFFFFFF
            return 0xFFFFFFFF
        self.sb(PRES_T + self.s32(slot) * 0x20, 0)
        self._rax = 1
        return 1

    def fb2d0(self, slot, src):
        """002FB2D0 — presence publish; >9 -> -1; flag already 1 ->
        -2 with NO write."""
        if (slot & 0xFFFFFFFF) > 9:
            self._rax = 0xFFFFFFFF
            return 0xFFFFFFFF
        e = PRES_T + self.s32(slot) * 0x20
        b = self._rd(e, 1, 0x2FB2E3)
        if b is None:
            return None
        if b == 1:
            self._rax = 0xFFFFFFFE
            return 0xFFFFFFFE
        for i in range(16):
            self.sb(e + 0x10 + i, self.mb(src + i))
        self.sb(e, 1)
        self._rax = 1
        return 1

    def fa730(self, rcx, obj):
        """003FA730 — flag test first, then intrusive-list walk."""
        b = self._rd(obj + 0x272, 1, 0x3FA730)
        if b is None:
            return None
        if not (b & 1):
            self._rax = 0
            return 0
        rax = self._rd(rcx + 0x2490, 8, 0x3FA739)
        if rax is None:
            return None
        while rax:
            self._rax = rax        # rax is the walk cursor
            if rax == obj:
                v = self._rd(obj + 0x260, 4, 0x3FA759)
                if v is not None:
                    self._rax = v
                return v
            rax = self._rd(rax + 0x278, 8, 0x3FA74A)
            if rax is None:
                return None
        self._rax = 0
        return 0

    def efe0(self, handle):
        """0028EFE0 — edx=handle; rcx=q[MGR_G]+0x57E0; jmp FA730.
        No null-manager test."""
        rcx = (self.mq(MGR_G) + 0x57E0) & 0xFFFFFFFFFFFFFFFF
        return self.fa730(rcx, handle & 0xFFFFFFFF)

    def fa6e0(self, rcx, obj, out):
        """003FA6E0 — same walk; match -> copy [obj]->out, ret 1."""
        b = self._rd(obj + 0x272, 1, 0x3FA6E4)
        if b is None:
            return None
        if not (b & 1):
            self._rax = 0
            return 0
        rax = self._rd(rcx + 0x2490, 8, 0x3FA6ED)
        if rax is None:
            return None
        while rax:
            self._rax = rax        # rax is the walk cursor
            if rax == obj:
                for i in range(16):
                    self.sb(out + i, self.mb(obj + i))
                self._rax = 1
                return 1
            rax = self._rd(rax + 0x278, 8, 0x3FA705)
            if rax is None:
                return None
        self._rax = 0
        return 0

    def efc0(self, handle, out):
        """0028EFC0 — r8=out; edx=handle; rcx=mgr+0x57E0; FA6E0."""
        rcx = (self.mq(MGR_G) + 0x57E0) & 0xFFFFFFFFFFFFFFFF
        return self.fa6e0(rcx, handle & 0xFFFFFFFF, out)

    def pres(self, handle, op, pl):
        """0028F000 — dispatcher. mgr null -> 0; op 1..6 jtab.
        Ops 4/5 share one arm that zeroes edx — the payload slot is
        never read."""
        r10 = pl
        ebx = handle & 0xFFFFFFFF
        mgr = self._rd(MGR_G, 8, 0x28F00B)
        if mgr is None:
            return None
        if mgr == 0:
            self._rax = 0
            return 0
        a = (op - 1) & 0xFFFFFFFF
        if a > 5:
            self._rax = 0
            return 0
        tgt = (self.md(0x28F09C + a * 4) + 0x120000) & 0xFFFFFFFF
        if tgt == 0x28F034:
            r9 = self._rd(r10 + 0x14, 4, 0x28F034)
            if r9 is None:
                return None
            r8d = self._rd(r10 + 0x10, 4, 0x28F03F)
            if r8d is None:
                return None
            self._rax = self.stub_l160(
                (mgr + 0x57E0) & 0xFFFFFFFFFFFFFFFF, r10, r8d, r9)
            return self._rax
        if tgt == 0x28F050:
            edx = self._rd(r10, 4, 0x28F050)
            if edx is None:
                return None
            self.stub_la10(ebx, edx)
            self._rax = ebx
            return ebx
        if tgt == 0x28F063:
            edx = self._rd(r10, 4, 0x28F063)
            if edx is None:
                return None
            self.stub_l820(ebx, edx)
            self._rax = ebx
            return ebx
        if tgt == 0x28F076:
            self.stub_l820(ebx, 0)
            self._rax = 0
            return 0
        if tgt == 0x28F088:
            self.stub_l900((mgr + 0x57E0) & 0xFFFFFFFFFFFFFFFF)
            self._rax = 0
            return 0
        self.faults.append(("unmodeled-pres-arm", tgt, 0))
        return None

    def _unlink(self, n):
        """prev/next relink; heads/tails to the globals."""
        rcx = self.mq(n + 0x10)
        rax = self.mq(n + 0x18)
        if rcx:
            self.sq(rcx + 0x18, rax)
        else:
            self.sq(HEAD_G, rax)
        rcx = self.mq(n + 0x18)
        rax = self.mq(n + 0x10)
        if rcx:
            self.sq(rcx + 0x10, rax)
        else:
            self.sq(TAIL_G, rax)

    def _zero(self, n):
        """retire tail: q[+4]=0 (state+stamp), q[+18]=0, q[+10]=0,
        d[+58]=0 — slotIndex +0x00 is never rewritten."""
        self.sq(n + 4, 0)
        self.sq(n + 0x18, 0)
        self.sq(n + 0x10, 0)
        self.sd(n + 0x58, 0)

    def _retire(self, n, op, pl):
        """the shared sequence: unlink, PRES(handle,op,&pl),
        FB2A0(slot), zero. rax ends as fb2a0's return."""
        self._unlink(n)
        r = self.pres(self.md(n + 0x58), op, pl)
        if r is None:
            return None
        self.fb2a0(self.md(n))
        self._zero(n)
        return 1

    def init(self):
        """00319B10 — the unrolled init; then tail-jmp FB250.
        rax = 0 on exit (xor at entry, never rewritten)."""
        self.sq(HEAD_G, 0)
        self.sq(TAIL_G, 0)
        for s in range(10):
            n = POOL + s * 0x60
            self.sq(n + 4, 0)        # state + stamp, one qword
            self.sq(n + 0x18, 0)
            self.sq(n + 0x10, 0)
            self.sd(n + 0x58, 0)
            self.sd(n + 0, s)
        self.fb250()
        self._rax = 0

    def create(self, drops, pos, vsp):
        """00319CA0 — scan->evict-if-full->append->copy->op1."""
        f = vsp - 0x48             # push rdi + sub 0x40
        rbx, eax = POOL, 0
        while True:
            st = self._rd(rbx + 4, 4, 0x319CC5)
            if st is None:
                return
            if st == 0:
                break
            eax += 1
            rbx += 0x60
            if eax >= 0xA:
                break
        if eax >= 0xA:
            # evict head; payload slot frame+0x20 uninitialized
            rbx = self.mq(HEAD_G)
            if self._retire(rbx, 5, f + 0x20) is None:
                return
        # append at tail
        rax = self.mq(TAIL_G)
        if rax:
            self.sq(rax + 0x18, rbx)
            self.sq(rbx + 0x10, rax)
        else:
            self.sq(HEAD_G, rbx)
            self.sq(rbx + 0x10, 0)
        self.sq(TAIL_G, rbx)
        self.sq(rbx + 0x18, 0)
        # 56B drop copy: 3 movups + 1 movsd
        for i in range(56):
            self.sb(rbx + 0x20 + i, self.mb(drops + i))
        self.sd(rbx + 4, 1)
        # payload at frame+0x20: pos.xyz, 1.0f, rare, tblval
        self.sd(f + 0x20, self.md(pos))
        self.sd(f + 0x24, self.md(pos + 4))
        self.sd(f + 0x28, self.md(pos + 8))
        self.sf(f + 0x2C, 1.0)
        r = self.rare(drops)
        if r is None:
            return
        self.sd(f + 0x30, r)
        gi = self.md(GIDX_G)
        if gi > 3:
            self.sd(f + 0x34, 0)
        else:
            self.sd(f + 0x34, self.md(TBLZ + gi * 4))
        h = self.pres(0, 1, f + 0x20)
        if h is None:
            return
        self.sd(rbx + 0x58, h & 0xFFFFFFFF)
        if self.s32(self.md(GGATE_G)) > 0:
            self.trace.append("gate0")    # GATE0 is a shipped ret 0
        self._rax = h & 0xFFFFFFFFFFFFFFFF  # eax survives to ret

    def tick(self, vsp):
        """00319600 — the walk. rax at entry becomes cookie^rsp; it
        survives to ret on the head==0 / skip paths and is overwritten
        by the bound computation on non-firing timers or by call
        returns on firing ones."""
        f = vsp - 0x78             # push rbx + sub 0x70
        self._rax = (self.mq(0x1F44830) ^
                     ((vsp - 0x78) & 0xFFFFFFFFFFFFFFFF)) \
            & 0xFFFFFFFFFFFFFFFF
        rbx = self.mq(HEAD_G)
        if rbx == 0:
            return
        while True:
            edx = self._rd(rbx + 4, 4, 0x319640)
            if edx is None:
                return
            if edx == 1:
                h = self.md(rbx + 0x58)
                r = self.efe0(h)
                if r is None:
                    return
                if r == 2:
                    clk = self.md(CLOCK_G)
                    self.sd(rbx + 8, clk)
                    self.sd(rbx + 4, 2)
                    r = self.efc0(h, f + 0x40)
                    if r is None:
                        return
                    for i in range(16):
                        self.sb(f + 0x20 + i, self.mb(f + 0x40 + i))
                    r = self.fb2d0(self.md(rbx), f + 0x20)
                    if r is None:
                        return
            elif self.s32(edx) <= 1:
                pass                       # state 0/-: skip
            elif edx <= 6:
                step = cvtt(f32(-30.0) * f32(
                    struct.unpack("<f", struct.pack(
                        "<I", self.md(SCAL_C)))[0]))
                r8d = (7 - edx) & 0xFFFFFFFF
                eax = (0x3C - r8d) & 0xFFFFFFFF
                ecx = (self.s32(step) * self.s32(eax)) & 0xFFFFFFFF
                bound = (self.md(rbx + 8) - ecx) & 0xFFFFFFFF
                if self.md(CLOCK_G) < bound:   # jb unsigned
                    self._rax = bound          # eax = stamp - ecx
                else:
                    ecx_h = self.md(rbx + 0x58)
                    self.sd(f + 0x20, r8d)
                    self.sd(rbx + 4, (edx + 1) & 0xFFFFFFFF)
                    r = self.pres(ecx_h, 2, f + 0x20)
                    if r is None:
                        return
            elif edx == 7:
                step = cvtt(f32(-30.0) * f32(
                    struct.unpack("<f", struct.pack(
                        "<I", self.md(SCAL_C)))[0]))
                ecx = (self.s32(step) * 0x3C) & 0xFFFFFFFF
                bound = (self.md(rbx + 8) - ecx) & 0xFFFFFFFF
                if self.md(CLOCK_G) >= bound:
                    # payload slot frame+0x20 uninitialized (op4)
                    if self._retire(rbx, 4, f + 0x20) is None:
                        return
                else:
                    self._rax = bound
            # advance — after a retire [rbx+0x18] is 0, so a despawn
            # ends the walk
            rbx = self._rd(rbx + 0x18, 8, 0x31977A)
            if rbx is None:
                return
            if rbx == 0:
                return

    def collect(self, node, payload, vsp):
        """00319920 — grant loop then retire op3."""
        f = vsp - 0x48
        rbx = node + 0x24
        for _ in range(7):
            ax = self._rd(rbx - 4, 2, 0x319950)
            if ax is None:
                return
            if ax != 0xFFFF:
                self._rax = self.stub_inv(ax, self.md(rbx), 1)
            rbx += 8
        self.sd(CNT_G, (self.md(CNT_G) + 1) & 0xFFFFFFFF)
        self._unlink(node)
        self.sd(f + 0x20, payload & 0xFFFFFFFF)
        r = self.pres(self.md(node + 0x58), 3, f + 0x20)
        if r is None:
            return
        self.fb2a0(self.md(node))
        self._zero(node)
        self._rax = 0                    # xor eax,eax before the
                                         # zero stores

    def remove(self, node, payload, vsp):
        """003197B0 — retire op3, no grant/counter."""
        f = vsp - 0x48
        self._unlink(node)
        self.sd(f + 0x20, payload & 0xFFFFFFFF)
        r = self.pres(self.md(node + 0x58), 3, f + 0x20)
        if r is None:
            return
        self.fb2a0(self.md(node))
        self._zero(node)
        self._rax = 0                    # xor eax,eax

    def cwrap(self, idx, payload, vsp):
        """00319A00 — node = POOL + movsxd(ecx)*0x60 -> COLLECT."""
        node = (POOL + self.s32(idx) * 0x60) & 0xFFFFFFFFFFFFFFFF
        return self.collect(node, payload, vsp)

    def rwrap(self, idx, payload, vsp):
        """00319830 — same -> REMOVE."""
        node = (POOL + self.s32(idx) * 0x60) & 0xFFFFFFFFFFFFFFFF
        return self.remove(node, payload, vsp)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        rdx = step[2] if len(step) > 2 else 0
        r8 = step[3] if len(step) > 3 else 0
        vsp = STACK + 0x80000
        if entry == INIT:
            m.init()
        elif entry == CREATE:
            m.create(rcx, rdx, vsp)
        elif entry == TICK:
            m.tick(vsp)
        elif entry == COLLECT:
            m.collect(rcx, rdx, vsp)
        elif entry == REMOVE:
            m.remove(rcx, rdx, vsp)
        elif entry == CWRAP:
            m.cwrap(rcx, rdx, vsp)
        elif entry == RWRAP:
            m.rwrap(rcx, rdx, vsp)
        elif entry == FB2A0:
            m._rax = m.fb2a0(rcx)
        elif entry == FB2D0:
            m._rax = m.fb2d0(rcx, rdx)
        elif entry == FB250:
            m.fb250()
        elif entry == EFE0:
            m._rax = m.efe0(rcx)
        elif entry == EFC0:
            m._rax = m.efc0(rcx, rdx)
        elif entry == RARE:
            m._rax = m.rare(rcx)
        elif entry == TIER:
            m._rax = m.tier(rcx)
        elif entry == DECODE:
            m._rax = m.decode(rcx)
        elif entry == PRES:
            m._rax = m.pres(rcx, rdx, r8)
        else:
            raise KeyError("no model entry %x" % entry)
        m.rets.append(m._rax & 0xFFFFFFFFFFFFFFFF
                      if m._rax is not None else
                      m._fault_rax & 0xFFFFFFFFFFFFFFFF)
        m.ends.append(m.fault_end)
        m._rax = 0
    mem = {}
    for addr, n in case.get("watch", []):
        try:
            mem["%x" % addr] = bytes(
                m.mem.get(addr + i, 0) for i in range(n)).hex()
        except KeyError:
            mem["%x" % addr] = None
    return {"trace": m.trace, "faults": m.faults,
            "rets": m.rets, "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

POOLW = [(POOL, 0x3C0), (HEAD_G, 8), (TAIL_G, 8)]
PRESW = [(PRES_T, 0x140)]
DROPS3 = [(0x0101, 2), (0x0202, 1), (0x0303, 5), (0xFFFF, 0)]
OBJRDY = {OBJ: dict(oflag=1, ostate=2,
                    pos=(1.0, 2.0, 3.0, 4.0), onlist=True)}


def cases():
    cs = {}
    # ---- INIT ----
    cs["d-init"] = dict(steps=[(INIT, 0)], dirty=True,
                        head=0xDEAD, tail=0xBEEF,
                        pres={3: (1, (9.0,) * 4)},
                        watch=POOLW + PRESW)
    cs["d-init-idem"] = dict(steps=[(INIT, 0), (INIT, 0)],
                             list=[3],
                             nodes={3: dict(state=4, stamp=9,
                                            handle=0x77)},
                             watch=POOLW + PRESW)
    # ---- CREATE ----
    cs["c-create1"] = dict(steps=[(CREATE, DROP, POSP)],
                           drops=DROPS3, pos=(5.0, 6.0, 7.0),
                           watch=POOLW)
    cs["c-create2"] = dict(
        steps=[(CREATE, DROP, POSP), (CREATE, DROP, POSP)],
        drops=DROPS3, pos=(5.0, 6.0, 7.0), watch=POOLW)
    cs["c-fill10"] = dict(
        steps=[(CREATE, DROP, POSP)] * 10,
        drops=DROPS3, pos=(1.0, 0.0, 0.0), watch=POOLW)
    # 11th drop: evict head (op5) then reuse the SAME node at tail
    cs["c-evict"] = dict(
        steps=[(CREATE, DROP, POSP)] * 11,
        drops=DROPS3, pos=(1.0, 0.0, 0.0), watch=POOLW)
    # free a middle slot then create -> reused slot, appended at tail
    # (slot2 keeps a stale stamp — kills the d[rbx+5] scan mutant)
    cs["c-midfree"] = dict(
        steps=[(CREATE, DROP, POSP)],
        list=[0, 1, 3],
        nodes={0: dict(state=2, stamp=1, handle=0xA),
               1: dict(state=2, stamp=1, handle=0xB),
               2: dict(state=0, stamp=0x99, handle=0),
               3: dict(state=2, stamp=1, handle=0xC)},
        drops=DROPS3, pos=(0.0, 0.0, 0.0), watch=POOLW)
    # null manager: presentation returns 0 -> handle 0 stored
    cs["c-nullmgr"] = dict(steps=[(CREATE, DROP, POSP)], mgr=0,
                           drops=DROPS3, pos=(1.0, 2.0, 3.0),
                           watch=POOLW)
    # op1 leaf returns 0 -> handle 0
    cs["c-op1ret0"] = dict(steps=[(CREATE, DROP, POSP)], op1ret=0,
                           drops=DROPS3, pos=(1.0, 2.0, 3.0),
                           watch=POOLW)
    # rarity paths through RARE+TIER
    cs["c-rare2"] = dict(steps=[(CREATE, DROP, POSP)],
                         drops=[(0x0101, 1), (0xFFFF, 0)],
                         pos=(0.0, 0.0, 0.0), watch=POOLW)
    cs["c-rare6"] = dict(steps=[(CREATE, DROP, POSP)],
                         drops=[(0x1001, 1), (0x0101, 1)],
                         itab={0x1001: 0x12},      # tier 6 -> r=1
                         pos=(0.0, 0.0, 0.0), watch=POOLW)
    cs["c-rare5"] = dict(steps=[(CREATE, DROP, POSP)],
                         drops=[(0x1001, 1), (0x1002, 1)],
                         itab={0x1001: 0x12,      # tier 6 -> r=1
                               0x1002: 0x1A},     # tier 5 -> early 0
                         pos=(0.0, 0.0, 0.0), watch=POOLW)
    # drop[6] exercises the cmove line (tier 6 -> r=1), gives the
    # drop-tail movsd nonzero bytes to observe, and makes the loop
    # bound matter (mutant count 6 would skip the classification)
    cs["c-rare7th"] = dict(steps=[(CREATE, DROP, POSP)],
                           drops=[(0, 0)] * 6 + [(0x1001, 1)],
                           itab={0x1001: 0x12},   # tier 6 -> r=1
                           pos=(0.0, 0.0, 0.0), watch=POOLW)
    # non-qualifying id classes are ignored by RARE
    cs["c-raremask"] = dict(steps=[(CREATE, DROP, POSP)],
                            drops=[(0x2001, 1), (0x0FFF, 1)],
                            itab={0x2001: 0x13},
                            pos=(0.0, 0.0, 0.0), watch=POOLW)
    # counter-gated call: GGATE>0 -> calls GATE0 (a shipped no-op)
    cs["c-gate"] = dict(steps=[(CREATE, DROP, POSP)],
                      drops=DROPS3, pos=(1.0, 0.0, 0.0), ggate=1,
                      watch=POOLW)
    # GIDX table path: gidx=3 is the last in-range index (TBLZ
    # patched nonzero — disclosed fixture edit)
    cs["c-tvalidx"] = dict(steps=[(CREATE, DROP, POSP)],
                           drops=DROPS3, pos=(1.0, 0.0, 0.0),
                           gidx=3,
                           patch_bytes=[(TBLZ, dw(0) + dw(0) +
                                        dw(0) + dw(0xBEEF))],
                           watch=POOLW)
    # ---- TICK ----
    cs["t-empty"] = dict(steps=[(TICK, 0)], watch=POOLW)
    cs["t-s1-ready"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects=OBJRDY, watch=POOLW + PRESW)
    cs["t-s1-notready"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects={OBJ: dict(oflag=1, ostate=1, onlist=True)},
        watch=POOLW + PRESW)
    cs["t-s1-noflag"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects={OBJ: dict(oflag=0, ostate=2, onlist=True)},
        watch=POOLW + PRESW)
    cs["t-s1-notonlist"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects={OBJ: dict(oflag=1, ostate=2, onlist=False),
                 OBJ2: dict(oflag=1, ostate=2, onlist=True)},
        watch=POOLW + PRESW)
    # null manager + flagged object -> faults at q[0x7C70]
    cs["t-s1-nullmgr"] = dict(
        steps=[(TICK, 0)], clock=1000, mgr=0,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects=OBJRDY, watch=POOLW)
    # presence already occupied -> FB2D0 refuses the republish (-2)
    cs["t-s1-occupied"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=OBJ)},
        objects=OBJRDY,
        pres={2: (1, (9.0, 9.0, 9.0, 9.0))},
        watch=POOLW + PRESW)
    # blink ladder: state s fires at stamp + 30*(0x3C-(7-s))
    # state2: +1650, state3: +1680, state4: +1710, state5: +1740,
    # state6: +1770, state7(despawn): +1800
    cs["t-blink2"] = dict(
        steps=[(TICK, 0)], clock=1650,
        list=[2], nodes={2: dict(state=2, stamp=0, handle=0xAB)},
        watch=POOLW + PRESW)
    cs["t-blink2-1"] = dict(
        steps=[(TICK, 0)], clock=1649,
        list=[2], nodes={2: dict(state=2, stamp=0, handle=0xAB)},
        watch=POOLW + PRESW)
    cs["t-blink6"] = dict(
        steps=[(TICK, 0)], clock=1770,
        list=[2], nodes={2: dict(state=6, stamp=0, handle=0xAB)},
        watch=POOLW + PRESW)
    cs["t-despawn"] = dict(
        steps=[(TICK, 0)], clock=1800,
        list=[2], nodes={2: dict(state=7, stamp=0, handle=0xAB)},
        pres={2: (1, (1.0, 2.0, 3.0, 4.0))},
        watch=POOLW + PRESW)
    cs["t-despawn-1"] = dict(
        steps=[(TICK, 0)], clock=1799,
        list=[2], nodes={2: dict(state=7, stamp=0, handle=0xAB)},
        watch=POOLW + PRESW)
    # despawn mid-list relinks neighbors and ends the walk — the
    # second due node survives this tick
    cs["t-despawn-mid"] = dict(
        steps=[(TICK, 0)], clock=1800,
        list=[0, 1, 2],
        nodes={0: dict(state=7, stamp=0, handle=0xA0),
               1: dict(state=7, stamp=0, handle=0xA1),
               2: dict(state=7, stamp=0, handle=0xA2)},
        watch=POOLW + PRESW)
    # tail despawn — head stays, tail cleared
    cs["t-despawn-tail"] = dict(
        steps=[(TICK, 0)], clock=1800,
        list=[0, 1],
        nodes={0: dict(state=2, stamp=0, handle=0xA0),
               1: dict(state=7, stamp=0, handle=0xA1)},
        watch=POOLW + PRESW)
    # state 0 node on the list (I6 violation injected): skipped
    cs["t-state0"] = dict(
        steps=[(TICK, 0)], clock=5000,
        list=[0, 1],
        nodes={0: dict(state=0, stamp=0, handle=0xA0),
               1: dict(state=7, stamp=0, handle=0xA1)},
        watch=POOLW + PRESW)
    # state 8 node on the list: skipped
    cs["t-state8"] = dict(
        steps=[(TICK, 0)], clock=5000,
        list=[0, 1],
        nodes={0: dict(state=8, stamp=0, handle=0xA0),
               1: dict(state=7, stamp=0, handle=0xA1)},
        watch=POOLW + PRESW)
    # scalar override: 2.0f -> step -60 -> state7 bound = stamp+3600
    cs["t-scalar2"] = dict(
        steps=[(TICK, 0)], clock=3599,
        list=[2], nodes={2: dict(state=7, stamp=0, handle=0xAB)},
        patch_bytes=[(SCAL_C, fw(2.0))],
        watch=POOLW + PRESW)
    cs["t-scalar2-hit"] = dict(
        steps=[(TICK, 0)], clock=3600,
        list=[2], nodes={2: dict(state=7, stamp=0, handle=0xAB)},
        patch_bytes=[(SCAL_C, fw(2.0))],
        watch=POOLW + PRESW)
    # two due blink nodes both advance in one tick (bounds 1650/1710)
    cs["t-multi-blink"] = dict(
        steps=[(TICK, 0)], clock=1710,
        list=[0, 1],
        nodes={0: dict(state=2, stamp=0, handle=0xA0),
               1: dict(state=4, stamp=0, handle=0xA1)},
        watch=POOLW + PRESW)
    # state-1 node whose handle is 0 -> FA730 flag read faults
    cs["t-s1-handle0"] = dict(
        steps=[(TICK, 0)], clock=1000,
        list=[2], nodes={2: dict(state=1, handle=0)},
        objects=OBJRDY, watch=POOLW)
    # ---- COLLECT / REMOVE ----
    cs["g-collect"] = dict(
        steps=[(COLLECT, POOL + 0x60, 0x777)],
        list=[0, 1, 2],
        nodes={0: dict(state=3, stamp=5, handle=0xA0),
               1: dict(state=3, stamp=5, handle=0xA1,
                       drops=DROPS3),
               2: dict(state=3, stamp=5, handle=0xA2)},
        pres={1: (1, (0.0, 0.0, 0.0, 0.0))},
        watch=POOLW + PRESW + [(CNT_G, 4)])
    cs["g-collect-all7"] = dict(
        steps=[(COLLECT, POOL, 0)],
        list=[0],
        nodes={0: dict(state=3, stamp=5, handle=0xA0,
                       drops=[(0x11, 1), (0x22, 2), (0x33, 3),
                              (0x44, 4), (0x55, 5), (0x66, 6),
                              (0x77, 7)])},
        watch=POOLW + [(CNT_G, 4)])
    cs["g-collect-empty"] = dict(
        steps=[(COLLECT, POOL, 0)],
        list=[0],
        nodes={0: dict(state=3, stamp=5, handle=0xA0,
                       drops=[(0xFFFF, 9)])},
        watch=POOLW + [(CNT_G, 4)])
    # collect the head — head global updated, list shrinks
    cs["g-collect-head"] = dict(
        steps=[(COLLECT, POOL, 0)],
        list=[0, 1],
        nodes={0: dict(state=3, stamp=5, handle=0xA0,
                       drops=[(0xAAAA, 1)]),
               1: dict(state=3, stamp=5, handle=0xA1)},
        watch=POOLW)
    cs["g-remove"] = dict(
        steps=[(REMOVE, POOL + 0x60, 0x999)],
        list=[0, 1, 2],
        nodes={0: dict(state=3, stamp=5, handle=0xA0),
               1: dict(state=3, stamp=5, handle=0xA1,
                       drops=DROPS3),
               2: dict(state=3, stamp=5, handle=0xA2)},
        pres={1: (1, (0.0, 0.0, 0.0, 0.0))},
        watch=POOLW + PRESW + [(CNT_G, 4)])
    cs["g-remove-tail"] = dict(
        steps=[(REMOVE, POOL + 2 * 0x60, 0)],
        list=[0, 1, 2],
        nodes={0: dict(state=3, stamp=5, handle=0xA0),
               1: dict(state=3, stamp=5, handle=0xA1),
               2: dict(state=3, stamp=5, handle=0xA2)},
        watch=POOLW)
    # ---- wrappers ----
    cs["w-collect2"] = dict(
        steps=[(CWRAP, 2, 0x555)],
        list=[2],
        nodes={2: dict(state=3, stamp=5, handle=0xA2,
                       drops=[(0xBEEF, 3), (0xFFFF, 0)])},
        watch=POOLW + [(CNT_G, 4)])
    cs["w-remove0"] = dict(
        steps=[(RWRAP, 0, 0x555)],
        list=[0],
        nodes={0: dict(state=3, stamp=5, handle=0xA0)},
        watch=POOLW)
    # idx 10: node = the HEAD global address — no bounds check;
    # documented UB edge (reads drops from the head/tail cells)
    cs["w-idx10"] = dict(
        steps=[(CWRAP, 10, 0)],
        list=[0],
        nodes={0: dict(state=3, stamp=5, handle=0xA0)},
        watch=POOLW + [(CNT_G, 4)])
    # negative idx: pool-0x60 — phantom node, still grants id 0
    cs["w-negidx"] = dict(
        steps=[(CWRAP, -1, 0)],
        list=[0],
        nodes={0: dict(state=3, stamp=5, handle=0xA0)},
        watch=POOLW + [(CNT_G, 4), (POOL - 0x60, 0x60)])
    # ---- direct bodies ----
    cs["d-fb2a0-ok"] = dict(steps=[(FB2A0, 3)],
                            pres={3: (1, (0.0,) * 4)}, watch=PRESW)
    cs["d-fb2a0-9"] = dict(steps=[(FB2A0, 9)],
                           pres={9: (1, (0.0,) * 4)}, watch=PRESW)
    cs["d-fb2a0-10"] = dict(steps=[(FB2A0, 10)],
                            pres={9: (1, (0.0,) * 4)}, watch=PRESW)
    cs["d-fb2d0-free"] = dict(steps=[(FB2D0, 4, POSP)],
                              pos=(7.0, 8.0, 9.0), watch=PRESW)
    cs["d-fb2d0-occ"] = dict(steps=[(FB2D0, 4, POSP)],
                             pos=(7.0, 8.0, 9.0),
                             pres={4: (1, (1.0,) * 4)}, watch=PRESW)
    cs["d-efe0-hit"] = dict(steps=[(EFE0, OBJ)], objects=OBJRDY)
    cs["d-efe0-miss"] = dict(
        steps=[(EFE0, OBJ)],
        objects={OBJ: dict(oflag=1, ostate=2, onlist=False),
                 OBJ2: dict(oflag=1, ostate=2, onlist=True)})
    cs["d-efe0-noflag"] = dict(
        steps=[(EFE0, OBJ)],
        objects={OBJ: dict(oflag=0, ostate=2, onlist=True)})
    # list walk past one node: OBJ behind OBJ2 in the chain
    cs["d-efe0-deep"] = dict(
        steps=[(EFE0, OBJ)],
        objects={OBJ: dict(oflag=1, ostate=2, onlist=False),
                 OBJ2: dict(oflag=1, ostate=2, onlist=True,
                            onext=OBJ)})
    cs["d-efc0"] = dict(steps=[(EFC0, OBJ, POSP)], objects=OBJRDY,
                        watch=[(POSP, 16)])
    cs["d-rare-2"] = dict(steps=[(RARE, DROP)],
                          drops=[(0x0101, 1), (0xFFFF, 0)])
    cs["d-rare-0"] = dict(steps=[(RARE, DROP)],
                          drops=[(0x1002, 1)], itab={0x1002: 0x10})
    cs["d-tier-13"] = dict(steps=[(TIER, IROWS + 0x20)],
                           itab={0x1001: 0x13})
    cs["d-tier-1a"] = dict(steps=[(TIER, IROWS + 0x20)],
                           itab={0x1001: 0x1A})
    cs["d-tier-1b"] = dict(steps=[(TIER, IROWS + 0x20)],
                           itab={0x1001: 0x1B})
    # dispatcher direct
    cs["d-pres-op0"] = dict(steps=[(PRES, 0xAB, 0, POSP)])
    cs["d-pres-op7"] = dict(steps=[(PRES, 0xAB, 7, POSP)])
    cs["d-pres-nullmgr"] = dict(steps=[(PRES, 0xAB, 3, POSP)], mgr=0)
    cs["d-pres-op2"] = dict(steps=[(PRES, 0xAB, 2, POSP)])
    cs["d-pres-op6"] = dict(steps=[(PRES, 0xAB, 6, POSP)])
    cs["d-decode"] = dict(steps=[(DECODE, 0x1234)])
    # ---- lifecycle integration ----
    # dirty init -> create (op1 plants handle OBJ) -> tick @clk 100:
    # s1->s2 transition + presence publish, all native
    cs["life"] = dict(
        steps=[(INIT, 0), (CREATE, DROP, POSP), (TICK, 0)],
        dirty=True,
        drops=DROPS3, pos=(5.0, 6.0, 7.0),
        objects=OBJRDY, clock=100,
        watch=POOLW + PRESW)
    return cs


# ---------------- mutations (verified byte-precise) ----------------
# (name, case, addr, orig_byte, mut_byte) — orig asserted vs image
MUTS = [
    # INIT
    ("i-slot1",     "d-init",    0x319B18, 0x01, 0x02),   # node1 idx
    # CREATE
    ("c-stride",    "c-create2", 0x319CCF, 0x60, 0x61),   # add rbx,0x60
    ("c-scanbound", "c-fill10",  0x319CD2, 0x0A, 0x09),   # cmp eax,0xA
    ("c-scanoff",   "c-midfree", 0x319CC7, 0x04, 0x05),   # d[rbx+4]->+5
    ("c-found-je",  "c-create1", 0x319CC8, 0x74, 0x75),   # je->jne
    ("c-ev-prevje", "c-evict",   0x319CEE, 0x74, 0x75),   # prev null je
    ("c-ev-nextje", "c-evict",   0x319D08, 0x74, 0x75),   # next null je
    ("c-ev-op5",    "c-evict",   0x319D20, 0x05, 0x06),   # op5->op6
    ("c-ev-handle", "c-evict",   0x319D19, 0x58, 0x59),   # d[rbx+0x58]
    ("c-state1",    "c-create1", 0x319D99, 0x01, 0x02),   # state=1 -> 2
    ("c-tailnull",  "c-create1", 0x319D49, 0x74, 0x75),   # tail null je
    ("c-drop-sd",   "c-rare7th", 0x319D95, 0x50, 0x51),   # movsd +0x50
    ("c-op1",       "c-create1", 0x319DFA, 0x01, 0x02),   # op1 -> op2
    ("c-gidx-cmp",  "c-tvalidx", 0x319DDD, 0x03, 0x02),   # cmp eax,3
    ("c-gate-jle",  "c-gate",    0x319E0E, 0x7E, 0x7F),   # jle->jg
    ("c-rare-mask", "c-rare6",   0x319A6E, 0xF0, 0xE0),   # and 0xF000
    ("c-rare-1k",   "c-rare6",   0x319A73, 0x10, 0x20),   # cmp 0x1000
    ("c-rare-cnt",  "c-rare7th", 0x319ADB, 0x07, 0x06),   # cmp rdi,7
    ("c-rare-cme",  "c-rare7th", 0x319AD3, 0x44, 0x45),   # cmove->cmovne
    ("c-rare-jle",  "c-rare6",   0x319ACC, 0x7E, 0x7F),   # jle->jg
    ("c-rare-ebp",  "c-rare2",   0x319A46, 0x02, 0x03),   # ebp=2
    # TICK
    ("t-head-je",   "t-empty",   0x319620, 0x84, 0x85),   # je->jne
    ("t-s1-cmp",    "t-s1-ready", 0x319645, 0x01, 0x02),  # cmp edx,1
    ("t-s1-jle",    "t-state0",  0x31964D, 0x8E, 0x8D),   # jle->jge
    ("t-blink-cmp", "t-blink6",  0x319654, 0x06, 0x05),   # cmp edx,6
    ("t-des-cmp",   "t-despawn", 0x31965D, 0x07, 0x06),   # cmp edx,7
    ("t-step-3c",   "t-despawn-1", 0x319676, 0x3C, 0x3B), # imul 0x3C
    ("t-des-jb",    "t-despawn", 0x319683, 0x82, 0x83),   # jb->jae
    ("t-blink-3c",  "t-blink2-1", 0x3196FF, 0x3C, 0x3B),  # mov eax,0x3C
    ("t-blink-7",   "t-blink2",  0x3196F3, 0x07, 0x06),   # r8d=7
    ("t-blink-jb",  "t-blink2-1", 0x319718, 0x72, 0x73),  # jb->jae
    ("t-blink-op2", "t-blink2",  0x319726, 0x02, 0x03),   # op2 -> op3
    ("t-des-op4",   "t-despawn", 0x3196C5, 0x04, 0x02),   # op4 -> op2
    ("t-ready-cmp", "t-s1-ready", 0x319743, 0x02, 0x03),  # cmp eax,2
    ("t-stamp-off", "t-s1-ready", 0x319756, 0x08, 0x10),  # [rbx+8]->+10
    ("t-adv-off",   "t-multi-blink", 0x31977D, 0x18, 0x10), # +18->+10
    # COLLECT
    ("g-cnt7",      "g-collect-all7", 0x319944, 0x07, 0x06), # esi=7
    ("g-sentinel",  "g-collect",  0x31994A, 0xFF, 0xFE),  # r14d=0xFFFF
    ("g-sent-je",   "g-collect",  0x319958, 0x74, 0x75),  # je->jne
    ("g-cnt-inc",   "g-collect",  0x319975, 0x05, 0x0D),  # inc->dec
    ("g-op3",       "g-collect",  0x3199B7, 0x03, 0x02),  # op3 -> op2
    ("g-pay-store", "g-collect",  0x3199BE, 0x20, 0x24),  # [rsp+0x20]
    # REMOVE
    ("r-op3",       "g-remove",   0x3197FA, 0x03, 0x02),  # op3 -> op2
    ("r-prev-je",   "g-remove",   0x3197C4, 0x74, 0x75),  # prev null je
    # wrappers
    ("w-shl5",      "w-collect2", 0x319A0A, 0x05, 0x06),  # shl rcx,5
    # PRES dispatcher
    ("p-opbound",   "d-pres-op6", 0x28F01C, 0x05, 0x04),  # cmp eax,5
    ("p-opbase",    "d-pres-op2", 0x28F019, 0xFF, 0xFE),  # lea -1 -> -2
    ("p-nullmgr",   "d-pres-nullmgr", 0x28F015, 0x74, 0x75),  # je->jne
    # FB2A0 / FB2D0
    ("f2a0-bound",  "d-fb2a0-9",  0x2FB2A2, 0x09, 0x08),  # cmp ecx,9
    ("f2a0-imm",    "g-remove",   0x2FB2B6, 0x00, 0x01),  # store 0 -> 1
    ("f2d0-cmp1",   "t-s1-ready", 0x2FB2E6, 0x01, 0x00),  # cmp byte,1
    ("f2d0-off10",  "t-s1-ready", 0x2FB2F7, 0x10, 0x11),  # entry+0x10
    # FA730 ready leaf
    ("fa-flag",     "t-s1-ready", 0x3FA736, 0x01, 0x02),  # test &1
    ("fa-match-je", "d-efe0-hit", 0x3FA748, 0x74, 0x75),  # je->jne
    ("fa-ret-off",  "t-s1-ready", 0x3FA75B, 0x60, 0x61),  # d[rdx+0x260]
    # TIER
    ("tier-bound",  "d-tier-1a",  0x31E9F6, 0x1A, 0x19),  # cmp 0x1A
    # DECODE
    ("dec-add",     "d-decode",   0x20E602, 0x48, 0x4C),  # REX add
]


def differs(a, b):
    for k in ("trace", "rets", "ends", "faults", "mem"):
        if a[k] != b[k]:
            return "%s: %s != %s" % (k, a[k], b[k])
    return None


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    native = w.obs()
    model = run_model(case, raw, secs)
    return native, model, differs(native, model)


def main():
    raw, secs = load_image()
    cs = cases()
    fails = {}
    for name in sorted(cs):
        native, model, diff = run_case(name, cs[name], raw, secs)
        if diff:
            fails[name] = diff
    print("functional: %d/%d" % (len(cs) - len(fails), len(cs)))
    for name, diff in sorted(fails.items()):
        print("  FAIL %s: %s" % (name, diff))
    mkilled, msurv = [], []
    for mname, cname, addr, orig, mut in MUTS:
        base = dict(cs[cname])
        ob = img_rd(raw, secs, addr, 1)[0]
        assert ob == orig, \
            "%s: byte %x is %02x not %02x" % (mname, addr, ob, orig)
        base["patch_bytes"] = base.get("patch_bytes", []) + \
            [(addr, bytes([mut]))]
        native, model, diff = run_case(mname, base, raw, secs)
        if diff:
            mkilled.append(mname)
        else:
            msurv.append(mname)
    print("mutants: %d/%d killed" % (len(mkilled), len(MUTS)))
    for mname in msurv:
        print("  SURVIVED %s" % mname)
    res = {"functional_total": len(cs),
           "functional_pass": len(cs) - len(fails),
           "functional_fail": sorted(fails),
           "mutants_total": len(MUTS),
           "mutants_killed": len(mkilled),
           "mutants_survived": msurv}
    with open(RESULT, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
    sys.exit(1 if (fails or msurv) else 0)


if __name__ == "__main__":
    main()
