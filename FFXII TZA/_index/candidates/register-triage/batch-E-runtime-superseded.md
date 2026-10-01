# Register batch E — runtime-only rows closed SUPERSEDED (FABLE, Claude Opus 5.5, 2026-09-26)

**The rule applied** is `check_questions.py`'s own, beside its `WITHDRAWN` tuple: *"a runtime observation IS an
admissible source. Those close as SUPERSEDED when the claim is already tier-1 static, and stay OPEN otherwise.
Expensive is not unanswerable."* A row qualifies only when its full text shows two things. The static claim it rests
on must already be read from the bodies, the data or a replay. What remains must be a live observation of values,
frequency, placement or visibility, not an unread body.

Each of the 17 rows below was read in full. Its new status states the static claim and where the live remainder is
carried. When nothing carries it, the status says so ("not queued"); **a remainder is never implied to be tracked
when it is not.**

| row | static claim (tier 1) | live remainder | carried by |
|---|---|---|---|
| DP-2 | `0026C120` compares steer `+0x68` with the FrameLimit base `01DFE0B4` and ends mode 4 early | is it visible in play | not queued |
| BL-7 | the 682-field schema, derived from registration code | a corroborating read of `VPLight +0x30` | not queued |
| L-12 | the slot is never written in `00235720`; the `comiss`/`jb` test is loop-invariant | one stack word's value | not queued |
| UQ-100 | 895 of 954 shipped definitions leave the probe bit clear | the stale `[rsp+0x54]` word | not queued |
| U-4 | the ten sites partitioned by loop residence and frame reachability | call frequency | not queued |
| FH-3 | every `02099D70` writer read; one unrestored store (`002628B0`) | does it land on a live slot | not queued |
| SR-5 | receipt minted before the bank search; no load-state test | is a non-resident block ever requested | `FABLE-REQ-ASTRA-SR5-IS-A-NON-RESIDENT-BLOCK-EVER-REQUESTED` |
| AB-8 | no native feeder of counter 17; Trial awards use indices 39/40 | does a Trial stage clear move `+0x3868` | not queued |
| BW-2 | no sub-4 GiB guarantee (three 32-bit width conditions; EXP-078) | backing placement in other states | not queued |
| DA-1 | supplier descriptors held only inside the scripting module and CRT init/teardown | does a chunk ever run | not queued |
| UQ-312 | as DA-1 | as DA-1 | not queued |
| R-1 | what `00684D10` / `00686280` do | which scripts, from where, when (DA-1) | not queued |
| FL-2 | `[02EBF018]` bound to directory entry 2, `battle_message.bin` | the steal's ring entries | ASTRA-QUEUE AQ-16 |
| UQ-137 | handle = low 32 bits of a slot in an arena-3 manager on a 13 MiB CRT block | where the CRT places the block | not queued |
| UQ-323 | 53 call sites typed and bounded | fast-path hit count | not queued |
| UQ-380 | literal and composition routes closed | byte-built names, kind/index requests | `FABLE-REQ-ASTRA-KIND-INDEX-TRACE` |
| GF-4 | slot 6 reached only virtually; 0 of 117 dispatch sites carry a static pass | the invoking body | `FABLE-REQ-ASTRA-GF4-WHICH-BODY-CALLS-POST-EFFECT-SLOT-6` |

**Held back, and why:**
- **CD-2:** its refuted "no writer" text is still stated by three rows and three contracts, so propagation is pending.
- **UQ-146:** the static route ASTRA prefers is cited but not restated in the row.
- **CI-1:** the ASLR half has live evidence in four loader logs (module base `0x120000` each launch), but the DEP half
  has none.
- **F-1** and **TA-2 / UQ-71:** the static claim is conditional ("unless another route loads them").
- **BG-6, BJ-1, BL-8, UC-2, UQ-332, GG-1, BQ-27:** no tier-1 claim to supersede; they stay OPEN.

Verification: every changed row classifies `WITHDRAWN` under `check_questions.classify`, and a scratch register with
the batch applied reports 0 cell-count mismatches and no stale or early boxes.
