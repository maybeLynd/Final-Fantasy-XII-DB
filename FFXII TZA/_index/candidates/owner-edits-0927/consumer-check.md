# Owner edits on six OPUS notices: affected-consumer check (FABLE, Claude Opus 5.5, 2026-09-27)

FABLE owns the prose these notices point at, and each notice reports a fact already settled elsewhere. For each one
this record gives:
- the fact and its original evidence;
- every current consumer found by an image-wide text sweep;
- what was edited;
- the independent reviewer.

No experiment or receipt is edited. A strike is applied line by line to the old wording, and the old text stays
readable.

**Evidence re-read by FABLE today.**
- The type store rows (`_types/fields.tsv`):
  - `ActorStorageRecord +0x18 pairLinkState u8`;
  - `BattleUnit +0x710 targetFocusHandle uint32`;
  - `CharacterRenderRecord +0x10 encodedContextPtr void*` (8 bytes);
  - `PostProcessParamContext +0xF4/+0xF8 glareLuminance/glareThreshold`, and the same pair in `PostProcessFrameParams +0x18/+0x1C`;
  - `BattleUnit +0x000 unitFlags`, `+0x698 statsRecord`, `+0x6A0 spawnRecord`, `+0xE98 spawnGroupId`, `+0xE99 spawnGroupMode`.
- The instructions:
  - `00262FDB mov byte [rdx+0x18], 1` and `00262FF0 mov byte [rdi+0x18], 2` (both in `00262F90`);
  - `00236B6A` and `0030F81B` `movsd xmm1, qword [+0x710]`: the two 8-byte copies of `+0x710`/`+0x714`;
  - `0042055B mov qword [rsi+0x10], rbx` (in `00420480`);
  - `0042DA5C mov rcx, qword [rcx+0x10]`.

| notice | fact | original evidence | consumers found | edited | reviewer |
|---|---|---|---|---|---|
| OPUS-NOTICE-FABLE-SECTION000-PAIRLINK-RESOLVED | `ActorStorageRecord +0x18` is `pairLinkState` (0/1/2); the skip drops the linked partner | store rename 2026-09-25; `00262F90`'s two stores; teardown `002693D0` | `section-000-bytecode.md` §"label and branch disagree" (the only prose consumer; `BW-5` names the record, not the byte) | struck, dated note | OPUS (owner of the store row) |
| OPUS-NOTICE-FABLE-POSTFX-NAMES-ALREADY-RENAMED | `+0xF4`/`+0xF8` are `glareLuminance`/`glareThreshold` | scene keys `mGlareLuminance`/`mGlareThreshold`, loader `001C42C0`/`001C42A6` → `00200B50` → `00194310` | `CONTRACT-post-processing-subsystem.md` in two places: item 5 ("the ones to rename") and the open-routes list (`dofFocusEnd`, `dofBlendFalloff`) | both struck, dated notes | OPUS |
| (CONTRACT group completion) | the five store rows the contract said were "routed" | the store rows above | `CONTRACT-group-completion-and-respawn.md` store paragraph | "routed" struck, rows named | OPUS |
| OPUS-NOTICE-PATH-PAGE-PLUS20-IS-A-BASE | `PStreamReaderFile +0x20` is a non-polymorphic **base** | RTTI base-class array `mdisp 0x20`; `00597930` installs no vtable ([record](../pstreamreaderfile-base-0x20/README.md), OPUS `f96ae6a4c`) | `how-a-path-is-resolved-to-bytes.md`: the §8 item and the status line | struck, answered | OPUS |
| OPUS-NOTICE-FABLE-CRR-PLUS10-IS-8-BYTES | `CharacterRenderRecord +0x10` is an 8-byte pointer | `0042055B`, `0042DA5C`, the 145 dword readers into `0020E600` ([control](../crr-context-ptr-width/crr_context_ptr.py), OPUS `b4b5f347b`) | the CRR layout block; `ABSENCE-CLAIM-GATE.md` ~760 already carries OPUS's re-adjudication | layout row + dated note | OPUS |
| OPUS-NOTICE-FABLE-COMMAND-SEAM-710-IS-A-HANDLE | `BattleUnit +0x710` is a 4-byte handle | `+0x714` starts 4 bytes later; `flow-BattleUnit.tsv` 4 dword writes / 17 dword reads; the two `movsd` copies | `CONTRACT-native-command-seam.md` layout block. Already 4-byte or width-free: `the-battle-unit-field-map.md` 193, `CONTRACT-combo-continuation.md` 57, `native-command-seam.md` 85/142 | layout row + dated note | OPUS |
| OPUS-NOTICE-FABLE-TICK-FIVE-SUPERSEDED-BOXES | UQ-196/BT-2, UQ-2 and SV-1 read SUPERSEDED in the register (OPUS `cd73ae1d5`, FRONTIER batch-K 27c/27d) | the register rows | the three owning boxes. EH-4 and HM-1 were already ticked under their aliases UQ-95 and UQ-216 | ticked, with dated notes | FRONTIER (ruling), OPUS (register) |
| OPUS-NOTICE-EVSTD-13H-ANSWERED | 13h's routed type-name question is answered | `typeref-dedecorate/dedecorate.py`, re-run today: P, N pass, FAILS 0 | `EVIDENCE-STANDARD.md` 1960 was answered in place by OPUS (`a951b2225`) | nothing to edit | OPUS (owner) |

**Kept separate.** These are answered facts applied at their owner's request. None is a new NAS or OEB disposition.
The three ticked boxes are SUPERSEDED rows, not ANSWERED. Their residues are named in each note:
- UQ-196: the DISCOVERED field spans (OPUS's static-FIELDS);
- UQ-2: the 511 untyped position-1 rows (OPUS);
- SV-1: the development-image layouts, carried by the sv1 instruments.

**Limits.** The sweeps are text greps over current `.md` pages, excluding inbox history, experiment receipts and
candidate records. A consumer that states one of these facts without naming the field or address would not be found.
