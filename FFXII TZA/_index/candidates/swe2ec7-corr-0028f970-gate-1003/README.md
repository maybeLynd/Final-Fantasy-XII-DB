# SWE2-EC7 correction: `0028F970` returns early on bit 13, and its `00273A20` argument comes from `[0209BE80]`

SWE2-EC7 (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Owner correction of SWE2-EC7's own 2026-09-18 sentence on `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md` (found by the EC7-220 helper while reading the sibling `0028F6A0`)

affected: 13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md

## SWE2-EC7 what was wrong

The section "Interior citation — frontier hub `0028F970`" said the function "requires bit `0x2000` of
`[0209BE80]+0x10F68`" and calls "`00273A20([0209BE78]+0xAB30)`". The bytes say otherwise:

```
0028F974 mov rax, [0209BE80] / 0028F97E je epilogue       ; null object returns
0028F980 mov ecx, [rax+0x10F68]
0028F986 bt ecx, 0xd / 0028F98A jb 0x28f9db                ; bit 13 SET -> epilogue (return)
...
0028F9B6 mov rcx, [0209BE80] / 0028F9BD add rcx, 0xab30 / 0028F9C4 call 0x273a20
```

- The bit-13 test is an early-out: the body runs only when the bit is clear.
- The `00273A20` argument is formed from `[0209BE80]`. `0209BE78` does not occur in the body.
- The rest of the sentence holds: the clears of `0x10` and `0x400`, word `+0x10FA0` zeroed, and `+0x10CFC |= 0x40` on
  success.
- Both clauses are revised-here, with the old text struck.

## SWE2-EC7 control

`check.py` (this folder) decodes `0028F970` from the certified image, with the hash asserted. It reports the
instruction after `bt ecx, 0xd` and the rip source of `rcx` before the `00273A20` call. It passes only if the
corrected reading holds (`jb` to the epilogue, `[0209BE80]`), and only if both old readings are refused: a `jae`
early-out for "requires", and the cell `0209BE78`.

run: check.py at 8f77943d0 -> `corrected (set bit returns; [0209BE80]): True; old 'requires the bit': False; old cell
[0209BE78]: False`, PASS.

## SWE2-EC7 consumer check

- A grep of the database for `0209BE78`, and for `0028F970` beside "require" or `0x2000`, finds only this section,
  which is revised-here.
- The new EC7-220 row for the sibling `0028F6A0` reads the same bit 13 as an early-out, so it agrees.

## SWE2-EC7 limits

Static only. What bit 13 means is not re-derived here.
