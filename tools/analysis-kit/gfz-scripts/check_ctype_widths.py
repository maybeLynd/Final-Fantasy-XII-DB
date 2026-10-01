#!/usr/bin/env python3
"""check_ctype_widths.py - when a field's ctype names a declared type, the width must agree.

229 field rows in the store give their ctype as the name of another declared type. That is a
checkable claim and nothing was checking it: if a row says its ctype is `PWorldMatrix` and
`PWorldMatrix` is 48 bytes, the row had better be 48 bytes wide, or be a pointer to one.

WHAT IT FOUND ON ITS FIRST RUN, 2026-09-19 (OPUS): fourteen rows whose ctype named a declared
type of 24 to 56 bytes while the row itself was exactly EIGHT bytes. All fourteen are pointers
whose `*` did not survive the reflection import - the schema records a member's TYPE, and the
pointer marker was dropped.

  THE CASE THAT SETTLES THE CLASS: `PComponent +0x000  m_next : PComponent`, an 8-byte field
  whose declared type is its own 24-byte class. A struct cannot embed itself. That one is a
  pointer beyond argument, and the other thirteen share its shape exactly - width 8, a declared
  type far larger, and a name that reads as a link (m_entity, m_firstComponent, m_worldMatrix,
  m_localToWorldMatrix, m_destination, m_targetWorldMatrix).

THE PARSE IS THE EASY PART TO GET WRONG, and this got it wrong once before being written down:
`ActorStorageRecord*[4]` is FOUR POINTERS, 32 bytes, and reads as a mismatch against
ActorStorageRecord's 7,040 bytes if the `*` is only stripped from the end of the string. The
marker sits BEFORE the subscript. PartyRosterSlots +0x000 is correct and was briefly reported as
a defect.

A ROW IS ACCEPTED WHEN:
  * ctype is `T`        and width == sizeof(T);
  * ctype is `T*`       and width == 8;
  * ctype is `T[n]`     and width == n * sizeof(T);
  * ctype is `T*[n]`    and width == n * 8;
  * or ctype does not name a declared type at all, which this check says nothing about.

WHAT THIS GATE DOES NOT OWN, learned by duplicating it. A first version also enumerated ctypes
naming an UNDECLARED type and called that a finding. `check_type_refs.py` already did exactly
that, and frames it better: "references OUT to middleware: 6 names, 53 rows - A BOUNDARY, NOT A
GAP", separating a reference that leaves the store from one that dangles inside it (of which
there are none). The count is still printed here as context; the enumeration belongs there.

AND THE WITHDRAWAL THAT FOLLOWED. On the strength of "every use has the same width" this tool's
author declared VPMatrix4 (64), VPMatrix4x3 (48) and UD3D11_DEPTH_STENCILOP_DESC (16), and added
pointer markers to twelve PClassDescriptor* rows. ALL OF IT WAS REVERTED WITHIN THE HOUR:

  * AUDIT-LOG 2026-09-17 had already dispositioned those exact six names as "genuinely external"
    middleware with no counterpart in this image. Declaring them crossed a standing boundary.
  * AUDIT-LOG 2026-09-19 warns, about these exact types, that delta-based sizing gave VPString
    "8, 24 and 88" and that "modal-voting would have produced confident wrong sizes for exactly
    the engine types that have no other evidence". Taking the width every row records is close
    enough to that method to be caught by the same warning.
  * The pointer markers rested on reading the class-descriptor contract's 0x100+ layout as the
    size of PClassDescriptorBase. That contract describes the descriptor the CONSTRUCTOR builds;
    PClassDescriptorBase is a different name whose size this database does not establish, and an
    8-byte base carrying only a vtable pointer is perfectly possible.

The width check against DECLARED types is sound and is what found the fourteen genuine pointer
defects in 8a8a8aab8. Everything past that boundary was someone else's settled question.

usage: check_ctype_widths.py [--db <root>]
"""
import argparse
import csv
import io
import os
import collections
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

SUB = re.compile(r"^(?P<base>[^\[\]]+?)(?P<ptr>\**)\s*(?:\[(?P<n>\d+)\])?$")
TYPEISH = re.compile(r"^[A-Z][A-Za-z0-9_]{3,}$")
NOT_A_TYPE = {"UNRESOLVED", "UNKNOWN", "PROVEN", "TYPE", "HIGH", "DISCOVERED"}
PTRW = 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=G.DB)
    a = ap.parse_args()

    tr = list(csv.reader(io.open(os.path.join(a.db, "_types", "types.tsv"),
                                 encoding="utf-8", newline=""), delimiter="\t"))
    sizes = {}
    declared = {r[0] for r in tr[1:] if r}
    for r in tr[1:]:
        if r and len(r) > 1 and r[1].lower().startswith("0x"):
            try:
                sizes[r[0]] = int(r[1], 16)
            except ValueError:
                pass

    rows = list(csv.reader(io.open(os.path.join(a.db, "_types", "fields.tsv"),
                                   encoding="utf-8", newline=""), delimiter="\t"))
    checked = 0
    bad = []
    sized_by_arg = 0
    for r in rows[1:]:
        if len(r) < 9:
            continue
        m = SUB.match((r[4] or "").strip())
        if not m:
            continue
        base = m.group("base").strip()
        if base not in sizes:
            # SIZED-BY-ARGUMENT (SWE2-FRONTIER ruling, OPUS-REQ-TEAM-CTYPE-FOR-SIZED-WIDGET,
            # 2026-09-19): a type the store DECLARES but whose size column is UNRESOLVED -
            # Widget, whose size is a construction argument over 26 values - is spelled as
            # the bare ctype and THE ROW'S OWN WIDTH CARRIES THE EXTENT. No equality check
            # is possible, but the row is still checkable twice over: a `*`/`T*[n]` form is
            # a pointer and is 8 bytes like any other, and a bare/`T[n]` form must carry a
            # positive width or the row asserts an extent nobody recorded. Previously these
            # fell into the "references OUT" bucket below, conflating a governed spelling
            # with a dangling name - which is exactly how a widget embedded in a container
            # read as unrecognisable to tools.
            if base in declared and TYPEISH.match(base) and base not in NOT_A_TYPE:
                n = int(m.group("n")) if m.group("n") else 1
                try:
                    got = int(r[2])
                except ValueError:
                    got = -1
                if m.group("ptr"):
                    if got != PTRW * n:
                        bad.append((r[0], r[1], r[4].strip(), got, PTRW * n,
                                    "pointer"))
                elif got <= 0:
                    bad.append((r[0], r[1], r[4].strip(), got, -1,
                                "sized-by-argument: the row must carry the extent"))
                else:
                    sized_by_arg += 1
                checked += 1
            continue
        checked += 1
        n = int(m.group("n")) if m.group("n") else 1
        unit = PTRW if m.group("ptr") else sizes[base]
        want = unit * n
        try:
            got = int(r[2])
        except ValueError:
            continue
        if got != want:
            bad.append((r[0], r[1], r[4].strip(), got, want,
                        "pointer?" if got == PTRW * n and unit != PTRW else ""))

    # AND THE GAP THIS GATE SHIPPED WITH. It compares only against types the store DECLARES, so a
    # ctype naming an UNDECLARED type is invisible to it - which is how twelve rows typed
    # `PClassDescriptorForClassDescriptor` and `PClassDescriptorBase` at 8 bytes survived the
    # first pass. They were the same missing-pointer defect as the fourteen it did catch, and the
    # only reason it missed them is that neither type was in types.tsv. A dangling ctype is
    # therefore reported too: it cannot be width-checked, and not being checkable is the finding.
    dangling = collections.Counter()
    dwhere = {}
    for r in rows[1:]:
        if len(r) < 9:
            continue
        m = SUB.match((r[4] or "").strip())
        if not m:
            continue
        base = m.group("base").strip()
        if base in declared or not TYPEISH.match(base) or base in NOT_A_TYPE:
            # `base in declared` now covers BOTH branches the tuple key used to separate:
            # declared-with-size is width-checked above, and declared-but-UNRESOLVED is the
            # sized-by-argument rule above it. What remains here is genuinely OUT.
            continue
        dangling[base] += 1
        dwhere.setdefault(base, (r[0], r[1], r[4].strip(), r[2]))

    print("field rows whose ctype names a declared type : %d" % checked)
    print("rows whose width disagrees with that type    : %d   <- the finding" % len(bad))
    print("  sized-by-argument rows accepted            : %d   (declared type, UNRESOLVED size;"
          " the row's own width is the extent)" % sized_by_arg)
    print()
    for t, off, ct, got, want, hint in bad:
        print("  %-32s %-8s %-28s %6d  expected %-6d %s" % (t, off, ct, got, want, hint))
    if not bad:
        print("  none - every ctype that names a type is consistent with its own width")
    print()
    print("ctypes that reference OUT of the store: %d distinct, %d row(s)"
          % (len({k[0] for k in dangling}), sum(dangling.values())))
    print("  NOT ENUMERATED HERE. check_type_refs.py already owns this and frames it better -")
    print("  \"references OUT to middleware ... a boundary, not a gap\" - and it distinguishes a")
    print("  reference that leaves the store from one that dangles inside it. Run that one.")
    print()
    print("A `pointer?` hint means the row is exactly 8 bytes while the named type is larger:")
    print("almost always a missing `*` rather than a wrong offset. Confirm from an instruction")
    print("before changing it - a self-referencing field settles it on its own, since a struct")
    print("cannot embed itself.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
