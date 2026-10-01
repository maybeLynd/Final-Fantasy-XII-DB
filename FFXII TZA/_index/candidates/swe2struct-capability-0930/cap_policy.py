"""REOPENED page (SWE2-STRUCT for OPUS, 2026-10-01):
15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md

Run: python -B cap_policy.py   (last line FAILS n; must be FAILS 0)
Inputs, read only: the certified image (sha 73461d08...) through retool.py / rc9_channels (R.at, R.md, extents), and the
typed BattleUnit access census 04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv. No check reads the page's status
line.

THE FALSIFICATION PASS - the page's headline mechanism: section 2's row-2 bit set published by 00313A00 and its
projection through the static table 01E0C2C0 into the inhibited UI requests {1, 2, 3, 5, 14, 21}, together with
section 7's C-7 writer census ("00313A00 publishes every row-2 bit but 1, 5 and 10 from one condition ... bit 5 goes
through 002E1C40") and the 002E1CD0 polarity stated in the 2026-09-18 evidence-only read.

  C0       the image is the certified EXE
  P1-P2    positive controls: the same argument decoder, run on the four Save/Load sites the page hand-read, gives
           row 1 bit 21 with the page's set / clear split; the table bytes hash to the page's SHA-256
  F1       01E0C2C0 decoded word by word equals section 2's projection table (22 entries)
  F2       00254500 walks 22 policy bits (11 iterations x 2) over 01E0C2C0
  F3       00313A00 writes row 2, bits {0..8, 10, 11, 12, 20}, through 002E1C20 / 002E1CA0 only
  F4       the selection-only bits (the register that follows "[02089350] != 0") are {0, 2, 3, 4, 5, 6, 7, 8, 11, 12, 20}:
           bit 5 IS among them; bit 1 adds 00253B90, bit 10 is the field bit alone
  F5       the tail jmp 002E1C40 (edx = 5, ecx = esi) never touches the policy table: 002E1C40 writes only the words
           0215F1AC (bts when ecx == 0, btr when ecx != 0) and 0215F1B4 (always btr)
  F6       row-2 bits through the table give exactly {1, 2, 3, 5, 14, 21}
  F7       002E1CD0: ecx != 0 clears 0x139203 (and 0xFFEC6DFC at 002E1CE3); ecx == 0 sets it (or at 002E1CFA)
  F8       002E0FA0: 29 call sites across 25 functions; 00313A00 is 289 bytes, called from 00234590 and 00313DB0

THE NULL-LEADER NARROWING (UQ-147's static half, FABLE-REQ-ASTRA-LEADER-STATS-NULL's precondition):
  L1       0023B040: rdi = BattleUnit_GetPartyLeader 003272A0's result; rdi is not written from 0023B089 to 0023B15E, and
           every branch from 0023B0AE through 0023B151 lands inside that range (FABLE's 2026-09-20 reading, re-measured)
  L2       003272A0 returns 0 unless byte [unit] & 8 (unit flag bit 3) - 003272CB
  L3       00236A60 (ResetStateForReuse) clears flag bits 2 and 3 (and dword [rdi], 0xFFFFB0E3 at 00236AA6) and stores
           zero into +0x698 (00236AB4) on one straight line, rdi unchanged
  L4       typed census: the only writes of BattleUnit +0x698 are 00236AB4 (zero) and 0023ABFA (r15)
  L5       typed census: the flag-word writes that can set bit 2 or 3 are exactly 0023AC56 (bit 2) and 00233B4B (bit 3);
           every register-valued write resolves to a constant without bits 2 / 3 or to a read-modify-write of the
           same word through btr / and only
  L6       0023A570: 0023AC56 is reached only through 0023ABFA (no branch from outside lands in 0023ABFB..0023AC56), and
           r15 there is never zero (rax + 0x80 after a non-null test, or [02EBF190] + 8 + 0x1C8 * row)
  L7       00233AD0: 00233B4B (or dword [rbx], 8) is reached only through the jne at 00233AF1, i.e. with bit 2 set
  L8       the unit pool is zeroed when it is allocated: 002368D0 calls memset 00861EC0 (pool, 0, 0x20 * 0xF50)
  L9       the engine itself treats bit 2 as "+0x698 armed": 0023A59C tests bit 2 and then dereferences +0x698 unguarded
  L10      cross-check outside the typed census: every immediate bit-2/3 setter at offset 0 in a function that touches
           +0x698 is one of the two above or a named non-unit base (10 sites, each base pinned)
  L11      no call 0023B040 makes between the leader lookup and 0023B15E can reach the reset 00236A60 or 0023A570
           (direct-call closure, no indirect calls in it)
  M1       the "not exercised" mask-1 callback branch, read statically: 003592C0 updates bit ecx of byte 022C8005, then
           if bit 0 of (022C8004 | 022C8006 | 022C8007 | the new 022C8005) is set it resolves [022C7FE0] through 003588B0
           and tail-calls 0026D6D0; 0023B040 passes ecx = 1, so its own write never decides that branch
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

R = T.R
TSV = os.path.join(DB, "FFXII TZA", "04-Actor-Entity", "Battle-Unit", "battle-unit-accesses.tsv")
FAILS = 0
N = 0


def check(cid, ok, text, detail=""):
    global FAILS, N
    N += 1
    if not ok:
        FAILS += 1
    print("%s %-4s %s%s" % ("PASS" if ok else "FAIL", cid, text, ("  -- " + str(detail)) if detail else ""))


SZ = T.sizes()


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def writes(i):
    try:
        _, w = i.regs_access()
    except Exception:
        return set()
    return {R.full(r)[0] for r in w} - {None}


def imm_target(i):
    if (i.mnemonic == "jmp" or i.mnemonic.startswith("j") or i.mnemonic == "call") and i.operands and i.operands[0].type == 2:
        return i.operands[0].imm
    return None


VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def track(ins, stop_at):
    """Linear constant tracker from the function start to stop_at (exclusive). Values are frozensets of ints."""
    st = {}
    for i in ins:
        if i.address >= stop_at:
            break
        m = i.mnemonic
        ops = i.operands
        if m == "call":
            for r in VOL:
                st.pop(r, None)
            continue
        dst = R.full(ops[0].reg)[0] if ops and ops[0].type == 1 else None
        if m == "xor" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 1 and ops[0].reg == ops[1].reg:
            st[dst] = frozenset([0])
            continue
        if m == "mov" and dst and ops[1].type == 2:
            st[dst] = frozenset([ops[1].imm & 0xFFFFFFFFFFFFFFFF])
            continue
        if m == "mov" and dst and ops[1].type == 1:
            src = R.full(ops[1].reg)[0]
            if src in st:
                st[dst] = st[src]
            else:
                st.pop(dst, None)
            continue
        if m == "lea" and dst:
            mem = ops[1].mem
            if mem.base == T.RIP:
                st[dst] = frozenset([i.address + i.size + mem.disp])
                continue
            b = R.full(mem.base)[0] if mem.base else None
            if mem.index == 0 and b in st:
                st[dst] = frozenset((v + mem.disp) & 0xFFFFFFFF for v in st[b])
                continue
            st.pop(dst, None)
            continue
        if m.startswith("cmov") and dst and ops[1].type == 1:
            src = R.full(ops[1].reg)[0]
            if dst in st and src in st:
                st[dst] = st[dst] | st[src]
            else:
                st.pop(dst, None)
            continue
        for r in writes(i):
            st.pop(r, None)
    return st


def calls_with_args(f, targets):
    """[(site, target set, ecx set, edx set)] for every call/jmp in f whose (possibly register) target is in targets."""
    ins = body(f)
    out = []
    for i in ins:
        if i.mnemonic not in ("call", "jmp") or not i.operands:
            continue
        st = track(ins, i.address)
        op = i.operands[0]
        if op.type == 2:
            tg = frozenset([op.imm])
        elif op.type == 1:
            tg = st.get(R.full(op.reg)[0], frozenset())
        else:
            continue
        if tg and tg <= set(targets):
            out.append((i.address, tg, st.get("rcx"), st.get("rdx")))
    return out


SET, CLR, GATE = 0x002E1C20, 0x002E1CA0, 0x002E1C40

# ---------------------------------------------------------------- C0, P1, P2
exe = open(R.b.EXE, "rb").read() if hasattr(R.b, "EXE") else None
sha = hashlib.sha256(exe).hexdigest() if exe else ""
check("C0", sha.startswith("73461d08") and sha.endswith("d89721f8"), "the image is the certified EXE", sha[:16])

want = {0x005823F8: (CLR, 1, 21), 0x0058252C: (SET, 1, 21), 0x005828B4: (SET, 1, 21), 0x00582F1B: (CLR, 1, 21)}
got = {}
for f in (0x005823B0, 0x00582860):
    for site, tg, ecx, edx in calls_with_args(f, (SET, CLR)):
        got[site] = (min(tg) if len(tg) == 1 else None, min(ecx) if ecx and len(ecx) == 1 else None,
                     min(edx) if edx and len(edx) == 1 else None)
check("P1", got == want, "positive control: the decoder gives row 1 bit 21 at the four hand-read Save/Load sites, "
      "set / clear as the page's table", {"%08X" % k: (hex(v[0]) if v[0] else None, v[1], v[2]) for k, v in sorted(got.items())})

tbl = R.at(0x01E0C2C0, 88)
check("P2", hashlib.sha256(tbl).hexdigest() == "eadec033c5635a6d9375347f46ff568904bd02c1fc465c931bc9f12d714bfd49",
      "01E0C2C0 (88 bytes) hashes to the page's SHA-256 eadec033...")

# ---------------------------------------------------------------- F1, F2
words = [int.from_bytes(tbl[k * 4:k * 4 + 4], "little") for k in range(22)]
proj = {b: sorted(r for r in range(32) if words[b] >> r & 1) for b in range(22)}
page_table = {0: [2], 1: [1, 3, 5], 2: [3], 3: [2], 5: [5], 6: [14], 8: [1, 21], 9: [5, 14], 10: [3]}
expect = {b: page_table.get(b, []) for b in range(22)}
check("F1", proj == expect, "01E0C2C0 decoded equals section 2's table (bits 4, 7, 11-21 zero)",
      {b: v for b, v in proj.items() if v})

ins = body(0x00254500)
txt = [(i.address, i.mnemonic, i.op_str) for i in ins]
lea_tab = [i for i in ins if i.mnemonic == "lea" and i.operands[1].mem.base == T.RIP]
tab = lea_tab[0].address + lea_tab[0].size + lea_tab[0].operands[1].mem.disp if lea_tab else None
it = [i for i in ins if i.mnemonic == "lea" and i.op_str.startswith("r9d") and "0xb" in i.op_str]
reads = [i for i in ins if i.mnemonic == "or" and "rdx" in i.op_str]
check("F2", SZ.get(0x00254500) == 67 and tab == 0x01E0C2C4 and len(it) == 1 and len(reads) == 2
      and "rdx - 4" in reads[0].op_str and "add rdx, 8" in " ".join("%s %s" % (i.mnemonic, i.op_str) for i in ins),
      "00254500 (67 B) walks 11 x 2 = 22 policy bits over 01E0C2C0 (base 01E0C2C4 - 4, stride 8)",
      "tab=%s" % (hex(tab) if tab else None))

# ---------------------------------------------------------------- F3, F4, F5, F6
F = 0x00313A00
ins = body(F)
pol = calls_with_args(F, (SET, CLR))
rows = sorted({min(c[2]) for c in pol if c[2] and len(c[2]) == 1})
bits = sorted(min(c[3]) for c in pol if c[3] and len(c[3]) == 1)
check("F3", SZ.get(F) == 289 and rows == [2] and bits == [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 20] and len(pol) == 13,
      "00313A00 (289 B) writes row 2, bits 0-8, 10, 11, 12, 20, each once, through 002E1C20 / 002E1CA0", {"rows": rows, "bits": bits})

# the selection register: the one that is cmov'd between CLR and SET on ebx (= [02089350] != 0)
sel_reg = None
for i in ins:
    if i.mnemonic == "cmovne" and i.operands[0].type == 1 and i.operands[1].type == 1:
        prev = [j for j in ins if j.address < i.address][-3:]
        if any(j.mnemonic == "test" and j.op_str == "ebx, ebx" for j in prev):
            sel_reg = R.full(i.operands[0].reg)[0]
            break
sel_bits = []
for i in ins:
    if i.mnemonic == "call" and i.operands[0].type == 1 and R.full(i.operands[0].reg)[0] == sel_reg:
        st = track(ins, i.address)
        sel_bits.append(min(st["rdx"]) if st.get("rdx") and len(st["rdx"]) == 1 else None)
cond = next((i for i in ins if i.mnemonic == "cmp" and "rip" in i.op_str), None)
cond_g = cond.address + cond.size + cond.operands[0].mem.disp if cond else None
check("F4", cond_g == 0x02089350 and sel_reg == "rdi" and sorted(sel_bits) == [0, 2, 3, 4, 5, 6, 7, 8, 11, 12, 20],
      "the selection-only bits (call rdi, rdi = SET iff [02089350] != 0) are 0, 2-8, 11, 12, 20 - bit 5 included",
      {"reg": sel_reg, "bits": sorted(sel_bits)})

tail = ins[-1]
st = track(ins, tail.address)
g = body(GATE)
g_refs = sorted({j.address + j.size + op.mem.disp for j in g for op in j.operands if op.type == 3 and op.mem.base == T.RIP})
g_w = [(j.address, j.mnemonic, j.op_str) for j in g if j.mnemonic == "mov" and j.operands[0].type == 3]
bts = [j for j in g if j.mnemonic == "bts"]
btr = [j for j in g if j.mnemonic == "btr"]
je = next(j for j in g if j.mnemonic == "je")
check("F5", tail.mnemonic == "jmp" and imm_target(tail) == GATE and st.get("rdx") == frozenset([5])
      and any(j.mnemonic == "mov" and j.op_str == "ecx, esi" for j in ins[-12:])
      and g_refs == [0x0215F1AC, 0x0215F1B4] and len(g_w) == 2 and len(bts) == 1 and len(btr) == 2
      and imm_target(je) == bts[0].address,
      "the tail jmp 002E1C40(ecx = esi, edx = 5) writes only the words 0215F1AC (bts if ecx == 0, else btr) and "
      "0215F1B4 (btr) - not the policy table 0215F1C0..0215F1FF", ["%08X" % x for x in g_refs])

row2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 20]
req = sorted({r for b in row2 for r in proj[b]})
check("F6", req == [1, 2, 3, 5, 14, 21], "row-2 bits through 01E0C2C0 inhibit exactly requests 1, 2, 3, 5, 14, 21", req)

# ---------------------------------------------------------------- F7, F8
c = body(0x002E1CD0)
t = {i.address: (i.mnemonic, i.op_str) for i in c}
je = next(i for i in c if i.mnemonic == "je")
check("F7", t.get(0x002E1CD0) == ("test", "ecx, ecx") and imm_target(je) == 0x002E1CEB
      and t.get(0x002E1CE3) == ("and", "dword ptr [rcx + rax*4], 0xffec6dfc")
      and t.get(0x002E1CFA) == ("or", "dword ptr [rcx + rax*4], 0x139203") and (~0x139203) & 0xFFFFFFFF == 0xFFEC6DFC,
      "002E1CD0: ecx != 0 falls through to the clear (and ~0x139203, 002E1CE3); ecx == 0 jumps to the set (or 0x139203, 002E1CFA)")

S = T.scan()
cs = S["calls"].get(0x002E0FA0, set())
cl = S["calls"].get(F, set())
check("F8", len(cs) == 29 and len({f for f, _ in cs}) == 25 and {f for f, _ in cl} == {0x00234590, 0x00313DB0},
      "002E0FA0: 29 call sites across 25 functions; 00313A00's callers are 00234590 and 00313DB0",
      "%d / %d" % (len(cs), len({f for f, _ in cs})))

# ---------------------------------------------------------------- L1, L2
L = 0x0023B040
ins = body(L)
a = {i.address: i for i in ins}
w_rdi = [i.address for i in ins if 0x0023B089 < i.address <= 0x0023B15E and "rdi" in writes(i)]
br = [(i.address, imm_target(i)) for i in ins if 0x0023B0AE <= i.address < 0x0023B152 and i.mnemonic.startswith("j")]
check("L1", imm_target(a[0x0023B084]) == 0x003272A0 and a[0x0023B089].op_str == "rdi, rax"
      and a[0x0023B0AE].mnemonic == "je" and imm_target(a[0x0023B0AE]) == 0x0023B0C7
      and a[0x0023B152].op_str == "rax, qword ptr [rdi + 0x698]" and a[0x0023B15E].op_str == "edx, dword ptr [rax + 0x64]"
      and not w_rdi and all(0x0023B0AE <= tg <= 0x0023B152 for _, tg in br),
      "0023B040: rdi = 003272A0's result, unwritten 0023B089..0023B15E; every branch in 0023B0AE..0023B151 stays inside",
      "%d branches" % len(br))

g = {i.address: i for i in body(0x003272A0)}
check("L2", g[0x003272CB].op_str == "byte ptr [rax], 8" and imm_target(g[0x003272CE]) == 0x003272D2
      and g[0x003272D0].op_str == "eax, eax" and imm_target(g[0x003272C1]) == 0x00263E30,
      "003272A0 returns the unit only when byte [unit] & 8 (unit flag bit 3), else 0 (003272CB-003272D0)")

# ---------------------------------------------------------------- L3
ins = body(0x00236A60)
a = {i.address: i for i in ins}
seg = [i for i in ins if 0x00236A93 <= i.address <= 0x00236AB4]
mask = a[0x00236AA6].operands[1].imm & 0xFFFFFFFF
check("L3", a[0x00236A93].op_str == "esi, esi" and a[0x00236AA6].op_str.startswith("dword ptr [rdi]")
      and mask & 0xC == 0 and a[0x00236AB4].op_str == "qword ptr [rdi + 0x698], rsi"
      and not any(i.mnemonic.startswith("j") or i.mnemonic == "call" or writes(i) & {"rdi", "rsi"}
                  for i in seg if i.address != 0x00236A93),
      "00236A60 clears flag bits 2 and 3 (and 0x%08X at 00236AA6) and nulls +0x698 (00236AB4) on one straight line" % mask)

# ---------------------------------------------------------------- L4, L5 (typed census)
rows = []
for ln in open(TSV, encoding="utf-8").read().splitlines()[1:]:
    p = ln.split("\t")
    if len(p) >= 6:
        rows.append(p)
w698 = sorted({p[2] for p in rows if p[3] == "0x698" and "w" in p[4]})
check("L4", w698 == ["00236AB4", "0023ABFA"], "typed census: BattleUnit +0x698 is written only at 00236AB4 (zero) and 0023ABFA", w698)

flagw = sorted({(int(p[0], 16), int(p[2], 16)) for p in rows if p[3] == "0x0" and "w" in p[4]})
imm_set, resolved, unresolved = [], [], []
for f, s in flagw:
    i = next(R.md.disasm(R.at(s, 16), s, 1))
    m, ops = i.mnemonic, i.operands
    if m in ("and", "btr"):
        continue
    if len(ops) > 1 and ops[1].type == 2:
        if (ops[1].imm & 0xC) and m in ("or", "mov"):
            imm_set.append((s, ops[1].imm & 0xFFFFFFFFFFFFFFFF))
        continue
    src = R.full(ops[1].reg)[0] if len(ops) > 1 and ops[1].type == 1 else None
    fi = body(f)
    k = next(n for n, j in enumerate(fi) if j.address == s)
    val = None
    for j in reversed(fi[max(0, k - 40):k]):
        if src not in writes(j):
            continue
        if j.mnemonic in ("movabs", "mov") and j.operands[1].type == 2:
            val = ("const", j.operands[1].imm & 0xFFFFFFFFFFFFFFFF)
        elif j.mnemonic in ("btr", "and") and j.operands[0].type == 1:
            continue
        elif j.mnemonic == "mov" and j.operands[1].type == 3 and j.operands[1].mem.disp == 0 \
                and j.operands[1].mem.base == ops[0].mem.base and j.operands[1].mem.index == 0:
            val = ("rmw", None)
        elif j.mnemonic == "mov" and j.operands[1].type == 3 and j.operands[1].mem.disp == 0:
            # the load is from [y] and the store base was copied from y (mov base, y) earlier in the function
            y = R.full(j.operands[1].mem.base)[0]
            sb = R.full(ops[0].mem.base)[0]
            cp = any(q.mnemonic == "mov" and len(q.operands) == 2 and q.operands[0].type == 1 and q.operands[1].type == 1
                     and {R.full(q.operands[0].reg)[0], R.full(q.operands[1].reg)[0]} == {y, sb} for q in fi[:k])
            val = ("rmw", None) if cp else ("other", "%s %s" % (j.mnemonic, j.op_str))
        else:
            val = ("other", "%s %s" % (j.mnemonic, j.op_str))
        break
    if val and val[0] == "const" and not (val[1] & 0xC):
        resolved.append((s, "const 0x%X" % val[1]))
    elif val and val[0] == "rmw" and m == "mov":
        resolved.append((s, "rmw"))
    else:
        unresolved.append((s, "%s %s" % (m, i.op_str), val))
check("L5", sorted(imm_set) == [(0x00233B4B, 8), (0x0023AC56, 4)] and not unresolved,
      "typed census: the flag-word writes able to set bit 2 or 3 are 0023AC56 (bit 2) and 00233B4B (bit 3) only; "
      "%d register-valued writes all resolve without bits 2/3" % len(resolved),
      {"imm": ["%08X:%X" % x for x in imm_set], "unresolved": unresolved})

# ---------------------------------------------------------------- L6
A = 0x0023A570
ins = body(A)
a = {i.address: i for i in ins}
jmps = [(i.address, imm_target(i)) for i in ins if imm_target(i) and i.mnemonic != "call"]
into = [(s, t_) for s, t_ in jmps if 0x0023ABFB <= t_ <= 0x0023AC56 and not 0x0023ABFA <= s <= 0x0023AC56]
r15w = [i.address for i in ins if "r15" in writes(i)]
# path 1 (class 1): [rsp+0x90] = rax + 0x80 with rax tested non-null, stored once before 0023AA49, reloaded into r15 at
# 0023AA15 / 0023AA2F, each followed by a jmp to 0023ABCA; path 2 (class 0, entered at 0023AA49): r15 =
# [02EBF190] + 8 + rcx at 0023AAAA..0023AAC1. No other r15 write lies between those defs and 0023ABFA.
st90 = [i.address for i in ins if i.address < 0x0023AA49 and i.mnemonic == "mov"
        and i.op_str.startswith("qword ptr [rsp + 0x90],")]
skip1 = [(s, t_) for s, t_ in jmps if s < 0x0023A795 and 0x0023A795 < t_ <= 0x0023AA44]
skip2 = sorted((s, t_) for s, t_ in jmps if s < 0x0023AAC2 and 0x0023AAAB <= t_ <= 0x0023ABFA)
late = [x for x in r15w if 0x0023AAC1 < x < 0x0023ABFA or (0x0023AA15 < x < 0x0023AA49 and x != 0x0023AA2F)]
g190 = a[0x0023AAAA]
nonnull = (a[0x0023A77E].op_str == "rax, rax" and a[0x0023A781].mnemonic == "je" and a[0x0023A787].op_str == "rax, -0x80"
           and st90 == [0x0023A795] and a[0x0023A795].op_str == "qword ptr [rsp + 0x90], rax"
           and a[0x0023AA15].op_str == "r15, qword ptr [rsp + 0x90]" and a[0x0023AA2F].op_str == "r15, qword ptr [rsp + 0x90]"
           and imm_target(a[0x0023AA2A]) == 0x0023ABCA and imm_target(a[0x0023AA44]) == 0x0023ABCA
           and g190.address + g190.size + g190.operands[1].mem.disp == 0x02EBF190
           and a[0x0023AABA].op_str == "r15, 8" and a[0x0023AAC1].op_str == "r15, rcx")
check("L6", a[0x0023ABFA].op_str == "qword ptr [rdi + 0x698], r15" and a[0x0023AC56].op_str == "dword ptr [rdi], 4"
      and not into and nonnull and not skip1 and skip2 == [(0x0023AA2A, 0x0023ABCA), (0x0023AA44, 0x0023ABCA)] and not late,
      "0023A570: bit 2 (0023AC56) is reached only through the arm 0023ABFA, and r15 there is rax + 0x80 after a non-null "
      "test (class-1 path) or [02EBF190] + 8 + 0x1C8 * row (class-0 path) - never zero",
      {"jumps in": into, "skip1": skip1, "skip2": ["%08X->%08X" % x for x in skip2], "late r15": late})


# ---------------------------------------------------------------- L7
ins = body(0x00233AD0)
a = {i.address: i for i in ins}
into = [(i.address, imm_target(i)) for i in ins if imm_target(i) and 0x00233AF3 <= imm_target(i) <= 0x00233B4B
        and i.mnemonic != "call"]
check("L7", a[0x00233AE2].op_str == "rbx, rax" and a[0x00233AEE].op_str == "byte ptr [rax], 4"
      and imm_target(a[0x00233AF1]) == 0x00233B0D and a[0x00233B0C].mnemonic == "ret"
      and a[0x00233B4B].op_str == "dword ptr [rbx], 8"
      and all(0x00233AF1 <= s for s, _ in into),
      "00233AD0: the only bit-3 setter 00233B4B is entered only past the bit-2 test (jne 00233AF1 -> 00233B0D)",
      ["%08X->%08X" % x for x in into])

# ---------------------------------------------------------------- L8
ins = body(0x002368D0)
a = {i.address: i for i in ins}
st = track(ins, 0x00236943)
check("L8", imm_target(a[0x00236943]) == 0x00861EC0 and a[0x0023693C].op_str.startswith("qword ptr [rip")
      and a[0x00236932].op_str == "r8, rcx, 0xf50" and a[0x00236939].op_str == "rcx, rax" and a[0x00236930].op_str == "edx, edx"
      and a[0x002368EB].op_str == "eax, 0x20",
      "002368D0 allocates the 0x20 x 0xF50 unit pool, stores it at 0208E688 and memsets it to zero (00236943)")

# ---------------------------------------------------------------- L9
a = {i.address: i for i in body(A)}
check("L9", a[0x0023A59C].op_str == "byte ptr [rcx], 4" and imm_target(a[0x0023A59F]) == 0x0023A5AE
      and a[0x0023A5A1].op_str == "rax, qword ptr [rcx + 0x698]" and a[0x0023A5A8].op_str == "ebx, word ptr [rax + 4]",
      "0023A570 reads [unit + 0x698] + 4 guarded only by flag bit 2 (0023A59C-0023A5A8): the engine's own bit-2 => armed reading")

# ---------------------------------------------------------------- L10 heuristic cross-check
typed = {int(p[0], 16) for p in rows}
outside = []
for f, n in sorted(SZ.items()):
    d = R.at(f, n)
    if not d:
        continue
    fi = list(R.md.disasm(d, f))
    if not any(op.type == 3 and op.mem.disp == 0x698 for i in fi for op in i.operands):
        continue
    for i in fi:
        if not i.operands or i.mnemonic not in ("or", "mov", "bts"):
            continue
        o = i.operands[0]
        if o.type != 3 or o.mem.disp != 0 or o.mem.index != 0 or o.mem.base in (0, T.RIP) or R.full(o.mem.base)[0] == "rsp":
            continue
        if len(i.operands) < 2 or i.operands[1].type != 2:
            continue
        v = i.operands[1].imm
        if (i.mnemonic == "bts" and v in (2, 3)) or (i.mnemonic != "bts" and v & 0xC):
            if i.address not in (0x00233B4B, 0x0023AC56):
                outside.append(i.address)
pinned = {0x0023429B: "[unit+0x6A0] record (0023427E)", 0x0031F305: "BattleMenu_BuildCommandEntryList's entry (rbx = rcx)",
          0x00321324: "out-parameter rdx", 0x0032134D: "out-parameter rdx", 0x00321386: "out-parameter rdx",
          0x003213AF: "out-parameter rdx (rbx = rdx)", 0x003213CC: "out-parameter rdx (rbx = rdx)",
          0x0032968C: "the r8 argument record 00329220 builds (rdi = r8)", 0x003298A3: "the same r8 record",
          0x003346D4: "[rcx + 0x100] locomotion sub-record (003343F2)"}
check("L10", sorted(outside) == sorted(pinned), "outside the typed census, the immediate bit-2/3 setters at offset 0 are the "
      "10 pinned non-unit bases", ["%08X" % x for x in outside])

# ---------------------------------------------------------------- L11
outs = {}
for tg, s in S["calls"].items():
    for f, _ in s:
        outs.setdefault(f, set()).add(tg)


def closure(f):
    seen, st, ind = {f}, [f], []
    while st:
        x = st.pop()
        if x not in SZ:
            continue
        for i in R.md.disasm(R.at(x, SZ[x]), x):
            if i.mnemonic == "call" and i.operands and i.operands[0].type != 2:
                ind.append(i.address)
            if i.mnemonic == "jmp" and i.operands and i.operands[0].type == 3:
                ind.append(i.address)
        for y in outs.get(x, ()):
            if y in SZ and not x <= y < x + SZ[x] and y not in seen:
                seen.add(y)
                st.append(y)
    return seen, ind


bad = {}
for f in (0x002E8100, 0x00313F60, 0x00322600, 0x00322920, 0x003272A0):
    s, ind = closure(f)
    if 0x00236A60 in s or 0x0023A570 in s or ind:
        bad["%08X" % f] = (0x00236A60 in s, 0x0023A570 in s, ["%08X" % x for x in ind])
check("L11", not bad, "every call 0023B040 makes between the leader lookup and 0023B15E (003272A0, 002E8100, 00313F60, "
      "00322600 x2, 00322920 x2) has a direct-call closure with no indirect call and no path to 00236A60 / 0023A570", bad)

# ---------------------------------------------------------------- M1
ins = body(0x003592C0)
a = {i.address: i for i in ins}
gl = lambda i: i.address + i.size + [op for op in i.operands if op.type == 3][0].mem.disp  # noqa: E731
lb = next(i for i in body(L) if i.address == 0x0023B1C2)
check("M1", gl(a[0x003592C8]) == 0x022C8005 and a[0x003592CF].op_str == "edx, ecx" and a[0x003592E1].op_str == "eax, ecx"
      and [gl(a[x]) for x in (0x003592ED, 0x003592F4, 0x003592FA)] == [0x022C8004, 0x022C8006, 0x022C8007]
      and a[0x00359300].op_str == "al, dl" and a[0x00359302].op_str == "al, 1" and gl(a[0x00359306]) == 0x022C7FE0
      and imm_target(a[0x0035930C]) == 0x003588B0 and imm_target(a[0x0035931D]) == 0x0026D6D0
      and lb.op_str == "ecx, 1",
      "003592C0: after updating bit ecx of 022C8005, bit 0 of the four-byte OR decides the 0026D6D0 call on actor "
      "[022C7FE0]; 0023B040 passes ecx = 1 (0023B1C2), so its write never decides that branch")

print("CHECKS %d" % N)
print("FAILS %d" % FAILS)
