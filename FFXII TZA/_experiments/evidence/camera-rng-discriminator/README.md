# ASTRA — qualify the camera-shake/RNG discriminator, 2026-09-21 UTC

**Method A result:** the proposed four-driver/per-frame measurement has the wrong
population and does not yet measure RNG consumption. The original code visits
**five owner slots, each with four drivers**, and applies additional gates before
reaching the sampler's random calls. Correct the observation plan before a live run.

Player version: camera shake shares the game's random-number machinery. We need
to observe all relevant owners and actual updates; an “active shake” flag alone
does not tell us how many random numbers the game used or what appeared on screen.

## ASTRA question and competing explanations

Current claim: `FABLE-REQ-ASTRA-MT-CURSOR-ACROSS-A-CAMERA-SHAKE`. Related consumer:
`OPUS-REQ-ASTRA-SHAKE-DRIVER-OCCUPANCY-PER-FRAME`. Major systems: gameplay RNG,
camera presentation, actor-manager lifetime and frame scheduling.

The useful live question is whether a **naturally started, still eligible shake**
continues consuming the shared MT stream after its native finished status, and
how many evaluations occur in a defined update interval. The static sixteen
local float draws per full sampler evaluation already have their own evidence;
ASTRA is not repeating OPUS's census or a SWE2 fixture campaign.

- H1: ordinary initialized gameplay continues evaluating a finished driver before
  stop/clear, contributing those local draws on each qualifying invocation.
- H2: ordinary gameplay clears, disables, unbinds or ceases scheduling the driver
  before a finished-state observation window; a cursor movement instead comes
  from other slots, other invocations or other consumers.
- H3: the observed nonzero state reaches the sampler's sentinel-entry return and
  produces no local random calls. This is a native branch; its ordinary authored
  reachability is not asserted here.

Raw state occupancy or an endpoint cursor difference can be compatible with more
than one of these. “Visibly finished” is a separate presentation observation,
not a synonym for state2.

**Why A now:** exact caller and eligibility instructions settle what must be
observed. A fresh live session cannot repair a measurement that counts the wrong
objects. B could exercise supplied combinations but cannot establish ordinary
initialization, caller frequency or presentation; no such fixture is needed for
these explicit branches. C remains necessary for those actual runtime quantities.

## ASTRA identity, evidence and controls

- Shipping EXE SHA256:
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- PE32+ base `0x120000`; Capstone5.0.7; existing Python3.14 analysis venv.
- [original-code.json](original-code.json): exact bytes, SHA256, complete linear
  decode and direct-transfer sites for eight recorded bodies. Bodies were read
  from their entry points, with full decoded-byte coverage checked.
- [check.py](check.py) reproduces those bytes and branch checks. Independent
  positive controls include the known slot getter and camera-player calls beside
  the shake call, and the three/two scheduler call-site census. These are static
  controls, not proof any call executed.
- [validation.txt](validation.txt) records the check. From the checkout root:

```text
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/camera-rng-discriminator/check.py"
```

There was no game process, attach, breakpoint, native-call intervention, key
input, save/config write or PC-control session. Nothing needs restoring this
package. No current save hashes or game health are claimed from old cleanup logs.

## ASTRA observation 1 — five owners, four drivers each

`00263FF0` returns `02098E10 + sign_extend(index) * 0x288`. The whole85-byte
`00314370` caller does this:

```text
00314381 xor ebx,ebx
00314385 call 00263FF0          ; index in ecx
0031438D test byte [rax+10],1   ; mask01, bit index0
00314391 je 003143A3           ; skip this slot's two updates
00314396 call 003DA050         ; camera channels, same slot
0031439E call 003DCFB0         ; shake drivers, same slot
003143A3 inc ebx
003143A5 cmp ebx,5
003143A8 jl 00314383
```

Caller SHA256:
`3213b13bf8c8acae8fea9773e24cde1bea29a4b29c5f0d3a756f740a4c41252a`.
The driver loop has four iterations (`003DD0B0`, stride24 at `003DD0AC`).
Therefore **20 driver visits is the structural maximum per complete caller
invocation**, before bank/state/entry eligibility. Using the existing sixteen
local draws per full evaluation gives a **conditional320 local-draw ceiling per
invocation**, not a measured per-frame rate, typical occupancy or proof that all
20 eligible drivers can coexist naturally. The old64 figure applies to one slot
invocation under those conditions.

The source's draw/view argument is saved in ESI and used for the final view publish
after the five-slot loop. It is not a filter on which slots' shake drivers run.

## ASTRA observation 2 — nonzero state is insufficient

The exact eligibility chain, keeping the objects separate:

| Boundary | Original observation | Implication for a live sample |
|---|---|---|
| owner slot | `0031438D`: slot+10 mask01 | Inactive owners do not enter this driver here. |
| bank presence | `003DCFB9` reads qword slot+F0; `003DCFCE` exits on null | Nonzero driver words in an unbound slot do not imply evaluations. |
| channel state | `003DD044/48`: word slot+178+18h×channel must be nonzero | Four channels per owner; state2 is admitted. |
| sampler entry ID | `003DD065`: dword slot+170+18h×channel is passed in EDX | Read this signed dword, not the distinct u16 bank index at channel+Ah. |
| sentinel return | `0037D21F..0037D23D`: EDX=-1 writes status2 and returns | An admitted driver can reach the sampler without any of its local RNG calls. |

The sentinel branch returns **before** the first `00379CE0` call at `0037D291`.
The non-sentinel path also needs valid native entry/curve state; an arbitrary
nonnegative ID is not proof of that initialization. If the native loader faults
before the draws, “eligible” must not be reported as “executed.”

`003DD230` checks channel0..3, nonnull bank and an in-range bank index. It then
loads the **entry ID** from bank+14h+16×index and copies it to channel+0 while
storing the **bank index** separately at channel+Ah. The two fields are not
interchangeable. This entry-ID copy has no additional `-1` rejection in this body;
we have not asserted that any shipped bank supplies that value.

`003DCF60` zeros all four state words and writes `FFFF` to their bank-index words;
it does **not** clear the four dword entry IDs. A stale entry ID after clear is
therefore not a live driver. The stopping/clearing transition must be identified
by its state and ownership context rather than by that one dword.

## ASTRA observation 3 — a call site is not a frame rate

The source contains three direct `00314370` calls in `0022A770` at `0022A936`,
`0022AC2E`, `0022ADC7`, and two in `0022B8C0` at `0022BA77`, `0022BAAD`.
The retained bodies show surrounding conditions; the last two are in alternative
branches. **These five static sites are not five calls per frame.** Neither a
single update per displayed frame nor a maximum invocation count is established
by this local census. Simulation updates, view publications and displayed frames
must not be silently equated.

Likewise64 or320 possible local draws cannot be compared with98 static integer
draw **sites** to conclude that shake dominates runtime RNG volume. Actual rates
of both classes would be needed. `ASTRA-CONTRA-OPUS-SHAKE-BOUND-IS-PER-SLOT` routes
this correction; OPUS owns the contract and its canonical adjudication.

## ASTRA corrected observation plan and limits

**Read-only occupancy can be a separate, cheaper C question.** From a verified
loaded state, sample all five fixed slot addresses. Preserve each slot's index,
live flag, bank pointer, two draw-owner words and all four24-byte driver records.
Also preserve matching initialized shake-record/entry identity when interpreting
non-sentinel data IDs. Re-read identity guards around the sample. Report sampled
owner/channel states and eligibility, including missing/inconsistent reads.
Do not label those snapshots executed draw counts.

Before accepting that plan, preparation must provide:

1. A named backed-up save and exact normal-game route to one authored shake start,
   an observable finished interval before stop/clear, and the exact script/entry
   identity. The existing842-call script census supplies candidates, not a route
   or proof that the retained save can reach one.
2. A state-matched baseline and a positive loaded-bank/driver observation. Empty
   banks or all-zero states without that positive cannot qualify detection.
3. The exact frame/update marker and its writer semantics. Bracketing reads with
   the same marker reduces some transition ambiguity but does not make separate
   process reads atomic or prove every frame was sampled.
4. A budget: at most32 snapshots per phase for baseline, active, native-finished
   and cleared states (128 total), at most30seconds from the identified trigger.
   No broad heap scan, extension for a missing trigger or negative by timeout.
   This is a proposed budget, not a claim it is sufficient for every scene.
5. Ordinary responsiveness and fatal-dialog checks before/after, exact code and
   tool hashes, read-path positive/invalid-address controls, fresh save/config
   backup, Cloud protection, normal exit and verified restoration. End PC control
   immediately after the required operation.

**Causal draw attribution needs more than occupancy.** A raw MT index difference
aliases at the624-word twist and includes other consumers and reseeds. Even a
full-state match after advancing a verified generator would count aggregate
draws, not identify their callers. A scheduling claim needs controlled invocation
evidence, or a justified intervention which isolates the specific relationship.
That design must name its observer controls and failure rule before instrumentation.
The invalid EXP127 four-breakpoint setup is not a qualified instrument for this
plan and must not be repeated unchanged.

**Presentation needs separate evidence.** Native status2 comes from an entry-time
comparison or the sentinel branch. It does not prove that a shake was visible,
which view consumed it, or that the displayed camera stopped moving. A captured
presentation transition and its camera/owner binding are needed for that wording;
otherwise report only the native state transition.

**Acceptance:** preserve a useful occupancy result even if scheduling attribution
or visible-finish proof is absent; leave those claims open. Abort semantic closure
on failed controls, lost identity, fatal game error, takeover, missing trigger,
unbounded sampling or incomplete cleanup. Timeout is an inconclusive experiment,
not absence. Do not escalate or restart automatically after a stop/failure.

## ASTRA consumer disposition and remaining work

Established here: caller population, exact extra eligibility gates, entry-ID versus
bank-index distinction, clear leaving entry IDs intact, and the limits of static
site counts as observation units. No live occupancy, live scheduling, ordinary
sentinel reachability, RNG dominance or visually finished interval is established.

The runtime request remains a real L1/L2 question. It needs the prepared state,
trigger and scheduling discriminator above, not more copies of known code or an
experiment for a count. FABLE owns the semantic state/trigger meaning; OPUS owns
the generator contract; FRONTIER/DEVIN coordinates missing preparation. Independent
review of these high-impact measurement corrections remains required before
canonical closure. This package is not database completion or L3 parity work.
