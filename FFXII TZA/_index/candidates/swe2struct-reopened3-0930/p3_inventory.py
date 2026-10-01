"""Reopened page 3 (SWE2-STRUCT for OPUS, 2026-10-01): 23-Third-Party-Libraries/third-party-middleware-inventory.md

Run: python -B p3_inventory.py   (last line FAILS n; must be FAILS 0)
Inputs, read only: Tools/work/graph/functions.tsv with its functions.parent.json stamp (the certified GN162 parent
59629b9b..., exported 2026-09-17); Tools/work/graph_gn/functions.tsv (the 2026-09-02 GN export the page's pass 3
measured, used only as the positive control); the certified image through retool.py (its call scan).

THE FALSIFICATION PASS - the census the page reopened on (section 2 'Corrected totals', the lede and section 8):
ThirdParty.* 691 with its per-library split, bare-name families EASTL 72 / Lua 21 / Bullet 18 = 111, total 802.
The selector is the page's own: rows whose tags contain no 'ThirdParty' token, carrying a
GFZ.V121.CodeDomain.<EASTL|Lua|Bullet>.* tag; the ThirdParty split groups by the first two tag components.

  N0     the stamp names the certified GN162 parent, 38,161 functions, the authorised EXE
  N1     CONTROL: the GN export reproduces the page's own 2026-09-02 figures exactly - ThirdParty 690, EASTL 72
         (BasicString 58, ContainerRuntime 14), Lua 21 (Math 15, Runtime 4, StringPattern 2), Bullet 18
         (Collision 11, Dynamics 5, LinearMath 1, Physics 1), total 801 - so the selector is the page's
  N2     GN162: ThirdParty.* 691, and every per-library row of the section 2 table holds (PPFX 348, Bullet 120,
         libvpx 73, Lua 90, zlib 25 = 16 + 9, libvorbis 11, Dear ImGui 7, Tremor 4, libxml2 4, JsonBox 4,
         YEBIS 3, zlib adapter 1) plus the R109 XML.ConfigParse 1
  N3     GN162: Lua 21 and Bullet 18 hold; EASTL is 97, not 72 - a third subfamily, OrderedContainerRuntime 25
  N4     the 25 are re-tags, not new functions: each was CxxStandardLibrary.OrderedContainerRuntime.* in the GN
         export; 0016D840 (the red-black insert of the-ordered-container-runtime.md) is among them
  N5     GN162 bare-name total 136, so the tag-census total is 691 + 136 = 827, not 802 (or 801)
  N6     the census is clean: 38,161 rows, 0 duplicate entries; every bare-name row carries a single family tag
  G1-G3  the correction to section 7's CF-2 box (register G-23, 2026-09-16): libvorbis IS reached - 001B7F30 calls
         0067A480, 0067A480 calls 00679A50, and 00679A50 calls libvorbis bodies inside 008800C0..008958B0
"""
import collections, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GRAPH = os.path.join(DB, "Tools", "work", "graph")
GN = os.path.join(DB, "Tools", "work", "graph_gn", "functions.tsv")
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
FAILS = 0
N = 0


def check(cid, ok, text, detail=""):
    global FAILS, N
    N += 1
    if not ok:
        FAILS += 1
    print("%s %-4s %s%s" % ("PASS" if ok else "FAIL", cid, text, ("  -- " + detail) if detail else ""))


def census(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    tp = collections.Counter()
    bare = collections.Counter()
    sub = collections.Counter()
    multi = 0
    tagof = {}
    for r in rows:
        tags = [t for t in r["tags"].split(";") if t]
        tagof[r["entry"]] = tags
        if "ThirdParty" in r["tags"]:
            keys = set(".".join(t.split("ThirdParty.")[1].split(".")[:2]) for t in tags if "ThirdParty" in t)
            tp[tuple(sorted(keys))] += 1
            continue
        fams = set()
        for t in tags:
            for fam in ("EASTL", "Lua", "Bullet"):
                if t.startswith("GFZ.V121.CodeDomain." + fam + "."):
                    fams.add(fam)
                    sub[(fam, t.split(".")[4])] += 1
        for fam in fams:
            bare[fam] += 1
        if len(fams) > 1:
            multi += 1
    return rows, tp, bare, sub, multi, tagof


stamp = json.load(open(os.path.join(GRAPH, "functions.parent.json")))
check("N0", stamp["parent_gzf_sha256"].startswith("59629b9b") and "GN162" in stamp["program_name"]
      and stamp["function_count"] == 38161 and stamp["executable_sha256"].startswith("73461d08"),
      "functions.parent.json: the certified GN162 parent 59629b9b, 38,161 functions, EXE 73461d08", stamp["exported_utc"])

g_rows, g_tp, g_bare, g_sub, g_multi, g_tag = census(GN)
ok = (sum(g_tp.values()) == 690 and dict(g_bare) == {"EASTL": 72, "Lua": 21, "Bullet": 18}
      and g_sub[("EASTL", "BasicString")] == 58 and g_sub[("EASTL", "ContainerRuntime")] == 14
      and (g_sub[("Lua", "Math")], g_sub[("Lua", "Runtime")], g_sub[("Lua", "StringPattern")]) == (15, 4, 2)
      and (g_sub[("Bullet", "Collision")], g_sub[("Bullet", "Dynamics")], g_sub[("Bullet", "LinearMath")],
           g_sub[("Bullet", "Physics")]) == (11, 5, 1, 1)
      and sum(g_tp.values()) + sum(g_bare.values()) == 801)
check("N1", ok, "CONTROL: the 2026-09-02 GN export reproduces the page's pass-3 figures exactly (690 + 72 + 21 + 18 = 801)",
      "%d %s" % (sum(g_tp.values()), dict(g_bare)))

rows, tp, bare, sub, multi, tag = census(os.path.join(GRAPH, "functions.tsv"))
want = {"Rendering.PPFX": 348, "Physics.Bullet": 120, "Video.LibVPX_VP8_1_6_0": 73, "Scripting.Lua": 90,
        "Compression.Zlib_1_2_11": 16, "Compression.Zlib": 9, "Audio.LibVorbis": 11, "UI.DearImGui": 7, "Audio.Tremor": 4,
        "XML.Libxml2": 4, "Serialization.JsonBox": 4, "Rendering.Yebis": 3, "Compression.ZlibAdapter": 1,
        "XML.ConfigParse": 1}
got = {k[0]: v for k, v in tp.items() if len(k) == 1}
check("N2", sum(tp.values()) == 691 and got == want and all(len(k) == 1 for k in tp),
      "GN162 ThirdParty.* = 691; every row of section 2's table holds, plus the R109 XML.ConfigParse member", str(got))
check("N3", bare["Lua"] == 21 and bare["Bullet"] == 18 and bare["EASTL"] == 97
      and sub[("EASTL", "BasicString")] == 58 and sub[("EASTL", "ContainerRuntime")] == 14
      and sub[("EASTL", "OrderedContainerRuntime")] == 25,
      "GN162 bare-name: Lua 21 and Bullet 18 hold; EASTL is 97 = BasicString 58 + ContainerRuntime 14 + "
      "OrderedContainerRuntime 25 (the page says 72)", str(dict(bare)))
oc = [e for e, t in tag.items() if any(x.startswith("GFZ.V121.CodeDomain.EASTL.OrderedContainerRuntime.") for x in t)]
was = [e for e in oc if any(x.startswith("GFZ.V121.CodeDomain.CxxStandardLibrary.OrderedContainerRuntime.") for x in g_tag.get(e, []))
       and not any("EASTL" in x for x in g_tag.get(e, []))]
check("N4", len(oc) == 25 and len(was) == 25 and "0016D840" in oc,
      "the 25 are re-tags of rows that were CxxStandardLibrary.OrderedContainerRuntime.* at GN, 0016D840 among them",
      "%d %d" % (len(oc), len(was)))
check("N5", sum(bare.values()) == 136 and sum(tp.values()) + sum(bare.values()) == 827,
      "GN162 bare-name total 136; tag-census total 691 + 136 = 827 (the page says 111 and 802; its lede and section 8 say 801)")
entries = [r["entry"] for r in rows]
check("N6", len(entries) == 38161 and len(set(entries)) == 38161 and multi == 0
      and all(len(tag[e]) == 1 for e in oc),
      "38,161 rows, 0 duplicate entries, no row in two bare families; the 25 carry a single tag each")

import retool as T  # noqa: E402
calls = T.scan()["calls"]


def callees_of(fn):
    return sorted(c for c, s in calls.items() if any(f == fn for f, site in s))


c1 = sorted(set(f for f, s in calls.get(0x0067A480, ())))
check("G1", 0x001B7F30 in c1, "001B7F30 calls 0067A480 (the movie player FR-1 names)", str([hex(x) for x in c1]))
c2 = sorted(set(f for f, s in calls.get(0x00679A50, ())))
check("G2", c2 == [0x0067A480], "00679A50 has exactly one caller, 0067A480", str([hex(x) for x in c2]))
v = [c for c in callees_of(0x00679A50) if 0x008800C0 <= c < 0x008958B0]
check("G3", {0x008800C0, 0x00880AF0, 0x00880BF0} <= set(v),
      "00679A50 calls libvorbis bodies 008800C0, 00880AF0, 00880BF0 inside 008800C0..008958B0: libvorbis is reached, "
      "two hops below the movie player", str([hex(x) for x in v]))
print("CHECKS %d" % N)
print("FAILS %d" % FAILS)
