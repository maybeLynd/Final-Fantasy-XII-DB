"""rc5b_actions.py - RC-5 residue item 2: the authored +0x24 word of every action row 00306BD0 can hand to 00309230, and
the event names those set ids reach (ORACLE, 2026-09-30). Static: shipping image + battle_pack.bin from the VBF.

Code (asserted):
  BattleAction_TryEnterGlobalSpecialSequence 0030CE10 calls 00306BD0(unit, row) only for an action row whose dword
  +0x0C has bit 30 (0030CE93); rows 0xD0..0xF1 are further refused while [022C2160] is 5 or 6 (0030CEC2-0030CEFE).
  00306BD0 loads manager 3 with set id 00309230(unit, row) (00306C4D-00306C56): the 13-entry Esper table by the unit's
  definition row for action row 0x113 (003092C0-003092DB), else the row's u16 +0x24 (003092C5).
Data: the action table is battle_pack.bin's directory word +0x3C (st2e: +4 rows, +8 stride, rows at +0x20); all nine
locale copies are compared. Names: RC-5's kind-8 path table (../rc5-event-slot-routes-0930/rc5_paths.tsv, region 1).
"""
import collections, csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img
FAILS = []


def check(ok, name):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


a = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x0030CE10)}
b = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x00309230)}
c = {x.address: (x.mnemonic, x.op_str) for x in img.fn_ins(0x00306BD0)}
check(a.get(0x0030CE93) == ("test", "dword ptr [rax + 0xc], 0x40000000") and a.get(0x0030CF0D) == ("call", "0x306bd0")
      and a.get(0x0030CEC2) == ("cmp", "eax, 0xd0") and a.get(0x0030CEEB) == ("cmp", "eax, 0xf1"),
      "K1 0030CE10 gates on row +0x0C bit 30; rows 0xD0..0xF1 carry the extra [022C2160] test")
check(b.get(0x003092B4) == ("imul", "ecx, edx, 0x113") and b.get(0x003092C5) == ("movzx", "eax, word ptr [rbx + 0x24]")
      and c.get(0x00306C0A) == ("mov", "ebx, 3") and c.get(0x00306C56) == ("call", "0x32fc30"),
      "K2 00309230 returns the row's u16 +0x24 (row 0x113: the Esper table); 00306BD0 loads manager 3 with it")
names = {}
for r in csv.DictReader(io.open(os.path.join(HERE, "..", "rc5-event-slot-routes-0930", "rc5_paths.tsv"), encoding="utf-8"), delimiter="\t"):
    if r["region_ecx"] == "1" and r["kind"] == "8":
        names[int(r["set_id"])] = (r["stored_name"], r["in_archive"])
tables = {}
for p in [n for n in arc.NAMES if n.lower().endswith("battle_pack.bin")]:
    d = arc.get(p)
    off = struct.unpack_from("<I", d, 0x3C)[0]
    n, st = struct.unpack_from("<II", d, off + 4)
    base = off + 0x20
    tables[p.split("/")[-3]] = [(i, struct.unpack_from("<I", d, base + i * st + 0xC)[0], struct.unpack_from("<H", d, base + i * st + 0x24)[0])
                                for i in range(n)]
same = all(t == tables["us"] for t in tables.values())
check(same and len(tables["us"]) == 543, "K3 the 543-row action table is identical in all %d locale copies" % len(tables))
rows = [(i, f, w) for i, f, w in tables["us"] if f & 0x40000000]
print("\naction rows with +0x0C bit 30 (the special-sequence gate): %d" % len(rows))
by = collections.defaultdict(list)
for i, f, w in rows:
    sid = "Esper table 42..78 (the sum_<x>0002 names)" if i == 0x113 else w
    by[sid].append(i)
flagA = []
for sid, idx in sorted(by.items(), key=lambda kv: str(kv[0])):
    nm = names.get(sid, ("(no kind-8 path)", "")) if isinstance(sid, int) else ("", "")
    cls = ""
    if nm[0].startswith("sum_") and nm[0].endswith("0001"):
        cls = "sets flag A (01F832E8)"
        flagA.append(sid)
    elif nm[0].startswith("spc_"):
        cls = "sets flag B (01F832E9)"
    gate = " (rows 0xD0..0xF1: skipped while [022C2160] is 5 or 6)" if any(0xD0 <= i <= 0xF1 for i in idx) else ""
    print("  set id %-44s rows %-30s %-12s %s%s" % (sid, ",".join(str(i) for i in idx) if len(idx) < 8 else "%d..%d (%d rows)" % (idx[0], idx[-1], len(idx)),
                                                nm[0], cls, gate))
check(sorted(flagA) == list(range(41, 78, 3)), "K4 the 13 sum_<x>0001 set ids 41, 44 .. 77 are exactly the +0x24 words of rows 183, 185 .. 207")
print("\nFAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
