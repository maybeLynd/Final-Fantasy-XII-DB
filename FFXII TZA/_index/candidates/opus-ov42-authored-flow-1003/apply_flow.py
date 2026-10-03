"""apply_flow.py [--apply] - OPUS consumes SWE2-DATA's authored getspattackskillinfo -> spattackread flow (c77a50981),
ACCEPTed by SWE2-AUDIT-SPEC (c5f35fc3c), on the OPUS-led calling-convention page: one new section placing the shipped
flow against the page's two-out-reference precondition (OPUS, 2026-10-03; ASTRA-REQ-OPUS-OV42-AUTHORED-FLOW-CONSUME-1003).
Additive and idempotent; the page's EOL is kept."""
import io
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CC = "01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md"
C = "../../_index/candidates/"

SECTION = """
## The shipped 029A -> 029B flow against that precondition (OPUS, 2026-10-03)

From SWE2-DATA's record [`swe2data-ov42-authored-spattack-flow-1003`](""" + C + """swe2data-ov42-authored-spattack-flow-1003/README.md)
(`c77a50981`), ACCEPTed by SWE2-AUDIT-SPEC's independent review
([REVIEW](""" + C + """auditspec-review-swe2data-ov42-authored-spattack-flow-1003/REVIEW.md), `c5f35fc3c`). OPUS re-read
both bridges and the class-1 reference decoder at the bytes
([`flow_check.py`](""" + C + """opus-ov42-authored-flow-1003/flow_check.py), 16 checks, FAILS 0). The script side rests on
SWE2-DATA's `prove_spattack_flow.py` and the reviewer's own decode, and is not repeated.

- **The sites.** SWE2-DATA's census found three call sites in `spc_z0000.ebp`, the same in each of its nine
  byte-identical language copies. The census is discovery only: no count or absence claim rests on it.
- **Bridge order.**
  - `getspattackskillinfo` (`029A`, bridge `00348330`): its first pop (the stack top, the later PUSHP) decodes to
    RDX, the **action** destination. Its second pop decodes to RCX, the **unit** destination. Both decodes use the
    one context read from `002640C0`.
  - `spattackread` (`029B`, bridge `00348870`): its first pop goes to EDX (the action word) and its second to ECX
    (the unit).
- **The cells.** Every reference involved is file class: class byte 1, decoded at `002650FC` as `[ctx + 0x40]` plus
  the 24-bit offset. All are `s32`: var0 / var1 at `+0x0C` / `+0x10`, and var5 / var6 at `+0x18` / `+0x1C`. Each
  `029A` call's two outputs are 4 bytes apart and byte-disjoint, so the precondition above holds for them.
- **Loop path: holds (H1) under premises.**
  - The script runs `PUSHP 6; PUSHP 5; CALL 029A; OPNOT; POPV 3`, then copies var5 to var0 and var6 to var1 as whole
    tag-1 dwords.
  - The reader calls `029B` only when var3 is 0, that is, when the same iteration's `029A` returned non-zero.
  - Premises: valid non-NULL cells, the private normal-return ABI, the shared context and load, and no interference.
    The writer `00309C00` guards each pointer, so "returned 1 means both outputs were written" holds only for
    non-NULL destinations.
- **Init path: cannot be established statically (H2).**
  - The script runs `PUSHP 1; PUSHP 0; CALLPOPA 029A` and does not test the result.
  - var3 stays 0, so the first `029B` can consume the image's initial zeros in cells `+0x0C`..`+0x14` when the queue
    is empty.
- **OPEN, as SWE2-DATA states them:**
  - the initial queue order (`022C2178` at init);
  - native writers of these cells outside the bytecode;
  - allocation, non-aliasing and lifetime of the image buffer against the queue globals;
  - the meaning of action word 0.
"""


def main(apply):
    p = os.path.join(DB, CC)
    t = io.open(p, encoding="utf-8", newline="").read()
    key = "## The shipped 029A -> 029B flow against that precondition (OPUS, 2026-10-03)"
    if key in t:
        print("SKIP", CC)
        return 0
    nl = "\r\n" if "\r\n" in t[:2000] else "\n"
    nt = t.rstrip("\r\n") + nl + SECTION.replace("\n", nl)
    if apply:
        io.open(p, "w", encoding="utf-8", newline="").write(nt)
    print("APPLY" if apply else "WOULD", CC)
    return 0


if __name__ == "__main__":
    print("FAILS %d" % main("--apply" in sys.argv))
