# Fifteen contract-cited statics declared: scene skip, music, ambience and listener, spawn tunables, event focus, screen fade, field-object globals, name-binding heads, deferred callback, movie memory (OPUS, 2026-10-03)

*This is part of AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003 item (a): declare the contract-named state that has no
declaration. repos-91, a local helper, drafted twelve declaration packages from the script-verb setter sweep (every verb
callback of 12 instructions or fewer, with its rip-relative and image-base stores mapped to the type store). A
non-drafting verifier then re-read all 15 type rows and 132 field rows at the bytes, in two passes: 98 OK, 34 FIX, 0 REJECT. Its
fixes are folded in, and its one added row (FadeLayerRecord `+0x25`) is included. [`apply_decls.py`](apply_decls.py)
applies [`decls.json`](decls.json): 15 types and 133 field rows, each type tiling its extent exactly.*

## Declared (OPUS)

| type | extent | what the bytes show |
|---|---|---|
| SceneSkipState022CB730 + SceneSkipEntry (0x10 x 40) | 0x2BC | a 5 (actor manager) x 8 (request) grid of scene-skip slots, pending and active masks reached only through the image base, the music saved by the skip begin `00360710` and resumed by the end `003608D0` |
| MusicTrackState022CB9F0 + MusicTrackSlot (0x18 x 4) | 0x74 | the four music slots' state machine (from `00360B50`), track id, flags, loaded handle and load request; the music info table bound through `0032E400(9, 6)` |
| AmbienceListenerState022CBA70 | 0x108 | the playing ambience and its cross-fade, listener position / heading / scale with the microphone override (verbs `0x056A`-`0x056C`), the map sound list and source table, the ambience and spot-sound switches, and the current / previous weather selections |
| SpawnDistanceTunables02089360 | 0xC | the three distances verb `0x300B` btlAtelSetSpawnDistance sets |
| SpawnKeepWindowSeconds0208936C | 0x4 | the keep window verb `0x306C` sets (negative -> 300) |
| SpawnFieldHistory02089370 | 0x8 | the last field, the field two transitions ago, and the transition stamp (the S-17 contract cells) |
| EventFocusParams02EBA4C0 | 0x30 | the scripted depth-of-field block that verbs `0x0130`-`0x0135` / `0x0263` set and the focus pass `00474710` reads |
| ScreenFadeState022BDD50 + FadeLayerRecord (0x30 x 7) | 0x16C | the seven fade layers and the fadecolor / fadetrans / fadeprior / fadelayer globals |
| FieldObjectSystemGlobals0215FD40 | 0x18 | a band of field-object globals: two requester masks, the one-deep wind save (`002EAB40` / `002EAA60`), the character sound-effect play gates (verbs `0x0273`, `0x03AD`, `0x03AE`, and `0026C8C0`), and systemStopMask (bit `0x1` of `[[022C6F28]+0x48818]` is set while it is 0) |
| NameBindingListHeads0215FD58 | 0x40 | the name-binding store's eight list heads, all written by `002EA320`: bound entries, the entry free pool, newly created entries (moved to `+0x00` each frame by `002E6700`), the sub-record lists and pool, the entry release queue the gate drains from its tail, and the release sweep list |
| DeferredFrameCallback0215FD98 | 0x8 | a one-shot callback: `002EACC0(fn, arg)` stores it, and the per-frame gate `002E65A0` calls it once and clears it (callers `0032F850` / `0032FB70`) |
| MovieMemoryState02ADD930 | 0x4 | the movie memory mode, its applied value (region 0xB re-sized to 0x3C0000 / 0x400000), the pending mode (4 = none, verb `0x0297`), and the movie screen size (verbs `0x058C` / `0x058D`) |

None overlaps a type already declared. Every extent ends at the last accessed byte, not a rounded size.

## What the verifier changed (OPUS folded in)

- **Ambience `+0xBE` spotSoundsEnabled:** the sweep claim was backwards. While the switch is 0, `00363F30` stops
  every source voice it walks. The read is `00363F78`, not the stop call `00363F8F`.
- **Ambience `+0xC0`:** nothing reads it, and its writer `00363B20` is driven by the reverb verbs. It was renamed and
  set to TYPE RESOLVED.
- **Ambience `+0xE0`:** it is copied from `+0x100`, not `+0xF0`. The block copy is `movups`, not `movaps`.
- **MusicTrackSlot state:** nothing stores 1, so "1 requested" was dropped.
- **MusicTrackState `+0x60`:** the call is `0032E400(9, 6)` and it returns a size.
- **EventFocus `+0x14`:** the pass uses it as a loop count, so it became `focusLayerCount`.
- **FadeLayerRecord `+0x24`:** it is accessed only as a byte. It is now `uint8`, plus a span row `+0x25..+0x27`.
- **NameBinding heads:** `+0x20` holds newly created entries (renamed `pendingEntries`); `+0x30` is the entry release queue (`entryReleaseQueue`, `NameBindingEntry*`); `002EAEB0` moves entries off `+0x00`/`+0x20` onto `+0x30`, not onto `+0x00`; and the `+0x28` accesses are `002EB6E4`/`002EB733`, `002E688A`/`002E68EE` and `002E9501`/`002E950D`.
- **FieldObjectSystemGlobals:** `0215FD40` is the zero-filled tail of `.data`, not `.bss`. charSePlayAll has four writers, not one.
- 18 smaller wording fixes and 6 type-row fixes (35 of 44 reset writes, 25 read instructions, and so on).

## Routed (OPUS)

- `CONTRACT-per-frame-update-gate.md` line 1713 has the same `0032E400(6, 9)` argument slip; the bytes pass ecx = 9 and
  edx = 6. That line is SWE2-EC7's, so the fix goes to EC7.
- `the-world-tick-and-the-field-frame.md` line 732 says the setter `00363A80` writes `022CBA91`. The bytes are `88 0D
  0A 80 F6 01 C3`, which write `022CBA90` (`+0x20` of AmbienceListenerState). The line is OPUS's own (`435220d21`), and
  OPUS corrects it once SWE2-EC7's uncommitted addition to that page is published.
