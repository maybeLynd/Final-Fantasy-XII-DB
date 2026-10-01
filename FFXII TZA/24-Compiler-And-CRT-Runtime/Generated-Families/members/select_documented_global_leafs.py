#!/usr/bin/env python3
"""select_documented_global_leafs.py - frontier NativeLeaf bodies whose single RIP-relative
target is a global a bearing page already names.

Request: FABLE-REQ-SWE2-EC7-GLOBAL-LEAF-ACCESSORS.

    "B rows for frontier NativeLeaf accessors of DOCUMENTED game globals: each member's class
     explanation is the documented global / field it reads, writes, tests or addresses."

A body qualifies when ALL of these hold:

  1. census tag contains `NativeLeaf`, body is neither A-measured nor already declared;
  2. the body has exactly ONE distinct RIP-relative memory target inside .rdata or .data
     (targets into .text are code, not globals; bodies with no data target - every Member*
     form, which works through `this` - stay frontier for lack of a static base, as do
     multi-target bodies the spec's "single rip target" clause does not cover);
  3. that target is cited VERBATIM (8-hex token) on an evidence-bearing page - the spec's
     "exact address" arm.  The "base + documented offset" arm is deliberately NOT claimed by
     this selector: a scan cannot tell `*(B)+off` pointer-target documentation (where B+off as
     a static address is an unrelated neighbour - e.g. the manager-pointer block
     01F7F4C0..01F82D00 on game-application.md, where 01F82CB8+8 is just the next slot) from a
     true embedded-struct field.  Uncited-but-adjacent targets are counted and stay frontier.

Access kind is read off the touching instruction(s): lea -> addr; a write-shape store or
read-modify-write (mov [T],reg / or|and|xor|add [T],.. / lock) -> write; test|cmp|bt -> test;
otherwise read.

The members TSV carries one row per member:
    entry <TAB> census-form <TAB> kind <TAB> target <TAB> owning-page(s)
so each member's per-global explanation is recorded next to its address, which is what the
task's "per-member 'global -> owning page' column" asks for.

Controls printed at the end:
  - frontier denominator and the three-way split (bound / uncited-single / not-single-or-none);
  - leftover census by reason, incl. near-cited uncited singles (<0x40 below a cite) kept out
    as proximity, not binding;
  - every member target re-checked against the citation index (positive control).
"""
import bisect
import collections
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(10):
    if os.path.isdir(os.path.join(ROOT, "Database", "FFXII TZA")):
        break
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as cd  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

DB = os.path.join(ROOT, "Database", "FFXII TZA")
WORK = os.path.join(ROOT, "Database", "Tools", "work")
EXE = os.path.join(WORK, "exe", "FFXII_TZA.exe")
OUT = os.path.join(HERE, "documented-global-leaf-accessors.tsv")

CITE8 = re.compile(r"(?<![0-9A-Za-z_])(?:0x)?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
RIP = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
MD = Cs(CS_ARCH_X86, CS_MODE_64)


def sections(exe):
    pe = struct.unpack_from("<I", exe, 0x3C)[0]
    n = struct.unpack_from("<H", exe, pe + 6)[0]
    o = pe + 0x18 + struct.unpack_from("<H", exe, pe + 0x14)[0]
    out = {}
    for i in range(n):
        name = exe[o + i * 40:o + i * 40 + 8].rstrip(b"\0").decode()
        vs, va, rs, rp = struct.unpack_from("<IIII", exe, o + i * 40 + 8)
        out[name] = (0x120000 + va, 0x120000 + va + vs, rp)
    return out


def main():
    exe = open(EXE, "rb").read()
    sec = sections(exe)
    t_lo, t_hi, t_raw = sec[".text"]
    rd_lo, rd_hi = sec[".rdata"][:2]
    d_lo, d_hi = sec[".data"][:2]

    def toff(va):
        return va - t_lo + t_raw

    def in_data(t):
        return rd_lo <= t < rd_hi or d_lo <= t < d_hi

    def secname(t):
        return ".rdata" if rd_lo <= t < rd_hi else ".data"

    sizes = cd.load_functions()
    a_set = cd.measure_a(DB, sizes)[0]
    declared = set()
    for doc, parts in cd.parse_families(DB):
        if len(parts) >= 5 and parts[1] in cd.LETTERS:
            if parts[2].endswith("documented-global-leaf-accessors.tsv"):
                continue   # own family: stay re-runnable after publication
            try:
                declared.update(cd.read_members(doc, parts[2]))
            except (IOError, OSError, ValueError):
                pass

    # verbatim 8-hex citations on evidence-bearing pages only
    cites = collections.defaultdict(set)
    for p in cd.docs(DB):
        text = io.open(p, encoding="utf-8", errors="replace").read()
        if not cd._bearing(text):
            continue
        rel = os.path.relpath(p, DB).replace("\\", "/")
        for m in CITE8.finditer(text):
            v = int(m.group(1), 16)
            if in_data(v):
                cites[v].add(rel)
    cited_sorted = sorted(cites)

    frontier = []
    for line in io.open(os.path.join(WORK, "graph", "functions.tsv"),
                      encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        try:
            a = int(p[0], 16)
        except ValueError:
            continue
        tag = p[8] if len(p) > 8 else ""
        if "NativeLeaf" in tag and a not in a_set and a not in declared:
            form = [x for x in tag.split(";") if "NativeLeaf" in x][0]
            frontier.append((a, sizes[a], form.replace("GFZ.V121.CodeDomain.", "")))

    WRITE = ("mov", "or", "and", "xor", "add", "sub", "lock", "bts", "btr", "btc")
    members, leftovers = [], collections.Counter()
    near_cited = []
    for a, size, form in sorted(frontier):
        touch = []   # (mnemonic, is_store, target)
        tgts = set()
        for ins in MD.disasm(exe[toff(a):toff(a) + size], a):
            m = RIP.search(ins.op_str)
            if not m:
                continue
            t = ins.address + ins.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            if in_data(t):
                tgts.add(t)
                # "dword ptr [rip + x], reg" is a store; "reg, dword ptr [rip + x]" a load
                store = bool(re.match(r"(?:\w+ ptr )?\[rip", ins.op_str))
                touch.append((ins.mnemonic, store, t))
        if not tgts:
            leftovers["no static rip target (member-field / register forms)"] += 1
            continue
        if len(tgts) > 1:
            leftovers["more than one data rip target"] += 1
            continue
        T = next(iter(tgts))
        if T not in cites:
            leftovers["single rip target is an undocumented global"] += 1
            i = bisect.bisect_right(cited_sorted, T) - 1
            if i >= 0 and T - cited_sorted[i] < 0x40:
                near_cited.append((a, T, cited_sorted[i]))
            continue
        kind = "addr"
        for mn, store, _t in touch:
            if mn == "lea":
                kind = "addr"
            elif (store and (mn.split()[0] in WRITE or mn.startswith("set"))
                    or mn.startswith(("or", "and", "xor", "lock"))):
                # setcc [rip+T] is a byte store, not a read (AUDITSEM contra DGLA-SETCC-KIND)
                kind = "write"
            elif mn in ("test", "cmp", "bt", "bts", "btr"):
                kind = "test" if kind != "write" else kind
            elif kind == "addr":
                kind = "read"
        members.append((a, form, kind, T, sorted(cites[T])))

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# frontier NativeLeaf bodies whose single .rdata/.data rip target is a global\n")
        f.write("# cited verbatim on the owning page listed in the last column.\n")
        f.write("# FABLE-REQ-SWE2-EC7-GLOBAL-LEAF-ACCESSORS\n")
        f.write("address\tform\tkind\ttarget\towning-page\n")
        for a, form, kind, t, pages in members:
            f.write("%08X\t%s\t%s\t%08X\t%s\n" % (a, form, kind, t, "|".join(pages)))

    print("frontier NativeLeaf bodies: %d" % len(frontier))
    print("members (bound, exact cite): %d over %d distinct targets" %
          (len(members), len({m[3] for m in members})))
    for reason, n in leftovers.most_common():
        print("  leftover %4d  %s" % (n, reason))
    print("  of the uncited singles, %d sit <0x40 above a cited address - proximity," % len(near_cited)
          + " NOT binding (manager-pointer-block adjacency class)")
    bad = [m for m in members if m[3] not in cites]
    assert not bad, "member whose target is not cited: %s" % bad[:3]
    # Count guard: the declared row count at the last reviewed re-run. 196 at declaration (2026-09-17); the row
    # then moved by A-drift removals to 211 without a re-run. 222 = 211 + 12 frontier admissions - 1 drop
    # (003DE970: the page citing its target is now REOPENED, not evidence-bearing), applied under FABLE family
    # ruling R3 (SWE2-EC7, 2026-09-29, _index/candidates/ec7-family-ruling-exec-0929). The predicate is unchanged.
    # 224 = 222 + 2 frontier admissions on the repaired frontier, applied under R3 (SWE2-EC7, 2026-09-30,
    # _index/candidates/ec7-f-shape-pass-0930). The predicate is unchanged.
    # 230 = 224 - 1 since measured A + 7 frontier admissions after OPUS e2cb21305 re-statused the render-record array
    # page (its exact global cites bind 7 more leaves), under R3 (SWE2-EC7, 2026-09-30, ec7-dd-adrift-pairing-0930 round 4).
    # 230 again = 230 - 1 since measured A + 1 re-admission (the field runtime pass, whose exact cite binds it, is
    # DOCUMENTED again after OPUS 56a49cc8c), A-drift round 5 (OPUS for SWE2-EC7, 2026-10-01, opus-adrift-round5-1001).
    # 223 = 230 - 7 since measured A: the map-screens page went DOCUMENTED (owner batch 21) and its exact global cites
    # make the seven leaves it binds individually explained (OPUS for SWE2-EC7, 2026-10-01, opus-dd-restatus-21-1001).
    assert len(members) == 223, "member count drifted: %d" % len(members)
    print("OK: %d members -> %s" % (len(members), os.path.basename(OUT)))


if __name__ == "__main__":
    main()
