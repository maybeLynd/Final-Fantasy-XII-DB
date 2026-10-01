# rekey-inner: 00322050 -> 003220E0 with the REAL callee layer —
# runtime validation for CONTRACT-battle-unit-construction.md (the
# rekey inner resolver was EXP-150's remaining scripted boundary).
#
#   00322050 (0x2C, real): d[unit+0xEA4]=0; b[unit+0xEA8]=0;
#     d[unit+8] = 3220E0(q[unit+0x10]).
#
#   003220E0 (0xAF, real): rbx=rcx (the rekeyed object)
#     esi = obj ? 3589B0(obj) : 0            # OLD composite id
#     2659D0(rbx)                            # w[+0x16]=(w+1)&0x7FF,
#                                            #   cmove 1 if 0 — NO NULL
#                                            #   GUARD: 3220E0(0) faults
#     ebx = rbx ? 3589B0(rbx) : 0            # NEW id
#     rax = 327150()                         # find slot occupant
#     edi = rax ? d[rax+8] : 0
#     if esi != edi -> return ebx            # early out: slot doesn't
#                                            #   hold our old id
#     eax = 0xFF
#     if b[02089340] & 0x10:                 # flag gates the RESOLVE,
#       rax = 3588B0(ebx)                    #   not the store: flag
#       rax = rax ? q[rax+0x30] : 0          #   clear -> store 0xFF
#       rax2 = rax ? q[rax+0x698] : 0        #   (263E30 leaf)
#       eax = rax2 ? b[rax2+4] : 0xFF
#     d[q[02EBF190]+0x5AA4] = eax            # DWORD store (idx byte +
#                                            #   3 zero bytes)
#     326500()                               # notify — scripted
#     return ebx
#
#   id compose 3589B0 (leaf): ((w[+0x16]&0x7FF)<<4 | b[+0x15]&0xF)<<16
#     | w[0]; null->0.   genbump 2659D0 (leaf): w16=(w16+1)&0x7FF ->1
#     if 0.
#   findocc 327150 (real): rdx=q[02EBF190]; idx=b[rdx+0x5AA4]; idx>0x27
#     ->0; rdi=rdx+8+idx*0x1C8; scan i=0..d[0208E6A0]-1 via 236820(i)
#     (bounds: 0<=i<=count-1; row=q[0208E688]+i*0xF50); first row with
#     q[row+0x698]==rdi wins, else 0.
#   resolve 3588B0 (real): id==0->0; gen=(id>>20)&0x7FF,
#     cls=(id>>16)&0xF, idx=id&0xFFFF; cls>=5->0;
#     row=263FF0(cls)=02098E10+cls*0x288; arr=q[row+8]; guards arr!=0,
#     q[row]!=0, idx<d[row+0x20], b[row+0x10]&1, idx<d[arr];
#     o=q[arr+idx*8+8]; return w[o+0x16]==gen ? o : 0.
#   clsrow 263FF0 / objcnt 236850=d[0208E6A0] / objrow 236820 /
#   getq30 263E30=q[+0x30]: leaves, real.
#
#   Scripted boundary (entry-intercepted, args recorded, disclosed):
#     00326500 notify dispatcher (calls 311E20/326620/30D9A0/377C70 —
#     separate package-sized surface).
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

# ---- subjects ----
F_REKEY = 0x00322050       # rekey wrapper (entry for 50-* cases)
F_INNER = 0x003220E0       # inner resolver (entry for e0-* cases)

# ---- real callees ----
R_89B0 = 0x003589B0        # id compose
R_59D0 = 0x002659D0        # generation bump
R_7150 = 0x00327150        # find slot occupant
R_88B0 = 0x003588B0        # id -> object resolve
R_3FF0 = 0x00263FF0        # class-table row
R_6850 = 0x00236850        # object count
R_6820 = 0x00236820        # object array row
R_3E30 = 0x00263E30        # q[+0x30]

# ---- scripted boundary ----
X_6500 = 0x00326500        # notify dispatcher

# ---- globals (canonical .data cells, fixture-planted) ----
GLOB    = 0x02EBF190       # context table ptr cell
GFLAG   = 0x02089340       # &0x10 gate byte (== EXP-150 TRACKT base)
CLSTB   = 0x02098E10       # class table base, stride 0x288
OBJCNT  = 0x0208E6A0       # object array count dword
OBJBASE = 0x0208E688       # object array base ptr cell

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


def mkid(gen, cls, idx):
    return ((gen & 0x7FF) << 20) | ((cls & 0xF) << 16) | (idx & 0xFFFF)


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.uc.mem_map(STACK, 0x100000)
        self.uc.mem_map(RETQ, 0x1000)
        self.uc.mem_map(HEAP, 0x400000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP
        self.entry = 0
        gm = self.gm

        self.unit = self.alloc(0x1000)
        self.obj = self.alloc(0x100)        # the rekeyed object
        self.glob = self.alloc(0x8000)      # context table block
        self.objarr = self.alloc(0x4000)    # object array rows (0xF50)
        self.arr = self.alloc(0x1000)       # class-row pointer array
        self.resolved = self.alloc(0x100)   # object 3588B0 returns
        self.r2 = self.alloc(0x100)         # q[resolved+0x30]
        self.r3 = self.alloc(0x100)         # q[r2+0x698]; b[+4] is stored

        # unit fixture (for 50-* wrapper cases)
        u = case.get("unit", {})
        gm.w(self.unit + 0x10, qw(u.get("q10", self.obj)))
        gm.w(self.unit + 0xEA4, dw(u.get("ea4", 0xDEADBEEF)))
        gm.w(self.unit + 0xEA8, dw(u.get("ea8", 0xBEEFCAFE)))

        # rekeyed object: gen in w16&0x7FF, cls in b15&0xF, idx in w0
        o = case.get("obj", {})
        self.gen = o.get("gen", 0x10)
        self.cls = o.get("cls", 1)
        self.oidx = o.get("idx", 2)
        gm.w(self.obj + 0x16, struct.pack("<H", self.gen & 0xFFFF))
        gm.w(self.obj + 0x15, bytes([self.cls & 0xFF]))
        gm.w(self.obj, struct.pack("<H", self.oidx & 0xFFFF))

        # glob / slot row
        self.gidx = case.get("gidx", 3)
        if case.get("glob_null"):
            gm.w(GLOB, qw(0))
        else:
            gm.w(GLOB, qw(self.glob))
        gm.w(self.glob + 0x5AA4, dw(case.get("gidx_dw", self.gidx)))
        self.slotrow = self.glob + 8 + self.gidx * 0x1C8

        # object array + occupant
        cnt = case.get("objcnt", 0)
        gm.w(OBJCNT, dw(cnt))
        gm.w(OBJBASE, qw(self.objarr))
        occ = case.get("occupant")          # None -> no match planted
        self.occ = self.objarr
        if occ is not None and cnt:
            gm.w(self.occ + 0x698, qw(self.slotrow))
            gm.w(self.occ + 8, dw(occ.get("id",
                 mkid(self.gen, self.cls, self.oidx))))

        # flag gate
        gm.w(GFLAG, bytes([case.get("gflag", 0x10) & 0xFF]))

        # class table row for self.cls (fixed canonical address)
        row = CLSTB + self.cls * 0x288
        rr = case.get("row", {"arr": 1, "cap": 0x20, "flag": 1,
                              "head": 1})
        # explicit zeros — shipped .data at CLSTB is not necessarily 0
        gm.w(row, qw(1 if rr.get("head", 1) else 0))
        gm.w(row + 8, qw(self.arr if rr.get("arr", 1) else 0))
        gm.w(row + 0x20, dw(rr.get("cap", 0x20)))
        gm.w(row + 0x10, bytes([rr.get("flag", 1) & 0xFF]))
        gm.w(self.arr, dw(rr.get("acnt", 0x20)))

        # resolve target at arr[oidx]
        res = case.get("res", {"gen": "new", "q30": 1, "q698": 1,
                               "b4": 0x2A})
        if rr.get("arr", 1) and rr.get("acnt", 0x20) > self.oidx:
            if res.get("elem", 1):
                gm.w(self.arr + 8 + self.oidx * 8, qw(self.resolved))
            rgen = res.get("gen", "new")
            if rgen == "new":
                rgen = (self.gen + 1) & 0x7FF or 1
            gm.w(self.resolved + 0x16,
                 struct.pack("<H", rgen & 0xFFFF))
            if res.get("q30", 1):
                gm.w(self.resolved + 0x30, qw(self.r2))
            if res.get("q698", 1):
                gm.w(self.r2 + 0x698, qw(self.r3))
            gm.w(self.r3 + 4, bytes([res.get("b4", 0x2A) & 0xFF]))

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def alloc(self, n):
        a = self.hb
        self.hb += (n + 0xFFF) & ~0xFFF
        return a

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    SCR = {X_6500: "notify"}
    REAL = {F_INNER: "inner", R_89B0: "idcompose", R_59D0: "genbump",
            R_7150: "findocc", R_88B0: "resolve", R_3FF0: "clsrow",
            R_6850: "objcnt", R_6820: "objrow", R_3E30: "getq30"}

    def on_code(self, uc, addr, size, _):
        if addr == self.entry:
            return
        tag = self.SCR.get(addr)
        if tag is not None:
            rsp = uc.reg_read(UC_X86_REG_RSP)
            self.rets.setdefault("calls", []).append(
                [tag, uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF])
            self.trace.append(tag)
            self._ret()
            return
        t = self.REAL.get(addr)
        if t is not None:
            self.trace.append(t)
            return
        if addr == F_REKEY and self.entry != F_REKEY:
            self.trace.append("rekey_real")

    def run(self, entry, rcx=0):
        uc = self.uc
        self.entry = entry
        rsp = STACK + 0x80000
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, timeout=60_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------------------------
def base_case(**kw):
    c = {"obj": {"gen": 0x10, "cls": 1, "idx": 2},
         "gidx": 3, "objcnt": 0, "gflag": 0x10}
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k] = {**c[k], **v}
        else:
            c[k] = v
    return c


CASES = {
    # ---- direct 3220E0 entry ----
    "e0-null":      base_case(**{"entry": "inner", "null_obj": 1,
                                 "expect_fault": 1}),
    "e0-basic":     base_case(**{"entry": "inner"}),
    "e0-genwrap":   base_case(**{"entry": "inner",
                                 "obj": {"gen": 0x7FF}}),
    "e0-glob-null": base_case(**{"entry": "inner", "glob_null": 1,
                                 "expect_fault": 1}),
    "e0-slot-oob":  base_case(**{"entry": "inner", "gidx": 0x28,
                                 "objcnt": 1, "occupant": {}}),
    "e0-slot-edge": base_case(**{"entry": "inner", "gidx": 0x27,
                                 "gidx_dw": 0xAAAAAA27,
                                 "objcnt": 1, "occupant": {}}),
    "e0-occ-hit-flagclear": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {}, "gflag": 0}),
    "e0-occ-mismatch": base_case(**{
        "entry": "inner", "objcnt": 1,
        "occupant": {"id": 0x777777}}),
    "e0-occ-hit-clsge5": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "obj": {"cls": 6}}),
    "e0-res-arrnull": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "row": {"arr": 0}}),
    "e0-res-rownull": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "row": {"head": 0}}),
    "e0-res-oob":   base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "row": {"cap": 2}}),
    "e0-res-flag0": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "row": {"flag": 0}}),
    "e0-res-arrcnt": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "row": {"acnt": 2}}),
    "e0-res-elemnull": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "res": {"elem": 0}}),
    "e0-res-genmm": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "res": {"gen": 0x55}}),
    "e0-res-q30null": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "res": {"q30": 0}}),
    "e0-res-q698null": base_case(**{
        "entry": "inner", "objcnt": 1, "occupant": {},
        "res": {"q698": 0}}),
    "e0-full":      base_case(**{"entry": "inner", "objcnt": 1,
                                 "occupant": {}, "gidx_dw": 0xAAAAAA03}),

    # ---- 322050 wrapper entry ----
    "50-basic":     base_case(**{"entry": "rekey"}),
    "50-null10":    base_case(**{"entry": "rekey",
                                 "unit": {"q10": 0},
                                 "expect_fault": 1}),
    "50-full":      base_case(**{"entry": "rekey", "objcnt": 1,
                                 "occupant": {}}),

    # ---- mutation controls ----
    "mut-occ-id":   base_case(**{"entry": "inner", "objcnt": 1,
                                 "occupant": {"id": 0x01010003}}),
    "mut-gen-off":  base_case(**{"entry": "inner", "objcnt": 1,
                                 "occupant": {},
                                 "res": {"gen": 0x10}}),
}


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    gm = w.gm
    if case.get("entry") == "inner":
        rcx = 0 if case.get("null_obj") else w.obj
        out["ret"] = w.run(F_INNER, rcx=rcx)
    else:
        out["ret"] = w.run(F_REKEY, rcx=w.unit)
    out["unit"] = {"d8": gm.d(w.unit + 8),
                   "dea4": gm.d(w.unit + 0xEA4),
                   "bea8": gm.b(w.unit + 0xEA8)}
    out["obj"] = {"w16": gm.w16(w.obj + 0x16)}
    out["gidx_d"] = gm.d(w.glob + 0x5AA4) if not case.get("glob_null") \
        else None
    out.update(w.rets)
    out["ok"], out["fail"] = check(name, case, w, out)
    return out


def check(name, c, w, o):
    f = []
    tr = o["trace"]

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %s want %s" % (k, hex(got) if
                     isinstance(got, int) else got,
                     hex(want) if isinstance(want, int) else want))

    def called(tag):
        return [x for x in o.get("calls", []) if x[0] == tag]

    allow_fault = c.get("expect_fault")
    if o["faults"] and not allow_fault:
        f.append("faults: %s" % (o["faults"][:3],))
    if allow_fault and not o["faults"]:
        f.append("expected fault, none")

    gen, cls, oidx = w.gen, w.cls, w.oidx
    newgen = (gen + 1) & 0x7FF or 1
    old_id = mkid(gen, cls, oidx)
    new_id = mkid(newgen, cls, oidx)

    if name == "e0-null":
        # 2659D0 has no null guard: read w[0x16] faults
        if not any(x[0] == "mem" and x[2] == 0x16 for x in o["faults"]):
            f.append("faults: %s" % (o["faults"],))
        return len(f) == 0, f

    if name == "e0-glob-null":
        # 327150 reads b[0+0x5AA4] — no glob guard either
        if not any(x[0] == "mem" and x[2] == 0x5AA4
                   for x in o["faults"]):
            f.append("faults: %s" % (o["faults"],))
        # genbump still ran before the fault
        eq("w16", o["obj"]["w16"], newgen)
        return len(f) == 0, f

    if name == "50-null10":
        # clears land BEFORE the inner call faults
        eq("dea4", o["unit"]["dea4"], 0)
        eq("bea8", o["unit"]["bea8"], 0)
        if not any(x[0] == "mem" and x[2] == 0x16 for x in o["faults"]):
            f.append("faults: %s" % (o["faults"],))
        return len(f) == 0, f

    # every non-null case: bump ran, ret = new id
    eq("w16", o["obj"]["w16"], newgen)
    eq("ret", o["ret"], new_id)
    if "genbump" not in tr:
        f.append("no genbump")
    if tr.count("idcompose") != 2:
        f.append("idcompose x%s" % tr.count("idcompose"))

    if name.startswith("50-"):
        eq("d8", o["unit"]["d8"], new_id & 0xFFFFFFFF)
        eq("dea4", o["unit"]["dea4"], 0)
        eq("bea8", o["unit"]["bea8"], 0)
        if "inner" not in tr:
            f.append("inner not entered")

    hit = (c.get("objcnt", 0) > 0 and
           c.get("occupant") is not None)
    occ_id = (c.get("occupant") or {}).get("id", old_id)
    in_bounds = c.get("gidx", 3) <= 0x27
    matched = hit and occ_id == old_id and in_bounds
    flagged = bool(c.get("gflag", 0x10) & 0x10)

    if not matched:
        # early return: no resolve, no store, no notify
        if "resolve" in tr:
            f.append("resolve ran without match")
        if called("notify"):
            f.append("notify without match")
        eq("gidx_d", o["gidx_d"], c.get("gidx_dw", w.gidx))
        return len(f) == 0, f

    # matched: the store+notify ALWAYS run; the flag only selects
    # resolve-derived byte vs unconditional 0xFF
    if flagged and "resolve" not in tr:
        f.append("no resolve")
    if not flagged and "resolve" in tr:
        f.append("resolve ran with flag clear")
    if not called("notify"):
        f.append("no notify")
    want_store = 0xFF
    if flagged:
        res = c.get("res",
                    {"gen": "new", "q30": 1, "q698": 1, "b4": 0x2A})
        rr = c.get("row",
                   {"arr": 1, "cap": 0x20, "flag": 1, "head": 1})
        resolved = (cls < 5 and rr.get("head", 1) and
                    rr.get("arr", 1) and oidx < rr.get("cap", 0x20) and
                    rr.get("flag", 1) & 1 and
                    oidx < rr.get("acnt", 0x20) and
                    res.get("elem", 1) and
                    (res.get("gen", "new") in ("new",) or
                     res.get("gen") == newgen))
        if resolved and res.get("q30", 1) and res.get("q698", 1):
            want_store = res.get("b4", 0x2A)
    eq("gidx_d", o["gidx_d"], want_store)
    if name == "e0-full" and "getq30" not in tr:
        f.append("no getq30")

    return len(f) == 0, f


def main():
    raw, secs = load_image()
    results = {}
    npass = 0
    for name, case in CASES.items():
        out = run_case(name, case, raw, secs)
        results[name] = out
        if out["ok"]:
            npass += 1
        else:
            print("FAIL %s: %s" % (name, out["fail"]))
    print("%d/%d pass" % (npass, len(CASES)))
    with open(RESULT, "w") as fh:
        json.dump({"sha256": SHA, "cases": results}, fh, indent=1,
                  default=str)
    return 0 if npass == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
