"""S-29 (OPUS, 2026-09-26): CONTRACT-inventory-class-storage section 4 executed with no stub over the SHIPPED binding.

S-29's runtime cell: 'CONTRACT-inventory-class-storage's mutate cap/handler-ratio invariants rest on EXP-064's stubbed path' (EXP-064
stubs 003008A0 itself). Section 4:
  P1  'The class must be <= 14'                               (00309F51, 00309446)
  P2  'the index must be < +0x3C, tested against count - 1 as a signed compare (00309F80-00309F82), so a class with itemCount == 0
      rejects every id'
  P3  'the storage pointers must have been bound. All of +0x08, +0x20 and +0x30 are NULL in the image ... and every handler
      null-tests before dereferencing'
  I   'the handler and the +0x10 : +0x3C ratio must agree ... nothing enforces their consistency'
  Q   'Postcondition of a mutate: the stored count is at most 99'

World: block 355's world.py (s29-opus-replay-inventory-rebase, imported from there), its real initialisers built; the descriptor table
01EEBCC0 is the image's own .data. NO APPLICATION STUB, no stop boundary. The allowed set grows by the static closures of 003008A0,
00309F30 and 0030B6A0, plus the four storage handlers the descriptors dispatch to
(002FD150 / 002FD420 through +0x48, 002FD8D0 / 002FD970 through +0x50 - indirect, so not in the static closure) and theirs.
  - P3 runs FIRST, in the unbound image state: every storage class x every query kind (00309F30) and every channel/mode (003008A0).
  - The storage is then bound by the shipped rebase 0030B6A0 over a zeroed 0x7410-byte block (as the game binds it), and the rest
    runs over that binding. Values are planted into the bound arrays only where a case needs a starting count.
  - One disclosed perturbation, the CONTROL for I: class 3's +0x48/+0x50 are swapped to the packed pair for one call and restored.
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes result.json.
"""
import importlib.util
import json
import os
import struct
import sys

from unicorn import UC_HOOK_MEM_WRITE

HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.join(HERE, "..", "s29-opus-replay-inventory-rebase")
sys.path.insert(0, WD)
spec = importlib.util.spec_from_file_location("world355", os.path.join(WD, "world.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
FX = json.load(open(os.path.join(WD, "world.json")))
IDOP, FAMD, REBASE, TABLE = 0x3008A0, 0x309F30, 0x30B6A0, 0x1EEBCC0
HANDLERS = (0x2FD150, 0x2FD420, 0x2FD8D0, 0x2FD970)      # reached through the descriptor's +0x48 / +0x50 (indirect: not in edges.tsv)
W.ALLOWED |= {0x16D6A0} | W.closure(IDOP) | W.closure(FAMD) | W.closure(REBASE) | set(HANDLERS)
for h_ in HANDLERS:
    W.ALLOWED |= W.closure(h_)
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
BLOCK, SIZE = 0x76280000, 0x7410
M32 = 0xFFFFFFFF
writes = []


def mw(u, acc, a, n, v, _):
    if not (W.STACK <= a < W.STACK + W.STACK_SZ):
        writes.append((a, n))


uc.hook_add(UC_HOOK_MEM_WRITE, mw)


def r(a, f):
    return struct.unpack(f, bytes(uc.mem_read(a, struct.calcsize(f))))[0]


def w(a, f, v):
    uc.mem_write(a, struct.pack(f, v))


def call(fn, *regs, stack=()):
    writes.clear()
    regs = list(regs) + [0] * (4 - len(regs))
    ok = S.call(fn, regs[0], regs[1], regs[2], regs[3], stack=stack)
    return ok, uc.reg_read(__import__("unicorn").x86_const.UC_X86_REG_RAX) & M32, list(writes), list(S.st["faults"]), list(S.st["bad"])


def desc(c):
    b = TABLE + c * 0x58
    return {"p08": r(b + 8, "<Q"), "n10": r(b + 0x10, "<I"), "p20": r(b + 0x20, "<Q"), "p30": r(b + 0x30, "<Q"),
            "cnt": r(b + 0x3C, "<I"), "p48": r(b + 0x48, "<Q"), "p50": r(b + 0x50, "<Q")}


PACKED, BITSET, EMPTY = [0, 1, 2], [3, 4, 6, 8, 12], [5, 7, 11]
STORAGE = PACKED + BITSET
cases, detail = {}, {}

# ---- P3: the unbound image state ----
d0 = {c: desc(c) for c in range(15)}
unbound = all(d0[c]["p08"] == 0 and d0[c]["p20"] == 0 and d0[c]["p30"] == 0 for c in range(15))
p3 = []
for c in STORAGE:
    for k in range(5):
        ok, ret, wr, f, bad = call(FAMD, (c << 12) | 0, k)
        p3.append({"class": c, "entry": "00309F30", "kind": k, "ok": ok, "ret": ret, "writes": len(wr), "faults": f, "bad": bad})
    for r9 in range(4):
        for r8 in (0, 1):
            ok, ret, wr, f, bad = call(IDOP, (c << 12) | 0, 1, r8, r9, stack=(0,))
            p3.append({"class": c, "entry": "003008A0", "r8": r8, "r9": r9, "ok": ok, "ret": ret,
                       "writes": ["%X" % a for a, n in wr], "faults": f, "bad": bad})
detail["P3_unbound"] = p3
cases["P3_image_pointers_null_for_all_15_classes"] = unbound
cases["P3_every_query_and_mutate_returns_without_fault_while_unbound"] = all(x["ok"] and not x["faults"] for x in p3)
cases["P3_no_store_outside_the_image_while_unbound"] = all(all(int(a, 16) < 0x3000000 for a in x["writes"]) for x in p3 if x["entry"] == "003008A0")

# ---- bind: the shipped rebase ----
uc.mem_write(BLOCK, bytes(SIZE))
okb, _, _, fb, _ = call(REBASE, BLOCK)
d = {c: desc(c) for c in range(15)}
detail["bound"] = {c: {k: ("%X" % v if k.startswith("p") else v) for k, v in d[c].items()} for c in range(15)}
cases["bind_by_shipped_rebase_returns"] = okb and all(d[c]["p08"] for c in STORAGE)


def region(c):
    """the storage the descriptor's own counts allocate: +0x08 is +0x10 uint16 elements; +0x20 is a count byte per id (packed) or a
    bit per id (bitset); +0x30 a bit per id (bitset kind 4)"""
    x = d[c]
    out = [(x["p08"], x["p08"] + 2 * x["n10"])]
    if x["p20"]:
        out.append((x["p20"], x["p20"] + (x["cnt"] if c in PACKED else (x["cnt"] + 7) // 8)))
    if x["p30"]:
        out.append((x["p30"], x["p30"] + (x["cnt"] + 7) // 8))
    return out


def inside(a, n, regs):
    return any(lo <= a and a + n <= hi for lo, hi in regs)


# ---- P1: class bound ----
p1 = {}
for idv in (0xF000, 0xF001, 0xFFFF, 0xF1FF):
    p1["%04X_idop" % idv] = call(IDOP, idv, 1, 0, 1, stack=(0,))[1]
    p1["%04X_famd" % idv] = call(FAMD, idv, 1)[1]
p1["C000_idop_valid_nibble"] = call(IDOP, 0xC000, 1, 0, 1, stack=(0,))[1]
detail["P1"] = {k: "%X" % v for k, v in p1.items()}
cases["P1_nibble_15_rejected_by_both_entries"] = all(p1["%04X_idop" % i] == M32 and p1["%04X_famd" % i] == M32 for i in (0xF000, 0xF001, 0xF1FF)) \
    and p1["FFFF_idop"] == M32
cases["P1_nibble_12_accepted"] = p1["C000_idop_valid_nibble"] != M32

# ---- X (not in section 4): the mutate entry also refuses 0x1000 (003008D8-003008E0); the query entry does not ----
uc.mem_write(BLOCK, bytes(SIZE))
w(d[1]["p08"], "<H", 5)                                       # class 1, index 0: owned 5
okx, retx, wrx, _, _ = call(IDOP, 0x1000, 1, 0, 1, stack=(0,))
X = {"idop_1000": retx, "idop_1000_writes_in_block": ["%X" % (a - BLOCK) for a, _ in wrx if BLOCK <= a < BLOCK + SIZE],
     "word_after": r(d[1]["p08"], "<H"), "famd_1000_kind1": call(FAMD, 0x1000, 1)[1], "idop_1001": call(IDOP, 0x1001, 1, 0, 1, stack=(0,))[1]}
detail["X_1000"] = {k: ("%X" % v if isinstance(v, int) else v) for k, v in X.items()}
cases["X_mutate_entry_refuses_0x1000_query_entry_reads_it"] = okx and X["idop_1000"] == M32 and not X["idop_1000_writes_in_block"] \
    and X["word_after"] == 5 and X["famd_1000_kind1"] == 5 and X["idop_1001"] == 1

# ---- P2: signed index bound ----
p2 = {}
for c in STORAGE:
    n = d[c]["cnt"]
    ok_last, ret_last, wr_last, _, _ = call(IDOP, (c << 12) | (n - 1), 1, 0, 1, stack=(0,))
    ok_past, ret_past, wr_past, _, _ = call(IDOP, (c << 12) | n, 1, 0, 1, stack=(0,))
    p2[c] = {"count": n, "last_ret": ret_last, "past_ret": ret_past, "past_writes_in_block": [("%X" % a) for a, _ in wr_past if BLOCK <= a < BLOCK + SIZE],
             "famd_past": call(FAMD, (c << 12) | n, 1)[1]}
for c in EMPTY:
    p2[c] = {"count": d[c]["cnt"], "id0_idop": call(IDOP, (c << 12) | 0, 1, 0, 1, stack=(0,))[1], "id0_famd": call(FAMD, (c << 12) | 0, 1)[1]}
detail["P2"] = p2
cases["P2_last_id_accepted_first_past_rejected_no_store"] = all(p2[c]["last_ret"] != M32 and p2[c]["past_ret"] == M32 and not p2[c]["past_writes_in_block"]
                                                             and p2[c]["famd_past"] == 0 for c in STORAGE)
cases["P2_count_0_classes_reject_every_id"] = all(p2[c]["count"] == 0 and p2[c]["id0_idop"] == M32 and p2[c]["id0_famd"] == 0 for c in EMPTY)

# ---- Q: the stored count is at most 99 ----
q = []
for c in PACKED:
    idx = 7
    wa = d[c]["p08"] + 2 * idx
    ba = d[c]["p20"] + idx if d[c]["p20"] else None
    for r9 in range(4):
        for r8 in (0, 1):
            for start, delta in ((0, 100), (0, 200), (98, 1), (99, 1), (50, 49), (0, 1023), (0, 0x7FFF)):
                w(wa, "<H", start)
                if ba:
                    w(ba, "<B", start)
                ok, ret, wr, f, _ = call(IDOP, (c << 12) | idx, delta, r8, r9, stack=(0,))
                wd, bd = r(wa, "<H"), (r(ba, "<B") if ba else None)
                stored_word = any(a == wa for a, _ in wr)
                stored_byte = ba is not None and any(a == ba for a, _ in wr)
                q.append({"class": c, "r9": r9, "r8": r8, "start": start, "delta": delta, "ok": ok, "ret": ret, "word": wd, "owned": wd & 0x3FF,
                          "reserved": wd >> 10, "byte": bd, "stored_word": stored_word, "stored_byte": stored_byte, "faults": f})
detail["Q"] = q
cases["Q_every_mutate_returns"] = all(x["ok"] for x in q)
cases["Q_stored_owned_and_reserved_and_byte_at_most_99"] = all((not x["stored_word"] or (x["owned"] <= 99 and x["reserved"] <= 99))
                                                             and (not x["stored_byte"] or x["byte"] <= 99) for x in q)
cases["Q_the_cap_is_reached"] = any(x["stored_word"] and x["owned"] == 99 for x in q) and any(x["stored_byte"] and x["byte"] == 99 for x in q)

# ---- I: handler and ratio agree - the last id writes its region's last element; the first id its first ----
inv = {}
for c in STORAGE:
    regs = region(c)
    n = d[c]["cnt"]
    res_c = {}
    for tag, idx in (("first", 1 if c == 1 else 0), ("last", n - 1)):     # 0x1000 is refused by the mutate entry (case X)
        uc.mem_write(BLOCK, bytes(SIZE))
        ok, ret, wr, f, _ = call(IDOP, (c << 12) | idx, 1, 1, 1, stack=(0,))
        blk = [(a, m) for a, m in wr if BLOCK <= a < BLOCK + SIZE]
        elem = (idx if c in PACKED else idx >> 4)
        res_c[tag] = {"ok": ok, "ret": ret, "writes": ["%X+%d" % (a - BLOCK, m) for a, m in blk],
                      "all_inside_own_region": bool(blk) and all(inside(a, m, regs) for a, m in blk),
                      "hits_element": any(a == d[c]["p08"] + 2 * elem for a, _ in blk),
                      "element": elem, "n10": d[c]["n10"],
                      "readback": call(0x309F30, (c << 12) | idx, 1 if c in PACKED else 0)[1]}
    inv[c] = res_c
detail["I"] = inv
cases["I_every_storage_class_first_and_last_id_write_inside_own_region"] = all(inv[c][t]["ok"] and inv[c][t]["all_inside_own_region"] for c in STORAGE for t in ("first", "last"))
cases["I_last_id_writes_the_last_element"] = all(inv[c]["last"]["hits_element"] and inv[c]["last"]["element"] == d[c]["n10"] - 1 for c in STORAGE)

# ---- control: nothing enforces the agreement ----
b3 = TABLE + 3 * 0x58
s48, s50 = r(b3 + 0x48, "<Q"), r(b3 + 0x50, "<Q")
w(b3 + 0x48, "<Q", 0x2FD150)
w(b3 + 0x50, "<Q", 0x2FD8D0)
uc.mem_write(BLOCK, bytes(SIZE))
okc, retc, wrc, fc, _ = call(IDOP, (3 << 12) | 80, 1, 1, 1, stack=(0,))
w(b3 + 0x48, "<Q", s48)
w(b3 + 0x50, "<Q", s50)
blkc = [(a, m) for a, m in wrc if BLOCK <= a < BLOCK + SIZE]
ctl = {"ok": okc, "ret": retc, "writes": ["%X+%d" % (a - BLOCK, m) for a, m in blkc], "own_region": ["%X-%X" % (lo - BLOCK, hi - BLOCK) for lo, hi in region(3)],
       "outside_own_region": [("%X" % (a - BLOCK)) for a, m in blkc if not inside(a, m, region(3))],
       "lands_in_class": sorted({c for a, m in blkc for c in STORAGE if inside(a, m, region(c))})}
detail["control_class3_packed_handler"] = ctl
cases["control_mismatched_handler_writes_outside_its_region_unchecked"] = okc and retc != M32 and bool(ctl["outside_own_region"])
cases["control_restored"] = (r(b3 + 0x48, "<Q"), r(b3 + 0x50, "<Q")) == (0x2FD420, 0x2FD970)

res = {"ok": all(cases.values()), "live_game": False, "cases": cases, "detail": detail, "allowed_functions": len(W.ALLOWED)}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("control:", json.dumps(ctl))
print("ALL PASS" if res["ok"] else "FAILED")
