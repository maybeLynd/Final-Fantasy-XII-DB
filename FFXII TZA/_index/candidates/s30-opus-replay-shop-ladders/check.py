"""S-30: execute CONTRACT-shop-stock-ladders.md's entries - the gate 002FAD40, the listing 002FA920, the row name 002FAE40, the
rank thunk 002536F0 and the clan rank 00315390 - as shipped code over the SHIPPED shop table, bound by the shipped binder, and
test SG-1..SG-7 (OPUS, 2026-09-25, block 324).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session with stack arguments from
block 323) supplies the image, the IAT traps and the named bridges; its world is built once. No application stub and no stop
boundary.
THE TABLES ARE THE SHIPPED ONES, BOUND BY SHIPPED CODE. battle_pack.bin (us, sha256 below) is copied raw to B = 0x76100000; then
the delivery path's own steps run: 003846F0(&[0208E680], B, 0) - 00238850's first call - turns the directory's 71 offsets into
pointers, then the two inner binders 00236C30 calls for these tables run on their directory entries: 00238160 (+0x38, the
equipment rows -> [02EBF0F8], which the listing's category test reads) and 00238660 (+0xA0, the shop table -> [02EBF158]).
00236C30 itself is not run whole: its gambit binder 00238880 allocates from engine heap 6, which halts unbuilt (block 321).
The codec base [01F83530] stays at the image's 0; the delivery path is only self-consistent with 0 (00238850 stores the ENCODED
blob address in [0208E680] and 00236C30 dereferences that cell as a raw pointer), and with 0 resolve is the identity.
Other fixtures (planted data only): the story-progress operand (the u16 array behind [02098E58], enabled by [02098E20] bit 0,
which 00264640 reads for query class 3), the clan-rank block behind [020927C0] (+0x3868 points, +0x3844 bits), the object behind [02092758] (the rank path 00316930 -> 00254E80 stores
into its +0x0C), and the
synthetic sections used for SG-3..SG-5 and SG-7, written in fixture memory and encoded relative to the codec base the same way.
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RSI

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
PACK = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "test_battle", "us",
                    "binaryfile", "battle_pack.bin")
PACK_SHA = "d1bb89aac759cfcd4eb181715d9e88afb78d62a9a3fcffa6242f365f182cbc98"
GATE, LIST, NAME, THUNK, RANK, BINDER, QUERY, CLASSIFY = 0x2FAD40, 0x2FA920, 0x2FAE40, 0x2536F0, 0x315390, 0x238660, 0x321190, 0x2FABD0
RELOCATE, EQUIP_BINDER, DELIVERY_CELL = 0x3846F0, 0x238160, 0x208E680
W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (GATE, LIST, NAME, THUNK, RANK, BINDER, CLASSIFY, RELOCATE, EQUIP_BINDER)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc

CODEC, SLOT, STORY_FLAG, STORY_PTR, RANK_CELL, BANK_CELL = 0x1F83530, 0x2EBF158, 0x2098E20, 0x2098E58, 0x20927C0, 0x2092758
B, DIR = 0x76100000, 0x22418
SYN, STORY, RANKBLK, BANK, OUT = B + 0x50000, B + 0x60000, B + 0x61000, B + 0x65000, B + 0x70000


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def run(fn, *args, stack=()):
    ok = S.call(fn, *args, stack=stack)
    return ok, uc.reg_read(UC_X86_REG_RAX)


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- bind the shipped table with the shipped code ----
pack = open(PACK, "rb").read()
assert hashlib.sha256(pack).hexdigest() == PACK_SHA
uc.mem_write(B, pack)
okr, _ = run(RELOCATE, DELIVERY_CELL, B, 0)            # 00238850's first step: the directory's 71 offsets become pointers
direntry = lambda off: r(B + off, "<I")[0]
oke, _ = run(EQUIP_BINDER, direntry(0x38))            # 00236D73/00236D76: eitm_data -> [02EBF0F8]
okb, _ = run(BINDER, direntry(0xA0))                  # 00236F28/00236F2E: the shop table -> [02EBF158]
okb = okr and oke and okb and direntry(0xA0) == B + DIR
hdr = r(SLOT, "<Q")[0]
tag, stride, count, data = r(hdr, "<IHHI")
res = lambda x: x                                      # the codec base [01F83530] is 0: resolve is the identity


def row(i):
    return res(data) + i * stride


def entries(i):
    """Independent Python walk of row i: [(entry address, kind, operand, threshold, [ids])]."""
    sec = res(r(row(i) + 4, "<I")[0])
    _, es, ec, ed = r(sec, "<IHHI")
    out = []
    for j in range(ec):
        ea = res(ed) + j * es
        kind, opi, thr, lst = r(ea, "<BBHI")
        la = res(lst)
        _, ls, lc, ld = r(la, "<IHHI")
        out.append((ea, kind, opi, thr, [r(res(ld) + k * ls, "<H")[0] for k in range(lc)]))
    return out


r3 = entries(3)
r0 = entries(0)
bind_ok = (okb and hdr == B + DIR and (tag, stride, count) == (0x64, 8, 57) and r3[0][1:4] == (2, 0, 200)
           and r3[0][4][:2] == [0x1002, 0x1037] and r3[-1][4][0] == 0x108B and r0[-1][4][:3] == [0x000A, 0x0000, 0x118C])
census = {"entries": sum(len(entries(i)) for i in range(count)), "ids": sum(len(e[4]) for i in range(count) for e in entries(i))}
record("bind_shipped_table", bind_ok and census == {"entries": 267, "ids": 2512}, header=["0x%X" % tag, stride, count], census=census,
       note="00238660 binds directory +0xA0: header {0x64, 8, 57}; row 3 opens with story >= 200 (Longsword 0x1002, Cypress Pole 0x1037) "
            "and ends in Mace 0x108B; row 0's base entry is Eye Drops, Potion, Onion Bolts; 267 entries, 2,512 ids (the page's census)")

# ---- the gate's inputs ----
uc.mem_write(STORY, bytes(0x200))
w(STORY_FLAG, "<B", 1)
w(STORY_PTR, "<Q", STORY)
uc.mem_write(RANKBLK, bytes(0x4000))
w(RANK_CELL, "<Q", RANKBLK)
uc.mem_write(BANK, bytes(0x100))
w(BANK_CELL, "<Q", BANK)                              # 00316930 -> 00254E80 stores a value at [[02092758] + 0xC]


def story(v, element=0):
    w(STORY + 2 * element, "<H", v & 0xFFFF)


exits = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: exits.append(u.reg_read(UC_X86_REG_RSI) & 0xFFFFFFFF), begin=0x2FAE28, end=0x2FAE28)
gate_calls, query_calls = [], []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: gate_calls.append(1), begin=GATE, end=GATE)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: query_calls.append(tuple(u.reg_read(x) & 0xFF for x in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8))),
            begin=QUERY, end=QUERY)


def gate(row_addr):
    """Run the gate; return (entry address, esi at the common exit 002FAE28: the passing index, or the count if exhausted)."""
    del exits[:]
    ok, a = run(GATE, row_addr)
    assert ok, (S.st["bad"] or S.st["faults"])[:2]
    return a, exits[-1] if exits else None


def expected_gate(i, sv, rank=1):
    es = entries(i)
    for k, e in enumerate(es):
        kind, thr = e[1], e[3]
        if kind == 0 or (kind in (1, 2) and sv >= thr) or (kind == 3 and rank >= thr):
            return e[0], k, "passed"
    return (es[-1][0] if es else 0), len(es), "exhausted"


def listing(i, cat):
    uc.mem_write(OUT, bytes(0x2000))
    del gate_calls[:]
    ok, n = run(LIST, i, 1, cat, OUT)
    assert ok, (S.st["bad"] or S.st["faults"])[:2]
    return list(r(OUT, "<%dH" % n)) if n else [], len(gate_calls)


cat_of = {}


def category(i):
    if i not in cat_of:
        ok, c = run(CLASSIFY, i)
        assert ok, (S.st["bad"] or S.st["faults"])[:2]
        cat_of[i] = c & 0xFFFFFFFF
    return cat_of[i]


# ---- SG-1 / SG-2 over every shipped row at three story values ----
per = {}
bad = []
for sv in (0, 200, 6000):
    story(sv)
    for i in range(count):
        want_e, want_k, how = expected_gate(i, sv)
        got_e, got_k = gate(row(i))
        if got_e != want_e or got_k != want_k:
            bad.append([sv, i, hex(got_e), hex(want_e), got_k, want_k])
        per.setdefault(sv, {})[i] = how
exhausted_at_0 = sorted(i for i, h in per[0].items() if h == "exhausted")
record("SG2_every_row_gate_matches_model", not bad, mismatches=bad[:5], exhausted_rows_story0_rank1=exhausted_at_0,
       note="all 57 shipped rows at story 0 / 200 / 6000 (clan rank as computed: 1): the gate returns the first passing entry, else "
            "the LAST entry via the exhausted loop, exactly as an independent walk of the bound table predicts")

# SG-1: the listing evaluates the gate once and lists from the chosen entry onward, by pointer
story(200)
s1 = {}
for i in (0, 3, 24, 43):
    want_e, _, _ = expected_gate(i, 200)
    es = entries(i)
    k = [e[0] for e in es].index(want_e)
    want_ids = [x for e in es[k:] for x in e[4] if x != 0xFFFF]
    cats = sorted({category(x) for x in want_ids})
    got, gates = [], []
    for c in cats:
        ids, g = listing(i, c)
        got += ids
        gates.append(g)
    s1[i] = {"from_entry": k, "ids_listed": len(got), "ids_expected": len(want_ids), "same_multiset": sorted(got) == sorted(want_ids),
             "gate_calls_per_listing": sorted(set(gates))}
record("SG1_one_gate_then_pointer_walk", all(v["same_multiset"] and v["gate_calls_per_listing"] == [1] for v in s1.values()), rows=s1,
       note="each listing call enters 002FAD40 once; over every category the listing returns exactly the ids of the chosen entry and "
            "all entries after it (rows 0, 3, 24, 43 at story 200)")

# row 2 (the clan provisioner): rank is never below 1, so its rank-1 line passes on its own gate
del exits[:]
rk_ok, rk = run(THUNK)
rows2 = entries(2)
e2, k2x = gate(row(2))
record("SG6_rank_floor_row2_not_all_gated", rk_ok and rk & 0xFF == 1 and k2x == len(rows2) - 1 and e2 == rows2[-1][0] and rows2[-1][1:4] == (3, 0, 1)
       and 2 not in exhausted_at_0, rank=rk & 0xFF, row2_last_entry=list(rows2[-1][1:4]), row2_exit_index=k2x, row2_entries=len(rows2),
       note="with zero points the rank is 1 (rung 1 is {0, 0, 0} and the fallback is also 1); row 2's last entry is kind 3 at 1, so it "
            "PASSES on its own gate - row 2 is not among the rows that fall through")

# section 10: the operand is sign-extended (003211EC movsx), so a story word >= 0x8000 fails even a threshold-0 gate
rows17 = entries(17)
story(0)
p0 = gate(row(17))
story(0x8000)
p8 = gate(row(17))
story(0)
record("S10_negative_operand_fails_threshold_0", rows17[-1][1:4] == (2, 0, 0) and p0 == (rows17[-1][0], len(rows17) - 1)
       and p8 == (rows17[-1][0], len(rows17)), story0=list(p0[1:]), story8000=list(p8[1:]), entries=len(rows17),
       note="row 17 ends in kind 2 at 0: story 0 passes it on its own gate (index %d); story 0x8000 reads as -32768 and falls through "
            "(index = count) - the same entry is returned either way" % (len(rows17) - 1))

# ---- synthetic sections (fixture memory, encoded relative to the codec base) ----
def enc(a):
    return a                                           # codec base 0: a stored field is the address


def section(at, ladder):
    """ladder: [(kind, operand, threshold, [ids])] -> a section at `at`; returns a row address (row = {name, section})."""
    rowa, sec, ents, lists = at, at + 0x10, at + 0x20, at + 0x100
    w(rowa, "<II", 0x22D, enc(sec))
    w(sec, "<IHHI", 0x164, 8, len(ladder), enc(ents))
    for j, (k, o, t, ids) in enumerate(ladder):
        la = lists + j * 0x40
        w(ents + 8 * j, "<BBHI", k, o, t, enc(la))
        w(la, "<IHHI", 0x264, 2, len(ids), enc(la + 0x10))
        w(la + 0x10, "<%dH" % len(ids), *ids)
    return rowa, ents


# SG-4: kinds 1 and 2 are the same query; kind 2 forces element 0
uc.mem_write(SYN, bytes(0x1000))
story(100, 0)
story(900, 5)
rw, ents = section(SYN, [(1, 5, 500, [0x0001]), (0, 0, 0, [0x0002])])
del query_calls[:]
k1 = gate(rw)[0] == ents
q1 = list(query_calls)
rw, ents = section(SYN, [(2, 5, 500, [0x0001]), (0, 0, 0, [0x0002])])
del query_calls[:]
k2 = gate(rw)[0] == ents + 8
q2 = list(query_calls)
story(0, 5)
record("SG4_kind1_kind2_one_argument", k1 and k2 and q1 == [(3, 0, 5)] and q2 == [(3, 0, 0)], kind1_query=q1, kind2_query=q2,
       note="element 0 = 100, element 5 = 900, threshold 500: kind 1 queries (3, 0, 5) and passes; kind 2 with the same operand byte "
            "queries (3, 0, 0) and fails to the next entry")

# SG-5: an unknown kind is skipped - and whether its ids vanish depends on where the gate stops
story(0)
rw, ents = section(SYN, [(2, 0, 50, [0x0010]), (4, 0, 0, [0x0020]), (0, 0, 0, [0x0030])])
low = gate(rw)[0]
story(60)
high = gate(rw)[0]
story(0)
record("SG5_unknown_kind_skipped", low == ents + 16 and high == ents, below=hex(low - ents), above=hex(high - ents),
       note="[story>=50, kind 4, kind 0]: below 50 the kind-4 line is skipped and the gate stops at the kind-0 line (its ids are not "
            "listed); at 50+ the first line passes and the listing, walking onward by pointer, WOULD include the kind-4 line's ids")

# SG-5b through the listing: patch shipped row 0's section field to the synthetic ladder, list, restore
orig = r(row(0) + 4, "<I")[0]
w(row(0) + 4, "<I", enc(SYN + 0x10))
lists = {}
for sv in (0, 60):
    story(sv)
    lists[sv] = sorted(listing(0, category(0x0010))[0] + (listing(0, category(0x0030))[0] if category(0x0030) != category(0x0010) else []))
w(row(0) + 4, "<I", orig)
story(0)
record("SG5b_unknown_kind_listed_when_above", lists == {0: [0x0030], 60: [0x0010, 0x0020, 0x0030]}, listed=lists,
       note="through the listing: below the gate only the kind-0 line is offered; above it the kind-4 line's ids ARE offered - an "
            "unknown kind drops its line only when the gate stops below it")

# SG-7: the loop bound is re-read every pass
rw, ents = section(SYN, [(2, 0, 50, [0x0010]), (2, 0, 60, [0x0020]), (2, 0, 70, [0x0030])])
sec = SYN + 0x10


def shrink(u, a, n, _):
    if u.reg_read(UC_X86_REG_RIP) == 0x2FAE21:
        w(sec + 6, "<H", 1)
h = uc.hook_add(UC_HOOK_CODE, shrink, begin=0x2FAE21, end=0x2FAE21)
got7 = gate(rw)
uc.hook_del(h)
w(sec + 6, "<H", 3)
full7 = gate(rw)
record("SG7_bound_not_snapshotted", got7 == (ents, 1) and full7 == (ents + 16, 3),
       shrunk_returns=hex(got7[0] - ents), unshrunk_returns=hex(full7[0] - ents),
       note="all three lines fail; with the count cut to 1 after the first pass the gate exits returning line 0, not line 2: the count "
            "at +6 is re-read at the top of every pass")

# SG-2b / SG-3: with the codec base 0 a stored field of 0 resolves to NULL
Z = SYN + 0x800
w(Z, "<II", 0, 0)                                   # row: section field 0 -> count 0
ok0, a0 = run(GATE, Z)
w(Z + 0x10, "<IHHI", 0x164, 8, 2, 0)                # section with 2 entries, data field 0 -> entry pointer 0
w(Z, "<II", 0, Z + 0x10)
ok3, _ = run(GATE, Z)
fault3 = (S.st["faults"] or [""])[0]
zero_data = [i for i in range(count) if (lambda s: r(s + 6, "<H")[0] and not r(s + 8, "<I")[0])(res(r(row(i) + 4, "<I")[0]))]
record("SG2b_SG3_null_section_and_null_data", ok0 and a0 == 0 and not ok3 and fault3 == "00000000" and not zero_data,
       empty_section_returns=hex(a0), unresolvable_data_faults_reading=fault3, shipped_sections_with_entries_and_null_data=zero_data,
       note="a section field of 0 gives count 0 and the gate returns NULL; a section with entries and a data field of 0 takes 002FADC3 "
            "and faults on the next read; no shipped section has entries and a null data field")

json.dump({"ok": allok, "battle_pack_sha256": PACK_SHA, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
