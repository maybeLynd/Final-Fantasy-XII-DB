# S-20 probe (OPUS draft, 2026-09-25) - read-only re-drive of EXP-091's own harness.
#
# Imports _experiments/evidence/commit-callees-exec/check.py as a module (bytecode
# writing disabled, so nothing is written into the evidence directory) and re-runs
# its 0030F760 "com-*" fixtures with extra PLANTED PATTERNS and extra READS that
# EXP-091's memprobes do not take:
#   P1  the commitment block +0x700..+0x717 vs its copy +0x718..+0x72F   (commit-action
#       §4 invariant; the-moment CM-5)
#   P2  the target buffer +0x778..+0x97F on band 1 / band 2 / unresolved target
#       (the-moment CM-3, CM-4; target-buffer reset postcondition)
#   P3  refused commits: whole actor + target unit byte diff (commit-action §4 "on
#       refusal only the optional cancel has run")
#   P4  refused commit WITH cancelFirst=1 (commit-action §4 precondition sentence)
#   P5  counterfactual: com-cancel-first with the MRESET stub (0033C9B0) removed, i.e.
#       the shipped body runs; diff of the fields the S-20 invariants assert
# Every run records: return value, final RIP, whether RIP == the return sentinel
# RETQ, final RSP vs entry RSP+8, faults, and the call trace names.
# Evidence class: isolated original-code replay (Unicorn). Not live.
import importlib.util, json, os, struct, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence",
                                    "commit-callees-exec", "check.py"))
spec = importlib.util.spec_from_file_location("exp091", CHK)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RSP

raw, secs, iat_names = m.load_image()
cases, _mut = m.build_cases()
by = {c["name"]: c for c in cases}
U0, U1 = m.unit_addr(0), m.unit_addr(1)
PAT_BLOCK = bytes((0xA0 + i) & 0xFF for i in range(0x30))          # +0x700..+0x72F
PAT_BUF = bytes([0xFF, 0x11, 0x22, 0x33]) + struct.pack("<i", 5) + \
          bytes((0x40 + i) & 0xFF for i in range(0x200))              # +0x778..+0x97F
ENTRY_RSP = m.STACK + 0x80000


def run(case, bodystubs=None, ring=None, setup=None):
    saved = list(m.BODYSTUBS)
    if bodystubs is not None:
        m.BODYSTUBS[:] = bodystubs
    try:
        w = m.build(case, raw, secs, iat_names)
        if ring is not None:
            from unicorn import UC_HOOK_CODE
            def _r(uc, a, s, _):
                ring.append(a)
                if len(ring) > 16:
                    del ring[0]
            w.uc.hook_add(UC_HOOK_CODE, _r)
        if setup is not None:
            setup(w)
        before0 = w.gm.r(U0, m.UNITSZ); before1 = w.gm.r(U1, m.UNITSZ)
        ret = m.invoke(w, case["entry"], rcx=case.get("rcx", 0), rdx=case.get("rdx", 0),
                       r8=case.get("r8", 0), r9=case.get("r9", 0),
                       stack=case.get("stack", ()))
        rip = w.uc.reg_read(UC_X86_REG_RIP); rsp = w.uc.reg_read(UC_X86_REG_RSP)
        after0 = w.gm.r(U0, m.UNITSZ); after1 = w.gm.r(U1, m.UNITSZ)
    finally:
        m.BODYSTUBS[:] = saved
    return dict(ret=hex(ret & 0xFFFFFFFF), final_rip=hex(rip),
                reached_return_sentinel=(rip == m.RETQ),
                rsp_restored=(rsp == ENTRY_RSP + 8), faults=w.faults,
                trace=[t[0] for t in w.trace]), before0, after0, before1, after1


def diff(a, b):
    return [hex(i) for i in range(len(a)) if a[i] != b[i]]


def spans(offs):
    out = []
    for o in (int(x, 16) for x in offs):
        if out and o == out[-1][1] + 1:
            out[-1][1] = o
        else:
            out.append([o, o])
    return ["+%#x..+%#x" % (a, b) if a != b else "+%#x" % a for a, b in out]


def with_fill(case, extra):
    c = dict(case); c["fill"] = list(case.get("fill", [])) + extra; return c


report = {}
# ---- P1 / P2: accepted commits, block + copy + buffer ------------------------------
for name in ("com-b1-basic", "com-b1-edge", "com-b2-lo", "com-b2-hi", "com-notarget",
             "com-gateoff", "com-cancel-first", "com-770-same", "com-posture", "com-masked"):
    c = with_fill(by[name], [(U0 + 0x700, PAT_BLOCK), (U0 + 0x778, PAT_BUF)])
    st, b0, a0, b1, a1 = run(c)
    blk, cpy = a0[0x700:0x718], a0[0x718:0x730]
    st.update(block_700=blk.hex(), copy_718=cpy.hex(), block_equals_copy=(blk == cpy),
              block_fields=dict(flags700=hex(struct.unpack_from("<I", a0, 0x700)[0]),
                                ctx708=hex(struct.unpack_from("<Q", a0, 0x708)[0]),
                                param710=hex(struct.unpack_from("<I", a0, 0x710)[0]),
                                id714=hex(struct.unpack_from("<H", a0, 0x714)[0]),
                                pad716=a0[0x716:0x718].hex()),
              buf_flags_before=hex(b0[0x778]), buf_flags_after=hex(a0[0x778]),
              buf_word1_after=a0[0x779:0x77B].hex(),
              buf_count_after=struct.unpack_from("<i", a0, 0x77C)[0],
              buf_entry0_actor=hex(struct.unpack_from("<Q", a0, 0x780)[0]),
              buf_entry0_tail=a0[0x788:0x790].hex(),
              buf_unchanged=(a0[0x778:0x980] == b0[0x778:0x980]),
              buf_rest_zero=(a0[0x790:0x980] == bytes(0x1F0)),
              phase6b4=hex(a0[0x6B4]),
              target_ea4=hex(struct.unpack_from("<I", a1, 0xEA4)[0]), target_ea8=hex(a1[0xEA8]),
              actor_changed=spans(diff(b0, a0)), target_changed=spans(diff(b1, a1)))
    report["P1P2 " + name] = st

# ---- P2b: band 1 with a DISTINCT resolved-target actorWork at target+0x10 -------------
# EXP-091's fixture leaves target+0x10 = 0, so a resolved append and CM-4's null append
# both store 0. Plant a mapped heap pointer (m.FB) to separate them.
for name in ("com-b1-basic", "com-notarget"):
    c = with_fill(by[name], [(U0 + 0x778, PAT_BUF), (U1 + 0x10, struct.pack("<Q", m.FB))])
    st, b0, a0, b1, a1 = run(c)
    st.update(planted_target_actorwork=hex(m.FB),
              buf_count_after=struct.unpack_from("<i", a0, 0x77C)[0],
              buf_entry0_actor=hex(struct.unpack_from("<Q", a0, 0x780)[0]))
    st.pop("trace")
    report["P2b " + name] = st

# ---- P3: refused commits, nothing written --------------------------------------------
for name in ("com-badid", "com-b1-edge2", "com-b2-oob"):
    c = with_fill(by[name], [(U0 + 0x700, PAT_BLOCK), (U0 + 0x778, PAT_BUF)])
    st, b0, a0, b1, a1 = run(c)
    st.update(actor_changed=spans(diff(b0, a0)), target_changed=spans(diff(b1, a1)))
    report["P3 " + name] = st

# ---- P4: refused id with cancelFirst = 1 ---------------------------------------------
c = with_fill(by["com-badid"], [(U0 + 0x700, PAT_BLOCK), (U0 + 0x778, PAT_BUF)])
c["stack"] = [1]
st, b0, a0, b1, a1 = run(c)
st.update(id714_after=hex(struct.unpack_from("<H", a0, 0x714)[0]),
          ctx708_after=hex(struct.unpack_from("<Q", a0, 0x708)[0]),
          param710_after=hex(struct.unpack_from("<I", a0, 0x710)[0]),
          shadow730_equals_old_copy=(a0[0x730:0x748] == b0[0x718:0x730]),
          buf_count_after=struct.unpack_from("<i", a0, 0x77C)[0],
          actor_changed=spans(diff(b0, a0)), target_changed=spans(diff(b1, a1)))
report["P4 com-badid + cancelFirst=1"] = st

# ---- P5: MRESET real vs stubbed, on com-cancel-first -----------------------------------
base = with_fill(by["com-cancel-first"], [(U0 + 0x700, PAT_BLOCK), (U0 + 0x778, PAT_BUF)])
st_s, _, a_s, _, t_s = run(base)
# Import bridge needed once MRESET's shipped body runs: 004686D0 calls thunk 00861F14 ->
# IAT 008C2BB8 = api-ms-win-crt-math-l1-1-0.dll!sqrtf, which EXP-091 leaves zeroed.
# Bridge: sqrtss xmm0,xmm0 ; ret  (F3 0F 51 C0 C3), placed in EXP-091's STUBS page.
SQRTF_IAT, SQRTF_BRIDGE = 0x8C2BB8, m.STUBS + 0x300
def bridge_sqrtf(w):
    w.gm.w(SQRTF_BRIDGE, bytes.fromhex("f30f51c0c3"))
    w.gm.w(SQRTF_IAT, struct.pack("<Q", SQRTF_BRIDGE))
ring0 = []
st_r0, *_ = run(base, bodystubs=[m.SINK, m.FAMH0, m.FAMH3], ring=ring0)
report["P5a com-cancel-first MRESET real, no extra bridge"] = dict(
    st_r0, last_16_executed=[hex(a) for a in ring0])
ring = []
st_r, _, a_r, _, t_r = run(base, bodystubs=[m.SINK, m.FAMH0, m.FAMH3], ring=ring,
                           setup=bridge_sqrtf)
report["P5 com-cancel-first MRESET stubbed"] = st_s
report["P5b com-cancel-first MRESET real + sqrtf bridge"] = dict(
    st_r, last_16_executed=[hex(a) for a in ring],
    NOTE="diffs below are only meaningful if reached_return_sentinel is True",
    actor_diff_vs_stubbed=spans(diff(a_s, a_r)),
    target_diff_vs_stubbed=spans(diff(t_s, t_r)),
    block_copy_equal_real=(a_r[0x700:0x718] == a_r[0x718:0x730]),
    invariant_fields_identical=all(a_s[x:y] == a_r[x:y] for x, y in
                                   ((0x6B4, 0x6B9), (0x700, 0x730), (0x770, 0x774),
                                    (0x778, 0x980))) and t_s[0xEA4:0xEA9] == t_r[0xEA4:0xEA9])

for k, v in report.items():
    print("==", k)
    for kk, vv in v.items():
        print("  %s: %s" % (kk, vv))
