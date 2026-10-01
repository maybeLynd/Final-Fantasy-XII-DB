# rc6_codes.py - RC-6: why console-table entries 670 ('rbl0102') and 1003 ('gil0301') name a different map than
# map_ref.bin's own pack for their field (rbl0121.mpk, gil0303.mpk). Authored-data facts, from the shipped archive and the
# committed map_ref census (03-World-Area-Field/Map-Pack/members/map-ref-field-packs.tsv, column 3 = own pack).
# Checks:
#  C1 which archive entries carry each code;
#  C2 whether a map_ctrl pack and a jsondata/maps json exist for each code;
#  C3 the map-code strings embedded in gil0303.mpk (does it carry gil0301's codes?);
#  C4 in the census, how many fields own each pack, and the own packs of fields 1000..1007 and 668..672.
# Control: the census row for field 1003 must name gil0303.mpk and field 670 rbl0121.mpk (SWE2-CONTRACT's join).
import sys, re, os, csv
sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract
VBF = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf"
TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "03-World-Area-Field", "Map-Pack",
                   "members", "map-ref-field-packs.tsv")
f = open(VBF, "rb")
names, blocks = vbfextract.load_index(f)
fails = 0
for code in ("rbl0102", "rbl0121", "gil0301", "gil0303"):
    hits = [n for n in names if code in n.lower()]
    mpk = [n for n in hits if n.lower().endswith(".mpk")]
    js = [n for n in hits if n.lower().startswith("jsondata/maps/")]
    kinds = sorted({n.split("/")[0] + "/" + n.split("/")[1] for n in hits})
    print("C1/C2 %s: %d entries %s | pack %s | map json %s" % (code, len(hits), kinds, mpk or "NONE", js or "NONE"))
p = vbfextract.read_entry(f, names, blocks, 'ps2data/plan_master/map_ctrl/gil03/gil0303/bin/gil0303.mpk')
codes = sorted({c.decode() for c in re.findall(rb'[a-z]{3}\d{4}', p)})
print("C3 map codes inside gil0303.mpk:", codes)
rows = [r for r in csv.reader((l for l in open(TSV, encoding="utf-8") if not l.startswith("#")), delimiter="\t")]
own = {}
for r in rows:
    try:
        own[int(r[0])] = r[2]
    except (ValueError, IndexError):
        pass
from collections import Counter
cnt = Counter(own.values())
print("C4 fields owning rbl0121.mpk %d, gil0303.mpk %d, gil0301.mpk %d" % (cnt["rbl0121.mpk"], cnt["gil0303.mpk"], cnt["gil0301.mpk"]))
print("C4 fields 1000..1007:", [(i, own.get(i)) for i in range(1000, 1008)])
print("C4 fields 668..672:", [(i, own.get(i)) for i in range(668, 673)])
ok = own.get(1003) == "gil0303.mpk" and own.get(670) == "rbl0121.mpk"
print("CONTROL census rows 1003 -> gil0303.mpk and 670 -> rbl0121.mpk:", "PASS" if ok else "FAIL")
fails += (not ok)
print("FAILS", fails)
