"""S-21 (OPUS, 2026-09-26): the applier's item scalar ResultRecord +0x38 executed into real inventory storage - one of the item is
granted, -1 grants nothing, and only the low word is dispatched (CONTRACT-apply-result-to-target.md section 3: "The item scalar at
+0x38 is absent when its dword equals -1 (the dispatched item ID is the low word)").

Loads block 332's check.py (its cases run first, unchanged). The applier 003112F0 runs whole with its real callees, as in block 332;
the one addition is the inventory storage: the shipped rebase 0030B6A0 binds the class descriptors into the battle-state block
[02EBF190] (as in s29-opus-replay-inventory-storage), so the grant lands in real storage and is read back through the query entry
00309F30. The item site: 0031148D cmp dword [rbx+0x38], -1 / je -> skip; else 003114A8 call 003008A0(movzx word [rbx+0x38],
edx 1, r8 0 = add, r9 1 = owned channel). The display boundary 002B4090 is lifted as in i4_numeric.py (disclosed). No application stub.
The owned count's 0 -> 1 fires the derived index (00325F40 -> 00252E60), whose lists live in the image-backed state block
*(020927C0). Its binders run as shipped, not planted: 00253970's prefix up to 00253997 (00249840, then 002EF640() + 0x8200 stored
at 00253990) and the list initialiser 00253480 (00253240(list, 1) x 12), which 00253970 reaches through 0035C560. The encoded
base [01F83530] keeps its load-time zero (CONTRACT-encoded-id-space-and-class-registry, the 01F83530 residual).
Not executed: the lethal chain - its display reaches the graphics context [01F811F8] before any contract step (lethal_boundary.py).
Evidence class NATIVE-REPLAY (unicorn), live_game false. Writes item38_result.json.
"""
import contextlib
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
cwd = os.getcwd(); os.chdir(HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
os.chdir(cwd)
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP

W, uc, S = C.W, C.uc, C.S
# block 332 stops numeric results at the display 002B4090; a granted item reaches that display after the grant. As in
# i4_numeric.py, the boundary is lifted (disclosed): the hook is neutralised and the display's closure joins ALLOWED.
C.on_display.__code__ = (lambda u, a, n, _: None).__code__
W.ALLOWED |= W.closure(C.DISPLAY) | {C.DISPLAY}
for f in (0x30B6A0, 0x3008A0, 0x309F30, 0x2FD150, 0x2FD8D0, 0x253480):
    W.ALLOWED |= W.closure(f) | {f}
# the derived index (00325F40 -> 00252E60 on the owned count's 0 -> 1) keeps its lists in the image-backed state block
# *(020927C0). Its binders run as shipped: 00253970's prefix (00249840, then 002EF640() + 0x8200 stored at 00253990) up to
# 00253997, then the list initialiser 00253480 (00253240(list, 1) for the twelve lists; reached from 00253970 through 0035C560).
W.ALLOWED |= {0x253970, 0x249840, 0x2EF640}
BIND_STOP = 0x253997
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: u.emu_stop(), begin=BIND_STOP, end=BIND_STOP)
grants = []
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: grants.append(tuple(u.reg_read(x) & 0xFFFFFFFF for x in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))),
            begin=0x3114A8, end=0x3114A8)
uc.ctl_flush_tb()
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]


def owned(item):
    S.call(0x309F30, item, 1)
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def run(item_dword):
    C.reset()
    block = q(0x2EBF190)
    uc.mem_write(block, bytes(0x7410))
    okb = S.call(0x30B6A0, block)
    S.call(0x253970)
    okb = okb and uc.reg_read(UC_X86_REG_RIP) == BIND_STOP and not S.st["faults"] and q(0x20927C0) == 0x2164280 + 0x8200
    okb = okb and S.call(0x253480)
    before = {i: owned(i) for i in (0x0001, 0x0002)}
    C.w(C.REC + 0x38, "<I", item_dword)
    del grants[:]
    ok = C.apply()
    after = {i: owned(i) for i in (0x0001, 0x0002)}
    ib = q(0x20927C0)
    index = {"list0_count": struct.unpack("<I", bytes(uc.mem_read(ib + 0x47B8, 4)))[0],
             "list0_head": "%04X" % struct.unpack("<H", bytes(uc.mem_read(ib + 0x38CC, 2)))[0],
             "flags_3244": "%02X" % uc.mem_read(ib + 0x3244, 1)[0]}
    return {"index": index, "ok": ok, "rebase": okb, "halt": (S.st["bad"] or S.st["faults"])[:2], "grant_calls": ["(%X, %X, %X, %X)" % g for g in grants],
            "owned_before": before, "owned_after": after}


R = {"item_1": run(0x0001), "item_2_high_word_junk": run(0xABCD0002), "absent": run(0xFFFFFFFF), "low_word_FFFF": run(0x0000FFFF)}
cases = {
    "item_scalar_grants_one_of_the_item": R["item_1"]["ok"] and R["item_1"]["grant_calls"] == ["(1, 1, 0, 1)"]
        and R["item_1"]["owned_after"][1] == R["item_1"]["owned_before"][1] + 1,
    "only_the_low_word_is_dispatched": R["item_2_high_word_junk"]["ok"] and R["item_2_high_word_junk"]["grant_calls"] == ["(2, 1, 0, 1)"]
        and R["item_2_high_word_junk"]["owned_after"][2] == R["item_2_high_word_junk"]["owned_before"][2] + 1,
    "dword_minus_1_is_absent_no_grant": R["absent"]["ok"] and R["absent"]["grant_calls"] == []
        and R["absent"]["owned_after"] == R["absent"]["owned_before"],
    "low_word_FFFF_with_zero_high_word_is_not_absent": R["low_word_FFFF"]["ok"] and R["low_word_FFFF"]["grant_calls"] == ["(FFFF, 1, 0, 1)"],
    "storage_bound_by_the_shipped_rebase": all(v["rebase"] for v in R.values()),
    "derived_index_appends_on_0_to_1": R["item_1"]["index"]["list0_count"] == 1 and R["item_1"]["index"]["list0_head"] == "0001"
        and R["item_2_high_word_junk"]["index"]["list0_head"] == "0002",
    "category_flag_bit4_set_by_list0": all(int(R[k]["index"]["flags_3244"], 16) & 0x10 for k in ("item_1", "item_2_high_word_junk")),
    "absent_leaves_the_index_empty": R["absent"]["index"] == {"list0_count": 0, "list0_head": "FFFF", "flags_3244": "00"},
}
res = {"live_game": False, "runs": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "item38_result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print({k: (v["grant_calls"], v["owned_before"], v["owned_after"], v["index"], v["halt"]) for k, v in R.items()})
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
