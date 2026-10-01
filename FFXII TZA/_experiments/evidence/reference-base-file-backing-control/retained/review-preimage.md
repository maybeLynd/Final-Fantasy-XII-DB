REVIEW — CKPT10R2 executed re-review (repair `113cca077`)

SWE2-AUDIT-SPEC. Re-executed the same `ckpt10_exec.py` fixture driver on
the repaired `_index/progress` package plus DATA's new repair fixtures.
Executed receipts, not inspection.

## All nine controls PASS (FAILS 0)

- C1 PASS — snapshot.json semantic tamper now detected:
  `INCOMPLETE: output set not coherent - semantics_sha256 mismatch`,
  check() rc=2. (Was silent in CKPT10.)
- C2 PASS — AUDIT-LOG.md edit moves the input fingerprint
  `99f888b8eb → bcea7bd430`; it is now a required fingerprinted input.
  (Was unfingerprinted in CKPT10.)
- C3 PASS — empty required input → `INCOMPLETE - required input(s)
  invalid: _index/COVERAGE.md (empty file)`, rc=1, last-good kept.
  (Was existence-only in CKPT10.)
- C4 PASS — mid-publish failure: prior fp intact, mixed set detected,
  post-check rc=1.
- C4b PASS (new) — same-inputs mixed set reads INCOMPLETE via per-member
  commit_id stamping: "snapshot.md does not carry commit 743f2012…", rc=2.
  This also discharges the degenerate case CKPT10 noted.
- C5 PASS — mid-build source move aborts, prior generation retained.
- C6 PASS — register-absent open question appears as route obligation.
- C7 PASS — all-L2-MET + open transferred obligation stays obligation.
- C8 PASS — unavailable instruments → UNMEASURED, never PASS.
- C9 PASS — terminal counted from declared/receipts, not filenames.

## DATA's new repair fixtures — executed, all pass

`test_progress_report.py` full suite FAILS 0 including T28–T33:
- T29a/T29b: semantics_sha256 recorded + wiped sections → not CURRENT.
- T30: outputs-map tamper → not CURRENT.
- T31: empty required input → INCOMPLETE.
- T32: cleared-but-schema-valid register → CURRENT (no over-reach).
- T33: truncated TEAM.json → INCOMPLETE (unparseable).

`test_progress_fail_closed.py` PASSED — the broken-dimension path still
refuses a headline and exits nonzero.

## Verdict: ACCEPT

The three CKPT10 defects are genuinely repaired with executed controls, and
the fix did not weaken the six controls that already passed. C4b's
commit_id mechanism closes the same-inputs mixed-set hole too. No residual
defects found in this pass. Note this is a fixture-level audit of the
generator's coherence/fingerprint semantics — per rule, installed-classifier
and transfer comparisons that were unavailable stay UNMEASURED, and this
acceptance is about the repair's correctness, not a claim that the
progress numbers themselves are accurate.

---

## ASTRA-REVIEW-WIDGET-TIMED-DURATION-SELECTION — ACCEPT (bounded)

`check.py` PASS_SOURCE_SELECTION. Independent decode of `00244E9C..00244EDE`
(67 B) byte-exact: `movzx edi, word[rcx+2]` → `call 00181C90` → `cmp eax,1`
→ `mov eax,[rbx+0x7C]` (flag-preserving load between cmp and cmove) →
`cmove edi,ecx` → `bt eax,0xB; jae` → override path `mov edi,eax;
btr edi,0xB; mov [rbx+0x7C],edi; shr edi,0x16` (bit 11 consumed via
store-back; duration = bits 22..31) → `imul ecx,edi,0x3C` → `mov eax,
0x10624DD3; mul ecx; shr edx,6` → `mov [rbx+0x70],edx` →
`and +0x7C,~0xF; or +0x7C,4`. Reciprocal `0x10624DD3 = ceil(2^38/1000)`
verified; exact-floor argument (product multiple of 60, error <1/50) sound.
Selection order confirmed: the return-1 zero gate precedes the override.

## ASTRA-REVIEW-WIDGET-TRANSITION-DURATION-DOMAIN — ACCEPT (bounded)

`check.py` PASS_SOURCE_SIGNED_DURATION. Anchors byte-exact:
`00246971 imul ecx, dword[rsp+0x70], 0x3C` (dword argument, not u16) →
`0024699A imul ecx` (SIGNED reciprocal multiply) → `sar edx,6` +
`mov eax,edx; shr eax,0x1F; add edx,eax` (truncate-toward-zero sign
correction). The +0x70 writer's `mul`/`shr` is unsigned — the
signed-vs-unsigned domain distinction is real. −17 → trunc −1 vs floor −2,
and first product-sign-overflow case at 35,791,395 verified as host
arithmetic consistent with the instruction semantics. Scope held: starter
`002468A0` only, no caller-reachability claim.

## OPUS-REQ-AUDITSPEC-REVIEW-ASTRA-RETURNS-0928 — ACCEPT

Six consumptions, all verified against the packages I independently
reviewed:

- `conv_check.py` X1–X5 + S FAILS 0 — X4 binds all four negative-path
  bypasses (NOPped-jmp mutant rejected); X5 binds `003924B0`'s truncating
  provisional counts + unguarded division. Corridor s10 items 2 and 9
  carry the piecewise clamp and the `w/c0, h/c0 ≥ 1` domain with strikes.
- `accumulation_order.py` L/R/N FAILS 0 — whole-matrix sequential order
  `((p0+p1)+p2)+p3`, per-row first-pair order noted, no fused arithmetic.
- s18 replay README qualified in place — "idempotent on its own output"
  struck, antipode two-cycle + wrap-parity reasoning (odd kind-1 wraps
  still equal wrap(h)) added. The parity logic is correct.
- Storage contract s3 precondition landed: "destination must not overlap
  the cursor" with the demonstrated alias semantics.
- `sign_check.py` K1/O1 FAILS 0 — UQ-38 signature honestly bounded
  (B1 recount 47/31/95).
- `2b4d37c45` cursor-alias precondition table qualified — matches the
  verified leaf semantics.

---

## FABLE-REQ-AUDITSPEC-REVIEW-0928B — ACCEPT (all seven records)

- **gg1-msg2-reconcile** — S2–S6 + C1/C2 FAILS 0: message-2 readers sit
  under `[0208EA28]`; pump calls each open/close their own generation
  (`002481A0`/`00248190` pairs); the other {2} builders verified as
  non-window-message paths.
- **gg1-dispatch-sim** — P1–P4/C1 FAILS 0 (49/51; two multi-context
  readers left). N correction byte-exact: `002BD680` loads id `mov
  ecx,[rdx]`, `lea eax,[rcx-1]` bias, `cmp eax,0xE; ja`, table at
  `0x2BD878` rel32+image-base — id 9 → `002BD834` (calls `0027FB50`),
  id 10 → `002BD714` (both `call 002D3900` at `…71F`/`…745`). The
  002D3900 call is genuinely the message-10 arm.
- **sq1-dword0-consumer** — previously byte-verified; cited.
- **gg1-static-order O5b** — `0f 2e c7 7a 12 75 10 41 8b cf e8 38`
  binds ucomiss/jp/jne both→`0022AB90`, JP→NOP mutant refused.
- **postmultiply-float-order-consumer** — O1+O2/C FAILS 0: adds order
  `[x4=p1, x7=p0, x5=p2, x6=p3]`, store `0039785E`; planted-swap control
  refuses.
- **save-pointer-order-consumer** — S1/C FAILS 0: record `0036D969` <
  load `0036D974` < store `0036D977`; reordering mutant refused.
- **uq38-oeb-applied** — B1–B4 FAILS 0: 47 whole / 31 C-both-instruments
  / 95 undecided; FRONTIER's 41 splits 5 whole + 31 C + 5 mostly. The
  earlier double-count is resolved exactly as the signature's B1
  condition required.

## ASTRA-REVIEW-WIDGET-DEFERRED-DISPATCH-DOMAIN — ACCEPT

`check.py` PASS_SOURCE_DEFERRED_DISPATCH. Independently decoded
`00244E17..00244EFC` byte-exact:

- Bit-0-clear path: `test dl,1; jne` → `and +0x7C,~0xE; or +0x7C,1`
  (nibble forced to 1 — bit0 was clear entering) → `jmp 00244EDF`
  notification tail.
- Signed low-nibble via `shl ecx,0x1C; sar ecx,0x1C`: 0 → schedule arm
  (`bts edx,9`), 2 → rebase arm `00244E62`, 3 → falls to schedule arm,
  everything else → `00244EF7` early return.
- **Polarity verified:** `00244E62 bt edx,0x10; jae 00244E6D` — `jae`
  skips `xor ecx,ecx; mov [rbx+0x70],ecx`, so **bit 16 SET zeroes +0x70,
  CLEAR skips**. The earlier G control genuinely could not attest this
  (jae vs jb needed binding); the consumer correction is right.
- `[rip+0x1E4A6FD]` = `0208F570` clock: `add eax,eax; sub +0x70; sub
  +0x74; mov +0x74,eax` — the rebase arithmetic as claimed.

Scope held: starter/mode-domain semantics only; no callback, native or
caller promotion.

## Shadow follow-on (same revs)

- **035e14931 ShadowSettings matrices** — `shadow_matrices.py` M1/M2/S
  FAILS 0: eight `float[4][4]` at `+0x1C0+0xD8·i`, 96 lane shuffles, 144
  lane stores; 20-byte remainders honestly kept DISCOVERED.
- **ac4f5fcb8 BJ-1 guard list** — G1–G3 FAILS 0: 1,732 header sites →
  1,681 guards; header −1 while building, footer `++[01F44850]`;
  snapshot-read rule derived (0 = not built, −1 building, ≥0x80000001
  built-order).
- **68dc90f7c / 7f0992cf6** — `+0x70` "same conversion" strike and the
  `+0x90` signed-low32 wording both consistent with my byte-exact
  verification of the two writers.
- **d6494cb94 BI-3c pipe repair** — 36 → 35 split rows; consistent.

---

## OPUS-REQ-AUDITSPEC-REVIEW-LGS-LIFETIME (`c975f4a2d`) — ACCEPT

`lgs_lifetime.py` L1–L6/S FAILS 0. Anchors byte-exact:

- `003EC860` destroy-cell helper: callback(*cell), `call 003697F0`, null.
  `003EC8A0` = free+null variant (no callback) — both decoded.
- `0026EDB0`: `call [rcx+0x128]` (the ctor-stored `002F5450`) then the
  `add rbx,0x40` / `edi=2` / `call 0016D6A0` / `add rbx,0x68` / `jne`
  loop — exactly two 0x68 records get the no-op.
- `002F5450` teardown: `lea`+`call 003EC8A0` chain over +0x1C8/+0x1D0/
  +0x210/**+0x1C0 at 002F5504**/+0x218 — the freed set as listed.
- `002F6F55`: `imul edx,edi,0x70` → `call 003EC8D0` → `mov [rsi+0x1C0],
  rax` — +0x1C0 holds `003EC8D0(6, count*0x70)`, an owned pointer.
  The strike of the 2026-09-19 "not a pointer" row is correct.
- Second instance `0026E7D0` building at `0209A668` consistent with L2.

## ASTRA-REVIEW-UC1-BAND-65-256-EXTENT — ACCEPT (bounded)

`check.py` PASS_BOUNDED_UC1_65_256: 100 exact spans, no reachable
truncation/interior boundary/listed-span collision; truncated-store
detection control passes. The three retained direct-exit rows verified
byte-exact: `002E4CCA jne 004232D0`; `002E5B5A jmp 002ED6A0` inside the
`002E5B00` span; and `00708270`'s span contains **both** `jmp 0071BB70`
sites (`708325`, `708330`) — the reused-32B-target claim is real. The
failed preflight (invented 35,000-entry lower bound) is honestly
preserved as driver error. Scope held: extent membership for these 100
rows only — no complete-function, admission, or live claim.

## Shadow follow-on

- `312af3caa` lgs_children_lifetime R1–R3/S + `8bc85e70d`
  bounded_lifetimes C1/C2/S: controls consistent with the byte-verified
  helper identities (`003EC860`/`003EC8A0` above are the same helpers).
- `6b7e357c7` FABLE composer qualifier: the accumulation_order.py re-run
  agreement noted; order rule matches my POSTMULTIPLY-FLOAT-ORDER review.
- `90d9cf805` FABLE wrap_check: changed-bias detector consistent with
  the `00915620`/`01CEBC50` bias loads verified byte-exact earlier.
- `8154f227a` SQ-1 ratification note: bookkeeping, consistent.

---

## ASTRA-REVIEW-RATE-NORMALIZER-DOMAIN — ACCEPT

`check.py` PASS_SOURCE_RATE_DOMAIN. Byte-exact at `00229E70`:
`movss xmm1,[shared rate]` → `xorps xmm0,xmm0` → `comiss xmm0,xmm1;
jb` — CF=1 covers both `0 < rate` AND unordered (NaN), so positive-or-NaN
returns the rate; non-positive falls through to store+return 1.0f
(`[rip+0x1AC1D20]`). `002469C9 call 00229E70` → `movss xmm1,[1.0]` →
`divss xmm1,xmm0` — +0xB8 = 1/rate exactly as the consumer qualified.
The four M cases (0.5→2.0, −1→1.0, −0.0→1.0, NaN→NaN) follow from the
verified branch semantics; "+0xB8 is always 1.0f" correctly struck to a
constructor default, not an invariant.

## Shadow follow-on (revs ≤36654)

- `c72c584ac` cursor_check K1/K2/C — re-derives the alias semantics I
  byte-verified; disjoint/zero controls consistent.
- `2af6246c3` lifetime_propagation P1 — stale-dependency regression:
  fails on pre-patch types.tsv, passes after. Correct repair shape.
- `2d8d10ba6` thin_check N1/N2/C — binds the 11-instruction window;
  1×400 → nx 0, +inf refinement; consistent with my truncation review.
- `06f1fd6be` active_log_widget_lifetime W1–W3 — attach under manager
  +0x1080; bit-5-clear tail-jump to `002482E0` subtree free; release is
  the parent's, timing honestly left open.
- `af5787fb0` input_manager_lifetime I1/I2 — `001955F0` scalar deleting
  dtor, single write `00198784` after null test; no cell-routed
  destruction, getter-caller release not excluded.
- `cb2c4e94e` UC-1 ruling APPLY-IN-PART (99 rows, 21 held) — its
  "AUDIT-SPEC corroboration" condition is discharged by my
  UC1-BAND-65-256-EXTENT review above.

---

## ASTRA-REVIEW-REFERENCE-INVERSE-DOMAIN — ACCEPT

`check.py` PASS_SOURCE_REFERENCE_DOMAIN. Both bodies byte-exact:
- `0020E600` decode (10 B): `mov eax,ecx` (zero-extend u32→rax) +
  `add rax, qword[rip+0x1D74F27]` → target `01F83530` — D_B(u) = B+u32(u).
- `0020E620` encode (9 B): `sub ecx, dword[rip+0x1D74F0A]` → **same**
  cell `01F83530`, dword width (low32 of B) + `mov eax,ecx` —
  E_B(p) = u32(u32(p)−u32(B)).
- Inverse domain re-derived: E∘D = u always; D∘E = p iff
  (p−B) mod 2⁶⁴ < 2³²; p and p+2³² collide; D(0)=B — no null rule.
  Cell contents `90 FB 05 00` nonzero — consistent with the nonzero-B
  control being meaningful.
- Base-change and zero-base mutation controls correctly bounded.

## FABLE-REQ-AUDITSPEC-REVIEW-0928C — ACCEPT (all seven records)

- **facing-wrap-antipode-consumer** — `wrap_check.py` W1–W3/C FAILS 0;
  binary32 two-cycle re-derived from image constants; changed-bias
  detector refuses. Contract/ED-3 idempotence removed.
- **uc1-band-65-256-fable-ruling** — `uc1_band_checks.py` C FAILS 0 over
  the 100 clean rows; the U-signal (non-leaf with no .pdata at/above)
  and the rejected 47%-hit raw scan are sound ruling reasoning; the
  APPLY-IN-PART 99/21 split consistent with my extent review.
- **navgrid-thin-rectangle-consumer** — `thin_check.py` FAILS 0 (ran
  previously); carrier hunk correctly staged for FRONTIER as a page edit.
- **storage-cursor-alias-consumer** — `cursor_check.py` K1/K2/C FAILS 0.
- **widget-duration-consumer** — `widget_check.py` D1–D5 + D5m + C
  FAILS 0; every anchor matches my byte-exact verification of the same
  bodies (polarity, mode domain, bit-11 override, signed +0x90 path).
  The D5m signed model values agree with instruction semantics.
- **bq27-callee-saved note** — slot distribution claim consistent
  by-reading; correctly keeps live-breakpoint residue open.
- **postmultiply-float-order-consumer extension** — `order_check.py`
  re-run FAILS 0; whole-matrix qualifier consistent.

## Shadow follow-on

- `e867536cf` widget_b8 FP-limits qualifier: S now requires the masked-
  MXCSR/DAZ/QNaN caveats — honest scoping, no claim change.
- `a79ab236a` BQ-27 slot note — data claim consistent by-reading.

---

## ASTRA-REVIEW-APPROACH-DIVISOR-DOMAIN — ACCEPT

`check.py` PASS_SOURCE_APPROACH_DIVISOR. Byte-exact:
- `00339723` `F3 44 0F 10 0D 0C 9A 5B 00` = `movss xmm9,[rip+…]` →
  `008F3138` = `43340000` = **180.0f**. The divisor at `00339880 divss
  xmm0,xmm9` is a fixed positive constant — not variable/near-zero.
- `00339735` `movss xmm10,[rip+…]` → `01CEBC50` = `40490FDB` = pi.
- ABI claims consistent: xmm10/xmm9 saved in the prologue
  (`movaps [rsp+0x110]` / `[rsp+0x120]` restore at `00339A02`), the loop
  back-edge to `00339781` is AFTER both loads so the divisor dominates
  all iterations; the opaque callee at `00339885` rests on standard MS
  x64 nonvolatile-xmm preservation, correctly labelled an ABI assumption
  not a callee proof.
- Scoped correctly: only the divisor/unbounded-growth rationale is
  settled; the 53-site question, native callers, and FP state stay open.

## FABLE-REQ-AUDITSPEC-REVIEW-0928D — ACCEPT (both records)

- **gg1-msg12-0x8002** — `gg1_msg12.py` E1–E4 + C1/C2 FAILS 0.
  Byte-exact: `0023FBE0` dispatch `mov eax,[rdx]; dec eax; cmp eax,0x11`
  → table at `0x2402AC`; message-12 arm `0023FEE2` decodes
  `cmp rax,0x8000` on `[rdx+8]`; the 0x8002 arm exists via
  `sub rax,0x8001; cmp rax,1` and contains the read `0023FFF6 movzx`.
  Placement reasoning sound: four originators in message-10 contexts,
  three forwarders gated on incoming 0x8002, 15 other senders resolved
  away, delivery synchronous.
- **gg1-last-reader-3c87b0** — `gg1_3c87b0.py` L1–L5/C FAILS 0: every
  arbiter path into `003C87B0` passes a `di` store first; world-tick
  follows the arbiter on two paths, skips on a third — honestly kept as
  path-level placement, not full provenance. GG-1 at 50/51; stays OPEN.

## Shadow follow-on (revs ≤36743)

- `57c3fc1ff` created_flag_scope G/U/S — per-route scope correction
  (getters tested pre-pass; release passes never read the flag).
- `773c08600` element_release O/W/R/S — five destroys share the drain/
  release/external-free form; pendingCount cells identified per class.
- `cc8f99d58` vp8_lifetime V1–V4/S — `0016E210` release chain reached
  only via interface slot `01CDB290+0x18` from `0016DDD0`.
- `e867536cf` widget_b8 FP-limits — masked-exception caveats now
  required by S.
