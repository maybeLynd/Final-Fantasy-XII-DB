"""dd_verdicts.py - documented_rule verdicts for the eight DD pages on an exported tree (FABLE, 2026-09-30).

    python dd_verdicts.py <db root of an export>                 judge the pages as they are
    python dd_verdicts.py <db root> --simulate-registered        also: map every FD-n<k> placeholder to a synthetic id
                                                                 FD-9<k-tail> registered OPEN, as after new_rows.tsv lands

It imports documented_rule.py from the LIVE tree, so the register, the foreign-id registries and the git-tracked set
(condition T) are the live ones; only the page texts (and, for a NOTE, its parent) come from the export. A plain run of
documented_rule.py inside a `git archive` export would read an empty tracked set (no .git), which is why this wrapper
exists. The S self-test runs first, as in documented_rule.main().
"""
import io, os, re, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
# installed in _index/candidates/dd-content-fable-0930/: the rule is its sibling folder; the draft copy uses the live tree
LIVE = os.path.join(_HERE, "..", "status-currency-ruling-fable")
if not os.path.isfile(os.path.join(LIVE, "documented_rule.py")):
    LIVE = r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates/status-currency-ruling-fable"
sys.path.insert(0, LIVE)
import documented_rule as R

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
PH = re.compile(r"\bFD-n(\d+)\b")


def main():
    db = sys.argv[1]
    sim = "--simulate-registered" in sys.argv
    state, kind, word, dup = R.register()
    foreign, untracked = R.foreign_ids(), R.evidence_status()
    real = set(state)
    if sim:
        state, kind = dict(state), dict(kind)
    print("dd_verdicts: db=%s simulate-registered=%s" % (db, sim))
    for p in PAGES:
        path = os.path.join(db, p)
        text = io.open(path, encoding="utf-8", errors="replace").read()
        used = sorted(set(PH.findall(text)), key=int)
        if sim and used:
            for k in used:
                rid = "FD-%d" % (900 + int(k[0]) * 10 + int(k[-1]))   # FD-n501 -> FD-951, FD-n101 -> FD-911
                assert rid not in real, rid
                state[rid], kind[rid], word[rid], dup[rid] = "OPEN", "open", "", None
                text = re.sub(r"\bFD-n%s\b" % k, rid, text)
        v, named, boxes, live, disposed, missing = R.judge(text, state, kind, word, dup, page_dir=os.path.dirname(path),
                                                          foreign=foreign, page_path=path, untracked=untracked)
        print("%-19s %s  kinds=%s boxes=%d live=%s disposed=%s missing=%s placeholders=%s" % (
            v, p, ",".join("%s:%s" % (i, kind[i]) for i in named) or "-", boxes, ",".join(live) or "-",
            ",".join("%s:%s" % (i, word[i]) for i in disposed) or "-", ",".join(missing) or "-",
            ",".join("FD-n" + k for k in used) or "-"))


if __name__ == "__main__":
    main()
