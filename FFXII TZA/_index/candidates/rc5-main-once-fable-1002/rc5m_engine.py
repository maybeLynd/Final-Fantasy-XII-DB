"""rc5m_engine.py - RC-5 residue, part (a) (FABLE, 2026-10-02). Static; the shipping image only.

Question: the six increment-only counters of FABLE's rc5-counter-loops record are bounded only if `main` of their actor
runs once per image load. ORACLE's RC-13 table says the engine files footer slot 1 (`main`) on channel 0 "at record
start", site 002669F5. Which function is that, which paths reach it, can respawn / re-init / reqenable re-runs reach it,
does any other native site file slot 1, and does a re-run of record start come with fresh class-1 variables?

Instruments (shared image helpers from ../rc12-footer-channels-runstate-0930/: img.py, rc12_slots.partC, rc14_sweep's
stream list = every .pdata chain root plus a linear sweep of the .text no .pdata entry covers):
- E0 control: RC-12 Part C reproduces (43 actor-entry footer resolves in 19 functions).
- E1 the filing site: owner function, override word +0xCA, footer word +4 (k = 1), channel edx = 0, submit 003DBB60.
- E2 raw reference index for the chain 00266530 <- 002679F0 <- 0026CE60: E8/E9 rel32, 0F 8x rel32, EB / 7x rel8,
  rip-relative lea, and 8-byte absolute / 4-byte RVA data words outside .text and .pdata (an RVA word is classed as an
  unwind chain copy when the 12 bytes there equal a .pdata entry).
- E3 the gates of 0026CE60 and what it consumes / sets; E4 the binder that arms it.
- E5 an image-wide sweep for writes that cover the manager slot's byte +0x13 (the arm) in any stream that touches the
  manager array (imul 0x288, a rip reference into 02098E10 + 5 x 0x288, the current-manager cell 02099D70, or a call to
  the slot getter 00263FF0), plus every rip-relative lea of a slot's +0x10..+0x13 (folded bases).
- E6 where the bound payload comes from: the binder's only caller, its callers and the pack loader.
- E7 the re-run routes: the forward direct-call closure of each named route must not contain the chain.
- E8 every other native filer of slot 1: Part C's fixed sites, and the slot argument of both variable-slot readers.
- E9 class-1 storage: the binder zeroes manager +0x40; the armed init points it into the fresh payload.
Output: rc5m_engine.out. Exit 0 only when every check passes.
"""
import collections, os, re, struct, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc12-footer-channels-runstate-0930"))
import img            # noqa: E402
import rc12_slots     # noqa: E402
import rc14_sweep     # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_REG_RIP, X86_REG_INVALID  # noqa: E402

OUT, FAILS = [], []


def say(s=""):
    OUT.append(s)
    print(s)


def check(name, ok, detail=""):
    say(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def at(va):
    """the decoded instruction at va, as 'mnemonic op_str'."""
    x = img.dis(va, 16)[0]
    return "%s %s" % (x.mnemonic, x.op_str)


def expect(va, pattern, label):
    t = at(va)
    check("%s: %08X %s" % (label, va, t), re.fullmatch(pattern, t) is not None)


PDSET = set(img.PDATA)


def raw_refs(target):
    t = img.blob[img.TR:img.TR + img.TN]
    out = []
    for m in re.finditer(rb"[\xe8\xe9]", t[:-4]):
        o = m.start()
        if img.T0 + o + 5 + struct.unpack("<i", t[o + 1:o + 5])[0] == target:
            out.append((img.T0 + o, "call" if t[o] == 0xE8 else "jmp"))
    for m in re.finditer(rb"\x0f[\x80-\x8f]", t[:-5]):
        o = m.start()
        if img.T0 + o + 6 + struct.unpack("<i", t[o + 2:o + 6])[0] == target:
            out.append((img.T0 + o, "jcc rel32"))
    for o in range(max(0, target - img.T0 - 130), min(len(t) - 1, target - img.T0 + 130)):
        if (t[o] == 0xEB or 0x70 <= t[o] <= 0x7F) and img.T0 + o + 2 + struct.unpack("<b", t[o + 1:o + 2])[0] == target:
            out.append((img.T0 + o, "jmp/jcc rel8"))
    for m in re.finditer(rb"[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", t[:-7]):
        o = m.start()
        if img.T0 + o + 7 + struct.unpack("<i", t[o + 3:o + 7])[0] == target:
            out.append((img.T0 + o, "lea rip"))
    q, r = struct.pack("<Q", target), struct.pack("<I", target - img.BASE)
    for name, start, size, raw, rawsz in img.SECS:
        if name in (".text", ".pdata"):
            continue
        d = img.blob[raw:raw + rawsz]
        for m in re.finditer(re.escape(q), d):
            out.append((start + m.start(), "abs64 " + name))
        for m in re.finditer(re.escape(r), d):
            o = m.start()
            if o % 4 == 0:
                b, e, u = struct.unpack("<III", d[o:o + 12])
                kind = "unwind chain copy" if (img.BASE + b, img.BASE + e, img.BASE + u) in PDSET else "RVA word"
                out.append((start + o, "rva32 %s (%s)" % (name, kind)))
    return out


def code_refs(target):
    return [(s, k) for s, k in raw_refs(target) if not k.startswith("rva32") or "unwind" not in k]


# ---------------------------------------------------------------- E0
rc = rc12_slots.partC()
check("E0 RC-12 Part C reproduces: 43 actor-entry footer resolves in 19 functions",
      (len(rc), len(set(r[0] for r in rc))) == (43, 19), "%d sites, %d functions" % (len(rc), len(set(r[0] for r in rc))))

# ---------------------------------------------------------------- E1
say("")
own = img.owner(0x002669F5)
check("E1 the RC-13 site 002669F5 lies in 00266530 (ActorStorage_InitializeRecord)", own == 0x00266530, "%08X" % own)
expect(0x002669AE, r"movzx eax, word ptr \[rbx \+ 0xca\]", "E1 record override slot 1 read first (0xC8 + 2*1)")
expect(0x002669C5, r"call 0x20e600", "E1 footer resolve [entry+0x18]")
expect(0x002669D7, r"movsx r8d, word ptr \[rcx \+ rdi \+ 4\]", "E1 footer word +4 = k 1 (main)")
expect(0x002669F0, r"xor edx, edx", "E1 channel 0")
expect(0x002669F5, r"call 0x3dbb60", "E1 native submit")

# ---------------------------------------------------------------- E2
say("")
CHAIN = [0x00266530, 0x002679F0, 0x0026CE60]
want = {0x00266530: {0x00267B79}, 0x002679F0: {0x0026CEB0}, 0x0026CE60: {0x0025BFF6, 0x0032F227}}
for tg in CHAIN:
    refs = raw_refs(tg)
    for s, k in refs:
        o = img.owner(s) if not k.startswith(("rva32", "abs64")) else None
        say("  %08X <- %08X %-34s %s" % (tg, s, k, ("in %08X" % o) if o else ""))
    live = {s for s, k in refs if not ("unwind chain copy" in k)}
    check("E2 every code reference to %08X is %s (unwind chain copies excluded)" % (tg, sorted("%08X" % x for x in want[tg])),
          live == want[tg], str(sorted("%08X" % x for x in live)))
expect(0x00267B70, r"mov r8d, ebp", "E2 002679F0 loop: record index ebp")
expect(0x00267B7E, r"inc ebp", "E2 002679F0 loop: next record")
expect(0x00267B80, r"cmp ebp, ebx", "E2 002679F0 loop: bound")

# ---------------------------------------------------------------- E3 / E4
say("")
expect(0x0026CE94, r"test byte ptr \[rbx \+ 0x10\], 1", "E3 gate 1: manager +0x10 bit 0 (initialised)")
expect(0x0026CE98, r"jne 0x26d383", "E3 gate 1 set -> leave")
expect(0x0026CE9E, r"cmp byte ptr \[rbx \+ 0x13\], 0", "E3 gate 2: manager +0x13 (armed)")
expect(0x0026CEA2, r"je 0x26d383", "E3 gate 2 clear -> leave")
expect(0x0026CEB0, r"call 0x2679f0", "E3 then the record pool is built (one 00266530 per record)")
expect(0x0026CED3, r"xor ebp, ebp", "E3 ebp = 0")
expect(0x0026D2E3, r"mov byte ptr \[rbx \+ 0x13\], bpl", "E3 the arm is consumed (+0x13 = 0)")
expect(0x0026D305, r"or byte ptr \[rbx \+ 0x10\], 1", "E3 bit 0 is set")
expect(0x0026D383, r"mov qword ptr \[rip \+ 0x1e2c9e6\], r13", "E3 exit restores the current-manager cell")
expect(0x0026CB1B, r"and r9b, 0xfe", "E4 binder 0026C8C0 clears bit 0 in its copy of +0x10")
expect(0x0026CB67, r"mov byte ptr \[rdi \+ 0x10\], r9b", "E4 binder stores +0x10")
expect(0x0026CC45, r"mov byte ptr \[rdi \+ 0x10\], r9b", "E4 binder stores +0x10 again")
expect(0x0026CC6C, r"mov word ptr \[rdi \+ 0x13\], 0x101", "E4 binder arms +0x13 = 1")
expect(0x00262DA8, r"and byte ptr \[rbx \+ 0x10\], 0xfe", "E4 unload 002628B0 clears bit 0")
expect(0x00262DB3, r"mov byte ptr \[rbx \+ 0x13\], bpl", "E4 unload 002628B0 clears +0x13")

# ---------------------------------------------------------------- E5 sweep
say("")
MB, ME = 0x02098E10, 0x02098E10 + 5 * 0x288
RO = {"cmp", "test", "bt", "push", "call", "jmp", "lea", "nop", "ucomiss", "comiss"}
HAND = {   # by-hand base verdicts for hits whose base is neither a stack frame nor resolved by last_def
    0x00226C4B: "r12 = r12 + r10*8 at 00226C2E: an 8-byte-stride table, not a 0x288-stride slot",
    0x00259752: "00259620 walks the foreign 0x860-stride array at 02098428 (bound 020994E8, manager field map +0x1C8 row)",
    0x003A43A5: "float4 store through rdi = r8 (argument) of the vector routine 003A4290, reached only by tail jumps",
    0x003A43C3: "float4 store through rsi = r9 (argument) of 003A4290",
    0x003A447B: "float4 store through rdi = r8 of 003A4290",
    0x003A4F93: "float4 store through rdi = r8 of 003A4290",
    0x003A5372: "float4 store through rsi = r9 of 003A4290",
    0x003A53F4: "qword store through rdi = r8 of 003A4290",
    0x003A5413: "qword store through rsi = r9 of 003A4290",
    0x003A543E: "float4 store through rsi = r9 of 003A4290",
    0x003A5836: "float4 store through r14 = r9 (003A574E) of 003A56F0",
    0x003A58D7: "float4 store through r14 = r9 of 003A56F0",
    0x003A62C3: "rbp = rsp - 0xE8 (003A56FD): stack frame",
    0x003A640C: "rbp = rsp - 0xE8: stack frame",
    0x003A6602: "rbp = rsp - 0xE8: stack frame",
    0x003A66DB: "float4 store through r14 = r9 of 003A56F0",
    0x003A6818: "qword store through r14 = r9 of 003A56F0",
    0x003DD61D: "rbx = rdx + index*0x1C (003DD51E-003DD52C): a 0x1C-stride table",
    0x0026C987: "rax = 02099014 = slot 0 +0x204 (0026C96A); the store lands at +0x214",
}
EXPECT13 = {0x0026CC6C: "binder: arm = 1", 0x0026D2E3: "manager init: arm consumed", 0x00262DB3: "unload: arm cleared"}


def marker(ins):
    for x in ins:
        if x.mnemonic == "imul" and any(o.type == X86_OP_IMM and o.imm == 0x288 for o in x.operands):
            return "imul 0x288"
        t = img.ripmem(x)
        if t is not None and (MB <= t < ME or t == 0x02099D70):
            return "rip %08X" % t
        if x.mnemonic == "call" and x.op_str == "0x263ff0":
            return "call 00263FF0"
    return None


hits13, folded, nstreams = [], [], 0
for name, ins in rc14_sweep.streams():
    nstreams += 1
    mk = marker(ins)
    for k, x in enumerate(ins):
        t = img.ripmem(x)
        if x.mnemonic == "lea" and t is not None and MB <= t < ME and 0x10 <= (t - MB) % 0x288 <= 0x13:
            folded.append((name, x))
        if not x.operands or x.operands[0].type != X86_OP_MEM or x.mnemonic in RO or x.mnemonic.startswith(("j", "cmp")):
            continue
        o = x.operands[0]
        sz = o.size or 1
        if o.mem.base == X86_REG_RIP:
            if any(t <= MB + s * 0x288 + 0x13 < t + sz for s in range(5)):
                hits13.append((name, x, "rip", "rip"))
            continue
        if mk is None or o.mem.index != X86_REG_INVALID or not (o.mem.disp <= 0x13 < o.mem.disp + sz):
            continue
        base = x.op_str.split("[")[1].split()[0].rstrip("]")
        hits13.append((name, x, base, rc14_sweep.last_def(ins, k, base)))
say("E5 streams swept: %d" % nstreams)
unexplained, on_slot = [], []
for name, x, base, ld in hits13:
    if base in ("rsp",) or re.search(r" (mov|lea) %s, \[?rsp" % base, ld):
        verdict = "stack frame"
    elif x.address in EXPECT13:
        verdict = "MANAGER SLOT +0x13: " + EXPECT13[x.address]
        on_slot.append(x.address)
    elif x.address in HAND:
        verdict = "not a slot: " + HAND[x.address]
    else:
        verdict = "UNEXPLAINED"
        unexplained.append(x.address)
    if verdict != "stack frame":
        say("  %08X %-6s %-40s base %s (%s) -> %s" % (x.address, x.mnemonic, x.op_str, base, ld, verdict))
say("  (%d stack-frame hits not listed)" % sum(1 for h in hits13 if h[2] == "rsp" or re.search(r" (mov|lea) %s, \[?rsp" % h[2], h[3])))
check("E5 the only writes of a manager slot's +0x13 are the binder's arm and the two clears",
      sorted(on_slot) == sorted(EXPECT13) and not unexplained,
      "on slot %s; unexplained %s" % (sorted("%08X" % a for a in on_slot), ["%08X" % a for a in unexplained]))
for name, x in folded:
    say("  folded base: %s %08X %s %s" % (name if isinstance(name, str) else "%08X" % name, x.address, x.mnemonic, x.op_str))
expect(0x00262FC4, r"test byte ptr \[rcx \+ rax\], 1", "E5 folded base 00262FBD is only tested")
expect(0x00266EFC, r"call 0x861ec0", "E5 folded base 00266EE0: each slot memset to zero (area init 00266D10)")
expect(0x002641A1, r"movzx eax, byte ptr \[rcx \+ rax\]", "E5 folded base 0026419A (leaf getter 00264190, +0x10 bit 1) only reads")
expect(0x00267201, r"movzx eax, byte ptr \[rcx \+ rax\]", "E5 folded base 002671FA (leaf getter 002671F0, +0x10 bit 0) only reads")
expect(0x00267401, r"movzx eax, byte ptr \[rcx \+ rax\]", "E5 folded base 002673FA (leaf getter 002673F0, +0x13) only reads")
check("E5 exactly the five folded bases above", sorted(x.address for _n, x in folded) ==
      [0x00262FBD, 0x0026419A, 0x00266EE0, 0x002671FA, 0x002673FA], str(["%08X" % x.address for _n, x in folded]))

# ---------------------------------------------------------------- E6 where the payload comes from
say("")
for tg, w in ((0x0026C8C0, {0x0032F966}), (0x0032F850, {0x00330514, 0x00330FAD}), (0x003304A0, {0x0033040E, 0x0033041B})):
    live = {s for s, k in code_refs(tg) if "unwind" not in k}
    check("E6 code references to %08X = %s" % (tg, sorted("%08X" % a for a in w)), live == w,
          str(sorted("%08X" % a for a in live)))
expect(0x0032F961, r"mov rdx, rdi", "E6 0032F850 binds the payload it was handed")
expect(0x003303AD, r"call 0x36c660", "E6 00330310 allocates a new payload buffer")
expect(0x003303C5, r"mov qword ptr \[rax \+ r13 \+ 0x21a6c00\], r15", "E6 ... and records it")
expect(0x00330407, r"call 0x861eba", "E6 ... then copies the resident image into it (pack 0xD4) and dispatches")
expect(0x0033041B, r"lea rax, \[rip \+ 0x7e\]", "E6 ... or files a read with 003304A0 as its completion")
expect(0x00330444, r"call 0x32e620", "E6 ... the read")
expect(0x00330FA6, r"call 0x36c660", "E6 003306E0 allocates a new buffer before naming 0032F850 as completion")
cache_w = []
for name, ins in rc14_sweep.streams():
    for x in ins:
        if img.ripmem(x) == 0x022C6F10 and x.mnemonic == "mov" and x.operands[0].type == X86_OP_MEM:
            cache_w.append(x.address)
check("E6 the resident copy 022C6F10 is written only by its loader 0032F430 (0 at 0032F607, a fresh allocation at "
      "0032F651, then a read)", sorted(cache_w) == [0x0032F607, 0x0032F651], str(["%08X" % a for a in cache_w]))

# ---------------------------------------------------------------- E7 re-run routes
say("")
CALLEES = {}


def body(root):
    """a .pdata root's fragments, or for leaf code (no .pdata) a linear run up to ret / int3 / jmp."""
    if root in img.ROOTS:
        return img.fn_ins(root)
    out = []
    for x in img.dis(root, 0x400):
        out.append(x)
        if x.mnemonic in ("ret", "int3", "jmp"):
            break
    return out


def callees(root):
    """direct call / jump targets that leave the body: their .pdata root, or the target itself for leaf code."""
    if root not in CALLEES:
        s = set()
        ins = body(root)
        lo, hi = (min(x.address for x in ins), max(x.address for x in ins)) if ins else (0, 0)
        frag = img.fragments(root) if root in img.ROOTS else [(lo, hi + 1)]
        for x in ins:
            if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and x.operands and x.operands[0].type == X86_OP_IMM:
                t = x.operands[0].imm
                if any(b <= t < e for b, e in frag):
                    continue
                r = img.owner(t)
                s.add(r if r is not None else t)
        s.discard(root)
        CALLEES[root] = s
    return CALLEES[root]


ROUTES = {0x0026B4A0: "reqenable tail (re-runs 00268EA0)", 0x00267CC0: "re-runner", 0x00269FE0: "re-runner",
          0x00238BF0: "unit refresh BattleUnit_RefreshActorRuntimeFromDefinition", 0x00268EA0: "talkhold/talkterm filer",
          0x00269860: "spawn / respawn filer", 0x00269640: "entry / parameter filer", 0x0025AD10: "spawn-table override",
          0x0025AE00: "spawn-table override", 0x0025D5E0: "reqdisable tail"}
say("E7 forward reachability is NOT a separating instrument here: following direct calls, tail jumps and jcc")
say("   forwarders, each route below reaches the world machinery and through it a loader, so the chain is reachable.")
say("   What separates is the gate (E3): every path enters 0026CE60 through 0025BFB0 or 0032F1B0 (E2), and the body")
say("   runs only on an armed slot, which only the binder arms (E5). Shortest path per route, for the record:")
for r0, label in ROUTES.items():
    root = img.owner(r0) or r0
    par, q = {root: None}, [root]
    while q:
        f = q.pop(0)
        if f == 0x0026CE60:
            break
        for c in sorted(callees(f)):
            if c not in par:
                par[c] = f
                q.append(c)
    if 0x0026CE60 in par:
        p, x = [], 0x0026CE60
        while x is not None:
            p.append(x)
            x = par[x]
        say("  %08X (%s): %d hops, last hop %08X; %s" % (r0, label, len(p) - 1, p[1],
                                                      " <- ".join("%08X" % y for y in p[:6]) + " ..."))
        check("E7 %08X reaches 0026CE60 only through 0025BFB0 / 0032F1B0" % r0, p[1] in (0x0025BFB0, 0x0032F1B0))
    else:
        say("  %08X (%s): closure of %d functions does not reach 0026CE60" % (r0, label, len(par)))

# ---------------------------------------------------------------- E8 other filers of slot 1
say("")
fixed1 = [(f, a) for f, a, form, val, O in rc if form == "FIXED" and val == 1]
var = sorted(set(f for f, a, form, val, O in rc if form == "VARIABLE"))
check("E8 Part C: the only fixed read of footer word k 1 is 00266530 at 002669C5", fixed1 == [(0x00266530, 0x002669C5)],
      str([("%08X" % f, "%08X" % a) for f, a in fixed1]))
check("E8 Part C: the variable-slot readers are 002652D0 and 00269860", var == [0x002652D0, 0x00269860],
      str(["%08X" % v for v in var]))
expect(0x00269932, r"mov ebx, 0xe", "E8 00269860 variable slot: 14 (respawn)")
expect(0x0026994D, r"cmovb ebx, r8d", "E8 ... or 7 (spawn) when the header word is below 6")
expect(0x0026993F, r"mov r8d, 7", "E8 ... r8d = 7")
SLOTARG = {0x00268D94: ("r8d = [0209A2BC]", 0x00268D87, r"mov r8d, dword ptr \[rip \+ 0x1e3152e\]"),
           0x00269B48: ("r8d = esi = the class popped by sysreqall 0x0AB", 0x00269B3F, r"mov r8d, esi"),
           0x00269BE3: ("r8d = edi = the class popped by sysreq / sysreqf", 0x00269BDA, r"mov r8d, edi"),
           0x002E2E68: ("r8d = 2 (talk)", 0x002E2E5C, r"mov r8d, 2"),
           0x00265389: ("tail jump from the leaf 00265380 (callers below)", 0x00265389, r"jmp 0x2652d0")}
refs = {s for s, k in code_refs(0x002652D0) if "unwind" not in k}
check("E8 code references to 002652D0 = the five slot-argument sites", refs == set(SLOTARG),
      str(sorted("%08X" % a for a in refs)))
for s, (lab, va, pat) in SLOTARG.items():
    expect(va, pat, "E8 slot argument at %08X: %s" % (s, lab))
refs = {s for s, k in code_refs(0x00265380) if "unwind" not in k}
check("E8 code references to the leaf 00265380 = 0034B388, 0034C67F", refs == {0x0034B388, 0x0034C67F},
      str(sorted("%08X" % a for a in refs)))
expect(0x0034B37F, r"xor r8d, r8d", "E8 0034B388 (entrysync 0x15D) asks for slot 0")
ins = img.fn_ins(0x0034C630)
check("E8 0034C67F is in sysreqwait 0x38C's begin 0034C630, which stores the id and submits nothing",
      not any(x.mnemonic in ("call", "jmp") and x.op_str in ("0x3dbb60", "0x3dbbe0", "0x268850") for x in ins)
      and at(0x0034C684) == "mov dword ptr [rdi + 8], eax", at(0x0034C684))
w2bc = []
for name, ins in rc14_sweep.streams():
    for k, x in enumerate(ins):
        if img.ripmem(x) == 0x0209A2BC and x.operands[0].type == X86_OP_MEM and x.mnemonic == "mov":
            w2bc.append((x.address, x.op_str.split(", ")[-1]))
say("  writers of 0209A2BC: %s" % ", ".join("%08X <- %s" % w for w in w2bc))
check("E8 0209A2BC holds 2 or 10: three stores of 2 and 0025BDE6 storing r12d = 0025BAD0's r9d",
      sorted(w2bc) == [(0x0025AB06, "2"), (0x0025BDE6, "r12d"), (0x0025D67B, "2"), (0x00267102, "2")],
      ", ".join("%08X %s" % w for w in sorted(w2bc)))
expect(0x0025BB1F, r"mov r12d, r9d", "E8 r12d = r9d")
expect(0x0025B984, r"mov r9d, ebx", "E8 0025B990 passes ebx")
expect(0x0025B8C7, r"mov ebx, 0xa", "E8 ... ebx = 10")
expect(0x0025B9D9, r"mov r9d, edx", "E8 0025B9E5 passes edx")
expect(0x0025B9D0, r"mov edx, 2", "E8 ... edx = 2 (and 0025B9BB on the footer path)")
expect(0x0025B9BB, r"mov edx, 2", "E8 ... edx = 2")
refs = {s for s, k in code_refs(0x0025BAD0) if "unwind" not in k}
check("E8 0025BAD0's only callers are 0025B990 and 0025B9E5", refs == {0x0025B990, 0x0025B9E5},
      str(sorted("%08X" % a for a in refs)))

# ---------------------------------------------------------------- E9 class-1 storage
say("")
expect(0x0026CAF4, r"mov qword ptr \[rdi \+ 0x40\], rbx", "E9 binder zeroes the class-1 base (manager +0x40)")
expect(0x0026D2E7, r"cmp qword ptr \[rbx \+ 0x40\], rbp", "E9 armed init: class-1 base still NULL?")
expect(0x0026D2F0, r"mov ecx, dword ptr \[rax \+ 0x38\]", "E9 ... payload header +0x38")
expect(0x0026D2F6, r"mov qword ptr \[rbx \+ 0x40\], rcx", "E9 ... class-1 base = payload + [payload + 0x38]")
expect(0x0026C8F7, r"mov r15, rdx", "E9 the binder's payload r15 is its rdx (0032F850's rdi)")
expect(0x0026C95A, r"mov qword ptr \[rdi\], rdx","E9 ... stored as manager +0x00, the base 0026D2ED reads")

say("")
say("FAILS %d %s" % (len(FAILS), FAILS))
with open(os.path.join(HERE, "rc5m_engine.out"), "w", encoding="utf-8") as w:
    w.write("\n".join(OUT) + "\n")
sys.exit(1 if FAILS else 0)
