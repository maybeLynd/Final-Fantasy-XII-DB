# SD-5: can a one-shot display request stay set and hold back the keyboard pass? (OPUS, 2026-09-30)

Register row SD-5 was registered by SWE2-DATA (`f7a3292bd`, input-stack-device-channel-and-bindings.md §5). The
keyboard transition pass (`0079C259` → `0079D010`) runs only while the application's bytes `+0x1E`, `+0x1F`, `+0x20`,
`+0x21` and `+0x29` are all zero (`0079C240`–`0079C257`, in the framework's per-frame update `0079C140`). This record
is static. The census is `sd5_display_requests.py` (output `sd5_display_requests.out`, control P PASS), built on the
SD-7 application census (`../sd7-slot15-callers-0930/`). Hand reads use `Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**Only one path leaves a request set across frames: `+0x1E` (the resize request) after a failed resize. Every other
set is cleared in the same pass that acts on it.**

| byte | set by (followed routes) | cleared by (`0079C140`, the same pass) |
|---|---|---|
| `+0x1E` | start-up `0079F150` (`0079F19E`, = 1); the per-frame update's screen-mode change `0079C4B5` (= 1, with `+0x20` cleared) | `0079C54E`, **after** app slot 9 (resize, `0079C526`) returns 0 |
| `+0x1F` | none found | `0079C55D`, after `0079F750` |
| `+0x20` | base-class slot 12 `007A0B10` (= 1) | `0079C4AB` / `0079C4B1` |
| `+0x21` | base-class slot 13 `0079F140` (= 1) | `0079C57B`, after `0079F0F0` |
| `+0x29` | base-class slot 18 `007A1180` (= 1) | `0079C5BF` |

- **Slots 12, 13 and 18 are never called on any route to the application** that the SD-7 census follows. That census
  finds callers for slots 1–9, 14, 17, 20, 25 and 30 only. Nothing calls these setters directly either.
- **The one surviving path.** When `+0x1E` is set, the pass stores the new size (`+0xD24` / `+0xD28`) and calls app
  slot 9 (`0079C526`). The game's slot 9 `0017D0C0` tail-jumps to the base `007A05D0`. That returns non-zero when the
  device resize (`006278B0`) or the renderer resize (`0060F6B0`) fails. The pass then logs `"App failed during resize
  with error"` and returns at `0079C549`, before the clear at `0079C54E`. So `+0x1E` stays 1, and every later frame
  skips the keyboard pass until a resize succeeds.
- **A census hit that is not the application.** `007A07C0` (the window procedure's `WM_SIZE` handler, `"Call On Size
  %d , %d!"`) stores a dword at `+0x1C` that overlaps `+0x1E`/`+0x1F`. Its object is the window data, which
  `0079B300` sets with `SetWindowLongPtrA(hwnd, GWLP_USERDATA, rcx)` at `0079B6EA`. That `rcx` is a stack object of the
  framework main `007980A0` (`lea rcx, [rbp − 0x40]`, `00798616`, via `0079E520`), not the application. The census took
  every `GetWindowLongPtrA` result as the application, an over-approximation carried from SD-7.

**For the player:** the keyboard can stop working only while the game is failing to resize its display device, for
example after a failed full-screen switch. Otherwise a display request lasts one pass.

## Limits (OPUS)

- **Runtime-dependent.** Whether a resize fails depends on the display device, so this is not measured here. Nor is
  whether the run loop continues after the per-frame update returns that error.
- **Holders not followed:** the census's application-pointer limits carry over from SD-7 (26 escapes, 34 indirect
  calls).

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
