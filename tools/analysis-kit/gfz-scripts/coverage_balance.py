#!/usr/bin/env python3
"""
coverage_balance.py - decide which category the next work block should target.

An unattended loop drifts. When one technique keeps yielding, the natural next block is
"more of that", and a session can spend nine iterations in two categories while sixteen sit
untouched. This makes the next choice data-driven instead of momentum-driven.

Ranks categories by unexplained weight:

    debt = functions / (documents + 1)

so a large category with no documents outranks a small one that is already covered, and
having written something never zeroes a category out.

Usage:
  coverage_balance.py --db "<database root>" [--top N] [--json out.json]

Exit code 1 if any category with >= --alert functions still has zero documents.
"""
import argparse
import io
import json
import os
import sys

# Function counts from the certified ledger. PrimaryOwner categories plus the
# CodeDomain-defined substrate categories. Update when the ledger moves materially.
CATEGORY_FUNCTIONS = {
    "00-Engine-Core-Runtime": 73,
    "01-Script-VM-Native-Bridge": 1900,
    "02-Resource-And-Asset-Pipeline": 572,
    "03-World-Area-Field": 108,
    "04-Actor-Entity": 235,
    "05-Spawn-Encounter-Lifecycle": 52,
    "06-Movement-And-Navigation": 485,
    "07-Combat-Action": 134,
    "08-Combat-Formula": 198,
    "09-Combat-AI-And-Gambits": 43,
    "10-Status-Periodic-Terminal": 24,
    "11-Party": 79,
    "12-Items-Equipment-Shops-License": 70,
    "13-Rewards-Progression-Economy": 38,
    "14-Story-Event-Quest-Hunt": 15,
    "15-Input": 1047,
    "16-UI": 544,
    "17-Presentation-Rendering": 1564,
    "18-Audio": 2064,
    "19-Save-Load-Settings": 87,
    "20-Platform-Online-Achievements": 59,
    "21-RNG-And-Determinism": 18,
    "22-Middleware-PhyreEngine": 6768,
    "23-Third-Party-Libraries": 1000,
    "24-Compiler-And-CRT-Runtime": 5150,
    "99-Unresolved-Residual": 158,
}

# Categories a modder reaches for first. Ties break toward these.
PLAYER_FACING = {
    "01-Script-VM-Native-Bridge", "02-Resource-And-Asset-Pipeline",
    "04-Actor-Entity", "05-Spawn-Encounter-Lifecycle",
    "06-Movement-And-Navigation", "07-Combat-Action", "08-Combat-Formula",
    "09-Combat-AI-And-Gambits", "11-Party", "12-Items-Equipment-Shops-License",
    "13-Rewards-Progression-Economy", "14-Story-Event-Quest-Hunt",
    "16-UI", "19-Save-Load-Settings",
}


def count_docs(path):
    n = 0
    for dirpath, _d, files in os.walk(path):
        for fn in files:
            if fn.lower().endswith(".md") and fn.lower() != "readme.md":
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--alert", type=int, default=200,
                    help="fail if a category this large has zero documents")
    ap.add_argument("--json")
    a = ap.parse_args()

    rows = []
    for cat, funcs in CATEGORY_FUNCTIONS.items():
        d = os.path.join(a.db, cat)
        docs = count_docs(d) if os.path.isdir(d) else 0
        debt = funcs / float(docs + 1)
        rows.append({
            "category": cat, "functions": funcs, "documents": docs,
            "debt": debt, "player_facing": cat in PLAYER_FACING,
        })
    rows.sort(key=lambda r: (-r["debt"], not r["player_facing"]))

    print("%-34s %8s %5s %10s" % ("category", "funcs", "docs", "debt"))
    print("-" * 62)
    for r in rows[:a.top]:
        mark = " *" if r["player_facing"] else "  "
        print("%-34s %8d %5d %10.0f%s"
              % (r["category"], r["functions"], r["documents"], r["debt"], mark))
    print()
    print("* = player-facing; a modder reaches for these first")

    starved = [r for r in rows if r["documents"] == 0 and r["functions"] >= a.alert]
    if starved:
        print()
        print("UNTOUCHED and large (>= %d functions):" % a.alert)
        for r in starved:
            print("  %-34s %6d functions" % (r["category"], r["functions"]))

    zero = [r["category"] for r in rows if r["documents"] == 0]
    print()
    print("categories with zero documents: %d of %d" % (len(zero), len(rows)))
    print("NEXT BLOCK SHOULD TARGET: %s" % rows[0]["category"])

    if a.json:
        with io.open(a.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows, f, indent=2)

    return 1 if starved else 0


if __name__ == "__main__":
    sys.exit(main())
