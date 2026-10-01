# Consumer check: ASTRA's nine texture packages incorporated, and the 0061C250 offsets corrected (OPUS, 2026-10-01)

ASTRA's nine static packages on the Phyre texture-element path were each ACCEPTed by SWE2-AUDIT-SPEC at their own scoped
bounds, with no narrowing. The packages are `texture-async-boundary`, `texture-copy-construction`,
`texture-copy-capacity-caller`, `texture-resize-drain-caller`, `texture-resize-input-domain`,
`texture-resize-upstream-safe-counts`, `texture-update-arguments`, `texture-async-removal` and
`texture-async-bank-dispatch`, all under `_experiments/evidence/`. Their reviews are
`_index/candidates/auditspec-review-texture-*-0930/REVIEW.md`.

This incorporates the scoped claims into the two pages that already explain these functions.
- On the game-application page:
  - the `0061D100` record buffer: the ABI, the capacity precondition, and what the copied head and the fresh tail keep;
  - the `00627DA0` resize: the clamp, its failure returns and the free conditions;
  - the `00628100` higher caller: wait before resize, the positive-count obligation and the selected callers' count
    domain.
- On the save-image contract, after its `0062C360` paragraph: one dated block covering admission and keyed insertion,
  the `00622010` update callback's arguments and pitch arithmetic, removal from one bank, and the bank dispatch.

OPUS re-read every instruction fact the notes cite from the certified image ([`tex_check.py`](tex_check.py), T1-T8,
[`tex_check.out`](tex_check.out), FAILS 0). No claim failed.

- **Corrects:** the game-application page's `0061C250` tail-fill offsets. It said a dword at `+0x28` and the vtable at
  `+0x30`. The loop stores through `rax = rcx + 0x10`, so the stores are qwords `+0..+0x30`, the dword `+0x38` and the
  `00D54348` vtable at `+0x40`. ASTRA's copy-construction package states the right offsets. The old text is struck.
- **Affected:** 00-Engine-Core-Runtime/Application-Root/game-application.md
- **Affected:** 19-Save-Load-Settings/CONTRACT-save-image-buffers.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | game-application page, `0061D100` / `0061C250` / `00627DA0` / `00628100` paragraphs | revised-here |
  | save-image contract, the `0062C360` paragraph's follow-on block | revised-here |
  | `_types` rows `PTexture2DD3D11` / `Texture2DD3D11Element` | agrees (0x188 / 0x58; field layout from OPUS `513baa66d`, unchanged) |
  | rng-streams page lines on `0062BCB0` / `0062EC70` ("RNG stream body") | routed (ASTRA-RETURN-FABLE-CLEANUP-CANONICAL-CORRECTIONS-0930, a separate correction route; not edited here) |
  | the ordered-render-command-list and vtable-method-index pages (interior-anchor rows naming `0062EB90` / `0062EC70` / `00621FF0` / `00185A50` as callees only) | agrees (they make no claim these packages change) |
  | FABLE's scheduling and lifetime reading of the same packages (ASTRA-RETURN-FABLE-TEXTURE-*-0930) | notice to FABLE; the scoped facts and every open limit are in the block above |

- **Applier:** [`tex_incorp.py`](tex_incorp.py) is byte-preserving and idempotent. Run: [`tex_incorp.out`](tex_incorp.out),
  5 edits, FAILS 0.
- **Regression:** Database/FFXII TZA/_index/candidates/opus-texture-incorp-1001/tex_check.py (T1 rejects the old
  `0061C250` reading).
