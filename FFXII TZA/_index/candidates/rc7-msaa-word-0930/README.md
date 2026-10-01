# RC-7: the MSAA word at 01DF0900 is a multisample count, 0 or 1 meaning off (ORACLE, 2026-09-30)

Input for `RC-7` ([what the console tunes](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)
section 7). SWE2-CONTRACT registered the row. Static evidence only (shipping image `73461d08…`). **Verdict: ANSWERED.**

## The question

What does the MSAA setting word at `01DF0900` hold? The render path copies it into the render-settings block `+0xB4`
(`02CB8084`) when it re-applies MSAA (`00186410` at `001865C6`, `00187950` at `00187B92`), and
`PhyreScene::disableMsaaInternal()` (`00186130`) replaces that copy with 0. Is the word a sample count, a quality index or
an enable?

## Method

`rc7_msaa.py` (output `rc7_msaa.out`, census `rc7_refs.tsv`, FAILS 0).

- **Census.** Every function body is swept (`memsweep.py`: the `.pdata` chain roots, plus the leaf bodies that have no
  unwind data, taken from `functions.tsv`). It records:
  - rip-relative operands of any width that overlap `01DF0900`..`01DF0903`;
  - the image-base-relative form (displacement `0x01CD0900` on any base register);
  - 8-byte pointers and 4-byte RVAs to the word anywhere in the file.

  Positive control: the census must find the reads `0018644D` (which feeds the compare `00186453` that the page cites)
  and `001865BD`.
- **Value sources and render side.** Each step below is checked against the decoded instruction. A mismatch fails the
  run.

## Result

**The census.** There are 15 references, all full dword accesses, in four functions: `00186130`, `00186410`,
`00186CD0` and `00187950`. No partial-width access exists, and no pointer or RVA to the word exists anywhere in the file.
Three instructions write the word:

| writer | value stored |
|---|---|
| `00186D68` in `00186CD0` | the framework setting `[framework + 0xD3C]`, with 1 folded to 0 |
| `00186D81` in `00186CD0` | 0, when the framework setting is 0 |
| `00187A7A` in `00187950` | `[scene + 0xDC8]`, when the scene's dirty byte `+1` is set |

The `.data` initial value is **4**.

**Where the values come from.** Both routes start from the same lookup: `001DE570` reads the `GameSetting` config
object's MSAA mode (`[01F82D20] + 0x20`), reduces it mod 5, and returns entry *n* of the table at `00900EE8`, which is
**{1, 2, 4, 8, 9}**.

- **Boot route.** `007980A0`, called from `007A3770` (`007A377E`, `007A378D`), stores that lookup into the framework
  object: `rdi = [02EA5368] + 0xD20` (`0079854C`), then `mov [rdi + 0x1C], eax` (`0079856F`). That is framework
  `+0xD3C`.
  - This is the framework field's value store. A search of the functions that load `[02EA5368]` or call its getter
    (`00796E20`/`00796E30`) for displacement stores to `+0xD20`..`+0xD54` finds only the constructor (`00792350`),
    which zeroes `+0xD38`..`+0xD3F` (`00792482`). The boot store escapes that search because it rebases first.
  - The scene constructor `00184F20` then calls `00186CD0` (`00185056`), which reads `+0xD3C` (`00186D3C`) and handles
    three cases:
    - **0:** the word is 0 and the MSAA flag `scene + 0xDBA` is cleared.
    - **1:** the word is 0, but `+0xDBA` is set.
    - **any other value n:** the word is n and `+0xDBA` is set.
- **Console route.** `00189520` stores `edx` at `scene + 0xDC8` and raises the dirty byte `+1`.
  - Its only callers are the two console arms at `001D4A80` (in the dispatcher `001D1660`) and `001D51D2` (in
    `001D5120`). Each passes the result of `001DE570` (`001D4A6F`, `001D51C1`).
  - The scene constructor zeroes `+0xDC8` (`00185046`, `esi` = 0 from `00184F54`).
  - The other `+0xDC8` writes in the image are on other objects: word stores, or the console object's own constructor
    `001CCB20`.
  - `00187950` copies `+0xDC8` into the word unchanged (`00187A73`/`00187A7A`), so on this route a count of 1 can reach
    the word.

So the word only ever holds **4** (the image default), **0, 1, 2, 4, 8 or 9**. The values 7 and 16 are never produced:
the mode is taken mod 5, so the 16× capability bit that the console-arm catalogue records can never be selected.

**What the render side does with it.** The value is used as a sample count.
- `00186410` and `00187950` each build three render commands whose `+8` is the word (for example `001864C3`/`001864C9`).
  The commands target the scene's `+0xB58`, `+0xB08[+0xC30]` and `+0xB18` objects.
- The commands' callback `00189110` copies the low byte into byte `+9` of the target object (`0018911B`).
- The texture creator `0061FDA0` reads byte `+9` of the object at `[texture + 0x20]` (`0061FEB0`/`0061FEC1`). It writes
  it into the `D3D11_TEXTURE2D_DESC` at `rsp+0x48`: `SampleDesc.Count` is `rsp+0x5C` and `Quality` is `rsp+0x60`
  (`0061FECC`). It then calls device vtable `+0x28`, which is `ID3D11Device::CreateTexture2D` (`006200E5`).
  - **7 → Count 4, Quality 16** (`0061FED5`/`0061FEDD`).
  - **9 → Count 8, Quality 16** (`0061FEEC`/`0061FEF4`).
  - **1 or less → single sampling** (`0061FEFE`/`0061FF01` skip the multisample setup).
  - **Any other value is the Count itself.**

**Answer.** The word at `01DF0900` is the **multisample mode as a D3D11 sample count**:
- 0 or 1 is off;
- 2, 4 and 8 are MSAA 2×, 4× and 8×;
- **9 is the one coded mode**: 8 samples at quality level 16. It is the fifth console mode, the one the capability
  probe enables when 8× reports more than 16 quality levels.

It is neither a quality index nor an enable. The enable is the separate byte `scene + 0xDBA`. The block's `+0xB4`
holds the last value applied, and 0 after `disableMsaaInternal()`, which acts only when the word is nonzero
(`0018614C`).

**How this relates to FABLE's record** ([`rc789-fable-0930/`](../rc789-fable-0930/README.md), RC-7):
- The two records agree on the render side and on the 7/9 remaps.
- This record closes FABLE's first limit: the framework `+0xD3C` writer is the boot store `0079856F`. FABLE's census
  looked for `[reg + 0xD3C]` displacements and missed it because the store uses `+0xD20` as its base with offset `+0x1C`.
- It also closes the second limit: the `+0xDC8` source is `00189520`, fed only by the console arms.

## Not claimed

- **The label list.** The image holds an anti-aliasing label list at `01DF0270`: `Off`, `MSAA2X`, `MSAA4X`, `MSAA8X`,
  `CSAA16x`, `CSAA16XQ`, `MSAA16x`. No code or data reference to it was found, so this record does not tie those names
  to the values. The Count/Quality pairs of 7 and 9 match the usual CSAA 16x / 16xQ encodings, but that is a
  resemblance, not evidence.
- **The type link.** That the object `0061FDA0` reads at `[texture + 0x20]` is the same object the render commands
  write through `00189110` is inferred from the shared `+9` byte and the call chain, not proven by a type.
- **Run order.** No execution. Which value a given machine ends up with depends on `GameSetting.ini` and on the
  capability mask. That the boot store runs before the scene is built was not traced.
