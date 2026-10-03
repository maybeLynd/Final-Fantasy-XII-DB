"""check_s21.py - FABLE, 2026-10-03: the S-21 post-result events - route, poster, ring, realiser, last mile.

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (I9-I12):

  K1  raw index: 0046AB10 has 48 call sites in 18 functions (chained .pdata fragments resolved to their roots: the
      dispatcher 00469EC0 with 10 sites and 17 others); 005369C0, 00469570, 00469EC0, 00385BA0, 0035B990 and 00536410
      each have exactly one caller; the only .rdata/.data constants naming them are chained-unwind parent records.
  K2  the route: 003112F0 calls 00385BA0 once (0031137A), after the eligibility gate; 00385BA0 dispatches only when
      result byte +0x1C == 1 (00385C6F) and passes the formula scratch word [02AEDFD4], not its own ecx (ecx is not read
      before 00385BC9 overwrites it); writers of 02AEDFD4 listed.
  K3  the dispatcher's context: +0x28 is the zero-extended 16-bit action (00469EFB, 00469F33), +0x2C..+0x2F are zero
      (00469EF0); all ten dispatcher sites pass r8 = rbp-0x48; no dispatcher path reads the poster's rax.
  K4  the poster's body, statically: signed cap, the target-unit-conditional veto, 32-bit row address with no bound
      against the row count, unsigned window compare, ring bounds, mod-10 index.
  K5  the ring is written only by the poster and by the leaf 004696A0, whose only caller chain is 0033A380 <- 00234463
      in area initialisation 002342F0, after that body's counter-restart call 00234349; the three 02089340 veto bits.
  K6  executed (Unicorn 2.1.4, original code: 0046AB10, 00469570, 0020E600, 0032A150, 004696A0 real; 0031B860,
      002FA3B0 and 005369C0 answered by hooks), with the shipped us battle_message.bin as the table:
        a admit; b cap (0x1FF dropped, -1 admitted); c the 0x3080 veto only when the target has a unit; d unit +4 bit 5;
        e the filter decides on the source's verdict alone when the source has client info; f the window, G 1 and 2;
        g eviction by ten later posts; h a stamp from before a counter restart suppresses until stamp + 450G, and the
        ring reset ends it; i an unbound table faults at 0046ABB3 when the filter admits; j the index wraps at 10.
  K7  executed 005369C0 (real; 003148F0, 00264ED0, 002FA390, 00536310, 0031B860, 00263A10, 00536280, 00536410,
      0035B990, 00808C40 hooked): slot kinds from row +0/+1/+2/+5, kinds 3-9 -> ctx +0x10/+0x14/+0x18/+0x1C/+0x20/
      +0x28/+0x24, kind 0 and 10 -> 0; the request handed to 0035B990.
  K8  executed 0035B990 (real; 00393740, 00254A10, 002B5680, 002B3050, 0028E110, 00254F30, 00808C40 hooked): word +0x30
      selects the stash; otherwise 0028E110 is always called; +0x32 and 00254A10 gate only the measure.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: 0046AB29 jge -> jg (cap): K6b must fail.
  S2  image: 0046ABB3 tests bit 1 instead of bit 0: K6f must fail.
  S3  image: 00536B00 `cmp eax, 8` -> `cmp eax, 7`: K7b must fail (kind 9 loses ctx +0x24).
  S4  image: 0035B9CB je -> jne: K8 must fail.
  S5  claim: "the 0x3080 veto applies to every post" checked against K6c's execution must fail.

Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, decode_fn  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM  # noqa: E402
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, __version__ as UC_VERSION  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,  # noqa: E402
                               UC_X86_REG_RSP, UC_X86_REG_RIP)

BM = r"D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle\us\binaryfile\battle_message.bin"
POSTER, FILTER, REALISE, DISPATCH, GATE = 0x0046AB10, 0x00469570, 0x005369C0, 0x00469EC0, 0x00385BA0
RING, RING_END, RING_IDX = 0x02EBB560, 0x02EBB6A0, 0x02EBB54C
TABLE, FLAGS, COUNTER, GWORD, RTBASE, OWNER = 0x02EBF018, 0x02089340, 0x0208D45C, 0x01DFE0B4, 0x01F83530, 0x02EBF188
HEAP, OBJ, STACK, SENT = 0x10000000, 0x11000000, 0x20000000, 0x30000000

fails = 0
quiet = [False]


def report(tag, ok, text=""):
    global fails
    if not ok:
        fails += 1
    if not quiet[0]:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return ok


def note(s):
    if not quiet[0]:
        print("      " + s)


def one(img, a):
    return next(img.cs.disasm(img.read(a, 16), a, 1))


def txt(ci):
    return (ci.mnemonic + " " + ci.op_str).strip()


# ---------------------------------------------------------------- unwind chains
def runtime_functions(img):
    va = img.base + img.exc_rva
    out = []
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack("<III", img.read(va + 12 * i, 12))
        if b:
            out.append((img.base + b, img.base + e, img.base + (u & ~1)))
    return out


def unwind_code_spans(img):
    """[(lo, hi)) of every UNWIND_INFO's unwind-code array: a u32 that matches there is opcode bytes, not a pointer."""
    out = []
    for b, e, u in runtime_functions(img):
        n = img.read(u, 4)[2]
        out.append((u + 4, u + 4 + 2 * n))
    return out


def chain_parent_fields(img):
    """{address of a chained RUNTIME_FUNCTION's BeginAddress field: (fragment start, parent start)}"""
    out = {}
    for b, e, u in runtime_functions(img):
        hdr = img.read(u, 4)
        flags, ncodes = hdr[0] >> 3, hdr[2]
        if flags & 4:
            at = u + 4 + 2 * ((ncodes + 1) & ~1)
            out[at] = (b, img.base + img.u32(at))
    return out


def root_of(img, va, chains=None):
    chains = chains if chains is not None else chain_parent_fields(img)
    by_start = {frag: parent for _, (frag, parent) in chains.items()}
    pd = img.pdata(va)
    s = pd[0] if pd else va
    seen = 0
    while s in by_start and seen < 8:
        s = by_start[s]
        seen += 1
    return s


# ---------------------------------------------------------------- K1..K5 static
def k1(img):
    chains = chain_parent_fields(img)
    refs, unc = text_refs(img, POSTER)
    roots = {}
    for r in refs:
        roots.setdefault(root_of(img, r["site"], chains), []).append(r["site"])
    forms = set(r["form"] for r in refs)
    report("K1a", len(refs) == 48 and len(roots) == 18 and forms == {"call"} and not unc,
           "0046AB10: %d sites (%s), %d functions after chained-fragment roots, %d unconfirmed" %
           (len(refs), sorted(forms), len(roots), len(unc)))
    report("K1b", len(roots.get(DISPATCH, [])) == 10,
           "the dispatcher 00469EC0 holds %d of them (with its fragment 00469FE0); 17 other functions hold %d" %
           (len(roots.get(DISPATCH, [])), 48 - len(roots.get(DISPATCH, []))))
    note("callers: " + " ".join("%08X:%d" % (k, len(v)) for k, v in sorted(roots.items())))
    singles = {REALISE: 0x0046AC66, FILTER: 0x0046AB65, DISPATCH: 0x00385C85, GATE: 0x0031137A,
               0x0035B990: 0x00536D79, 0x00536410: 0x00536C06}
    bad = []
    for tgt, site in singles.items():
        rr, _ = text_refs(img, tgt)
        if [(r["site"], r["form"]) for r in rr] != [(site, "call")]:
            bad.append(("%08X" % tgt, ["%08X %s" % (r["site"], r["form"]) for r in rr]))
    report("K1c", not bad, "005369C0/00469570/00469EC0/00385BA0/0035B990/00536410 each have exactly one call site %s" % bad)
    cbad, chain_hits, code_hits = [], [], []
    spans = unwind_code_spans(img)
    for tgt in [POSTER, REALISE, FILTER, DISPATCH, GATE, 0x0035B990, 0x00536410]:
        for s, at, kind, v in data_refs(img, tgt):
            if kind == "u32" and at in chains and chains[at][1] == tgt:
                chain_hits.append("%08X" % at)
            elif kind == "u32" and any(lo <= at < hi for lo, hi in spans):
                code_hits.append("%08X" % at)
            else:
                cbad.append("%08X %s %s" % (at, s, kind))
    lits = []
    for r in refs:
        pd, ins = decode_fn(img, r["site"])
        prev = [ins[x] for x in sorted(ins) if x < r["site"]]
        for ci in reversed(prev):
            _, wr = ci.regs_access()
            if set(ci.reg_name(x) for x in wr) & {"edx", "rdx", "dx", "dl"}:
                if ci.mnemonic == "mov" and ci.operands[1].type == X86_OP_IMM:
                    lits.append(ci.operands[1].imm)
                elif ci.mnemonic == "xor" and ci.op_str == "edx, edx":
                    lits.append(0)
                break
    report("K1e", len(lits) == 25 and max(lits) == 0x4D,
           "%d of the 48 sites load a literal event id; the largest is 0x%X (the other %d are computed)" %
           (len(lits), max(lits), 48 - len(lits)))
    report("K1d", not cbad, "no pointer constant names these entries: %d u32 matches are chained-unwind parent records %s, "
           "%d lie inside an unwind-code array (opcode bytes) %s; other %s" %
           (len(chain_hits), chain_hits, len(code_hits), code_hits, cbad))


def regs_read(ci):
    r, _ = ci.regs_access()
    return set(ci.reg_name(x) for x in r)


def k2(img):
    seq = list(img.cs.disasm(img.read(0x00311354, 0x0031137F - 0x00311354), 0x00311354))
    t = [txt(c) for c in seq]
    report("K2a", t[0] == "test r10b, 1" and "call 0x30b9b0" in t and "jne 0x311aca" in t and t[-1] == "call 0x385ba0",
           "0031137A calls 00385BA0 after the eligibility gate 00311354..00311367 (bit 0 bypass, non-zero return exits)")
    pre = list(img.cs.disasm(img.read(GATE, 0x00385BC9 - GATE + 8), GATE))
    pre = [c for c in pre if c.address < 0x00385BC9]
    rd = [c for c in pre if regs_read(c) & {"rcx", "ecx", "cx", "cl"}]
    last = one(img, 0x00385BC9)
    report("K2b", not rd and txt(last) == "movzx ecx, byte ptr [r9 + 0x138]",
           "00385BA0 does not read its ecx before 00385BC9 overwrites it %s" % [txt(c) for c in rd])
    gate = [txt(one(img, a)) for a in (0x00385C6F, 0x00385C73, 0x00385C75, 0x00385C85)]
    report("K2c", gate == ["cmp byte ptr [rbx + 0x1c], 1", "jne 0x385c8a", "movzx ecx, word ptr [rip + 0x2768358]",
                           "call 0x469ec0"],
           "dispatch only when result +0x1C == 1, with ecx = word [02AEDFD4]: %s" % gate)
    refs, _ = text_refs(img, 0x02AEDFD4, 0x02AEDFD6)
    wr = []
    for r in refs:
        ci = one(img, r["site"])
        if ci.operands and ci.operands[0].type == X86_OP_MEM and ci.mnemonic not in ("cmp", "test"):
            wr.append("%08X %s" % (r["site"], txt(ci)))
    report("K2d", any(w.startswith("00385FE4") for w in wr),
           "02AEDFD4: %d references; writers %s (the resolver's store 00385FE4 among them)" % (len(refs), wr))


def k3(img):
    a = [txt(one(img, x)) for x in (0x00469EF0, 0x00469EFB, 0x00469F2F, 0x00469F33)]
    report("K3a", a == ["mov qword ptr [rbp - 0x20], rax", "movzx edi, cx", "movzx r12d, di",
                        "mov dword ptr [rbp - 0x20], r12d"] and txt(one(img, 0x00469ED6)) == "xor eax, eax",
           "ctx +0x28 = zero-extended 16-bit action, +0x2C..+0x2F = 0 (qword clear 00469EF0, dword store 00469F33)")
    refs, _ = text_refs(img, POSTER)
    chains = chain_parent_fields(img)
    sites = [r["site"] for r in refs if root_of(img, r["site"], chains) == DISPATCH]
    ctxs = []
    for s in sites:
        pd, ins = decode_fn(img, s)
        prev = [ins[x] for x in sorted(ins) if x < s]
        c = next((ci for ci in reversed(prev) if ci.op_str.startswith("r8,")), None)
        ctxs.append(txt(c) if c else None)
    report("K3b", len(sites) == 10 and set(ctxs) == {"lea r8, [rbp - 0x48]"},
           "all ten dispatcher sites pass r8 = rbp-0x48: %s" % sorted(set(ctxs)))
    used = []
    for s in sites:
        stack, seen = [s + 5], set()
        while stack:
            a = stack.pop()
            n = 0
            while n < 40 and a not in seen:
                seen.add(a)
                ci = one(img, a)
                r, w = ci.regs_access()
                rn, wn = set(ci.reg_name(x) for x in r), set(ci.reg_name(x) for x in w)
                if rn & {"rax", "eax", "ax", "al"} and not (ci.mnemonic == "xor" and "eax, eax" in ci.op_str):
                    used.append("%08X->%08X %s" % (s, a, txt(ci)))
                    break
                if wn & {"rax", "eax"} or ci.mnemonic in ("ret", "call") or ci.mnemonic == "jmp" and ci.op_str.startswith("r"):
                    break
                if ci.mnemonic.startswith("j"):
                    tgt = ci.operands[0].imm
                    if ci.mnemonic == "jmp":
                        a = tgt
                        n += 1
                        continue
                    stack.append(tgt)
                a += ci.size
                n += 1
    report("K3c", not used, "no path from a dispatcher site reads the poster's rax before writing it %s" % used)


def k4(img):
    want = {0x0046AB19: "cmp dword ptr [r8 + 0x28], 0x1ff", 0x0046AB29: "jge 0x46ac7a",
            0x0046AB2F: "mov rcx, qword ptr [r8 + 8]", 0x0046AB36: "je 0x46ab5c", 0x0046AB38: "call 0x31b860",
            0x0046AB40: "je 0x46ab5c", 0x0046AB42: "test dword ptr [rip + 0x1c1e7f4], 0x3080",
            0x0046AB52: "test byte ptr [rax + 4], 0x20", 0x0046AB65: "call 0x469570",
            0x0046ABA6: "movzx ecx, word ptr [rcx + 8]", 0x0046ABAA: "imul ecx, edi", 0x0046ABAD: "add ecx, eax",
            0x0046ABB1: "xor ecx, ecx", 0x0046ABB3: "test byte ptr [rcx + 4], 1",
            0x0046ABD4: "cmp qword ptr [rbx + 8], rsi", 0x0046ABDA: "movzx eax, word ptr [rbx]",
            0x0046ABE6: "imul ecx, dword ptr [rip + 0x19934c4], 0x1c2", 0x0046ABF5: "ja 0x46ac6b",
            0x0046AC43: "mov eax, 0x66666667", 0x0046AC66: "call 0x5369c0"}
    bad = [("%08X" % a, txt(one(img, a))) for a, t in want.items() if txt(one(img, a)) != t]
    report("K4a", not bad, "the poster's gates, row read, window compare and ring arithmetic read as stated %s" % bad)
    body = list(img.cs.disasm(img.read(POSTER, 0x0046AC83 - POSTER), POSTER))
    cmps = ["%08X %s" % (c.address, txt(c)) for c in body if c.mnemonic in ("cmp", "test")]
    want_c = ["0046AB19 cmp dword ptr [r8 + 0x28], 0x1ff", "0046AB33 test rcx, rcx", "0046AB3D test rax, rax",
              "0046AB42 test dword ptr [rip + 0x1c1e7f4], 0x3080", "0046AB52 test byte ptr [rax + 4], 0x20",
              "0046AB6A test eax, eax", "0046AB7E test rax, rax", "0046AB8B test rax, rax",
              "0046ABB3 test byte ptr [rcx + 4], 1", "0046ABD4 cmp qword ptr [rbx + 8], rsi", "0046ABDD cmp eax, edi",
              "0046ABF3 cmp ecx, eax", "0046ABFB cmp rbx, rbp"]
    report("K4b", cmps == want_c, "the poster's only tests are the gates, the row bit and the ring scan; edi (the event) "
           "is compared only with a ring entry's word (0046ABDD), never with the table's row count %s" %
           ([c for c in cmps if c not in want_c]))
    fil = [txt(one(img, a)) for a in (0x004695C4, 0x004695F9, 0x004695FD, 0x0046963D, 0x0046967E, 0x00469685)]
    report("K4c", fil == ["add eax, edx", "cmp byte ptr [rcx + 3], 0x80", "jae 0x469685", "call 0x2fa3b0",
                          "call 0x2fa3b0", "mov eax, 1"], "the filter: row +3 >= 0x80 admits; one 002FA3B0 verdict per path")


def k5(img):
    refs, _ = text_refs(img, RING, RING_END)
    refs2, _ = text_refs(img, RING_IDX, RING_IDX + 4)
    w = []
    for r in refs + refs2:
        ci = one(img, r["site"])
        if ci.mnemonic == "lea":
            continue
        if ci.operands[0].type == X86_OP_MEM and ci.mnemonic not in ("cmp", "test"):
            w.append(r["site"])
    inleaf = [a for a in w if 0x004696A0 <= a < 0x004697BC]
    others = [a for a in w if not 0x004696A0 <= a < 0x004697BC]
    report("K5a", len(inleaf) == 41 and others == [0x0046AC5D],
           "rip writers of the ring and its index: 41 in the leaf 004696A0..004697BB, plus the poster's index store "
           "0046AC5D (its entry stores are [rax+r15] off the `lea r15` at 0046ABB7): others=%s" % ["%08X" % a for a in others])
    leaf = list(img.cs.disasm(img.read(0x004696A0, 0x004697BC - 0x004696A0), 0x004696A0))
    report("K5b", txt(leaf[0]) == "xor ecx, ecx" and txt(leaf[1]) == "mov eax, 0xffff" and txt(leaf[-1]) == "ret" and
           not [c for c in leaf if c.mnemonic.startswith("j") or c.mnemonic == "call"],
           "004696A0 is branch-free: event word := 0xFFFF, stats := 0, tick := 0, +0x18 := 0 for ten entries, index := 0")
    r1, _ = text_refs(img, 0x004696A0)
    r2, _ = text_refs(img, 0x0033A380)
    report("K5c", [x["site"] for x in r1] == [0x0033A3B0] and [x["site"] for x in r2] == [0x00234463] and
           root_of(img, 0x00234463) == 0x002342F0 and not data_refs(img, 0x004696A0) and not data_refs(img, 0x0033A380),
           "004696A0 <- 0033A3B0 (in 0033A380) <- 00234463, in area initialisation 002342F0; no pointer constants")
    seq = list(img.cs.disasm(img.read(0x00234349, 0x00234468 - 0x00234349), 0x00234349))
    js = [c for c in seq if c.mnemonic.startswith("j")]
    back = [c for c in js if c.operands[0].imm <= c.address]
    fwd_ok = all(c.operands[0].imm <= 0x00234463 for c in js if c not in back)
    loop_ok = [(c.address, c.operands[0].imm) for c in back] == [(0x0023438E, 0x00234360)] and         txt(one(img, 0x0023435A)) == "lea edi, [rsi + 0x28]" and txt(one(img, 0x0023438A)) == "sub rdi, 1"
    report("K5d", txt(seq[0]) == "call 0x239960" and fwd_ok and loop_ok,
           "from the counter-restart call 00234349 to the ring reset 00234463: every forward branch lands at or before "
           "00234463 %s, and the one back-edge is the counted 0x28-iteration loop 0023438E -> 00234360" %
           ["%08X->%08X" % (c.address, c.operands[0].imm) for c in js])
    bits = [txt(one(img, a)) for a in (0x00238AEA, 0x00238B0A, 0x00238B2A, 0x0023432D, 0x00234339)]
    report("K5e", bits == ["btr eax, 7", "btr eax, 0xc", "btr eax, 0xd", "and eax, 0xffffc01e", "or eax, 0x10"],
           "veto bits 7 / 12 / 13 are set by 00238AE0 / 00238B00 / 00238B20; area initialisation clears all three "
           "(0023432D and 0xFFFFC01E)")


# ---------------------------------------------------------------- emulator
class Emu(object):
    def __init__(self, img, patches=None):
        self.img = img
        top = max(img.base + va + vs for n, va, vs, ra, rs in img.secs)
        self.uc = uc = Uc(UC_ARCH_X86, UC_MODE_64)
        size = ((top - img.base) + 0xFFFF) & ~0xFFFF
        uc.mem_map(img.base, size)
        for n, va, vs, ra, rs in img.secs:
            uc.mem_write(img.base + va, img.d[ra:ra + min(vs, rs)])
        for a, b in (patches or {}).items():
            uc.mem_write(a, b)
        uc.mem_map(HEAP, 0x01000000)
        uc.mem_map(OBJ, 0x00100000)
        uc.mem_map(STACK, 0x00100000)
        uc.mem_map(SENT, 0x1000)
        uc.mem_write(STACK, b"\xA5" * 0x100000)
        self.stubs = {}
        self.calls = []
        uc.hook_add(UC_HOOK_CODE, self._hook)

    def _hook(self, uc, addr, size, _):
        fn = self.stubs.get(addr)
        if fn is None:
            return
        regs = {k: uc.reg_read(v) for k, v in (("rcx", UC_X86_REG_RCX), ("rdx", UC_X86_REG_RDX),
                                                 ("r8", UC_X86_REG_R8), ("r9", UC_X86_REG_R9))}
        self.calls.append((addr, regs))
        rv = fn(regs)
        uc.reg_write(UC_X86_REG_RAX, rv & 0xFFFFFFFFFFFFFFFF)
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)

    def w(self, a, fmt, *v):
        self.uc.mem_write(a, struct.pack(fmt, *v))

    def r(self, a, fmt):
        return struct.unpack(fmt, bytes(self.uc.mem_read(a, struct.calcsize(fmt))))

    def call(self, fn, rcx=0, rdx=0, r8=0, r9=0):
        uc = self.uc
        rsp = STACK + 0x80000
        uc.mem_write(rsp, struct.pack("<Q", SENT))
        for reg, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9),
                       (UC_X86_REG_RSP, rsp)):
            uc.reg_write(reg, v & 0xFFFFFFFFFFFFFFFF)
        uc.emu_start(fn, SENT, count=200000)
        return uc.reg_read(UC_X86_REG_RAX)


def load_table(emu, raw):
    """battle_message.bin at HEAP, its +0xC rebased the way 003845F0 does (add the blob's address)."""
    emu.uc.mem_write(HEAP, raw)
    off = struct.unpack_from("<I", raw, 0xC)[0]
    emu.w(HEAP + 0xC, "<I", HEAP + off)
    emu.w(TABLE, "<Q", HEAP)


def poster_world(img, raw, patches=None, G=1):
    e = Emu(img, patches)
    if raw is not None:
        load_table(e, raw)
    e.w(GWORD, "<I", G)
    e.units = {}
    e.verdict = {}
    e.realised = []
    e.stubs[0x0031B860] = lambda r: e.units.get(r["rcx"], 0)
    e.stubs[0x002FA3B0] = lambda r: e.verdict.get(r["rcx"], 1)

    def realise(r):
        e.realised.append((r["rcx"], r["rdx"] & 0xFFFFFFFF, r["r8"]))
        return 0x5555
    e.stubs[REALISE] = realise
    return e


SRC, TGT, TGT2, CTX = OBJ + 0x1000, OBJ + 0x2000, OBJ + 0x3000, OBJ + 0x8000
USRC, UTGT, CI_S, CI_T = OBJ + 0x11000, OBJ + 0x12000, OBJ + 0x21000, OBJ + 0x22000


def mkctx(e, src=SRC, tgt=TGT, action=0x10, extra=0):
    e.uc.mem_write(CTX, b"\0" * 0x30)
    e.w(CTX, "<QQ", src, tgt)
    e.w(CTX + 0x28, "<I", action & 0xFFFFFFFF)
    e.w(CTX + 0x2C, "<I", extra)
    return CTX


def post(e, stats, ev, now, **kw):
    e.w(COUNTER, "<I", now)
    n = len(e.realised)
    e.call(POSTER, stats, ev, mkctx(e, **kw))
    return len(e.realised) > n


def ring(e):
    return [e.r(RING + 32 * i, "<HxxIQ") for i in range(10)], e.r(RING_IDX, "<i")[0]


def k6(img, raw, patches=None, tag=""):
    res = {}
    # a admit
    e = poster_world(img, raw, patches)
    e.units = {TGT: UTGT}
    ok = post(e, SRC, 0x10, 1000)
    rg, idx = ring(e)
    res["a"] = ok and e.realised[-1] == (SRC, 0x10, CTX) and rg[0] == (0x10, 1000, SRC) and idx == 1
    report("K6a" + tag, res["a"], "admitted: realiser called with (stats, 0x10, ctx); ring[0] = %s, index %d" % (rg[0], idx))
    # b cap
    e = poster_world(img, raw, patches)
    d1 = post(e, SRC, 0x10, 1000, action=0x1FF)
    r1 = ring(e)
    d2 = post(e, SRC, 0x10, 1000, action=0x1FE)
    d3 = post(e, SRC, 0x10, 1000, action=-1)
    res["b"] = (not d1) and r1[1] == 0 and r1[0][0][0] == 0 and d2 and d3
    report("K6b" + tag, res["b"], "cap: action 0x1FF dropped with no ring write (%s, index %d); 0x1FE admitted %s; "
                                  "-1 admitted %s (signed jge)" % (not d1, r1[1], d2, d3))
    # c the veto bits only with a target unit
    out = []
    for bit in (0x80, 0x1000, 0x2000):
        e = poster_world(img, raw, patches)
        e.w(FLAGS, "<I", bit)
        e.units = {TGT: UTGT}
        with_unit = post(e, SRC, 0x10, 1000)
        e.units = {}
        no_unit = post(e, SRC, 0x10, 1000)
        null_tgt = post(e, SRC, 0x10, 1000, tgt=0)
        out.append((hex(bit), with_unit, no_unit, null_tgt))
    res["c"] = all(not a and b and c for _, a, b, c in out)
    res["c_raw"] = out
    report("K6c" + tag, res["c"], "02089340 bits 7/12/13 drop a post only when ctx +0x08 has an owning unit "
                                  "(bit, with unit, unit-less target, null target): %s" % out)
    # d unit +4 bit 5
    e = poster_world(img, raw, patches)
    e.units = {TGT: UTGT}
    e.w(UTGT + 4, "<B", 0x20)
    a = post(e, SRC, 0x10, 1000)
    e.w(UTGT + 4, "<B", 0xDF)
    b = post(e, SRC, 0x10, 1000)
    res["d"] = (not a) and b
    report("K6d" + tag, res["d"], "target unit byte +4 bit 5 drops (%s); the other seven bits do not (%s)" % (not a, b))
    # e filter: source verdict alone
    rows = rowbytes(raw)
    ev = next(i for i in range(len(rows)) if not rows[i][3] & 0x80 and not rows[i][4] & 1)
    e = poster_world(img, raw, patches)
    e.units = {SRC: USRC, TGT: UTGT}
    e.w(USRC + 0x10, "<Q", CI_S)
    e.w(UTGT + 0x10, "<Q", CI_T)
    e.verdict = {CI_S: 0, CI_T: 1}
    s0 = post(e, SRC, ev, 1000)
    e.verdict = {CI_S: 1, CI_T: 0}
    s1 = post(e, SRC, ev, 1000)
    e.units = {TGT: UTGT}
    e.verdict = {CI_T: 0}
    t0 = post(e, SRC, ev, 1000)
    e.verdict = {CI_T: 1}
    t1 = post(e, SRC, ev, 1000)
    alw = next(i for i in range(len(rows)) if rows[i][3] & 0x80 and not rows[i][4] & 1)
    e.units = {SRC: USRC, TGT: UTGT}
    e.verdict = {CI_S: 0, CI_T: 0}
    a7 = post(e, SRC, alw, 1000)
    res["e"] = (not s0) and s1 and (not t0) and t1 and a7
    report("K6e" + tag, res["e"], "filter on row 0x%02X (+3 bit 7 clear): source verdict 0 drops though the target's is 1 "
           "(%s); source 1 admits though the target's is 0 (%s); no source unit -> the target decides (0: %s, 1: %s); "
           "row 0x%02X (+3 bit 7) admits with both verdicts 0 (%s)" % (ev, not s0, s1, not t0, t1, alw, a7))
    # f window
    lim = next(i for i in range(len(rows)) if rows[i][4] & 1)
    outs = {}
    for G in (1, 2):
        e = poster_world(img, raw, patches, G=G)
        w = 0x1C2 * G
        first = post(e, SRC, lim, 1000)
        inside = post(e, SRC, lim, 1000 + w - 1)
        other = post(e, TGT2, lim, 1000 + w - 1)
        edge = post(e, SRC, lim, 1000 + w)
        outs[G] = (first, not inside, other, edge)
    res["f"] = all(all(v) for v in outs.values())
    report("K6f" + tag, res["f"], "row 0x%02X (+4 bit 0): admitted, then suppressed at stamp + 0x1C2*G - 1, admitted for "
           "other stats at the same tick, admitted at stamp + 0x1C2*G; G=1 and G=2: %s" % (lim, outs))
    # g eviction
    e = poster_world(img, raw, patches)
    post(e, SRC, lim, 1000)
    for k in range(10):
        post(e, TGT2, 0x10, 1001 + k)
    again = post(e, SRC, lim, 1100)
    res["g"] = again
    report("K6g" + tag, res["g"], "ten later unlimited posts evict the stamp: row 0x%02X repeats for the same stats at "
                                  "stamp + 100 (%s)" % (lim, again))
    # h stamp across a counter restart, then the ring reset
    e = poster_world(img, raw, patches)
    post(e, SRC, lim, 5000)
    after = post(e, SRC, lim, 10)
    late = post(e, SRC, lim, 5449)
    free = post(e, SRC, lim, 5450)
    e2 = poster_world(img, raw, patches)
    post(e2, SRC, lim, 5000)
    e2.call(0x004696A0)
    rg2, idx2 = ring(e2)
    reset = post(e2, SRC, lim, 10)
    res["h"] = (not after) and (not late) and free and reset and rg2[0][0] == 0xFFFF and idx2 == 0
    res["h_after"] = after
    report("K6h" + tag, res["h"], "stamp 5000, counter restarted to 10: suppressed (%s), still at 5449 (%s), admitted at "
           "5450 (%s); after 004696A0 (event 0x%04X, index %d) admitted at 10 (%s)" %
           (not after, not late, free, rg2[0][0], idx2, reset))
    # i unbound table
    e = poster_world(img, None, patches)
    fault = None
    try:
        e.call(POSTER, SRC, 0x10, mkctx(e))
    except UcError as ex:
        fault = (e.uc.reg_read(UC_X86_REG_RIP), str(ex))
    res["i"] = fault is not None and fault[0] == 0x0046ABB3
    report("K6i" + tag, res["i"], "[02EBF018] = 0 and the filter admits: the poster faults at %s (%s)" %
           ("%08X" % fault[0] if fault else None, fault[1] if fault else "no fault"))
    # j wrap
    e = poster_world(img, raw, patches)
    for k in range(11):
        post(e, SRC, 0x10, 2000 + k)
    rg, idx = ring(e)
    res["j"] = idx == 1 and rg[0][1] == 2010 and rg[1][1] == 2001
    report("K6j" + tag, res["j"], "eleven posts: index %d, slot 0 holds the 11th stamp %d, slot 1 the 2nd %d" %
           (idx, rg[0][1], rg[1][1]))
    return res


def rowbytes(raw):
    n, st, off = struct.unpack_from("<III", raw, 4)
    return [raw[off + i * st: off + i * st + st] for i in range(n)]


# ---------------------------------------------------------------- K7 the realiser
def realise_world(img, raw, patches=None):
    e = Emu(img, patches)
    load_table(e, raw)
    e.units = {SRC: USRC, TGT: UTGT}
    e.w(USRC + 0x10, "<Q", CI_S)
    e.w(UTGT + 0x10, "<Q", CI_T)
    e.w(SRC + 5, "<B", 1)
    e.w(TGT + 5, "<B", 1)
    e.cat = 1
    e.reqA = None
    e.reqB = None
    e.textbuf = None
    e.stubs[0x003148F0] = lambda r: 0
    e.stubs[0x00264ED0] = lambda r: 0x1234
    e.stubs[0x002FA390] = lambda r: e.cat
    e.stubs[0x0031B860] = lambda r: e.units.get(r["rcx"], 0)
    e.stubs[0x00263A10] = lambda r: {CI_S: 3, CI_T: 4}.get(r["rcx"], 0)
    e.stubs[0x00808C40] = lambda r: 0

    def name(r):
        e.w(r["rdx"], "<B", 1)
        return {SRC: 0x0101, TGT: 0x0202}.get(r["rcx"], 0xFFFF)
    e.stubs[0x00536310] = name
    e.stubs[0x00536280] = lambda r: 0x0F000000 | (r["rcx"] & 0xFFFF)

    def fmt(r):
        e.reqA = bytes(e.uc.mem_read(r["rcx"], 0x48))
        e.textbuf = (r["rdx"], r["r8"], r["r9"])
        return 0
    e.stubs[0x00536410] = fmt

    def last(r):
        e.reqB = bytes(e.uc.mem_read(r["rcx"], 0x38))
        return 0
    e.stubs[0x0035B990] = last
    return e


def k7(img, raw, patches=None, tag=""):
    res = {}
    rows = rowbytes(raw)
    # a: a shipped row, 0x18 = {02 05 ..} "{target} is cured of {status}"
    e = realise_world(img, raw, patches)
    ctx = mkctx(e, action=0x55)
    for k, off in enumerate((0x10, 0x14, 0x18, 0x1C, 0x20, 0x24)):
        e.w(ctx + off, "<I", 0x1000 + k)
    e.call(REALISE, SRC, 0x18, ctx)
    A = e.reqA
    s = [A[8 + 16 * i: 8 + 16 * (i + 1)] for i in range(4)]
    k0 = struct.unpack_from("<H", s[0], 8)[0]
    k1v = struct.unpack_from("<I", s[1], 0)[0]
    res["a"] = rows[0x18][:2] == b"\x02\x05" and k0 == 0x0202 and s[0][1] == 4 and k1v == 0x1002
    report("K7a" + tag, res["a"], "row 0x18 (%s): slot 0 = target name word %04X + letter %d, slot 1 = ctx +0x18 = %08X"
           % (rows[0x18].hex(), k0, s[0][1], k1v))
    # b: synthetic rows, kinds 3..9, 0, 10, and slot 3 from +5
    got = {}
    for kinds in ((3, 4, 5, 6), (7, 8, 9, 0), (10, 0, 0, 9)):
        raw2 = bytearray(raw)
        off = struct.unpack_from("<I", raw2, 0xC)[0]
        raw2[off + 0x18 * 8: off + 0x18 * 8 + 8] = bytes([kinds[0], kinds[1], kinds[2], 0x00, 0x00, kinds[3], 0, 0])
        e = realise_world(img, bytes(raw2), patches)
        ctx = mkctx(e, action=0x77)
        for off2 in (0x10, 0x14, 0x18, 0x1C, 0x20, 0x24):
            e.w(ctx + off2, "<I", 0xC0000000 | off2)
        e.call(REALISE, SRC, 0x18, ctx)
        for i in range(4):
            got.setdefault(kinds[i], set()).add(struct.unpack_from("<I", e.reqA, 8 + 16 * i)[0])
    want = {3: {0xC0000010}, 4: {0xC0000014}, 5: {0xC0000018}, 6: {0xC000001C}, 7: {0xC0000020}, 8: {0x77},
            9: {0xC0000024}, 0: {0}, 10: {0}}
    res["b"] = got == want
    report("K7b" + tag, res["b"], "kinds 3..9 -> ctx +0x10/+0x14/+0x18/+0x1C/+0x20/+0x28/+0x24, kind 0 and 10 -> 0, "
           "slot 3 read from row +5: %s" % {k: sorted("%X" % x for x in v) for k, v in sorted(got.items())})
    # c: the request handed to 0035B990, and the id word
    out = {}
    for ev, extra in ((0x18, 0), (0x24, 0), (0x25, 7), (0x26, 0)):
        e = realise_world(img, raw, patches)
        ctx = mkctx(e, action=0x1A9, extra=extra)
        e.w(ctx + 0x14, "<I", 0xBEEF)
        e.cat = 1 if ev == 0x18 else 0
        e.call(REALISE, SRC, ev, ctx)
        B = e.reqB
        out[ev] = dict(kind=struct.unpack_from("<I", B, 0)[0], src=struct.unpack_from("<Q", B, 8)[0],
                       tgt=struct.unpack_from("<Q", B, 0x10)[0], ls=B[0x18], lt=B[0x19],
                       act=struct.unpack_from("<H", B, 0x1A)[0], mag=struct.unpack_from("<H", B, 0x1C)[0],
                       cat=B[0x1F], m1=struct.unpack_from("<i", B, 0x20)[0], text=struct.unpack_from("<Q", B, 0x28)[0],
                       stash=struct.unpack_from("<H", B, 0x30)[0], obtain=struct.unpack_from("<H", B, 0x32)[0],
                       tb=e.textbuf, idw=struct.unpack_from("<I", e.reqA, 4)[0], hw=struct.unpack_from("<H", e.reqA, 0)[0])
    o = out[0x18]
    ok = (o["kind"] == 7 and o["src"] == 0x0F000101 and o["tgt"] == 0x0F000202 and o["ls"] == 3 and o["lt"] == 4 and
          o["act"] == 0x1A9 and o["mag"] == 0xBEEF and o["cat"] == (rows[0x18][3] >> 2) & 0x1F and o["m1"] == -1 and
          o["text"] == o["tb"][0] and o["tb"][1:] == (0x180, 1) and o["stash"] == 0 and o["obtain"] == 0 and
          o["idw"] & 0xFFFF == 0x8018 and o["hw"] == 0x1234)
    ok2 = out[0x24]["obtain"] == 1 and out[0x25]["obtain"] == 1 and out[0x26]["obtain"] == 0 and \
        out[0x25]["stash"] == 7 and out[0x24]["idw"] & 0xFFFF == 0x0024
    res["c"] = ok and ok2
    report("K7c" + tag, res["c"], "request to 0035B990: +0 = %d, names %X/%X, letters %d/%d, +0x1A action %X, +0x1C %X, "
           "+0x1F category %d, +0x20 %d, +0x28 = the 00536410 buffer (cap 0x180), +0x30 = ctx word +0x2C (%d, %d for "
           "0x25), +0x32 = 1 only for 0x24/0x25 (%s); id word %04X (bit 15 = 002FA390)" %
           (o["kind"], o["src"], o["tgt"], o["ls"], o["lt"], o["act"], o["mag"], o["cat"], o["m1"], o["stash"],
            out[0x25]["stash"], [out[x]["obtain"] for x in (0x18, 0x24, 0x25, 0x26)], o["idw"] & 0xFFFF))
    res["hi"] = o["idw"] >> 16
    note("id dword bits 16-31 = %04X with the stack pre-filled 0xA5: 005369C0 does not initialise them (005369F0 reads "
         "the slot before any store); 00536410 masks them away (00536448-0053645B)" % (o["idw"] >> 16))
    return res


# ---------------------------------------------------------------- K8 the last mile
def k8(img, patches=None, tag=""):
    seen = {}
    for stash, obtain, mode in ((0, 0, 0), (0, 1, 0), (0, 1, 1), (3, 1, 0)):
        e = Emu(img, patches)
        REQ, TEXT, STASHREC = OBJ + 0x40000, OBJ + 0x41000, OBJ + 0x50000
        e.uc.mem_write(REQ, b"\0" * 0x38)
        e.w(REQ, "<I", 7)
        e.w(REQ + 0x1F, "<B", 9)
        e.w(REQ + 0x28, "<Q", TEXT)
        e.w(REQ + 0x30, "<HH", stash, obtain)
        e.w(0x022CA430, "<Q", STASHREC)
        e.stubs[0x00393740] = lambda r: TEXT
        e.stubs[0x00254A10] = lambda r, m=mode: m
        e.stubs[0x002B5680] = lambda r: 0

        def width(r):
            e.w(r["r8"], "<H", 10)
            return 0
        e.stubs[0x002B3050] = width
        e.stubs[0x0028E110] = lambda r: 0
        e.stubs[0x00254F30] = lambda r: 0
        e.stubs[0x00808C40] = lambda r: 0
        e.call(0x0035B990, REQ)
        names = [a for a, _ in e.calls if a not in (0x00808C40,)]
        hud = [r for a, r in e.calls if a == 0x0028E110]
        cp = [r for a, r in e.calls if a == 0x00254F30]
        seen[(stash, obtain, mode)] = (names, hud, cp)
    a = seen[(0, 0, 0)]
    b = seen[(0, 1, 0)]
    c = seen[(0, 1, 1)]
    d = seen[(3, 1, 0)]
    ok = (len(a[1]) == 1 and 0x002B5680 not in a[0] and a[1][0]["rdx"] & 0xFF == 9 and
          len(b[1]) == 1 and 0x002B5680 in b[0] and 0x002B3050 in b[0] and
          len(c[1]) == 1 and 0x002B5680 not in c[0] and
          not d[1] and len(d[2]) == 1 and d[2][0]["rcx"] == OBJ + 0x50000 + 0x568 and d[2][0]["r8"] == 0x180)
    res = ok
    report("K8" + tag, ok, "0035B990: +0x30 = 0 -> 0028E110(text, +0x1F) once whether or not the measure runs (measure "
           "only for +0x32 != 0 with 00254A10() = 0: %s / %s / %s); +0x30 != 0 -> 00254F30([022CA430] + 0x568, text, "
           "0x180) and no HUD call (%d HUD calls)" % (0x002B5680 in a[0], 0x002B5680 in b[0], 0x002B5680 in c[0], len(d[1])))
    return res


def main():
    print("FABLE check_s21 - the S-21 post-result events: route, poster, ring, realiser (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    img = Img.load()
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION == "2.1.4", "unicorn pinned 2.1.4")
    raw = open(BM, "rb").read()
    n, st, off = struct.unpack_from("<III", raw, 4)
    report("V1", (n, st, off) == (102, 8, 0x20) and len(raw) == 6668,
           "us battle_message.bin: %d rows x %d B at +0x%X, %d B" % (n, st, off, len(raw)))
    rows = rowbytes(raw)
    report("V2", sum(1 for r in rows if r[4] & 1) == 28 and sum(1 for r in rows if r[3] & 0x80) == 70,
           "us rows: %d with +4 bit 0 (rate-limited), %d with +3 bit 7 (always shown)" %
           (sum(1 for r in rows if r[4] & 1), sum(1 for r in rows if r[3] & 0x80)))
    base = os.path.dirname(os.path.dirname(os.path.dirname(BM)))
    lang = {}
    for lg in sorted(os.listdir(base)):
        p = os.path.join(base, lg, "binaryfile", "battle_message.bin")
        if os.path.exists(p):
            rr = rowbytes(open(p, "rb").read())
            same = all(rr[i][3:5] + rr[i][6:8] == rows[i][3:5] + rows[i][6:8] for i in range(min(len(rr), 100)))
            lang[lg] = (len(rr), same)
    report("V3", len(lang) == 9 and all(v[1] for v in lang.values()) and min(v[0] for v in lang.values()) == 100,
           "nine languages, rows 0-99 agree with us in bytes +3/+4/+6/+7 (only kind bytes differ): %s" % lang)
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k5(img)
    r6 = k6(img, raw)
    k7(img, raw)
    k8(img)

    quiet[0] = True
    f0 = fails
    rs1 = k6(img, raw, {0x0046AB29: b"\x0F\x8F"})
    rs2 = k6(img, raw, {0x0046ABB3: b"\xF6\x41\x04\x02"})
    rs3 = k7(img, raw, {0x00536B00: b"\x83\xF8\x07"})
    rs4 = k8(img, {0x0035B9CB: b"\x75"})
    quiet[0] = False
    globals()["fails"] = f0
    report("S1", not rs1["b"], "0046AB29 jge -> jg: K6b fails (action 0x1FF admitted)")
    report("S2", not rs2["f"], "0046ABB3 tests bit 1: K6f fails (the limited row is no longer limited)")
    report("S3", not rs3["b"], "00536B00 bound 8 -> 7: K7b fails (kind 9 no longer reads ctx +0x24)")
    report("S4", not rs4, "0035B9CB je -> jne: K8 fails")
    claim = all(not wu and not nu and not nt for _, wu, nu, nt in r6["c_raw"])
    report("S5", not claim, "the claim 'the 0x3080 veto drops every post' is refuted by K6c's execution")
    print("FAILS %d" % fails)
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
