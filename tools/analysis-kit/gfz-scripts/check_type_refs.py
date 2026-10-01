#!/usr/bin/env python3
"""Every type name the store's own `ctype` column names must be a type the store declares.

A field whose `ctype` is `BattleStatsRecord*` or `SteeringRecord[2]` is a reference from
one store row to another. Nothing checked those references resolved, and the first run
found one of mine: `BattleTargetBuffer +0x008` was declared as `BattleTargetEntry[32]`
while `BattleTargetEntry` was never declared at all. A layout that points at a type
nobody wrote is a dead end for anyone rebuilding from the store.

Middleware is reported separately rather than as a failure. Phyre and D3D types
(`VPString`, `PClassDescriptorBase`, `UCD3D11_*`) legitimately live in their SDKs and
not in this database, so naming them in a ctype is a reference OUT of the store, not a
broken reference inside it. The split matters: one is work to do, the other is a
boundary to record.

It also reports the scalar spelling conventions in use. The column currently carries
three - `uint32`, `u32`, and bare `int`/`short` - which is worth knowing about and is
NOT worth mass-rewriting: a reader understands all three, and churning hundreds of rows
to unify a spelling would bury the evidence columns in diff noise for no recovered fact.

    check_type_refs.py
"""
import collections
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA", "_types")

LONG = {"uint8", "int8", "uint16", "int16", "uint32", "int32", "uint64", "int64",
        "float", "double", "void", "char", "bool", "wchar_t", "byte"}
SHORT = re.compile(r"^(u|i|s|f)\d+$")
BARE = {"int", "short", "long", "unsigned", "signed"}
SKIP = {"UNRESOLVED", "options", "ptr"}
# A reference to a middleware SDK type is a reference OUT of this database.
FOREIGN = re.compile(r"^(VP|PClassDescriptor|UCD3D11_|UD3D11_|CD3D11_|D3D11_)")
IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ARRAY = re.compile(r"\[\s*\d*\s*\]$")


def base_of(ctype):
    """`SteeringRecord[2]` -> `SteeringRecord`; `BattleStatsRecord*` -> `BattleStatsRecord`.

    Trailing digits are part of the NAME, not an array bound - stripping them turns
    `uint16` into `uint` and `VPMatrix4` into `VPMatrix`, which is how the first draft
    of this check invented fourteen dangling references that did not exist.
    """
    b = ARRAY.sub("", ctype.strip()).strip()
    return b.rstrip("*").strip()


def main():
    types = set()
    tp = os.path.join(DB, "types.tsv")
    for n, line in enumerate(io.open(tp, encoding="utf-8")):
        if n and line.strip():
            types.add(line.split("\t")[0])

    refs = collections.defaultdict(list)
    conv = collections.Counter()
    fp = os.path.join(DB, "fields.tsv")
    for n, line in enumerate(io.open(fp, encoding="utf-8")):
        if not n:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 5:
            continue
        b = base_of(c[4])
        if not b or not IDENT.match(b):
            continue
        if b in LONG:
            conv["long (uint32)"] += 1
            continue
        if SHORT.match(b):
            conv["short (u32)"] += 1
            continue
        if b in BARE:
            conv["bare C (int)"] += 1
            continue
        if b in SKIP:
            continue
        refs[b].append((c[0], c[1], c[4]))

    inside = sorted((k, v) for k, v in refs.items() if k not in types and not FOREIGN.match(k))
    outside = sorted((k, v) for k, v in refs.items() if k not in types and FOREIGN.match(k))
    ok = sorted(k for k in refs if k in types)

    print("TYPE REFERENCES FROM THE ctype COLUMN")
    print("  resolved to a declared type : %d name(s)" % len(ok))
    if ok:
        print("      %s" % ", ".join(ok))
    print("  references OUT to middleware: %d name(s), %d row(s) - a boundary, not a gap"
          % (len(outside), sum(len(v) for _, v in outside)))
    for k, v in outside:
        print("      %-36s x%d" % (k, len(v)))
    print()
    print("  scalar spellings in use: %s"
          % ", ".join("%s %d" % (k, n) for k, n in sorted(conv.items())))
    print("  three spellings is not an error and is deliberately not normalised - see the"
          "\n  module docstring.")
    print()
    if not inside:
        print("  DANGLING references inside the store: 0")
        return 0
    print("  DANGLING references inside the store: %d" % len(inside))
    for k, v in inside:
        print("    %-32s x%-3d e.g. %s %s declared as %s" % (k, len(v), v[0][0], v[0][1], v[0][2]))
    print("\n  A ctype naming a type the store does not declare is a dead end for anyone")
    print("  rebuilding from it. Declare the type or change the ctype; do not leave it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
