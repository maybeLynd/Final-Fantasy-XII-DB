# S-34: the six flag-bank entries §17 does not cover, executed as shipped code over the shipped lists (OPUS, 2026-09-25, block 306)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- S-34's binding gap names "live capture, and six of the contract's seventeen entries".
- `CONTRACT-persistent-flag-banks.md` §17's differential covers the eleven bank accessors and names these six as
  outstanding.
- This is a narrow OPUS harness, not an ORACLE EXP. It does not touch the live half of the gap.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Failure rule.** Entering any function outside the six entries' own static reach fails a case: `002EF640`,
  `00265270` (FieldData_GetVariable0), `0032AB60` (SetPrimary) and the import thunk `00861EC0`.
- **One import bridge.** `002EF2D0`'s `memset` goes through thunk `00861EC0` → IAT `008C2A60`, which the PE import
  directory names `VCRUNTIME140!memset`. The slot points at a bridge that performs the fill. Only the reset case
  reaches it, and it recorded one call: `(0x02164480, 0, 0x1538)`.
- **Data.** The three shipped files, loaded verbatim (SHA-256 in `result.json`):

  | file | magic | count | published at |
  |---|---|---|---|
  | `mapjumpgroupflagrom.bin` | `FLAGROM1` | 152 | `[02ADD0C8]`, the MJGP_ROM schedule table |
  | `mapjumpgroupinit.bin` | `FLAGDEF1` | 53 | `[02ADD0D0]` |
  | `eventmemorylist.bin` | `EVMEMLST` | 8 | `[02ADD0A8]` |

- **Fixtures** are planted data only: the progress word read by `00265270` (`[02098E20]` bit 0, `[02098E58]`), and
  the payload at `0x02164480`, which is where `002EF640` points.

Each result is compared with a **direct decode of the files** per the contract's §7, §8 and §12. **6 / 6 cases
pass, and `result.json` is byte-identical over three runs.**

| entry | cases | result |
|---|---|---|
| `002EF2B0` payload base | 1 | returns `0x02164480` (= `002EF640`'s `0x02164280` + `0x200`) |
| `00377970` threshold schedule | **47,740**: every one of the 152 indexes, plus `count`, `count+1` and `0x3FFF`, × 308 progress values (each of the 104 distinct thresholds ±1, plus 0, 1, `0x7FFF`, `0x8000`, `0xFFFF`); the ungated read; a null table | 0 mismatches against §7's parity rule |
| `0032A8A0` authored gate | **262,144**: all 65,536 `u16` encodings × two Primary payloads × two progress values; the upper 16 bits of `ecx` | 0 mismatches against §12; the upper half is ignored; `gate(0xFFFF)` = 0 (§8) |
| `00379160` new-game list | the shipped list over a zero payload; a null table | exactly the decoded bits and nothing outside Primary; a null table writes nothing |
| `002EF2D0` reset + list | payload and 16 guard bytes on each side filled with `0xA5` | the body equals zero plus the list's bits; **the guards are untouched**, so the clear is exactly `0x1538` bytes (§3's size, by execution) |
| `00377440` event-memory predicate | **65,541**: every `u16` id, plus `0x10000`, `0x10031`, `0x7FFFFFFF`, −1, −0xFFCF; a null table | 0 = listed and 1 = absent (the inverted polarity of §2); a null table returns 1 |

## What the execution adds to the contract

| item | observed |
|---|---|
| **§14 item 4 is contradicted: 52 flags, not 53** | `mapjumpgroupinit.bin` has count 53, but **its first entry is `0x0000`**, which `SetPrimary`'s `id − 2u > 0x1FD` bound drops. A new game starts with **52** Primary bits set. §14 item 4 says the file carries "53 … all inside `SetPrimary`'s accepted range" and lists only 52 of them. `persistent-flag-banks.md` (FABLE, DS-1) already reads it correctly |
| `00377440` compares the id **as 32 bits** | `r10d` is compared with each zero-extended `u16`, so `0x10031` reads absent (1) although `0x31` is listed |
| schedule: **the ungated read is progress 0** | with `[02098E20]` bit 0 clear, `00265270` returns 0, and every schedule is evaluated at progress 0 |
| schedule: **no shipped index is "no schedule"** | none of the 152 offsets is 0. §10's "offset 0 = no schedule" edge is not exercised by the shipped file |
| **latent: `00377970` accepts a negative index** | its bound is `cmp ecx,eax / jge` (signed) followed by `movsxd`, so −1 reads the header's count word (`0x98`) as an offset. −2 and −5 walk off the table until a bit-15 entry (the planted page faults). The only caller in `edges.tsv` is the gate, which masks with `0x3FFF`, so no shipped path passes a negative. That is a call-graph negative, not a proof |

## The evidence-class position

- **Before this note:** 11 of 17 entries were covered by §17's differential (reimplementation vs. shipped bytes), and
  6 were not executed.
- **After it:** **17 of 17 entries have been executed as shipped code**, with one declared import bridge (`memset`,
  reset only).
- **What is still true** is §13's own sentence: "Live capture: still absent". Nothing here observes a running game's
  payload.

## Not covered

- a live process: the three §13 confirmations (a known story flag's bit, `gate(0x400B)` at a save, the
  `+0x1394..+0x13B3` zero stretch);
- the script verbs that call these entries;
- the resource-loader publishers `00378B90` / `00378A50` / `00378BA0` (the fixtures stand in for their stores).
