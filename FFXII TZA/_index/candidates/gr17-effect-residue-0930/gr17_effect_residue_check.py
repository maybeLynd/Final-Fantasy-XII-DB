"""gr17_effect_residue_check.py - GR-17 residue: can releasing a battle unit (00234200 -> 00300140(unit, 1) -> ...
-> 00319420, stop the unit's +0x774 effect with sequence 1) deliver a hit that reaches the reward computer 00312280
after the .ard free? (SWE2-ORACLE for OPUS, 2026-09-30)

Static: the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py (extents, disassembly, the cached
direct call/jmp graph), plus the one shipped file the chain reads, c_all.efx (kind 10 id 0), from the VBF extraction in
Tools/work/DATA/mesh54/fx_all (sha256 pinned below; the same parser is run over all 3,288 .efx files as a control).

E1  +0x774 writers: image-wide, the only stores at displacement 0x774 that are not float stores are 00236BE6 (-1, the
    reset) and 0032A045 (eax from 002EACD0, in 00329F80); the five +0x6B0 action-block bases never store +0xC4 (the one
    reader/writer is 00319420, which stores -1); the only bulk writers of the block are the suspend copy 0030EFF0 and
    its restore 0030EDA0 (a copy of the same unit's block).
E2  what 00329F80 puts there: an effect id from the static tables 00D106B0 (9 x 2) / 00D10720 (9 x 5) = {104-111,
    142-147}, created through 002EACD0 -> 003B02A0 with kind 5 (handle = 5 << 28 | counter), source id = unit +8,
    one target = the unit's own id, context = 0024F610({kind 5, id 0}).
E3  the stop route: 00319420 skips handles 0 / -1, else 002EAEA0(h, 1) = 0024FE30, which sends kind 5 to 003B1260 ->
    0024FE70(obj, 1). 0024FE70 runs header byte +0xA+seq (= +0xB) through 00333280 -> 0046EFD0; an effect still in state
    2 is first started through 003A74F0 -> 003337B0 (header bytes +1, +2..+7, +9) -> 003331A0 -> 0046EFD0.
E4  the context is c_all.efx: the only 0024B3A0 build with template byte 5 is 003B0660 (003B0730), which loads resource
    (10, 0) = path array 0215F050 <- 01E127B8 entry 0 = PS2Data\\effect_finish\\jp\\common\\c_all.efx; 0024B3A0
    publishes 02EBEFA8 = ctx + 0x38; the 0x600 / 0x610 / 0x620 handlers 003A79C0 / 003A7B50 / 003A77F0 build the header
    table, the sequence slots and the tracks the checker's parser mirrors.
E5  0046EFD0 hands 003B8670 only tracks with index >= 1, flag +5 bit 0 and kind +1 == 2; its other launches
    (003A8AE0 for kind 1, 004FF2C0 -> 005372D0 for kind 3, 003A8020 / 003A8240 / 0046EF10 / 00314960 / 001EDDA0) do not
    reach 00312280.
E6  which timeline opcodes can reach 00312280: the 003B8670 opcode table (003B994C / 003B9854) gives direct routes only
    through opcodes 3, 13, 17, 26, 34, 37, 40, 128 and indirect calls in 24 and 31; 00319F50 reaches 0030E360 only on
    event kinds 0 (003191B0) and 2 (00300520), and the opcodes pass kinds 3 -> 0, 13 -> 1, 26 -> 3/6/7/8, 34 -> 2,
    37 -> 4, 128 -> 5 (128 joins the call at 003B8A13, past 26's `xor edx, edx`, so it keeps its target). So the opcodes
    that can reach are exactly {3, 34, 17, 40} plus the indirect {24, 31}.
E7  data: c_all.efx has 40 kind-2 timeline tracks in all; their opcodes are {5, 6, 9, 25, 26, 39, 41}; none is in the
    reaching set. For each of the 14 ids: sequence 1 -> slot 2 -> one kind-2 track firing 6, 41, 25 at time 0; the start
    slot 1 fires 5. None of those arms reaches 00312280.
E8  the release does not exclude the unit by liveness: 003588B0 needs the manager's loaded bit, cleared (00262DA8) only
    after the release loop (00262D34); 003105D0 / 00310780 need +0x698 != 0, zeroed only by the memset at 002342CE after
    the release's 0023423F call; kind 2 targets the acting unit (context +8 = unit +8). The gate therefore is the data.
C1  parser control: the same parser finds opcode 3 (347) and 34 (6) across the 3,288 shipped .efx files; every c_all
    header slot reference has its 0x610 chunk; every kind-2 track's entries fit and are time-sorted.
C2  graph control: 003B1260, 0046EFD0 and 00319F50 do reach 00312280 in the direct graph (the question is live).
Prints PASS/FAIL per check and FAILS n last.
"""
import collections, glob, hashlib, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
CALLS = SC["calls"]
FXROOT = os.path.join(DB, "Tools", "work", "DATA", "mesh54", "fx_all")
CALL_EFX = os.path.join(FXROOT, "ps2data", "effect_finish", "jp", "common", "c_all.efx")
CALL_SHA = "0f2f15d9787f4d234f54ba978797ed3687956482aa2f3a456e382cb617869029"
B = 0x00120000
TGT = 0x00312280
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a, n=16):
    return next(R.md.disasm(R.at(a, n), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def u32(a):
    return struct.unpack("<I", R.at(a, 4))[0]


def same(pairs):
    return [("%08X" % a, txt(a), t) for a, t in pairs.items() if txt(a) != t]


FWD = collections.defaultdict(set)
for t, cs in CALLS.items():
    for f, s in cs:
        FWD[f].add(t)


def reaches(src, dst=TGT):
    seen, q = {src}, [src]
    while q:
        f = q.pop()
        if f == dst:
            return True
        for t in FWD.get(f, ()):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return False


def arm_calls(fn, start, stops):
    """direct call targets (and indirect sites) reachable inside fn from start, not crossing stops"""
    code = {i.address: i for i in body(fn)}
    seen, out, q = set(), set(), [start]
    while q:
        x = q.pop()
        while x not in seen and x not in stops:
            seen.add(x)
            i = code.get(x)
            if i is None:
                out.add(("gap", x))
                break
            m = i.mnemonic
            if m == "call":
                out.add(int(i.op_str, 16) if i.op_str.startswith("0x") else ("ind", x))
            if m == "ret":
                break
            if m == "jmp":
                if not i.op_str.startswith("0x"):
                    out.add(("indj", x))
                    break
                t = int(i.op_str, 16)
                if fn <= t < fn + SZ[fn]:
                    x = t
                    continue
                out.add(t)
                break
            if m.startswith("j"):
                q.append(int(i.op_str, 16))
            x = i.address + i.size
    return out


# ---------------------------------------------------------------- E1: who writes +0x774
st774, bases, c4 = [], [], []
for f, n in sorted(SZ.items()):
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        ops = i.operands
        if ops and ops[0].type == 3 and ops[0].mem.disp == 0x774 and i.mnemonic.startswith("mov"):
            st774.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
        if any(o.type == 3 and o.mem.disp == 0x6B0 for o in ops) and i.mnemonic == "lea" or \
                (i.mnemonic == "add" and len(ops) == 2 and ops[1].type == 2 and ops[1].imm == 0x6B0):
            bases.append((f, i.address))
nonfloat = [(f, a, t) for f, a, t in st774 if not t.startswith("movss") and "0x3fb4fdf4" not in t]
e1_st = [(a, t) for f, a, t in nonfloat] == [(0x00236BE6, "mov dword ptr [rdi + 0x774], 0xffffffff"),
                                            (0x0032A045, "mov dword ptr [rbx + 0x774], eax")]
e1_call = txt(0x0032A040) == "call 0x2eacd0"
base_fns = sorted({f for f, a in bases})
for f in base_fns:
    for i in body(f):
        if i.operands and i.operands[0].type == 3 and i.operands[0].mem.disp == 0xC4 and f != 0x003CA860:
            c4.append("%08X" % i.address)
e1_blk = same({0x0030F0AC: "mov r8d, 0x4f0", 0x0030F0EC: "call 0x861ec0", 0x0030F0F1: "mov qword ptr [rbx + 0xb88], rdi",
               0x0030EDA0: "mov r8, qword ptr [rcx + 0xb88]", 0x0030EDA7: "add rcx, 0x6b0",
               0x00319429: "mov ecx, dword ptr [rcx + 0xc4]", 0x00319441: "mov dword ptr [rbx + 0xc4], 0xffffffff"})
check("E1", e1_st and e1_call and base_fns == [0x00304850, 0x0030EDA0, 0x0030EFF0, 0x00310780, 0x003CA860]
      and not c4 and not e1_blk,
      "+0x774 stores (non-float) %s; float stores elsewhere %s; +0x6B0 base fns %s; [base+0xC4] stores %s; block copy %s"
      % (["%08X" % a for f, a, t in nonfloat], ["%08X" % a for f, a, t in st774 if (f, a, t) not in nonfloat],
         ["%08X" % f for f in base_fns], c4 or "none", e1_blk or "as read"))

# ---------------------------------------------------------------- E2: which effects 00329F80 creates
A = struct.unpack("<18i", R.at(0x00D106B0, 72))
Bt = struct.unpack("<45i", R.at(0x00D10720, 180))
ids = sorted(set(A + Bt) - {-1})
e2 = same({0x00329F86: "cmp dword ptr [rcx + 0x774], -1", 0x00329FEC: "cmp ecx, 8",
           0x0032A00C: "mov r9d, dword ptr [rax + rdx*4 + 0xbf06b0]", 0x0032A026: "mov r9d, dword ptr [rax + rcx*4 + 0xbf0720]",
           0x0032A034: "mov ecx, dword ptr [rbx + 8]", 0x0032A037: "lea r8, [rbx + 8]", 0x0032A03B: "mov edx, 1",
           0x002EACE5: "mov dword ptr [rsp + 0x20], 5", 0x002EACF0: "call 0x3b02a0",
           0x003B03C6: "shl eax, 0x1c", 0x003B03F3: "mov byte ptr [rsp + 0x30], 5", 0x003B03F8: "mov word ptr [rsp + 0x34], r15w",
           0x003B03FE: "call 0x24f610", 0x003B04DA: "mov dword ptr [rbx + 8], eax", 0x003B053D: "mov dword ptr [rbx + rcx*4 + 0x10], eax",
           0x003B0592: "mov qword ptr [rbx + 0x340], r12", 0x003B0599: "mov word ptr [rbx + 0x370], 0x102",
           0x003B05AC: "mov byte ptr [rbx + 0x373], dil"})
check("E2", ids == [104, 105, 106, 107, 108, 109, 110, 111, 142, 143, 144, 145, 146, 147] and not e2 and
      sorted(f for f, s in CALLS.get(0x00329F80, ())) == [0x00304850],
      "effect ids %s (tables 00D106B0 / 00D10720, selector [r9+0x21] <= 8); kind 5, source = unit+8, one target = "
      "&unit+8, context 0024F610({5,0}); mismatches %s" % (ids, e2 or "none"))

# ---------------------------------------------------------------- E3: the stop route and what it runs
kind5 = same({0x0024FE32: "sar eax, 0x1c", 0x0024FE42: "cmp eax, 6", 0x0024FE45: "jbe 0x24fe59", 0x0024FE59: "jmp 0x3b1260",
              0x0031942F: "lea eax, [rcx + 1]", 0x00319432: "cmp eax, 1", 0x00319435: "jbe 0x319441",
              0x00319437: "mov edx, 1", 0x0031943C: "call 0x2eaea0", 0x002EAEA0: "jmp 0x24fe30",
              0x003B12D4: "call 0x24fe70",
              0x0024FEAB: "cmp al, 2", 0x0024FEC7: "call 0x3a74f0", 0x0024FF23: "movzx ecx, byte ptr [rsi + rdx + 0xa]",
              0x0024FF2F: "mov ecx, dword ptr [rdx + rcx*4 + 0x2c]", 0x0024FF42: "call 0x333280",
              0x00333303: "call 0x46efd0", 0x003A7590: "call 0x3337b0",
              0x0033386B: "mov ecx, dword ptr [rcx + rax*4 + 0x2c]", 0x00333897: "movzx eax, byte ptr [rcx + rbx + 2]",
              0x003338E1: "cmp rbx, 6", 0x00333957: "movzx eax, byte ptr [rcx + 9]", 0x0033323A: "call 0x46efd0"})
check("E3", not kind5,
      "00319420 skips 0/-1 -> 002EAEA0(h,1) = 0024FE30 -> kind 5 -> 003B1260 -> 0024FE70(obj,1): header byte +0xB -> "
      "00333280 -> 0046EFD0; state 2 first starts header bytes +1,+2..+7,+9 via 003A74F0 -> 003337B0 -> 003331A0; "
      "mismatches %s" % (kind5 or "none"))

# ---------------------------------------------------------------- E4: the kind-5 context is c_all.efx
builds = sorted(s for f, s in CALLS.get(0x0024B3A0, ()))
tmpl = {0x0026FC6C: 2, 0x002FC541: 1, 0x003B0730: 5, 0x003B2250: 7, 0x003B2A60: 4, 0x003B3977: 3}
tbad = [("%08X" % a, txt(a)) for a, v in tmpl.items() if not txt(a).startswith("mov byte ptr [rsp + ") or not txt(a).endswith(", %d" % v)]
path_slot = u32(0x01E127B8) | (u32(0x01E127BC) << 32)
e4 = same({0x003B06E0: "xor edx, edx", 0x003B06E2: "lea ecx, [rdx + 0xa]", 0x003B06E5: "call 0x32e400",
           0x003B070A: "lea ecx, [rdx + 0xa]", 0x003B070D: "call 0x32e620", 0x003B073A: "call 0x24b3a0",
           0x003B0745: "call 0x3edad0", 0x002DF9FD: "lea rax, [rip + 0x1b32db4]",
           0x002DFA04: "mov qword ptr [rip + 0x1e7f645], rax",
           0x0024B48A: "lea rax, [rbx + 0x38]", 0x0024B48E: "mov qword ptr [rip + 0x2c73b13], rax",
           0x003A79E5: "mov byte ptr [rsi], bpl", 0x003A7A10: "mov qword ptr [rax + rcx*8 + 8], rsi",
           0x003A7B91: "mov dword ptr [r9 + rbx*4 + 0x2c], eax", 0x003A7BA8: "lea rcx, [r14 + 0x24]",
           0x003A7845: "lea rdx, [rsi + 0x10]", 0x003A785D: "mov dword ptr [rbp + rdx*4 + 0x20], eax",
           0x003EDE3C: "call 0x3a79c0", 0x003EDE64: "call 0x3a7b50", 0x003EDEA7: "call 0x3a77f0"})
check("E4", len(builds) == 6 and not tbad and not e4 and path_slot == 0x0096BEA0
      and T.cstr(0x0096BEA0) == "PS2Data\\effect_finish\\jp\\common\\c_all.efx",
      "0024B3A0 builds %d, template byte 5 only at 003B0730 (003B0660 loads (10,0)); path 0215F050 <- 01E127B8[0] = %r; "
      "header/sequence/track handlers as read; mismatches %s" % (len(builds), T.cstr(path_slot), (tbad + e4) or "none"))

# ---------------------------------------------------------------- E5: 0046EFD0 launches
e5 = same({0x0046F05C: "cmp esi, eax", 0x0046F068: "mov ebx, r12d", 0x0046F083: "mov ecx, dword ptr [r13 + rax*4 + 0x20]",
           0x0046F092: "test byte ptr [rax + 5], r12b", 0x0046F098: "cmp byte ptr [rax + 1], 2", 0x0046F0AF: "call 0x3b8670",
           0x0046F129: "movzx ecx, byte ptr [rbx + 1]", 0x0046F132: "cmp ecx, 2", 0x0046F14B: "call 0x4ff2c0",
           0x004FF2D5: "cmp dl, 3", 0x004FF2DD: "call 0x5372d0"})
others = sorted(t for t in FWD[0x0046EFD0] if t not in (0x003B8670, 0x004FF2C0)
                and not 0x0046EFD0 <= t < 0x0046EFD0 + SZ[0x0046EFD0])
e5_reach = [("%08X" % t) for t in others + [0x005372D0] if reaches(t)]
check("E5", not e5 and not e5_reach,
      "only kind-2 tracks (index >= 1, +5 bit 0) reach 003B8670; kind 3 -> 004FF2C0 -> 005372D0; other callees %s; "
      "reaching %s; mismatches %s" % (["%08X" % t for t in others], e5_reach or "none", e5 or "none"))

# ---------------------------------------------------------------- E6: opcodes that can reach 00312280
F8 = 0x003B8670
case = {}
for op in range(1, 129):
    k = R.at(B + 0x29994C + op - 1, 1)[0]
    case[op] = u32(B + 0x299854 + 4 * k) + B
STOP = {0x003B88F4, 0x003B88F8, 0x003B8740, 0x003B97EE}
direct, indirect = {}, {}
for op, t in case.items():
    cs = arm_calls(F8, t, STOP)
    r = sorted(c for c in cs if isinstance(c, int) and reaches(c))
    if r:
        direct[op] = r
    ind = [c for c in cs if not isinstance(c, int)]
    if ind:
        indirect[op] = ind
F9 = 0x00319F50
arm = [u32(B + 0x1FA200 + 4 * k) + B for k in range(9)]
arm_reach = [k for k in range(9) if any(isinstance(c, int) and reaches(c)
                                        for c in arm_calls(F9, arm[k], {0x0031A1D7, 0x0031A1D5, 0x0031A1CE}))]
params = same({0x003B8822: "mov dword ptr [rsp + 0x30], ebp", 0x003B87EE: "mov r14d, ebp",
               0x003B895F: "mov dword ptr [rsp + 0x30], r12d", 0x003B89C3: "mov dword ptr [rsp + 0x30], 8",
               0x003B89CD: "mov dword ptr [rsp + 0x30], 7", 0x003B89D7: "mov dword ptr [rsp + 0x30], 6",
               0x003B89ED: "mov dword ptr [rsp + 0x30], 3", 0x003B91B5: "mov dword ptr [rsp + 0x30], 2",
               0x003B923B: "mov dword ptr [rsp + 0x30], 4", 0x003B933D: "mov dword ptr [rsp + 0x30], 5",
               0x003B8A11: "xor edx, edx", 0x003B935B: "jb 0x3b8a13",
               0x003B8A13: "mov ecx, dword ptr [r9 + 8]", 0x0031A160: "test rdi, rdi", 0x00319FB9: "movsxd rax, dword ptr [rsi]"})
kinds = {3: {0}, 13: {1}, 26: {3, 6, 7, 8}, 34: {2}, 37: {4}, 128: {5}}
via_eb = {op for op, r in direct.items() if r == [0x002EB740]}
danger = {op for op in via_eb if kinds.get(op, {-1}) & set(arm_reach)} | {op for op in direct if op not in via_eb}
DANGER = danger | set(indirect)
check("E6", sorted(direct) == [3, 13, 17, 26, 34, 37, 40, 128] and sorted(indirect) == [24, 31] and arm_reach == [0, 2]
      and via_eb == set(kinds) and not params and sorted(DANGER) == [3, 17, 24, 31, 34, 40],
      "direct-reaching opcodes %s (17 -> 002FD0C0, 40 -> 003B3C00, rest -> 002EB740); indirect in %s; 00319F50 arms "
      "reaching 0030E360 %s; event kinds per opcode %s; reaching set %s; mismatches %s"
      % (sorted(direct), sorted(indirect), arm_reach, {k: sorted(v) for k, v in kinds.items()}, sorted(DANGER),
         params or "none"))


# ---------------------------------------------------------------- the c_all.efx parser (mirrors E4's handlers)
def chunks(d):
    o, out = 16, []
    while o + 8 <= len(d):
        ln, fl, ty = struct.unpack_from("<IHH", d, o)
        if ln < 8:
            return out, o
        out.append((o, ln, fl, ty))
        o += ln
    return out, o


def entries(Tr):
    return [(Tr[0x14 + 16 * k], struct.unpack_from("<H", Tr, 0x16 + 16 * k)[0])
            for k in range(Tr[0x10]) if 0x14 + 16 * k + 16 <= len(Tr)]


def track(d, o):
    return d[o + 0x1C:o + struct.unpack_from("<I", d, o)[0]]


d = open(CALL_EFX, "rb").read()
sha = hashlib.sha256(d).hexdigest()
ch, end = chunks(d)
hdr, seqs, trk = {}, {}, collections.defaultdict(dict)
for o, ln, fl, ty in ch:
    p = o + 0xC
    if ty == 0x600:
        hdr[d[p + 1]] = d[p + 4:p + 4 + 0xA0]            # 003A79C0: table[p[1]] = p + 4
    elif ty == 0x610:
        seqs[(d[p], d[p + 1])] = (d[p + 7] or 0x40)      # 003A7B50: slot q[1] of header q[0]; count S[3]
        trk[(d[p], d[p + 1])] = {}                       # its memset clears the track table
    elif ty == 0x620:
        trk[(d[p], d[p + 1])][d[p + 2]] = o              # 003A77F0: track s[2] = chunk + 0x1C
k2 = [(key, t, track(d, o)) for key, tr in trk.items() for t, o in tr.items() if track(d, o)[1] == 2]
ops_all = collections.Counter(e[0] for key, t, Tr in k2 for e in entries(Tr))


def fired(i, slot):
    """leading time-0 opcodes of every launchable kind-2 track of sequence (i, slot)"""
    out = []
    n = seqs.get((i, slot), 0)
    for t, o in sorted(trk.get((i, slot), {}).items()):
        Tr = track(d, o)
        if 1 <= t < n and Tr[5] & 1 and Tr[1] == 2:
            z = []
            for op, tm in entries(Tr):
                if tm > 0:
                    break
                z.append(op)
            out.append(z)
    return out


per = {}
for i in ids:
    h = hdr.get(i)
    if h is None:
        per[i] = None
        continue
    stop = fired(i, h[0xB]) if h[0xB] else []
    start = [fired(i, h[x]) for x in list(range(1, 8)) + [9] if h[x]]
    per[i] = (h[0xB], stop, start)
flat = set(ops_all)
cand_ops = {op for v in per.values() if v for seq in [v[1]] + v[2] for tr in seq for op in tr}
check("E7", sha == CALL_SHA and end == len(d) == 1017904 and len(hdr) == 191 and len(seqs) == 218
      and sum(len(v) for v in trk.values()) == 1272 and len(k2) == 40 and sorted(flat) == [5, 6, 9, 25, 26, 39, 41]
      and not (flat & DANGER) and all(v == (2, [[6, 41, 25]], [[[5]]]) for v in per.values()),
      "c_all.efx sha256 %s..., %d B walked to %d; headers %d, sequences %d, tracks %d, kind-2 tracks %d; opcodes in the "
      "whole file %s; reaching opcodes present %s; the 14 ids: seq1 -> slot 2 fires %s at time 0, start slot 1 fires %s"
      % (sha[:12], len(d), end, len(hdr), len(seqs), sum(len(v) for v in trk.values()), len(k2), dict(sorted(ops_all.items())),
         sorted(flat & DANGER) or "none", sorted({tuple(x) for v in per.values() if v for x in v[1]}),
         sorted({tuple(x) for v in per.values() if v for s in v[2] for x in s})))

# ---------------------------------------------------------------- E8: liveness does not exclude the unit
e8 = same({0x003588E6: "call 0x263ff0", 0x003588FF: "test byte ptr [rax + 0x10], 1",
           0x00263FF3: "lea rcx, [rip + 0x1e34e16]", 0x00262D34: "call 0x25b070",
           0x00262DA8: "and byte ptr [rbx + 0x10], 0xfe",
           0x003105DE: "cmp qword ptr [rcx + 0x698], 0", 0x0031078E: "cmp qword ptr [rcx + 0x698], 0",
           0x0023423F: "call 0x300140", 0x002342CE: "call 0x861ec0",
           0x0031A089: "mov rcx, qword ptr [rbx + 0x698]", 0x0031A09B: "call 0x300520",
           0x00300520: "sub edx, dword ptr [rcx + 0x48]", 0x00300553: "call 0x31b860",
           0x003B897E: "mov ecx, dword ptr [rax + 8]",
           0x00319FA3: "test byte ptr [rax], 2", 0x00319FAC: "call 0x306bb0",
           0x00306BB8: "add eax, -5"})
check("E8", not e8 and 0x00262D34 < 0x00262DA8 and 0x0023423F < 0x002342CE,
      "003588B0 needs [mgr+0x10] bit 0, cleared at 00262DA8 after the release loop 00262D34; 003105D0 / 00310780 need "
      "+0x698, zeroed at 002342CE after 0023423F; kind 2 = HP -= HP on the acting unit's own +0x698; unsettled gates "
      "00319FA3 (unit bit 1) and 00306BB0 ([022C2160] in 5..6); mismatches %s" % (e8 or "none"))

# ---------------------------------------------------------------- C1: parser control
all_ops, nfiles = collections.Counter(), 0
for P in glob.glob(os.path.join(FXROOT, "**", "*.efx"), recursive=True):
    x = open(P, "rb").read()
    if x[:3] != b"EFX":
        continue
    nfiles += 1
    for o, ln, fl, ty in chunks(x)[0]:
        if ty == 0x620 and ln > 0x1C + 0x14:
            Tr = track(x, o)
            if Tr[1] == 2:
                all_ops.update(e[0] for e in entries(Tr))
missing = [(i, s) for i, h in hdr.items() for s in list(h[1:10]) + list(h[0xB:0x15]) if s and (i, s) not in seqs]
fit = all(len(entries(Tr)) == Tr[0x10] for key, t, Tr in k2)
srt = all([e[1] for e in entries(Tr)] == sorted(e[1] for e in entries(Tr)) for key, t, Tr in k2)
check("C1", nfiles == 3288 and all_ops[3] == 347 and all_ops[34] == 6 and not missing and fit and srt
      and max(all_ops) == 128 and not any(64 <= k < 128 for k in all_ops),
      "%d .efx files: opcode 3 x%d, 34 x%d, 17 x%d, 40 x%d (range %d..%d, none in the 64..127 no-op band); c_all header "
      "refs without a 0x610 %d; entries fit %s; time-sorted %s"
      % (nfiles, all_ops[3], all_ops[34], all_ops[17], all_ops[40], min(all_ops), max(all_ops), len(missing), fit, srt))

# ---------------------------------------------------------------- C2: graph control
live = {"%08X" % a: reaches(a) for a in (0x003B1260, 0x0046EFD0, 0x00319F50, 0x00300140)}
check("C2", all(live.values()), "direct-graph reach to 00312280: %s" % live)

print("FAILS %d" % fails)
