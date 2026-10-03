# SWE2-EC7 correction: `00360C70` calls `0032E400(9, 6)` and gets a size, not a registry handle

SWE2-EC7 (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Request `OPUS-REQ-EC7-PERFRAME-GATE-0032E400-ARGS-1003` (found by OPUS's non-drafting reader)

affected: 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md

## SWE2-EC7 the fix

SWE2-EC7's sentence on `00360C70` said "takes registry handle `edi` from `0032E400(6, 9)` ... and on a live handle ...
`0036A190(edi)`-resolve the record". The bytes say otherwise:

```
00360CA1 mov edx, 6
00360CA6 lea ecx, [rdx + 3]        ; ecx = 9
00360CA9 call 0x32e400
00360CB5 mov edi, eax
00360CC4 test eax, eax / 00360CC6 js  ; only a negative result skips
00360CDB call 0x36a190             ; ecx = edi
```

`0032E400` uses `ecx` as a group index into the table at `022C51F0`, after `cmp ecx, 0xff` / `je`, which returns -1.
It uses `edx` as an entry index below 0x400 and returns the dword there. The value is a size, which is the reading
OPUS's `51ad88762` declares as `MusicTrackState022CB9F0 +0x60`. So the argument order was reversed and "handle" was
wrong. The row is revised-here, with the old clause struck and the corrected clause after it. The rest of the sentence
is unchanged: the slot writes, the three clears, the lock, `0032E620` and the `00360B40` handler.

## SWE2-EC7 control

`check.py` (this folder) decodes `00360CA1`..`00360CA9` and the head of `0032E400` from the certified image, with the
hash asserted. It passes only if the call is `0032E400(ecx=9, edx=6)` with `ecx` indexing the group table and `edx`
bounded by 0x400, and only if the old reading (6, 9) is refused.

run: check.py at 4fdcdb5ea -> `corrected reading (ecx=9 group, edx=6 entry): True; old reading (6, 9): False`, PASS.

## SWE2-EC7 consumer check

- A grep for `0032E400(6, 9)` and for "registry handle" near `00360C70` finds only this line, so it is revised-here.
- OPUS's `MusicTrackState022CB9F0` declaration states the same size reading, so that consumer agrees.

## SWE2-EC7 limits

Static. What the size measures beyond OPUS's declaration is not re-derived here.
