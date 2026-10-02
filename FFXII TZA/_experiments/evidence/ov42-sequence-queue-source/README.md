# The special-sequence kind-4 queue writer

**Question.** Does the previously uncovered queue store `003068D4` locally exclude action IDs 511–534, or does its source remain dynamic? H1: its dispatch/value checks constrain the queued ID to a fixed subset. H2: only the dispatch kind is constrained locally; a row/base/stride relationship supplies the ID.

**Player view.** This is the queue-writing branch normally associated with Quickenings. We checked what the original instructions calculate. We have not demonstrated a disputed action entering that branch during play.

**Method A, STATIC_ONLY.** Shipping bytes and their embedded dispatch table suffice for the local branch and arithmetic. Live state is unnecessary for those questions. Normal kind/row consistency, actual scheduling, initialized descriptors and lifetime are separate requirements.

## Identity and original inputs

EXE SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, preferred base `120000`. Five original exception records chain to entry `306760`, covering 936 physical bytes through `306B08`. Those bytes are **911 code bytes**, one NOP at `306AEF`, and six original relative dispatch DWORDs at `306AF0..306B08`. The producer checks actual directory records, unwind headers and chained footers against the EXE; metadata is not assumed to consist entirely of code. The reviewed shared access-role adapter is used by the actual capture and annotation validator.

The exact six relative entries resolve at the preferred base to `306931`, `306A3D`, `3067DB`, `306848`, `3069F8`, `306A8E`. Original `DEC EAX`, unsigned compare against 5, `CDQE`, image-base LEA, indexed DWORD load, ADD and JMP establish the kind selection. Analytical CFG copies resolve that one indirect JMP using those verified entries; the original bytes are unchanged. Among the six admitted dispatch kinds, **only kind 4** reaches the queue store. This is a source reach set, not six native runs.

## Result

Entry RDX is saved in nonvolatile RDI. Under normal ABI, valid readable state and the declared no-interference premises, let:

- `D = (low32(incoming row pointer) - low32(20E600(first context + C) return)) mod 2^32`;
- `S = u16(second context + 8)`, with **S > 0**;
- `q = floor(D / S)` and `w = q & FFFF`.

`3068D4` writes DWORD `FFFFFFFF` when `w == FFFF`; otherwise it writes `(w - 208) mod 2^32` to `022C2178`. The pointer subtraction is 32-bit, DIV is unsigned, and the quotient is narrowed to AX before sentinel comparison/conversion. This is not a general 64-bit pointer difference or a universal inverse for the queue remap.

The descriptor QWORD `2EBF138` is loaded twice. The first supplies the lookup key at DWORD+C; the second supplies WORD+8 as divisor. No equality/stability of those two descriptors or their contents is established. There is **no zero-divisor check** between the WORD load and DIV: S>0 is a precondition, not a live initialized invariant or observed fault.

With coherent original row/base/stride-60 premises, row 511 computes queue 303 and row 534 computes queue 326. These two calculations illustrate the proven formula; they are not executed FF12 instructions or natural samples. There is no local row-ID/category exclusion in this branch. The dispatch kind alone does not prove that this call's row belongs to the usual Quickening range. Any such exclusion needs the **kind-to-row/caller/owner consistency invariant**, which remains OPEN.

The preceding `306D90`, memset-like import, `30D720`, `30D550` and lookup calls are opaque for native effects. Register preservation is the Win64 ABI premise, not stub evidence. Their scheduling/state effects and whether normal execution supplies a compatible row are not proved.

## Actual checks and limits

Current producer `b07bf14e`, `result-03.json`, `prove-04` is terminal 0. Current controls `f4be90ac`, `control-02` are complete: four real disposable CLI refusals (failed extent despite retained apparent output; failed capture; missing data status; missing table data) and six labelled derive countermodels. Countermodels cover a wrong kind-4 table target, stride width, signed division, queue width, low16 conversion and an arithmetic bypass. The last is the smallest regression for the corrected dominance direction. CLI cases invoke the real producer; synthetic derive cases are not EXE patches or native executions.

Historical failures remain preserved and receive no pass credit: decoding all 936 bytes as code refused before any source output; the first dominance check reversed the shared helper's argument order and produced no result; an output-location mismatch was caught before controls/publication. Exact historical drivers and receipts are retained. The final producer resolves relative outputs under its package directory; missing/failed upstream receipts cannot be converted into valid output. No published evidence was overwritten.

**Not established:** normal kind4/candidate pairing; full caller/owner coherence; global kind persistence; descriptor initialization or table-binding stability; natural queue consumption/command execution; helper effects; lifetime/reuse; whole OV-42 or L1+L2 completion. No FF12/native/emulator process, PC control, save/config/reference mutation or instrumentation was used. All owned scientific children terminated.

## Consumers

FABLE: replace the unread `3068D4` local producer leg with this kind-4 dispatch/quotient/remap result, leaving kind-to-row/caller/owner consistency OPEN. Do not infer normal candidate reachability. OPUS: exact pointer/width/divisor/two-descriptor read preconditions and queue ABI. SPEC: independently inspect original code/data/metadata, actual prerequisite propagation and pin-bound producer/control paths. Integrity and producer controls are not independent acceptance. Required reviews and canonical incorporation remain pending.
