"""Original-code replay (bounded) of the event-slot setter 0020AC30 and pusher 0020AF10, with 0020A760 run real.
FABLE, Claude Opus 5.5, 2026-09-25.

Stubbed at their entries (the harness supplies their documented effect): the path check 0020A800 (returns 1), the
matched-text extractor 0020AA50 (copies the planted name), EASTL assign 001A5760, substring search 001C34D0,
concat 001B31E0, memcmp, the cutscene JSON reader 001C5750 (records its argument), the notifier 00189120 and
_guard_check_icall. The allocator's +0x18 slot is a recording stub, so every free is observed.

Regression controls (each must hold, and each byte mutant must break the named case):
  polarity  - 0001 is tested INSIDE the sum_ arm; spc_ only when sum_ is absent;
  same-name - a repeated same-name call returns after entry has cleared both flags;
  marker    - the setter restores 01DFE40C to -1; the pusher leaves it at the pushed index.
Mutants: 0020AD3F je->jne (the sum_ branch) and 0020ACD2 je->jne (the same-name early exit)."""
import struct, json, sys, os
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import *

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
b = open(EXE, "rb").read()
pe = struct.unpack_from("<I", b, 0x3C)[0]; nsec = struct.unpack_from("<H", b, pe + 6)[0]
so = struct.unpack_from("<H", b, pe + 20)[0]; sec = pe + 24 + so
BASE = 0x120000; SIZE = struct.unpack_from("<I", b, pe + 24 + 56)[0]

SETTER, PUSHER = 0x20AC30, 0x20AF10
FLAG_E8, FLAG_E9, MARKER, COUNTERS, CURRENT = 0x1F832E8, 0x1F832E9, 0x1DFE40C, 0x1F832B0, 0x1F832C8
SLOTS, VECS = 0x1F832F0, 0x1F83390
STACK, HEAP, STUB, RET = 0x70000000, 0x71000000, 0x72000000, 0x73000000
VT = STUB + 0x100            # fake allocator vtable; +0x18 -> dealloc stub
DEALLOC = STUB + 0x200
HOOKED = {0x20A800, 0x20AA50, 0x1A5760, 0x1C34D0, 0x1B31E0, 0x861ED2, 0x1C5750, 0x189120, 0x16D6A0, 0x1A4250}

def fresh(patches=()):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(BASE, (SIZE + 0xFFF) & ~0xFFF)
    for i in range(nsec):
        s = sec + 40 * i
        vs, va, rs, ro = struct.unpack_from("<IIII", b, s + 8)
        mu.mem_write(BASE + va, b[ro:ro + min(rs, vs if vs else rs)])
    for a, byte in patches:
        mu.mem_write(a, bytes([byte]))
    for m in (STACK, HEAP, STUB, RET):
        mu.mem_map(m, 0x100000)
    mu.mem_write(STUB, b"\xC3" * 0x400)
    mu.mem_write(RET, b"\xF4")
    mu.mem_write(VT + 0x18, struct.pack("<Q", DEALLOC))
    st = {"heap": HEAP, "json": [], "frees": 0}
    def alloc(data):
        p = st["heap"]; mu.mem_write(p, data + b"\0"); st["heap"] += (len(data) + 0x20) & ~0xF; return p
    def setstr(obj, data):
        p = alloc(data)
        mu.mem_write(obj, struct.pack("<QQQQ", p, p + len(data), p + len(data) + 1, VT))
    def getstr(obj):
        bg, en = struct.unpack("<QQ", mu.mem_read(obj, 16)); return bytes(mu.mem_read(bg, en - bg)) if en > bg else b""
    for i in range(5):
        setstr(SLOTS + i * 0x20, b"")
        vb = alloc(b"\0" * 64); mu.mem_write(VECS + i * 0x20, struct.pack("<QQQ", vb, vb, vb + 64))
        mu.mem_write(COUNTERS + 4 * i, b"\0" * 4)
    setstr(CURRENT, b"")
    mu.mem_write(MARKER, struct.pack("<i", -1))
    mu.mem_write(FLAG_E8, b"\0\0")
    st["alloc"], st["setstr"], st["getstr"] = alloc, setstr, getstr
    def ret(uc, rax):
        rsp = uc.reg_read(UC_X86_REG_RSP); ra = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8); uc.reg_write(UC_X86_REG_RIP, ra); uc.reg_write(UC_X86_REG_RAX, rax)
    def hook(uc, addr, size, ud):
        R = lambda r: uc.reg_read(r)
        if addr == DEALLOC:
            st["frees"] += 1
            return
        if addr not in HOOKED:
            return
        rcx, rdx, r8, r9 = R(UC_X86_REG_RCX), R(UC_X86_REG_RDX), R(UC_X86_REG_R8), R(UC_X86_REG_R9)
        if addr == 0x20A800:
            ret(uc, 1)
        elif addr == 0x20AA50:                       # dest string (rcx) <- planted name object (rdx)
            uc.mem_write(rcx, bytes(uc.mem_read(rdx, 0x20))); ret(uc, rcx)
        elif addr == 0x1A5760:                       # assign(dest, begin, end)
            setstr(rcx, bytes(uc.mem_read(rdx, r8 - rdx)) if r8 > rdx else b""); ret(uc, rcx)
        elif addr == 0x1C34D0:                       # search(begin, end, needle, needle_end) -> ptr or end
            hay = bytes(uc.mem_read(rcx, rdx - rcx)); nd = bytes(uc.mem_read(r8, r9 - r8)); k = hay.find(nd)
            ret(uc, rdx if k < 0 else rcx + k)
        elif addr == 0x1B31E0:                       # out(rcx) = str(rdx) + cstr(r8)
            s = getstr(rdx); c = bytes(uc.mem_read(r8, 16)).split(b"\0")[0]; setstr(rcx, s + c); ret(uc, rcx)
        elif addr == 0x861ED2:                       # memcmp
            n = r8; a = bytes(uc.mem_read(rcx, n)); c = bytes(uc.mem_read(rdx, n)); ret(uc, 0 if a == c else 1)
        elif addr == 0x1C5750:
            st["json"].append(getstr(rcx).decode()); ret(uc, 0)
        elif addr in (0x189120, 0x16D6A0, 0x1A4250):
            ret(uc, 0)
    mu.hook_add(UC_HOOK_CODE, hook)
    return mu, st

def call(mu, fn, rcx, rdx):
    rsp = STACK + 0x80000
    mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp); mu.reg_write(UC_X86_REG_RCX, rcx); mu.reg_write(UC_X86_REG_RDX, rdx)
    mu.emu_start(fn, RET, count=100000)

def state(mu, st):
    return {"E8": mu.mem_read(FLAG_E8, 1)[0], "E9": mu.mem_read(FLAG_E9, 1)[0],
            "marker": struct.unpack("<i", mu.mem_read(MARKER, 4))[0], "json": list(st["json"]), "frees": st["frees"]}

def set_name(mu, st, idx, name):
    obj = STACK + 0x90000; st["setstr"](obj, name.encode()); st["json"].clear(); st["frees"] = 0
    try:
        call(mu, SETTER, idx, obj)
    except Exception as e:                 # a crash is a failed case, recorded as such
        return {"crash": str(e)}
    return state(mu, st)

def run(patches=()):
    out = {}
    mu, st = fresh(patches)
    out["sum_with_0001"] = set_name(mu, st, 0, "sum_a0001")
    out["same_name_repeat"] = set_name(mu, st, 0, "sum_a0001")
    out["0001_without_sum"] = set_name(mu, st, 1, "n0001")
    out["spc_"] = set_name(mu, st, 2, "spc_z0000")
    out["sum_without_0001"] = set_name(mu, st, 3, "sum_x0000")
    out["sum_and_spc"] = set_name(mu, st, 4, "sum_spc_0001")
    # pusher: slot 2 holds "spc_z0000"
    try:
        call(mu, PUSHER, 2, 7)
    except Exception as e:
        out["push_slot2"] = {"crash": str(e)}; return out
    cnt = struct.unpack("<5I", mu.mem_read(COUNTERS, 20))
    out["push_slot2"] = {"marker": struct.unpack("<i", mu.mem_read(MARKER, 4))[0], "counter2": cnt[2],
                         "current": st["getstr"](CURRENT).decode()}
    call(mu, PUSHER, 1, -1 & 0xFFFFFFFF)
    out["push_event_minus1"] = {"marker": struct.unpack("<i", mu.mem_read(MARKER, 4))[0],
                                "counter1": struct.unpack("<5I", mu.mem_read(COUNTERS, 20))[1]}
    return out

EXPECT = {
    "sum_with_0001": lambda s: s["E8"] == 1 and s["E9"] == 0 and s["json"] == ["sum_a0001.json"] and s["marker"] == -1,
    "same_name_repeat": lambda s: s["E8"] == 0 and s["E9"] == 0 and s["json"] == [] and s["marker"] == -1,
    "0001_without_sum": lambda s: s["E8"] == 0 and s["E9"] == 0 and s["json"] == [],
    "spc_": lambda s: s["E8"] == 0 and s["E9"] == 1 and s["json"] == [],
    "sum_without_0001": lambda s: s["E8"] == 0 and s["E9"] == 0 and s["json"] == ["sum_x0000.json"],
    "sum_and_spc": lambda s: s["E8"] == 1 and s["E9"] == 0,
    "push_slot2": lambda s: s["marker"] == 2 and s["counter2"] == 1 and s["current"] == "spc_z0000",
    "push_event_minus1": lambda s: s["marker"] == 1 and s["counter1"] == 0,
}

def verdict(out):
    v = {}
    for k in EXPECT:
        try:
            v[k] = bool(EXPECT[k](out[k]))
        except Exception:
            v[k] = False
    return v

if __name__ == "__main__":
    base = run(); v = verdict(base)
    m_sum = run(((0x20AD3F, 0x75),))     # je -> jne on the sum_ found test
    m_same = run(((0x20ACD2, 0x75),))    # je -> jne on the same-name early exit
    res = {"shipped": base, "verdict": v,
           "mutant_sum_branch": {"verdict": verdict(m_sum), "must_fail": ["sum_with_0001", "spc_"]},
           "mutant_same_name": {"verdict": verdict(m_same), "must_fail": ["same_name_repeat"]}}
    ok = all(v.values()) and not any(res["mutant_sum_branch"]["verdict"][k] for k in res["mutant_sum_branch"]["must_fail"]) \
         and not any(res["mutant_same_name"]["verdict"][k] for k in res["mutant_same_name"]["must_fail"])
    res["ok"] = ok
    json.dump(res, open(os.path.join(HERE, "event_slot_setter_replay.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))
    sys.exit(0 if ok else 1)
