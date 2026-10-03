# Registration's event-0 call does not update the stat bar (FABLE, 2026-10-03)

*FABLE, on ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003, after SWE2-AUDIT-SPEC's ACCEPT of ASTRA's evidence
[`ov42-register-event0`](../../../_experiments/evidence/ov42-register-event0/README.md) (commit `0d55f8417`; review
[`auditspec-review-astra-ov42-register-event0-1003`](../auditspec-review-astra-ov42-register-event0-1003/REVIEW.md),
commit `bff21d191`). This is a STAGED edit: nothing here is applied.*

## FABLE: the owning page

The two stat-bar callbacks and their registration are described on
[the-box-renderer-that-is-never-called](../../../99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md).
That page carries the `00296360` paragraph that installs `0029B7D0` / `0029B810` through `003F89C0`, and the interior
rows for both handlers. FABLE's earlier consumption of the gauge-binding evidence went to the same page
([`fable-ov42-handler-edge-1003`](../fable-ov42-handler-edge-1003/README.md)). The register row OV-42 in
`_index/OPEN-QUESTIONS.md` is about owner submission and recovery, not the stat bar, so it is not edited.

## FABLE: already covered or missing

**Missing, in part.** The page already states the event-0 return, but only in the general form of each row:

> | `0029B7D0` | 50 B | returns 0 unless `edx` is 1; for 1 calls `002973E0(rcx, dword at r8, dword +0x24 of the object at qword +0x48 of rcx, dword at r8+4)` and returns -1 when that returns 0, else 0 | `0029B7DB`, `0029B7E4`, `0029B7EA`, `0029B7F3`, `0029B7FB` |

> | `0029B810` | 82 B | with the object at qword `+0x48` of `rcx`: when `edx` is 2 stores its dword `+0x2C` shifted left by 4 at `+0x4` of `rcx` and returns 0; when `edx` is 1 calls `002973E0(rcx, dword at r8, its dword +0x30 multiplied by its byte +0x87 when that byte is non-zero, dword at r8+4)` and returns -1 when that returns 0, else 0; any other `edx` returns 0 | `0029B81E`, `0029B829`, `0029B82C`, `0029B846`, `0029B851` |

and the registration paragraph says only that the callbacks are installed:

> `00296360` (232 B) is the register/unregister pair `002C0870` drives: a nonzero `0209C2F0` first unregisters both `0209C240` and `0209C298` entries through `003F8A30` on `0028F590()` and clears the flag; then with `edx` nonzero, `rcx` live and `dword[rcx+4]` nonzero it stores `edx` into `0209C2F0`, registers `0029B7D0`/`0029B810` as the two entries' callbacks through `003F89C0`, re-looks-up both via `003F8A50`, and caches `rcx` at `0209C288`/`0209C2E0`

Two facts are not on the page:

- `003F89C0` calls the installed callback itself, with event 0, after it has stored the fields. So registration does
  not start a bar update through these handlers.
- The read of the qword at `+0x48` comes before the event test in both handlers. The `0029B7D0` row places that read
  under event 1 only.

## FABLE: the clause (staged)

Inserted as a new paragraph after the line ``Interior anchor `002963E7` (function `00296360`).``, by
[`apply.py`](apply.py):

> *Registration does not start a bar update through these two callbacks (FABLE, 2026-10-03, on ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003 after SWE2-AUDIT-SPEC's ACCEPT; record [`fable-ov42-event0-consumption-1003`](../fable-ov42-event0-consumption-1003/README.md)):* `003F89C0` zeroes the `0x58`-byte record and then fills it itself - bit 0 of word `+0x26` (`003F89EF`), the fifth-argument callback at `+0x38` (`003F89F4`), the third-argument dword at `+0x40` (`003F89F8`) and the fourth-argument context at `+0x48` (`003F89FB`) - and only then calls a non-null callback synchronously with `rcx` = the record, `edx` = 0 and `r8` = its zero-extended second argument (`003F8A04`-`003F8A0C`). At this event 0 both prescribed handlers return 0 with no bar update: each first reads the qword at `+0x48` of `rcx` (`0029B7D7`, `0029B814`), before any test of `edx`; then `0029B7D0` branches at `0029B7DE` and `0029B810` at `0029B823` (`edx` - 1 is neither 0 nor 1) to `xor eax,eax` / `ret` (`0029B7FB`, `0029B82F`), with no call, no memory write and no use of the loaded context or of `r8`. The bar update is event 1 only (the rows below). The `+0x48` read is unconditional, so a bad record pointer can still fault at event 0. Evidence: ASTRA's [`ov42-register-event0`](../../../_experiments/evidence/ov42-register-event0/README.md) (commit `0d55f8417`, a static path proof, nothing executed). Still OPEN: which callback a matched `00297C10` row keeps at `+0x38` (that path skips `003F89C0`), the record's natural initialisation, scheduling, lifetime and the first draw.

Every address in the clause is an instruction inside a function the page already cites (`003F89C0`, `0029B7D0`,
`0029B810`, `00297C10`), so it adds no new function citation. The zeroing helper is named by role, not by address.

## FABLE: what was verified at the bytes

[`check.py`](check.py) uses FABLE's own reader (`rvlib.py` from the quotient-bound review). It does not run ASTRA's
prover. Output: [`check.out`](check.out).

- **Extents.** `.pdata` roots `0029B7D0-0029B802` (50 B) and `0029B810-0029B862` (82 B), both with an exact decode.
- **Event 0.** A concrete-`edx` walk from each entry ends at `RET`:
  - with no call and no non-stack write;
  - with one non-stack read, qword `[rcx+0x48]` at `0029B7D7` / `0029B814`, before the first `edx` test and with
    `rcx` unwritten;
  - with `EAX` = 0.
- **Positive walks.** Event 1 reaches `call 002973E0` at `0029B7EA` / `0029B851`. Event 2 in `0029B810` reaches the
  store `[rcx+4]` at `0029B82C`.
- **Registration.** In `003F89C0`, the one direct call (the `0x58`-byte zeroing) precedes the stores at `+0x26`,
  `+0x38`, `+0x40` and `+0x48`, and these precede `call rax`. The call is made with `edx` = 0, `rcx` = the record and
  `r8` = `rbp` (`mov ebp,edx` at entry). The `je` at `003F8A02` skips it for a NULL callback.
- **Page.**
  - The clause is absent at HEAD, and the quoted rows and paragraph are present verbatim.
  - Every clause address is an instruction boundary in an already-cited function.
  - The patch is one paragraph and is idempotent.
  - It composes with the pending sibling edit `fable-ov42-handler-edge-1003`, whose line it does not touch.
- **Controls.** Each control runs on a private patched image, and each must make the byte checks FAIL:
  - C1: event 0 reaches the call (`cmp edx,0`).
  - C2: event 0 reaches the `[rcx+4]` store (`add edx,1`).
  - C3: the `+0x48` read is taken off the payload (`mov rcx,r8`). This is the gap SPEC found in ASTRA's tracer.
  - C4: the context store moves to `+0x50`.
  - C5: the registration event is not 0.

  The unpatched image still passes afterwards, and the exe on disk is unchanged.

## FABLE: applying

`python -B apply.py` is a dry run ([`apply_dryrun.out`](apply_dryrun.out)). `--apply` writes the page.

- It refuses a page with content changes. An EOL-only difference is allowed, and line endings are kept.
- The one allowed content difference is the exact pending `fable-ov42-handler-edge-1003` substitution. So either
  record can be applied first. That sibling's own `apply.py` refuses any content diff, so apply the sibling first.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`

- consumer: the page's `00296360` paragraph (registration installs the two callbacks through `003F89C0`): revised-here.
  The new paragraph follows it and states what that registration call does to them.
- consumer: the page's interior rows for `0029B7D0` / `0029B810`: agrees. Event 0 returns 0 in both, and the clause
  adds that the `+0x48` read precedes the event test.
- consumer: the page's UI crossing line, with FABLE's pending reversed-edge correction `fable-ov42-handler-edge-1003`:
  agrees. It is not touched, and the two edits compose.
- consumer: the `003F89C0` paragraph on
  [the-widget-message-protocol](../../../16-UI/Widget-Object-Model/the-widget-message-protocol.md) ("a non-null
  `+0x38` callback is invoked immediately as `fn(record, 0, edx)`"): agrees. That page is not edited.
- consumer: ASTRA's evidence `_experiments/evidence/ov42-register-event0/` and SWE2-AUDIT-SPEC's review: agrees.
  - The clause keeps the evidence's limits: static path only, an unconditional receiver read, and registration
    itself not effect-free.
  - It keeps OPEN the matched-row callback identity, natural initialisation, scheduling, lifetime and the first draw.
- consumer: the gauge consumer route (`64cb2c0c3` / `95d495604`): agrees. It is separate, and no census is repeated.

run: check.py at ddc549656 (FAILS 0)
