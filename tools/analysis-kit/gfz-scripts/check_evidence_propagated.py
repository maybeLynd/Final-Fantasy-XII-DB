#!/usr/bin/env python3
"""check_evidence_propagated.py - did work we ACTUALLY DID reach the documentation?

**THIS IS NOT A COVERAGE TOOL AND MUST NOT BE USED AS ONE.** It takes a hand-written list of
functions whose behaviour a session genuinely established - read the body, settled the mechanism,
fixed the signature - and asks whether that evidence landed somewhere the corpus's own adjudicated
rule can see. The input is the list, and the list is a claim about work done. Adding an address
here that nobody read is falsifying the input, and every number downstream inherits it.

The distinction that makes it safe to run and dangerous to abuse: the failing direction is
*documentation debt*, never *missing citations*. A `MENTION-ONLY` row does not mean "go add a
backtick". It means: we know something about this function that the page does not say, so either
write what we know or drop it from the list.

THE RULE IT MEASURES (SWE2-AUDIT-SPEC, 9efc6221, narrowed 2026-09-17): a function counts when an
EVIDENCE-BEARING page cites it and the citation is strictly INTERIOR, or an entry cite of a body
under 128 bytes. Entry-only cites of larger bodies are mentions by design - that cut is the
anti-padding rule and this tool exists inside it, not around it.

    COUNTED       an evidence-bearing page cites it in a counting form - nothing to do
    MENTION-ONLY  cited, but entry-only on a body >= 128 B, or only on non-bearing pages
    ABSENT        not cited anywhere in the corpus

WORKED EXAMPLE, 2026-09-18, and both halves matter. Of 21 functions one session established, 16
were already COUNTED - including `0051F240`, whose complete body had been re-derived twice
independently and was already anchored in `CONTRACT-coast-down-latch.md`. **Checking first is the
point**: the obvious next move would have been to add a citation that was already there.

The five real gaps were the per-frame group handlers, and the fix was not a citation. What had
been established was their SIGNATURE - each takes one named `ManagerSub0209BE80_*` child - while
the contract's reconstruction sketch wrote them as nullary `Group_003F9F40()`. Writing the
argument types into the contract, each anchored on the instruction that reads it, is the work;
the state change is a side effect of doing it. It also turned up a correction that a citation
never would have: `003FA4E0` WRITES the list head at `+0x2490` (`003FA50E`), where the prose had
it only reading.

A BEARING PAGE IS NOT THE SAME AS A DOCUMENTED ONE, and this bit is easy to get wrong. The gate
page carries `status: DOCUMENTED` but `readiness: SEMANTICALLY IDENTIFIED`, and an explicit
non-bearing `readiness:` VETOES a bearing `status:` on the depth axis - so the narrative page is
correctly non-bearing while its CONTRACT (`readiness: BEHAVIORALLY UNDERSTOOD`) is bearing. The
anchors belong in the contract on the merits anyway: that is the artifact asserting behaviour.
**Never flip a status to move a row here.** The gate page's `SEMANTICALLY IDENTIFIED` is its
owner's honest answer about depth - four of its fifteen groups are read to call shape only.

    python check_evidence_propagated.py
"""
import bisect
import collections
import io
import os
import re
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import progress
import kit_paths as KP

# (address, what this session established about it)
ESTABLISHED = [
    (0x0051F240, "complete body: 2-bit mode, two container paths, id*0x30, lazy rebind"),
    (0x00424080, "Movement->Movement hop; the real transition is one level down"),
    (0x001F4DA0, "ctor zero-fills +0x78..+0x38F as one 0x318 unit"),
    (0x00336710, "caches the BattleUnit at ctx+0xF0 from the slot byte at [ctx+0x108]+0x177"),
    (0x00301AD0, "writes the global 022C17A8; it is read by no other body"),
    (0x003247F0, "fills two STACK pointer arrays at [rsp+0x70], never passed to a call"),
    (0x00189120, "8-byte accessor for BootSingleton01F7F598; 117 callers"),
    (0x002367A0, "third BattleUnit accessor, previously unseeded"),
    (0x00234480, "the binder writes NO back-pointer into the actor record"),
    (0x00236820, "BattleUnit_GetBySlotIndex, the pool accessor"),
    (0x003F8EC0, "receives ManagerSub0209BE80_00A0 as arg1"),
    (0x003F80D0, "receives ManagerSub0209BE80_A0D0 as arg1"),
    (0x003F9F40, "receives ManagerSub0209BE80_57E0 as arg1"),
    (0x003FA790, "receives ManagerSub0209BE80_57E0 as arg1"),
    (0x003FA4E0, "receives ManagerSub0209BE80_57E0 as arg1"),
    (0x00296860, "receives ManagerSub0209BE80_7FB0 as arg1"),
    (0x0028C870, "receives ManagerSub0209BE80_7EA0 by tail jmp"),
    (0x003278D0, "calls the navigation fill helpers; touches nothing in BattleUnit +0x298"),
    (0x003291B0, "BattleLocomotion_ResetPathAndSetTargets; same"),
    (0x0030EFF0, "BattleUnit_SnapshotAndSuspendActionState; same"),
    (0x00236A60, "BattleUnit_ResetStateForReuse; same"),
]

FUNCS = os.path.join(KP.WORK, "graph", "functions.tsv")
sizes, names = {}, {}
for line in io.open(FUNCS, encoding="utf-8", errors="replace"):
    f = line.rstrip("\n").split("\t")
    if len(f) > 2 and len(f[0]) == 8:
        try:
            sizes[int(f[0], 16)] = int(f[2])
            names[int(f[0], 16)] = f[1]
        except ValueError:
            pass
entries = sorted(sizes)

cited_any = collections.defaultdict(set)      # entry -> pages that cite it at all
counting = collections.defaultdict(set)       # entry -> pages that cite it in a COUNTING form

for p in progress.docs(KP.DB):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    bearing = progress.evidence_bearing(t)
    rel = os.path.relpath(p, KP.DB).replace("\\", "/")
    for h in re.findall(r"`(?:0x)?(0[0-9A-Fa-f]{7})`", t):
        v = int(h, 16)
        i = bisect.bisect_right(entries, v) - 1
        if i < 0 or not (entries[i] <= v < entries[i] + sizes[entries[i]]):
            continue
        e = entries[i]
        cited_any[e].add(rel)
        if bearing and (v != e or sizes[e] < 128):
            counting[e].add(rel)

print("%-10s %-6s %-14s %s" % ("addr", "size", "state", "what this session established"))
print("-" * 110)
gaps = []
for va, what in ESTABLISHED:
    sz = sizes.get(va, 0)
    if counting.get(va):
        state = "COUNTED"
    elif cited_any.get(va):
        state = "MENTION-ONLY"
        gaps.append((va, sz, what, sorted(cited_any[va])[:2]))
    else:
        state = "ABSENT"
        gaps.append((va, sz, what, []))
    print("%08X   %-6d %-14s %s" % (va, sz, state, what[:62]))

print()
print("=== the only rows that warrant action ===")
if not gaps:
    print("  none - every function this session established is already carried in a counting form")
for va, sz, what, where in gaps:
    print("  %08X (%d B) %s" % (va, sz, names.get(va, "")))
    print("      established: %s" % what)
    print("      cited on   : %s" % (", ".join(where) if where else "nothing"))
