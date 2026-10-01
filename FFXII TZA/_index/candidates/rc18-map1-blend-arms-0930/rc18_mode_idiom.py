"""rc18_mode_idiom.py - RC-18: do shipped scripts rebuild slot map 1 right after changing the runtime mode?
ORACLE, 2026-09-30. Static, over FABLE's decompiled US corpus (../../../../Tools/work/FABLE/pub140-scratch/corpus/us,
*.txt). The mode setters (seteventpartymode 00307240, seteventparty2mode 00307200, setchocobomode / the chocobo
setter 00303D90, the summon setter 00313550) only flip a bit of block +0x5B04; slot map 1 is rebuilt only by
BattleGroup_RefreshFourActorDefinitions 003266C0, reached from the read-in verbs (partyallread 0x03EB,
partyallread2 0x046F, summonread 0x0203, summontopartyread 0x0207 -> 0037C980/0037CA00/0037CA80 -> 00233CF0) and
from the reconcile functions 003261D0 / 003273D0. For every mode-verb call this lists the next statement.
Positive control: the census must find `seteventpartymode(1);` followed by `partyallread();` (seen by hand in the
corpus)."""
import collections, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
MODE = re.compile(r"\b(seteventpartymode|seteventparty2mode|setchocobomode|ridechocobo|getoffchocobo|btlAtelSetSummonMode)\s*\(([^;]*)\)\s*;")
READIN = ("partyallread", "partyallread2", "summonread", "summontopartyread")


def main():
    files = sorted(glob.glob(os.path.join(CORPUS, "*.txt")))
    tally = collections.Counter()
    nxt_by = collections.defaultdict(collections.Counter)
    for p in files:
        lines = [l.strip() for l in open(p, encoding="utf-8", errors="replace")]
        for k, l in enumerate(lines):
            m = MODE.search(l)
            if not m:
                continue
            verb, arg = m.group(1), m.group(2).strip()
            tally[(verb, arg)] += 1
            nxt = ""
            for l2 in lines[k + 1:k + 6]:
                if l2 and l2 not in ("{", "}"):
                    nxt = l2
                    break
            name = re.match(r"([A-Za-z_0-9]+)\s*\(", nxt)
            nxt_by[(verb, arg)][name.group(1) if name else nxt[:30]] += 1
    print("scripts read: %d" % len(files))
    ok = nxt_by[("seteventpartymode", "1")]["partyallread"] > 0
    print("%s  control: seteventpartymode(1) followed by partyallread() found" % ("PASS" if ok else "FAIL"))
    for key in sorted(tally):
        c = nxt_by[key]
        ri = sum(v for n, v in c.items() if n in READIN)
        print("%-22s arg %-6s calls %5d  next statement a read-in verb %5d  other next: %s" % (
            key[0], key[1], tally[key], ri, ", ".join("%s x%d" % kv for kv in c.most_common() if kv[0] not in READIN)[:300]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
