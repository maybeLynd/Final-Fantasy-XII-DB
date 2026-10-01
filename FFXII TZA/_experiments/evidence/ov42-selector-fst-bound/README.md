# ASTRA: remaining empirical obligations — method re-triage

Full L1+L2 goal ACTIVE / NOT_MET. This package is evidence-method selection and
one bounded original-code/data discriminator, not database completion. No L3.
Current user ladder controls method choice; an RT label is not a method mandate.
No game launch, PC controls, forced native call or instrumentation was used.

## Exact OV-42 discriminator and result

**Question:** Can the shipped FST extent/population alone prove that an indexed
owner never receives a negative signed WORD file index? Competing explanations:
(H1) large mapped indices always fail the loader's size check, invalidating the
metadata; (H2) the unchecked flat size lookup can obtain a nonnegative size from
another namespace row. This is an implementation-relevant prerequisite to the
remaining natural-play rejection question, not a substitute for it.

**Cheapest sufficient method:** shipping instruction analysis and exhaustive
bounded-state analysis against actual install FST bytes. Existing retained
owner fixtures establish narrowing but do not establish selector reachability.
No harness or process observation is needed to distinguish H1/H2.

**Identity:** EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base `0x120000`. `index-path-raw-02.json` preserves bounded original spans,
bytes, decoder version, driver identity and the actually invoked reviewed
`reg_tracking.op_kind` adapter. Each FST is frozen under `fst-inputs-01/`;
the result pins all twelve hashes. Tables have exactly 205,000 words and
kind0/id0=57, the independently documented size positive.

**Original instruction sequence:** `0032F170` maps group0 to kind5/index3*k
and groups1–3 to kind8/index4*k. `003DD610` reads the low WORD, `003DD618`
increments AX, `003DD61D` stores that WORD, and `003DDAA8` sign-extends it for
`0032E620`. The requester rejects a negative signed EDX at `0032E64A`–`0032E64E`.
The size helper's fallback at `0032E431` passes through `0046DE70` to
`002DF960`: `kind*5000 + signed32(index)`, then an unchecked DWORD load.
For the negative-narrowing cases analyzed here the full index is positive and
above 32,767, so the per-kind override's `<0x400` arm is not selected even if
its pointer is nonnull. No assumption that overrides are absent is needed.

**Result:** H1 is false as a general argument from table extent. Exhaustively
considering declared selectors `0..32767`, without claiming that this is the
caller domain:

| group mapping | negative narrowed index selectors | positive aliased FST sizes per language | first common positive alias |
|---|---:|---:|---|
| group0, ns5, 3*k+1 | 10,922 | 385 or 386 | k=11,667; full35,002; narrowed−30,534; flat60,002 = kind12/id2; size24,832 |
| groups1–3, ns8, 4*k+1 | 16,384 | 961 | k=8,751; full35,005; narrowed−30,531; flat75,005 = kind15/id5; size163,840 |

First negative selectors are 10,923 and 8,192 respectively. Group0 selectors
0..10,922 and groups1–3 selectors0..8,191 cannot produce negative narrowed
indices. Within the tested domain the ns8 negative intervals are 8,192..16,383
and 24,576..32,767: a universal monotonic threshold would also be wrong.
Group4 is excluded by the original metadata providers, not by this arithmetic.

**A separate observed code fact:** on a negative `.mot` size the loader branches
at `0032FED2` to `0032FF25`, loads the directory pointer and clears its first
byte at `0032FF2D`. An old nonzero header therefore does not survive that
specific negative-size branch's completed store. This does not establish
intervening caller effects, async write order, positive-size branch contents,
all aliases or thread interleavings. The reset's loaded flag and subsequent
primary-payload completion remain separate from metadata contents.

**Controls:** the actual capture path checks an SSE memory-store, LEA/address
computation and atomic RMW role. Reducer refuses lost spans, a failed upstream
role control, altered narrowing and missing language inputs through its real
analysis entry. Six hand-derived modular arithmetic boundaries check the
reducer's arithmetic. These are producer controls, not native execution or
independent acceptance. Completed reducer terminal exit0; invalid runs cannot
pass. Raw01 is exploratory: its producer was revised before raw02; raw02 and
its final source are the reproducible delivery. Earlier arbitrary end330000
was refused as an incomplete instruction span, then corrected to the shipping
exception-table fragment end330048. Optional pefile was unavailable; direct
shipping PE records supplied the endpoints. No invalid capture was promoted.

**Interpretation/limits:** neither the counterexample selectors nor an
unmodified loaded owner were observed. No path-table access to those indices,
successful companion load, natural selector producer or original interpreter
reachability is proved. These are FST lookup counterexamples to a proposed
bound, not rejection/leak witnesses. Actual input-domain proof remains needed;
the remaining OV-42 and its OV-21 rejection dependency stay OPEN. No runtime
question newly closed or independently accepted by this result (count=0).

**Consumer:** FABLE owns resource semantic integration; OPUS owns owner/index
contracts. They must retain the selector-domain precondition and avoid an
implicit FST-bounds safety guarantee. Independent SPEC review precedes T2
adjudication. Do not edit their claimed pages or repeat settled synthetic
rejection/arena evidence. Next discriminator: establish every non-debug
selector producer's range to `0032FC30`/`0032FCA0`, including variables and
resource-derived values; prove that range stays in safe intervals, or exhibit
a shipped valid input outside them and analyze metadata/owner ordering.

## Reproduction and cleanup

Use `Collaboration/Tools/analysis/venv/Scripts/python.exe` from repository root.
`capture-index-path.py FRESH_RAW.json` refuses overwritten output, changed
reference/adapter or incomplete spans. `prove-index-domain.py FRESH_RAW.json
fst-inputs-01 FRESH_RESULT.json` refuses empty/missing controls/tables and
overwritten results. Raw02/result01 are immutable; use new output paths.

All analysis is read-only against the reference and install; copied tables
are disposable evidence inputs. No saves/config/game process were modified.
There is nothing to detach or restore. Source-file/copy hashes are checked
by the frozen input receipt. Do not infer host-wide process cleanliness.

## Reusable preconditions and failed hypotheses

- Counts/path populations do not constrain an unchecked flat lookup's caller.
- Prove source and intermediate widths, modulo operations and all producer
  paths before natural-reachability closure; a convenient signed16 domain is
  not an established domain.
- Read full shipping exception-table fragment ends before capture; refusal
  on a split instruction is required. Unavailable pefile is not a need to
  rebuild a runtime lab: fixed PE fields suffice for this bounded lookup.
- Upstream invalid/missing input must stop downstream result production;
  observed zero and valid empty output differ from missing evidence.
- Adapter identity alone is insufficient: call it in the concrete producer
  and run store/LEA/RMW controls there. Raw Capstone flags are not the policy.
- EXP127 remains INVALID_POST_TRACE, not a reusable semantic closure source.
  No unchanged four-breakpoint trace or parked menu retry is permitted.
