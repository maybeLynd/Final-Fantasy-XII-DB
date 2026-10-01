"""gr18_astra_incorp.py - incorporate two ACCEPTed ASTRA returns into OPUS's GR-18 record and the GR-18 register cell
(OPUS, 2026-10-01; ASTRA-REQ-OPUS-BTS-INDEX-BINDING-1001, ASTRA-REQ-OPUS-ARD-CALLBACK-WIDTH-1001).
Byte-preserving, idempotent. Prints PATCHED / ALREADY per edit and FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "..", "gr18-reward-edge-reachability-0930", "README.md")
REG = os.path.join(HERE, "..", "..", "OPEN-QUESTIONS.md")
BTS = ("*(Narrowed 2026-10-01, OPUS, on ASTRA's [`bts-index-binding`](../../../_experiments/evidence/bts-index-binding/README.md), "
       "ACCEPTed by SWE2-AUDIT-SPEC ([review](../auditspec-review-bts-index-binding-1001/REVIEW.md)): the 31 `bts_*` zones are "
       "missing resource entries, not empty bound tables. Both shipped namespace-26 arrays name them at the same 31 area "
       "indices. At those indices both namespace-21 ARD slot pairs are NULL. At their field ids all ten namespace-5 script "
       "triples are NULL, and the twelve shipped FSTs hold -1. So their ordinary lookup selects no `.ard`, none of the four "
       "empty-table areas, and no map script. Whether another loading route (manager 0's `0032FCA0` primary carrier) can run "
       "their scripts stays open.)*")
ARD = ("\n\n**The fourth case's observer (OPUS, 2026-10-01).** ASTRA's "
       "[`ard-callback-width`](../../../_experiments/evidence/ard-callback-width/README.md), ACCEPTed by SWE2-AUDIT-SPEC "
       "([review](../auditspec-review-ard-callback-width-1001/REVIEW.md)), re-read by OPUS at the bytes. The `.ard` read "
       "goes to the full 64-bit allocator result: `003EA971` `mov r8, rax` before the `0032E620` call at `003EA97F`. The "
       "request descriptor at `rsp+0x30` keeps only its low half: `003EA976` `mov dword ptr [rsp+0x38], eax`, and its "
       "`+0x10` slot holds the callback `003EA710`. The callback zero-extends its argument (`003EA732` `mov ebp, ecx`) and, "
       "with no other assignment to `rbp`, publishes it as the root `02B5E0C0` (`003EA809`). So a sample of `02B5E0C0` can "
       "never show a buffer at or above 4 GB. A runtime answer has to record the full allocator result at `003EA93E` (`rax`) "
       "or `r8` at `003EA97F`, with the request's identity. Natural placement stays a runtime fact.\n")
REGOLD = ("since the install stores each cached reward row as a 32-bit value (`+0xE70` / `+0xE78`).**")
REGNEW = (REGOLD + " *(Narrowed 2026-10-01, OPUS, on ASTRA's ard-callback-width, ACCEPTed by SWE2-AUDIT-SPEC: the observer must "
          "read the full allocator result (`rax` at `003EA93E` or `r8` at `003EA97F`); the published root `02B5E0C0` keeps only "
          "the low 32 bits, so sampling it cannot answer. The 31 `bts_*` zones' ordinary lookups are NULL (missing entries, "
          "not empty tables), ASTRA's bts-index-binding, ACCEPTed.)*")
E1END = ("which `.ard` is bound while they run, and whether they are enterable.)* |")
EDITS = [
    (REC, E1END, E1END[:-2] + " " + BTS + " |"),
    (REC, None, ARD),     # appended once after the edge-state table
    (REG, REGOLD, REGNEW),
]
fails = 0
for path, old, new in EDITS:
    b = open(path, "rb").read()
    n = new.encode("utf-8")
    if n.strip() in b:
        print("ALREADY", os.path.basename(path)); continue
    if old is None:
        anchor = b"\n## "
        i = b.find(b"| **zero-count / missing descriptor (E1)**")
        j = b.find(anchor, i) if i >= 0 else -1
        if j < 0:
            print("REFUSING: no section after the E1 table"); fails += 1; continue
        b = b[:j] + n + b[j:]
    else:
        o = old.encode("utf-8")
        if b.count(o) != 1:
            print("REFUSING (%d): %s" % (b.count(o), old[:60])); fails += 1; continue
        if path == REG and b"|" in n[len(o):]:
            print("REFUSING: pipe in register cell"); fails += 1; continue
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("PATCHED", os.path.basename(path))
print("FAILS", fails)
sys.exit(1 if fails else 0)
