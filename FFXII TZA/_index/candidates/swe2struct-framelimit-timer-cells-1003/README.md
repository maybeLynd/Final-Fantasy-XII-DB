# SWE2-STRUCT: the FrameLimit timer-period statics (01F82E3C, 01F82E40)

SWE2-STRUCT (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Source: census3 (`_index/candidates/auditspec-census3-1003/`) finding on S-44

## SWE2-STRUCT finding

The game-settings contract's State section says the FrameLimit path writes `0x01DFE0B4/B8/BC` and `0x01F82E38/3C/40`
(`19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md`, the **written** row).
- Four of those six cells were declared: `FrameLimitSetting`, `FrameCountScale01DFE0B8`, `TimeBaseScale01DFE0BC` and
  `FrameRate60Gate`.
- `0x01F82E3C` and `0x01F82E40` were not.
- S-44's types cell is MET under the declaration-granularity criterion, so the two missing rows were a gap in that MET.
  This record closes the gap by declaring them, so the cell stays MET.

## SWE2-STRUCT evidence (raw capstone over the certified image, `.text`, rip- and image-base-relative)

```
001EDE01 cmp byte ptr [01F82E3C], 0        ; 60 fps arm: is a period outstanding?
001EDE0A mov ecx, dword ptr [01F82E40]     ;   its value
001EDE10 mov byte ptr [01F82E3C], 0
001EDE17 call [008C2AA0]                   ;   WINMM timeEndPeriod
001EDE29 call [008C2A90]                   ; 30 fps arm: WINMM timeGetDevCaps(&caps @rsp+0x38, 8)
001EDE3A mov dword ptr [01F82E40], eax     ;   caps.wPeriodMin (low dword of the 8-byte TIMECAPS)
001EDE40 call [008C2A98]                   ;   WINMM timeBeginPeriod
001EDE46 mov byte ptr [01F82E3C], 1
```

- The whole sweep over `01F82E38..01F82E47` finds 19 references.
  - `01F82E3C` has 3 references (1 read, 2 writes), and `01F82E40` has 2 (1 read, 1 write). All five are in `001EDDC0`.
  - The other 14 are the `FrameRate60Gate` write `001EDDE8` and its 13 readers. Those match its declared row, which is the
    sweep's positive control.
- The import names come from the PE import table: `008C2A90` timeGetDevCaps, `008C2A98` timeBeginPeriod, `008C2AA0`
  timeEndPeriod.
- Both cells lie in `.data` past `SizeOfRawData` (raw end `01F7E400`), so they are zero-initialised BSS.
- The page `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md` already describes the same
  logic in prose (L517-L526).

## SWE2-STRUCT store change

- `_types/types.tsv`: `TimerPeriodRaised` (0x1, STATIC 0x01F82E3C) and `TimerPeriodMin` (0x4, STATIC 0x01F82E40), both
  added after `FrameRate60Gate`.
- `_types/fields.tsv`: one field row each, `periodRaised` uint8 and `periodMs` uint32.
- The edit script is `Tools/work/SWE2-STRUCT/standin1003/edit_s44.py` (idempotent). The sweep script is `cellrefs.py`, in
  the same folder.

## SWE2-STRUCT limits

Static only. These rows add no claim about when the 30 fps arm runs at runtime or how often. The remaining census3
findings on other systems are not addressed here.
