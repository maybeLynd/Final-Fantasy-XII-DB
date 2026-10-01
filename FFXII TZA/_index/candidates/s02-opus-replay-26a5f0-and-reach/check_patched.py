# EXP-191: S-02 runtime — world tick 00314020 + system-stop registry
# executed as shipped bytes (NATIVE-REPLAY, live_game: false).
# Contracts: CONTRACT-world-simulation-tick.md (WT-1..WT-6),
# CONTRACT-system-stop-registry.md (SS-1..SS-7).
#
#   00226B30 init (leaf, real): dirty=0, byte571=0, bitset=0;
#     rax walks 01FD4160 x28 per pass writing q0=-1, b[+0x14]=0;
#     rdx walks 01FD46B4..01FD46E4 by 0x18 (2 passes) writing
#     q[-0x14]=-1 (combined q0), d[-4]=-1 (dword10), b[+0]=0.
#   00225CD0 start (real): ecx=idx, edx=fade. edi=1<<idx;
#     b[01FD46D0]=1 dirty; d[01FD46D4] &= ~edi (clears pending bit);
#     3-manager x actor fan-out: 263FF0(i)=0208E688+i*0x288 slot,
#     b[obj+0x10]&1 gate, rows w[+0x1DE]..+w[+0x1D6] via 358940
#     (q[obj+8] ptr array, d[arr] bound, q[arr+8+i*8]=row);
#     per row: 359B80(row)->q[row+0x30] (0 planted -> rax=0 arm
#     skips); or d[row+0x114]|=edi, and d[row+0x110]&=~edi;
#     q[row+0xC0] chain x3: or +0x178/+0x16C/+0x160, and +0x174/0x168/
#     0x15C; rax!=0 arm: or rax+0x60/+0x58/+0x5C, and +0x54/+0x4C/0x50.
#     Then q[recA]=-1, q[recB]=-1, b[+0x14]=0 both, d[recB+0x10]=fade;
#     idx dispatch: 0->2DDC30?(182DA0), 0xC->182D60, 0xD->mask bank B
#     q0 &= ~bit41 then 182D40, else>2 -> 182D40.
#   00225EB0 stop-sweep (real): ecx loops 0..27 via d[rsp+0x50];
#     edi=1<<i (rol edi,1); test d[01FD46D4] -> if set: dirty=1,
#     clear bit, same actor fan-out, rec[i] reset q0=-1/bankB=-1/
#     b14=0/bankB-dword10=-1, same idx msg dispatch.
#   00226280 apply (real): gate b[01FD46D0]!=0 else ret.
#     r9=01FD46B0 bound; rax walks 01FD4410 (bank B) by 0x18:
#     r8=q[B], rdi&=q[B-0x2B0] (bank A), rbx&=r8; edx=d[B+0x10] fade:
#     >=0 -> ecx=min(ecx,edx) (init ecx=-1); d[B+0x10]=-1 consumed;
#     r8|=bit41 -> q[B] written back (SS-5). Then bit tests on
#     rdi/rbx build r14w/bp mask words (0x3FF/0x3EE, or 0x76, or 2,
#     or 0x108, special 0x10C/4), w[0209215D]=r14w, w[0209215B]=bp;
#     effector calls 2E24C0/2E24E0 (bit39), 2EA8B0/2EA8E0 (bit24->edx),
#     25A5D0 (bit30->ecx), 226640 (ecx=bits8..D all-set?1:0, edx=min
#     fade, r8d=0), 2547C0/254840 (u16 masks), 35B4B0/35B510 (bit29->
#     cl=5/0xFF), 2DF370 x3 + 2DF640 x2 (bits 32/33/35/40/44 gated
#     msgs), 2EBBF0 (bit35>>35&1). b[01FD46D1]==0 -> fade block else
#     clears byte571. Tail: movups combined[0]=rbx, movsd
#     d[+8]=fade... writes 01FD46A0..01FD46C7, dirty=0.
#   00314410 latch (real): d[01EED060]<0 -> 26A5F0(4) scripted then
#     d[01EED060]=arg; >=0 -> no store (first-writer-wins).
#   0025BFB0 drain (real): mask d[02099ABC]; loop1 bits 4..0 ->
#     26CE60(idx); clears xmm cells 0209A1F0/0209A200; loop2 bits
#     0x10,8,4,2,1 -> 2628B0(idx) + mask &= ~bit.
#   00314020 tick (real): ecx=mode r14d, edx=r12d.
#     d[022C2548]=1 (TIP); 16D6A0/3EB9A0/3DAA20; xmm7=f[020DABB8];
#     3DA2F0/3DD210(xmm7); 25BFB0 drain (WT-2 before mode consult);
#     eax=d[01EED060] -> cmovns -1 -> store (consume WT-4);
#     d[01EED064]>=0 -> 17D280 x2 + 32FC30(edx=that,ecx=0) +
#     d[01EED064]=-1; 3DAA40; 46AFA0;
#     mode==0 -> 358C60; r15b=(mode==0); 268650/25D650/255810/37D890/
#     25D640; ebp=3; mode==1 -> slots ebx=3,4: 234590/25D9E0/3DB1F0/
#     234520 + 2E0D90; mode==0 -> 3DF760(edx=1..5) x5, then outer
#     esi=0..15: inner ebx=0..4 267310 gate -> 234590/25D9E0/234520;
#     second inner 3DB1F0; esi==0 -> 2E0D90/268D00;
#     inc d[022C252D]; inc d[022C2531]; 3DAC70(rcx=fmt 03140CF?);
#     mode!=0&&mode==1 -> 2623A0 slots 3,4; mode==0 -> 2623A0 0..4;
#     358EE0(mode); 2E09A0/359800/3DE640/2E0940/37C1A0/3E7EC0/228480;
#     eax!=0 -> skip 36FD90(0); 2F1770(mode,r12d); 2EF910/36E1E0/
#     3DEB30/3DF670/3606E0/362850/362DA0; eax!=0 -> skip
#     362DB0/xmm6/265760/259AF0 chain + minss -> 361700;
#     3E7650/25D950/263660/2EEEB0; d[022C2548]=0; ret eax=r15d.
#
#   Scripted boundaries (entry-intercepted, args recorded, disclosed):
#   all effector/message callees — 2E24C0/2E24E0/2EA8B0/2EA8E0/
#   25A5D0/226640/2547C0/254840/35B4B0/35B510/2DF370/2DF640/2EBBF0/
#   182D60/182D40/182DA0/2DDC30/26A5F0/26CE60/2628B0 + the tick's
#   subsystem callees (all traced, default ret 0; 267310 gate +
#   228480/362DA0/2DDC30 rets case-controlled).
#
import hashlib
import json
import os
import struct
import sys

from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO = 0x120000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)


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
    def __init__(self, uc, raw, secs):
        self.uc = uc
        for va, vs, ra, rs in secs:
            lo = (va + IMG_LO) & ~0xFFF
            hi = (va + IMG_LO + max(vs, rs) + 0xFFF) & ~0xFFF
            uc.mem_map(lo, hi - lo)
            if rs:
                uc.mem_write(va + IMG_LO, raw[ra:ra + rs])

    def w(self, addr, data):
        if isinstance(data, int):
            data = qw(data)
        try:
            self.uc.mem_write(addr, bytes(data))
        except UcError:
            lo = addr & ~0xFFF
            self.uc.mem_map(lo, 0x1000)
            self.uc.mem_write(addr, bytes(data))

    def q(self, a):
        return struct.unpack("<Q", bytes(self.uc.mem_read(a, 8)))[0]

    def d(self, a):
        return struct.unpack("<I", bytes(self.uc.mem_read(a, 4)))[0]

    def w16(self, a):
        return struct.unpack("<H", bytes(self.uc.mem_read(a, 2)))[0]

    def b(self, a):
        return self.uc.mem_read(a, 1)[0]

    def f(self, a):
        return struct.unpack("<f", bytes(self.uc.mem_read(a, 4)))[0]


# ---- registry statics ----
REG   = 0x01FD4160            # SystemStopRegistry base
RECB  = REG + 0x2A0           # bank B
COMB  = REG + 0x540           # combined[2]
DIRTY = REG + 0x570           # u8 dirty
B571  = REG + 0x571           # u8 byte571
BITS  = REG + 0x574           # u32 activeRequestBits
# ---- tick statics ----
LATCH = 0x01EED060            # latched request (first-writer-wins)
DEFER = 0x01EED064            # deferred mode request
TIP   = 0x022C2548            # tick-in-progress
CNT1  = 0x022C252D            # inc counters (observed)
CNT2  = 0x022C2531
DRAINM = 0x02099ABC           # manager request mask
DRAIN0 = 0x0209A1F0           # cleared cells
DRAIN1 = 0x0209A200
SLOTS = 0x02098E10            # manager slot array, stride 0x288
# (263FF0: movsxd/imul 0x288/add 02098E10 -- verified 2025-*)


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.uc.mem_map(STACK, 0x100000)
        self.uc.mem_map(RETQ, 0x1000)
        self.uc.mem_map(HEAP, 0x600000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP
        self.entry = 0
        gm = self.gm

        # ---- statics ----
        gm.w(BITS, dw(case.get("bitset", 0)))
        gm.w(DIRTY, bytes([case.get("dirty", 0) & 0xFF]))
        gm.w(B571, bytes([case.get("byte571", 0) & 0xFF]))
        gm.w(LATCH, dw(case.get("latch", -1)))
        gm.w(DEFER, dw(case.get("defer", -1)))
        gm.w(TIP, dw(0))
        gm.w(DRAINM, dw(case.get("drainm", 0)))
        for _a, _v in case.get("pokes", {}).items():   # OPUS block 263 patch
            gm.w(_a, _v)
        gm.w(DRAIN0, b"\xAA" * 16)
        gm.w(DRAIN1, b"\xBB" * 16)
        gm.w(0x02089340, dw(case.get("flagword", 0)))
        gm.w(0x02099D70, qw(0))
        gm.w(0x02099D78, qw(0))
        # WT-6: 234520's one-shot callback cell 0208E6A8
        cb = case.get("slotcb")
        if cb:
            stub = self.alloc(0x10)
            gm.w(stub, b"\xc3")               # bare ret
            gm.w(0x0208E6A8, qw(stub))
        else:
            gm.w(0x0208E6A8, qw(0))

        # registry slots: bank A and bank B, per-slot mask + fade
        slots = case.get("slots", {})
        for i in range(28):
            spec = slots.get(i, {})
            a = spec.get("a", 0)
            b = spec.get("b", 0)
            gm.w(REG + i * 0x18, qw(a))
            gm.w(RECB + i * 0x18, qw(b))
            gm.w(REG + i * 0x18 + 0x10,
                 dw(spec.get("a10", -1)))
            gm.w(RECB + i * 0x18 + 0x10,
                 dw(spec.get("b10", -1)))
            gm.w(REG + i * 0x18 + 0x14,
                 bytes([spec.get("a14", 0) & 0xFF]))
            gm.w(RECB + i * 0x18 + 0x14,
                 bytes([spec.get("b14", 0) & 0xFF]))

        # ---- manager slot array: nman managers x nactor rows ----
        # slot obj at SLOTS+i*0x288: b[+0x10]&1 gate, w[+0x1DE] head,
        # w[+0x1D6] count; q[obj+8] ptr array {d bound, q rows};
        # d[+0x20] row count for 3DB1F0; b[+0x201] = 267310 gate flag;
        # b[+0x11]/+0x12/+0x13/+0x17 = 25D9E0 flag bytes.
        self.mrows = []
        self.objs = []
        nman = case.get("nmgr", 5)
        nactor = case.get("nactor", 1)
        sflags = case.get("slotflags", [1] * nman)
        for m in range(nman):
            obj = SLOTS + m * 0x288
            self.objs.append(obj)
            gm.w(obj + 0x10, bytes([case.get("mgate", 1)]))
            gm.w(obj + 0x11, bytes([case.get("ob11", 0)]))
            gm.w(obj + 0x12, bytes([case.get("ob12", 0)]))
            gm.w(obj + 0x13, bytes([case.get("ob13", 0)]))
            gm.w(obj + 0x17, bytes([case.get("ob17", 0)]))
            gm.w(obj + 0x1DE, struct.pack("<H", 0))
            gm.w(obj + 0x1D6, struct.pack("<H", nactor))
            gm.w(obj + 0x20, dw(case.get("rowcnt", nactor)))
            gm.w(obj + 0x201, bytes([sflags[m] if m < len(sflags) else 0]))
            arr = self.alloc(0x400)
            gm.w(obj + 8, qw(arr))
            gm.w(arr, dw(nactor))
            rows = []
            for a in range(nactor):
                row = self.alloc(0x200)
                gm.w(arr + 8 + a * 8, qw(row))
                # 359B80 path: q[row+0x30]==0 -> rax=0 arm
                gm.w(row + 0x30, qw(case.get("row30", 0)))
                # 3DB1F0 row fields: b[+0x63] flag, q[+0xA0] bin,
                # b[+0x89] count
                gm.w(row + 0x63, bytes([case.get("row63", 0)]))
                gm.w(row + 0x89, bytes([case.get("row89", 0)]))
                buf = case.get("rowa0", self.alloc(0x80))
                gm.w(row + 0xA0, qw(buf))
                row89 = case.get("row89", 0)
                if row89:
                    # inner scan: b[buf+0x11+k*0x14]==1 -> 2
                    for k in range(row89):
                        gm.w(buf + 0x11 + k * 0x14, b"")
                    self.rowbufs = getattr(self, "rowbufs", {})
                    self.rowbufs[row] = buf
                chain = self.alloc(0x200)
                gm.w(row + 0xC0, qw(chain))
                rows.append(row)
            self.mrows.append(rows)

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)
        if case.get("watch_bits"):
            self.bitreads = []
            self.uc.hook_add(UC_HOOK_MEM_READ, self.on_rd,
                             begin=BITS, end=BITS + 3)

    def on_rd(self, uc, access, addr, size, value, _):
        self.bitreads.append((addr, size,
                              uc.reg_read(UC_X86_REG_RIP)))

    def alloc(self, n):
        a = self.hb
        self.hb += (n + 0xFFF) & ~0xFFF
        return a

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def _args(self, tag):
        uc = self.uc
        self.rets.setdefault("calls", []).append(
            [tag,
             uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF])

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    # scripted boundaries: tag -> case retkey (0 default)
    SCR = {
        # apply effectors
        0x2E24C0: ("e24c0", None), 0x2E24E0: ("e24e0", None),
        0x2EA8B0: ("ea8b0", None), 0x2EA8E0: ("ea8e0", None),
        0x25A5D0: ("a5d0", None), 0x226640: ("m226640", None),
        0x2547C0: ("m2547c0", None), 0x254840: ("m254840", None),
        0x35B4B0: ("m35b4b0", None), 0x35B510: ("m35b510", None),
        0x2DF370: ("m2df370", None), 0x2DF640: ("m2df640", None),
        0x2EBBF0: ("m2ebbf0", None),
        # start/stop tail msgs
        0x182D60: ("m182d60", None), 0x182D40: ("m182d40", None),
        0x182DA0: ("m182da0", None), 0x2DDC30: ("g2ddc30", "g2ddc30_ret"),
        # latch + drain
        0x26A5F0: ("s26a5f0", None),
        0x26CE60: ("d26ce60", None), 0x2628B0: ("d2628b0", None),
        # tick callees
        0x16D6A0: ("t16d6a0", None), 0x3EB9A0: ("t3eb9a0", None),
        0x3DAA20: ("t3daa20", None), 0x3DA2F0: ("t3da2f0", None),
        0x3DD210: ("t3dd210", None), 0x17D280: ("t17d280", "allocx"),
        0x32FC30: ("t32fc30", None), 0x3DAA40: ("t3daa40", None),
        0x46AFA0: ("t46afa0", None), 0x358C60: ("t358c60", None),
        0x268650: ("t268650", None), 0x25D650: ("t25d650", None),
        0x255810: ("t255810", None), 0x37D890: ("t37d890", None),
        0x25D640: ("t25d640", None), 0x234590: ("t234590", None),
        0x25D9E0: ("t25d9e0", None), 0x3DB1F0: ("t3db1f0", None),
        0x234520: ("t234520", None), 0x2E0D90: ("t2e0d90", None),
        0x3DF760: ("t3df760", None), 0x267310: ("t267310", "t267310_ret"),
        0x268D00: ("t268d00", None), 0x2623A0: ("t2623a0", None),
        0x358EE0: ("t358ee0", None), 0x2E09A0: ("t2e09a0", None),
        0x359800: ("t359800", None), 0x3DE640: ("t3de640", None),
        0x2E0940: ("t2e0940", None), 0x37C1A0: ("t37c1a0", None),
        0x3E7EC0: ("t3e7ec0", None), 0x228480: ("t228480", "t228480_ret"),
        0x36FD90: ("t36fd90", None), 0x2F1770: ("t2f1770", None),
        0x2EF910: ("t2ef910", None), 0x36E1E0: ("t36e1e0", None),
        0x3DEB30: ("t3deb30", None), 0x3DF670: ("t3df670", None),
        0x3606E0: ("t3606e0", None), 0x362850: ("t362850", None),
        0x362DA0: ("t362da0", "t362da0_ret"),
        0x362DB0: ("t362db0", None), 0x265760: ("t265760", "t265760_ret"),
        0x259AF0: ("t259af0", None), 0x2DEBA0: ("t2deba0", None),
        0x361700: ("t361700", None), 0x3E7650: ("t3e7650", None),
        0x25D950: ("t25d950", None), 0x263660: ("t263660", None),
        0x2EEEB0: ("t2eeeb0", None), 0x3DAC70: ("t3dac70", None),
        # ---- WT-6 callee stubs: 234590 slot-0 chain ----
        0x32A150: ("w32a150", None), 0x32A100: ("w32a100", None),
        0x35C700: ("w35c700", None), 0x306BB0: ("w306bb0", None),
        0x2371B0: ("w2371b0", None), 0x237140: ("w237140", None),
        0x35C7A0: ("w35c7a0", None), 0x313A00: ("w313a00", None),
        0x30C0D0: ("w30c0d0", None), 0x30A880: ("w30a880", None),
        0x300140: ("w300140", None), 0x23B040: ("w23b040", None),
        0x32A650: ("w32a650", None), 0x3226C0: ("w3226c0", None),
        0x30CBE0: ("w30cbe0", None), 0x3065D0: ("w3065d0", None),
        0x325060: ("w325060", None), 0x307E70: ("w307e70", None),
        0x319600: ("w319600", None), 0x313760: ("w313760", None),
        0x304440: ("w304440", None), 0x307030: ("w307030", None),
        0x237260: ("w237260", None), 0x35C8A0: ("w35c8a0", None),
        0x35C8E0: ("w35c8e0", None), 0x3272A0: ("w3272a0", None),
        0x313F60: ("w313f60", None), 0x3137F0: ("w3137f0", None),
        0x31B770: ("w31b770", None), 0x3135C0: ("w3135c0", None),
        0x392740: ("w392740", None), 0x33B6D0: ("w33b6d0", None),
        0x383C80: ("w383c80", None), 0x3246C0: ("w3246c0", None),
        0x2F82F0: ("w2f82f0", None),
        # ---- 234520 chain ----
        0x313DB0: ("w313db0", None), 0x319090: ("w319090", None),
        # ---- 25D9E0 chain ----
        0x583920: ("w583920", None), 0x32F6E0: ("w32f6e0", None),
        0x3603C0: ("w3603c0", None), 0x25E400: ("w25e400", None),
        0x3590D0: ("w3590d0", None), 0x3588B0: ("w3588b0", None),
        0x377DB0: ("w377db0", None), 0x32F6C0: ("w32f6c0", None),
        0x25DF00: ("w25df00", None), 0x3DB280: ("w3db280", None),
        0x2620E0: ("w2620e0", None), 0x261F90: ("w261f90", None),
        0x3148F0: ("w3148f0", None), 0x2EF2B0: ("w2ef2b0", None),
        0x3EAA70: ("w3eaa70", None), 0x361010: ("w361010", None),
        0x37C8F0: ("w37c8f0", None), 0x37C860: ("w37c860", None),
        0x360D60: ("w360d60", None), 0x37CB40: ("w37cb40", None),
        0x269860: ("w269860", None), 0x233AA0: ("w233aa0", None),
        0x2F1A30: ("w2f1a30", None), 0x17E7D0: ("w17e7d0", None),
        0x363A80: ("w363a80", None), 0x3B7130: ("w3b7130", None),
        0x2EFD20: ("w2efd20", None), 0x2EFE40: ("w2efe40", None),
        0x2EFE50: ("w2efe50", None), 0x183070: ("w183070", None),
        0x2EFA70: ("w2efa70", None), 0x2677B0: ("w2677b0", None),
        0x268690: ("w268690", None), 0x3148D0: ("w3148d0", None),
        0x314DA0: ("w314da0", None), 0x2E1C40: ("w2e1c40", None),
        0x254A90: ("w254a90", None), 0x259FB0: ("w259fb0", None),
        0x234150: ("w234150", None), 0x250960: ("w250960", None),
        0x25B740: ("w25b740", None), 0x25C170: ("w25c170", None),
        0x25B250: ("w25b250", None), 0x25B820: ("w25b820", None),
        0x25B600: ("w25b600", None),
        # ---- 3DB1F0 chain ----
        0x3DB6E0: ("w3db6e0", None),
    }

    # executed bodies to trace
    REAL = {
        0x225CD0: "r25cd0", 0x225EB0: "r25eb0",
        0x226280: "r226280", 0x226B30: "r226b30",
        0x314410: "r314410", 0x25BFB0: "r25bfb0",
        0x314020: "r314020", 0x263FF0: "r263ff0",
        0x358940: "r358940", 0x359B80: "r359b80",
        0x00861EC0: "l861ec0",
        # WT-6 bodies (run real only in wt6 cases via realbodies,
        # else still stubbed — see on_code ordering)
        0x267310: "r267310", 0x234590: "r234590",
        0x234520: "r234520", 0x25D9E0: "r25d9e0",
        0x3DB1F0: "r3db1f0",
    }

    FN_STARTS = set(int(l.split('\t')[0], 16) for l in open(r'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv', encoding='utf-8', errors='replace') if l[:1] in '0123456789ABCDEF')

    def on_code(self, uc, addr, size, _):
        if addr in self.FN_STARTS and addr != self.entry:
            self.rets.setdefault('entered', []).append('%08X' % addr)
        if addr == self.entry:
            return
        rb = self.case.get("realbodies")
        if rb and addr in rb:
            self.trace.append(self.REAL.get(addr, hex(addr)))
            return
        if addr == 0x00861EC0:      # memset(rcx, dl, r8)
            dst = uc.reg_read(UC_X86_REG_RCX)
            cnt = uc.reg_read(UC_X86_REG_R8)
            uc.mem_write(dst, b"\0" * cnt)
            self.rets.setdefault("memsets", []).append(
                [dst & 0xFFFFFFFFFFFFFFFF, cnt & 0xFFFFFFFFFFFFFFFF])
            self.trace.append("memset")
            self._ret()
            return
        ent = self.SCR.get(addr)
        if ent is not None:
            tag, retkey = ent
            self._args(tag)
            self.trace.append(tag)
            if retkey == "allocx":
                uc.reg_write(UC_X86_REG_RAX, self.alloc(
                    uc.reg_read(UC_X86_REG_RCX)))
            else:
                uc.reg_write(UC_X86_REG_RAX,
                             self.case.get(retkey, 0)
                             if retkey else 0)
            self._ret()
            return
        t = self.REAL.get(addr)
        if t is not None:
            self.trace.append(t)
            return

    def run(self, rcx=0, edx=0, r8=0, r9=0):
        uc = self.uc
        self.entry = self.case.get("entry", 0x226280)
        rsp = STACK + 0x80000
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, edx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R8,
                     self.case.get("r8", r8) & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9,
                     self.case.get("r9", r9) & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(self.entry, RETQ, timeout=60_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


ALL1 = 0xFFFFFFFFFFFFFFFF


def bc(**kw):
    c = {}
    c.update(kw)
    return c


CASES = {
    # ---------- stop registry ----------
    "ss-init": bc(entry=0x226B30),
    "ss-start": bc(entry=0x225CD0, rcx=3, edx=0x1E,
                   bitset=(1 << 3)),
    "ss-start-idx0": bc(entry=0x225CD0, rcx=0, edx=0x40,
                        bitset=1),
    "ss-start-idxd": bc(entry=0x225CD0, rcx=0xD, edx=0x77,
                        bitset=(1 << 0xD)),
    "ss-stop": bc(entry=0x225EB0, bitset=(1 << 5) | (1 << 0xD)),
    "ss-stop-idle": bc(entry=0x225EB0, bitset=0),
    "ss-apply": bc(entry=0x226280, dirty=1, bitset=0,
                   slots={1: {"a": 0x0FF0FF00FF00FF00,
                              "b": 0x00FF00FF00FF00FF},
                          7: {"a": 0xFFFFFFFFFFFFFFFF,
                              "b": 0x0000000000000001,
                              "b10": 0x55},
                          9: {"a": 0xAAAAAAAAAAAAAAAA,
                              "b": 0x5555555555555555,
                              "b10": 0x30}}),
    "ss-apply-gated": bc(entry=0x226280, dirty=0,
                         slots={0: {"a": 0x1234, "b": 0x5678}}),
    "ss-apply-bits0": bc(entry=0x226280, dirty=1, bitset=0,
                         slots={0: {"a": 0x0F0F0F0F0F0F0F0F,
                                    "b": 0x3333333333333333}}),
    "ss-apply-bitsff": bc(entry=0x226280, dirty=1, bitset=0xFFFFFFFF,
                          slots={0: {"a": 0x0F0F0F0F0F0F0F0F,
                                     "b": 0x3333333333333333}}),
    "ss-apply-watch": bc(entry=0x226280, dirty=1, bitset=0xFFFFFFFF,
                         watch_bits=1,
                         slots={0: {"a": 0xFF, "b": 0xFF}}),
    "ss-apply-full": bc(entry=0x226280, dirty=1, bitset=0,
                        slots={i: {"a": ALL1, "b": ALL1}
                               for i in range(28)}),
    "ss-apply-571": bc(entry=0x226280, dirty=1, byte571=1,
                       slots={0: {"a": 0xFF, "b": 0xFF, "b10": 9}}),

    # ---------- latch + drain ----------
    "wt-latch-store": bc(entry=0x314410, rcx=9, latch=-1),
    "wt-latch-held": bc(entry=0x314410, rcx=9, latch=5),
    "wt-latch-store-real": bc(entry=0x314410, rcx=9, latch=-1, drainm=0x3,   # OPUS block 263 patch
                               realbodies={0x26A5F0},
                               pokes={0x0215F1A0: b"\x5A\xA5", 0x0215F1A4: b"\x11\x11\x11\x11",
                                      0x0215F1A8: b"\x22\x22\x22\x22"}),
    "wt-drain": bc(entry=0x25BFB0, drainm=0x11),
    "wt-drain-idle": bc(entry=0x25BFB0, drainm=0),

    # ---------- world tick ----------
    "wt-mode0": bc(entry=0x314020, rcx=0, edx=0),
    "wt-mode1": bc(entry=0x314020, rcx=1, edx=0),
    "wt-mode2": bc(entry=0x314020, rcx=2, edx=0),
    "wt-mode0-gated": bc(entry=0x314020, rcx=0, t267310_ret=1),
    "wt-latched": bc(entry=0x314020, rcx=0, latch=7),
    "wt-deferred": bc(entry=0x314020, rcx=0, defer=4),
    "wt-drain-live": bc(entry=0x314020, rcx=1, drainm=0x5),
    "wt-tail-branch": bc(entry=0x314020, rcx=0,
                         t228480_ret=1, t362da0_ret=1),

    # ---------- WT-6: per-slot bodies real ----------
    "wt6-gate-on": bc(entry=0x267310, rcx=2,
                      slotflags=[1, 1, 1, 1, 1]),
    "wt6-gate-off": bc(entry=0x267310, rcx=2,
                       slotflags=[1, 1, 0, 1, 1]),
    "wt6-234590-s0": bc(entry=0x234590, rcx=0),
    "wt6-234590-s3": bc(entry=0x234590, rcx=3),
    "wt6-234520-s0": bc(entry=0x234520, rcx=0,
                       flagword=1, slotcb=1),
    "wt6-234520-s3": bc(entry=0x234520, rcx=3,
                       flagword=1, slotcb=1),
    "wt6-25d9e0-s0": bc(entry=0x25D9E0, rcx=0),
    "wt6-25d9e0-s3": bc(entry=0x25D9E0, rcx=3),
    "wt6-3db1f0-s2": bc(entry=0x3DB1F0, rcx=2, row63=4, row89=2),
    "wt6-3db1f0-idle": bc(entry=0x3DB1F0, rcx=2, row63=0),
    # full tick with the slot bodies real: gate flags all 1 so
    # 267310 passes; flagword=1 + slotcb arms 234520's callback
    "wt-mode0-wt6": bc(entry=0x314020, rcx=0,
                      flagword=1, slotcb=1,
                      slotflags=[1] * 5,
                      realbodies={0x267310, 0x234590, 0x234520,
                                  0x25D9E0, 0x3DB1F0}),
}

# OPUS block 266 patch: SS-7 per-request record template 00227680 (stub-free leaf), ids 0..27
for _id in range(28):
    CASES["ss-record-id-%02d" % _id] = bc(entry=0x227680, rcx=_id, edx=REG + _id * 0x18,
                                         r8=REG + 0x2A0 + _id * 0x18, r9=0)


def main():
    raw, secs = load_image()
    res = {}
    for name, case in CASES.items():
        w = World(case, raw, secs)
        eax = w.run(rcx=case.get("rcx", 0), edx=case.get("edx", 0))
        gm = w.gm
        ok = True
        notes = []

        def ck(cond, msg):
            nonlocal ok
            if not cond:
                ok = False
                notes.append(msg)

        exp_fault = case.get("expect_fault")
        if exp_fault:
            ck(any(f[-1] == exp_fault for f in w.faults),
               f"expected fault@{exp_fault:07X} got {w.faults}")
        else:
            ck(not w.faults, f"unexpected fault {w.faults}")

        calls = w.rets.get("calls", [])

        if name == "ss-init":
            ck(w.faults == [], "faults")
            bad = [i for i in range(56)
                   if gm.q(REG + i * 0x18) != ALL1
                   or gm.b(REG + i * 0x18 + 0x14) != 0]
            ck(not bad, f"records not reset {bad[:4]}")
            ck(gm.q(COMB) == ALL1, "comb0 q0")
            ck(gm.d(COMB + 0x10) == 0xFFFFFFFF, "comb0 d10")
            ck(gm.b(COMB + 0x14) == 0, "comb0 b14")
            ck(gm.q(COMB + 0x18) == ALL1, "comb1 q0")
            ck(gm.d(COMB + 0x28) == 0xFFFFFFFF, "comb1 d10")
            ck(gm.b(COMB + 0x2C) == 0, "comb1 b14")
            ck(gm.b(DIRTY) == 0, "dirty")
            ck(gm.b(B571) == 0, "b571")
            ck(gm.d(BITS) == 0, "bits")

        elif name.startswith("ss-record-id-"):   # OPUS block 266 patch: measurement, no prediction
            _i = case["rcx"]
            _a = gm.q(REG + _i * 0x18)
            _b = gm.q(REG + 0x2A0 + _i * 0x18)
            _reach = ((~(_a >> 30)) & 2) | 1
            notes.append("id=%d A=%016X B=%016X reach=%d" % (_i, _a, _b, _reach))
            notes.append("calls=%s" % [x[0] for x in calls])
            notes.append("entered=%s" % sorted(set(w.rets.get("entered", []))))

        elif name.startswith("ss-start"):
            idx = case["rcx"]
            ck(w.faults == [], "faults")
            ck(gm.b(DIRTY) == 1, "dirty set")
            ck(gm.d(BITS) & (1 << idx) == 0, "bit cleared")
            ck(gm.q(REG + idx * 0x18) == ALL1, "recA q0")
            # idx 0xD clears bit41 of bank-B q0 on top of the -1 write
            expb = 0xFFFFFDFFFFFFFFFF if idx == 0xD else ALL1
            ck(gm.q(RECB + idx * 0x18) == expb, "recB q0")
            ck(gm.b(REG + idx * 0x18 + 0x14) == 0, "b14 A")
            ck(gm.b(RECB + idx * 0x18 + 0x14) == 0, "b14 B")
            ck(gm.d(RECB + idx * 0x18 + 0x10) == case["edx"],
               "fade stored")
            # actor fan-out: row bits or'd / and'd
            for m, rows in enumerate(w.mrows[:3]):
                for r in rows:
                    ck(gm.d(r + 0x114) & (1 << idx), "row or 114")
                    ck(gm.d(r + 0x110) & (1 << idx) == 0, "row and 110")
            # idx dispatch
            tags = [c[0] for c in calls]
            if idx == 0:
                ck("g2ddc30" in tags, "idx0 gate call")
                ck("m182da0" in tags, "idx0 msg")
            elif idx == 0xD:
                ck("m182d40" in tags, "idxD msg")
            else:
                ck(not any(t.startswith("m182") for t in tags),
                   f"unexpected msg {tags}")

        elif name == "ss-stop":
            ck(w.faults == [], "faults")
            ck(gm.b(DIRTY) == 1, "dirty")
            ck(gm.d(BITS) == 0, "bits cleared")
            for i in (5, 0xD):
                ck(gm.q(REG + i * 0x18) == ALL1, f"recA{i} q0")
                expb = 0xFFFFFDFFFFFFFFFF if i == 0xD else ALL1
                ck(gm.q(RECB + i * 0x18) == expb, f"recB{i} q0")
                ck(gm.d(RECB + i * 0x18 + 0x10) == 0xFFFFFFFF,
                   f"recB{i} d10")
            tags = [c[0] for c in calls]
            ck("m182d40" in tags, "idxD msg fired")

        elif name == "ss-stop-idle":
            ck(w.faults == [], "faults")
            ck(gm.b(DIRTY) == 0, "dirty untouched")
            ck(not w.rets.get("calls"), "no calls")
            ck(gm.q(REG) == 0, "no record writes")

        elif name.startswith("ss-apply"):
            ck(w.faults == [], "faults")
            if name == "ss-apply-full":
                # all masks ~0 -> both combined banks stay ~0
                ck(gm.q(COMB) == ALL1, f"combA {gm.q(COMB):#x}")
                ck(gm.q(COMB + 0x18) == ALL1, "combB")
                m = [c for c in calls if c[0] == "m226640"]
                ck(m and m[0][1] == 1, f"bits8-D flag {m}")
            elif name == "ss-apply-gated":
                ck(not calls, f"gated calls {calls}")
                ck(gm.q(COMB) == 0, "no combined write")
                ck(gm.b(DIRTY) == 0, "dirty stays 0")
            else:
                comb = gm.q(COMB)
                combd10 = gm.d(COMB + 0x10)
                if name in ("ss-apply",):
                    # unplanted slots AND to 0 -> combined masks 0
                    ck(comb == 0, f"combined {comb:#x}")
                    ck(gm.q(RECB + 7 * 0x18) ==
                       (0x0000000000000001 | (1 << 41)), "bit41 or")
                    ck(gm.d(RECB + 7 * 0x18 + 0x10) == 0xFFFFFFFF,
                       "d10 consumed 7")
                    ck(gm.d(RECB + 9 * 0x18 + 0x10) == 0xFFFFFFFF,
                       "d10 consumed 9")
                    m = [c for c in calls if c[0] == "m226640"]
                    ck(m and m[0][2] == 0x30,
                       f"226640 fade arg {m}")
                if name in ("ss-apply-bits0", "ss-apply-bitsff"):
                    ck(comb == 0, f"combined {comb:#x}")
                    ck(gm.b(DIRTY) == 0, "dirty")
                    res.setdefault("BITSET_CMP", []).append(
                        [comb, combd10])
                if name == "ss-apply-watch":
                    ck(gm.b(DIRTY) == 0, "dirty")
                    ck(not w.bitreads,
                       f"bitset read by apply: {w.bitreads[:4]}")
                if name == "ss-apply-571":
                    ck(gm.b(DIRTY) == 0, "dirty")
                    ck(gm.b(B571) == 0, "byte571 cleared")
                    m = [c for c in calls if c[0] == "m226640"]
                    ck(m and m[0][2] == 9, f"fade via callee {m}")

        elif name == "wt-latch-store":
            ck(w.faults == [], "faults")
            ck(gm.d(LATCH) == 9, "latch stored")
            c = [x for x in calls if x[0] == "s26a5f0"]
            ck(c and c[0][1] == 4, "26A5F0(4) before store")

        elif name == "wt-latch-store-real":   # OPUS block 263 patch: 0026A5F0 run real
            ck(w.faults == [], "faults")
            ck(gm.d(LATCH) == 9, "latch stored")
            ck(gm.d(DRAINM) == (0x3 | 0x10), "mask |= 0x10 (26A5F0(4) real)")
            ck(gm.b(0x0215F1A0) == 0, "mailbox pending byte cleared")
            ck(gm.b(0x0215F1A1) == 1, "0215F1A1 set by 2E1690")
            ck(gm.d(0x0215F1A4) == 0, "mailbox arg A cleared")
            ck(gm.d(0x0215F1A8) == 0, "mailbox arg B cleared")
            ck(not [x for x in calls if x[0] == "s26a5f0"], "26A5F0 not scripted")

        elif name == "wt-latch-held":
            ck(w.faults == [], "faults")
            ck(gm.d(LATCH) == 5, "latch held (first-writer-wins)")
            ck(not [x for x in calls if x[0] == "s26a5f0"],
               "no 26A5F0 when nonneg")

        elif name in ("wt-drain", "wt-drain-idle"):
            ck(w.faults == [], "faults")
            tags = [c[0] for c in calls]
            if name == "wt-drain":
                c26 = [c for c in calls if c[0] == "d26ce60"]
                c28 = [c for c in calls if c[0] == "d2628b0"]
                # mask&1 gates 26CE60 pass (idx 4..0 for bitv 0x10..1);
                # 2628B0 pass always runs the same 5 bits + clears
                ck([c[1] for c in c26] == [4, 0], f"26CE60 idxs {c26}")
                ck([c[1] for c in c28] == [4, 0], f"2628B0 idxs {c28}")
                ck(gm.d(DRAINM) == 0, "mask cleared")
                ck(gm.q(DRAIN0) == 0, "cell0 zeroed")
                ck(gm.q(DRAIN1) == 0, "cell1 zeroed")
            else:
                ck(not calls, "idle calls")

        elif name in ("wt-mode0", "wt-mode1", "wt-mode2",
                      "wt-mode0-gated"):
            ck(w.faults == [], "faults")
            ck("r25bfb0" in w.trace, "drain ran")
            ck(gm.d(TIP) == 0, "TIP cleared")
            ck(gm.d(LATCH) == 0xFFFFFFFF, "latch consumed")
            tags = [c[0] for c in calls]
            n590 = tags.count("t234590")
            n9e0 = tags.count("t25d9e0")
            nb1f0 = tags.count("t3db1f0")
            n520 = tags.count("t234520")
            n23a0 = [c for c in calls if c[0] == "t2623a0"]
            nf760 = [c for c in calls if c[0] == "t3df760"]
            mode = case["rcx"]
            if mode == 0:
                ck("t358c60" in tags, "mode0 358C60")
                ck(len(nf760) == 5, f"3DF760 x5 {len(nf760)}")
                ck([c[2] for c in nf760] == [1, 2, 3, 4, 5],
                   "3DF760 edx 1..5")
                if case.get("t267310_ret"):
                    # 267310 nonzero -> run slot calls (gate inverted)
                    ck(n590 == 80, f"234590 x80 {n590}")
                    ck(nb1f0 == 80, f"3DB1F0 x80 {nb1f0}")
                else:
                    # ret 0 -> skip; substep0 always runs (5 calls)
                    ck(n590 == 5, f"234590 x5 {n590}")
                    ck(nb1f0 == 5, f"3DB1F0 x5 {nb1f0}")
                ck([c[1] for c in n23a0] == [0, 1, 2, 3, 4],
                   f"2623A0 slots {n23a0}")
            elif mode == 1:
                ck("t358c60" not in tags, "mode1 no 358C60")
                ck(not nf760, "mode1 no 3DF760")
                ck(n590 == 2, f"234590 x2 {n590}")
                ck([c[1] for c in n23a0] == [3, 4],
                   f"2623A0 slots {n23a0}")
            else:
                ck(not nf760 and n590 == 0, "mode2 skips")
                ck(not n23a0, "mode2 no 2623A0")
            tail = [c for c in calls if c[0] == "t358ee0"]
            ck(tail and tail[0][1] == mode, "358EE0(mode)")

        elif name == "wt-latched":
            ck(w.faults == [], "faults")
            ck(gm.d(LATCH) == 0xFFFFFFFF, "latch consumed")

        elif name == "wt-deferred":
            ck(w.faults == [], "faults")
            ck(gm.d(DEFER) == 0xFFFFFFFF, "defer cleared")
            c32 = [c for c in calls if c[0] == "t32fc30"]
            ck(c32 and c32[0][2] == 4, f"32FC30(edx=4) {c32}")
            a = [c for c in calls if c[0] == "t17d280"]
            ck(len(a) == 2, f"17D280 x2 {a}")

        elif name == "wt-drain-live":
            ck(w.faults == [], "faults")
            d = [c for c in calls if c[0] == "d2628b0"]
            ck(d and d[0][1] == 2, f"drain under mode1 {d}")
            ck(gm.d(DRAINM) == 0, "mask cleared in-tick")

        elif name == "wt-tail-branch":
            ck(w.faults == [], "faults")
            tags = [c[0] for c in calls]
            ck("t36fd90" not in tags, "36FD90 skipped (eax!=0)")
            ck("t362db0" not in tags, "362DB0 skipped (eax!=0)")

        elif name == "wt6-gate-on":
            ck(w.faults == [], "faults")
            ck(eax == 1, f"267310 flag {eax:#x}")

        elif name == "wt6-gate-off":
            ck(w.faults == [], "faults")
            ck(eax == 0, f"267310 flag {eax:#x}")

        elif name == "wt6-234590-s0":
            ck(w.faults == [], "faults")
            tags = [c[0] for c in calls]
            ck(tags.count("w32a150") == 2, f"32A150 x2 {tags}")
            ck("w313a00" in tags and "w30c0d0" in tags
               and "w30a880" in tags, "slot0 chain calls")
            # and [02089340],0xFFFFDFFF then (d&~4)|4 -> 4
            ck(gm.d(0x02089340) & 0x2000 == 0, "bit13 cleared")
            ck(gm.d(0x02089340) & 4 == 4, "bit2 set (equal rets)")

        elif name == "wt6-234590-s3":
            ck(w.faults == [], "faults")
            ck(not calls, f"slot3 calls {calls}")
            ck(gm.d(0x02089340) == 0, "flagword untouched")

        elif name == "wt6-234520-s0":
            ck(w.faults == [], "faults")
            tags = [c[0] for c in calls]
            for t in ("w23b040", "w313db0", "w319090", "t16d6a0"):
                ck(t in tags, f"{t} missing")
            ck(gm.q(0x0208E6A8) == 0, "callback consumed+cleared")

        elif name == "wt6-234520-s3":
            ck(w.faults == [], "faults")
            ck(not calls, f"slot3 calls {calls}")
            ck(gm.q(0x0208E6A8) != 0, "callback still armed")

        elif name.startswith("wt6-25d9e0"):
            ck(w.faults == [], "faults")
            slot = case["rcx"]
            obj = SLOTS + slot * 0x288
            # per-slot publish: q[02099D70] = this slot's obj
            ck(gm.q(0x02099D70) == obj,
               f"published obj {gm.q(0x02099D70):#x} != {obj:#x}")
            ck(gm.d(obj + 0x24) == 1, "obj+0x24 inc")
            ck(gm.d(obj + 0x38) == 1, "obj+0x38 inc")
            tags = [c[0] for c in calls]
            if slot == 0:
                ck("w25b740" in tags and "w25b600" in tags,
                   "slot0 extra work absent")
            else:
                ck("w25b740" not in tags and "w25b600" not in tags,
                   "nonzero slot ran slot0 arms")

        elif name.startswith("wt6-3db1f0"):
            ck(w.faults == [], "faults")
            row = w.mrows[2][0]
            # 3DB6E0(row) fires per row unconditionally; row63 only
            # gates the inner b[+0x11+k*0x14]==1->2 scan
            d6 = [c for c in calls if c[0] == "w3db6e0"]
            ck(d6 and d6[0][1] == row, f"3DB6E0(row) {d6}")
            if case.get("row63"):
                ck(gm.b(row + 0x63) == 2, "row63 >>=1")
                buf = w.rowbufs[row]
                ck(gm.b(buf + 0x11) == 2 and gm.b(buf + 0x25) == 2,
                   "byte-scan 1->2")
            else:
                ck(gm.b(row + 0x63) == 0, "row63 idle")

        elif name == "wt-mode0-wt6":
            ck(w.faults == [], "faults")
            tags = [c[0] for c in calls]
            # real bodies entered per (substep,slot)
            ck(w.trace.count("r234590") == 80, "234590 x80")
            ck(w.trace.count("r234520") == 80, "234520 x80")
            ck(w.trace.count("r3db1f0") == 80, "3DB1F0 x80")
            ck(w.trace.count("r25d9e0") == 80, "25D9E0 x80")
            ck(w.trace.count("r267310") >= 150,
               f"267310 count {w.trace.count('r267310')}")
            # but the slot-0 chain fires only 16x (once per substep)
            ck(tags.count("w32a150") == 32,
               f"32A150 {tags.count('w32a150')} != 32")
            # 234520's own chain = 313DB0/319090/16D6A0 -> 16x
            ck(tags.count("w313db0") == 16,
               f"313DB0 {tags.count('w313db0')} != 16")
            ck(tags.count("w319090") == 16,
               f"319090 {tags.count('w319090')} != 16")
            # 25D9E0's slot-0-only arms fire 16x (not 80)
            ck(tags.count("w25b740") == 16,
               f"25B740 {tags.count('w25b740')} != 16")
            ck(tags.count("w25b600") == 16,
               f"25B600 {tags.count('w25b600')} != 16")
            # real interleaving: flagword ends 0x10D ->
            # 234520's (d&5)==1 gate fails -> callback never fires
            # in-tick (still fires direct: wt6-234520-s0)
            ck(gm.d(0x02089340) & 5 != 1, "cb gate (d&5)==1 closed")
            ck(gm.q(0x0208E6A8) != 0, "callback suppressed in-tick")

        res[name] = {"pass": ok, "notes": notes,
                     "faults": w.faults[:4],
                     "trace": w.trace}
        print(("PASS " if ok else "FAIL ") + name +
              ("" if ok else "  " + "; ".join(notes)))

    # SS-1 control: apply result identical under bitset 0 vs all-ones
    cmpv = res.get("BITSET_CMP")
    if cmpv and len(cmpv) == 2:
        same = cmpv[0] == cmpv[1]
        res["ss-apply-bitset-invariance"] = {
            "pass": same,
            "notes": [] if same else [
                f"bitset0={cmpv[0]} bitsFF={cmpv[1]}"],
            "faults": [], "trace": []}
        print(("PASS " if same else "FAIL ") +
              "ss-apply-bitset-invariance")

    npass = sum(1 for k, v in res.items()
                if k != "BITSET_CMP" and v["pass"])
    ntot = sum(1 for k in res if k != "BITSET_CMP")
    print(f"{npass}/{ntot} pass")
    del res["BITSET_CMP"]
    with open(RESULT, "w") as f:
        json.dump({"pass": npass, "total": ntot,
                   "cases": {k: {"pass": v["pass"],
                                 "notes": v["notes"],
                                 "faults": v["faults"]}
                             for k, v in res.items()}},
                  f, indent=1)
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
