# SWE2-AUDIT-SPEC review of SD-100 (sd100-reveal-modes-0930, OPUS, da3426b96): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `da3426b96` (the record's only commit), [README](../sd100-reveal-modes-0930/README.md) and `sd100_modes.py`,
measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD100-0930 | sd100-reveal-modes-0930 | `da3426b96` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd100_modes_b58c633f7.out](rerun_sd100_modes_b58c633f7.out) is identical to the committed `.out` (CR
ignored), M1-M6 PASS, `FAILS 0`. The earlier worker's [rerun_sd100_modes.out](rerun_sd100_modes.out) at `3cae47364`
was also identical. Package dir clean after re-run: yes. No `__pycache__` was created by these runs.

**Re-derived independently.**
- **Dispatch** ([stepper_dis.out](stepper_dis.out), lane `b8dis.py`). `002ABF79` loads the dword `+0xB0` and
  `002ABF7F` takes `cl`. `002ABF82 cmp eax, 7` / `ja 002AC1AB` means any mode above 7 also exits. The 8 dwords at
  `002AC1B4` plus the image base decode to `002AC06B 002AC06B 002AC04F 002ABF9F 002AC06B 002ABFFC 002AC1AB 002AC18B`,
  which is M1 exactly.
- **Arms. M1-M6's cited instructions are right. Four readings in the "what it does / on screen" table are not:**
  - **Modes 0/1/4 (`002AC06B`), the paging trigger.** The branch to the page path tests the speed byte
    (`002AC06B movzx eax, byte [rbx+0x9c]` ... `002AC078 cmp al, 0x1e` / `jne 002AC0DC`). It is taken when `+0x9C` is
    30, not "when a line is full". It then pages when `+0xA0` > 1 (`002AC07C`/`002AC083 jg`), or when `00248F20` returns
    1. `00248F20` returns 2 exactly when `00229EA0` (the signed byte `[02064AD3]`) is 2, and 1 otherwise
    (`00248F24`..`00248F31`).
  - **Modes 0/1/4, the page path.** It copies `+0x8C` to `+0x8E`, zeroes `+0x9B` and calls `002ABB20`. `002ABB20`
    advances the head `+0x8C` (`002ABE71`, `002ABE9D`, `002ABEAD`; [abb20_dis.out](abb20_dis.out)): this is the scroll
    step that stops at a `#` page wait, per SWE2-DATA's page §4. After the call it sets `+0x90 = +0x8C` and the lag
    `+0x9D = 0` (`002AC0B8`, `002AC0BF`). **`0x7D00` is an upper clamp on `+0x8C`** (`002AC0C6 cmp` / `jle` /
    `002AC0CF` store), not a "restore".
  - **Modes 0/1/4, the normal path (`002AC0DC`).** Once `+0x9B` reaches 30, `+0x9B` is zeroed. The lag `+0x9D` moves
    by `+0xA0` toward `+0x9E` (`002AC10C`..`002AC129`). `+0x90` steps by `+0xA0` only while `+0x90 <= +0x8C - +0x9D`
    (`002AC144`, `002AC148 jg`). **The head `+0x8C` always advances by `+0xA0`**, clamped at `0x7D00`
    (`002AC16E`..`002AC17E`). The README's row never mentions the head.
  - **Modes 3 and 5.** Both step `+0x90` only while `+0x90 < +0x8C` (`002ABFD1`/`002ABFD8 jge`, `002AC024`/`002AC02B jge`)
    and neither writes `+0x8C`. They catch the target up to the head and never move the head. Mode 3 also exits without
    stepping when `+0x88` is already 0 on entry (`002ABFA6`/`002ABFA9 je`).
  - Modes 2, 6 and 7 are as the README says, and so is "mode 5 never reads `+0x88`" (no `+0x88` operand in
    `002ABFFC`..`002AC04E`).
- **Mode-byte writer census, done independently of `pe.funcs` and the package regex** ([sd100_census.py](sd100_census.py) /
  [.out](sd100_census.out)).
  - Method: a raw disp32 search for every displacement `0x91`..`0xB0`, back-decoded, taking every base (rsp and rbp
    included) and every mnemonic capstone marks WRITE, of any width covering byte `+0xB0`.
  - Totals: 931 writes and 1487 reads cover the byte. The package's 20 stores are 20 of 20 and the read `002ABF79` is
    present (controls). 909 writes can change the low byte.
  - These are the corrected counts. capstone 5.0.7 marks a `movups` memory destination as READ, and my first run
    trusted that flag and gave 861 writes
    ([sd100_census_v1-capstone-movups-blind.out](sd100_census_v1-capstone-movups-blind.out)). The fix, found through the
    SD-105 review's control `002A48C5`, adds 68 `movups` stores and 2 `vmovaps` stores image-wide and none in the text
    cluster. The embedded and offsets sweeps below were re-run with the same fix. Only the count of writes outside the
    cluster changed, from 217 to 243.
  - In the text cluster `0029E000`..`002B6000`, the only writes outside the package's 20 are 15 dword stores. I read all
    15 ([sd100_ctx.out](sd100_ctx.out), [dwordrmw_dis.out](dwordrmw_dis.out), [pager_dis.out](pager_dis.out),
    [parser_dis.out](parser_dis.out)). Each is a read-modify-write of the dword it loaded from `+0xB0`, touching bits
    17-31 only, so each keeps the low byte. One case needs care: `002A9877` stores `r14d`, loaded at `002A9066`, and on
    that path `002A9824 test r14b, r14b` / `jne` has already required the mode to be 0.
  - **The two "variable" stores are constant 0.** `002A9A27 mov byte [rcx+0xb0], dil` follows `002A9A00 xor edi, edi`,
    and nothing between them writes `edi`. `002B3963 mov byte [rcx+0xb0], al` follows `002B395A xor eax, eax`.
- **Writers the +0xB0 census cannot see: elements addressed at an offset** ([sd100_instances.py](sd100_instances.py),
  [sd100_embedded.py](sd100_embedded.py), [sd100_offsets.py](sd100_offsets.py) and their `.out` files).
  - The message window keeps its element at `+0xD0`. `002A6190` passes `lea rcx, [rdi+0xd0]` (`002A6348`) and loads
    `lea rsi, [rcx+0xd0]` before its own mode-6 store at `002A67DB`. `002A3730` passes `rdi+0xD0` to `002B3950` and
    switches on `byte [rdi+0x180]` (`002A3790`). So window `+0x180` is the element's mode byte. Three more writers
    address it that way:
    - `002A6190` at `002A6606 mov byte [rdi+0x180], 1` sets **mode 1**, after saving the old mode at `+0x181`
      (`002A65F9`, `002A6600`). This happens when `[rdi+0x7C] & 0xF` is 3 (`002A65EA`..`002A65F7`), and `rdi` is the
      window throughout (its only write is `002A61AC`).
    - `002A5F40` at `002A5FE8 mov byte [rdi+0x180], cl` **swaps the saved byte `+0x181` back in** (`002A5FD4`..`002A5FE8`).
      It skips the swap when the mode it read at `002A5FAA` is 2 or 4 (`lea eax, [rbx-2]` / `test eax, 0xfffffffd` / `je`).
      It is called from `002A6190` (`002A6685`), and passes `lea rcx, [rdi+0xd0]` to `002B27E0` at `002A5F96`.
    - `002A6F80` at `002A6FB3 mov byte [rcx+0x180], 0` sets **mode 0**, after the same save to `+0x181`
      (`002A6FA3`..`002A6FB3`). That its `rcx` is the window rests on the shared `+0x180`/`+0x181` pattern and its
      `+0x3BB`/`+0x3B9` fields. Its only caller, `002A2DDE` in `002A2C00`, was not traced for `rcx`.
    - `002A3210` at `002A323B` is a dword read-modify-write of `+0x180` (bits 17 and 18). It keeps the low byte.
  - A stack copy in `002AC5F0`. `002ADB0E`..`002ADB90` copies the 0xD0-byte element at `r14` to `[rbp-0x70]`, and
    `r14` is the same element the `#` escape sets to mode 5 at `002AD225`. Then `002ADBAF`..`002ADBC2` stores
    `([rbp+0x40] & 0xFFF7FF04) | 4` into the copy's `+0xB0`. The low byte is always 4, so this **sets mode 4** (and
    clears bit 19) on the copy, just before `002ADBC9 call 002AE610`.
  - Stack elements built by `002AC1E0` / `002B3C30` in `002A5460`, `002B3050`, `002B5390` and `002A1B00`: none of them
    writes its element's mode byte. The one covering write, `002A54AE or dword [rsp+0xe0], 0x2000000`, keeps the low
    byte.
  - Copies that carry the mode without choosing it: `002ABB20`'s 0xD0-byte copy to the stack (`002ABB60`..`002ABBDB`)
    and `002AC5F0`'s copy above.

**Controls.**
- The census is sensitive to a missed width or base: the package's byte stores must appear, and `002ABF79` must appear
  as a read. Both pass.
- The embedded sweep is sensitive to an element at an offset: the read `002A3790` (`[rdi+0x180]`) must appear, and it
  does. The offsets sweep must return `002A6190` with K = 0xD0 and the write `002A6606`, and it does.
- **Blind spots, stated.** Elements reached through a register shifted by arithmetic (as in `002ABB20`, `lea rdx,
  [rdx+0x80]`), copies through `memcpy`, and elements passed to callers of `002A8C50` / `002A9980` (no E8/E9 caller,
  so reached by pointer) are not swept. The census cannot rule out another writer of those kinds.

**Citations checked.** Every writer row's store was opened. For the mode 2, 3 and 4 parser stores (`002A989E`,
`002A9428`, `002A9193`), the README's bit and argument details were checked at the store: bit 19 at `002A98A5` and
`002A919A`. The UQ-178 / UQ-173 contradiction is confirmed, since `002ABF9F` is the mode-3 slot.

**Runtime routing.** None. Everything above is settled statically, except which control codes reach each parser store.
The README states that as a static limit, not a runtime one.

**Correction wording (the producer applies).**
1. The mode 0, 1, 4 row, "what it does": *"`+0x9B += +0x9C`. When the speed `+0x9C` is 30, it scrolls through
   `002ABB20`, which advances the head `+0x8C` to the next line or `#` page wait, and snaps `+0x90` to the head with no
   lag. It does this when `+0xA0` > 1, or when `00248F20` answers 1 (the mode query `00229EA0` is not 2). Otherwise,
   each time `+0x9B` reaches 30, the head `+0x8C` advances by `+0xA0`, the lag `+0x9D` moves by `+0xA0` toward `+0x9E`,
   and `+0x90` steps by `+0xA0` while it is at most `+0x8C - +0x9D`. `0x7D00` is an upper clamp on `+0x8C`."*
2. The mode 3 and mode 5 rows: add *"`+0x90` steps only while it is below the head `+0x8C`, which this arm never
   advances"*. Mode 3 also gets *"exits at once if `+0x88` is already 0"*. On screen for both: *"catches the reveal up
   to the head at a step per tick (3) or at the rate (5)"*.
3. "Who sets each mode":
   - Mode 0 adds *the pager `002A9980` (`002A9A27`, `dil` = 0 after `002A9A00 xor edi, edi`)*, *the setter `002B3950`
     (`002B3963`, `al` = 0 after `002B395A xor eax, eax`)* and *`002A6F80` (`002A6FB3`, through window `+0x180`)*.
   - Mode 1 adds *the message-window procedure `002A6190` (`002A6606`, through window `+0x180`, the old mode saved at
     `+0x181`)*.
   - Mode 4 adds *`002AC5F0` on its stack copy of the element (`002ADBC2`, `(dword & 0xFFF7FF04) | 4`)*.
   - Delete the "variable" row. Add a row *"restore: `002A5F40` (`002A5FE8`) swaps the byte saved at `+0x181` back in,
     unless the mode is 2 or 4"*.
4. Limits: replace the bullet "`002B3950` and the pager's variable store set the mode from a value their callers
   supply..." with *"The writers are complete for stores addressed as `[element + 0xB0]` (any width or base, image-wide)
   and through the window's `+0xD0` element and the stack elements of `002A5460`, `002B3050`, `002B5390`, `002A1B00` and
   `002AC5F0` (SWE2-AUDIT-SPEC review). Elements reached through shifted pointers, `memcpy` copies, and the elements
   handed to `002A8C50` / `002A9980` by pointer are not swept."*
