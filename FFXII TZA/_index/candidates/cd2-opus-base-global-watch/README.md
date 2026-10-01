# CD-2: the base global `01F83530`, watched through the boot and bounded by its neighbour (OPUS, 2026-09-26)

**Evidence classes: STATIC and NATIVE-REPLAY. `live_game: false`.**

CD-2 asks whether anything writes `01F83530` at run time. It is FABLE's narrowed row: zero at image load, and one
in-image store route (the texture-id writer `00210570`, signed bound, id `0xFFFB`) that is undriven, not absent. This
package adds three measurements and changes none of that.

| case | observed |
|---|---|
| `C1` | **STATIC.** `01F83530` lies in `.data`'s zero-fill tail and starts at 0. The census decodes every rip-relative disp32 in `.text` at every candidate length. The only instructions naming the global are the reads `0020E602` `add rax, [01F83530]` and `0020E620` `sub ecx, [01F83530]`. No `DIR64` relocation points into `01F83500`–`01F83560`. |
| `C2` | **STATIC. The object just below cannot reach it.** `AmdAdapterInfo` at `01F83460` is `0xD0` bytes and ends exactly at `01F83530`. It has vtable `009064B8`, is constructed by `0020D2F0` from the initialiser at `0015DC84`, and is destroyed by `008A7360`. Its constructor zeroes `+0x08`–`+0xCF` with qword, dword and byte stores. The only bytes it skips are `+0x29`–`+0x2B`, the alignment padding after the byte at `+0x28`. No displacement at or past `0xD0` off a base register appears in its constructor, destructor or three virtual slots. The one `lea rdx, [rax + 0x118]` in slot 1 is off a loaded record pointer, not `this`. |
| `C3` | **NATIVE-REPLAY.** In the [S-15 boot world](../s15-opus-replay-boot-world/), a write-watch on `01F83530`–`01F83537` and an entry hook on `00210570` are armed before the CRT runs. The world covers the CRT tables, main, app slot 2, the init job, the save reset, UI message 16, two field-script binds and the field-pass frames. **No write occurs, `00210570` is never entered, and the value at the end is 0.** |

**What it settles.**
- The neighbouring static object is ruled out as a writer: it ends exactly where the global begins.
- The replayed start-up leaves the global at zero, and the only known store route is never reached there.

**What it leaves.** Whether some later run-time state drives `00210570` past its shipped id range is still
live-only, as the row says.

**Run:** `python check.py` (about 15 minutes, because C3 runs the boot world). It needs the sibling
`s15-opus-replay-boot-world` package and everything that package needs.
