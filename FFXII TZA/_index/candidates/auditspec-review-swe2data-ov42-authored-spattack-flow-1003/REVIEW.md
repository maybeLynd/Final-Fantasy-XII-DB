# SWE2-AUDIT-SPEC review: SWE2-DATA OV-42 authored getspattackskillinfo → spattackread flow

Reviewer: SWE2-AUDIT-SPEC (a Claude stand-in subagent for the rate-limited Devin session; it never worked the
SWE2-DATA lane) · 2026-10-03 · Task: `SWE2DATA-REQ-AUDITSPEC-OV42-AUTHORED-FLOW-1003` · Record:
`_index/candidates/swe2data-ov42-authored-spattack-flow-1003/` (commit `c77a50981`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The loop path (flow B) meets H1 under the record's stated premises. For the init path (flow A), "cannot statically
establish" (H2) is the correct finding: `029B` runs whether or not the init `029A` wrote anything.

## SWE2-AUDIT-SPEC independent re-derivation

**Script.** I extracted all 9 copies of `spc_z0000.ebp` from `FFXII_TZA.vbf` myself. They are byte-identical
(sha256 `616f885d0ecd…`, 3,008 bytes). I then read the raw bytes with my own linear decode, with code at file +80h:

- **Descriptor dwords** are each present once in the table: `4100000C` at file 4A4h, `41000010` at 4ACh, `41000018`
  at 4CCh, `4100001C` at 4D4h and `11000015` at 4BCh. The class byte is 1 (`file`). The 24-bit offsets are 0Ch, 10h,
  18h and 1Ch (s32), and 15h for var3.
- **Flow A** (image `0x470..0x4AD`):
  - `PUSHII 0; POPV 3`, then seven debug `PUSHII/PUSHDBG/DVAR` triples;
  - then `PUSHP 1; PUSHP 0; CALLPOPA 029A`;
  - the result goes to A and is not tested.
- **Flow B** (image `0x605..0x627`):
  - `PUSHP 6; PUSHP 5; CALL 029A; OPNOT; POPV 3`;
  - then `PUSHV 5; POPV 0; PUSHV 6; POPV 1`;
  - then `PUSHII 3,1,1; REQEW`.
- **Reader** (image `0x71B..0x747`):
  - `PUSHV 3; OPNOT; POPXNCJMP(5Ch) L2`;
  - then an inner one-shot block gated on var4 (`PUSHV 4 == 0`) that calls `0151(0)`/`0152(0)` and sets var4 = 1;
  - then `PUSHV 1; PUSHV 0; CALLPOPA 029B; RET` (0x747).
- **Raw call bytes:** `58 9A 02` appears at image 0x60B, the `029A` operand at 0x4AE, and the `029B` operand at 0x745.

**Native, from the shipping image:**

- **`00348330` (029A bridge):**
  - The context comes from one `2640C0` call (`rbx`).
  - The first pop (stack top = the second PUSHP = var5 in flow B, var0 in flow A) goes through `2650B0(ctx, …)` into
    RSI, then RDX: the **action** destination.
  - The second pop goes through `2650B0` with the same ctx into RCX: the **unit** destination.
  - It then calls `309C00(rcx, rdx)`. The action store comes before the unit store, as the queue-output-alias review
    records.
- **`002650B0`:** the class is `(desc >> 24) & 7`. The table at `00265180`, decoded, sends class 1 to `002650FC`,
  which returns `[ctx+40h] + (desc & FFFFFFh)`.
  - So var5 and var6 (and var0 and var1) are one shared base +18h/+1Ch (+0Ch/+10h), and RCX − RDX = +4 exactly.
  - They are byte-disjoint, so both values survive the ordered stores.
- **`00348870` (029B bridge):** first pop (var0) → EBX → EDX = **action**; second pop (var1) → ECX = **unit**; then
  `30EEA0`.
- **`00267E10`:** tag 1 returns the raw dword. PUSHV on an s32 cell loads a whole dword with tag 1 when bit 27 is
  clear (table arm `00268040`). So every load is word-preserving, which matches the interpreter-transfer review.

## SWE2-AUDIT-SPEC reproduction

`prove_spattack_flow.py` re-run from the repository root:

- exit 0, `FAILS 0`;
- stdout identical to the committed `prove_spattack_flow.out` (34 PASS lines);
- the regenerated `result.json` is equal to the committed one;
- the six synthetic controls (overlapping unit cell, `local`-home unit cell, s16 action cell, extra writer in
  `PC00`, swapped loop pushes, removed reader guard) each make their named check refuse.

## SWE2-AUDIT-SPEC notes (no correction required)

- The reader also has an inner one-shot block gated on var4, set to 0 at `0x4BC` before `REQEW(2)` and to 1 at
  `0x73B`. It does not change the var3 guard or the `029B` pushes, and both flows still reach `029B`.
- This premise is load-bearing for flow B: var3 = `!result` means the reader runs only when the same iteration's
  `029A` returned non-zero. "Returned 1 ⇒ both outputs written" holds only for non-null destinations (`309C00`
  guards each pointer).
- Flow A's input state (queue `022C2178` at init), native writers outside the bytecode, the image buffer versus the
  queue globals, and the meaning of action word 0 all stay OPEN, as the record says.
