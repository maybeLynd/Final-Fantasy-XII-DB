#!/usr/bin/env python3
"""contract_map_sync.py - report how a harness's CONTRACT_MAP differs from its contract's section 15.

Why this exists
---------------
`parity_status.py` already REFUSES a harness whose CONTRACT_MAP has drifted from section 15 - wrong
wording, a missing claim, or the same claims in a different order. What it does not do is say what
to write instead, and the failure is easy to cause by accident: adding one evidence row to a
contract silently invalidates the map of every harness that declares it.

This does the read-only half of the fix. It prints, in section-15 order:

  * the claims the map is MISSING, with the exact string to paste
  * the map rows that match NO claim (usually a reworded row - the old text is shown so the
    hand-written status and reason can be moved across rather than retyped)
  * whether the two agree on order once the sets match

**It never edits the harness.** The status and the reason on each row are judgements about what a
suite actually drives, and a tool that invented them would be manufacturing exactly the kind of
unearned coverage the campaign exists to catch. Pasting is the point: the claim string is
mechanical, the verdict is not.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("harness", nargs="*",
                    help="diff_*.py to check; default every harness parity_status knows")
    a = ap.parse_args()

    import parity_status as PS

    harnesses = a.harness
    if not harnesses:
        harnesses = [os.path.join(PS.DIFF, f) for f in sorted(os.listdir(PS.DIFF))
                     if f.startswith("diff_") and f.endswith(".py")]

    bad = 0
    for h in harnesses:
        name = os.path.basename(h)
        try:
            decl = PS.read_declaration(h)
            cmap = PS.read_contract_map(h)
        except Exception as e:                      # noqa: BLE001 - report, never crash a sweep
            print("%s: cannot read (%s)" % (name, e))
            bad += 1
            continue
        if cmap is None:
            print("%s: no CONTRACT_MAP" % name)
            bad += 1
            continue
        rel = (decl or {}).get("contract")
        if not rel:
            print("%s: declares no contract" % name)
            continue
        claims = PS.contract_claims(rel)
        if claims is None:
            print("%s: contract %s not found" % (name, rel))
            bad += 1
            continue

        mapped = [r[0] for r in cmap]
        missing = [c for c in claims if c not in mapped]
        extra = [c for c in mapped if c not in claims]
        if not missing and not extra and mapped == claims:
            print("%s: in step with %s (%d claims)" % (name, rel, len(claims)))
            continue

        bad += 1
        print()
        print("%s  vs  %s" % (name, rel))
        if missing:
            print("  MISSING from CONTRACT_MAP - paste these, then write the verdict yourself:")
            for c in missing:
                print("    (%r,\n     \"NOT EXERCISED\",\n     \"...\")," % c)
        if extra:
            print("  MATCHES NO CLAIM - reworded or deleted; move its verdict across:")
            for c in extra:
                row = next(r for r in cmap if r[0] == c)
                print("    %r" % (c,))
                print("        was: %s - %s" % (row[1], row[2][:70]))
        if not missing and not extra:
            print("  Same claims, WRONG ORDER. Section 15 order is:")
            for i, c in enumerate(claims):
                print("    %2d  %s" % (i, c))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
