"""apply_narrowings.py [--apply] - FABLE's non-author review of SWE2-ORACLE's EXP-091 resolver-base repair
(_index/candidates/auditspec-review-oracle-exp091-resolver-repair-1003/REVIEW.md, section 4, items A-E) gives exact
replacement text for three OPUS-owned consumers; OPUS applies them as written (OPUS, 2026-10-03, on
SWE2ORACLE-REQ-OPUS-EXP091-CONSUMER-NARROWINGS-1003). Item A also takes the review's offered count fix in the same
sentence: 85/85 -> 87/87 (the retained result since f7bbac4ef).

Old text is matched with flexible whitespace (the pages wrap it across lines); the replacement is written as one
paragraph run in place. Refuses unless every target file is clean and every old text occurs exactly once; idempotent
(ALREADY when every new text is present and no old text is). Prints FAILS n."""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SEVEN = "`0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80` or `003DC780`"
ITEMS = [
    ("A", "07-Combat-Action/CONTRACT-commit-action.md",
     "ran exactly those insides — every scripted callee plus its bounded transitive closure, ~54 shipped bodies, then "
     "`0030F760` re-driven end to end with the real callees wired in.",
     "ran those insides — every scripted callee and 47 of the 54 bodies `bodies.json` lists for their bounded transitive "
     "closure — then `0030F760` re-driven end to end with the real callees wired in. The retained 87 cases and 10 "
     "mutants execute no instruction of " + SEVEN + ", and run `0030C0E0` only to `0030C179` (`canc-fixup`). That is a "
     "coverage gap of the retained fixtures. It invalidates no retained case (bit 22, copy, cancel, commit, mutants), and "
     "it does not show that the game never runs those bodies. `0020E600` and `0030C0E0`'s action-row arm "
     "`0030C187..0030C1CA` are executed by [`exp091-resolver-base-repair-1003`](../_experiments/evidence/"
     "exp091-resolver-base-repair-1003/README.md) (`tv-row6-set`/`tv-row6-zero`, resolver base planted at `01F83530`, "
     "method B; returns 1 iff action-row byte 6 != 0)."),
    ("A-count", "07-Combat-Action/CONTRACT-commit-action.md",
     "**85/85 cases, 10/10 byte-level mutants detected, stable across two processes.**",
     "**87/87 cases (85/85 before `f7bbac4ef` added the two copy-origin cases), 10/10 byte-level mutants detected, "
     "stable across two processes.**"),
    ("B", "07-Combat-Action/CONTRACT-commit-action.md",
     "approximate on jump-table dispatchers**, though every listed VA was genuinely executed.",
     "approximate on jump-table dispatchers**. The list is not an execution record: under the retained 87 cases and 10 "
     "mutants, 47 of its 54 VAs execute and the seven named in §13a do not (instruction-level span census, "
     "`_index/candidates/auditspec-review-oracle-exp091-resolver-repair-1003/REVIEW.md`)."),
    ("C", "_experiments/EXP-091-commit-callees-exec.md",
     "plus their bounded transitive closure (~54 shipped bodies)",
     "plus their bounded transitive closure (`bodies.json` lists 54 bodies; the retained fixtures execute 47 — see "
     "`evidence/exp091-resolver-base-repair-1003/`)"),
    ("D", "_experiments/EXP-091-commit-callees-exec.md",
     "every listed VA was genuinely executed.",
     "47 of the 54 listed VAs execute under the retained 87 cases and 10 mutants. `0020E600`, `0025AAD0`, `002F1710`, "
     "`00316A50`, `00317E50`, `003BBC80` and `003DC780` do not. This is a coverage gap of these fixtures, not a "
     "reachability result. The harness planted the resolver base at `0x1F85D30`, not the `0x1F83530` that `0020E602` "
     "reads. No retained case reaches `0020E600` or reads either cell, so no retained result changes. The repair and "
     "the action-row control are in `evidence/exp091-resolver-base-repair-1003/`."),
    ("E", "_index/candidates/s20-runtime-per-invariant-exposure.md",
     "~54 bodies (`bodies.json`), including",
     "54 bodies listed in `bodies.json`, 47 of which the retained fixtures execute (not `0020E600`, `0025AAD0`, "
     "`002F1710`, `00316A50`, `00317E50`, `003BBC80`, `003DC780`), including"),
]


def flex(s):
    return re.compile(r"\s+".join(re.escape(t) for t in s.split()))


fails = 0
texts = {}
dirty = []
for _id, rel, old, new in ITEMS:
    if rel not in texts:
        p = os.path.join(DB, *rel.split("/"))
        texts[rel] = io.open(p, encoding="utf-8", newline="").read()
        if subprocess.run(["git", "-C", DB, "diff", "--quiet", "--", rel]).returncode:
            dirty.append(rel)
done = 0
for _id, rel, old, new in ITEMS:
    t = texts[rel]
    n_old = len(flex(old).findall(t))
    if new in t and n_old == 0:
        done += 1
        continue
    if n_old != 1:
        print("%s: old text occurs %d times in %s (need 1)" % (_id, n_old, rel))
        fails += 1
        continue
    texts[rel] = flex(old).sub(lambda m: new, t, count=1)
if done == len(ITEMS) and not fails:
    print("ALREADY (%d items)" % done)
    print("FAILS 0")
    sys.exit(0)
for rel in dirty:
    print("REFUSED: %s has uncommitted changes" % rel)
    fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
for rel, t in texts.items():
    p = os.path.join(DB, *rel.split("/"))
    io.open(p + ".opus-tmp", "w", encoding="utf-8", newline="").write(t)
    os.replace(p + ".opus-tmp", p)
print("APPLIED: %d items" % (len(ITEMS) - done))
print("FAILS 0")
