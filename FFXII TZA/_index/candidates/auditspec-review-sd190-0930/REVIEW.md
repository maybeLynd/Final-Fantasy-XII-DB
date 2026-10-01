# REVIEW: sd190-tween-turn-bit-0930

- **Package:** `sd190-tween-turn-bit-0930` (OPUS, commit `8de16e58c`)
- **Task:** `OPUS-REQ-AUDITSPEC-SD190-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS author maybeLynd)
- **Verdict: ACCEPT**

## Controls re-run

`sd190_tween.py` re-executed: `rerun_sd190_tween.out` text-identical to committed `.out`
(CRLF only), T1–T6 PASS, `FAILS 0`. (Commit message says T1–T5; README/script carry T6 —
cosmetic only.)

## Independent verification (capstone, certified image `73461d08…21f8`)

- **T1** — `003E6A70`: `call 003E6E60` → null-guard → `lea rcx,[rbx+0x550]` → tail `jmp
  003AEF50`. Exact.
- **T2** — `003AEF50` list walk verified instruction-for-instruction: head `[rcx+0x18]`, next
  `[r8+0x48]`; per node `movzx ecx,[r8+1]` → `cmove` sets bit 0 iff byte+1 nonzero;
  `cmp byte[r8+2],0; cmove` sets bit 1 iff byte+2 nonzero. Exactly the claimed OR-of-two-flags.
- **T3** — `003AED70` allocator: scans a **128-slot, 0x60-stride** pool (`cmp edx,0x80` /
  `add rcx,0x60`) for `byte[rcx]==0`; on allocation writes `word [rcx]=0x0101` (bytes +0/+1
  set) and `byte [rcx+2]=1`. Then `003AEEA0` loop clears `byte [rax+1]` on every existing node
  of the object's list — "a new turn supersedes an old one" verified.
- **T4** — `003AEF90` stepper: `003AF098 cmp byte [rbx+2],0` gates the move phase
  (`mulss [rbx+0x30]/[rbx+0x34]/[rbx+0x38]` scaled vector accumulated into translation output
  `[r14]..[r14+8]`; cleared at `003AF104` when its count expires); `003AF123 cmp byte
  [rbx+1],0` gates the turn phase (angle stepped into rotation output `[r15]`; cleared at
  `003AF1EC`). Two-phase reading exact.
- **Callers (raw rel32 + jcc + absolute-qword census over .text/all sections):**
  - `003AED70` ← `{003E6589 ∈ 003E6340, 003E6677 ∈ 003E65E0}` — exactly the two claimed.
  - `003AEF90` ← `{003AF239 ∈ 003AF220}` — the single caller claimed.
  - `003E6A70` ← `{0025E35A ∈ 0025DF00}` — the single caller claimed.
  - `003AEF50` ← `{003E6A95}` tail-jump only. No stored pointers for any of the four — no
    indirect-call path exists.
- **Pool reachability:** the node pool base cell `02B3F530` has exactly 4 rip refs — the
  allocator's load (`003AED85`) and `003AF2B4`/`003AF2D4`/`003AF2E0` in `003AF220`'s region.
  Nothing else addresses the pool directly.
- **Command 0x1A:** the authored-command page's table line 96 lists `0x1A → 00422D50 +
  003E6340` — "move and turn toward the target along profile n", matching T3's caller claim.

## Limits

- "Every writer of node byte+1" is bounded by reachability, not an image-wide taint: the pool
  base cell's 4-ref census shows only the allocator/stepper family touches the pool, and node
  byte+1 writes go through the object list — reachable only via the tween object pointer. No
  counterexample found; residual is stated, not hidden.
- The integrator's third-argument floats are not traced back to `003AEF90`'s output — the
  record's own limit stands.

**Verdict: ACCEPT** — all six controls reproduce; every load-bearing instruction, caller set
and the 0x1A-handler identification independently verified on the certified image.
