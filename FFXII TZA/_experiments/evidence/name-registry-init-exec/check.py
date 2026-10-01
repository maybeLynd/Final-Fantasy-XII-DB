# EXP-116 — input-name-registry-init-exec
#
# Executes the real CRT initialiser sequence that builds both input-name
# registries: the insert twins 00879570 (channels) / 00876C80 (keys) and
# the 240 shipped init thunks (97 + 143), each `lea rcx,[static node];
# call insert; lea rcx,[dtor-cb]; jmp 00808B90` run in .CRT-table order
# (link order — shuffled relative to the thunk arrays).  The atexit
# registrar 00808B90 is a scripted boundary: its rcx argument (the dtor
# callback thunk) is traced and the call returns.
#
# The oracle is the produced chain: after each registry's thunks run,
# the list head is walked via node+0x10 and the node-pointer sequence
# is compared against an independent Python simulation of the insert.
# All node objects, name strings and the .CRT order come from shipped
# bytes; nothing is hand-built except injected nodes for the dup/null
# edge cases, which are disclosed.
#
# Both list heads are BSS (no shipped bytes) — the mapped image gives
# the real load-time zero.  Every node+0x10 link is shipped zero.
import ctypes, hashlib, json, os, re, struct
from unicorn import UcError
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import (Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE,
                     UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL)
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RIP,
                               UC_X86_REG_RCX, UC_X86_REG_RAX)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

INSERT_C = 0x00879570    # channels insert — list head 0x2EB9D80
INSERT_K = 0x00876C80    # keys insert — list head 0x2EB83B8
ATE      = 0x00808B90    # atexit registrar — scripted boundary
HEAD_C   = 0x02EB9D80
HEAD_K   = 0x02EB83B8

KTHUNKS = [0x16B5E0 + i * 0x20 for i in range(97)]
CTHUNKS = [0x16C380 + i * 0x20 for i in range(143)]
KTSET, CTSET = set(KTHUNKS), set(CTHUNKS)

# .CRT init-table window (extracted from the image; see init_order)
CRT_LO, CRT_HI = 0x008C4000, 0x008C5C00

# injected-node area for edge cases
FNODE  = HEAP + 0x10000   # fake node (0x20 bytes)
FNAME  = HEAP + 0x20000   # fake name string


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


def img_str(raw, secs, va):
    out = bytearray()
    while True:
        b = img_rd(raw, secs, va + len(out), 1)[0]
        if b == 0:
            return bytes(out)
        out.append(b)


def thunk_node(raw, secs, tv):
    """resolve `lea rcx, [rip + X]` (the static node arg)."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    ins = list(md.disasm(img_rd(raw, secs, tv, 0x20), tv))
    lea = ins[1]
    assert lea.mnemonic == "lea", "thunk %x: expected lea got %s" % (
        tv, lea.mnemonic)
    return lea.address + lea.size + int(
        lea.op_str.split("+")[1].rstrip("]"), 16)


def thunk_dtorcb(raw, secs, tv):
    """resolve the second `lea rcx, [rip + X]` (dtor-callback thunk)."""
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    ins = list(md.disasm(img_rd(raw, secs, tv, 0x20), tv))
    lea = ins[3]
    assert lea.mnemonic == "lea", "thunk %x: expected lea got %s" % (
        tv, lea.mnemonic)
    return lea.address + lea.size + int(
        lea.op_str.split("+")[1].rstrip("]"), 16)


def init_order(raw, secs):
    """.CRT-table order of the 240 registry thunks (link order,
    shuffled relative to the thunk arrays)."""
    order = {"keys": [], "chan": []}
    va = CRT_LO
    while va < CRT_HI:
        q = img_qw(raw, secs, va)
        if q in KTSET:
            order["keys"].append(q)
        elif q in CTSET:
            order["chan"].append(q)
        va += 8
    assert len(order["keys"]) == 97 and len(order["chan"]) == 143
    return order


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

        # injected fake node for edge cases: {vtable, name, next, value}
        gm.w(FNODE, qw(case.get("fvtable", 0xDEAD0000)) +
                   qw(case.get("fname_ptr", FNAME)) +
                   qw(case.get("fnext", 0)) +
                   qw(case.get("fval", 0x77)))
        name = case.get("fname", b"ZetaInj\x00")
        gm.w(FNAME, name + b"\x00" * (64 - len(name)))

        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)

        self.trace, self.faults, self.ins_args = [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr in (INSERT_C, INSERT_K):
            self.ins_args.append(uc.reg_read(UC_X86_REG_RCX))
        elif addr == ATE:
            # scripted boundary: record the dtor-callback arg, return
            self.trace.append("ate:%x" % uc.reg_read(UC_X86_REG_RCX))
            uc.reg_write(UC_X86_REG_RIP, RETQ)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.reg_write(UC_X86_REG_RIP, RETQ)
        return True

    def run_thunk(self, tv):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        # worst case: ~143-node list scan with per-byte name compare
        # (~60 insns/node) plus the 7-insn thunk — 60000 is generous
        try:
            uc.emu_start(tv, RETQ, count=60000)
        except UcError as e:
            self.faults.append(("emuerr", str(e)))

    def run_insert(self, entry, node):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, node)
        try:
            uc.emu_start(entry, RETQ, count=60000)
        except UcError as e:
            self.faults.append(("emuerr", str(e)))
        return uc.reg_read(UC_X86_REG_RAX)

    def run(self):
        for tv in self.case.get("seq", []):
            self.run_thunk(tv)
        for entry, node in self.case.get("direct", []):
            rc = self.run_insert(entry, node)
            self.trace.append("rc:%x" % rc)

    def walk(self, head_va):
        out, seen, cur = [], set(), self.gm.qw(head_va)
        while cur and cur not in seen and len(out) < 400:
            out.append(cur)
            seen.add(cur)
            try:
                cur = self.gm.qw(cur + 0x10)
            except KeyError:
                self.faults.append(("wildnext", cur))
                break
        return out

    def obs(self):
        return {"trace": self.trace, "faults": self.faults,
                "ins": self.ins_args,
                "chan": self.walk(HEAD_C), "keys": self.walk(HEAD_K),
                "head_c": self.gm.qw(HEAD_C),
                "head_k": self.gm.qw(HEAD_K)}


# ---------------- Python model ----------------

def run_model(case, raw, secs):
    """Expected observables: chains + trace + ins args."""
    order = init_order(raw, secs)
    allnodes = {tv: thunk_node(raw, secs, tv)
                for tv in KTHUNKS + CTHUNKS}
    # shipped memory: image bytes with node+0x10 writes applied
    def ship_qw(va):
        return img_qw(raw, secs, va)
    heads = {"chan": 0, "keys": 0}
    link = {}                      # addr -> stored qword
    exp_trace, exp_ins = [], []
    seq = case.get("seq", [])
    for tv in seq:
        node = allnodes[tv]
        exp_ins.append(node)
        which = "chan" if tv in CTSET else "keys"
        def mem(va):
            return link.get(va, ship_qw(va))
        name_p = mem(node + 8)
        code = 0
        if name_p == 0:
            code = 0x11
        else:
            cur = heads[which]
            while cur:
                a, b = mem(cur + 8), name_p
                sa = img_str(raw, secs, a) if a else b""
                sb = img_str(raw, secs, b) if b else b""
                if sa == sb:
                    code = 0x12
                    break
                cur = mem(cur + 0x10)
        if code == 0:
            link[node + 0x10] = heads[which]
            heads[which] = node
        exp_trace.append("ate:%x" % thunk_dtorcb(raw, secs, tv))
    # direct-insert cases on the post-seq state
    fnode = case.get("fnode", FNODE)
    for entry, node in case.get("direct", []):
        exp_ins.append(node)
        which = "chan" if entry == INSERT_C else "keys"
        def mem(va):
            return link.get(va, ship_qw(va))
        name_p = case.get("fname_ptr", FNAME) if node == fnode \
            else mem(node + 8)
        code = 0
        if name_p == 0:
            code = 0x11
        else:
            def cstr_of(p):
                if p == FNAME:
                    return case.get("fname", b"ZetaInj\x00").split(b"\x00")[0]
                return img_str(raw, secs, p) if p else b""
            cur = heads[which]
            while cur:
                if cstr_of(mem(cur + 8)) == cstr_of(name_p):
                    code = 0x12
                    break
                cur = mem(cur + 0x10)
        if code == 0:
            link[node + 0x10] = heads[which]
            heads[which] = node
        exp_trace.append("rc:%x" % code)

    def model_walk(which):
        out, cur = [], heads[which]
        seen = set()
        while cur and cur not in seen and len(out) < 400:
            out.append(cur)
            seen.add(cur)
            cur = link.get(cur + 0x10, ship_qw(cur + 0x10))
        return out

    return {"trace": exp_trace, "faults": [], "ins": exp_ins,
            "chan": model_walk("chan"), "keys": model_walk("keys"),
            "head_c": heads["chan"], "head_k": heads["keys"]}


# ---------------- cases ----------------

def build_cases(raw, secs):
    order = init_order(raw, secs)
    C = {}
    C["keys-full"] = {"seq": order["keys"]}
    C["channels-full"] = {"seq": order["chan"]}
    C["interleaved"] = {"seq": order["keys"][:8] + order["chan"][:8]}
    # edge cases via direct insert (fresh World per case = empty list)
    C["dup-shipped-name"] = {
        "seq": order["chan"],
        "fname_ptr": None,   # fake node reuses a shipped name
        "direct": [(INSERT_C, None)],  # node resolved in run
    }
    C["dup-shipped-name-keys"] = {
        "seq": order["keys"],
        "fname_ptr": None,
        "direct": [(INSERT_K, None)],
    }
    # copied name at a different address — same bytes, different pointer
    C["dup-copied-name"] = {"seq": order["chan"],
                            "fname": b"Button_0\x00",
                            "direct": [(INSERT_C, None)]}
    C["null-name"] = {"fname_ptr": 0,
                      "direct": [(INSERT_C, None)]}
    C["fresh-insert"] = {"seq": order["chan"][:5],
                         "direct": [(INSERT_C, None)]}
    C["fresh-insert-keys"] = {"seq": order["keys"][:5],
                              "direct": [(INSERT_K, None)]}
    C["cross-list"] = {  # key node inserted into channel head — no type check
        "seq": order["chan"][:4],
        "direct": [(INSERT_C, thunk_node(raw, secs, order["keys"][0]))]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])
def W(x): return struct.pack("<i", x)

MUTS = [
    # NULL-name gate: jne -> je (name==0 falls into the scan -> wild deref)
    ("m-nulljne",   0x87957E, B(0x75), B(0x74), "channels-full"),
    # compare: sub edx,ecx -> add edx,ecx (equality inverted)
    ("m-cmpadd",    0x8795B8, B(0x2B), B(0x03), "dup-shipped-name"),
    # dup exit: je 0x8795e6 -> jne (distinct names get the dup return)
    ("m-dupjne",    0x8795C5, B(0x74), B(0x75), "channels-full"),
    # compare walk: inc rax -> dec rax (walks backward -> wild reads)
    ("m-cmpdec",    0x8795BE, B(0xC0), B(0xC8), "dup-copied-name"),
    # scan loop: jne 0x8795a0 -> je (checks only the head for dup)
    ("m-scanje",    0x8795CE, B(0x75), B(0x74), "dup-shipped-name"),
    # empty-list guard: je 0x8795d0 -> jne (scans from a NULL head)
    ("m-headjne",   0x87959A, B(0x74), B(0x75), "channels-full"),
    # name load disp: [r9+8] -> [r9+0x10] (compares links, not names)
    ("m-namedisp",  0x8795A3, B(0x08), B(0x10), "dup-shipped-name"),
    # scan next disp: [r9+0x10] -> [r9+0x18] (walks values)
    ("m-linkdisp",  0x8795CA, B(0x10), B(0x18), "dup-shipped-name"),
    # insert next-store disp: [r11+0x10] -> [r11+0x18] (writes value)
    ("m-storedisp", 0x8795D3, B(0x10), B(0x18), "channels-full"),
    # head-store target: [0x2EB9D80] disp byte -> writes elsewhere
    ("m-headdisp",  0x8795DD, B(0x9F), B(0xA3), "channels-full"),
    # NULL-name return imm: 0x11 -> 0x12
    ("m-rc11",      0x879583, B(0x11), B(0x12), "null-name"),
    # dup return imm: 0x12 -> 0x11
    ("m-rc12",      0x8795E7, B(0x12), B(0x11), "dup-shipped-name"),
    # ---- INSERT_K twin sites (same logic, head 0x2EB83B8) ----
    ("m-k-cmpadd",  0x876CC8, B(0x2B), B(0x03), "dup-shipped-name-keys"),
    ("m-k-dupjne",  0x876CD5, B(0x74), B(0x75), "keys-full"),
    ("m-k-stored",  0x876CE3, B(0x10), B(0x18), "keys-full"),
    # ---- thunk mutants ----
    # call target: INSERT_C rel32 -> INSERT_K (channel node to key head)
    ("m-t-call",    0x16C38C, W(0x879570 - (0x16C38B + 5)),
                              W(0x876C80 - (0x16C38B + 5)), "channels-full"),
    # lea disp: node arg -> adjacent node (wrong name registers)
    ("m-t-lea",     0x16C387, B(0x7D), B(0x5D), "channels-full"),
]


def run_native(case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    return w.obs()


def main():
    raw, secs = load_image()
    cases = build_cases(raw, secs)
    keys = ("trace", "ins", "chan", "keys", "head_c", "head_k", "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        # resolve deferred node arg for direct inserts
        if case.get("direct"):
            fixed = []
            for entry, node in case["direct"]:
                fixed.append((entry, node if node is not None
                              else FNODE))
            case["direct"] = fixed
            if case.get("fname_ptr") is None:
                # point the fake node's name field at a shipped name —
                # a duplicate of a real registration
                if name == "dup-shipped-name":
                    n0 = thunk_node(raw, secs, CTHUNKS[0])
                    case["fname_ptr"] = img_qw(raw, secs, n0 + 8)
                elif name == "dup-shipped-name-keys":
                    n0 = thunk_node(raw, secs, KTHUNKS[0])
                    case["fname_ptr"] = img_qw(raw, secs, n0 + 8)
        nat = run_native(case, raw, secs)
        mod = run_model(case, raw, secs)
        d = [k for k in keys if k in nat and nat[k] != mod.get(k)]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:170])
                print("  mod:", str(mod.get(k))[:170])
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
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + [(va, mut)]
        try:
            nat = run_native(case, raw, secs)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case, raw, secs)
        if [k for k in keys if k in nat and nat[k] != mod.get(k)]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
