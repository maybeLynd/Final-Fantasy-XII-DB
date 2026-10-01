#!/usr/bin/env python3
"""test_uc1_band_readers.py -- the UC-1 band applies across every own `load_functions`
reader, and ONLY to the shared census.

OPUS-REQ-DATA-UC1-POPULATION-READERS: the 2026-09-28 series break moved the
scorer population to 34,269 listed + 795 UC-1 frontier (696 from the 1-64 B
band + 99 from the 65-256 B band); the 257-up band (2026-09-29,
OPUS-REQ-DATA-UC1-READERS-257-UP) adds 1 = 796 frontier, 35,065. Every reader that walks its own
functions.tsv loader must see the same corrected set, while a reader pointed
at a fixture/other TSV loads exactly what it names.

T1-T14 live-tree checks assert the band on the shared census; T15-T17 assert
the realpath guard refuses to band a fixture.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")
BAND = uc1_band.load()
FRONTIER = set(BAND["frontier"])
REMOVED = set(BAND["removed"])
EXTEND = dict(BAND["extend"])
POP_NF = 34269 + len(FRONTIER)   # 35,065 - non-funclet listed + frontier
POP_FN = 38160 + len(FRONTIER)   # 38,956 - funclet-keeping listed + frontier
AUTHORED = 28660 + len(FRONTIER) # program_coverage's authored subset

passed = []


def ok(name, cond, detail=""):
    if cond:
        passed.append(name)
        print("PASS %s" % name)
    else:
        print("FAIL %s  %s" % (name, detail))
        raise SystemExit(1)


def has_frontier_members(container_entries):
    return all(e in container_entries for e in list(FRONTIER)[:5])


def no_removed(container_entries):
    return not (REMOVED & set(container_entries))


# --- T1-T14: live-tree, shared census --------------------------------------

import actor_field_scan  # noqa: E402
f = actor_field_scan.load_functions(actor_field_scan.FUNCS)
ok("T1 actor_field_scan banded", len(f) == POP_NF and
   has_frontier_members(set(f)) and no_removed(set(f)), str(len(f)))

import arg_extent_scan  # noqa: E402
f = arg_extent_scan.load_functions()
ok("T2 arg_extent_scan banded", len(f) == POP_FN and
   has_frontier_members(set(f)) and no_removed(set(f)), str(len(f)))

import audit_crossrefs  # noqa: E402
f = audit_crossrefs.load_functions(FUNCS)
ent = {int(k, 16) for k in f}
ok("T3 audit_crossrefs banded", len(f) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(f)))
e0 = "%08X" % next(iter(FRONTIER))
ok("T3b audit_crossrefs frontier unclassified",
   f[e0]["classified"] is False and f[e0]["owner"] == "")

import check_chain_rederivation  # noqa: E402
f = check_chain_rederivation.load_functions(FUNCS)
ok("T4 check_chain_rederivation banded", len(f) == POP_FN and
   has_frontier_members(f) and no_removed(f), str(len(f)))

import check_extent_overruns  # noqa: E402
rows = check_extent_overruns.load_functions(check_extent_overruns.FUNCS)
ent = {e for e, _, _ in rows}
sizes = {e: s for e, _, s in rows}
ok("T5 check_extent_overruns banded", len(rows) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(rows)))
ok("T5b extended sizes applied",
   all(sizes[e] == en - e for e, en in EXTEND.items()))

import check_interior_anchors  # noqa: E402
rows = check_interior_anchors.load_functions()
ent = {e for e, _, _ in rows}
sizes = {e: s for e, s, _ in rows}
ok("T6 check_interior_anchors banded", len(rows) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(rows)))
ok("T6b extended sizes applied",
   all(sizes[e] == en - e for e, en in EXTEND.items()))

import check_literal_base_access  # noqa: E402
ents, ends, meta, _b = check_literal_base_access.load_functions(
    check_literal_base_access.GRAPH)
ok("T7 check_literal_base_access banded", len(ents) == POP_FN and
   has_frontier_members(set(ents)) and no_removed(set(ents)), str(len(ents)))
ok("T7b extended ends applied",
   all(ends[e] == en for e, en in EXTEND.items()))

import globals_index  # noqa: E402
f = globals_index.load_functions(KP.WORK)
ent = {int(k, 16) for k in f}
ok("T8 globals_index banded", len(f) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(f)))

import imagebase_refs  # noqa: E402
f = imagebase_refs.load_functions()
ok("T9 imagebase_refs banded", len(f) == POP_FN and
   has_frontier_members(set(f)) and no_removed(set(f)), str(len(f)))

import rtti_challenge  # noqa: E402
f = rtti_challenge.load_functions(FUNCS)
ent = {int(k, 16) for k in f}
ok("T10 rtti_challenge banded", len(f) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(f)))

import verify_doc_addresses  # noqa: E402
f = verify_doc_addresses.load_functions(verify_doc_addresses.DEFAULT_FN)
ent = {int(k, 16) for k in f}
ok("T11 verify_doc_addresses fns banded", len(f) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(f)))
rows = verify_doc_addresses.load_ranges(verify_doc_addresses.DEFAULT_FN)
ent = {e for e, _, _ in rows}
ok("T12 verify_doc_addresses ranges banded", len(rows) == POP_FN and
   has_frontier_members(ent) and no_removed(ent), str(len(rows)))
st = next(iter(FRONTIER))
c = verify_doc_addresses.containing(rows, st)
ok("T12b interior citation resolves frontier body",
   c is not None and c[0] == st and c[1] == BAND["frontier"][st])

import widget_messages  # noqa: E402
f = widget_messages.load_functions(widget_messages.FUNCS)
ok("T13 widget_messages banded", len(f) == POP_NF and
   has_frontier_members(set(f)) and no_removed(set(f)), str(len(f)))

import program_coverage  # noqa: E402
f = program_coverage.load_functions(KP.WORK)
gen = {k for k, v in f.items() if v["generated"]}
thunks = {k for k, v in f.items() if v["thunk"]}
authored = set(f) - gen - thunks
ent = {int(k, 16) for k in authored}
ok("T14 program_coverage banded", len(f) == POP_FN and
   len(authored) == AUTHORED and has_frontier_members(ent) and
   no_removed({int(k, 16) for k in f}), "%d/%d" % (len(f), len(authored)))


# --- T15-T17: the guard refuses to band a fixture --------------------------

FIXTURE = os.path.join(HERE, "_fixture_uc1_funcs.tsv")
with io.open(FIXTURE, "w", encoding="utf-8", newline="") as fh:
    fh.write("entry\tname\tbody_bytes\towner\tfinal_no_owner\ttags\tthunk\n")
    fh.write("00123456\tFUN_00123456\t32\tSYS\tfalse\t\tfalse\n")
    fh.write("007EE7F0\tFUN_007EE7F0\t9\tSYS\tfalse\t\tfalse\n")
try:
    f = actor_field_scan.load_functions(FIXTURE)
    ok("T15 fixture unbanded (actor_field_scan)",
       len(f) == 2 and 0x007EE7F0 in f, str(len(f)))
    f = audit_crossrefs.load_functions(FIXTURE)
    ok("T16 fixture unbanded (audit_crossrefs)",
       len(f) == 2 and "007EE7F0" in f, str(len(f)))
    f = verify_doc_addresses.load_functions(FIXTURE)
    ok("T17 fixture unbanded (verify_doc_addresses)",
       len(f) == 2 and "007EE7F0" in f, str(len(f)))
finally:
    os.unlink(FIXTURE)

print("self-test: %d case(s) passed" % len(passed))
