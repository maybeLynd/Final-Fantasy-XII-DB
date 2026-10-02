"""rv_queue.py - FABLE independent re-derivation for ASTRA packet ov42-queue-output-alias (4fe271b46).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the filecache-route2-commit-key review).  Does not
import ASTRA's prove.py, control.py, freeze/publication scripts or the shared role adapter (reg_tracking.py).
Method: complete linear decode of the queue primitive 00309C00 (no .pdata record: bounded by its closed local CFG,
its final ret and int3 padding on both sides) and of the script bridge 00348330 (one .pdata record); local CFGs from
rvlib.Body; the reviewer's own concrete walk of the primitive over the 8 partitions (queue available x RDX null x RCX
null); register-carrier census for the bridge's two destinations; a byte-level simulation of the two output stores
in the order the image puts them, compared with the packet's nine arithmetic countermodels.  Controls patch a
private in-memory copy of the image and require at least one named check to fail.
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest, find_exe, fam, SHA256 as SHA_PIN  # noqa: E402

PRIM = (0x00309C00, 0x00309C32)    # queue primitive, 50 B, no .pdata
BRIDGE = (0x00348330, 0x003483D5)  # script bridge, 165 B, one .pdata record
QUEUE = 0x022C2178
UNIT = 0x022C218C
SLUG = "ov42-queue-output-alias"
MANIFEST_SHA = "44d660e4e849ee60dfb50a3a9bbde0beafdae41eab667020a775d05d527ec382"
PRODUCER = "4fe271b46"


class Rep(Report):
    def __init__(self, title):
        Report.__init__(self, title)
        self.n = 0
        self.failed = []

    def check(self, name, cond, detail=""):
        self.n += 1
        if not cond:
            self.failed.append(name)
        return Report.check(self, name, cond, detail)


class _Missing(object):
    """Stands in for an instruction boundary that a patched image no longer has, so a check FAILS by name."""
    def __init__(self, a):
        self.address, self.size, self.mnemonic, self.op_str, self.text = a, 1, "", "", "<no boundary>"
        self.mems = [{"base": None, "index": None, "scale": 1, "disp": 0, "size": 0, "read": False, "write": False,
                      "cs_write": False}]
        self.imm, self.reg_reads, self.reg_writes, self.bytes = [], set(), set(), b""

    def direct_target(self):
        return None


def X(B, a):
    return B.ins.get(a) or _Missing(a)


def T(B, a):
    I = B.ins.get(a)
    return I.text if I else "<no boundary>"


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def writers(B, fam, lo=None, hi=None):
    return [a for a in B.order if fam in B[a].reg_writes and (lo is None or lo <= a) and (hi is None or a < hi)]


def walk_primitive(B, queue_val, rdx, rcx):
    """Reviewer's own concrete walk of the primitive.  Registers hold concrete values; memory reads of the two
    globals return queue_val / 0x89ABCDEF; branches are evaluated from the last cmp/test.  Returns
    (events, eax at ret).  events = list of ('W'|'R', address-or-register-name, value-or-None) in program order."""
    regs = {"rax": 0xDEADBEEF, "rcx": rcx, "rdx": rdx}
    globs = {QUEUE: queue_val, UNIT: 0x89ABCDEF}
    flags = None
    pc = B.start
    ev = []
    steps = 0
    while steps < 64:
        steps += 1
        I = B[pc]
        m, ops = I.mnemonic, I.op_str
        nxt = pc + I.size
        if m == "ret":
            return ev, regs["rax"] & 0xFFFFFFFF
        if m == "mov" and I.mems and I.mems[0]["write"]:
            mm = I.mems[0]
            val = I.imm[0] & 0xFFFFFFFF if I.imm else regs["rax"] & 0xFFFFFFFF
            tgt = rip_target(I) if mm["base"] == "rip" else ("[%s]" % mm["base"], regs[mm["base"]])
            ev.append(("W", tgt, val, mm["size"]))
        elif m == "mov" and I.mems and ops.startswith("eax, "):
            tgt = rip_target(I)
            ev.append(("R", tgt, None, I.mems[0]["size"]))
            regs["rax"] = globs.get(tgt, 0)
        elif m == "mov" and I.imm:
            regs["rax"] = I.imm[0] & 0xFFFFFFFF
        elif m == "xor" and ops == "eax, eax":
            regs["rax"] = 0
        elif m == "cmp" and ops == "eax, -1":
            flags = (regs["rax"] & 0xFFFFFFFF) == 0xFFFFFFFF
        elif m == "cmp" and ops.startswith("eax, "):
            flags = (regs["rax"] & 0xFFFFFFFF) == (I.imm[0] & 0xFFFFFFFF)
        elif m == "test" and fam(ops.split(",")[0]) in regs:
            r = fam(ops.split(",")[0])
            flags = (regs[r] & (0xFFFFFFFF if ops.startswith("e") else 0xFFFFFFFFFFFFFFFF)) == 0
        elif m in ("je", "jne"):
            taken = flags if m == "je" else not flags
            if taken:
                nxt = I.direct_target()
        else:
            ev.append(("?", I.text, None, 0))
        pc = nxt
        if pc not in B.ins:
            return ev, None
    return ev, None


def simulate(order, delta, action_val, unit_val, pre=b"\x00" * 16):
    """Byte simulation of the two output stores in the given program order; returns the final 4 action bytes."""
    mem = bytearray(32)
    A = 12
    U = A + delta
    for who in order:
        if who == "action":
            mem[A:A + 4] = struct.pack("<I", action_val)
        else:
            mem[U:U + 4] = struct.pack("<I", unit_val)
    return bytes(mem[A:A + 4])


def checks(img, R):
    P = Body(img, *PRIM)
    G = Body(img, *BRIDGE)

    # ---------------- bodies ----------------
    s, e = PRIM
    nx = e
    while img.read(nx, 1) == b"\xcc":
        nx += 1
    rets, tails, outs = P.exits()
    R.check("primitive 00309C00 + 0x32 (50 B) decodes exactly into 15 instructions; no .pdata covers it; int3 before "
            "entry and after the last ret", P.exact and len(P.order) == 15 and img.pdata(s) is None and
            img.pdata(e - 1) is None and img.read(s - 1, 1) == b"\xcc" and nx - e >= 1,
            "%d insns, int3 run after = %d B" % (len(P.order), nx - e))
    R.check("primitive local CFG closed: no call, no tail or out-of-body branch; two rets, 309C0D (unavailable) and "
            "309C31 (the last instruction)", not P.calls() and not tails and not outs and
            rets == [0x309C0D, 0x309C31] and P.order[-1] == 0x309C31, "rets=%s" % ["%X" % x for x in rets])
    ents, ok = img.pdata_cover(*BRIDGE)
    R.check("bridge 00348330 + 0xA5 (165 B) decodes exactly into 42 instructions and one .pdata record covers it "
            "exactly (%s)" % ",".join("%08X+0x%X fl%d" % (b, en - b, fl) for b, en, fl, rt in ents),
            G.exact and ok and len(ents) == 1 and len(G.order) == 42, "%d insns" % len(G.order))
    rets, tails, outs = G.exits()
    R.check("bridge local CFG has no conditional branch, no ret, and one exit: the tail jump 3483D0 -> 26B4E0",
            not rets and tails == [(0x3483D0, 0x26B4E0)] and not outs and
            not [a for a in G.order if G[a].mnemonic.startswith("j") and G[a].mnemonic != "jmp"], str(tails))

    # ---------------- primitive: availability test and unavailable arm ----------------
    R.check("309C00 `mov eax, dword ptr [rip + ...]` reads DWORD 022C2178 (4 B)",
            X(P, 0x309C00).mnemonic == "mov" and rip_target(X(P, 0x309C00)) == QUEUE and X(P, 0x309C00).mems[0]["size"] == 4
            and not X(P, 0x309C00).mems[0]["write"])
    R.check("309C06 `cmp eax, -1` (32-bit, against FFFFFFFF), 309C09 `jne 0x309c0e`; equality falls to the "
            "unavailable arm", T(P, 0x309C06) == "cmp eax, -1" and T(P, 0x309C09) == "jne 0x309c0e")
    un = P.reach(0x309C0B)
    R.check("unavailable arm 309C0B `xor eax, eax`, 309C0D ret: no memory write, no call, return DWORD 0",
            T(P, 0x309C0B) == "xor eax, eax" and un == {0x309C0B, 0x309C0D} and
            not [a for a in un for m in P[a].mems if m["write"]])

    # ---------------- primitive: available arm ----------------
    R.check("309C0E `test rdx, rdx`, 309C11 `je 0x309c15` skips only the action store 309C13",
            T(P, 0x309C0E) == "test rdx, rdx" and T(P, 0x309C11) == "je 0x309c15" and
            0x309C11 in P.ins and P.succ(0x309C11) == [0x309C13, 0x309C15])
    R.check("309C13 `mov dword ptr [rdx], eax` stores the queue DWORD (4 B); eax still the 309C00 load (no rax writer "
            "on the 309C00 -> 309C0E -> 309C13 path)", T(P, 0x309C13) == "mov dword ptr [rdx], eax" and X(P, 0x309C13).mems[0]["size"] == 4 and
            writers(P, "rax", 0x309C01, 0x309C0B) == [] and writers(P, "rax", 0x309C0E, 0x309C13) == [] and
            P.dominates(0x309C0E, 0x309C13))
    R.check("309C15 `test rcx, rcx`, 309C18 `je 0x309c22` skips the unit load and store",
            T(P, 0x309C15) == "test rcx, rcx" and T(P, 0x309C18) == "je 0x309c22")
    R.check("309C1A reads DWORD 022C218C (4 B), 309C20 `mov dword ptr [rcx], eax` stores it (4 B)",
            rip_target(X(P, 0x309C1A)) == UNIT and X(P, 0x309C1A).mems[0]["size"] == 4 and
            T(P, 0x309C20) == "mov dword ptr [rcx], eax" and X(P, 0x309C20).mems[0]["size"] == 4)
    rd = [a for a in P.order for m in P[a].mems if not m["write"] and m["base"] == "rip" and rip_target(P[a]) == UNIT]
    st = [a for a in P.order for m in P[a].mems if m["write"] and m["base"] == "rdx"]
    R.check("order: the only 022C218C read (309C1A) comes after the only RDX store (309C13) in the straight available "
            "arm, and 309C13 is not reachable from it", rd == [0x309C1A] and st == [0x309C13] and
            0x309C13 not in P.reach(0x309C1A) and 0x309C1A in P.reach(0x309C13), "reads %s stores %s" %
            (["%X" % x for x in rd], ["%X" % x for x in st]))
    R.check("309C22 resets DWORD 022C2178 to FFFFFFFF (4 B); it post-dominates both output stores and dominates the "
            "309C31 ret", rip_target(X(P, 0x309C22)) == QUEUE and X(P, 0x309C22).imm and
            (X(P, 0x309C22).imm[0] & 0xFFFFFFFF) == 0xFFFFFFFF and X(P, 0x309C22).mems[0]["size"] == 4 and
            P.dominates(0x309C22, 0x309C31, entry=0x309C0E) and 0x309C31 not in P.reach(0x309C13, avoid=[0x309C22])
            and 0x309C31 not in P.reach(0x309C20, avoid=[0x309C22]))
    R.check("return DWORD 1: 309C2C `mov eax, 1` is the last rax writer before 309C31 and dominates it",
            T(P, 0x309C2C) == "mov eax, 1" and writers(P, "rax", 0x309C2D, 0x309C31) == [] and
            P.dominates(0x309C2C, 0x309C31))
    allw = sorted((a, m["base"], m["size"]) for a, m in P.mem_writes())
    R.check("primitive writes memory at exactly three sites: 309C13 [rdx], 309C20 [rcx], 309C22 the queue (all 4 B); "
            "no rbx/rsi/rsp write", allw == [(0x309C13, "rdx", 4), (0x309C20, "rcx", 4), (0x309C22, "rip", 4)] and
            not [a for a in P.order if P[a].reg_writes & {"rbx", "rsi", "rsp"} and P[a].mnemonic != "ret"],
            str([("%X" % a, b, s_) for a, b, s_ in allw]))

    # ---------------- primitive: reviewer's own 8 partitions ----------------
    parts = []
    for avail in (False, True):
        for an in (False, True):
            for un_ in (False, True):
                ev, eax = walk_primitive(P, 0x12F if avail else 0xFFFFFFFF, 0x1000 if an else 0, 0x2000 if un_ else 0)
                w = [x for x in ev if x[0] == "W"]
                parts.append((avail, an, un_, w, eax, [x for x in ev if x[0] == "?"]))
    okp = True
    det = []
    for avail, an, un_, w, eax, unk in parts:
        exp = []
        if avail:
            if an:
                exp.append((("[rdx]", 0x1000), 0x12F))
            if un_:
                exp.append((("[rcx]", 0x2000), 0x89ABCDEF))
            exp.append((QUEUE, 0xFFFFFFFF))
        got = [(t, v) for _, t, v, sz in w]
        good = got == exp and eax == (1 if avail else 0) and not unk
        okp = okp and good
        det.append("%s%s%s:%d writes,eax=%s" % ("A" if avail else "u", "D" if an else "-", "C" if un_ else "-",
                                                len(got), eax))
    R.check("own walk of all 8 partitions: unavailable -> no writes, EAX 0; available -> [rdx] = queue DWORD if RDX "
            "nonnull, then [rcx] = unit DWORD if RCX nonnull, then queue = FFFFFFFF, EAX 1", okp, " ".join(det))
    both_null = [p for p in parts if p[0] and not p[1] and not p[2]][0]
    R.check("both outputs NULL with the queue available: no output write, queue still reset, EAX 1 (value consumed)",
            [(t, v) for _, t, v, s_ in both_null[3]] == [(QUEUE, 0xFFFFFFFF)] and both_null[4] == 1)

    # ---------------- overlap algebra (order taken from the image) ----------------
    order = []
    for a in P.order:
        for m in P[a].mems:
            if m["write"] and m["base"] in ("rdx", "rcx"):
                order.append("action" if m["base"] == "rdx" else "unit")
    rs = json.load(open(os.path.join(ev_dir(), "result-02.json")))
    cms = rs["facts"]["arithmetic_countermodels"]
    bad = []
    for c in cms:
        d = c["unit_pointer_minus_action_pointer"]
        av = struct.unpack("<I", bytes.fromhex(c["initial_action_hex"]))[0]
        uv = struct.unpack("<I", bytes.fromhex(c["unit_hex"]))[0]
        fin = simulate(order, d, av, uv)
        ov = max(0, 4 - abs(d))
        formula = bytes((struct.pack("<I", uv)[j - d] if 0 <= j - d < 4 else struct.pack("<I", av)[j]) for j in range(4))
        if fin.hex() != c["final_action_bytes"] or struct.unpack("<I", fin)[0] != c["final_action_DWORD"] or \
                ov != c["overlap_bytes"] or formula != fin:
            bad.append(d)
    R.check("the packet's 9 countermodels (delta -4..+4) equal the reviewer's byte simulation of the image's store "
            "order %s, and its byte formula" % order, len(cms) == 9 and order == ["action", "unit"] and not bad,
            "mismatch at deltas %s" % bad)
    R.check("same buffer (delta 0) leaves the unit DWORD in the action view; |delta| >= 4 preserves the action DWORD",
            simulate(order, 0, 0x12F, 0x89ABCDEF) == struct.pack("<I", 0x89ABCDEF) and
            all(simulate(order, d, 0x12F, 0x89ABCDEF) == struct.pack("<I", 0x12F) for d in (-8, -4, 4, 8)))

    # ---------------- bridge ----------------
    R.check("bridge frame: three home-slot saves (rbx, rbp, rsi) + push rdi + sub 20h; restores at 3483BC..3483CF",
            [T(G, a) for a in (0x348330, 0x348335, 0x34833A, 0x34833F, 0x348340)] ==
            ["mov qword ptr [rsp + 8], rbx", "mov qword ptr [rsp + 0x10], rbp", "mov qword ptr [rsp + 0x18], rsi",
             "push rdi", "sub rsp, 0x20"] and
            [T(G, a) for a in (0x3483BC, 0x3483C1, 0x3483C6, 0x3483CB, 0x3483CF)] ==
            ["mov rbx, qword ptr [rsp + 0x30]", "mov rbp, qword ptr [rsp + 0x38]", "mov rsi, qword ptr [rsp + 0x40]",
             "add rsp, 0x20", "pop rdi"])
    R.check("the action destination: 348363 call 2650B0, 34836B `mov rsi, rax`, 348381 `mov rdx, rsi` -> RDX at the "
            "34838A call", X(G, 0x348363).direct_target() == 0x2650B0 and T(G, 0x34836B) == "mov rsi, rax" and
            T(G, 0x348381) == "mov rdx, rsi" and writers(G, "rsi") == [0x34836B, 0x3483C6] and
            writers(G, "rdx", 0x348382, 0x34838A) == [], str(["%X" % x for x in writers(G, "rsi")]))
    R.check("the unit destination: 34837C call 2650B0, 348384 `mov rcx, rax`, 348387 `mov rbx, rax` -> RCX at the "
            "call and RBX hold the same value", X(G, 0x34837C).direct_target() == 0x2650B0 and
            T(G, 0x348384) == "mov rcx, rax" and T(G, 0x348387) == "mov rbx, rax" and
            writers(G, "rbx") == [0x348352, 0x348387, 0x3483BC] and
            writers(G, "rax", 0x348385, 0x34838A) == [] and writers(G, "rcx", 0x348385, 0x34838A) == [] and
            X(G, 0x34838A).direct_target() == PRIM[0], str(["%X" % x for x in writers(G, "rbx")]))
    R.check("both destination selectors come from 267E10 on the same VM argument source (rdi = incoming r9) and the "
            "same rbp/rbx context", X(G, 0x348355).direct_target() == 0x267E10 and X(G, 0x34836E).direct_target() == 0x267E10
            and T(G, 0x348344) == "mov rdi, r9" and T(G, 0x348347) == "mov rbp, rcx" and
            T(G, 0x34835D) == "mov rdx, rbp" and T(G, 0x348360) == "mov rcx, rbx" and
            T(G, 0x348376) == "mov rdx, rbp" and T(G, 0x348379) == "mov rcx, rbx")
    R.check("3483A9 `mov ecx, dword ptr [rbx]` reads the unit destination (4 B); 3483B1 `mov ecx, dword ptr [rsi]` "
            "reads the action destination (4 B)", T(G, 0x3483A9) == "mov ecx, dword ptr [rbx]" and
            T(G, 0x3483B1) == "mov ecx, dword ptr [rsi]" and X(G, 0x3483A9).mems[0]["size"] == 4 and
            X(G, 0x3483B1).mems[0]["size"] == 4)
    seg = [a for a in G.order if 0x34838F <= a <= 0x3483B1]
    R.check("from the call's return 34838F to 3483B1: straight line (%d insns), no branch, no call, no rbx/rsi writer; "
            "EAX is only copied to EDX (348395), never tested" % len(seg),
            all(G.succ(a) == [a + G[a].size] for a in seg[:-1]) and
            not [a for a in seg if G[a].mnemonic.startswith("j") or G[a].mnemonic == "call"] and
            not [a for a in seg if G[a].reg_writes & {"rbx", "rsi"}] and
            [a for a in seg if "rax" in G[a].reg_reads] == [0x348395] and T(G, 0x348395) == "mov edx, eax")
    R.check("3483A9 and 3483B1 are dominated by the 34838A call and reached on every normal return of it",
            G.dominates(0x34838A, 0x3483A9) and G.dominates(0x34838A, 0x3483B1) and
            {0x3483A9, 0x3483B1} <= G.reach(0x34838F))
    gw = [(a, rip_target(G[a])) for a, m in G.mem_writes() if m["base"] == "rip"]
    R.check("the two reads are copied to globals 01EF920C and 01EF9214, whose previous values are first shifted to "
            "01EF9208 and 01EF9210", [(a, t) for a, t in gw] == [(0x348397, 0x1EF9208), (0x3483A3, 0x1EF9210),
                                                                  (0x3483AB, 0x1EF920C), (0x3483B3, 0x1EF9214)] and
            rip_target(X(G, 0x34838F)) == 0x1EF920C and rip_target(X(G, 0x34839D)) == 0x1EF9214,
            str([("%X" % a, "%X" % t) for a, t in gw]))
    R.check("the bridge writes no memory through rbx or rsi (only stack home slots and the four globals)",
            all(m["base"] in ("rsp", "rip") for a, m in G.mem_writes()))
    R.check("the primitive's EAX reaches the tail callee as EDX: 348395 `mov edx, eax`, no rdx writer before the "
            "3483D0 jump, rcx = rbp (3483B9)", writers(G, "rdx", 0x348396, 0x3483D0) == [] and
            T(G, 0x3483B9) == "mov rcx, rbp")


def ev_dir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))),
                        "FFXII TZA", "_experiments", "evidence", SLUG)


def packet_checks(img, R):
    ev = ev_dir()
    got = []
    mism = []
    for f, n in (("spattack-queue-reader-raw-01.json", 15), ("spattack-info-raw-01.json", 42)):
        d = json.load(open(os.path.join(ev, f)))
        for r in d["ranges"]:
            s_, e_ = int(r["start"], 16), int(r["end_exclusive"], 16)
            got.append((s_, e_))
            if hashlib.sha256(img.read(s_, e_ - s_)).hexdigest() != r["sha256"] or len(r["instructions"]) != n:
                mism.append(r["start"])
            for ins in r["instructions"]:
                if img.read(int(ins["pc"], 16), len(ins["bytes"]) // 2).hex() != ins["bytes"]:
                    mism.append(ins["pc"])
    R.check("packet raw ranges equal this image: 309C00..309C32 (15 records) and 348330..3483D5 (42 records), range "
            "sha256 and every instruction's bytes", not mism and got == [PRIM, BRIDGE], str(mism))
    rs = json.load(open(os.path.join(ev, "result-02.json")))
    bad = [p["path"] for p in rs["input_pins"] + rs["source_pins"]
           if hashlib.sha256(open(os.path.join(ev, p["path"]), "rb").read()).hexdigest() != p["sha256"]]
    R.check("result-02 input/source pins hash as listed (%d pins)" % len(rs["input_pins"] + rs["source_pins"]),
            not bad and rs["exe_sha256"] == SHA_PIN, str(bad))
    rel = "Database/FFXII TZA/_experiments/evidence/%s/manifest.json" % SLUG
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(find_exe())))))
    blob = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (PRODUCER, rel)], capture_output=True).stdout
    R.check("committed manifest at %s hashes to the same sha256" % PRODUCER,
            hashlib.sha256(blob).hexdigest() == MANIFEST_SHA, hashlib.sha256(blob).hexdigest())
    rd = open(os.path.join(ev, "README.md"), encoding="utf-8").read()
    R.check("README states no bridge byte total and calls the eight partitions logical, not native calls",
            "215" not in rd and "they are not eight native calls" in rd)
    # direct callers of the primitive (raw E8/E9 over .text)
    hits = []
    for name, sva, vs, ra, rs_ in img.secs:
        if name == ".text":
            d = img.d[ra:ra + rs_]
            for i in range(len(d) - 5):
                if d[i] in (0xE8, 0xE9) and img.base + sva + i + 5 + struct.unpack_from("<i", d, i + 1)[0] == PRIM[0]:
                    hits.append(img.base + sva + i)
    R.note("raw E8/E9 references to 00309C00 in .text: %s (direct only; not an indirect-caller census)" %
           ["%X" % h for h in hits])
    B2 = Body(img, 0x2D616B, 0x2D617A)
    R.check("the other direct caller passes two stack locals 20h apart: 2D616B `lea rdx, [rsp + 0x20]`, 2D6170 "
            "`lea rcx, [rsp + 0x40]`, 2D6175 call", hits == [0x2D6175, 0x34838A] and
            T(B2, 0x2D616B) == "lea rdx, [rsp + 0x20]" and T(B2, 0x2D6170) == "lea rcx, [rsp + 0x40]" and
            X(B2, 0x2D6175).direct_target() == PRIM[0])


CONTROLS = [
    ("309C06 `cmp eax, -1` -> `cmp eax, 0` (wrong sentinel)", 0x309C08, bytes([0x00])),
    ("309C0B `xor eax, eax` -> `mov [rdx], eax` (the unavailable arm writes an output)", 0x309C0B, bytes.fromhex("8902")),
    ("309C11 `je` -> `jne` (reversed action null guard)", 0x309C11, bytes([0x75])),
    ("309C13 `mov [rdx], eax` -> `mov [rcx], eax` (action store retargeted)", 0x309C13, bytes.fromhex("8901")),
    ("309C20 `mov [rcx], eax` -> `mov [rdx], eax` (unit store into the action destination)", 0x309C20,
     bytes.fromhex("8902")),
    ("309C22 reset value FFFFFFFF -> 00000000", 0x309C28, bytes(4)),
    ("309C2C `mov eax, 1` -> `mov eax, 0` (available arm returns 0)", 0x309C2D, bytes(4)),
    ("309C0E..309C21 rewritten (20 B, guards narrowed to 32-bit tests) to load 022C218C into r8d BEFORE the action store", 0x309C0E, None),
    ("34838F: `test eax, eax; je 3483B9` inserted (bridge reads made conditional on the result)", 0x34838F,
     bytes.fromhex("85C07426") + b"\x90\x90"),
    ("348387 `mov rbx, rax` -> `mov rbx, rsi` (RBX no longer the unit destination)", 0x348387,
     bytes.fromhex("488BDE")),
    ("3483B1 `mov ecx, [rsi]` -> `mov ecx, esi` (action destination no longer read)", 0x3483B1,
     bytes.fromhex("8BCE")),
]


def reorder_bytes():
    # mov r8d,[rip+X]; test edx,edx; je +2; mov [rdx],eax; test ecx,ecx; je +3; mov [rcx],r8d   (20 B, fits)
    base = 0x309C0E
    disp = UNIT - (base + 7)
    b = bytes.fromhex("448B05") + struct.pack("<i", disp)
    b += bytes.fromhex("85D2" "7402" "8902" "85C9" "7403" "448901")
    assert len(b) == 20
    return b


def main():
    img = Img.load()
    R = Rep("rv_queue")
    print("== packet integrity")
    check_manifest(R, SLUG, MANIFEST_SHA)
    packet_checks(img, R)
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    Rn = Rep("null control")
    Rn.quiet = True
    same = img.patched(0x309C00, img.read(0x309C00, 4))
    checks(same, Rn)
    R.check("null control: an unchanged private copy (sha check off) passes every check", Rn.fails == 0 and Rn.n > 0,
            "%d of %d" % (Rn.n - Rn.fails, Rn.n))
    nctl = 0
    for label, va, nb in CONTROLS:
        if nb is None:
            nb = reorder_bytes()
        Pimg = img.patched(va, nb)
        if Pimg.d == img.d:
            raise SystemExit("control %s did not change the image" % label)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(Pimg, Rc)
            failed = Rc.fails
            why = "%d failed: %s" % (failed, "; ".join(Rc.failed))
        except Exception as e:
            failed = 1
            why = "refused: %r" % e
        nctl += 1
        R.check("control: " + label, failed > 0, why)
    disk = hashlib.sha256(open(find_exe(), "rb").read()).hexdigest()
    R.check("exe on disk still hashes to the pinned sha256 after all controls", disk == SHA_PIN, disk)
    print("TOTAL: %d checks, %d PASS, %d FAIL (%d controls)" % (R.n, R.n - R.fails, R.fails, nctl))


if __name__ == "__main__":
    main()
