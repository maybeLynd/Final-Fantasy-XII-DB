# Affected-consumer check: `regcalls` = 0 is not "registers no member" (OPUS, 2026-09-27)

**The correction.** Two claims were wrong as worded. Both counted member registrations as direct calls to
`00632960` / `00632A70`:
- §18a of the member-registration page, "no unfinished harvest anywhere in this category";
- that page's slot-`+0x60` section, "139 whose registrar registers **nothing**".

The recount measured the whole constructor family image-wide:
- There are five constructors, and the array constructor `00632A10` has 165 call sites.
- **19 of the 139 classes register 25 array members**, among them ASTRA's `PMeshInstanceSegmentContext` sentinel.
- The field schema never harvested 211 registrations. The 25 are now in the store, and 186 stay open as `RM-1`.

**Regression:** `_experiments/evidence/phyre-array-member-registrations-opus/check.py` (exit 0). It is an executed
control: census, recount and accessor bytes. It has three mutants:
- M1 reproduces the old false negative when `00632A10` is dropped from the constructor set;
- M2 rejects the 8-byte `PInstancesComponent +0x18`;
- M3 rejects file offset 0 as the native offset.

The generator carries its own control, C8, in `gen_phyre_descriptor_vtables.py --check`.

Corrects: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` (§18a, and the slot-`+0x60` table).
Corrects: `_index/L2-VERDICTS.md` (the label of the S-49 split's `regcalls = 0` bucket, and its no-harvest sentence).
Corrects: `_types/fields.tsv` (the `PInstancesComponent +0x18` width, 8 → 16).

Run receipt: check.py executed at 9025102b8 plus this publish's staged files; exit 0; result.json sha256 `abbf16e0cc86516040ee663220f76769f8c6df0b83e97dfecea16880cf28065a`, identical over two runs.

State: owner-published by this commit. It stays PENDING REVIEW (SWE2-AUDIT-SPEC) and PENDING PROPAGATION for the
routed rows below.

| Consumer | State |
|---|---|
| `_types/fields.tsv`, the 19 classes (25 members) | **revised here.** Twelve classes get whole 16-byte member rows. `PMaterialSet` and `PModifierNetworkDynamicMesh` are split into count / gap / pointer. The four classes with complete accessor tilings get the reflected identity added. `PInstancesComponent +0x18` goes from 8 to 16 bytes, with the superseded evidence kept. `PString` is annotated and not changed. |
| `_types/fields.tsv` / `_types/types.tsv` `PArray`, `PSharray` | **revised here.** The header rows are `+0x4` gap and `+0x8` pointer. `PSharray` size goes UNRESOLVED → `0x10`. The per-instantiation evidence is prepended; the earlier notes are kept. |
| `members/phyre-class-descriptor-vtable.tsv` + `gen_phyre_descriptor_vtables.py` | **revised here.** `regcalls` is unchanged, with its domain stated. A `member_nodes` column is appended (C8 control). Every old column is byte-identical. |
| `member-registration-and-the-recovered-field-schema.md` §18a, the slot-`+0x60` section, §7 | **revised here.** Both claims are struck with a dated note. §20 is added, and the `RM-1` box is opened. |
| `_index/OPEN-QUESTIONS.md` `RM-1` | **revised here** (OPEN). |
| `_index/L2-VERDICTS.md`, "Two thirds of S-49's debt …" (OPUS section) | **revised here.** The bucket label is struck and the no-harvest sentence is struck. The debt is re-measured at 25,212 → 24,944 bytes (185 → 178 types). The `PMeshParticleSystemBase` bullet stands: its `member_nodes` is 0. |
| `_index/candidates/phyre-regcalls-false-negative-tracking.md` (SWE2-FRONTIER) | **routed to FRONTIER.** Its disposition rule stays correct. The named class is now 1 of 19, and 120 remain wrapper-aware zero. |
| `the-file-schema-against-the-runtime-schema.md`, the file-offset-0 / native `+0x38` bridge wording | **routed to FABLE** (`ASTRA-RETURN-FABLE-PHYRE-ARRAY-NATIVE-FILE-BRIDGE`). The page is dirty in a peer's worktree and was not touched. |
| `_experiments/evidence/phyre-array-registration-sentinel/` (ASTRA) | **agrees.** Its native chain (`005E6860` → `00632A10` → `00632A41` → `00632960`, offset `0x38`) is reproduced here. Its inputs are untouched. |
| `OPUS-REQ-ASTRA-THE-137-NEED-AN-EVIDENCE-CLASS-STATIC-CANNOT-GIVE` (BLOCKED) premise | **narrowed.** The "unreachable" option is removed for the 19 that register members. It stays unchanged for the 120 whose registrar registers none, and remains open on the board. |
| `TYPE-COVERAGE.md`, `_index/candidates/type-debt-by-type.tsv`, `knowledge.sqlite` | derived. They follow the store, and DATA regenerates them. |
