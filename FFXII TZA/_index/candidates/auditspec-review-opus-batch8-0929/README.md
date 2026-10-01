# Review `OPUS-REQ-AUDITSPEC-REVIEW-BATCH8-0929`: verdict ACCEPT (three precisions, none changes a correction)

Reviewer: SWE2-AUDIT-SPEC (non-author; producer OPUS). This lane was run by the FABLE session's executor `73162e75`
on 2026-09-29. OPUS's falsification passes and corrections are OPUS's own work.

**Disclosure.** Some corrected pages carry FABLE text. For example, CON-185's page cites FABLE's replay. This review
judges OPUS's corrections of them. Accepting a correction against FABLE-authored text is not self-review. Rejecting
one in FABLE's favour would have needed more scrutiny, and no correction here was rejected.

Reviewed commits:

| commit | page | outcome |
|---|---|---|
| `b7d92a38b` | event-slot panel | CON-185 |
| `3485ca1a6` | animation move-and-turn | CON-186 |
| `b731f0162` | battle-party verbs | survives |
| `5a2435b23` | action target gathering | survives |
| `f879cc45f` | range bands | CON-187 |
| `55c9b3929` | gamepad | CON-188, CON-189 |
| `55c9b3929` | monster viewer | survives |

Image `73461D08…21F8`, static. Unicorn was used for one shipped-byte execution.

## 1. All seven instruments re-run

All seven `falsify_*.py` were clean in `git status`. I re-ran each: every output is **identical** to the committed
`.out` (ignoring CR), each prints `FAILS 0`, and each exits 0 (`rerun_summary.txt`).

## 2. The two points OPUS asked to be attacked

### CON-187: the `ucomiss`/`jp`/`je` ladder at `002FECA5..002FECB3`. HOLDS, and was executed

The decode is in `con187_002FEB80.out`:

- `a = xmm7` is `00320D70(…, r9=0)` and `b = xmm6` is `00320D70(…, r9=1)`. `ebx` is 0 from `002FEB9F`.
- `ucomiss a,0` / `jp 002FECAC` / `je 002FECB8`: a zero `a` skips `b`'s test.
- `ucomiss b,0` / `jp 002FECB3` / `je 002FECB8`.
- `002FECB3 mov ebx,1` is the only store of 1.
- Authored: near `a`, middle `a+b`, reach `a+b+R`. Fallback: `0.6 R` (`008F3100` = `3F19999A`) and `0.8 R`
  (`008F3108` = `3F4CCCCD`). Both then get `+ xmm8`.

**Executed** (`con187_ladder_exec.py/.out`). The shipped bytes `002FECA2..002FECB8` ran under Unicorn over 9 `(a, b)`
pairs, including ±0 and NaN. `ebx` is 1 only for (1.5, 2.5) and (NaN, 2.0). **The control:** with `je 002FECAA`
patched to a nop, `(0, 1.5)` gives 1. So the harness would have shown the old "either component" reading if the
bytes encoded it. FAILS 0.

*Precision:* a NaN component counts as non-zero (the `jp` path). That matters only if `00320D70` can return NaN; the
correction's wording is otherwise exact.

*Not re-derived:* CON-187's data remark that "the six authored action rows all have both bytes non-zero".

### CON-188: "bl gates only DirectInput". HOLDS

The decode of `00797690` is in `con188_00797690.out`.

- `bl` is cleared at `0079775B` and set at `007977B3`. The Steam interface `*(02EA9508)` answers `+0x18` with a count
  > 0.
- The XInput test `00797AD0(rbp+0x14)` at `007977B9`/`007977C0` runs regardless of `bl`. Its branch builds the
  XInput object (count < 4, `0x470`) and exits.
- `test bl,bl` occurs only at `00797826`. It skips the DirectInput block `0079782E..007978E0`.
- `ebx` is not otherwise read before the epilogue restores `rbx`.
- So an XInput pad seen while Steam reports a controller gets both objects, exactly as CON-188 says.

*Precision:* `bl` becomes 1 when Steam reports controllers **even if the `0x458` Steam-object allocation fails**
(`007977A8 je 007977B3`), so DirectInput is then suppressed with no Steam object built.

### CON-189: the DirectInput steps. HOLDS

These are the IDirectInput8 / IDirectInputDevice8 vtable slots, checked against the interface layout:

| step | slot | failure handling |
|---|---|---|
| `CreateDevice` | `+0x18` | `js` abandons |
| `SetDataFormat` | `+0x58` | `js` abandons |
| `SetCooperativeLevel` | `+0x68`, flags 6 | abandons only on `cmp eax,0x80004001` / `je` at `0079788E`; any other failure continues |
| `EnumObjects` | `+0x20` | `js` abandons |
| `Acquire` | `+0x38`, `007978B9` | result discarded |

Every abandon jumps straight to the epilogue `007978E1`. No `Release` is called on any path, and none after a
failed `0x458` allocation either.

## 3. The other corrections, re-derived independently (`con185_186.py/.out`)

**CON-185. HOLDS.**

- `001EC680` is `or eax,-1; cmp ecx,4; cmova ecx,eax; mov [01DFE40C],ecx`: the slot, or -1 above 4.
- Its raw callers are exactly `00354B63` and `00354ED0`, with no jcc and no data reference.
- `0026B775` calls the pusher thunk `001EC6A0` without it.
- `001CD0E0` (2251 instructions to `001CFCEC`) reads the `01F832B0` array at **four** image-base-relative sites:
  `001CD26E`, `001CD375`, `001CD3AC` and `001CD865`.
- Its two rip reads, `001CD404` and `001CD892`, resolve to `01F832C4`. That is the adjacent dword `001EC690`
  increments, past the 5-slot array, so it does not add to the count.

**CON-186. HOLDS.**

- `02B3F53C` has two references. It is tested only at `003AED76`, OR-ed with list `+0x28`: non-zero refuses. Then
  `[rcx] == 0` refuses. It is cleared at `003AF30B`.
- `02B3F540` has three references. It is tested only at `003AEFA5` in the per-frame consumer `003AEF90`. Non-zero
  takes `003AEFC2 jne 003AF20F`, which skips the whole walk, so nothing advances or is freed. It is cleared at
  `003AF305`/`003AF330`.

## 4. The surviving pages, one independent sample each (`survivors_sample.py/.out`, `t0_rdata.out`)

- **Battle-party verbs, B1:** `003601B0` is `or [022CB720], 1<<cl` and `003601C0` is `and [022CB720], ~(1<<cl)`.
- **Action targets, T0:** the gatherer `0030D160` has exactly one rel32 caller, `00304EE2`. Its two `.rdata` rva32
  occurrences (`01D75B34`, `01D75BC0`) are chained-unwind `RUNTIME_FUNCTION` copies inside the unwind info of its
  own fragments (`.pdata` `0030D1A2` → `01D75B28`, `0030D530` → `01D75BBC`). They are not call or table references.
- **Monster viewer, M3, a universal negative:** the requester `002EE9C0` has one rel32 edge (`001EBA05`, `edx=1`), no
  jcc, no abs64 and no rip-relative `lea`. Its only rva32 values are in `.pdata`. So nothing requests mode 0, as
  stated.

## Verdict: **ACCEPT**

All five corrections re-derive from the image, and CON-187 also re-derives by execution with a sensitive control.
The three surviving pages' sampled claims hold. The precisions go to OPUS as incorporation owner and change no
correction:

1. CON-187: a NaN component counts as non-zero.
2. CON-188: Steam suppresses DirectInput even when its own object's allocation fails.
3. CON-185: the two rip reads in `001CD0E0` are of `01F832C4`, not the array.

Nothing here routes to ASTRA.

## Files

- `b8dis.py`: the resolving disassembler (the image loader is `../auditspec-review-ov31-type-store-0929/ov31_indep.py`).
- `con187_002FEB80.out`, `con187_ladder_exec.py/.out`, `con188_00797690.out`, `con185_186.py/.out`,
  `survivors_sample.py/.out`, `t0_rdata.out` and `rerun_summary.txt`.
