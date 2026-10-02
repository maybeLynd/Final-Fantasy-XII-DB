"""restatus_spawn.py [--apply] - re-status spawn-placement-and-retirement.md DOCUMENTED (OPUS, 2026-10-01).

FABLE's 2026-09-30 condition: keep REOPENED until a fresh graph audit of the amended citation surface is clean and
the owner has read the DD pass. The audit (audit_crossrefs.py over this page alone, xref_report.md) reports 0
findings; documented_rule.py reads READY-WITH-POINTER (L-12 / L-13 SUPERSEDED, L-13's live residue routed, section 7).
FABLE is inactive; OPUS reads it under the user's 2026-10-01 authority. Idempotent; dry run unless --apply; FAILS n.
"""
import os
import sys

P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                  "05-Spawn-Encounter-Lifecycle", "spawn-placement-and-retirement.md"))
OLD_PREFIX = "status: REOPENED — reopened 2026-09-12 by ASTRA's independent falsification"
NEW = ("status: DOCUMENTED — owner re-status 2026-10-01 (OPUS, for FABLE; documented_rule READY-WITH-POINTER): FABLE's "
       "2026-09-30 conditions are met - a fresh graph audit of this page reports 0 findings "
       "(_index/candidates/opus-spawn-restatus-1001/xref_report.md) and the DD pass is read. History: REOPENED 2026-09-12 "
       "by ASTRA's independent falsification (§11), whose corrections are integrated; the two rows it opened are closed "
       "as L-12 SUPERSEDED (2026-09-26) and L-13 SUPERSEDED (2026-09-27), and L-13's live-only residue is routed for a "
       "runtime carrier (§7)")


# citation form only: four interior call-site citations inside generated-family members would refuse those families
# once the page is DOCUMENTED (adrift_report); each is narrowed to its function entry, the claim unchanged
NARROW = [
    ("| `0050F52C` only |", "| one call site, in `0050F520` |"),
    ("| `0051026C` only |", "| one call site, in `00510260` |"),
    ("read there: `0050F52C`, `0051026C`, ", "read there: the sites in `0050F520` and `00510260`, "),
    ("| [`0039440A`](../_index/ADDRESS-INDEX.md) |", "| [`00394400`](../_index/ADDRESS-INDEX.md) |"),
    ("| [`00394522`](../_index/ADDRESS-INDEX.md) |", "| [`00394520`](../_index/ADDRESS-INDEX.md) |"),
]


def narrow(apply):
    t = open(P, "rb").read().decode("utf-8")
    fails = 0
    for old, new in NARROW:
        if new in t:
            continue
        if t.count(old) != 1:
            print("REFUSING narrow", old, t.count(old)); fails += 1; continue
        t = t.replace(old, new, 1)
        print(("PATCHED" if apply else "WOULD PATCH") + " narrow " + old[:20])
    if apply and not fails:
        open(P, "wb").write(t.encode("utf-8"))
    return fails


def main():
    apply = "--apply" in sys.argv
    if narrow(apply):
        print("FAILS 1"); return 1
    t = open(P, "rb").read().decode("utf-8")
    lines = t.split("\n")
    if any(l.rstrip("\r") == NEW for l in lines) and "  crossref_clean: true" in t:
        print("ALREADY"); print("FAILS 0"); return 0
    st = [i for i, l in enumerate(lines) if l.startswith(OLD_PREFIX)]
    cc = [i for i, l in enumerate(lines) if l.rstrip("\r") == "  crossref_clean: false"]
    if len(st) != 1 or len(cc) != 1:
        print("REFUSING", len(st), len(cc)); print("FAILS 1"); return 1
    for i, new in ((st[0], NEW), (cc[0], "  crossref_clean: true")):
        cr = "\r" if lines[i].endswith("\r") else ""
        lines[i] = new + cr
    print(("PATCHED" if apply else "WOULD PATCH") + " status and crossref_clean")
    if apply:
        open(P, "wb").write("\n".join(lines).encode("utf-8"))
    print("FAILS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
