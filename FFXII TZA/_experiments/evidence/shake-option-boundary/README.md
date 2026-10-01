# ASTRA — Screen Shake option: evaluation and output are different boundaries

2026-09-21. Task `ASTRA-SHAKE-OPTION-BOUNDARY`. Major systems: camera presentation,
settings, shared RNG. Consumers: FABLE camera semantics, OPUS generator contract,
SWE2-FRONTIER prepared camera observation. Independent review pending.

Player version: the setting can stop one set of camera adjustments from being
copied into an output buffer, after those adjustments have been calculated.
There is also an override and a separate authored-shake path. An OFF setting or
a quiet-looking camera cannot establish that all camera calculations stopped.

## Question, hypotheses and method

The prepared queue says Screen Shake OFF does not gate native evaluation. The
earlier ASTRA note only warned against inferring that OFF disables evaluation.
H1: the option suppresses evaluation; H2: it suppresses a later output step;
H3: its binding is not established sufficiently to decide.

**Method A** follows the already identified settings command 10 setter through
its exact global and consumer, then compares the existing original driver and
sampler evidence. The local branch and its ordering are sufficient; no B harness
or live session is needed. Actual caller frequency, screen effect and ordinary
state transitions remain C questions. There was no game launch, input, attach,
save/config write, intervention or cleanup operation.

## Primary evidence and observations

Authority EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Original complete bodies and decoded instructions are in `observation.json`;
`check.py` re-reads them from the pinned executable. Catalog body extents were
checked for complete decode. The three existing camera bodies are also compared
byte-for-byte with `camera-rng-discriminator/original-code.json`.

| Boundary | Original instructions | Bounded result |
|---|---|---|
| Option record | `002DE200` and `002DDD60` resolve `*(0215E6E0)`, bit 14 | Setter masks its input to one bit and getter reads that bit. The existing settings-command table supplies the command/label identity and inverted UI selection. |
| Native flag | `002DE21D` tails to `0037DDC0`; the latter writes `dword[02EBF3C4]=ECX` | This is a dword, distinct from nearby script-controlled gate `02EBF3C0`. The leaf itself does not normalize arbitrary direct callers. |
| Initialization | `0037D80A` in `0037D7F0` writes 1 to `02EBF3C4` | An initialization writer exists. This does not prove a particular live session's effective setting or application order. |
| Candidate calculation | `0037D9F6` calls `003D83A0` | The call precedes all option-dependent branches in this body. It is not suppressed by those branches, assuming normal return and valid state. |
| Override | `0037D989` calls `00237420`; `0037D98E` preserves its result in EBX; `0037D9FD` jumps to the copy when nonzero | `00237420` tests pointer `02089350 != 0`. This path bypasses both local flag checks. No new semantic name or live reachability is assigned to the pointer. |
| Ordinary copy gate | `0037D9FF` / `0037DA07` compare `02EBF3C4` / `02EBF3C0` with zero when EBX is zero | Either zero skips this body's output copy. |
| Copy | `0037DA23..0037DA45` write 28 bytes at `02EBF380 + sign_extend(draw) * 32` | The final four bytes of that 32-byte row are not copied here. Skipping the copy does not clear it in this body. |
| Gather | `0037D4F1` calls the above step; `0037D552..0037D756` gathers authored channel values; `0037D75C` then tests `02EBF3C0` | The later gate adds the auxiliary output row only when the **other** gate is nonzero. It is not a second read of the Screen Shake flag. Authored channel gathering precedes that gate. |

Thus the **local copy** condition is:

```text
pointer[02089350] != 0
    OR (dword[02EBF3C4] != 0 AND dword[02EBF3C0] != 0)
```

This is a static branch interpretation, not an executed truth table. The
neighbor gate's setter is `0037DB70`, reached through `003DD220`; it must not be
substituted for the option setter. `00358320` supplies the draw selection.
The existing camera page already describes gathering and the neighbor gate;
this package resolves the previously unconnected **option-to-copy boundary**.

The retained `00314370 ->003DCFB0 ->0037D1F0` path remains separate: live owner,
bound bank, nonzero channel state and non-sentinel entry are its known eligibility
conditions. The complete driver/sampler bodies agree with the earlier package.
Their local draw path has no direct read of this option global. This is **not**
a proof that all indirect callers, scheduling or initialization are invariant
under a UI change. No new sampler execution or live draw count is claimed.

## Controls, search limits and falsification

The original option setter/getter resolve the same settings record; initialization,
setter and copy-gate reader resolve the same dword. The neighboring flag and the
32-byte output row are independently resolved rather than conflated. Known driver
and sampler bodies are positive controls for the separate path.

The retained `xref-discovery.txt` reports three positive references to the option
flag using the existing entry-based `data_xref_scan.py`, with the distinct known
battle-state-pointer control `02EBF190`. Each discovered instruction was then
read in its complete original body. The source is retained with its hash.
This is discovery, **not an exhaustive no-alias proof**: the tool's image-base
heuristic does not establish every register's provenance or every indirect use.

The first exploratory command mistakenly used the wanted address as its control.
The tool reported three control hits but removed the control from the result set,
leaving `0 of 0` wanted addresses. That was not a valid query for the requested
sites; no absence or semantic result was accepted from it. A distinct control
fixed the query. The retained receipt check requires a nonempty wanted set, the
distinct control and all three positive instruction sites. No peer tool changed.

A direct option guard before the named evaluator call, an alias to the other
gate, or a store clearing the row on the skipped local branch would contradict
the stated local result. The verified complete body instead computes first,
tests the two distinct flags, and branches around its own copy. Effects of
callee internals or other routines are outside this local-store conclusion.

## Consumer changes and remaining live preparation

- FABLE/OPUS: incorporate the exact settings-to-output connection and override;
  keep sampler evaluation, output copying and visible presentation separate.
  Do not interpret a skipped copy as stopped evaluation or a cleared output row.
- FRONTIER: narrow the positive “does not gate native evaluation” wording to
  these verified entry paths. A screenshot of OFF does not identify effective
  native flag values, override state, initialization order, or the selected view.
  For a presentation test, record the actual flag pair, override and output
  identity alongside the UI setting and the authored driver/bank identity.
- The prepared shake request still lacks an exact reachable save-to-event route.
  A nonzero channel state cannot identify which candidate script fired. Tick
  brackets plus occupied slots also cannot count eligible-driver **visits** or
  establish invocation frequency. Preserve the useful occupancy-only plan;
  scheduling requires a separately qualified invocation observation.

This package does not consume a live allowance or close the actual finished-
driver scheduling question. The broad database L1+L2 goal remains active.
