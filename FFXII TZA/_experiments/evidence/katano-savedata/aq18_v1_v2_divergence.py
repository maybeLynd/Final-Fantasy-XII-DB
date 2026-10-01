"""Does v1's defect actually FIRE in shipping FF12? ASTRA's package could not say.

ASTRA proved v1 misplaces addresses on synthetic fixtures and was careful to add that this
"does not show that one of these synthetic patterns occurs in the historical FF12 scan".
That is the open question in the contradiction's MISSING_INFORMATION, and it decides whether
any historical claim built on v1 has to move.

METHOD. Both sources are executed unmodified except for one injected collector on the line
they share - `resolved_sites += 1` - so every site either tracker resolves is recorded with
the address it resolved to. Nothing else is patched; both read the same catalog and the same
image. The two address maps are then compared site by site:

  AGREE      - same site, same address. The repair changed nothing there.
  MISPLACED  - same site, DIFFERENT address. v1 was wrong at a real instruction: this is the
               defect firing in shipping code, and it is the number that decides whether
               historical claims move.
  V2-ONLY    - v2 resolves a site v1 lost, from the recovered register-add and narrow-merge
               rules. Pure coverage gain.
  V1-ONLY    - v1 resolved a site v2 does not. Expected to be zero; a non-zero count would
               mean the repair LOST coverage and would need explaining, not shipping.
"""
import contextlib, io, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INJECT = "            resolved_sites += 1"
COLLECT = INJECT + "\n            _ALL.append((ins.address, addr))"


def run(path):
    src = path.read_bytes().decode("utf-8")
    assert src.count(INJECT) == 1, ("collector anchor moved in %s" % path.name)
    ns = {"__name__": "__divergence_probe__", "_ALL": []}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src.replace(INJECT, COLLECT), str(path), "exec"), ns)
    return ns["_ALL"], ns


v1_sites, v1ns = run(HERE / "aq18_span_write_census.py")
v2_sites, v2ns = run(HERE / "aq18_span_write_census_v2.py")

# A site can appear more than once (two memory operands on one instruction); compare as
# multisets keyed by site, so a genuine difference cannot hide behind ordering.
from collections import defaultdict
m1, m2 = defaultdict(list), defaultdict(list)
for s, a in v1_sites: m1[s].append(a)
for s, a in v2_sites: m2[s].append(a)
for d in (m1, m2):
    for k in d: d[k].sort()

agree = misplaced = 0
mis_examples = []
for s in set(m1) & set(m2):
    if m1[s] == m2[s]:
        agree += len(m1[s])
    else:
        misplaced += 1
        if len(mis_examples) < 20:
            mis_examples.append((s, m1[s], m2[s]))
v2_only = sum(len(m2[s]) for s in set(m2) - set(m1))
v1_only = sum(len(m1[s]) for s in set(m1) - set(m2))

print("v1 resolved sites: %7d   (%d distinct instructions)" % (len(v1_sites), len(m1)))
print("v2 resolved sites: %7d   (%d distinct instructions)" % (len(v2_sites), len(m2)))
print()
print("AGREE     %7d" % agree)
print("MISPLACED %7d   <- v1's defect firing at a real instruction" % misplaced)
print("V2-ONLY   %7d   <- coverage the repair recovered" % v2_only)
print("V1-ONLY   %7d   <- must be 0, or the repair lost coverage" % v1_only)
print()
if mis_examples:
    print("MISPLACED SITES (v1 address -> v2 address):")
    for s, a1, a2 in sorted(mis_examples):
        print("  %08X  v1 %s   v2 %s"
              % (s, ",".join("%08X" % x for x in a1), ",".join("%08X" % x for x in a2)))
    print()

LO, HI = v2ns["LO"], v2ns["HI"]
into = [(s, a1, a2) for s, a1, a2 in
        [(s, m1[s], m2[s]) for s in set(m1) & set(m2) if m1[s] != m2[s]]
        if any(LO <= x < HI for x in a1) or any(LO <= x < HI for x in a2)]
print("Of the misplaced sites, ones where EITHER address lands in the contested span: %d"
      % len(into))
print("span %08X..%08X" % (LO, HI))
print()
print("v1 span hits: %d    v2 span hits: %d" % (len(v1ns["span_hits"]), len(v2ns["span_hits"])))
print("v1 record hits: %d  v2 record hits: %d" % (len(v1ns["record_hits"]), len(v2ns["record_hits"])))
