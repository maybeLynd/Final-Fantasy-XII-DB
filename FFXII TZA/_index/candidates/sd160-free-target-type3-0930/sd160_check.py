"""sd160_check.py - SD-160: which units carry free-target type 3, the value the bestiary defeat tally skips (OPUS,
2026-09-30). F1-F3 are static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py; C1-C3 check
the shipped-script census written by sd160_census.py (sd160-census.tsv, sd160-type3-scripts.tsv beside this file).
"""
import collections, csv, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# F1 - the skip: for a unit whose record is kind 1 (+0x698 -> +5 == 1), 003171C0 always calls 00253770(4, 1), then
#      calls the bestiary tally 00253750 only when the actor's free-target type (00263C20 = actor +0x0E & 0xF) is not 3
#      and the unit's definition +0x52 is not 0xFFFF
check("F1", txt(0x003171E7) == "call 0x253770" and txt(0x00317202) == "call 0x263c20" and txt(0x00317207) == "cmp eax, 3"
      and txt(0x0031720A) == "je 0x317224" and txt(0x00317217) == "cmp ecx, 0xffff" and txt(0x0031721F) == "call 0x253750",
      "type 3 (or definition +0x52 == 0xFFFF) skips the tally call 00253750")
# F2 - writer 1: setfreetargettype (0x0265, handler 003528C0) pops an int and stores its low nibble into the executing
#      actor's +0x0E through 00269FE0 - the value 3 is stored as 3
check("F2", txt(0x003528CC) == "call 0x267e10" and txt(0x003528D3) == "mov rcx, rbx" and txt(0x003528D6) == "call 0x269fe0"
      and txt(0x0026A033) == "and byte ptr [rbx + 0xe], 0xf0" and txt(0x0026A037) == "and dil, 0xf"
      and txt(0x0026A03B) == "or byte ptr [rbx + 0xe], dil",
      "setfreetargettype(v) -> actor +0x0E low nibble = v")
# F3 - writer 2: btlAtelSetUnitType (0x3005, handler 00510340) pops an int and tail-calls 002396B0(actor, v), which stores
#      table[v] (v <= 3, else 0) from 01E09EE8 = {1, 5, 3, 4} into the actor's unit +0x58 - the mode the refresh copies
#      into the nibble (AL-3) - so argument 2, not 3, is the one that gives type 3
tab = struct.unpack("<4I", R.at(0x01E09EE8, 16))
check("F3", txt(0x0051035B) == "jmp 0x2396b0" and txt(0x002396B9) == "call 0x31b760" and txt(0x002396C3) == "cmp ebx, 3"
      and txt(0x002396C8) == "lea rdx, [rip + 0x1bd0819]" and 0x002396CF + 0x1BD0819 == 0x01E09EE8 and tab == (1, 5, 3, 4)
      and txt(0x002396D6) == "mov byte ptr [rax + 0x58], dl",
      "btlAtelSetUnitType(v) -> unit +0x58 = {1, 5, 3, 4}[v]; type 3 <- argument 2")
# C1 - the census: every call of the two verbs in every shipped .ebp has a pushed-constant argument; the totals by value
out = open(os.path.join(HERE, "sd160_census.out"), encoding="utf-8").read()
check("C1", "| rows: 63432" in out and "sites whose argument is not a pushed constant: 0" in out
      and "297  ('btlAtelSetUnitType', 'PUSHII:2')" in out and "315  ('setfreetargettype', 'PUSHII:3')" in out
      and "59814  ('btlAtelSetUnitType', 'PUSHII:0')" in out and "2340  ('setfreetargettype', 'PUSHII:4')" in out,
      "63,432 sites, all constant; btlAtelSetUnitType(2) 297, setfreetargettype(3) 315 (sd160_census.out)")
rows = list(csv.DictReader(open(os.path.join(HERE, "sd160-census.tsv"), encoding="utf-8"), delimiter="\t"))
# C2 - the type-3 sites are 68 per language: every plan_master language copy carries the same (script, verb) sites
T3 = {("setfreetargettype", "PUSHII:3"), ("btlAtelSetUnitType", "PUSHII:2")}
z = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    if (r["verb"], r["args_push_order"]) in T3:
        p = r["file"].split("/")
        z["/".join(p[:2] + p[3:])][p[2]].append((r["script"], r["verb"]))
langs = set(l for v in z.values() for l in v)
agree = all(len(set(frozenset(collections.Counter(x).items()) for x in v.values())) == 1 and set(v) == langs for v in z.values())
per = sum(len(next(iter(v.values()))) for v in z.values())
check("C2", all(r["file"].split("/")[1] == "plan_master" for r in rows) and len(langs) == 9 and agree and per == 68
      and len(z) == 29 and per * 9 == sum(len(x) for v in z.values() for x in v.values()) == 612,
      "612 sites = 68 x 9 languages, identical per language, in 29 zone files")
# C3 - who: the 68 sites are 68 distinct (zone, script) pairs (sd160-type3-scripts.tsv): THIRD_* third-party allies,
#      npc_battle_00, event_garif_00, the Nalbina Dalan soldiers and BASH, four Trial Mode ex_trial scripts
#      (btlAtelSetUnitType(2)), and the five Giruvegan disp_tama scripts in seven rbl_ zones (setfreetargettype(3))
lst = list(csv.DictReader(open(os.path.join(HERE, "sd160-type3-scripts.tsv"), encoding="utf-8"), delimiter="\t"))
by = collections.Counter(r["verb"] for r in lst)
fam = lambda s: "THIRD" if s.startswith("THIRD_") else s.rstrip("0123456789_ABC")
fams = collections.Counter(fam(r["script"]) for r in lst)
check("C3", len(lst) == 68 == len(set((r["zone_file"], r["script"]) for r in lst)) and by == {"btlAtelSetUnitType": 33, "setfreetargettype": 35}
      and fams == {"THIRD": 10, "npc_battle": 6, "event_garif": 1, "DAL_SOLDIER": 9, "BASH": 3, "ex_trial": 4, "disp_tama": 35}
      and all(r["script"].startswith("disp_tama") and r["zone_file"].startswith("rbl_") for r in lst if r["verb"] == "setfreetargettype"),
      "33 unit-type sites (THIRD_* 10, npc_battle 6, event_garif 1, DAL_SOLDIER 9, BASH 3, ex_trial 4) + 35 disp_tama sites in rbl_")
print("FAILS %d" % fails)
