# Some debug source coordinates have no indexed physical line

The canonical ATEL companion page describes q0 as a bytecode-to-source map into paired SBN blocks. **Method A** tests the physical addressability of those coordinates using the eight actual admitted extracted DBG/SBN files and OPUS's unchanged published SBN32 parser. No compiler, original machine code, guest or game executes; no formula sweep for SN1 head X is performed.

Two internal q0 groups contain a concrete exception:

| Module / scope | q0 indices | Source block | Coordinate line | Physical indexed lines |
|---|---|---|---|---|
| btlctrl /1 | 3978..3980 | 2 (`mapctrl_mj.src`) | **559** | **558** |
| mapctrl /1 | 5201..5203 | 2 (`mapctrl_mj.src`) | **558** | **557** |

Each group has one record with instruction-start flag1 and two flag0 records. Both are well inside a larger scope, not at the q0 table's trailing padding. The coordinates lie one past the physical line table under either one-based or zero-based candidate indexing. The final indexed source text and remaining tail bytes are retained: btlctrl ends in `ucon()`, mapctrl in `wait(1);`; the remaining bytes are zeros, not an extra indexed source line. This does not identify the cause. Compiler-generated EOF coordinates, virtual line numbers, snapshot omission or different source material are competing explanations, not findings.

Nine further records use lineCount itself, which is addressable under a one-based candidate and not a zero-based candidate. Bounds alone do not independently prove the compiler's index convention. Most nonzero records lie inside both candidate ranges; that is addressability evidence, not proof that the source line produced the instruction. Preserve the accepted source relationship and original layout/page-map findings; do not use this exception to retract every source attribution.

The zero-line records reveal a second precise correction. All61 are all-zero suffix records with no instruction-start flag. **Five scopes have three of them**: ctrl1, btlctrl22, evctrl3, mapctrl1 and mapctrl3. The published `0–2` suffix bound is false for these files. The actual observed range is0–3. This does not alter the accepted q2/q3 laws: it corrects the q0 physical span/domain qualification, and is not a universal claim about the original writer or padding cause.

The first reducer was **INVALID_ZERO_SUFFIX_ASSUMPTION** before result creation: it copied the canonical0–2 bound and stopped on ctrl1. Its checker is retained under `retained/invalid-zero-suffix-assumption`. The first repair also stopped after a partial checker edit because a truncated diagnostic omitted evctrl3 from its expected list. Its source and partial checker are preserved. The corrected procedure reads the full retained exception set, validates preimages before writes, and reports all five scopes. Raw capture and original inputs were not recaptured or rewritten.

The initial capture's control dictionaries perturb parsed coordinate fields and retain original `record_hex` as context; they are not encoded byte mutants. No raw-reader control proof is attributed to those dictionaries. The corrected default checker performs actual four-byte encode/decode controls: original positive, blockCount rejection, lineCount+1 rejection, zero-line category and lineCount convention boundary. Future fresh capture controls now encode/decode and update hex consistently. With retained raw present, the actual default `capture.py` invokes the corrected checker and exits without recapture. The frozen invocation receipt verifies that path and unchanged raw. A clamp-missing-line mutation must fail, as must restoration of the old two-record suffix bound. These are host producer regressions, not new original-game experiments.

Required consumer change: a source mapper must preserve an unresolved/missing physical-line result instead of indexing past the table or clamping to the last line. Canonical q0 prose and its actual producer/domain guard should record the six internal EOF+1 coordinates and observed0–3 suffixes. FABLE semantic, OPUS type and DATA companion-page owners receive the original inputs, parser/control identities and exact examples; peer files remain untouched. Independent SPEC acceptance remains pending. SN1 head X and the cause of missing source coordinates stay open; a range check is not an exclusion or disposition.

Exact input hashes/lengths, selected original parser AST/source, canonical consumer preimage, original/current driver identities, raw maps, reductions and failure/control receipts are retained. The reference is the existing admitted extraction used by OPUS/FABLE; exact local bytes are pinned. This package does not perform a fresh full-VBF provenance audit or prove original toolchain equivalence. Original files and peer producer readbacks are unchanged. PC control is off; S19's spent allowance/unapproved extension persists; full L1+L2 NOT_MET, L3 later.

Reproduce the retained default path from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain/capture.py"
```

Player view: a few bytecode records name a source line that the shipped source snapshot does not contain. A reconstructed debugger must show that gap honestly. We also corrected a small bound: some debug tables end with three zero records rather than at most two.
