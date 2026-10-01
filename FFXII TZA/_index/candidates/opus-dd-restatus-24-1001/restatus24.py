"""restatus24.py - owner re-status batch 24 (OPUS, 2026-10-01): the largest-unclassified page. Its "still unknown" lines for
rows the register has since closed get dated pointers to the answers, and the page moves PARTIAL -> DOCUMENTED.
Byte-preserving, idempotent; PATCHED / ALREADY per edit, FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "99-Unresolved-Residual", "Largest-Unclassified-Code", "the-largest-unclassified-functions.md")
N = " *(OPUS owner read 2026-10-01: answered since - %s.)*"
BI1 = "BI-1 is the render-model subresource-variant binding system, register row BI-1"
EDITS = [
    ("**What it DOES is still unknown.** **BI-1.**", "**What it DOES is still unknown.** **BI-1.**" + N % BI1),
    ("**What the machine models is still unknown. BI-2.**",
     "**What the machine models is still unknown. BI-2.**" + N % "BI-2 is superseded into BI-1 (the same machine), and BI-1 is answered"),
    ("**What it is a state machine *for* is still unknown**, and that is the honest limit.",
     "**What it is a state machine *for* is still unknown**, and that is the honest limit." + N % BI1),
    ("none has been decoded. **BI-1** stands.", "none has been decoded. **BI-1** stands." + N % BI1),
    ("**What chain A computes over that sub-block is still unknown — BI-1 stands** —",
     "**What chain A computes over that sub-block is still unknown — BI-1 stands** —" + N % BI1 + " —"),
    ("is not established** (`SD-121`; 2026-09-30, SWE2-DATA:",
     "is not established** (`SD-121`, answered 2026-09-30: the script-assigned effect-actor slots; 2026-09-30, SWE2-DATA:"),
    ("**Still unknown:** what any of it *holds*. **BI-8** narrows to:",
     "**Still unknown:** what any of it *holds*." + N % "BI-8 is the per-manager table of script-requested event-effect loads, and BI-11 the engine's typed effect and presentation handles" + " **BI-8** narrows to:"),
    ("**What the buckets hold is still unknown.** This does not answer BI-8;",
     "**What the buckets hold is still unknown.**" + N % "BI-11, the engine's typed handles for effect and presentation objects, one class per kind" + " This does not answer BI-8;"),
    ("original scan did not match. **Untested. BI-12.**",
     "original scan did not match. **Untested. BI-12.**" + N % "BI-12 is answered no: none of the ten operations writes the region by any addressing mode"),
    ("status: PARTIAL — what the packed-id bucket registry family holds (BI-11) is answered 2026-09-27 (OPUS);",
     "status: DOCUMENTED — every register row the page names is answered and its stale 'still unknown' lines point to the answers (owner re-status 2026-10-01, OPUS, batch 24); what the packed-id bucket registry family holds (BI-11) is answered 2026-09-27 (OPUS);"),
]
fails = 0
b = open(P, "rb").read()
for old, new in EDITS:
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", old[:50]); continue
    if b.count(o) != 1:
        print("REFUSING (%d): %s" % (b.count(o), old[:60])); fails += 1; continue
    b = b.replace(o, n); print("PATCHED", old[:50])
if not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
