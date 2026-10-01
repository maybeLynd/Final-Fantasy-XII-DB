# EXP-101 find-owning-unit-exec
#
# Executes the SHIPPED bytes of BattleStats_FindOwningBattleUnit (0031B860)
# plus its two pool helpers under Unicorn:
#
#   0031B860  FIND    - if (!rec) ret 0; for i in [0,count):
#                         u = GET(i); if (u && u[0x698]==rec) ret u; ret 0
#   00236850  COUNT   - mov eax,[0x208E6A0]; ret          (7 B leaf)
#   00236820  GET     - i<0 || i>count-1 -> 0;
#                       else [0x208E688] + i*0xF50        (0x25 B leaf)
#
# The pool is the 0xF50-stride battle-unit array whose +0x698 qword is the
# back-pointer to the owning stats record (the same unit kind EXP-100 read
# at +0xE80/+0xE90). 0031B860 is the reverse lookup used by 35
# CombatFormula callers (CONTRACT-auto-status-rebuild + status-write).
#
# No scripted boundaries: every body in the chain runs from shipped bytes.
# Direct-call cases exercise the getter's refusal arm, which the subject's
# loop invariant (0 <= i < count) makes unreachable from 0031B860 itself.
#
# Globals planted in the image's .data:
#   [0x208E688] qword = pool base      [0x208E6A0] dword = count
#   [0x208E690] qword = decoy base     [0x208E6A4] dword = decoy count
# (decoys exist only so base-source mutants diverge; unpatched reads
# never touch them.)
#
# Trace tokens: n = count getter fired, g<i> = element getter fired with
# signed index i. Observables: ret (unit ptr or 0), trace, faults.

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
POOL   = HEAP + 0x000000       # real unit pool, stride 0xF50
DECOY  = HEAP + 0x800000       # decoy pool for base-source mutants
REC    = HEAP + 0x400000       # stats record being looked up
STRIDE = 0xF50
MATCH  = 0x698                 # unit+0x698 == rec back-pointer

SUBJ  = 0x0031B860
COUNT = 0x00236850
GET   = 0x00236820

G_BASE   = 0x0208E688
G_COUNT  = 0x0208E6A0
G_DBASE  = 0x0208E690
G_DCOUNT = 0x0208E6A4

HOOKS = {COUNT: "n", GET: "g"}


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


class World:
    def __init__(self, case, raw, secs):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        # whole image, then heap/stack
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)

        # globals: real pool/count plus decoys at the mutant-targeted
        # neighbour slots (unpatched code never reads them)
        gm.w(G_BASE, qw(case.get("base", POOL)))
        gm.w(G_COUNT, dw(case.get("count", 0)))
        gm.w(G_DBASE, qw(case.get("decoy_base", DECOY)))
        gm.w(G_DCOUNT, dw(case.get("decoy_count", 1)))

        # pool rows: unit i at base+i*0xF50; match qword at +0x698
        for i, match in enumerate(case.get("matches", [])):
            base = case.get("base", POOL)
            gm.w(base + i * STRIDE + MATCH, qw(match))
        for i, match in enumerate(case.get("decoy_matches", [])):
            gm.w(case.get("decoy_base", DECOY) + i * STRIDE + MATCH,
                 qw(match))

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in HOOKS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        if addr == COUNT:
            self.trace.append("n")
        elif addr == GET:
            self.trace.append("g%d" % s32(uc.reg_read(UC_X86_REG_RCX)))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", SUBJ)
    if entry == SUBJ:
        uc.reg_write(UC_X86_REG_RCX, 0 if case.get("null_rec") else REC)
    else:
        uc.reg_write(UC_X86_REG_RCX,
                     case.get("index", 0) & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(entry, RETQ, count=100_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX)}
    return " ".join(w.trace) or "-", w.faults, w, obs


# ---- model -------------------------------------------------------------------

def model(case):
    """Expected trace + return from the shipped semantics."""
    base = case.get("base", POOL)
    count = s32(case.get("count", 0))
    matches = case.get("matches", [])
    tr = []
    if case.get("entry", SUBJ) == GET:
        i = s32(case.get("index", 0))
        tr.append("g%d" % i)
        ret = 0 if i < 0 or i > count - 1 else base + i * STRIDE
        return " ".join(tr), {"ret": ret}, None
    if case.get("entry", SUBJ) == COUNT:
        return "n", {"ret": count & 0xFFFFFFFF}, None
    if case.get("null_rec"):
        return "-", {"ret": 0}, None
    ret = 0
    fault = None
    tr.append("n")
    i = 0
    while i < count:
        tr.append("g%d" % i)
        u = 0 if i < 0 or i > count - 1 else base + i * STRIDE
        if u:
            if not (HEAP <= u + MATCH < HEAP + 0x1000000):
                fault = "MEM"
                break
            if i < len(matches) and matches[i] == REC:
                ret = u
                break
            # any other value fails the compare; fixture plants qw only
            # where a match is intended, else the row reads zero
        i += 1
        tr.append("n")
    return " ".join(tr), {"ret": ret}, fault


# ---- cases --------------------------------------------------------------------

def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # subject path
    A("null-rec", null_rec=True)
    A("count0", count=0)
    A("count-neg", count=0xFFFFFFFE)
    A("hit0", count=3, matches=[REC, 0, 0])
    A("hit-mid", count=5, matches=[0, 0, REC, 0, 0])
    A("hit-last", count=4, matches=[0, 0, 0, REC])
    A("miss-all", count=3, matches=[0, 0, 0])
    A("miss-adjacent", count=2, matches=[REC + 8, REC - 0xF50])
    A("miss-low32", count=1,
      matches=[(REC & 0xFFFFFFFF) | 0x1111111100000000])
    A("hit-dup-first", count=3, matches=[REC, REC, REC])
    A("base-null-c1", base=0, count=1)
    A("base-null-fault", base=0, count=2)
    # direct getter calls: the refusal arm the subject's loop never reaches
    A("getter-neg", entry=GET, count=3, index=0xFFFFFFFF)
    A("getter-neg-huge", entry=GET, count=3, index=0x80000000)
    A("getter-at-count", entry=GET, count=3, index=3)
    A("getter-over", entry=GET, count=3, index=12)
    A("getter-last", entry=GET, count=4, index=3)
    A("getter0-empty", entry=GET, count=0, index=0)
    # direct count read
    A("count-read", entry=COUNT, count=7)
    return C


# ---- mutants -------------------------------------------------------------------

MUTANTS = [
    ("m-nullrec", 0x31B86C, b"\xeb",
     "null-rec jne -> jmp: rcx=0 still scans the pool"),
    ("m-cmpneq",  0x31B899, b"\x75",
     "match je -> jne: first NON-matching unit is returned"),
    ("m-off698",  0x31B895, b"\x99\x06\x00\x00",
     "match offset 0x698 -> 0x699: compare reads a shifted qword"),
    ("m-off690",  0x31B895, b"\x90\x06\x00\x00",
     "match offset 0x698 -> 0x690: compare reads the wrong field"),
    ("m-missret", 0x31B8A6, b"\x8b\xc3",
     "miss xor eax,eax -> mov eax,ebx: miss returns the count"),
    ("m-looplt",  0x31B8A4, b"\x7e",
     "loop jl -> jle: one extra getter call past count-1"),
    ("m-js",      0x236822, b"\x79",
     "getter js -> jns: negative index returns a pre-pool pointer"),
    ("m-jg",      0x23682E, b"\x7d",
     "getter jg -> jge: the last in-range index is refused"),
    ("m-dec",     0x23682A, b"\x90\x90",
     "getter dec eax removed: bound becomes i>count not i>count-1"),
    ("m-stride",  0x236836, b"\x40\x0f\x00\x00",
     "unit stride 0xF50 -> 0xF40: elements read off-grid"),
    ("m-getbase", 0x23683D, b"\x4f\x7e\xe5\x01",
     "pool base [0x208E688] -> [0x208E690]: decoy pool scanned"),
    ("m-countsrc",0x236852, b"\x4e\x7e\xe5\x01",
     "count [0x208E6A0] -> [0x208E6A4]: decoy count bounds the scan"),
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
        ok = bool(tr == exp_tr and bool(mem_faults) == bool(exp_fault)
                  and (exp_fault or obs["ret"] == exp_obs["ret"]))
        npass += ok
        nfail += (not ok)
        results[case["name"]] = (tr, obs, bool(mem_faults))
        if not ok:
            print("FAIL %s\n  got:  %s ret=%x fault=%s\n  want: %s ret=%x fault=%s"
                  % (case["name"], tr, obs["ret"], mem_faults,
                     exp_tr, exp_obs["ret"], exp_fault))
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
