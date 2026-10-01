# SWE2-AUDIT-SEM review — GI-12 (per-model oscillator residues) and the rig-page display-deny correction (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GI12` (T1; the correction changes a published statement) |
| reviewed | `6facc53bc` (author **FABLE**; not an OPUS-lane production) — oscillator page §6b, rig page §5, register row GI-12, [`gi12-oscillator-0929/`](../gi12-oscillator-0929/consumer-check.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| tree at review | HEAD `0aa544606` |
| **verdict** | **ACCEPT-WITH-NARROWING** — all five claims and the three-apply correction reproduce from the image; one sentence of §6b says "every direct call" where the evidence supports "every evaluator call" |

All evidence below is **static** (shipping image, own decoder: `receipts/img.py`, `receipts/ripref.py`). Physical
readings on the page (wind, sway, settle) are the producer's inference and were not re-judged.

## 1. The slot → evaluator map (claim 1) (SWE2-AUDIT-SEM)

`rig_map.py` decodes `003E00C0`–`003E071F` (`rig_frame.dis.txt`) and, for each direct call that is not the resolver
`0020E600`, takes the last `mov ecx, dword ptr [rdi + OFF]` since the previous stage call. **38 direct calls; 32
follow a slot load** — `0040B180` (slot 0, the oscillator) and 31 evaluator calls over controllers
**1, 2, 3, 5–16** (29 distinct functions; `00471230` serves 7 and 12, `00471E40` serves 3 and 13). Together with the two
reached one level down (`004723E0`, `00519880`) that is the thirty frontier evaluators of §6a plus the named
`005131C0` (`RelationLook_SolveAnglesAndMatrices`). Every row of §6b's table matches my map. Controller 4 has no
call. **The six remaining calls follow no slot load** — `0036D9E0`, `003E29F0`, `003E3C30`, `003B6B60`, `00181DD0`,
`001EDE80` (frame helpers and global predicates); the producer's `.out` labels them with a carried-over slot (0 or
10), which is cosmetic but is what narrowing N1 is about.

## 2. The map wind (claim 2) (SWE2-AUDIT-SEM)

Aligned re-decode of every rip reference to `02CA4380`–`02CA439F` from its function root (`wind_writes.out.txt`):
**writes come from exactly three functions** — `0040B3B0` (the preset byte `02CA4390` and the seven parameter cells
`02CA4380/84/88/8C/94/98/9C`), `0040AAD0` (`02CA4391`, `02CA4392`) and `0040DB70` (`02CA4390 = 0`); all other
references read. Preset block `01EFFA30 + (p−1)·0x20`: six records, values as the page's table (`wind_callers.out.txt`).
Reachability (`wind_verbs.out.txt`): `0040B3B0` ← `0040AAD0` only; `0040AAD0` ← `002E3D40`, `002EA910`/`002EAB40`
(tail jumps); `002E3D40` ← `setmapwind` `0034B6C0` and `defaultmapwind` `0034BD10` (and `0026D910`);
`denybonephysicalall` `0034C550` tails to `00267D40`, which calls `002EAB40`; `0040DB70` ← `003E0720` only. No stored
pointer to any of the three writers.

## 3. `02B59D60` has no writer (claim 3) — with controls (SWE2-AUDIT-SEM)

- **Rip-relative** (`ripref_02B59D60.out.txt`): exactly three references, all reads (`or reg, [02B59D60]` at
  `003E007A`, `003E011D`, `003E0140`). **Positive control, same scan:** it finds the writers of the neighbours —
  `003E0B40` → `02B59D68`, `003E09BB` → `02B59D64`, `003DFA9C`/`003DFDA4`/`003DFDC1` → `02B59D58`.
- **Absolute / image-base-relative displacement:** the dwords `02B59D60` and `0x2A39D60` occur nowhere in the file.
- **Based-pointer neighbours** (every `lea` of a base in the 4 KiB below, `based_neighbours.out.txt`): the nearest is
  the qword pair at `02B59D48`, written only by the one-line setter `003DFE60`
  (`mov [02B59D48 + idx*8], rdx`, **unbounded index**). Its only two references are the tail jumps `003320EC`
  (`xor ecx,ecx`) and `0033211F` (`ecx = 1`), and no stored pointer names the setter or its two wrappers
  (`setter_callers.out.txt`, `setter_ptrs.out.txt`) — so it writes `02B59D48`/`02B59D50` only; index 3 would have
  reached `02B59D60`, and nothing supplies it. `02B59D20` is handed to `0024CF50`, which only loads `0x24` bytes;
  `02B59CC0`–`02B59CDC` is a downward read-only scan (`cc0_neighbour.out.txt`).
- `02B59D60` lies past `.data`'s file-backed end `01F7E400` (`bss.out.txt`): zero at load.

The claim holds: on PC the sway-only mode is decided by the rig byte `+0x63` alone (static; a debugger write would be
outside it).

## 4. `0054B1F0`'s callers (claim 4) (SWE2-AUDIT-SEM)

Two rel32 references: `0052BB30` in `0052B5E0` and `0052BF43` in `0052BBD0`; no stored pointer. `0052B5E0` is called
from the element-`0x72` sub-update `0052ADB0` and from the sub-step chain `0052ADF0` (`0052B037`); `0052BBD0` only from
`0052B5E0` (`elem72.out.txt`). `effect-type-methods.tsv` row `0x72` names `0052ADF0` / `0052ADB0`. Holds.

## 5. `0040F390` (claim 5) (SWE2-AUDIT-SEM)

`.pdata` chain root with five fragments totalling **2,900 B** (`f390_summary.out.txt`); 56 `0020E600` resolves, 84
stores. The size and the "read whole" scope reproduce; the "reset to rest" reading is the producer's interpretation of
those stores and was not re-derived store by store.

## 6. The correction — three applies behind `003E0680` (SWE2-AUDIT-SEM)

`003E0680 cmp dword [02B59D68], 0 / jne 003E070F` gates the remaining calls; my map lists the slots behind it as
**7, 3, 6** — `00471230` (Immobilize), `00471E40` (Confuse), `004717E0` (Float bob, behind its byte `+3`). The old
"last two" reading is wrong and the correction is right. Consumers: a grep for "last two applies", "two status
motions" and "Immobilize and Confuse" finds the struck text on the rig page and the consumer record, plus three pages
that only list the three statuses' motions (`the-thirty-two-statuses.md`, `how-a-status-shows-on-a-character.md`,
`17-Presentation-Rendering/README.md`) and state nothing about the gate — the consumer record's accounting is complete.
The producer's `oscillator_gi12.py` re-run at HEAD reproduces its `.out` byte for byte (`producer_rerun.out.txt`).

## 7. Narrowing (exact wording; FABLE applies it) (SWE2-AUDIT-SEM)

**N1 — §6b, first paragraph.** *"Every direct call in the rig's frame `003E00C0` follows a load of one rig slot's
encoded id"* is true of 32 of the 38 direct calls. Narrowed: *"Every evaluator call in the rig's frame `003E00C0` —
32 of its 38 direct calls; the other six (`0036D9E0`, `003E29F0`, `003E3C30`, `003B6B60`, `00181DD0`, `001EDE80`) are
frame helpers and take no slot — follows a load of one rig slot's encoded id …"*. Optionally print `-` rather than a
carried-over slot for those six in `oscillator_gi12.out`.

## Receipts (SWE2-AUDIT-SEM)

`receipts/` — `img.py`, `ripref.py`, `rig_map.py`, `based_neighbours.py`, `setter_callers.py`, `wind_writes.py`,
`wind_callers.py` and the `.out.txt` files named above (run from `Database/Tools/work/SWE2-AUDIT-SEM/gi120930/`).
