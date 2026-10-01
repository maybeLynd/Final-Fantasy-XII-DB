#!/usr/bin/env python3
"""
rtti_challenge.py - try to prove the recovered RTTI mapping WRONG before trusting it.

rtti_recover.py produces address -> class::slot. That is a claim, not a fact. This script
attacks it four ways:

  1. AGREEMENT   For methods GFZ already classified independently (e.g. a Phyre.* CodeDomain
                 assigned from body evidence), does the RTTI class agree? Compared at
                 NAMESPACE level, not leaf name - see toks(). Restricted to unique-class
                 methods, because linker-folded addresses cannot carry one class identity.
  2. COLLISION   Does one address appear as a method of several unrelated classes? Some
                 sharing is legitimate (shared thunks, identical implementations); sharing
                 across unrelated namespaces is a red flag for a bad vtable walk.
  3. BOUNDS      Does every recovered method address land on a real Ghidra function entry?
                 A method pointing into the middle of a function means the walk over-ran.
  4. SLOT SANITY Are slots contiguous from 0 per vtable? Gaps mean the walk terminated early
                 or picked up non-vtable data.

Exit code 1 if any check finds something that blocks applying the mapping.
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc1_band

DOMAIN_PREFIX = "GFZ.V121.CodeDomain."


def load_functions(path):
    fn = {}
    with io.open(path, encoding="utf-8") as f:
        hdr = f.readline().rstrip("\n").split("\t")
        idx = {n: i for i, n in enumerate(hdr)}
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < len(hdr):
                continue
            tags = p[idx["tags"]]
            doms = [t[len(DOMAIN_PREFIX):] for t in tags.split(";")
                    if t.startswith(DOMAIN_PREFIX)]
            fn[p[idx["entry"]].upper()] = {
                "name": p[idx["name"]],
                "owner": p[idx["owner"]],
                "domains": doms,
            }
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..",
            "work", "graph", "functions.tsv")):
        _b = uc1_band.load()
        for e in _b["removed"]:
            fn.pop("%08X" % e, None)
        for st in _b["frontier"]:
            k = "%08X" % st
            fn[k] = {"name": "UC1-FRONTIER-%s" % k, "owner": "", "domains": []}
    return fn


def load_methods(path):
    rows = []
    with io.open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                rows.append((p[0].upper(), p[1], int(p[2])))
    return rows


def toks(s):
    """
    Comparable identifier tokens from either an RTTI class path or a GFZ CodeDomain.

    Why not a leaf-name substring test: GFZ CodeDomains are frequently GENERIC
    (`Phyre.SceneCamera.NativeQualified`, `Phyre.Middleware.NativeImplementation`), so
    comparing only the RTTI leaf (`PCameraPerspective`) scores a miss even when both
    derivations agree on the subject. That naive test reported 5.9 % agreement on
    2026-09-02 and looked like proof the mapping was broken; the correct namespace-level
    test on the same data reported 99.1 %. See _index/AUDIT-LOG.md.

    Strips the Phyre `P` / `V` / `C` type prefixes and template markers, and drops tokens
    too short to be discriminating.
    """
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    out = set()
    for w in s.split():
        w = re.sub(r'^(P|V|C)(?=[A-Z])', '', w)
        if len(w) > 3:
            out.add(w.lower())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--functions", required=True)
    ap.add_argument("--methods", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    fn = load_functions(a.functions)
    rows = load_methods(a.methods)

    by_addr = collections.defaultdict(set)
    by_vt = collections.defaultdict(list)
    for addr, cls, slot in rows:
        by_addr[addr].add(cls)
        by_vt[cls].append(slot)

    L = ["# RTTI mapping challenge", "",
         "Attacking the recovered mapping rather than assuming it. "
         "Findings below are reasons **not** to apply it as-is.", ""]
    blocking = 0

    # ---- 1. agreement with independently assigned CodeDomains -----------------
    agree = disagree = untested = 0
    examples_ok, examples_bad = [], []
    for addr, cls, _slot in rows:
        if len(by_addr[addr]) != 1:
            continue          # linker-folded: no unique class identity to test
        rec = fn.get(addr)
        if not rec or not rec["domains"]:
            continue
        dom = rec["domains"][0]
        if not dom.startswith(("Phyre.", "Bullet.", "EASTL.", "Media.", "SQEX.")):
            continue
        untested += 1
        if toks(cls) & toks(dom):
            agree += 1
            if len(examples_ok) < 5:
                examples_ok.append((addr, cls, dom))
        else:
            disagree += 1
            if len(examples_bad) < 15:
                examples_bad.append((addr, cls, dom))

    L += ["## 1. Agreement with independently assigned CodeDomains", "",
          "For methods GFZ already classified from body evidence, does the RTTI class name "
          "appear in that classification? These are two independent derivations.", "",
          "| Result | Count |", "|---|---:|",
          "| tested (unique-class, named-library domains) | %d |" % untested,
          "| **agree** | **%d** |" % agree,
          "| disagree | %d |" % disagree]
    if untested:
        L.append("| agreement rate | **%.1f %%** |" % (100.0 * agree / untested))
    L.append("")
    if examples_ok:
        L += ["Agreeing samples:", ""]
        for addr, cls, dom in examples_ok:
            L.append("- `%s` RTTI `%s` ⟷ GFZ `%s`" % (addr, cls, dom))
        L.append("")
    if examples_bad:
        L += ["Disagreeing samples (each needs re-derivation — one of the two is wrong):", ""]
        for addr, cls, dom in examples_bad:
            L.append("- `%s` RTTI `%s` ✗ GFZ `%s`" % (addr, cls, dom))
        L.append("")

    # ---- 2. cross-class collisions -------------------------------------------
    multi = {a_: cs for a_, cs in by_addr.items() if len(cs) > 1}
    cross_ns = {}
    for a_, cs in multi.items():
        roots = {c.split("::")[0] for c in cs}
        if len(roots) > 1:
            cross_ns[a_] = cs
    L += ["## 2. Address shared across classes", "",
          "| Kind | Count |", "|---|---:|",
          "| addresses in >1 class | %d |" % len(multi),
          "| ...across different top-level namespaces | **%d** |" % len(cross_ns), ""]
    if cross_ns:
        L.append("Cross-namespace sharing is the suspicious kind. Samples:")
        L.append("")
        for a_, cs in list(cross_ns.items())[:10]:
            L.append("- `%s` → %s" % (a_, ", ".join(sorted(cs)[:4])))
        L.append("")
        blocking += 1

    # ---- 3. method addresses must be real function entries -------------------
    not_entry = [a_ for a_ in by_addr if a_ not in fn]
    L += ["## 3. Method addresses that are not Ghidra function entries", "",
          "| Result | Count |", "|---|---:|",
          "| distinct method addresses | %d |" % len(by_addr),
          "| **not a function entry** | **%d** |" % len(not_entry), ""]
    if not_entry:
        L.append("Samples: " + ", ".join("`%s`" % x for x in sorted(not_entry)[:15]))
        L.append("")
        L.append("These mean the vtable walk over-ran into non-code, or Ghidra has no "
                 "function there. Neither is safe to apply.")
        L.append("")
        blocking += 1

    # ---- 4. slot contiguity ---------------------------------------------------
    bad_slots = []
    for cls, slots in by_vt.items():
        s = sorted(set(slots))
        if s and s != list(range(len(s))):
            bad_slots.append(cls)
    L += ["## 4. Slot contiguity per class", "",
          "| Result | Count |", "|---|---:|",
          "| classes | %d |" % len(by_vt),
          "| non-contiguous slots | %d |" % len(bad_slots), ""]
    if bad_slots:
        L.append("Samples: " + ", ".join("`%s`" % c for c in bad_slots[:10]))
        L.append("")
        L.append("Expected for classes with multiple vtables (multiple inheritance); "
                 "suspicious otherwise.")
        L.append("")

    L += ["---", "", "## Verdict", ""]
    if blocking:
        L.append("**DO NOT APPLY AS-IS** — %d blocking check(s) failed above." % blocking)
    else:
        L.append("No blocking structural defect found. Agreement with independently "
                 "assigned classifications is the load-bearing result; read it above before "
                 "deciding what subset is safe to apply.")
    L.append("")

    with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("wrote %s" % a.out, file=sys.stderr)
    print("agreement %d/%d, cross-ns collisions %d, non-entry %d, blocking %d"
          % (agree, untested, len(cross_ns), len(not_entry), blocking), file=sys.stderr)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
