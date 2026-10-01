# BJ-1: actual startup guards — cheapest sufficient method

Question: which of OPUS's 1,681 named local-static guards have completion
tokens at an ordinary idle title screen, and which additional guards have
tokens after one specified save is loaded and the field is idle? Consumer:
OPUS's BJ-1 boot-static partition and its owning CRT/initialization page.

Competing explanations: the device-free replay's 19 constructed guards may
be the full observed title set or a strict subset. Field initialization may
add guards, leave the set unchanged, or catch a construction in progress.
The replay omits device/process state and is not a natural-title positive
control. No universal partition across all boots/saves is proposed.

Method A: reuse EXP124 raw reads before any new session. The valid
title-defaults and readable-pilot spans contain **zero** complete requested
guards or the epoch DWORD. title-full is INVALID and happens to contain three
guard DWORDs; those remain provisional, not semantic closure. The normalized
coverage receipt points to exact raw read indexes and hashes; no recapture of
173 descriptors/defaults. No new review of OPUS's completed census/replay.

Static/dataflow analysis explains the guard/epoch rule and identifies the
population, but cannot supply actual title/loaded-field values. A new analyzer
or invariant proof cannot determine the selected natural initialization path
from missing device/save state. Method B would prove only the imposed path
and its stubs, duplicating the existing bounded replay. It cannot settle this
actual-state proposition. The cheapest sufficient method is therefore C:
two focused read-only snapshots in one otherwise justified, healthy session.
Interactive actions are needed only to obtain the two states; reads require
no input, hook, breakpoint, watchpoint, callback or experimental write.

Reuse runtime_probe.Probe.read, its exact nonzero Lua constant and full-length
read rule. bj1_guard_capture.collect is the scoped 1,681-DWORD seam, not a
runtime platform. Four actual controls reject a crossed inaccessible page,
an unreadable guard, a wrong positive constant and a missing population.
The 1,681 synthetic values verify decoding, including zero, building sentinel
and values outside the prepared completion rule. These are **transport tests
on owned disposable Python memory**, not FF12 instruction execution or new
live-game evidence. A successful collect result remains
COLLECTED_CONTEXT_PENDING; it cannot establish health/title/field by itself.

Failed controls01/02 are INVALID, preserved with their source preimages.
Control02 preserved native ERROR_PARTIAL_COPY(299) while the opened process
was still running. The concrete cause is the Windows venv redirector: a
targeted ownership-only control reports launcher PID80256 and allocation-owner
PID80716. No read against that launcher was repeated. The corrected path uses
the base interpreter and requires its reported allocation-owner PID to equal
Popen.pid before OpenProcess. Controls03/04 then succeeded. This failure has
no downstream FF12 conclusion: none was captured. EXP124 identified FF12 via
the actual process census, not this new Python Popen PID assumption.

## Exact remaining capture prerequisites

Reference: designated vanilla Steam x64 FF12 test instance; executable SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Addresses: the retained bj1-guards.tsv VA list, image base00120000;
epoch01F44850; Lua control01CCD300 bytes19930d0a1a0a. Each read uses the
verified actual module load delta. Retain tool hashes, main-module identity,
environment/module census and mapped-code verification from the existing
qualified session procedure. A matching EXE alone does not prove clean state.

**Not yet prepared:** exact backed-up test-save identifier/hash/slot, field/area,
ordinary load trigger, session/state-proof owner and canonical OPUS acceptance
scope. No guessed save or claim that every one of the replay19 must naturally
be completed at title. This packet does not authorize another menu attempt.
Its consumed setup allowance and unapproved extension persist. A future
eligible capture may piggyback a separately authorized/prepared session.

At title and field: preserve visible state proof, identity/positive read
controls before and after; no debugger; epoch-before, all1,681 DWORDs,
epoch-after, exact raw reads/timestamps and replay annotations. Budget:
3 seconds per snapshot, at most10 seconds explicit scoped override; 1,685
positive/epoch/guard reads plus one failed-null detection control. No polling
loop. An incomplete read/control/budget failure invalidates the capture and
retains the partial raw output. Epoch movement and building/out-of-rule values
are observations, not silently discarded to make a partition pass.

Acceptance: after both captures the designated instance must remain normally
responsive, with no fatal dialog; the state owner supplies before/after state
and session-health proof appropriate to this read-only experiment. CPU
activity, process existence and CloseHandle success are insufficient. The
semantic reducer must retain CONTEXT_PENDING/INVALID until that proof exists.
Check actual trigger/state, not merely simulated input success. A fresh zero
guard means no completed token at that observation; it does not prove that
initialization never ran or can never occur. Token offsets are conditional
sequence observations, not an all-process/lifetime identity guarantee.

Restoration: no memory writes/instruments to undo. Verify read-handle closure,
health, original-save/config hashes and designated-instance exit if this
session owns it; never overwrite real saves/sync progress. Stop/takeover
halts automation without automatic restart. No process is launched by this
module. Return an immutable raw+normalized packet and independently reviewed
OPUS incorporation; no semantic closure from collector readiness.

This is a precise preparation return, **not an executable manual checklist**.
When its missing save/state prerequisites and existing permission conditions
are satisfied, consolidate ordinary player actions with other compatible
prepared questions. The user should run no technical commands.
