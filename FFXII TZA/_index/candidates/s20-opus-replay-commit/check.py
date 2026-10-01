"""S-20: CONTRACT-the-moment-an-action-is-committed.md's CM-1..CM-6 executed as shipped code - the commit 0030F760 and the cancel
003105D0 (OPUS, 2026-09-26).

Runs over block 332's world (s21-opus-replay-applier-stub-free/check.py, imported: its cases run first, unchanged): the image, the
IAT traps with memset bridged by name, the shipped battle_pack bindings and the unit pool [0208E688] with two planted units whose
+0x698 are stats records. No application stub. ALLOWED += the static closures of 0030F760 and 003105D0.
Signature, read from the prologue: 0030F760(rcx = unit, rdx = a qword stored at +0x708, r8w = action id, r9d = target id,
[rsp+0x28] = cancel first). The target id resolves through 0031B7E0, which returns null while the leader gate byte [02089340]
bit 0x10 is clear - the world's default, used here as the "target does not resolve" case.
The target buffer at unit +0x778 (0x208 bytes): +0 flag byte (bit 0 preserved by the reset 00316CF0), +4 count, entries at
+8 + 16*i (first qword), 32 at most (the append 00316CD0).
Cases:
 M1  CM-1 / CM-4: action 0x10 (low range), target unresolved: the commit completes; the buffer was reset keeping flag bit 0 and
     then APPENDED a null entry - count 0 -> 1, entry 0 = 0 - not skipped.
 M2  CM-2: accepted = 0 .. 0x21E and 0x4000 .. 0x4166; 0x21F, 0x3FFF and 0x4167 are refused - no command block written.
 M3  CM-3: a high-range id (0x4010) writes the command block and leaves the target buffer untouched (no write into +0x778..).
 M4  CM-5: the block +0x700 (low two bits cleared) / +0x708 = rdx / +0x710 = target / +0x714 = id is copied verbatim to
     +0x718..+0x72F, unconditionally.
 M5  CM-6: the cancel with a null unit returns; with +0x698 = 0 it returns without writing the unit.
Writes result.json next to this file.
"""
import json
import os
import struct
import sys

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "s21-opus-replay-applier-stub-free")))
import check as C                                          # block 332 (its cases run first, unchanged)

W, S, uc, w = C.W, C.S, C.uc, C.w
r = lambda a, fmt: C.r(a, fmt)[0]
COMMIT, CANCEL = 0x30F760, 0x3105D0
W.ALLOWED |= W.closure(COMMIT) | {COMMIT} | W.closure(CANCEL) | {CANCEL}
UNIT = C.POOL                                             # unit 0, +0x698 = the planted stats record
buf_w, unit_w = [], []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: buf_w.append(a - UNIT), begin=UNIT + 0x778, end=UNIT + 0x778 + 0x207)
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: unit_w.append("%08X" % u.reg_read(UC_X86_REG_RIP)), begin=UNIT, end=UNIT + 0xF4F)
uc.ctl_flush_tb()


def setup(stats=True):
    C.reset()
    uc.mem_write(UNIT + 0x700, bytes(0x50))
    w(UNIT + 0x700, "<I", 0xFFFFFFFF)
    uc.mem_write(UNIT + 0x778, bytes(0x208))
    w(UNIT + 0x778, "<BBHI", 0x01, 0x5A, 0x5A5A, 3)             # flag bit 0 set, junk, count 3
    w(UNIT + 0x778 + 8, "<Q", 0x1111)
    w(0x2089340, "<B", 0)                                        # leader gate clear -> targets do not resolve
    if not stats:
        w(UNIT + 0x698, "<Q", 0)


def commit(aid, target=0x00120034, rdx=0xABCDEF, cancel=0):
    del buf_w[:], unit_w[:]
    ok = S.call(COMMIT, UNIT, rdx, aid, target, stack=(cancel,))
    blk = bytes(uc.mem_read(UNIT + 0x700, 0x30))
    return {"ok": ok, "halt": (S.st["bad"] or S.st["faults"])[:2], "id_714": "%X" % struct.unpack_from("<H", blk, 0x14)[0],
            "q708": "%X" % struct.unpack_from("<Q", blk, 8)[0], "d710": "%X" % struct.unpack_from("<I", blk, 0x10)[0],
            "d700": "%X" % struct.unpack_from("<I", blk, 0)[0], "shadow_ok": blk[0x18:0x28] == blk[0:0x10] and blk[0x28:0x30] == blk[0x10:0x18],
            "buf_flag": r(UNIT + 0x778, "<B"), "buf_count": r(UNIT + 0x77C, "<I"), "buf_e0": "%X" % r(UNIT + 0x780, "<Q"),
            "buf_writes": len(buf_w), "unit_writes": len(unit_w)}


res, cases = {}, {}
setup()
m1 = commit(0x10)
cases["M1_unresolved_target_is_not_an_error_and_appends_a_null_entry"] = m1["ok"] and m1["buf_flag"] & 1 == 1 and m1["buf_count"] == 1 \
    and m1["buf_e0"] == "0" and m1["id_714"] == "10"
m2 = {}
for aid in (0, 0x21E, 0x21F, 0x3FFF, 0x4000, 0x4166, 0x4167):
    setup()
    m2["%X" % aid] = commit(aid)
cases["M2_two_disjoint_ranges"] = all(m2[k]["ok"] for k in m2) and all(m2[k]["id_714"] == k and m2[k]["d710"] == "120034" for k in ("0", "21E", "4000", "4166"))     and all(m2[k]["id_714"] == "0" and m2[k]["d710"] == "0" for k in ("21F", "3FFF", "4167"))
setup()
m3 = commit(0x4010)
cases["M3_high_range_never_touches_the_target_buffer"] = m3["ok"] and m3["id_714"] == "4010" and m3["buf_writes"] == 0 and m3["buf_count"] == 3
setup()
m4 = commit(0x20, target=0x12345678, rdx=0x1122334455667788)
cases["M4_block_shadowed_verbatim"] = m4["ok"] and m4["shadow_ok"] and m4["q708"] == "1122334455667788" and m4["d710"] == "12345678" \
    and m4["id_714"] == "20" and int(m4["d700"], 16) & 3 == 0
setup()
del unit_w[:]
ok_null = S.call(CANCEL, 0)
null_halt = (S.st["bad"] or S.st["faults"])[:2]
setup(stats=False)
del unit_w[:]
ok_nostats = S.call(CANCEL, UNIT)
m5 = {"null_unit": [ok_null, null_halt], "no_stats": [ok_nostats, (S.st["bad"] or S.st["faults"])[:2], len(unit_w)]}
cases["M5_cancel_is_a_no_op_without_unit_or_stats"] = ok_null and ok_nostats and m5["no_stats"][2] == 0
res.update(M1=m1, M2=m2, M3=m3, M4=m4, M5=m5)
out = {"ok": all(cases.values()), "cases": cases, **res}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
print(json.dumps({k: (v if k != "M2" else {a: [b["ok"], b["id_714"], b["d710"], b["halt"]] for a, b in v.items()}) for k, v in res.items()})[:1600])
