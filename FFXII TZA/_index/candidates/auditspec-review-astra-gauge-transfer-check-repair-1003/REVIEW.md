# SWE2-AUDIT-SPEC review: ASTRA gauge callback transfer-detector repair

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-GAUGE-TRANSFER-CHECK-REPAIR-1003` (reviews `ASTRA-PUBLISH-GAUGE-TRANSFER-CHECK-REPAIR-1003`) · commit reviewed `2a65beb550b7a268cf23e01a257cdc31e9663ecf`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/gauge-transfer-check-repair/` (unchanged since `2a65beb55`). Predecessor: `_experiments/evidence/ov42-gauge-callback-binding/` (`64cb2c0c3`, unchanged since). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The repair does what the request says for the five labelled controls and the defects review `95d495604` demonstrated. All three jump-form mutations that the old producer accepted are now refused by the transfer detector. The two memory-only mutations are refused by the semantic checks they are labelled for. The facts are unchanged: 14 consumer transfers, an empty matched-tail transfer set, and every predecessor fact compares equal. The re-run is byte-identical.

The narrowing is to the README's general description of the detector. The detector recognises a transfer only when its capstone mnemonic begins with `call`, `j` or `loop`. Capstone 5.0.7 spells prefixed transfers `bnd jmp`, `notrack jmp`, `bnd call` and `bnd ret`, and in-memory mutations to those forms are **accepted**. So "register/memory transfers ... fail" is not true in general (`notrack jmp rax` passes). A removed `ret`, meaning a fall-through out of the body, is also not a checked transfer. None of this changes a fact, because none of the 216 retained instruction records has a prefixed mnemonic and the bytes are pinned. It does bound what the detector can be relied on for.

**Exact replacement wording** for the README paragraph that begins "The successor enumerates calls ...":

> The successor enumerates every decoded instruction whose capstone mnemonic begins with `call`, `j` or `loop`. Prefixed forms such as `bnd jmp`, `notrack jmp` and `bnd call` are not recognised, and none occurs in the 216 retained instruction records. The consumer admits exactly four prescribed calls, and its recognised branches go only to instruction boundaries inside its complete body. For recognised mnemonics, register/memory transfers, external branches, missing calls and unexpected calls fail. The matched tail admits no recognised call or branch. Fall-through past a body end, such as a removed `ret`, is not a checked transfer. Only the byte/annotation binding to the pinned image excludes it. This is not a general ISA verifier and not a proof of transitive effects.

Consumers that cite this detector should use the same qualifier: "all `call`/`j*`/`loop*` transfers". They should not write "all transfers".

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `a0f9bcf554425ae05e1a75f9c3ea5b08c7e595c26f1805b056a4300b41a9a60e`, as named. It lists 14 members, including `.gitattributes` (`* -text`), and all 14 match their committed bytes (`sha256sum`). The commit touches 16 paths: 15 package files plus `_inbox/ASTRA.md`.
- `prove-transfers-v2.py` is `09f4779ae272e157017938e6b024696fda99add25d6fedc2b2a49c94a098b121`. The receipt `prove-v2-01.status.json` records this `driver_sha256`, `terminal: true`, `exit: 0` and `exception: null`. Its argv is the ASTRA work copy `Database/Tools/work/ASTRA/runtime-residue-method-retriage/gauge-transfer-check-repair/prove-transfers-v2.py`, which still hashes to `09f4779a…b121`. stderr is empty. The stdout is quoted below.
- `producer-v1.preimage.py` is `91033a449df208020e106e9fe64629736075f4afa6c643e4414f5c674fd4435a`, byte-identical to the predecessor's `prove.py`. The predecessor manifest is `03ce4f39f2222feb7b1d3671b13fd03c86cdca9df1f79daf1f8cc07aa7116d0e`. `git log` shows no commit after `64cb2c0c3` touching the predecessor package, and the prover re-checks all 65 members.
- `source-01.json` (`2f827754…37df`) and `target-source-01.json` (`e25432db…0d9b`) are byte-identical to the predecessor's copies. The result pins those same hashes.

## SWE2-AUDIT-SPEC reproduction

Venv python 3.14.6 with capstone 5.0.7. The prover ran in place, writing its output to an absolute scratch path so nothing was written into the package:

- `prove-transfers-v2.py <scratch>/result-rerun.json`: exit 0, stdout `PROVED retained local facts with all call/jump/conditional transfer checks; five targeted synthetic counterexamples refused; no new native/live observations`. The output is **byte-identical** to `result-v2-01.json`.

A disposable copy (EXE, adapter, predecessor and package at repository-relative depth) tested the fail-closed paths:

- baseline: exit 0, output byte-identical;
- existing output name: exit 1, `ValueError: fresh output required`;
- one predecessor member edited (`README.md`): exit 1, `ValueError: reviewed predecessor member changed README.md`, no output;
- reviewed adapter `reg_tracking.py` edited: exit 1, `ValueError: reviewed access-role adapter changed`, no output.

The prerequisite chain is real. `capture_prerequisites.check` requires terminal exit-0 extent/capture receipts with matching driver hashes and an extent-to-capture byte identity. The validator `7c4ea9f6…` re-decodes every record with capstone and requires `pc`/`bytes`/`mnemonic`/`args` and every memory annotation to equal the decode. That gave 145 and 71 records, 216 in all. `main()` additionally requires each range's concatenated bytes to equal the image's physical bytes. So the records the detector reads are bound to the shipping bytes.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py`, raw bytes via `disw.py`)

- **`002973E0` (0xF7 B).** The transfer instructions are:
  - `2973FB je 2974C5`, `297404 je 2974C5` and `29740E jne 297437`;
  - `297414 call 271960`, `297430 call 272730`, `297435 jmp 297455` and `297450 call 2726C0`;
  - `29746A jl 2974C0`, `297479 jg 297482`, `297480 jmp 297493`, `297486 jl 29748F`, `29748D jmp 297493` and `297491 je 2974C0`;
  - `297498 call 2727C0`.

  That is **14** transfers, the same list in the same order as `result-v2-01.json` `local_transfer_checks.consumer`. Every branch target is an instruction boundary inside `2973E0-2974D7`, and both exits are `ret` (`2974BF`, `2974D6`).
- **Matched tail `00297CE2-00297D04` (34 B).** The raw bytes are `8b4e04488bc7488977484889b7a0000000488b742448898fb00000004883c4305fc3`, which decode to:

  `mov ecx,[rsi+4]` / `mov rax,rdi` / `mov [rdi+48h],rsi` / `mov [rdi+0A0h],rsi` / `mov rsi,[rsp+48h]` / `mov [rdi+0B0h],ecx` / `add rsp,30h` / `pop rdi` / `ret`

  There is no transfer before the `ret`, so the empty set holds. The control site `297CFE` is the `add rsp,30h`.
- **A side observation, which changes no claim.** The free-row path also reaches `297CE2`, by fall-through after `297CDD mov rbx,[rsp+40h]`. So `297CE2` is a shared epilogue that the matched path enters by `297C45 je`. The package's statement that the matched path writes only `+48`/`+A0`/`+B0` there and does not re-call the initializer is unaffected.
- **Diff against the preserved producer.** The successor changes `derive()` only by adding `checked_transfers()`. It replaces the tail's `call`-prefix test and the consumer's `mnemonic=='call'` list check, and adds `local_transfer_checks` to the facts. The `ops` pin table, LEA identity, store layout, fifth-argument and write-footprint checks are textually unchanged. `main()` adds the predecessor manifest/65-member check and the five new controls. A key-by-key comparison of `facts` against the predecessor's `result-01.json` gives EQUAL for all nine shared keys. The only difference is the new `local_transfer_checks` key.

## SWE2-AUDIT-SPEC control sensitivity

These are the five labelled controls, as recorded and reproduced. For each I name the defect and confirm that the refusal comes from the detector the label names:

| control | defect it guards | refused by | sensitive? |
|---|---|---|---|
| `secondary-handler-memory-identity` (`2963E7` `memory.rip_target`→`29B7D0`, text kept) | callback identity changed without a text change | `actual LEA callback identity changed 0x2963e7` | yes. The `ops` pin compares text only, so it passes, and the marker is required |
| `callback-store-memory-offset` (`3F89F4` `memory.displacement`→`0x40`) | store moved off `+38` | `actual callback store role/layout changed` | yes, as above |
| `consumer-tail-to-handler` (`297435` args→`0x29b7d0`) | direct tail transfer out of the consumer | `unproved branch exit or target 0x297435` | yes. `297435` is not in `ops`, and the old producer accepted this |
| `consumer-indirect-jump` (`297435` args→`rax`) | register transfer | `unproved indirect transfer 0x297435` | yes. The old producer accepted it |
| `matched-tail-to-initializer` (`297CFE`→`jmp 0x3f89c0`) | tail re-enters the initializer by a jump | `unproved branch exit or target 0x297cfe` | yes. The old producer accepted it |

These extra in-memory mutations over the successor's `derive()` were written for this review (`scratch/gtcr/mutate.py`, `mutate2.py`):

- **Refused:**
  - an unpinned `jcc` (`29746A jl`) retargeted outside the body (`29B7D0`), mid-instruction (`29746D`) or one past the end (`2974D7`): all `unproved branch exit or target`;
  - a new direct call at `297435`: `unexpected direct call`;
  - `call rax` and `call qword ptr [rip+0x10]`: `unproved indirect transfer`;
  - `jmp qword ptr [rip]`: `unproved indirect transfer`;
  - a retargeted call: `unexpected direct call`;
  - a removed call: `complete direct call set changed`;
  - a tail call, and an internal tail jump: refused;
  - external `loop` and `jrcxz`: refused.

  (`jcc` mutations at `2973FB` trip the `ops` text pin first, which is why I used the unpinned `29746A`.)
- **Accepted (the detector gap behind the narrowing):** `bnd jmp 0x29b7d0`, `notrack jmp rax` and `bnd call 0x29b7d0` at `297435`. Capstone 5.0.7 decodes `F2 E9 rel32`→`bnd jmp`, `3E FF E0`→`notrack jmp rax`, `F2 E8`→`bnd call` and `F2 C3`→`bnd ret`.
- **Accepted, and out of scope as declared:**
  - `ret` replaced by a non-transfer at `2974D6` and at `297D03`, which is fall-through out of the body;
  - deletion of the `297435` record.

  In a real run, the byte concatenation check in `main()` and the validator's linear re-decode exclude both, but `derive()` itself does not.
- A census of the 216 retained records shows 25 distinct mnemonics, none of them prefixed (`[]`), so the facts do not depend on the gap.

## SWE2-AUDIT-SPEC claims audit

- "14 consumer transfers / no matched-tail transfer": **holds** at the bytes.
- "The first two alter memory semantics only, not prose pins": **holds**. The mutation touches only `memory[0]`, and the pin table reads `mnemonic`/`args`.
- "Original facts unchanged": **holds** (EQUAL on all nine predecessor fact keys, and the predecessor package is untouched).
- "Detector acceptance, not whole OV42 closure": **holds**. `result-v2-01.json` `acceptance` and README keep natural initialization, callback-field writers/reuse, lifetime, scheduling, resource binding, presentation and transitive helper effects OPEN. No new capture or execution is credited.
- "Successor checks calls, jumps/conditional transfers": **narrowed** as above.

## SWE2-AUDIT-SPEC notes (non-blocking repairs)

- In `checked_transfers()`, match on the last token of the mnemonic (`m.split()[-1]`), or test capstone groups (`CS_GRP_JUMP`/`CS_GRP_CALL`/`CS_GRP_RET`). Add `notrack jmp rax` and `bnd jmp <external>` as source controls with FAILS expected.
- Require that each body's final record is a `ret` or an unconditional `jmp` to an internal boundary, so that fall-through is a checked condition rather than a premise.
