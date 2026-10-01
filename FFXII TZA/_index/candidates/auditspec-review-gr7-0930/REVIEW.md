# SWE2-AUDIT-SPEC review of GR-7 (gr7-kind10-reader-0930 at f0c46d818): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `f0c46d818` (the record's only commit), [README](../gr7-kind10-reader-0930/README.md) and `gr7_kind10_check.py`.
Measured at HEAD 48de14c6b (a parked draft started at 9b6c5bc93; its outputs reproduce identically). Static,
certified image (sha256 asserted by [img.py](img.py)) and shipped data.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-GR7-0930 | gr7-kind10-reader-0930 | `f0c46d818` | ACCEPT-WITH-NARROWING |

These claims stand:
- kind 10 = BattleUnit dword `+0xB90`, index 0;
- the only reader is `00301AD0` through opcode `0x36` / `0x37` mode 3;
- no player gambit reaches it.

The narrowing adds the five `+0xB90` functions the Limits leave out (all now typed as not battle units), a writer the
writer table misses (the full-slot clear), and the reason the player-gambit check is valid.

**Re-run.** [rerun_gr7_kind10_check.out](rerun_gr7_kind10_check.out) is identical to the committed `.out` (CR
ignored): K1-K6 PASS, `FAILS 0`. It reproduced again at 48de14c6b. `git status --porcelain --ignored` on the package
directory shows nothing.

**Re-derived independently** ([gr7_indep.py](gr7_indep.py) / [.out](gr7_indep.out); pefile + capstone, no retool / regval).
- **Selector entry bytes.** In `00301AD0` the entry is at `rdx + 6*idx`:
  - `00301B0F` reads the u16 operand at `+6`;
  - `00301B1A` reads the u8 at `+8` into ebp, stored at `[rsp+0x128]` and compared with 3 at `00301C45` (the mode);
  - `00301B14` reads the u8 at `+9` into r12d, stored at `[rsp+0x30]`: this is the byte the opcode dispatch
    `00301C04`..`00301C25` compares with `0x33` / `0x35` / `0x37`;
  - `00301B1F` reads the s16 param at `+0xA`;
  - `r12 = ~opcode & 1` at `00301B44` / `00301B4C` gives the polarity.

  So the package's `{u16 operand, u8 mode, u8 opcode, s16 param}` is right. (The gambit page §Z-2 note calls `+8` the
  opcode, which is the other way round. That is a neighbour's wording, not this record's.)
- **Mode != 3 path.** Opcode `0x36` / `0x37` with mode != 3 calls `00321190(operand >> 12, self r15, operand & 0xFF)`
  at `00301C52`, so the kind is dynamic.
- **Jump tables.**
  - The reader `00321190` and the writer `00329E60` tables have 10 slots each, and only slot 10 goes to `0032126F` /
    `00329F1C`.
  - The candidate-loop table in `00301AD0` covers 70 opcodes and 31 distinct arms. Opcodes `0x36` / `0x37` go to
    `00303079` only.
  - `00303079` calls `00321190(ecx = 10, rdx = r15, r8 = 0)` at `00303088`, then `bt eax, esi` and `setb` feed the
    polarity compare at `003021D9`.
- **Callers.** Raw E8/E9 + jcc + stored qwords: `00321190` has 6 call sites and `00329E60` has 2, with 0 jcc and 0
  stored pointers. These are the same sets as K3. `002FADDF` / `002FAE00` pass the constant 3.
- **Raw `+0xB90` census, all forms.** I scanned for disp32 `0xB81`..`0xB93` covering any byte of `+0xB90..+0xB93`,
  with any base, index or width, plus `lea` and imm32 `0xB90`, each confirmed by decode. There are **18 hits in 15
  functions**.
  - Only three are battle-unit sites: `00236BE0`, `0032127C` and `00329F29`.
  - Every other hit is typed as not a BattleUnit (a 0xF50 heap-pool slot, so rip / image-base forms cannot reach it):
    - `00172750` / `001728C0`: the object also has `+0x1958` / `+0x2230`.
    - `00177B71`: the object has `+0x2E3C`.
    - `00186800` / `00186CD0`: the boot singleton's `+0xB90` array.
    - `0070A83C` / `0070A894`: float / matrix initialisation.
    - `00791E70`: a memset of 0x24E0 bytes at `+0xFA8`.
    - `007D44BC`: an rbp stack frame.
    - `004B8F20`: writes only. It fills constant packet words (`0x1000404`, `0x6C14010E` …) in 8-byte runs through
      `+0xBA4`, a descriptor builder.
    - **`0052D1E7`** (new): `rdx = [02CA84F8] + 0xB90` goes to `00430B90`, which reads that pointer only at `+0x30`
      (`00430BA5`, `00430D59`), so there is no `+0xB90..+0xB93` read.
    - **`0054FE00`** (new): `lea rcx, [rbp+0xB90]` goes to `00430AF0`, which does read `[rcx]`, but as a
      file-relative offset it rebases in place through `0020E600` / `0020E620`. `0054FE00` is reached only through
      `00538982`, an arm of the record-type dispatch `00538910` on byte `+0x44` (a loaded-resource relocator), so
      this is not a unit.
  - So among the 18 raw hits, `0032127C` is the only battle-unit read.
- **Where the evaluator's records come from** ([gr7_sets.py](gr7_sets.py) / [.out](gr7_sets.out)).
  - `00301AD0`'s only caller is `003016A8` in `003014C0` (rdx = the order record). `003014C0`'s only caller is
    `00305DD2` in the walker reached from `00305AB0`.
  - `00305AB0` calls the walker `00305CC0` four times. rdx there is BattleUnit `+0x6E8`, `+0x6F8`, `+0x6E0` or
    `+0x6F0`, or one of two built-in sets: `01EEC370` (1 record) and `01EEC320` (2 records). Neither built-in set
    has an entry with opcode `0x36` / `0x37`.
- **Player gambits reach the same evaluator**, through the rebuild `00328140`.
  - Read at `00328226`..`00328273`, for each entry e it stores operand ← row byte `+0x10+e`, the {mode, opcode} word
    ← row word `+8+2e`, and param ← row word `+0x18+2e`, into `record +6+6e`.
  - So the opcode of entry e is row byte `+9+2e`, exactly K6's `word(row+8+2e) >> 8`.
  - [gr7_gambit.py](gr7_gambit.py) / [.out](gr7_gambit.out) decodes all **9** language copies. Each has 256 rows of
    stride 32, with an identical section hash, **0** entries with opcode `0x36` / `0x37`, and 22 distinct opcodes.
  - As a decode control, the entry-0 relation byte gives 137 / 68 / 51 rows for 1 / 2 / 4, the gambit page's Z-15
    counts.

**Controls.**
- The census's positive controls are the package's three battle sites and the known outside hits, all re-found.
- A census blind to indexed forms would miss `0032127C` / `00329F29` (`[rdx + rax*4 + 0xB90]`). This one finds them.
- The K6 gambit check could be blind to the defect "wrong byte decoded as opcode". It is now tied to the rebuild's own
  stores, and its relation-byte control reproduces an independent published count.

**Citations checked.**
- K1 arms, K3 caller set, K4 `00303079` and K5's `bts` / `btr` order ids (the `002FE660` table: `0x4122` / `0x4156`
  bts, `0x4123` / `0x4157` btr, `0x4149` set, `0x4155` add, everything else fails) support their sentences.
- Not checked: the `gil_b` set 2 records 63/64 example, and the bit → action-name table (a data join). The re-run
  reproduces their counts but not the names.

**Correction wording** (the producer applies):
1. Limits, first bullet: replace the list with "The other `+0xB90` accesses in the image are in `00172750`,
   `001728C0`, `00177A70` (fragment `00177B71`), `00186800`, `00186CD0`, `004B8F20`, `0052D1E7`, `0054FE00`,
   `0070A7F0` (fragments `0070A83C` / `0070A894`), `00791E70` and `007D44BC`. The raw disp32 census covers every
   width and form, and none of these bases is a BattleUnit (the review record types each one). A reader through a
   biased base (a unit pointer plus a folded offset) or a bulk copy of a unit is outside any displacement census."
2. Writer table: add "and the full 0xF50 clear of the slot on allocate (`002344D2`, `memset(slot, 0, 0xF50)` in
   `00234480`), which has no displacement." (The BattleUnit type row also records a clear on release. I did not
   re-read that one.)
3. K6 / "No player gambit": add "The gambit rebuild `00328140` writes row word `+8+2e` into entry e's {mode, opcode}
   word, so K6 reads the evaluator's opcode byte. The 256 rows are identical in all nine language packs."
