#!/usr/bin/env python3
"""check_named_not_cited.py - functions a document names in prose and never cites by address.

Why this exists
---------------
On 2026-09-03 the pair census reported an offset as **still uncompared** when a document had in fact
compared its two touchers at length. The document named both functions **in pseudocode**, by name, and
cited **no address inside either** -- so every instrument in this project was blind to it.

> **A document that names a function without citing it is invisible to every instrument here.**

Adding two interior anchors cleared **two** frontier rows at once. Measured across the corpus
afterwards: **426 named-but-uncited mentions in 82 documents.**

This is the read-but-uncited mode one step earlier. The other checker asks *"was this function's body
opened?"*; this asks *"did the document that talks about it say where it is?"*

What it is NOT
--------------
**Not a defect list.** A document may legitimately mention a function it is not documenting -- *"the
same helper the other document reads"* is a reference, not a claim, and needs no anchor.

**The signal is repetition.** A name mentioned once without an address is a passing reference; a name
mentioned repeatedly, or many distinct names in one document, is a document whose subject matter is
unreachable from its text.

So it ranks by **count per document** and exits 0.

**This checker can be satisfied dishonestly, and that is its most important limit.**
`functions.tsv` will supply an address for every name in this list in one pass. Pasting them in
clears the tool completely.

> **An address supplied from a name lookup is a transcription, not a citation.** A bulk anchor
> **asserts a reading nobody made** -- and the checker goes quiet while the document becomes *less*
> honest, because a cited address reads as evidence that someone opened the body.

**Anchor only names you have read.** Leave the rest listed, and say in the document which is which:
the gap then stays visible instead of being papered over by the tool that found it.

> **A checker measures what it can see; satisfying it is not the same as fixing what it points at.**

**The failure this checker cannot see at all** (found 2026-09-03 by `repos-78`, in a sentence that
*did* cite an address): a document wrote *"a save is in progress"* on the strength of the ledger name
`SaveWrite_GetBusyFlag`. The function is seven bytes -- read one global, return. **What had been read
was "a global is non-zero"; what had been written was "a save is in progress."** The call site was
anchored; the callee was never opened.

> **An anchor on the caller does not vouch for a claim about the callee.**

This checker asks *did the document say where this is*. `check_located_not_read.py` asks *did anyone
open the body*. **Neither asks whose body a claim actually rests on**, and that is the question the
defect above was. No instrument here answers it.

Only ledger-named functions are considered -- a `FUN_xxxxxxxx` mention *is* an address.

Usage
-----
    python check_named_not_cited.py --db "Database/FFXII TZA"
    python check_named_not_cited.py --self-test
"""
import argparse
import collections
import io
import os
import sys

import check_located_not_read as C

MIN_NAME = 12          # short names collide with ordinary prose


def scan(db, entries, sizes, names):
    # **A name that maps to two addresses fails differently in every tool that assumes it maps to
    # one.**  In this corpus that is not hypothetical: a seeding routine's name is carried by BOTH a
    # 5-byte thunk and its body, and that one collision has already produced a false "zero callers"
    # (a query against the body while the call graph indexed the thunk) and a wrong anchor (a bulk
    # fix writing the body's address onto the thunk's row).
    #
    # So a name keeps **every** entry that carries it, a mention counts as cited when **any** of them
    # is cited, and an ambiguous name is **reported as ambiguous** rather than resolved arbitrarily.
    # **Whatever an arbitrary resolution reports is arbitrary.**
    by_name = collections.defaultdict(set)
    for e, n in names.items():
        if n and not n.startswith("FUN_") and len(n) >= MIN_NAME:
            by_name[n].add(e)
    rows = []
    for root, _d, files in os.walk(db):
        parts = os.path.relpath(root, db).split(os.sep)
        if "_inbox" in parts or parts[0].startswith("_"):
            continue                     # staging and the shared index are not documents
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            cited = {int(h, 16) for h in C.cited_addresses(t)}
            for nm, ee in by_name.items():
                if nm not in t:
                    continue
                if any(e <= a < e + sizes[e] for e in ee for a in cited):
                    continue          # any one of the name's addresses counts as cited
                rows.append((rel, nm, sorted(ee)))
    return rows


SELF_NAMES = {0x1000: "BattleStats_DoSomethingLong", 0x2000: "BattleUnit_OtherLongName"}
SELF_SIZES = {0x1000: 100, 0x2000: 100}


def self_test(tmp):
    d = os.path.join(tmp, "nc_db", "00-Cat")
    if not os.path.isdir(d):
        os.makedirs(d)
    io.open(os.path.join(d, "a.md"), "w", encoding="utf-8").write(
        "BattleStats_DoSomethingLong is described at length and never located.\n"
        "BattleUnit_OtherLongName at `00002000` is cited properly.\n")
    rows = scan(os.path.join(tmp, "nc_db"), [0x1000, 0x2000], SELF_SIZES, SELF_NAMES)
    if len(rows) != 1 or rows[0][1] != "BattleStats_DoSomethingLong":
        print("SELF-TEST FAILED: %r" % rows)
        return 1
    print("self-test ok: flags the named-but-uncited function, silent on the cited one")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        import tempfile
        return self_test(tempfile.mkdtemp())
    if not a.db:
        return ap.error("--db required unless --self-test")

    entries, sizes, names, _vendor = C.load(C.FUNCS)
    rows = scan(a.db, entries, sizes, names)
    if not rows:
        print("every ledger-named function mentioned in prose is also cited by address")
        return 0

    by = collections.defaultdict(list)
    amb = 0
    for rel, nm, ee in rows:
        by[rel].append((nm, ee))
        if len(ee) > 1:
            amb += 1

    print("NAMED IN PROSE, NEVER CITED BY ADDRESS")
    print("A document that names a function without citing it is invisible to every instrument here.")
    print("**Suspicions, not defects** - a passing reference needs no anchor. The signal is how many.")
    print("")
    print("  DO NOT BULK-ANCHOR THESE. functions.tsv will supply every address below in one pass and")
    print("  clear this tool completely. An address supplied from a name lookup is a TRANSCRIPTION,")
    print("  not a citation - it asserts a reading nobody made, and a cited address reads as evidence")
    print("  that someone opened the body. Anchor only what you have read; leave the rest listed and")
    print("  say in the document which is which.\n")
    print("  %d mention(s) across %d document(s), %d of them AMBIGUOUS\n"
          % (len(rows), len(by), amb))
    if amb:
        print("  An AMBIGUOUS name is carried by more than one function - a thunk and its body, most")
        print("  often. Anchoring one of them is correct; resolving arbitrarily is how a bulk fix")
        print("  writes the body's address onto the thunk's row.")
        print("  Measured image-wide: 57 duplicated names - 53 a thunk plus its own body, 1 a thunk")
        print("  chain, 3 compiler artifacts. NO engine function shares a name with a different")
        print("  engine function. Sizes are printed so the thunk is visible. WHICH to anchor depends")
        print("  on the question: the BODY for what it does, the THUNK for what calls it, the union")
        print("  followed transitively for reachability.\n")
    for rel in sorted(by, key=lambda r: -len(by[r]))[:a.top]:
        print("  %3d  %s" % (len(by[rel]), rel))
        for nm, ee in sorted(by[rel])[:3]:
            # Sizes are printed for an ambiguous group because they separate the thunk from the
            # body without this tool asserting a classification: a thunk is a handful of bytes.
            # Measured image-wide: **57 duplicated names, 53 of them a thunk plus its own body,
            # one a thunk chain, and 3 genuinely distinct -- all three compiler artifacts.**
            # **No engine function shares a name with a different engine function.**
            tag = ("%08X" % ee[0]) if len(ee) == 1 else (
                "AMBIGUOUS: " + " ".join("%08X(%dB)" % (x, sizes.get(x, 0)) for x in ee))
            print("           %-52s %s" % (nm[:52], tag))
        if len(by[rel]) > 3:
            print("           ... %d more" % (len(by[rel]) - 3))
    return 0


if __name__ == "__main__":
    sys.exit(main())
