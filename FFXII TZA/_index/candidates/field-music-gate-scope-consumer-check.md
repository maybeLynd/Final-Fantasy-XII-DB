# Affected-consumer check: the field-music "dead actor" implication narrowed to the manager-slot gate (OPUS, 2026-09-27)

**What this answers.** `ASTRA-RETURN-OPUS-FIELD-MUSIC-GATE-SCOPE`, from ASTRA's `_experiments/evidence/field-music-gate-scope/`.

OPUS re-read `00265270` (28 B):
- `test byte [02098E20], 1` / `je`;
- `mov rax, [02098E58]` / `test` / `je`;
- `movzx eax, word [rax]` / `ret`;
- `xor eax, eax` / `ret`.

It has no actor argument and no death or health operand. `02098E20` is ActorManager slot 0 `+0x10`, the store's
`ActorManagerSlot.slotFlags` live bit, and `02098E58` is slot 0 `+0x48`.

Corrects: `18-Audio/CONTRACT-field-music-selection.md` (the composition paragraph's "dead actor" / "`liveness & 1 == 0`" and "for a dead actor").

**Regression:** `_experiments/evidence/field-music-gate-scope/check.py` (ASTRA). It has four rejecting controls,
including an actor-pointer substitution for the fixed global. Run receipt: check.py executed at 280cc7570 (PASS)
before this publish.

| consumer | state |
|---|---|
| `18-Audio/CONTRACT-field-music-selection.md`, the composition paragraph | revised-here (struck and narrowed to *gate off or null bank → getter 0 → default track*; the death link is not established) |
| same contract, gate/ladder results, 22 cases / 20 mutants | agrees (unchanged) |
| `_types/fields.tsv` `ActorManagerSlot +0x10 slotFlags` (bit 0 = slot live) | agrees |
| `18-Audio/Audio-Boundary/CONTRACT-sound-request.md` `0x02098E20` row (slot-array liveness) | agrees (manager-slot liveness, not actor death) |
| `_experiments/EXP-099-field-music-selection-exec.md` lines 43/55 ("dead actor", "liveness") | routed-to-ASTRA-RETURN-ORACLE-FIELD-MUSIC-GATE-SCOPE (SWE2-ORACLE, the EXP-099 producer). The producer report's scope is its owner's; the raw case names stay as history |

PENDING PROPAGATION for the EXP-099 record.
