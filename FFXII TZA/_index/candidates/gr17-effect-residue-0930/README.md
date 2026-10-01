# GR-17 residue: stopping a released unit's effect cannot land a hit, because no shipped effect that can sit in `+0x774` has a hit or self-KO event (SWE2-ORACLE for OPUS, 2026-09-30)

This closes the one chain that [`gr17-reward-table-lifetime-0930`](../gr17-reward-table-lifetime-0930/README.md)
left open (its point 5 and step S10). There, releasing a unit calls `00300140(unit, 1)`, which stops the unit's effect
handle at `+0x774` with sequence 1. The sequence starter `0046EFD0` can launch a timeline track synchronously through
`003B8670` → `002EB740` → `00319F50` (an event on a battle unit) and on to KO → `0030E360` → `00312280`, the reward
computer that reads the unit's cached reward rows. The method is static: the certified image, plus the one shipped
file the chain reads. The checker is `gr17_effect_residue_check.py` (output `gr17_effect_residue_check.out`,
**`FAILS 0`**). It uses the kit's `retool.py` and parses `c_all.efx` the way the engine's own chunk handlers do.

## The answer

**No. The chain cannot deliver a hit during the release, and GR-17 has no window left along direct control flow.**
The code narrows the question to one file, and the data in that file closes it.

- **(a) Which effects can be in `+0x774`.** Only one store puts a real handle there: `0032A045` in `00329F80`, called
  only by the action advance `00304850`. The other stores write −1: the reset `00236BE6`, and `00319441` in the stop
  itself. The suspend/restore pair copies the unit's own block back. `00329F80` picks the effect id from two static
  tables: `00D106B0` (9 × 2) and `00D10720` (9 × 5), indexed by the action byte `+0x21` (≤ 8). The ids are
  **104–111 and 142–147**. It creates the effect through `002EACD0` → `003B02A0` as kind 5. The source is the unit's
  own id, and the one target is the unit itself. The kind-5 context is `c_all.efx`, the battle-common effect file,
  which is resource (10, 0).
- **(b) What "sequence 1" is.** Each effect has a header, built from a `0x600` chunk. Its byte `+0xA + n` names the
  slot of stop sequence `n`. The slots are built from `0x610` chunks, and their tracks from `0x620` chunks.
  `0024FE70` runs header byte `+0xB` for sequence 1. If the effect has not started yet (state 2), it first runs the
  start slots, header bytes `+1`, `+2`…`+7` and `+9`. `0046EFD0` hands `003B8670` only kind-2 timeline tracks, and at
  time 0 only their leading time-0 entries fire.
  - **The only opcodes that can reach `00312280` are 3 (the hit), 34 (KO the acting unit), 17 (stop another effect)
    and 40**, plus the indirect calls in opcodes 24 and 31.
  - **For all 14 ids**, sequence 1 is slot 2: one kind-2 track that fires opcodes **6, 41, 25**. The start slot fires
    opcode **5**. None of the four reaches `00312280`.
  - **The whole of `c_all.efx`** has 40 kind-2 tracks, and their opcodes are only {5, 6, 9, 25, 26, 39, 41}. So no
    effect in that file, whatever its id, can deliver a hit or a KO on any path.
- **(c) Could the hit kill, if the data had one?** **Yes. No code gate excludes the unit being released.**
  - The id resolver `003588B0` needs the manager's loaded bit. The unload clears that bit only after the release
    loop.
  - `003105D0` / `00310780` need `+0x698` to be set. It is zeroed only by the memset that follows the stop.
  - Opcode 34 would KO the acting unit, which is the unit being released. Its `+0x698` still matches, so
    `0031B860` would pick it, and `00312280` would read its `+0xE70` / `+0xE78` from the freed buffer.
  - So the closing gate is the data, not the code. Two early exits in `00319F50` were not settled, and neither is
    needed (see Limits).

**In player terms:** when you leave an area while an enemy is mid-action, the game stops that enemy's "gathering
power" glow as it discards the enemy. Every glow the game ships only fades out, and none of them can strike or defeat
anyone, so no EXP, LP or gil can come from the discarded reward tables.

| step | what it shows (addresses) |
|---|---|
| **E1** | Image-wide, the stores at displacement `0x774` are `00236BE6` (−1), `0032A045` (`eax` from `call 002EACD0` @`0032A040`), and two float stores in other objects (`0070B571` `movss`, `007D2959` float constant). The five `+0x6B0` block bases (`00304850`, `0030EDA0`, `0030EFF0`, `00310780`, and `003CA860` on another object) store nothing at `+0xC4`. `00319420` reads `+0xC4` and stores −1 (`00319429`, `00319441`). The block is bulk-written only by the suspend (`0030F0AC`–`0030F0F1`: copy `0x4F0` to `+0xB88`, then memset) and the restore from `+0xB88` (`0030EDA0`). |
| **E2** | `00329F80` (only caller `00304850` @`00304B62`) acts only when `+0x774 == −1` (`00329F86`). It picks `r9d` from `00D106B0` or `00D10720` (`0032A00C` / `0032A026`), with the selector `[r9+0x21] ≤ 8` (`00329FEC`). It calls `002EACD0([unit+8], 1, &unit+8, id)` (`0032A034`–`0032A040`), which passes kind 5 to `003B02A0` (`002EACE5`). There the handle is `5 << 28` or'd with a counter (`003B03C6`), the context is `0024F610({5, 0})` (`003B03F3`–`003B03FE`), `obj+8` is the source (`003B04DA`), the targets are at `+0x10` (`003B053D`), and `+0x370` = 2 (`003B0599`). |
| **E3** | `00319420` skips handles 0 and −1 (`0031942F`–`00319435`). Otherwise it calls `002EAEA0(h, 1)`, which is `jmp 0024FE30`. `0024FE30` sends kind 5 to `003B1260` (`0024FE42`–`0024FE59`), and `003B1260` calls `0024FE70(obj, 1)` (`003B12D4`). `0024FE70` takes header byte `+0xA + seq` and its slot dword `+0x2C` (`0024FF23`–`0024FF2F`), then calls `00333280` → `0046EFD0` (`0024FF42`, `00333303`). In state 2 it first calls `003A74F0` (`0024FEC7`), which calls `003337B0` (`003A7590`). That runs header byte `+1`, bytes `+2`…`+7` and byte `+9` through `003331A0` → `0046EFD0` (`0033386B`, `00333897`–`003338E1`, `00333957`, `0033323A`). |
| **E4** | `0024B3A0` has 6 callers, each with its own template byte. Kind 5 is set only at `003B0730`, in `003B0660`, which loads resource (10, 0) (`003B06E2`–`003B070D`) and parses it (`003B0745`). The kind-10 path array is `0215F050` ← `01E127B8` (`002DF9FD`), and entry 0 is `PS2Data\effect_finish\jp\common\c_all.efx`, the only `c_all` string in the image. `0024B3A0` publishes the header table as `ctx+0x38` in `02EBEFA8` (`0024B48E`). The `0x600` handler `003A79C0` stores `table[p[1]] = p+4` (`003A7A10`). The `0x610` handler `003A7B50` stores slot `q[1]` of header `q[0]` (`003A7B91`) and clears its track table (`003A7BA8`). The `0x620` handler `003A77F0` stores track `s[2]` after moving it down by 12 bytes (`003A7845`–`003A785D`). The loader calls them at `003EDE3C` / `003EDE64` / `003EDEA7`. |
| **E5** | `0046EFD0` passes to `003B8670` (`0046F0AF`) only tracks with index ≥ 1, `+5` bit 0 and `+1 == 2` (`0046F068`–`0046F098`). It passes kind 3 to `004FF2C0` (`0046F14B`), which sends it to `005372D0` (`004FF2DD`). None of its other callees (`003A8AE0`, `003A8020`, `003A8240`, `0046EF10`, `00314960`, `001EDDA0`, `0020E600`), nor `005372D0`, reaches `00312280`. |
| **E6** | The opcode table (`003B994C` / `003B9854`) gives the direct routes: opcodes 3, 13, 26, 34, 37 and 128 → `002EB740`, 17 → `002FD0C0`, and 40 → `003B3C00`. Opcodes 24 and 31 make indirect calls. In `00319F50`, only event kinds 0 (`003191B0`) and 2 (`00300520`) reach `0030E360`. The kinds per opcode are set at `003B8822`, `003B895F`, `003B89C3`–`003B89ED`, `003B91B5`, `003B923B` and `003B933D`: 3 → 0, 13 → 1, 26 → 3/6/7/8, 34 → 2, 37 → 4, 128 → 5. The reaching set is therefore {3, 34, 17, 40} plus {24, 31}. |
| **E7** | `c_all.efx`: sha256 `0f2f15d9…9029`, 1,017,904 B, walked to its end. It has 191 headers, 218 sequences, 1,272 tracks and 40 kind-2 tracks, with opcodes {5: 19, 6: 17, 9: 1, 25: 14, 26: 4, 39: 1, 41: 14}. No reaching opcode appears. For each of the 14 ids, header byte `+0xB` = 2, slot 2's track 1 fires (6, 41, 25) at time 0, and start slot 1's kind-2 track fires (5). |
| **E8** | `003588B0` resolves through `00263FF0` and needs `[mgr+0x10]` bit 0 (`003588FF`). That bit is cleared at `00262DA8`, after the release loop `00262D34`. `003105DE` / `0031078E` need `+0x698 ≠ 0`, which is zeroed by `002342CE`, after `0023423F`. Kind 2 is `HP −= HP` on the acting unit's own `+0x698` (`0031A089`–`0031A09B`, `00300520`), and the acting unit is context `+8` (`003B897E`). |
| **C1** | Control for the parser: across the 3,288 shipped `.efx` files, it finds opcode 3 ×347 and opcode 34 ×6, and every opcode lies in 1…63 or is 128, as the interpreter expects. Every `c_all` header slot reference has its `0x610` chunk, and every kind-2 track's entries fit and are sorted by time. |
| **C2** | Control for the graph: `003B1260`, `0046EFD0`, `00319F50` and `00300140` all reach `00312280` in the direct graph, so the question was live before the data closed it. |

## Contradicted or corrected statements

- **The field map's `+0x774` rows** (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`: "2 / 1" writers, and
  `releasedEffectHandle` with only −1 stores) miss the one store of a real handle, `0032A045` in `00329F80`. The same
  page's `00304850` subtree table calls `00329F80` "a one-call wrapper into `002EACD0`". It also stores the result at
  `+0x774`, and it is where the unit's action-charge effect is created.
- **The timeline-interpreter section** (`00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`
  §12) says "128 and a dozen others are inline without a call", and its event-kind list stops at 37 → 4. Opcode 128 does
  call `002EB740`. It builds a target from `+0x90` / `+0x10` and joins the call at `003B8A13`, past opcode 26's
  `xor edx, edx`, as event kind 5 with that target. It is authored alongside the hit: 347 times each across the
  corpus.
- **My own GR-17 record, point 5 and S10**, route sequence 1 through "`0024FE30` / `002FD0C0`". The `+0x774` handle
  is kind 5, so the route is `0024FE30` → `003B1260` → `0024FE70`. `002FD0C0` serves kind 1. That record also says
  "a track with kind 2 … is a hit". Only opcodes 3 and 34, and 17 / 40 through further effects, can reach the
  reward computer. That record's wording should take these corrections when it is published.

## Limits

- **Direct edges only.** This follows the same rule as the parent record. The opcode arms that reach are found by
  direct-call closure. The indirect calls in opcodes 24 (`[02091140]`) and 31 (an import slot) are counted as
  reaching without being resolved. Neither opcode occurs in `c_all.efx`, so this does not change the verdict.
- **The data is one extracted file.** `Tools/work/DATA/mesh54/fx_all/…/jp/common/c_all.efx` is in the ignored work
  tree. The checker pins its sha256 and size, and the size matches the kind-10 maximum in the size tables
  (1,017,904). The image names only this one `c_all.efx` path. A modded or different-language build that replaces it
  would need the census re-run. The checker does that as-is.
- **Load-time base.** The parser assumes the relative-reference base `01F83530` is zero, so a compressed null is 0.
  The encoded-id contract gives this as the load-time value. The census does not depend on it, because it keys
  tracks by their chunk indices, not by pointers.
- **Not settled, and not needed.** `00319F50` returns early when the source unit's flag bit 1 is set (`00319FA3`),
  or when the battle state `[022C2160]` is 5 or 6 (`00306BB0`). Whether either holds during an area unload was not
  determined. The verdict does not rest on them.
