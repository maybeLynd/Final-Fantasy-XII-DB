"""gr9_subgroup_check.py - GR-9: what enters the enemy order subgroups no switch inside the set reaches? (OPUS, 2026-09-30)
Static, the certified image (kit retool.py, regval.py).

K1  the battle unit's subgroup byte +0x6B5 has three byte writers in the image: 002FE0BB (the subgroup command arm of the
    direct-state order dispatcher 002FDDA0), 002FE09F (0, the variant switch) and 00236BA3 (0, BattleUnit_ResetStateForReuse).
    Every other access whose width covers +0x6B5 is a wider access at +0x6B0 / +0x6B4 on another base (listed).
K2  002FE0BB stores dl = (the unit's committed order id +0x714, 002FDDB0) - 0x16 in its low byte: order 0x4116 + k enters
    subgroup k.
K3  +0x714 is written with an id only by BattleUnit_CommitAction (0030F760 @0030F806); BattleUnit_CancelAndResetCurrentAction
    (0031071B) and the reset (00236B55) store 0xFFFF.
K4  CommitAction has five call sites (FE-7 R3's list): 00305B2F (the issued command word +0xBA0), 00305C9B (the static
    0x4021 record 01EEC298), 00305DF4 (the evaluated record of the unit's own order set), 0030FA5C (+0x714 again, a combo)
    and 003130DC (0x96).
K5  +0xBA0 is written only by BattleUnit_IssueCommand (00311CF0 @00311D7A) with its r9w; its callers pass 0x9C / 0x9D /
    0x113 or a battle-menu word (BattleMenu_UpdateCommandSelectionAndDispatch 002778C0 @0027868A / @0027875A, 0027C3D0
    @0027C591) through the focus-handle issuers 00311B20 / 00311CD0, and 003138D0 passes 0x113.
So the only run-time (non-authored) order id that can reach +0x714 comes from the player's battle menu for the focus
units. An enemy's subgroup is entered only by a switch record of its own current set, and left to 0 by a variant switch
or a reset.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
MEM = re.compile(r"(byte|word|dword|qword|xmmword) ptr \[(\w+)(?: \+ \w+\*\d)? \+ (0x[0-9a-f]+)\]")


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def covering(lo, hi, writes_only):
    out = []
    for f in sorted(SZ):
        try:
            ins = list(R.md.disasm(R.at(f, SZ[f]), f))
        except Exception:
            continue
        for i in ins:
            text = i.op_str.split(",")[0] if writes_only else i.op_str
            m = MEM.search(text)
            if not m or m.group(2) in ("rip", "rsp", "rbp") or (writes_only and i.mnemonic in ("cmp", "test", "bt")):
                continue
            d, w = int(m.group(3), 16), W[m.group(1)]
            if d <= hi and lo < d + w:
                out.append((f, i.address, m.group(1), "%s %s" % (i.mnemonic, i.op_str)))
    return out


# K1
cov = covering(0x6B5, 0x6B5, False)
bytew = sorted(a for f, a, w, t in cov if w == "byte" and t.startswith("mov byte ptr"))
others = [(f, a, t) for f, a, w, t in cov if w != "byte"]
ok = bytew == [0x00236BA3, 0x002FE09F, 0x002FE0BB] and txt(0x002FE09F) == "mov byte ptr [rbx + 0x6b5], 0" \
    and V.value_at(0x00236A60, 0x00236BA3, "rax", 0) == {("C", 0)} \
    and all(w != "byte" for f, a, w, t in cov if a not in bytew and a != 0x00305C34)
# the one battle-adjacent wide store, 002E03C4, is on a global pointer table, not a unit
ok &= V.value_at(0x002DF9A0, 0x002E03C4, "rax", 1) == {("M", "002E03BD qword ptr [rip + 0x1e7ec74]")}
check("K1", ok, "+0x6B5 byte writers %s; reader 00305C34; wider accesses on other bases: %s"
      % (["%08X" % a for a in bytew], ["%08X" % a for _, a, _ in others]))
# K2
check("K2", txt(0x002FDDB0) == "movzx edx, word ptr [rcx + 0x714]" and txt(0x002FE0B8) == "sub dl, 0x16"
      and txt(0x002FE0BB) == "mov byte ptr [rbx + 0x6b5], dl",
      "subgroup = low byte of the committed order id - 0x16 (order 0x4116 + k -> subgroup k)")
# K3
w714 = [(f, a, t) for f, a, w, t in covering(0x714, 0x715, True)]
battle = [(f, a) for f, a, t in w714 if 0x00230000 <= f < 0x00330000]
ok = sorted(battle) == [(0x00236A60, 0x00236B55), (0x0030F760, 0x0030F806), (0x003105D0, 0x0031071B)] \
    and V.value_at(0x003105D0, 0x0031071B, "rax", 2) == {("C", 0xFFFF)} and V.value_at(0x00236A60, 0x00236B55, "rbx", 0) == {("C", 0xFFFF)} \
    and txt(0x0030F806) == "mov word ptr [rbx + 0x714], di"
check("K3", ok, "battle-layer +0x714 writers %s (0xFFFF except CommitAction); outside the battle layer: %s"
      % (["%08X" % a for _, a in sorted(battle)], sorted({"%08X" % f for f, a, t in w714 if (f, a) not in battle})))
# K4
ca = sorted(set(c["calls"].get(0x0030F760, ())))
check("K4", ca == [(0x00305AB0, 0x00305B2F), (0x00305AB0, 0x00305C9B), (0x00305CC0, 0x00305DF4), (0x0030FA00, 0x0030FA5C),
                   (0x00312FA0, 0x003130DC)] and int.from_bytes(R.at(0x01EEC298, 2), "little") == 0x4021,
      "CommitAction call sites %s; the static record 01EEC298 holds 0x4021" % ["%08X" % s for _, s in ca])
# K5
ba_ = [(f, a) for f, a, w, t in covering(0xBA0, 0xBA1, True) if 0x00230000 <= f < 0x00330000]
ic = sorted(set(c["calls"].get(0x00311CF0, ())))
ids = {s: V.value_at(f, s, "r9", 3) for f, s in ic}
menu = {("C", 0x9C), ("C", 0x9D), ("C", 0x113), ("M", "0027868A word ptr [rax]"), ("M", "0027875A word ptr [rsi]"),
        ("M", "0027C591 word ptr [rdx + 0x50]")}
ok = ba_ == [(0x00311CF0, 0x00311D7A)] and txt(0x00311D07) == "movzx esi, r9w" and txt(0x00311D7A) == "mov word ptr [rbx + 0xba0], si" \
    and ic == [(0x00311B20, 0x00311C7B), (0x00311B20, 0x00311CA6), (0x003138D0, 0x0031395D)] \
    and ids[0x00311C7B] == menu and ids[0x00311CA6] == menu and ids[0x0031395D] == {("C", 0x113)} \
    and sorted({f for f, _ in c["calls"].get(0x00311B20, ())}) == [0x002778C0, 0x00311CD0] \
    and sorted({f for f, _ in c["calls"].get(0x00311CD0, ())}) == [0x002778C0, 0x0027AA70, 0x0027C3D0]
check("K5", ok, "+0xBA0 written only at 00311D7A; issued ids: menu path %s; 003138D0: 0x113"
      % sorted(str(x) for x in ids[0x00311C7B]))
print("FAILS %d" % fails)
