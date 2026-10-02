"""rv_removal.py - FABLE independent re-derivation for ASTRA packet render-removal-phase-contracts (31f29775a).

Own reader (rvlib.py: struct + capstone 5).  Does not import ASTRA's prove.py or the shared role adapter.
Method: complete linear decode of the three bodies, a local CFG from rvlib.Body, and region / dominance /
straight-line-predecessor checks for every branch and phase claim.  The controls patch a private copy of the
image and require at least one named check to fail.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import Img, Body, Report, check_manifest  # noqa: E402

REM = (0x00429140, 0x004292A6)
SWEEP = (0x00427C90, 0x00427DD8)
CLEAN = (0x004200A0, 0x004201EB)
CLEAR = 0x0041F730
POOL = 0x022C6F28
COUNT, CURSOR, AHEAD, ATAIL, PHEAD, PTAIL, PFLAGS = 0x4880C, 0x48808, 0x48800, 0x48804, 0x48810, 0x48814, 0x48818


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


def rip_target(I):
    m = I.mems[0]
    return I.address + I.size + m["disp"] if m["base"] == "rip" else None


def nonstack_writes(B, addrs):
    out = []
    for a in sorted(addrs):
        for m in B[a].mems:
            if m["write"] and m["base"] != "rsp" and B[a].mnemonic != "lea":
                out.append((a, m))
    return out


def calls_in(B, addrs):
    return [(a, B[a].direct_target()) for a in sorted(addrs) if B[a].mnemonic == "call"]


def branch_targets(B):
    t = set()
    for a in B.order:
        I = B[a]
        if I.mnemonic.startswith("j"):
            x = I.direct_target()
            if x is not None:
                t.add(x)
    return t


def ret_value(B, ret):
    """Walk back from a ret through straight-line code to the nearest eax/rax definition; refuse when a branch
    target lands strictly inside the walked segment (another path could join with a different eax)."""
    bt = branch_targets(B)
    a = ret
    idx = B.order.index(ret)
    while idx > 0:
        idx -= 1
        a = B.order[idx]
        I = B[a]
        if I.mnemonic.startswith("j") or I.mnemonic == "ret":
            return None, "control transfer at %X before an eax def" % a
        if "rax" in I.reg_writes:
            nxt = B.order[idx + 1]
            joins = [x for x in bt if a < x <= ret and x != a]
            if I.mnemonic == "xor" and I.op_str == "eax, eax":
                v = 0
            elif I.mnemonic == "mov" and I.op_str.startswith("eax, ") and I.imm:
                v = I.imm[0]
            else:
                return None, "eax def %s" % I.text
            return (v, a, joins), ""
    return None, "start"


def checks(img, R):
    Br, Bs, Bc = Body(img, *REM), Body(img, *SWEEP), Body(img, *CLEAN)
    tot = 0
    for (s, e), B in ((REM, Br), (SWEEP, Bs), (CLEAN, Bc)):
        ents, pok = img.pdata_cover(s, e)
        R.check("body %08X..%08X decodes exactly and .pdata tiles it (%d record(s))" % (s, e, len(ents)), B.exact and pok)
        tot += e - s
    R.check("bytes total 1017 (358 + 328 + 331)", tot == 1017, str(tot))
    for (s, e), B in ((REM, Br), (SWEEP, Bs)):
        rets, tails, outs = B.exits()
        R.check("%08X local CFG closed (no tail/out branch, last insn ret)" % s, not tails and not outs and
                B[B.order[-1]].mnemonic == "ret", "tails=%s outs=%s" % (tails, outs))
    rets, tails, outs = Bc.exits()
    R.check("4200A0 has no ret; its only exit is the last insn `jmp 0x41f730`", not rets and not outs and
            tails == [(Bc.order[-1], CLEAR)], "rets=%s tails=%s" % (rets, tails))
    R.check("4200A0 rcx = rbx at 4201D2 and no rcx write between it and the tail jmp",
            Bc[0x4201D2].text == "mov rcx, rbx" and not [a for a in Bc.order if 0x4201D2 < a < Bc.order[-1]
                                                       and "rcx" in Bc[a].reg_writes])
    R.check("every 4200A0 call precedes its tail", all(a < Bc.order[-1] for a, t in Bc.calls()))
    R.note("4200A0 calls: %s" % " ".join("%X" % t for a, t in Bc.calls()))
    # pool global shared by both bodies
    p1 = rip_target(Br[0x429146]) if 0x429146 in Br.ins else None
    p2 = rip_target(Bs[0x427C9A]) if 0x427C9A in Bs.ins else None
    R.check("429146 rdx and 427C9A rdi load the same pool global 022C6F28", p1 == POOL and p2 == POOL,
            "%s %s" % (p1, p2))

    # ---------------- 429140 partitions ----------------
    R.check("429150/429153: `test rcx, rcx` then `jne 0x42915d`",
            Br[0x429150].text == "test rcx, rcx" and Br[0x429153].text == "jne 0x42915d")
    null_path = [0x429140, 0x429142, 0x429146, 0x42914D, 0x429150, 0x429153, 0x429155, 0x429157, 0x42915B, 0x42915C]
    recreads = [a for a in null_path for m in Br[a].mems if m["base"] not in ("rip", "rsp", None)]
    R.check("NULL arm: no call, no nonstack write, no record dereference",
            not calls_in(Br, null_path) and not nonstack_writes(Br, null_path) and not recreads, str(recreads))
    rv = {r: ret_value(Br, r) for r in Br.exits()[0]}
    R.note("429140 rets: %s" % {("%X" % k): (("eax=%d def %X joins %s" % (v[0][0], v[0][1], [hex(x) for x in v[0][2]]))
                                              if v[0] else v[1]) for k, v in rv.items()})
    R.check("three rets: 42915C eax=0; 429203 and 4292A5 eax=1; no join between def and ret",
            sorted(rv) == [0x42915C, 0x429203, 0x4292A5] and rv[0x42915C][0] and rv[0x42915C][0][0] == 0 and
            not rv[0x42915C][0][2] and all(rv[r][0] and rv[r][0][0] == 1 and not rv[r][0][2] for r in (0x429203, 0x4292A5)))
    R.check("NULL ret 42915C is reachable only through the jne fallthrough (no branch targets 429155..42915C)",
            not [x for x in branch_targets(Br) if 0x429155 <= x <= 0x42915C])
    R.check("non-NULL dispatch: 42915D `test byte ptr [rcx + 0x284], 4`; 429169 `je 0x429204`",
            Br[0x42915D].text == "test byte ptr [rcx + 0x284], 4" and Br[0x429169].text == "je 0x429204")
    # mark arm
    M = Br.reach(0x42916F)
    Mw = nonstack_writes(Br, M)
    rec = [(a, m["disp"], m["size"], Br[a].mnemonic) for a, m in Mw if m["base"] == "rcx"]
    R.check("mark arm record writes = OR 290h dword, OR 2AEh byte, 108h qword, 110h dword, 284h dword",
            [(d, s, mn) for a, d, s, mn in rec] == [(0x290, 4, "or"), (0x2AE, 1, "or"), (0x108, 8, "mov"),
                                                    (0x110, 4, "mov"), (0x284, 4, "mov")], str(rec))
    R.check("mark arm immediates: 290h |= 2, 2AEh |= 1, 108h/110h <- 0 (xor eax at 429176)",
            Br[0x42916F].imm == [2] and Br[0x429178].imm == [1] and Br[0x429176].text == "xor eax, eax" and
            Br[0x42917F].op_str.endswith("rax") and Br[0x429186].op_str.endswith("eax"))
    R.check("mark arm 284h = (old & ~4) | bit 30 (42918C..429199)",
            [Br[a].text for a in (0x42918C, 0x429192, 0x429195, 0x429199)] ==
            ["mov eax, dword ptr [rcx + 0x284]", "and eax, 0xfffffffb", "bts eax, 0x1e", "mov dword ptr [rcx + 0x284], eax"])
    mc = calls_in(Br, M)
    R.check("all mark-arm record writes precede its first call", all(a < mc[0][0] for a, d, s, mn in rec))
    R.check("mark arm: no 41F730/4200A0 call and no write to the pool count/cursor",
            all(t not in (CLEAR, CLEAN[0]) for a, t in mc) and
            not [a for a, m in Mw if m["disp"] in (COUNT, CURSOR)], str(mc))
    R.note("mark-arm calls: %s" % " ".join("%X" % t for a, t in mc))
    other = [(a, Br[a].text) for a, m in Mw if m["base"] != "rcx"]
    R.note("mark-arm writes on helper-returned objects (not the record): %s" % other)
    R.check("4291D8 `mov rbx, rax` follows call 2ED570 and dominates 4291F3 (so +A0h is written on that callee's object)",
            Br[0x4291D8].text == "mov rbx, rax" and Br[0x4291D3].direct_target() == 0x2ED570 and
            Br.dominates(0x4291D8, 0x4291F3))
    # no-op arm
    R.check("no-op dispatch: 429204 `test byte ptr [rcx + 0x290], 1`; 42920B `je 0x429296`",
            Br[0x429204].text == "test byte ptr [rcx + 0x290], 1" and Br[0x42920B].text == "je 0x429296")
    N = [0x429204, 0x42920B] + [a for a in Br.order if a >= 0x429296]
    R.check("no-op path 429204 -> 429296 -> ret: no call, no nonstack write",
            not calls_in(Br, N) and not nonstack_writes(Br, N))
    R.check("stated no-op input (284h = 2010F9h, 290h = 0) selects the no-op path", (0x2010F9 & 4) == 0 and (0 & 1) == 0)
    # unlink arm
    Ua = Br.reach(0x429211)
    uc = calls_in(Br, Ua)
    R.check("unlink arm: one call, to 41F730 at 429291; no 4200A0", uc == [(0x429291, CLEAR)], str(uc))
    dec = [a for a in Ua if Br[a].mnemonic == "dec" and Br[a].mems and Br[a].mems[0]["disp"] == COUNT]
    R.check("unlink arm: one `dec dword [rdx+4880Ch]` (42924D), dominating the 41F730 call",
            dec == [0x42924D] and Br.dominates(0x42924D, 0x429291))
    pre = Br.reach(0x429204, avoid=[0x42924D])
    cr = [a for a in pre for m in Br[a].mems if m["base"] == "rdx" and m["disp"] in (COUNT,)]
    R.check("no read of the count on any path 429204 -> 42924D (no positive-count guard)", not cr, str(cr))
    upath = [a for a in Br.order if 0x429146 < a <= 0x429169 or 0x429204 <= a < 0x42924D]
    R.check("rdx (pool) is not rewritten on the unlink path 429146..429169, 429204..42924D (no call on it)",
            not [a for a in upath if "rdx" in Br[a].reg_writes] and not calls_in(Br, upath) and
            set(Br.reach(0x429204, avoid=[0x42924D])) - {0x42924D} <= set(upath) | set(a for a in Br.order if a >= 0x42924D))
    uw = [(a, m["base"], m["index"], m["disp"], m["size"]) for a, m in nonstack_writes(Br, Ua)]
    R.note("unlink-arm writes: %s" % [("%X" % a, b, i, "%X" % d, s) for a, b, i, d, s in uw])
    R.check("unlink writes: neighbour rows +4/+2 (indexed), head 48810h, tail 48814h, count, cursor 48808h",
            sorted((d, s) for a, b, i, d, s in uw) == sorted([(4, 2), (2, 2), (COUNT, 4), (PHEAD, 4), (PTAIL, 4), (CURSOR, 4)]))
    R.check("cursor reset 429288 follows `cmp [rdx+4880Ch], 0` (42927D) and is dominated by the dec",
            Br[0x42927D].text == "cmp dword ptr [rdx + 0x4880c], 0" and Br.dominates(0x42924D, 0x429288)
            and Br.dominates(0x42927D, 0x429288))

    # ---------------- 427C90 active sweep ----------------
    R.check("427CA1 esi = [rdi+48800h] (active head)", Bs[0x427CA1].text == "mov esi, dword ptr [rdi + 0x48800]")
    R.check("loop row: rbx = rdi + sext(esi)*740h (427CC0..427CCA)",
            [Bs[a].text for a in (0x427CC0, 0x427CC3, 0x427CCA)] == ["movsxd rax, esi", "imul rbx, rax, 0x740", "add rbx, rdi"])
    R.check("427CCD tests 290h mask 02; next WORD +4 sign-extended into esi (427CD4/427CD8) before the je",
            Bs[0x427CCD].text == "test byte ptr [rbx + 0x290], 2" and Bs[0x427CD4].text == "movsx edx, word ptr [rbx + 4]"
            and Bs[0x427CD8].text == "mov esi, edx" and Bs[0x427CDA].text == "je 0x427dba")
    ew = [a for a in Bs.order if "rsi" in Bs[a].reg_writes]
    R.check("esi written only at 427CA1 (head) and 427CD8 (cached next) plus the epilogue restore",
            ew == [0x427CA1, 0x427CD8, 0x427DCD], str([hex(a) for a in ew]))
    R.check("loop continues on cached esi: 427DBA `cmp esi, -1`; 427DBD `jne 0x427cc0`",
            Bs[0x427DBA].text == "cmp esi, -1" and Bs[0x427DBD].text == "jne 0x427cc0")
    sc = Bs.calls()
    sdec = [a for a in Bs.order if Bs[a].mnemonic == "dec" and Bs[a].mems and Bs[a].mems[0]["disp"] == COUNT]
    R.check("one count dec (427D18), dominating every call in the sweep",
            sdec == [0x427D18] and all(Bs.dominates(0x427D18, a) for a, t in sc), str(sc))
    R.note("sweep calls in order: %s" % " ".join("%X@%X" % (t, a) for a, t in sc))
    before = Bs.reach(0x427CC0, avoid=[0x427D18])
    id_reads = [a for a in before for m in Bs[a].mems if m["base"] == "rbx" and m["disp"] == 0 and not m["index"]]
    cnt_reads = [a for a in before for m in Bs[a].mems if m["base"] == "rdi" and m["disp"] == COUNT]
    R.check("no read of WORD +0 (ID) on any loop path before the dec", not id_reads, str(id_reads))
    R.check("no read of the count on any loop path before the dec (no positive-count guard)", not cnt_reads, str(cnt_reads))
    bw = [a for a in Bs.order if "rbp" in Bs[a].reg_writes]
    R.check("cursor reset: 427D48 `cmp [rdi+4880Ch], ebp`; 427D50 writes ebp to 48808h; ebp = 0 at 427CBA only",
            Bs[0x427D48].text == "cmp dword ptr [rdi + 0x4880c], ebp" and
            Bs[0x427D50].text == "mov dword ptr [rdi + 0x48808], ebp" and bw == [0x427CBA, 0x427DC3] and
            Bs.dominates(0x427D18, 0x427D50), str([hex(a) for a in bw]))
    R.check("4200A0 call at 427DAE with rcx = rbx (427DAB), after 42F4C0 (427D59)",
            (0x427DAE, CLEAN[0]) in sc and Bs[0x427DAB].text == "mov rcx, rbx" and (0x427D59, 0x42F4C0) in sc)
    R.note("after 4200A0 returns: %s" % Bs[0x427DB3].text)
    R.check("active unlink uses 48800h/48804h ends; pending unlink in 429140 uses 48810h/48814h",
            {Bs[a].mems[0]["disp"] for a in (0x427D2D, 0x427D42)} == {AHEAD, ATAIL} and
            {Br[a].mems[0]["disp"] for a in (0x429262, 0x429277)} == {PHEAD, PTAIL})


CONTROLS = [
    ("429296 `mov eax, 1` -> `mov eax, 2`", 0x429297, bytes([2])),
    ("429204 test moved onto the count: `test byte [rdx+4880Ch], 1`", 0x429204, bytes.fromhex("F6820C88040001")),
    ("429291 call retargeted to 4200A0", 0x429291, None),
    ("427D18 count dec NOPed", 0x427D18, bytes([0x90] * 6)),
    ("427CD4 next load reads WORD +0 instead of +4", 0x427CD7, bytes([0x00])),
    ("427CD8 `mov esi, edx` NOPed", 0x427CD8, bytes([0x90, 0x90])),
    ("42915D mask 04 -> 08", 0x429163, bytes([0x08])),
    ("42916F mark-arm OR replaced by `dec dword [rdx+4880Ch]` + nop", 0x42916F, bytes.fromhex("FF8A0C88040090")),
    ("4201E6 tail jmp retargeted to 41F740", 0x4201E6, None),
]


def rel32(img, site, target):
    return bytes([img.read(site, 1)[0]]) + struct.pack("<i", target - (site + 5))


def main():
    img = Img.load()
    R = Rep("rv_removal")
    print("== packet integrity")
    check_manifest(R, "render-removal-phase-contracts", "fc26ae31f8ddb389fff58deeb7616680334f0e93723e35f4556159e32b47bc5c")
    print("== shipping-image re-derivation")
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check above)")
    for label, va, nb in CONTROLS:
        if nb is None:
            nb = rel32(img, va, CLEAN[0] if va == 0x429291 else 0x41F740)
        P = img.patched(va, nb)
        Rc = Rep(label)
        Rc.quiet = True
        try:
            checks(P, Rc)
            failed = Rc.fails
            why = "%d failed, e.g. %s" % (failed, "; ".join(Rc.failed[:4]))
        except Exception as e:
            failed = 1
            why = "refused: %r" % e
        R.check("control: " + label, failed > 0, why)
    print("TOTAL: %d checks, %d PASS, %d FAIL" % (R.n, R.n - R.fails, R.fails))


if __name__ == "__main__":
    main()
