#!/usr/bin/env python3
"""EXP-097 class-descriptor-dtor-exec - the PClass descriptor destructor
00633390 executed as real shipped bytes with its two scripted callees
running real: 0063D640 (+0x70 sub-object registry detach) and 006B6700
(+0x60 intrusive-list drain).

CONTRACT-phyre-class-descriptor.md's destructor pilot
(diff_class_descriptor_dtor.py) ran 00633390 with BOTH callees stubbed:
what they do to the +0x70 sub-object and the +0x60 list is the open
residual. Here they execute real; only the heap stays scripted.

    00633390  subject   REAL - vtable swap 0xD581C0->0xD31168, counter
              guard 0x2CF8260 ([obj+0xE8]+1 == counter -> counter--),
              0063D640(obj, [obj+0x70]), owned-node free walks at
              +0x90/+0xA0 (node+0x20 bit0 = owned: unlink, free(node+0x18
              payload), free(node); unowned nodes skipped), unconditional
              unlink drains at +0x80,+0x90,+0xA0,+0xB0, 006B6700(obj+0x60).
    0063D640  sub-obj   REAL - unlinks the embedded node at rdx+0x50/0x58,
              self-links it; iff obj+0x10's list is empty AND obj != the
              TLS-registered current object, calls 006373D0 a second time
              and unlinks obj's own registry node at obj+0/+8.
    006B6700  list60    REAL - pure unlink-drain of the intrusive
              circular list at rcx; no frees, head self-linked.
    006373D0  tlsctx    REAL - gs:[0x58] -> slot array, idx [0x2EAED3C],
              ctx+4 vs lazy-state [0x2CF94EC] (planted 0 -> no init arm),
              returns the registered object 0x1F2E330.
    00584730  free      SCRIPTED at entry - _aligned_free boundary; logs
              rcx (freed address) in call order. Heap internals are the
              disclosed boundary, exactly as the pilot left them.

Node layout (from the body): intrusive circular list {flink@0, blink@8};
owned-node payload ptr @+0x18, ownership bit = node+0x20 & 1.
List heads are sentinels self-linked {flink=head, blink=head}.

NOT EXERCISED (disclosed): _aligned_free internals, the lazy-init arm of
006373D0 (0x8092FC/0x808B90/0x80929C CRT init machinery), any other
descriptor method, no live process.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
TLS    = 0x63000000

DTOR   = 0x00633390          # class-descriptor destructor
SUBOBJ_FN = 0x0063D640       # +0x70 sub-object registry detach
LIST60_FN = 0x006B6700       # +0x60 list drain
TLSCTX = 0x006373D0          # TLS ctx getter -> 0x1F2E330
FREE_FN = 0x00584730         # _aligned_free thunk (STUB)

VTBL1 = 0x00D581C0           # written at entry
VTBL2 = 0x00D31168           # written at exit
G_COUNTER = 0x02CF8260       # registry counter, guarded decrement
G_TLSIDX = 0x2EAED3C         # dword tls index
G_LAZYST = 0x2CF94EC         # lazy-state dword
CURR_OBJ = 0x1F2E330         # the TLS-registered "current" object

OBJ    = HEAP + 0x000000     # the descriptor under destruction
SUBOBJ = HEAP + 0x010000     # the +0x70 sub-object (node embedded +0x50)
NODES  = HEAP + 0x100000     # node arena (per-list 0x10000, per-node 0x100)
PAYLOAD= HEAP + 0x200000     # owned payload arena
REG    = HEAP + 0x300000     # registry list head (sub-object's node)
OBJREG = HEAP + 0x310000     # list holding obj's embedded +0x50 node

CALLS = {DTOR: "d", SUBOBJ_FN: "S", LIST60_FN: "L", TLSCTX: "T",
         FREE_FN: "F"}
STUBS = {FREE_FN: "F"}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)

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
    iat = []
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt or iat_rva) + 8 * j)[0]
            if e == 0:
                break
            iat.append(0x120000 + iat_rva + 8 * j)
            j += 1
        i += 1
    return raw, secs, iat

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
    def q(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]
    def d(self, addr):
        return struct.unpack("<I", self.r(addr, 4))[0]

class World:
    def __init__(self, case, raw, secs, iat):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x400000), (STACK, 0x100000), (RETQ, 0x1000),
                     (TLS, 0x10000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        for va in STUBS:
            gm.w(va, b"\xc3")
        for slot in iat:
            gm.w(slot, qw(0))

        # TLS: gs base -> TLS; gs:[0x58] -> slot array; slot[idx] -> ctx;
        # ctx+4 > lazy-state [0x2CF94EC]=0 -> skip init, ret CURR_OBJ.
        self.uc.reg_write(UC_X86_REG_GS_BASE, TLS)
        gm.w(TLS + 0x58, qw(TLS + 0x1000))
        gm.w(G_TLSIDX, dw(3))
        gm.w(TLS + 0x1000 + 3 * 8, qw(TLS + 0x8000))
        gm.w(TLS + 0x8000 + 4, dw(4))
        gm.w(G_LAZYST, dw(0))

        obj = case.get("obj", OBJ)
        self.obj = obj
        gm.w(G_COUNTER, dw(case.get("counter", 5)))
        gm.w(obj + 0xE8, dw(case.get("counter_field", 5)))

        # obj's embedded list node at +0x50/+0x58 (0063D640 unlinks it
        # from whatever list owns it)
        if case.get("objnode_linked"):
            gm.w(OBJREG, qw(obj + 0x50)); gm.w(OBJREG + 8, qw(obj + 0x50))
            gm.w(obj + 0x50, qw(OBJREG)); gm.w(obj + 0x58, qw(OBJREG))
        else:
            gm.w(obj + 0x50, qw(obj + 0x50)); gm.w(obj + 0x58, qw(obj + 0x50))

        # the +0x70 sub-object; its member list at +0x10 decides whether
        # the registry detach runs (empty -> compare vs TLS current obj)
        sub = CURR_OBJ if case.get("sub_is_current") else SUBOBJ
        self.sub = sub
        gm.w(obj + 0x70, qw(sub))
        gm.w(sub + 0x10, qw(sub + 0x10)); gm.w(sub + 0x18, qw(sub + 0x10))
        if case.get("sub_members"):
            self._seed_list(gm, sub + 0x10, case["sub_members"], 14)
        # sub-object's registry node at +0/+8 -> REG (unlinked on detach)
        gm.w(REG, qw(sub)); gm.w(REG + 8, qw(sub))
        gm.w(sub + 0, qw(REG)); gm.w(sub + 8, qw(REG))

        for off in (0x60, 0x80, 0x90, 0xA0, 0xB0):
            gm.w(obj + off, qw(obj + off)); gm.w(obj + off + 8, qw(obj + off))
        for li, (off, nodes) in enumerate(case.get("lists", [])):
            self._seed_list(gm, obj + off, nodes, li)

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def _seed_list(self, gm, head, nodes, li):
        prev = head
        for i, (owned, pay) in enumerate(nodes):
            na = NODES + li * 0x10000 + i * 0x100
            gm.w(na + 0x18, qw(pay))
            gm.w(na + 0x20, bytes([owned]))
            gm.w(prev, qw(na))
            gm.w(na + 8, qw(prev))
            prev = na
        if nodes:
            gm.w(prev, qw(head))
            gm.w(head + 8, qw(prev))

    def on_call(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        self.fired.add(addr)
        if addr == FREE_FN:
            self.trace.append("F%x" % (rcx & 0xFFFFFFFF))
            sp = uc.reg_read(UC_X86_REG_RSP)
            back = struct.unpack("<Q", uc.mem_read(sp, 8))[0]
            uc.reg_write(UC_X86_REG_RSP, sp + 8)
            uc.reg_write(UC_X86_REG_RIP, back)
            return
        if addr == SUBOBJ_FN:
            self.trace.append("S%x" % (rcx & 0xFFFFFFFF))
            return
        if addr == LIST60_FN:
            self.trace.append("L%x" % ((rcx - self.obj) & 0xFFFFFFFF))
            return
        self.trace.append(CALLS[addr])

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def run_case(case, raw, secs, iat):
    w = World(case, raw, secs, iat)
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, w.obj)
    try:
        uc.emu_start(DTOR, RETQ, count=2_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    tr = " ".join(w.trace) or "-"
    obs = {
        "vtbl": gm.q(w.obj),
        "counter": gm.d(G_COUNTER),
        "reg_head": (gm.q(REG), gm.q(REG + 8)),
        "subnode": (gm.q(w.sub), gm.q(w.sub + 8)),
        "objnode": (gm.q(w.obj + 0x50), gm.q(w.obj + 0x58)),
        "objreg": (gm.q(OBJREG), gm.q(OBJREG + 8)),
        "heads": {"%x" % off: (gm.q(w.obj + off), gm.q(w.obj + off + 8))
                  for off in (0x60, 0x80, 0x90, 0xA0, 0xB0)},
    }
    return tr, w.faults, w, obs

# ---- cases -------------------------------------------------------------------

def build_cases():
    C = []
    def A(name, trace, obs=None, **kw):
        C.append(dict(kw, name=name, want_trace=trace, want_obs=obs or {}))

    SELF = lambda a: (a, a)
    D = "d S%x T T L60" % SUBOBJ
    BASE_OBS = {"vtbl": VTBL2, "counter": 5, "reg_head": SELF(REG),
                "subnode": SELF(SUBOBJ), "objnode": SELF(OBJ + 0x50),
                "heads": {"60": SELF(OBJ + 0x60), "80": SELF(OBJ + 0x80),
                          "90": SELF(OBJ + 0x90), "a0": SELF(OBJ + 0xA0),
                          "b0": SELF(OBJ + 0xB0)}}
    # empty descriptor: sub+0x10 empty, sub != current -> T,T + detach;
    # every head self-linked; no frees.
    A("empty", D, BASE_OBS)
    # counter guard: field+1 == counter -> decrement
    A("counter-eq", D, dict(BASE_OBS, counter=4), counter_field=4)
    # owned node in +0x90: pass1 frees payload then node; pass2 no-op
    A("l90-owned", "d S%x T T F%x F%x L60" % (SUBOBJ, PAYLOAD, NODES),
      BASE_OBS, lists=[(0x90, [(1, PAYLOAD)])])
    # unowned node in +0x90: pass1 skips, pass2 unlinks; no frees
    A("l90-unowned", D, BASE_OBS, lists=[(0x90, [(0, PAYLOAD)])])
    # mixed +0xA0: unowned skipped then owned freed
    A("la0-mixed", "d S%x T T F%x F%x L60" % (SUBOBJ, PAYLOAD + 8, NODES + 0x100),
      BASE_OBS, lists=[(0xA0, [(0, PAYLOAD), (1, PAYLOAD + 8)])])
    # +0x80 and +0xB0: drain-only, ownership bit ignored, no frees
    A("l80-drain", D, BASE_OBS,
      lists=[(0x80, [(1, PAYLOAD), (1, PAYLOAD + 8)])])
    A("lb0-drain", D, BASE_OBS, lists=[(0xB0, [(1, PAYLOAD)])])
    # +0x60 drain via real 006B6700: unlinks, no frees
    A("l60-drain", D, BASE_OBS, lists=[(0x60, [(0, PAYLOAD), (0, PAYLOAD + 8)])])
    # obj's +0x50 node linked into OBJREG -> real unlink self-links both
    A("objnode-linked", D, dict(BASE_OBS, objreg=SELF(OBJREG)),
      objnode_linked=True)
    # sub+0x10 nonempty -> detach skipped: no T calls, REG keeps sub
    A("sub-members", "d S%x L60" % SUBOBJ,
      dict(BASE_OBS, reg_head=(SUBOBJ, SUBOBJ), subnode=(REG, REG)),
      sub_members=[(0, PAYLOAD)])
    # sub IS the TLS-registered current object -> one T, no detach
    A("sub-current", "d S%x T L60" % CURR_OBJ,
      dict(BASE_OBS, reg_head=(CURR_OBJ, CURR_OBJ),
           subnode=(REG, REG)),
      sub_is_current=True)
    # two owned nodes in +0x90: free order is node0 then node1
    A("l90-two-owned",
      "d S%x T T F%x F%x F%x F%x L60" % (SUBOBJ, PAYLOAD, NODES,
                                        PAYLOAD + 8, NODES + 0x100),
      BASE_OBS, lists=[(0x90, [(1, PAYLOAD), (1, PAYLOAD + 8)])])
    # counter edge: field 0xFFFFFFFF +1 wraps to 0 == counter 0 -> 0xFFFFFFFF
    A("counter-wrap", D, dict(BASE_OBS, counter=0xFFFFFFFF),
      counter=0, counter_field=0xFFFFFFFF)
    # all five lists populated at once
    A("all-lists",
      "d S%x T T F%x F%x F%x F%x L60" % (SUBOBJ, PAYLOAD + 0x10, NODES + 0x20000,
                                        PAYLOAD + 0x18, NODES + 0x30000),
      BASE_OBS,
      lists=[(0x60, [(0, PAYLOAD)]), (0x80, [(1, PAYLOAD + 8)]),
             (0x90, [(1, PAYLOAD + 0x10)]), (0xA0, [(1, PAYLOAD + 0x18)]),
             (0xB0, [(0, PAYLOAD + 0x20)])])
    # obj's +0x50 node linked AND sub has members: node unlinks, no detach
    A("objnode-linked-members", "d S%x L60" % SUBOBJ,
      dict(BASE_OBS, reg_head=(SUBOBJ, SUBOBJ), subnode=(REG, REG),
           objreg=SELF(OBJREG)),
      objnode_linked=True, sub_members=[(0, PAYLOAD)])
    return C

# ---- mutants -----------------------------------------------------------------

MUTANTS = [
    ("m-counteq",  0x6333CF, b"\x74",
     "counter guard jne->je: decrements when NOT equal"),
    ("m-ownbit",   0x633418, b"\x02",
     "owned-node test byte[rbx+0x20],1 -> ,2: owned never freed"),
    ("m-payoff",   0x633439, b"\x10",
     "free payload [rbx+0x18] -> [rbx+0x10]: wrong address freed"),
    ("m-drain90",  0x6334EA, b"\x75",
     "pass2 +0x90 drain je->jne: empty head enters the loop"),
    ("m-sublink",  0x63D655, b"\x90" * 4,
     "subobj unlink mov[rdx+8],rax removed: node half-detached"),
    ("m-regcmp",   0x63D68B, b"\x75",
     "registry-current compare je->jne: detaches the current object"),
    ("m-list60",   0x6B6736, b"\x90" * 4,
     "list60 unlink mov[rcx+8],rax removed: corrupt drain"),
    ("m-vtbl2",    0x633568, b"\x90" * 5,
     "final vtable write removed: object keeps derived vtable"),
    ("m-inc",      0x6333C5, b"\x90" * 2,
     "inc eax removed: counter compare off by one"),
    ("m-selflink", 0x6334F1, b"\x90" * 4,
     "pass2 unlink mov[rcx+8],rax removed: survivors keep stale links"),
]

def main():
    raw, secs, iat = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs, iat)
        ok = tr == case["want_trace"] and not [f for f in faults if f[0] == "MEM"]
        bad_obs = []
        for k, v in case["want_obs"].items():
            if k == "heads":
                for off, want in v.items():
                    if obs["heads"].get(off) != want:
                        bad_obs.append(("heads." + off, obs["heads"].get(off), want))
            elif obs.get(k) != v:
                bad_obs.append((k, obs.get(k), v))
        ok = ok and not bad_obs
        npass += ok; nfail += (not ok)
        if not ok:
            print("FAIL %s\n  got:  %s\n  want: %s\n  obs-bad: %s faults=%s"
                  % (case["name"], tr, case["want_trace"], bad_obs, faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr, "ok": bool(ok),
                             "obs": obs, "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))
    fired = set()
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs, iat)
        fired |= w.fired
    out["bodies_fired"] = ["0x%X" % v for v in sorted(fired)]
    print("fired:", " ".join("%s@%x" % (CALLS[v], v) for v in sorted(fired)))

    base = {c["name"]: (c["trace"], json.dumps(c["obs"], sort_keys=True))
            for c in out["cases"]}
    for name, va, data, why in MUTANTS:
        n_diff = 0; diffs = []
        for case in build_cases():
            c = dict(case); c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs, iat)
            obs_json = json.dumps(obs, sort_keys=True)
            if (tr, obs_json) != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s" % tr))
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
