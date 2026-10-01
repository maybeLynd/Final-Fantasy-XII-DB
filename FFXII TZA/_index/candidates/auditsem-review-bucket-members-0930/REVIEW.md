# SWE2-AUDIT-SEM review — the `.bin` / `.dat` bucket member-format declaration (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929` (T1, with T2 aspects) |
| reviewed | `bafa49c9f` (author **SWE2-DATA** — subject prefix; not an OPUS / ORACLE / CONTRACT / STRUCT production, so this lane may review it) |
| record under review | [`bucket-members-0929/README.md`](../bucket-members-0929/README.md), [`_index/bucket-members.tsv`](../../bucket-members.tsv), [`bucket-member-units.tsv`](../bucket-members-0929/bucket-member-units.tsv), `checks/`, the three new sheets and the new sections |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` (checked); archive `D:\SteamLibrary\…\FFXII_TZA.vbf` read through `agent_flow/tools/vbfextract.py` |
| tree at review | HEAD `0aa544606` |
| **verdict** | **ACCEPT-WITH-NARROWING** (wording, three items; the enumeration, every member binding, the SIG=N splits and the correction stand) |

Evidence classes are kept apart below: **archive** (bytes read from the installed VBF), **static** (the shipping image),
**producer re-run** (the package's own instruments re-executed). Nothing here is live.

## 1. The enumeration, re-derived from the archive before reading the producer's numbers (SWE2-AUDIT-SEM)

`receipts/vbf_census.py` loads the VBF index and decompresses only the first block of every `.bin`/`.dat` entry
(archive class; it does not read the extracted tree or the producer's census TSVs):

- **89,414** archive entries; **1,439 `.bin` + 2,948 `.dat` = 4,387** — the producer's totals.
- **59 `.bin` + 21 `.dat` distinct leading signatures** — the full census's 59 + 21 rows. `req_controls.py` then
  compares the tracked full census (`bucket-members-input-0929/format-magic-census-full.tsv`) row by row with my
  counts: **0 differences over 80 rows**.
- `xcheck_units.py` binds `bucket-member-units.tsv` to my own census with **my own** locale folding: every one of the
  4,387 entries lands on a units row carrying **its own** leading signature (0 misses). The only disagreement is
  granularity: I folded `in_sdver` as a locale, the producer keeps `myoshiok/in_sdver/packfiles/*` as four separate
  units — the four `packdirectory` rows then differ by one entry each and the member totals do not move. Not a defect;
  noted so nobody re-derives it as one.
- `vbf_vs_extract.out.txt`: the extracted tree `D:/FFXII_TZA_extract` equals the VBF for all 4,387 entries (size and
  leading dword) and for 80 whole files by SHA-256, so the producer's corpus checks that read the extract read the
  shipped bytes.

## 2. The measurement (MP-3) and its controls (SWE2-AUDIT-SEM)

- `requirements.bucket_members_check(['bin','dat'])` → **`[]`** (`reqcheck.out.txt`); 53 `.bin` + 5 `.dat` members.
- **Four mutants of `bucket-members.tsv` (scratch copies), each refused** (`req_controls.out.txt`): dropping the
  `summoneffectdata` row (census signature `'dP<d'` in no member); `'FLAG'=8` for `flagrom` (split sums to 17 of 18);
  a phantom signature `'dP<e'`; `MUS0` entries 3 against a take of 2. The check is not a green that accepts anything.
- `gen_bucket_members.py --check` at HEAD: C1–C7 PASS, FAILS 0 (`gen_check.out.txt`).
- All eleven member checks re-run at HEAD, FAILS 0 (`producer-rerun/`); `callpairs.py` re-run with the producer's
  arguments reproduces `callpairs_run1.txt` **byte for byte** (36 s over 122,250 call sites; its three controls pass).

## 3. The four shared signatures are unrelated layouts (archive) (SWE2-AUDIT-SEM)

Read from the entries themselves (`pull.py`):

| signature | members | what the bytes show |
|---|---|---|
| `'FLAG'` | `flagdef` / `flagrom` | 8-byte magics differ: `FLAGDEF1` (u32 count 0x35, then a u16 list) vs `FLAGROM1` (count 152, u16 offset table, 856 B) |
| `00 00 00 00` | `binmenuimage` / `behindcamera` | headerless pixel rows vs `behindcamera`'s 1,040-byte table (`00000000 10000000 …` then floats `1.3`, `-0.7`) |
| `80 00 00 00` | `packdirectory` / `musicinfo` / `st2enames` | `mrppack_ys` = 32-slot self-relative directory (`0x80` = its own header size, sentinel-filled); `musicinfo` = a 512-byte table whose leading `80 00 00 00` is record data (it recurs at `+0x18`), not a header size; `growth_rate_growth_rate_name` = u32 count 128 + offsets |
| `01 00 00 00` | `skeletonmapping` / `testmapref` | count 1 + the name `hc1006_03` vs 274 × 8-byte map_ref-shaped rows |

The split is right: none of these pairs is one layout.

## 4. Spot-checked member formats (archive + static) (SWE2-AUDIT-SEM)

- **`summoneffectdata` correction (b7) — confirmed independently.** My own rip sweep (`ripref.py`, no function
  list) of `02AD9B00`–`02AD9E40` finds the loader `003B541D lea r8,[02AD9B60]` with `mov edx,0x2A` /
  `lea ecx,[rdx-0x21]` (kind 9, id `0x2A`; kind-9 array entry `0x2A` = `common\summoneffectdata.bin`,
  `kind9_paths.out.txt`) and the readers `0036FA0A` / `0036FC13` indexing `lea rdx,[rax+rax*4]` →
  `[rcx+rdx*2+k]` (10-byte stride). The tail reads land on `02AD9DE0`–`02AD9DF4`; `02AD9E00` onward are separate
  byte/word globals written elsewhere (`0036FD60`…), so the blob is exactly `0x2A0` = 672 B = 64 × 10 + 32, matching
  the file. `'dP<d'` = `64 50 3C` = 1.00 / 0.80 / 0.60 at the 0.01 scale — record 0's data, not a magic. The struck
  readings are wrong and the correction is supported.
- **`amap` (new sheet).** Kind-7 id `0xA5` → `menumap_area.bin`; 396 B; `amap`, `0xC9`, offsets `0x10/0x38/0x74/0xEC`;
  counts 39/59/59/39; closure 396; `S[i] = 60099 + i`, `S[0] = −1`. My rip sweep of `020927D0` finds the three
  loader-side accesses (`002538F4`, `00253907`, `00253931`) and **exactly four** readers `00254381` / `002543A1` /
  `002543D1` / `002543F5` — the sheet's four accessors.
- **`menuquest` (new sheet), all 27 entries** (`mq.out.txt`): `{u16 off[6], 0xFFFF, u16 N}`, records end exactly at
  `off[0]` (`16 + 20N`), `QHD0` at `off[3]`, `QHT0` at `off[4]`, and `off[5] + 28N` equals the file size in every
  locale. The four leading patterns are `off[0..1]`, as claimed. (Kind-7 ids `0x12A`–`0x12D` name `menuquest00`–`03`;
  `03` does not ship, which the shipped-entry enumeration correctly ignores.)
- **`binmenuimage`** (`pull.py` over the `us` copies): all eighteen are raw 8-bit rows sized `128 × rows`; the
  byte-pair equality is **1.000 in every `face_guest`**, 0.75–0.79 in `map_efe00`–`06` and 0.63 in `mini_guest_face`.
  One layout family, as §2 of the sheet says — but see narrowing N1.
- **`packdirectory`** (`us`): `clutpack`/`texpack`/`tex2pack`/`fontpack_fs`/`fontpack_it` have a 0x40 header (16
  slots), `mrppack` 0x80 (32 slots); offsets ascend and the tails are `0xFFFFFFFF` sentinels — one layout across both
  leading signatures.
- **`st2enames` / `logicpack`** (`endslot.out.txt`): see narrowing N2.

## 5. The T2 negatives — "no requester found" — re-derived without the producer's sweeps (SWE2-AUDIT-SEM)

Static class. The claims: `fhmusicdata` (kind 9 `0x1C`), `test_map_ref` (kind 9 `0x01`), `menu_version` (kind 7
`0x90`), standalone `shop_data` / `wepjob_matrix` (kind 2 `0x27` / `0x00`).

- **Own request-site census** (`reqsites.py`): every rel32 call/jmp in `.text` to `0032E620` / `0032E400` — 122 sites;
  constant kind-9 ids `{3–0xB, 0x27–0x2A}`. **Positive controls**: `0x2A` (summoneffectdata, the `lea ecx,[rdx-0x21]`
  idiom) and `0x0A` (flagrom) are found.
- **Counter-example search, loops**: the one kind-9 site with a register id, `002EA5A9`, is a loop
  (`lea edx,[rbx+0xB]`, `ebx` 0..9) — ids `0x0B`–`0x14` (the charseinfo run). It cannot reach `0x1C` or `0x01`.
- **Counter-example search, wrappers** (`wrappers.py`): the 88 sites whose kind or id is register-held are lifted to
  their 40 `.pdata` functions and their callers (two levels). **Positive control**: the census finds wrapper
  `0051ED10`'s callers passing kind 9 ids `0x1F`/`0x20`/`0x21`. No caller passes `(9, 0x1C)` or `(9, 0x01)`.
- **Any-argument probe** (`probe_any.py`, all 130,395 direct calls, any two of rcx/rdx/r8/r9): `(7,0x90)` 0,
  `(9,0x1C)` 0, `(2,0x27)` 0. `(9,1)` has four hits: the producer's two (`00252B40`, `003E12A0`, neither a request
  API) and two looser ones (`002CE7D0→002A1F20`, `0057FA12→00393160`) whose callees reach no request API
  (`kind2_callers.out.txt`). `(2,0)` is too common to probe this way; instead the kind-2 loader `00384420` has exactly
  three callers — the battle_pack path `003843F0` (ecx `0x13`, twice), the board loader (`add ecx,0x47`) and the
  message dispatcher `002385D0` (id table `01E09F68`, which holds neither 0 nor 39) — the producer's b6 reading.

**Result:** the negatives hold at the scope the README states — a whole-image static result; a kind/id computed at
run time at one of the register-held sites (my count 88, the producer's 89; different site accounting, same class) is
outside it. The README already discloses that residual; nothing to narrow.

## 6. Narrowings (exact wording; the producer applies them) (SWE2-AUDIT-SEM)

- **N1 — `binmenuimage` claim row** (the bin_menu sheet's `archive_formats:` row). It says *"the eighteen headerless
  byte-doubled bin_menu images … its six leading patterns are pixel bytes"*. Two words overreach: only the ten
  `face_guest` files are byte-doubled (the sheet's own §3 measures `map_efe` and `mini_guest_face` as undoubled), and
  the member carries **seven** leading patterns (the README and `bucket-members.tsv` say seven). Narrowed row text:
  *"the eighteen headerless raw 8-bit bin_menu images face_guest07-16 (2x2-upscaled, byte-doubled), map_efe00-06 and
  mini_guest_face (undoubled) (.bin member; its seven leading patterns are pixel bytes, not magics)"*.
- **N2 — `st2enames` claim row** (unnamed-bin-families). It says `{u32 count, u32 offsets[count], UTF-16LE strings}`.
  The frame has **count + 1** offsets: `offsets[0] = 8 + 4·count` and `offsets[count]` equals the file size in all four
  copies (`endslot.out.txt`). Narrowed: *`{u32 count, u32 offsets[count+1] (the last = file size), UTF-16LE strings}`*.
  The `logicpack` row's `{u32 count, u32 offsets}` has the same end slot (`offsets[1310]` = 1,035,896 = the file size)
  and should say so; it is not wrong as written, only silent. The control it cites (`uq70_name_tables.py`) does not
  test the end slot — a one-line check (`offsets[count] == len(file)`) would make the row falsifiable.
- **N3 — README "What is not claimed", first bullet.** It says the committed MP-3 check reports 22 problems on this
  file. That was true before OPUS's SIG=N gate (`6446068ef`); at HEAD `bucket_members_check` returns `[]`, as the
  commit message itself states. Replace the bullet's present tense with the current state and keep the old sentence
  as dated history.

## 7. Not reviewed here (SWE2-AUDIT-SEM)

Record semantics inside `st2e`, `battle_pack` and the pack directories (the R family, as the README says); the gmap
sheet's "only guide00 is ever requested" beyond the producer's re-run check (198 checks, FAILS 0); the fontdat and
handbook `.dat` layouts beyond the per-entry signature binding.

## Receipts (SWE2-AUDIT-SEM)

`receipts/` — scripts `vbf_census.py`, `xcheck_units.py`, `req_controls.py`, `pull.py`, `img.py`, `ripref.py`,
`reqsites.py`, `wrappers.py`, `probe_any.py`, `st2n.py`, `mq.py`, `endslot.py` (run from
`Database/Tools/work/SWE2-AUDIT-SEM/bucket0930/`, where `vbf_bin_dat.tsv` and `ent/` are regenerated) and their
`.out.txt` outputs; `producer-rerun/` holds the eleven member checks and `callpairs_run1.txt` re-run at `0aa544606`.
