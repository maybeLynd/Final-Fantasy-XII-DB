# DD residue closure, batch 14: batch 10's proposed rows answered statically (SWE2-CONTRACT for OPUS)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 14 (brief `Tools/work/OPUS/lane_brief_dd_b14.md`). A Claude
session ran the batch in the SWE2-CONTRACT lane, started by OPUS. It used no subagents, no board tasks and no commits.

Batch 10 ([record](../swe2contract-ddres-b10-0930/README.md)) proposed seven register rows, P1–P7. This batch answers
six of them statically, in place on their pages. P2 was answered by OPUS
([`opus-look-bit7-0930`](../opus-look-bit7-0930/README.md)) and is skipped. Two id-less rows remain for what cannot be
settled statically. Their dispositions are runtime and NO ADMISSIBLE SOURCE.

The work is static only:
- the certified image (`73461d08…`), through `retool.py` and `structflow.py`;
- the installed `FFXII_TZA.vbf`, for `map_ref.bin`, the 410 `.efb` names, all 89,414 archive names and the
  namespace-12 `.cm` heads;
- the extract `D:/FFXII_TZA_extract`, for the 1,066 `.cm` files. Control Z1 re-decodes `m1132.cm` from the archive.

No status word was moved. Every correction keeps the removed text under a strike, with a
*Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)* note. The checker is
[`b14_checks.py`](b14_checks.py) ([`b14_checks.out`](b14_checks.out)): 317 PASS, FAILS 0.

## The answers, row by row (SWE2-CONTRACT for OPUS)

| row | page | answer | checks |
|---|---|---|---|
| P1 | fef-and-motion-entries.md | **Answered, no route.** The `+0x30` pointer goes only to the `ret 0` stub. A census from every source of the binder's record finds `+0x230` written once and read nowhere. `003EDAD0`'s six callers pass the `.efb` blobs, a boot block filled by file loads, menu `.efx` files and the appended companion, never an `@FEF` entry | A1–A9 |
| P3 | ftr-node-table.md | **Answered (boundary).** No bone record marks an attachment or a marker. The bind path reads only the link, the flag word and the transform stream. Other tables name the bones by index: FCP section 3, the special-bone ids of `003E5AD0`, and the bone-trail descriptors | B1–B2 |
| P4 | ftr-node-table.md | **Answered, except bit 29.** Bits 23–25 are the rest translation (`+0xF0`–`+0xF8`) and bits 26–28 the rest rotation, Euler radians through the `@FMW` sine table. Bit 21 is the `+0x150` matrix that the composer and the skinning palette use. Bit 29's value is never read (row below) | G1–G6 |
| P5 | ftr-node-table.md / fcp-character-parameter-block.md | **Stale.** `UQ-220` was answered on 2026-09-26 (FABLE): section 2 is the rig of seventeen controllers. What each controller holds is the rig page's own section 7. SWE2-STRUCT's batch 12 (`swe2struct-ddres-b12-0930`, no README yet) covers other FCP sections, not section 2. It was checked first, and this row was done last | D1 |
| P6 | ftr-node-table.md | **Answered.** A per-consumer field table for `0041C260`, `00373860` and `00372610`, `00418880` and `003703A0`. `+0x94` is written by `00372820` and `003713C0`, and read by 28 functions, each through `0020E600` | C1–C6 |
| P7 | efx-and-efb-effect-containers.md | **Answered.** Mode 0 asks for the `.efb` of the field block's shared map_ctrl pack. None of the 89 such names ships. Both requests can be pending: FIFO, mode 0 first, and its read fails and frees its own block before mode 1 starts. On shipped data nothing is orphaned. A shipped mode-0 file would leak its block (a modding hazard). The null-name path is runtime (row below) | Q1–Q13 |

## The findings, in player terms (SWE2-CONTRACT for OPUS)

- **The effect inside a model file is never shown.** What appears on a summon or a monster is the separate
  `chara\hNNNN.efx` file the loader appends after the model.
- **Every field load also asks for a second map-effect file, named after the area's shared pack.** No such file
  ships, so the request quietly fails and returns its buffer. A modder who supplies one would see it read and never
  used, and while the field's own effect file also loads, that 4.4 MB buffer is never freed.
- **Each bone's resting pose is in its record:** where it sits, how it is turned, and the matrix skinning uses. One
  more value, close to 1.0, sits in 1,953 bones and is never used.
- **Which bone holds a weapon or a trail is decided by other tables,** never by the bone itself.

## How each answer was reached (SWE2-CONTRACT for OPUS)

**P7, the queue (Q5–Q10).** The OPUS lead was verified and extended. Three corrections to it:
- the job callback is `001D6D70`, not `001D6E7C`;
- `001D6B40` is not a mounted-root check. It looks the path's 31-bit djb2 key up in the in-memory file cache
  `[01F83438]` (`0020BE50`, the key compared alone), and the cache gains keys only from files the open `0059EE90` has
  read (`0059A9B0` → `001D6A20` → `0020B680`);
- that first branch also needs the file-system flag `+0x88` (`0017D930`) and two worker flags (`001D6EF0`).

The stale-status hazard needs a cached key. No mode-0 path's key collides with the key of any archive name (Q12),
which unicorn checks by running `00674A00` itself. The other branch sets the status word to −1, and the job writes
`0xFFFFFFFE` for a failed open (`001A0CF0`). The pump takes state 6, and `0032E370` calls the completion with ok = 0.

**P1, the six callers (A2–A8).** The lead was verified, with one correction: `003B0660`'s pointer is `[01FD4A30]`,
loaded at `003B06F8`, not its argument. `[01FD4A30]` has one writer, the boot hub's `0x3000100`-byte allocation
(`0022A240`), and three file loaders fill it. The `003B2220` table field `+0x28` has four kinds of writer over the 21
functions that address the table: `003B2310` (`[01FD4A30]`), `003B1A80` (0), the memset, and whole-entry moves. The UI
callers' pointer is a fresh namespace-7 block.

**P1, the census (A9).** It is `structflow` with the record's real size `0x260` as stride. One fix was needed:
`__chkstk` (`00808F10`) keeps the argument registers. Without it the census lost every large-frame callee, and it
missed `0053AB50`. Its positive control is batch 10's three `+0x218` / `+0x21C` readers, and it finds all three.

**P6, the `+0x94` census (C6)** seeds both skeleton pools (`+0xD98`, `+0x330`). Its control is the four known writes.

## Proposed register rows, id-less, for SWE2-DATA (SWE2-CONTRACT for OPUS)

| page | question | disposition |
|---|---|---|
| efx-and-efb-effect-containers.md | For the 34 fields whose block index names no map_ctrl package, and the 121 whose own index names none, 002DF880 returns -1 without writing and 00377DC0 requests whatever its stack buffer held. Which path is requested, and is any such field ever loaded? | runtime (stack contents and which fields a session loads) |
| ftr-node-table.md | What does the u16 that bit 29 adds to an @FTR record name? It always indexes the aux pool, on a float between 0.92 and 1.38 (1.0 in 1,697 of 1,953), and no code reads it | NO ADMISSIBLE SOURCE (no reader in the image; the binder sets every bone's scale to 1.0) |

## Proposed status lines (SWE2-CONTRACT for OPUS)

These are for OPUS's owner read. None is applied.
- **efx-and-efb-effect-containers.md:** `DOCUMENTED — §2b and §2c (SWE2-CONTRACT DD batches 10 and 14) answer the residue
  this line named and the mode-0 request; the null-name request path is runtime (<row id>)`, once the first row above is
  registered.
- **fef-and-motion-entries.md:** `DOCUMENTED — the embedded EFX0010 reaches only the ret 0 stub (DD batch 14, A1–A9);
  which @FEF models a session loads and the target-bearing arm's look are runtime-only`.
- **ftr-node-table.md:** `DOCUMENTED — flags, aux values, consumers and tail readers read (DD batches 10 and 14); bit 29's
  value is NO ADMISSIBLE SOURCE (<row id>)`, once the second row above is registered.
- **fte-fct-texture-colour-tables.md:** `DOCUMENTED — the residue is answered (DD batch 10); what a co-drawn model that
  shares a texture key shows is runtime-only`.

## Receipts (SWE2-CONTRACT for OPUS)

| script | result |
|---|---|
| `b14_checks.py` (`b14_checks.out`) | Q1–Q13, A1–A9, G1–G6, C1–C6, B1–B2, D1, Z1: 317 PASS, FAILS 0 |
| `documented_rule.py` on the four edited pages (`documented_rule.out`) | READY for all four (`TALLY READY=4 of 4`), FAILS 0 |

Controls and blind spots:
- **Q11's indices** equal `map-ref-field-packs.tsv` in all 1,315 rows, and the archive's 410 `.efb` names are
  counted.
- **Q12 tests collisions against archive names only.** A cached file from outside the archive is not covered.
  Q13 shows the install holds no loose `PS2Data` tree.
- **The file layer `0059EE90` was not read whole.** Q8 pins the failed-open result, and Q13 shows no loose file exists.
- **A9 and C6 are `structflow` censuses,** three calls deep. They do not see indirect-call targets (none was tagged)
  or code outside retool's extents. Each has a positive control.
- **C4 reads `00418880` only through `r15`.** That register holds the bone at `0041947A` and the owner elsewhere in
  the body. Snapshot reads through other registers are not claimed.

## Consumer check (EVIDENCE-POLICY 4a/4b/4c) (SWE2-CONTRACT for OPUS)

See [`consumer-check.md`](consumer-check.md). No consumer disagrees. FABLE's `uq218-embedded-efx-sweep` record
leaves the caveat open, and it is routed, not edited.

## Not touched, and why (SWE2-CONTRACT for OPUS)

- **`fcp-character-parameter-block.md`** carries SWE2-STRUCT's uncommitted batch-12 edits, so it was not opened for
  editing. P5's answer is on the ftr page.
- **OPUS's P2 note on the fef page** (the `opus-look-bit7-0930` line in the batch-10 residue list) was in the working
  tree at the start of this batch. It was gone when the fef page was edited: `git status` showed the page clean at
  HEAD. Please re-apply it on top of this batch's edits.
- **The status lines** were left for OPUS's owner read, and the proposals are above.
