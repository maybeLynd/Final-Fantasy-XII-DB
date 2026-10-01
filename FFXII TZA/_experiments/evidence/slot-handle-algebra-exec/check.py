# EXP-117 — slot-handle-algebra-exec
#
# Executes the alloc/resolve/index algebra of the 0xE0-stride slot
# pool at q[0x02B40528] — the same pool whose consumers ran real in
# EXP-113/114, now exercised from the allocation side:
#
#   HID   003B56D0(ecx=index) — slot allocator + handle issuer:
#         scans b[slot+0x40]&1==0, bumps gen counter d[0x02B40520]
#         (clamp >0xFFFFFF -> 1), writes handle=(gen<<8)|slot at
#         +0x10, initialises the slot record, resolves the parent
#         record in the 0x740-stride pool q[0x022C6F28] (gate
#         d[+0x284]), pulls two name-table words via 003E5AD0.
#   FLDR  003E5AD0(rcx=record, edx=field) — word resolver leaf:
#         r8=[rcx+0x400]; edx<0x20 -> w[r8+w[r8+2]+edx*2+0x14C];
#         edx==0x104/5/6 -> w[r8+0x3A/0x3C/0x3E]; else 0xFFFF.
#   RES   003AB7F0(rcx=handle) — handle dispatcher: null->0,
#         low2==0 -> passthrough, low2==1 -> 0036B130 (scripted
#         boundary — executed real in EXP-084), else ->0.
#   MIDS  002ED570(rcx=ctx, edx=idx) — middle resolver: two RES
#         resolves (deposits at +0x38/+0x10) + BASE + arithmetic.
#   D6A   003E6DA0(rcx=ctx) — MIDS consumer driver: BASE ->
#         [+0xD98] ctx -> MIDS -> tail jmp 00370E20 (boundary).
#   BASE  0020E600(ecx) — arena codec base: rax = rcx + q[0x01F83530].
#
# Scripted boundaries: 0036B130 (planted per-case return map) and
# 00370E20 (tail-call return).  Boundary args are recorded as trace
# tokens.  All pool/table memory is planted fixture — disclosed.
import ctypes, hashlib, json, os, struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import UcError
from unicorn import (Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE,
                     UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL)
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RIP,
                               UC_X86_REG_RCX, UC_X86_REG_RDX,
                               UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

HID   = 0x003B56D0
FLDR  = 0x003E5AD0
RES   = 0x003AB7F0
MIDS  = 0x002ED570
D6A   = 0x003E6DA0
BASE  = 0x0020E600
HRES  = 0x0036B130    # RES mode-1 arm — scripted boundary
E20   = 0x00370E20    # D6A tail      — scripted boundary

POOLP   = 0x02B40528   # q: slot-pool base
GENC    = 0x02B40520   # d: generation counter (pool-8)
RECP    = 0x022C6F28   # q: 0x740-stride record pool
CODEC   = 0x01F83530   # q: arena codec base

# planted fixture addresses
POOL    = HEAP + 0x100000          # 0xA0 * 0xE0 slot pool
RECPOOL = HEAP + 0x200000          # 0x740-stride record pool
FTAB    = HEAP + 0x300000          # record+0x400 field table
MCTX    = HEAP + 0x400000          # MIDS context object
DCTX    = HEAP + 0x500000          # D6A context object
ARENA   = HEAP + 0x600000          # arena base (codec value)


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)


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


def img_rd_or_zero(raw, secs, va, n):
    try:
        return img_rd(raw, secs, va, n)
    except KeyError:
        return b"\0" * n


def img_qw(raw, secs, va):
    return struct.unpack("<Q", img_rd_or_zero(raw, secs, va, 8))[0]


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
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]
    def dw(self, addr):
        return struct.unpack("<I", self.r(addr, 4))[0]
    def ww(self, addr):
        return struct.unpack("<H", self.r(addr, 2))[0]


SLOT_N   = 0xA0
SLOT_ST  = 0xE0
REC_ST   = 0x740
ONE_F    = 0x3F800000


def hid_args(case):
    """the sx16 record indices HID steps resolve."""
    out = []
    for entry, rcx, rdx in case.get("steps", []):
        if entry == HID:
            v = rcx & 0xFFFF
            v = v - 0x10000 if v & 0x8000 else v
            out.append(v)
    return out


def build_fixture(case):
    """bytes/plants shared by native World and python model.
    Returns a list of (addr, bytes) writes."""
    W = []
    # --- slot pool: b[+0x40] bit0 = occupied; extra flag bits via
    # slot_flags ---
    occ = set(case.get("occupied", ()))
    sflags = case.get("slot_flags", {})
    for i in range(SLOT_N):
        base = POOL + i * SLOT_ST
        flag = sflags.get(i, 0x01 if i in occ else 0x00)
        W.append((base + 0x40, bytes([flag & 0xFF])))
        W.append((base + 4, dw(case.get("slot_arg", {}).get(i, 0))))
        W.append((base + 0x10, dw(case.get("slot_h", {}).get(i, 0))))
    W.append((POOLP, qw(POOL)))
    W.append((GENC, dw(case.get("gen", 0x41))))
    # --- record pool: one record per HID arg (index = sx16(arg)) ---
    W.append((RECP, qw(RECPOOL)))
    ftab = case.get("ftab", FTAB)
    for ridx in hid_args(case):
        if ridx < 0:
            continue
        rec = RECPOOL + ridx * REC_ST
        W.append((rec + 0x284, dw(case.get("rec_gate", 1))))
        W.append((rec + 0x400, qw(ftab)))
    # also FLDR steps use RECPOOL+3*REC_ST directly
    if any(e == FLDR for e, _, _ in case.get("steps", [])):
        rec = RECPOOL + 3 * REC_ST
        W.append((rec + 0x284, dw(1)))
        W.append((rec + 0x400, qw(ftab)))
    # --- field table: r8 = ftab; rcx = r8 + w[r8+2] ---
    W.append((ftab + 2, ww(case.get("ftab_off", 0x40))))
    sub = ftab + case.get("ftab_off", 0x40)
    for i in range(0x20):
        W.append((sub + 0x14C + i * 2, ww(0x1000 + i)))
    W.append((ftab + 0x3A, ww(case.get("f104", 0x00AA))))
    W.append((ftab + 0x3C, ww(case.get("f105", 0x00BB))))
    W.append((ftab + 0x3E, ww(case.get("f106", 0x00CC))))
    # --- MIDS context ---
    mc = case.get("mctx", {})
    W.append((MCTX + 0x30, qw(mc.get("h30", 0))))
    W.append((MCTX + 0x38, qw(0)))
    W.append((MCTX + 0x08, qw(mc.get("h08", 0))))
    W.append((MCTX + 0x10, qw(0)))
    W.append((MCTX + 0x4C, dw(mc.get("shift", 2))))
    W.append((MCTX + 0x48, dw(mc.get("mult", 0x40))))
    W.append((MCTX + 0x50, dw(mc.get("mask", 0xFF))))
    # MIDS's resolved tables live at the RESOLVED h30/h08 values:
    # elem gate at [h30 + edx*16], record dword at
    # [h08 + (edx>>shift)*32 + 0x10] feeding BASE.
    for edx, v in mc.get("elem", {}).items():
        W.append((mc.get("h30", 0) + edx * 16, dw(v)))
    for idx, v in mc.get("rt_e10", {}).items():
        W.append((mc.get("h08", 0) + idx * 32 + 0x10, dw(v)))
    # D6A context: d[+0x18] index, d[+0x10] codec offset
    dc = case.get("dctx", {})
    W.append((DCTX + 0x18, dw(dc.get("idx", 5))))
    W.append((DCTX + 0x10, dw(dc.get("coff", 0))))
    W.append((CODEC, qw(ARENA)))
    coff = dc.get("coff", 0)
    W.append((ARENA + coff + 0xD98, qw(dc.get("midctx", MCTX))))
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
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets = [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr == HRES:
            # scripted boundary: record arg, plant return, pop the call
            self.trace.append("hres:%x" % uc.reg_read(UC_X86_REG_RCX))
            ret = self.case.get("hres_map", {}).get(
                uc.reg_read(UC_X86_REG_RCX), 0)
            uc.reg_write(UC_X86_REG_RAX, ret)
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)
        elif addr == E20:
            # tail-call boundary: inherits caller's frame -> ret to it
            self.trace.append("e20:%x" % uc.reg_read(UC_X86_REG_RCX))
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("e20_ret", 0))
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.emu_stop()
        return True

    def run_one(self, entry, rcx, rdx=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        try:
            uc.emu_start(entry, RETQ, count=60000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for entry, rcx, rdx in self.case.get("steps", []):
            self.run_one(entry, rcx, rdx)

    def obs(self):
        slotw = {}
        for i in range(SLOT_N):
            base = POOL + i * SLOT_ST
            if self.gm.r(base, SLOT_ST) != bytes(SLOT_ST):
                slotw[i] = self.gm.r(base, SLOT_ST).hex()
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets,
                "gen": self.gm.dw(GENC),
                "slots": slotw,
                "m38": self.gm.qw(MCTX + 0x38),
                "m10": self.gm.qw(MCTX + 0x10),
                "head_p": self.gm.qw(POOLP)}


# ---------------- python model ----------------

def model_res(case, h, hres_calls):
    """RES dispatch: null->0, low2==0->identity, any nonzero->hres.
    The setne/cmp-1 pair routes ALL low2!=0 handles to 0036B130 —
    verified by res-mode2/mode3 producing hres tokens."""
    if h == 0:
        return 0
    if h & 3 == 0:
        return h
    hres_calls.append(h)
    r = case.get("hres_map", {}).get(h, 0)
    # movsxd rcx,eax; cmp rcx,0x40; cmovbe rax,0 — small-index
    # results are treated as failures
    lo = r & 0xFFFFFFFF
    sx = lo - 0x100000000 if lo & 0x80000000 else lo
    if sx & 0xFFFFFFFFFFFFFFFF <= 0x40:
        return 0
    return r


def model_fldr(case, rcx, edx, ftab, rec):
    """003E5AD0 over planted field table; rcx==0 -> fault (deref)."""
    if rcx == 0:
        return "FAULT"
    r8 = ftab
    if edx < 0x20:
        sub = ftab + case.get("ftab_off", 0x40)
        return (0x1000 + edx) & 0xFFFF
    if edx == 0x104:
        return case.get("f104", 0x00AA)
    if edx == 0x105:
        return case.get("f105", 0x00BB)
    if edx == 0x106:
        return case.get("f106", 0x00CC)
    return 0xFFFF


def sx16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def mids_calc(case, edx, hres_calls):
    """shared MIDS model: returns (ret, m38, m10, gate_fault)."""
    mc = case.get("mctx", {})
    h30 = model_res(case, mc.get("h30", 0), hres_calls)
    h08 = model_res(case, mc.get("h08", 0), hres_calls)
    shift = mc.get("shift", 2)
    mult = mc.get("mult", 0x40)
    mask = mc.get("mask", 0xFF)
    elem = (h30 + edx * 16) & 0xFFFFFFFFFFFFFFFF
    recp = (h08 + (edx >> shift) * 32) & 0xFFFFFFFFFFFFFFFF
    gate = mc.get("elem", {}).get(edx, 0)
    e10 = mc.get("rt_e10", {}).get(edx >> shift, 0)
    base_v = (e10 + ARENA) & 0xFFFFFFFFFFFFFFFF
    if gate == 0xFFFFFFFF or gate == -1:
        return 0, h30, h08, False
    prod32 = ((mask & edx) * mult) & 0xFFFFFFFF
    return (base_v + sx32(prod32)) & 0xFFFFFFFFFFFFFFFF, \
        h30, h08, False


def slot_image(arg, handle, w3c, w3e, old_flag):
    """expected 0xE0 bytes after a successful HID alloc."""
    b = bytearray(SLOT_ST)
    b[0x04:0x08] = dw(arg)               # d[slot+4] = edi
    b[0x08:0x0C] = dw(ONE_F)
    b[0x0C:0x10] = dw(ONE_F)
    b[0x10:0x14] = dw(handle)
    b[0x14:0x1C] = qw(ONE_F)             # qword store 0x3F800000
    b[0x2C:0x30] = dw(ONE_F)
    b[0x38:0x3A] = ww(w3c)               # w[+0x38] = w[+0x3C]
    b[0x3C:0x3E] = ww(w3c)
    b[0x3E:0x40] = ww(w3e)
    b[0x40] = (old_flag & 0x81) | 0x01
    b[0x44:0x48] = dw(ONE_F)
    b[0x58:0x5C] = dw(ONE_F)
    b[0x5C:0x64] = qw(ONE_F)
    b[0x78:0x80] = qw(ONE_F)
    b[0x88:0x8C] = dw(ONE_F)
    b[0x8C:0x94] = qw(ONE_F)
    b[0x94:0x9C] = qw(ONE_F)
    b[0xC8:0xCC] = dw(ONE_F)
    b[0xCC:0xD4] = qw(ONE_F)
    b[0xD4:0xD8] = dw(ONE_F)
    return bytes(b)


def fault_slot_image(arg, handle, old_flag):
    """expected 0xE0 bytes when the FLDR call faults (rcx==0): all
    writes before the first FLDR land; +0x38/+0x3C/+0x3E and the
    post-FLDR +0xC8/+0xCC/+0xD4 float stores stay zero."""
    b = bytearray(slot_image(arg, handle, 0, 0, old_flag))
    b[0xC8:0xD8] = bytes(0x10)
    return bytes(b)


def run_model(case):
    """expected observables for the step list."""
    occ = set(case.get("occupied", ()))
    sflags = case.get("slot_flags", {})
    def slot_flag(i):
        return sflags.get(i, 0x01 if i in occ else 0x00)
    # live flag state — HID writes b[+0x40] = (old & 0x81) | 1
    flags = {i: slot_flag(i) for i in range(SLOT_N)}
    gen = case.get("gen", 0x41)
    mc = case.get("mctx", {})
    slots = {}                       # idx -> expected 0xE0 image
    exp_trace, exp_rets, faults = [], [], []
    hres_calls = []
    m38m, m10m = 0, 0

    for entry, rcx, rdx in case.get("steps", []):
        if entry == HID:
            found = None
            for i in range(SLOT_N):
                if flags[i] & 1 == 0:
                    found = i
                    break
            if found is None:
                exp_rets.append(0)
                continue
            gen = gen + 1
            if gen > 0xFFFFFF:
                gen = 1
            handle = ((gen << 8) | found) & 0xFFFFFFFF
            di = sx16(rcx)
            parent = 0
            if di != -1 and case.get("rec_gate", 1):
                parent = RECPOOL + di * REC_ST
            ftab = case.get("ftab", FTAB)
            if parent == 0:
                # FLDR derefs rcx+0x400 with rcx==0 -> AV at 0x400
                faults.append(0x400)
                slots[found] = fault_slot_image(
                    rcx & 0xFFFFFFFF, handle, flags[found])
                flags[found] = (flags[found] & 0x81) | 0x01
                exp_rets.append(None)      # wildcard — mid-fault rax
                continue
            w3c = model_fldr(case, parent, 0x104, ftab, di)
            w3e = model_fldr(case, parent, 0x106, ftab, di)
            slots[found] = slot_image(rcx & 0xFFFFFFFF, handle,
                                      w3c, w3e, flags[found])
            flags[found] = (flags[found] & 0x81) | 0x01
            exp_rets.append(handle)
        elif entry == RES:
            exp_rets.append(model_res(case, rcx, hres_calls))
        elif entry == MIDS:
            r, m38m, m10m, _ = mids_calc(case, sx32(rdx), hres_calls)
            exp_rets.append(r)
        elif entry == D6A:
            dc = case.get("dctx", {})
            idx = sx32(dc.get("idx", 5))
            if idx == -1:
                exp_rets.append(0)
                continue
            r, m38m, m10m, _ = mids_calc(case, idx, hres_calls)
            if r == 0:
                exp_rets.append(0)
            else:
                exp_trace.append("e20:%x" % r)
                exp_rets.append(case.get("e20_ret", 0))
        elif entry == FLDR:
            r = model_fldr(case, rcx, rdx,
                           case.get("ftab", FTAB), 0)
            if r == "FAULT":
                faults.append(("fldr0",))
                exp_rets.append(None)
            else:
                exp_rets.append(r)
    exp_trace.extend("hres:%x" % h for h in hres_calls)

    # every nonzero slot appears in obs — occupied/extra-flag
    # fixtures plus HID-written images
    out_slots = {}
    for i in range(SLOT_N):
        if i in slots:
            img = slots[i]
        else:
            b = bytearray(SLOT_ST)
            b[0x40] = slot_flag(i) & 0xFF
            b[0x04:0x08] = dw(case.get("slot_arg", {}).get(i, 0))
            b[0x10:0x14] = dw(case.get("slot_h", {}).get(i, 0))
            img = bytes(b)
        if img != bytes(SLOT_ST):
            out_slots[i] = img.hex()
    ran_mids = any(e in (MIDS, D6A) for e, _, _ in
                   case.get("steps", []))
    return {"trace": exp_trace, "faults": faults, "rets": exp_rets,
            "gen": gen,
            "slots": out_slots,
            "m38": m38m if ran_mids else 0,
            "m10": m10m if ran_mids else 0,
            "head_p": POOL}


# ---------------- cases ----------------

def build_cases():
    C = {}
    C["alloc-first"] = {"steps": [(HID, 5, 0)]}
    C["alloc-occupied"] = {"occupied": {0, 1, 2},
                           "steps": [(HID, 5, 0)]}
    C["alloc-two"] = {"steps": [(HID, 5, 0), (HID, 7, 0)]}
    C["alloc-gen-wrap"] = {"gen": 0xFFFFFF, "steps": [(HID, 5, 0)]}
    C["alloc-full"] = {"occupied": set(range(SLOT_N)),
                       "steps": [(HID, 5, 0)]}
    C["alloc-neg1"] = {"steps": [(HID, 0xFFFF, 0)]}
    C["alloc-gate0"] = {"rec_gate": 0, "steps": [(HID, 3, 0)]}
    # free slot whose flag has bit1 set — distinguishes &1 vs &2
    C["alloc-bit2-flag"] = {"slot_flags": {0: 0x02},
                            "steps": [(HID, 5, 0)]}
    # gen+1 == 0xFFFFFF exactly: cmp 0xFFFFFF vs 0xFFFFFE differ
    C["alloc-gen-edge"] = {"gen": 0xFFFFFE, "steps": [(HID, 5, 0)]}
    C["res-null"] = {"steps": [(RES, 0, 0)]}
    C["res-ptr"] = {"steps": [(RES, 0x40000100, 0)]}
    C["res-mode1"] = {"hres_map": {0x12345: 0x4ABC0000},
                      "steps": [(RES, 0x12345, 0)]}
    C["res-mode2"] = {"steps": [(RES, 0x12346, 0)]}
    C["res-mode3"] = {"steps": [(RES, 0x12347, 0)]}
    # low3=4: &3==0 passthrough vs &7!=0 hres — discriminates the
    # test-mask mutant
    C["res-low4"] = {"steps": [(RES, 0x12344, 0)]}
    # hres returning a small index (<=0x40) is zeroed by the caller
    C["res-hres-low"] = {"hres_map": {0x12345: 0x30},
                         "steps": [(RES, 0x12345, 0)]}
    # sign-bit low32: sx32 -> huge unsigned -> returned verbatim
    C["res-hres-neg"] = {"hres_map": {0x12345: 0x80000000},
                         "steps": [(RES, 0x12345, 0)]}
    C["mids-basic"] = {"mctx": {"h30": HEAP + 0x480000,
                              "h08": HEAP + 0x490000,
                              "shift": 2, "mult": 0x40,
                              "mask": 0xFF,
                              "elem": {9: 7},
                              "rt_e10": {2: 0x55}},
                      "steps": [(MIDS, MCTX, 9)]}
    C["mids-neg-gate"] = {"mctx": {"h30": HEAP + 0x480000,
                                 "h08": HEAP + 0x490000,
                                 "elem": {4: -1}},
                        "steps": [(MIDS, MCTX, 4)]}
    # negative index: sar vs shr diverge on the row address
    C["mids-neg"] = {"mctx": {"h30": HEAP + 0x480000,
                             "h08": HEAP + 0x490000},
                     "steps": [(MIDS, MCTX, 0xFFFFFFFF)]}
    C["d6a-flow"] = {"mctx": {"h30": HEAP + 0x480000,
                             "h08": HEAP + 0x490000,
                             "elem": {5: 3}, "rt_e10": {1: 0x10}},
                     "dctx": {"idx": 5, "coff": 0, "midctx": MCTX},
                     "e20_ret": 0x77,
                     "steps": [(D6A, DCTX, 0)]}
    C["d6a-neg"] = {"dctx": {"idx": -1},
                    "steps": [(D6A, DCTX, 0)]}
    # idx=0: the -1 guard must not fire — discriminates cmp imm
    C["d6a-zero"] = {"mctx": {"h30": HEAP + 0x480000,
                             "h08": HEAP + 0x490000,
                             "elem": {0: 5}, "rt_e10": {0: 0x10}},
                     "dctx": {"idx": 0, "coff": 0, "midctx": MCTX},
                     "e20_ret": 0x77,
                     "steps": [(D6A, DCTX, 0)]}
    # edx*32 vs edx*16 land on different elems: the shifted one is -1
    C["mids-stride-gap"] = {"mctx": {"h30": HEAP + 0x480000,
                                    "h08": HEAP + 0x490000,
                                    "elem": {4: 3, 8: -1},
                                    "rt_e10": {1: 0x10}},
                            "steps": [(MIDS, MCTX, 4)]}
    # product wraps negative in eax; cdqe sign-extends the add
    C["mids-negprod"] = {"mctx": {"h30": HEAP + 0x480000,
                                 "h08": HEAP + 0x490000,
                                 "mask": 0xFFFF, "mult": 0x10000},
                         "steps": [(MIDS, MCTX, 0xFFFF)]}
    C["fldr-low"] = {"steps": [(FLDR, RECPOOL + 3 * REC_ST, 0x15)]}
    C["fldr-104"] = {"steps": [(FLDR, RECPOOL + 3 * REC_ST, 0x104)]}
    C["fldr-hi"] = {"steps": [(FLDR, RECPOOL + 3 * REC_ST, 0x105)]}
    C["fldr-unk"] = {"steps": [(FLDR, RECPOOL + 3 * REC_ST, 0x200)]}
    C["alloc-then-resolve"] = {
        "steps": [(HID, 5, 0)],
        "mctx": {"h30": HEAP + 0x480000, "h08": HEAP + 0x490000}}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])
def W(x): return struct.pack("<i", x)

MUTS = [
    # HID: occupancy test bit (F6 43 40 01 -> tests bit1 instead)
    ("m-hid-bit",    0x3B56F3, B(0x01), B(0x02), "alloc-bit2-flag"),
    # HID: slot cap 0xA0 -> 0xA1 (scans one past the pool)
    ("m-hid-cap",    0x3B5701, B(0xA0), B(0xA1), "alloc-full"),
    # HID: gen clamp imm low byte 0xFFFFFF -> 0xFFFFFE
    ("m-hid-clamp",  0x3B572A, B(0xFF), B(0xFE), "alloc-gen-edge"),
    # HID: cmova -> cmovbe (clamp direction inverted)
    ("m-hid-cmov",   0x3B573B, B(0x47), B(0x46), "alloc-gen-wrap"),
    # HID: shl eax,8 -> shl eax,9
    ("m-hid-shl",    0x3B574C, B(0x08), B(0x09), "alloc-first"),
    # HID: or eax,edx -> and eax,edx (slot bits dropped)
    ("m-hid-or",     0x3B574D, B(0x0B), B(0x23), "alloc-first"),
    # HID: flag mask and al,0x81 -> or al,0x81 (preserves flag bits)
    ("m-hid-fmask",  0x3B575D, B(0x24), B(0x0C), "alloc-bit2-flag"),
    # HID: or al,cl -> and al,cl (occupied bit never set)
    ("m-hid-fset",   0x3B5763, B(0x0A), B(0x22), "alloc-two"),
    # HID: arg store disp +4 -> +8 (writes over the 1.0f field)
    ("m-hid-arg",    0x3B5728, B(0x04), B(0x08), "alloc-first"),
    # HID: handle store disp +0x10 -> +0x18
    ("m-hid-hstore", 0x3B5758, B(0x10), B(0x18), "alloc-first"),
    # HID: parent gate disp +0x284 -> +0x288
    ("m-hid-gate",   0x3B57F2, B(0x84), B(0x88), "alloc-first"),
    # HID: field id 0x104 -> 0x105 (wrong name-table word)
    ("m-hid-f104",   0x3B57FB, B(0x04), B(0x05), "alloc-first"),
    # RES: test dl,3 -> test dl,7 (wider mode mask)
    ("m-res-mask",   0x3AB805, B(0x03), B(0x07), "res-low4"),
    # RES: cmp ecx,1 -> cmp ecx,2 (mode-1 arm unreachable)
    ("m-res-mode",   0x3AB81B, B(0x01), B(0x02), "res-mode1"),
    # RES: setne cl -> sete cl (mode inverted)
    ("m-res-setne",  0x3AB813, B(0x95), B(0x94), "res-ptr"),
    # RES: hres result bound 0x40 -> 0x20
    ("m-res-bound",  0x3AB837, B(0x40), B(0x20), "res-hres-low"),
    # MIDS: shl rdi,4 -> shl rdi,5 (element stride doubled)
    ("m-mids-stride",0x2ED5A5, B(0x04), B(0x05), "mids-stride-gap"),
    # MIDS: sar ebp,cl -> shr ebp,cl (unsigned shift)
    ("m-mids-sar",   0x2ED5AD, B(0xFD), B(0xED), "mids-neg"),
    # MIDS: shl rax,5 -> shl rax,4 (record stride halved)
    ("m-mids-rst",   0x2ED5C6, B(0x05), B(0x04), "mids-basic"),
    # MIDS: mask and eax,esi -> or eax,esi
    ("m-mids-and",   0x2ED5E2, B(0x23), B(0x0B), "mids-basic"),
    # MIDS: mult disp +0x48 -> +0x4C (reads the shift instead)
    ("m-mids-mult",  0x2ED5E7, B(0x48), B(0x4C), "mids-basic"),
    # FLDR: index bound 0x20 -> 0x10 (table halved)
    ("m-fldr-bound", 0x3E5AE9, B(0x20), B(0x10), "fldr-low"),
    # FLDR: field-0x104 disp +0x3A -> +0x3C
    ("m-fldr-104",   0x3E5B04, B(0x3A), B(0x3C), "fldr-104"),
    # D6A: idx guard cmp ebx,-1 -> cmp ebx,0
    ("m-d6a-neg",    0x3E6DAB, B(0xFF), B(0x00), "d6a-zero"),
    # BASE: rip-rel disp -> wrong base (codec off by 4)
    ("m-base-disp",  0x20E605, B(0x27), B(0x2B), "mids-basic"),
]


def run_native(case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    return w.obs()


def differs(k, nv, mv):
    if k == "rets":
        if len(nv) != len(mv):
            return True
        return any(m is not None and n != m for n, m in zip(nv, mv))
    if k == "faults":
        # model emits expected fault addresses; native tuples are
        # (access, addr, size) — compare address multisets
        naddrs = sorted(t[1] if isinstance(t[1], int) else -1
                        for t in nv)
        return naddrs != sorted(mv)
    return nv != mv


def main():
    raw, secs = load_image()
    cases = build_cases()
    keys = ("trace", "rets", "gen", "slots", "m38", "m10",
            "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case, raw, secs)
        mod = run_model(case)
        d = [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:180])
                print("  mod:", str(mod.get(k))[:180])
    print("functional: %d/%d" % (len(cases) - fails, len(cases)))

    for mid, va, orig, mut, cname in MUTS:
        got = img_rd(raw, secs, va, len(orig))
        if got != orig:
            results["bad_sites"].append((mid, hex(va), got.hex()))
            print("BAD SITE", mid, hex(va), "want", orig.hex(),
                  "got", got.hex())
    if results["bad_sites"]:
        print("aborting mutant run — fix sites first")
        json.dump(results, open(RESULT, "w"), indent=1)
        return

    alive = 0
    for mid, va, orig, mut, cname in MUTS:
        case = dict(cases[cname])
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + \
            [(va, mut)]
        try:
            nat = run_native(case, raw, secs)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case)
        if [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
