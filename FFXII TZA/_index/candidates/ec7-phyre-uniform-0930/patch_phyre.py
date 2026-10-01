"""patch_phyre.py MEMBERS_DIR - apply FABLE's closure-source ruling to select_phyre_panimation.py and select_phyre_module.py.
Idempotent: refuses if the old block is not found and the new one is not present."""
import io, os, sys

D = sys.argv[1]
DOC = '''
CLOSURE SOURCES AND ACCOUNTING STATE (FABLE ruling, SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, applied
2026-09-30 by SWE2-EC7). Module identity and evidence accounting are separate properties. The seed and closure
predicate is evaluated IGNORING A status: an A-measured body that passes the same predicate a member passes (seed
slot, or every inbound reference from qualifying bodies) is a closure source for its callees, but it stays A and is
never written as a member (no double accounting). Being A alone never qualifies a body. Without this, re-statusing a
page DOCUMENTED shrank a module family by cascade (2026-09-30: PAnimation -75, PPostProcessing -18). The same holds
for bodies another family declares (FABLE ruling on SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930, point 3): for the
closure a body counts as a module member by the predicate whichever family declared it, but ownership stays with the
declaring family - it is never written here (the collisions are printed). Derived families (accounting-defined) are
never closure inputs here: the predicate does not read any family's membership. Control hook: PHYRE_FAIL=<hex,hex,...> (or
PHYRE_FAIL_FILE=<file of the same>) forces the named bodies to fail the predicate (the ruling's mutation control);
unset in normal runs.'''

OLD_PAN = '''members = {e for e in seeds if e in span and e not in a_set and e not in declared}
allowed = members | bound_templates
rounds = 0
while True:
    grew = set()
    for e in span - members - bound_templates:
        if e in a_set or e in declared or e in icf_foreign: continue'''
NEW_PAN = '''# closure-source rule (see the docstring): the predicate ignores A status; A bodies that pass it are sources, not members
FAIL = {int(x, 16) for x in (os.environ.get("PHYRE_FAIL", "") + "," + (open(os.environ["PHYRE_FAIL_FILE"]).read() if os.environ.get("PHYRE_FAIL_FILE") else "")).split(",") if x.strip()}
blocked = FAIL
members = {e for e in seeds if e in span and e not in blocked}
allowed = members | bound_templates
rounds = 0
while True:
    grew = set()
    for e in span - members - bound_templates:
        if e in blocked or e in icf_foreign: continue'''
OLD_MOD = '''members = {e for e in seeds if e not in a_set and e not in declared}
allowed = members | bound_templates
rounds = 0
while True:
    grew = set()
    for e in eset - members - bound_templates:
        if e in a_set or e in declared or e in icf_foreign: continue'''
NEW_MOD = OLD_MOD.replace("members = {e for e in seeds if e not in a_set and e not in declared}",
    '''# closure-source rule (see the docstring): the predicate ignores A status; A bodies that pass it are sources, not members
# EXCEPT PhyreCore: its predicate has no geography and no namespace segment, so without the A/declared firewall the
# closure runs into game code (sample read 2026-09-30: FFXII movement, battle-menu and 28 KB presentation bodies among
# the +988). Per the ruling a misfit stops that family's admission: PhyreCore keeps the firewall until its predicate
# is repaired (record ec7-phyre-uniform-0930).
FIREWALL = (MODULE == "PhyreCore")
FAIL = {int(x, 16) for x in (os.environ.get("PHYRE_FAIL", "") + "," + (open(os.environ["PHYRE_FAIL_FILE"]).read() if os.environ.get("PHYRE_FAIL_FILE") else "")).split(",") if x.strip()}
blocked = FAIL | ((set(declared) | a_set) if FIREWALL else set())
members = {e for e in seeds if e not in blocked}''').replace(
    "        if e in a_set or e in declared or e in icf_foreign: continue",
    "        if e in blocked or e in icf_foreign: continue")
TAIL = '''    members |= grew; allowed |= grew; rounds += 1
'''
TAIL_NEW = '''    members |= grew; allowed |= grew; rounds += 1
promoted_sources = members & a_set      # qualify ignoring A: closure sources only
collisions = sorted((members - a_set) & set(declared))
members -= a_set
members -= set(declared)                # ownership stays with the declaring family
print("closure sources that are A-measured (qualify, stay A, not members): %d" % len(promoted_sources))
print("predicate members owned by another family (collisions, not written): %d" % len(collisions))
for e in collisions: print("  collision %08X  owned by %s" % (e, declared[e][:60]))
if os.environ.get("PHYRE_SOURCES_OUT"):
    TAB, NL = chr(9), chr(10)
    with open(os.path.join(os.environ["PHYRE_SOURCES_OUT"], "%s-sources.tsv" % NAME.replace(" ", "_")), "w") as _f:
        _f.write("address" + TAB + "role" + TAB + "owner" + NL)
        for e in sorted(promoted_sources): _f.write("%08X" % e + TAB + "A-measured closure source" + TAB + NL)
        for e in collisions: _f.write("%08X" % e + TAB + "predicate member owned elsewhere" + TAB + declared[e] + NL)
'''
for fn, old, new, anchor in (("select_phyre_panimation.py", OLD_PAN, NEW_PAN, '  Usage: python select_phyre_panimation.py [--write]"""'),
                             ("select_phyre_module.py", OLD_MOD, NEW_MOD, 'graph/functions.tsv; needs capstone."""')):
    p = os.path.join(D, fn)
    t = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    t = t.replace("\r\n", "\n")
    if new in t:
        print(fn, "already patched"); continue
    assert t.count(old) == 1, (fn, "old block")
    t = t.replace(old, new)
    assert t.count(TAIL) == 1, (fn, "tail")
    t = t.replace(TAIL, TAIL_NEW)
    assert t.count(anchor) == 1, (fn, "anchor")
    t = t.replace(anchor, anchor[:-3] + DOC.replace("\n", "\n" + ("  " if fn.endswith("panimation.py") else "")) + '"""')
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))
    print(fn, "patched")
