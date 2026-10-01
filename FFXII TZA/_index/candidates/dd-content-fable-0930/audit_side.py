"""audit_side.py - one side of the neighbour differential for the eight DD pages (FABLE, 2026-09-30).

    python audit_side.py <docs dir> <out.json>

Runs the same measurement check_publish_neighbours.py runs on each of its two worktrees - audit_crossrefs over the whole
docs tree (its findings() helper) and check_links --raw (its broken_links() helper) - on an exported tree, because the
guard itself copies the published paths from the shared working tree, which this draft must not touch. Writes every
finding attributed to one of the eight pages, and every broken link whose source is one of them."""
import importlib.util, json, os, sys
KIT = r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
spec = importlib.util.spec_from_file_location("cpn", os.path.join(KIT, "check_publish_neighbours.py"))
cpn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpn)
PAGES = [
    "04-Actor-Entity/the-field-runtime-pass.md",
    "04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md",
    "05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md",
    "07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md",
    "07-Combat-Action/Action-Definition-Row/the-action-definition-row.md",
    "08-Combat-Formula/combos-and-the-guard-parry-flag.md",
    "08-Combat-Formula/where-a-stat-number-comes-from.md",
    "08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md",
]
docs, out = sys.argv[1], sys.argv[2]
tmp = out + ".audit.json"
allf = cpn.findings(docs, tmp)
norm = lambda s: s.replace("\\", "/")
mine = sorted(f for f in allf if any(norm(f[1]).endswith(p) for p in PAGES))
links = cpn.broken_links(docs) or set()
mylinks = sorted(l for l in links if any(norm(l[0]).endswith(p) for p in PAGES))
json.dump({"findings": mine, "neighbours": sorted(cpn.neighbours(set(mine))), "broken_links": mylinks,
           "total_findings_all_docs": len(allf)}, open(out, "w", encoding="utf-8"), indent=1)
print("%s: %d findings on the eight pages (%d NEIGHBOUR), %d broken links from them; %d findings corpus-wide"
      % (docs, len(mine), len(cpn.neighbours(set(mine))), len(mylinks), len(allf)))
