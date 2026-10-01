# SWE2-AUDIT-SEM review: FABLE's pass-22 crossing readings, 19 pairs on 7 pages (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor), self-initiated from OPUS's list of today's unreviewed FABLE-side
commits. FRONTIER's pass-22 batches 1-7 were already reviewed (`d14435a65`, `316986fa1`). This review covers FABLE's
own batch.*

| | |
|---|---|
| task | `AUDITSEM-REVIEW-P22-FABLE-0930` |
| reviewed | `4407f8484` (author **FABLE**): 10 crossing sections on seven pages, 9 `neighbour-dispositions.tsv` rows, one struck sentence (gamepad page) and one prose correction (field map). Record [`pass22-fable-0929/consumer-check-0929-p22-crossings.md`](../pass22-fable-0929/consumer-check-0929-p22-crossings.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| checker | [`p22f_sem.py`](p22f_sem.py), [out](p22f_sem.out): 76 PASS, `FAILS 0`. Capstone reads the image directly, edges come from `Tools/work/graph/edges.tsv`, owners from `functions.tsv`, and verbs from the shipped verb table. The producer's `rebuild_edges.py`, `groups.py`, `apply.py` and `audit_crossrefs.py` are not run. |
| **verdict** | **ACCEPT-WITH-NARROWING**. Every sampled far end is real, every relationship matches the bytes, and every cited site holds. Each section is a reading, not a count. The narrowing: the two consumers the package routed to "FABLE-P22-FOLLOWUP" have no board task, and both false sentences are still unstruck at HEAD. |

## 1. The sample (SWE2-AUDIT-SEM)

The sample covers every registry row, every section on six of the seven pages, and on the field map one check per
group:

| check | what the package says | what the image says |
|---|---|---|
| Ra | `003601B0` / `003601C0`: 14 B / 16 B, set / clear one bit of `022CB720`; callers `002628B0`, `003614E0`, `00361460`, `003145E0` | holds, and all four edges are in `edges.tsv` |
| Rb | `00203170`: 44 B identity-matrix store; seven UI callers; `seteventlightdir` `00356160` | holds. The four rows read back as the 4×4 identity. See N2 for the address range. |
| Rc | `001EDE70`: `mov eax,[01F82E38]; ret`, 22 callers; `00253C70` calls it at `00253D8F` | holds (22 callers) |
| Rd | `001EDE80`: 61 B, 7 callers, returns 1 unless half-rate, else two frame counters summed; `0025DFA9` then `je 0025E12B`; `003FA7F8` skips `003FC170` | holds |
| Re | `00187950` calls `001A1470` (35 callers) three times with `[01F7F4C0]` and size 0x10 | holds at `00187AB5`, `00187AFE`, `00187B4F` |
| Rf | four D3D11 bodies call `005FD050` (55 callers) | holds |
| S1 | `00236760` / `00236780` are bit 12 / bit 14 of `[02EBF190]+4`; save sites `001C1758`, `002EF696`; `00583D60` ORs `+0x57` with 1 and 4 | holds (`00583F5A`-`00583F70`) |
| S2 | `00290180` = `mov eax,2; ret`; `is_ntsc` (0x4EB, handler `003423E0`) pushes `== 2` | holds (`cmp eax, 2; sete dl`) |
| S3 | `00264670`: 35 B; for class 3, float `[[+0xB8]+0xD4]`, else 0.0; floor probe `002F3750` and `getgroundy` `00343520` | holds |
| S4 | `00265090` for class 3 tail-jumps with `rcx = [+0xB8]+0x50`; loot `002FB150` calls it at `002FB1C1` | holds |
| S5 | `003E7650`'s only caller is `00314020`, at `00314341` | holds |
| S6 | `00182E80`: 41 B; `+0x14` of the display object at `01F82D18`, else `0x438`; `00187993` | holds (through `001DDAB0` and `002256A0`) |
| S7 | dispatch page: 57 edges, 54 handlers, six accessors (23/17/14/1/1/1) | holds by ledger owner. Every script-layer caller of `0053DD10` is a verb-table handler. `00341876` tests its constant answer. |
| S8 | field map F1/F2/F3/F5, I1: `0031B860` matches `[unit+0x698]`; `imul 0x1C8` at `00320A4B`/`00320AC7`; `00300BDD`-`00300BF0`; `00386C2E`-`00386C3F`; `003244E1 or [rbx],0x40`; `00324380` builds the snapshot at `022C257C` | holds |
| S9 | RNG: LCG `00328370` draws at `002356A3`, `003081FF`, `00239547`; MT `00379CD0` from `00386C70` / `00388660`; `00308EC0` | holds |

**Reading, not volume.** Each section names its far end, gives one relationship per group with the direction, and
cites the instruction sites that show it. The nine registry rows each carry the body of the shared leaf and why the
crossing is mechanical. That is what the 2026-09-14 ruling and the pass22-debt README ask for.

The field map's larger groups (F3, F4, F6, and I1-I5) split their SERVICE and CLIENT counts by ledger name and call
direction, not by reading each far end. Each section's "Tier" line states this, and the representative sites I sampled
hold. This is disclosed, not overclaimed.

## 2. Narrowings (SWE2-AUDIT-SEM)

1. **N1: the routed follow-ups are not tracked, and both false sentences remain at HEAD** (checks H1, H2). The consumer
   check routes two consumers to "FABLE-P22-FOLLOWUP", but no board task carries them.
   - **Field map, section 11 crossing note.** Line 921 still says "`00236780` is the shared RNG/roll helper",
     unstruck. The same page's pass-22 section now says it is the bit-14 flag getter. The page contradicts itself.
   - **Staged-look page, `Gameplay - CLIENT`.** It says "`00203170`, the per-slot visitor this page's `003E3C30`
     section names". The page is AUDITED. `003E3C30` is the visitor: it loops over the index array and calls
     `00203170` once per slot at `003E3C7A`. `00203170` is the 44-byte identity-matrix store it applies. The page's own
     `003E3C30` section already says this. The `UI - CLIENT` paragraph's "one shared per-slot routine serving the UI's
     own record walks" would read better as the identity-matrix store.

   Routed:
   - the staged-look sentence as the contradiction `AUDITSEM-CONTRA-FABLE-STAGED-LOOK-00203170-0930`;
   - the section 11 strike and N2 as the request `AUDITSEM-REQ-FABLE-P22-FOLLOWUPS-0930`.
2. **N2: the address range (wording).** The dispatch page's `00203170` bullet says the four rows are "copied from
   `008C5F80`..`008C5FD0`". The sources are `008C5F80`, `008C5F90`, `008C5FB0` and `008C5FD0`, not a contiguous 64-byte
   run. The registry row already lists all four, and the dispatch bullet could do the same.

Nothing else is corrected. Classes, counts and cited sites all hold.
