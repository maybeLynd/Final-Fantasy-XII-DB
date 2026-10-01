"""S-04 I1, I3, I4, I5, I6 (OPUS, 2026-09-26): CONTRACT-encoded-id-space-and-class-registry.md's remaining invariants executed
over block 328's world (check.py, imported: its four cases run first, unchanged - battle_pack bound by shipped code).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No application stub. ALLOWED += the static closures of the fill
0031C5D0, the two wrappers 0035D330 / 0035D380 and the rebase 0030B6A0. memset is an import, bridged by name (world.py), as
N05 recorded. A fill that reaches an unplanted object stops there and is reported per class (not substituted).
Cases:
 I1  the fill 0031C5D0 on a 0x98 record whose DWORD+4 and WORD+6 carry different ids: a memory-read hook on +4..+7 shows which
     lane each class reads first - WORD+6 for 1, 5..11, 13..18, 30, 31; DWORD+4 for 2..4, 19..29, 32; class 12 reads neither
     and returns -2.
 I3  the rebase 0030B6A0 over the fifteen SHIPPED descriptors at 01EEBCC0 with a state above 4 GiB: each non-zero offset
     QWORD writes u32(low32(offset) + low32(state)) (zero-extended, not the full pointer); a zero offset leaves the
     destination as it was; a high-half-only offset (0x1_00000000) still selects the write.
 I4  the same call zeros exactly state+57C8..59C7 and ANDs state+59C8..5A47 with F8 through the FULL 64-bit state pointer
     (sentinels just outside both ranges survive); +0x40 receives the exclusive prefix sum of +0x3C; a second call recomputes
     the same pointers and prefixes and resets the ranges again.
 I5  the direct fill clears only +0x18 at entry: on an early refusal (class 12) every other byte of a 0xCC-filled record
     survives; the wrappers clear the whole 0x98 record on a negative return.
 I6  each wrapper returns its static record (0035D330 -> 022CA520, 0035D380 -> 022CA480); a second call to the same wrapper
     returns the same address with the new result in it; the two wrappers' records are distinct. Measured on ids the shipped
     bindings resolve: class 2 ids 0 / 1 (DWORD wrapper) and class 16 ids B000 / B001 (WORD wrapper).
The I3 / I4 calls rewrite the shipped descriptors; they are put back before I5 / I6.
Writes i1_i6_result.json.
"""
import json
import os
import struct

from unicorn import UC_HOOK_MEM_READ, UC_PROT_ALL
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RIP

import check as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
uc, S, r = C.uc, C.S, C.r
FILL, WDWORD, WWORD, REBASE, DESC = 0x31C5D0, 0x35D330, 0x35D380, 0x30B6A0, 0x1EEBCC0
REC_D, REC_W = 0x22CA520, 0x22CA480
W.ALLOWED |= set().union(*(W.closure(f) | {f} for f in (FILL, WDWORD, WWORD, REBASE)))
REC = 0x76700000
uc.mem_map(REC, 0x1000)
HI = 0x123450000                                          # a state block above 4 GiB
uc.mem_map(HI, 0x10000, UC_PROT_ALL)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


lane = []
uc.hook_add(UC_HOOK_MEM_READ, lambda u, acc, a, n, v, _: lane.append([a - REC, n, "%08X" % u.reg_read(UC_X86_REG_RIP)]),
            begin=REC + 4, end=REC + 7)


def fill(cls, dw=0x00AA0000, wd=0x00BB, pattern=0x00):
    uc.mem_write(REC, bytes([pattern]) * 0x98)
    w(REC, "<I", cls)
    w(REC + 4, "<I", dw)                                  # DWORD+4 ...
    w(REC + 6, "<H", wd)                                  # ... whose upper half is WORD+6
    del lane[:]
    ok = S.call(FILL, REC)
    return {"returned": ok, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "stopped_at": (S.st["bad"] or S.st["faults"])[:2],
            "first_lane_read": lane[0] if lane else None, "lane_reads": len(lane)}


# ---- I1 ----
WORD_CLASSES = {1} | set(range(5, 12)) | set(range(13, 19)) | {30, 31}
DWORD_CLASSES = {2, 3, 4} | set(range(19, 30)) | {32}
i1 = {c: fill(c) for c in range(1, 33)}
lane_of = lambda x: None if not x["first_lane_read"] else ("WORD+6" if x["first_lane_read"][:2] == [6, 2] else
                                                           "DWORD+4" if x["first_lane_read"][:2] == [4, 4] else str(x["first_lane_read"]))
i1_ok = all(lane_of(i1[c]) == "WORD+6" for c in WORD_CLASSES) and all(lane_of(i1[c]) == "DWORD+4" for c in DWORD_CLASSES) \
    and i1[12]["returned"] and i1[12]["ret"] == 0xFFFFFFFE and i1[12]["lane_reads"] == 0

# ---- I3 / I4 ----
desc0 = bytes(uc.mem_read(DESC, 15 * 0x58))
state_lo = HI & 0xFFFFFFFF


def rebase(variant):
    uc.mem_write(DESC, desc0)
    if variant == "synthetic":
        w(DESC + 0x00, "<Q", 0x100000000)                 # descriptor 0: high-half-only offset in slot +0x00
        w(DESC + 0x08, "<Q", 0xDEAD)
        w(DESC + 0x18, "<QQ", 0, 0xBEEF)                  # zero offset in slot +0x18: its destination must survive
        w(DESC + 0x28, "<Q", 0xFFFFFFF0)                  # a low half that wraps when added
    uc.mem_write(HI, b"\x5A" * 0x6000)
    ok = S.call(REBASE, HI)
    d = [struct.unpack_from("<QQQQQQQIII", bytes(uc.mem_read(DESC + 0x58 * k, 0x4C))) for k in range(15)]
    region = bytes(uc.mem_read(HI + 0x57C0, 0x5A50 - 0x57C0))
    return ok, d, region


ok3, d3, reg3 = rebase("shipped")
ok3b, d3b, reg3b = rebase("shipped")                     # repetition
oks, ds, regs = rebase("synthetic")


def expect_ptr(off, dst_before):
    return dst_before if off == 0 else (((off & 0xFFFFFFFF) + state_lo) & 0xFFFFFFFF)


src = [struct.unpack_from("<QQQQQQQIII", desc0, 0x58 * k) for k in range(15)]
ship_ptr_ok = all(d3[k][1] == expect_ptr(src[k][0], src[k][1]) and d3[k][4] == expect_ptr(src[k][3], src[k][4])
                  and d3[k][6] == expect_ptr(src[k][5], src[k][6]) for k in range(15))
prefix = [sum(src[j][8] for j in range(k)) & 0xFFFFFFFF for k in range(15)]
prefix_ok = [d3[k][9] for k in range(15)] == prefix
syn_ok = ds[0][1] == state_lo and ds[0][4] == 0xBEEF and ds[0][6] == ((0xFFFFFFF0 + state_lo) & 0xFFFFFFFF)
high_halves_shipped_zero = all(src[k][0] >> 32 == 0 and src[k][3] >> 32 == 0 and src[k][5] >> 32 == 0 for k in range(15))
i3_ok = ok3 and ship_ptr_ok and oks and syn_ok


def ranges_ok(reg):
    base = 0x57C0
    before = reg[:0x57C8 - base]
    zero = reg[0x57C8 - base:0x59C8 - base]
    anded = reg[0x59C8 - base:0x5A48 - base]
    after = reg[0x5A48 - base:]
    return before == b"\x5A" * len(before) and zero == bytes(0x200) and anded == bytes([0x5A & 0xF8]) * 0x80 and after == b"\x5A" * len(after)


i4_ok = ranges_ok(reg3) and ranges_ok(reg3b) and prefix_ok and d3 == d3b
uc.mem_write(DESC, desc0)                                 # the descriptors go back to the world's own values

# ---- I5 ----
refused = fill(12, pattern=0xCC)
rec_after = bytes(uc.mem_read(REC, 0x98))
direct_only_18 = rec_after[0x18:0x20] == bytes(8) and all(rec_after[i] == 0xCC for i in range(0x98) if not (0 <= i < 8 or 0x18 <= i < 0x20))
wrap = {}
for nm, fn, rec, arg in (("dword_wrapper_class12", WDWORD, REC_D, 5), ("word_wrapper_class12", WWORD, REC_W, 5)):
    uc.mem_write(rec, b"\xCC" * 0x98)
    ok = S.call(fn, 12, arg)
    wrap[nm] = {"returned": ok, "stopped_at": (S.st["bad"] or S.st["faults"])[:2], "rax": "%X" % uc.reg_read(UC_X86_REG_RAX),
                "record_all_zero": bytes(uc.mem_read(rec, 0x98)) == bytes(0x98)}
i5_ok = refused["returned"] and refused["ret"] == 0xFFFFFFFE and direct_only_18 and all(v["record_all_zero"] for v in wrap.values())

# ---- I6 ----
al = {}
for nm, fn, rec, a1, a2 in (("dword", WDWORD, REC_D, (2, 0), (2, 1)), ("word", WWORD, REC_W, (16, 0xB000), (16, 0xB001))):
    ok1 = S.call(fn, *a1)
    p1 = uc.reg_read(UC_X86_REG_RAX)
    v1 = bytes(uc.mem_read(p1, 8)).hex()
    ok2 = S.call(fn, *a2)
    p2 = uc.reg_read(UC_X86_REG_RAX)
    v2 = bytes(uc.mem_read(p1, 8)).hex()
    al[nm] = {"returned": [ok1, ok2], "first": "%X" % p1, "second": "%X" % p2, "record_head_after_first": v1, "same_address_after_second": v2}
i6_ok = all(al[k]["returned"] == [True, True] for k in al) and al["dword"]["first"] == al["dword"]["second"] == "%X" % REC_D and al["word"]["first"] == al["word"]["second"] == "%X" % REC_W \
    and REC_D != REC_W and all(al[k]["record_head_after_first"] != al[k]["same_address_after_second"] for k in al)

cases = {"I1_tag_selects_the_input_lane_class12_reads_neither": i1_ok, "I3_rebase_stores_u32_sums_zero_keeps_high_half_selects": i3_ok,
         "I4_rebase_resets_state_through_the_full_pointer_and_repeats": i4_ok, "I5_direct_clears_only_18_wrappers_clear_all": i5_ok,
         "I6_wrappers_return_static_aliased_records": i6_ok}
res = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(W.ALLOWED),
       "i1": {str(c): dict(v, lane=lane_of(v)) for c, v in i1.items()},
       "i3": {"state": "%X" % HI, "shipped_high_halves_zero": high_halves_shipped_zero, "shipped_pointers_ok": ship_ptr_ok,
              "synthetic_desc0": ["%X" % x for x in ds[0][:7]], "prefix": prefix, "prefix_ok": prefix_ok},
       "i5": {"direct_class12": refused, "direct_only_18_cleared": direct_only_18, "wrappers": wrap}, "i6": al}
json.dump(res, open(os.path.join(HERE, "i1_i6_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-62s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
for c in range(1, 33):
    x = i1[c]
    print(c, lane_of(x), x["returned"], "%X" % x["ret"], x["stopped_at"])
print(json.dumps(res["i3"]), json.dumps(res["i5"]), json.dumps(al))
