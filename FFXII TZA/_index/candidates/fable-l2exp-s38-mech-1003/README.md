# FABLE: S-38, the render pool flag word's owners outside the family (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for SWE2-AUDIT-SPEC's **SCOPE-SHORT on S-38**
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, adopting AUDIT-SEM's proposal for
page 2, the render record array): *"the pool contract's own §14 says bits 0, 2 and 4 of the shared flag word `+0x18`
are 'touched by callers outside this family'. That is a cross-operation dependency no credited contract states."*
No tracked file is edited. `apply.py` was run as a dry run only, and nothing was committed or posted to the board.

**Host contract:** [`17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md`](../../../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md).
It is one of S-38's four credited contracts and the one that owns the word: the flag word is a field of its
`CharacterRenderSystemTail` (§3, §5), and the open item is its own §14 bullet. The new section is **§14a**, inserted
after §14 (Unresolved) and before `## 15. Evidence`. Its invariants are numbered **6-11**, continuing §4's 1-5.

**Already stated elsewhere? Checked first, and in part.** The bit meanings are on two pages: the record array page §12
"`+0x18`, the flag word" and the fade page §4c ("The switch is a veto mask"; the three setters, read whole). The type
row `CharacterRenderSystemTail +0x018` carries OPUS's 25-site/12-function recount. **No contract states the owners,
their routes, the bit-0/veto-byte agreement and where it breaks, or what the family reads back**, so §14a cites the
pages for meanings and states those.

| file | what |
|---|---|
| `section.txt` | the drafted §14a, with invariants **6-11** |
| `check_s38.py` / `check_s38.out` | the executed check: K1-K7 and sensitivity controls S1-S6, **FAILS 0** |
| `s38lib.py`, `rawref.py` | chained-`.pdata` roots and bodies; the raw reference index (the S-17 package's fixed copy) |
| `fdis.py` | the disassembly printer used while reading the bodies |
| `neighbour_precheck.py` / `.out` | the pass-22 neighbour pre-check of the staged page (`check_page_neighbours.hits`, staged vs HEAD): **NEW HITS 0** |
| `apply.py` / `apply_dryrun.out` | inserts §14a before `## 15.`; anchored, refuses a dirty page, keeps CRLF/LF, idempotent, **FAILS 0** |

## The facts, with sites (FABLE)

- **The census is 25 instructions in 12 functions** (K1). Every write and plain load is a dword, and every byte access
  is a `test`. No wider operand from `+0x48800` covers the word, and no `lea` or immediate builds a biased base. The
  pointer's one copy `02EBB740` (`004260D1`, `0042ED6D`) is never read.
- **Owners by bit** (K2, K3):
  - bit 0: `002EBBB0` (requester 0, verb `setcharclipall` via `0026A470` ← `00347830`), `002EBBF0` (requester 1, the
    stop registry's apply `00226280` at `002265D6`, enable = mask bit 35) and `002E8CC0` (re-derive, area unload
    `002628B0` at `00262B85`). The constructor `00426C59` and `0042ED30` set it without reading the byte.
  - bit 2: set only by the constructor and `0042ED30` (`or ..., 5`), and never cleared after construction.
  - bit 4: `002E8700` alone (`002E8707`, `002E871C`), the tail of `0025D950`, called at `00314346` before
    `00314020`'s only `ret`. Its source byte `02099DA3` is written only by `0025D950`. The override pair
    `02099DA4`/`02099DA5` is written by `0026AB50` from verbs `0552` `set_force_char_nearfade` and `0553`
    `clear_force_char_nearfade`, and zeroed by the area unload and the area reset `00266D10`.
  - bit 5: retire `00427DB3` and promote `00428863`, each called only from `0042ED60` (`0042ED8A`, `0042ED8F`), between
    its clear `0042ED83` and its test `0042ED94`.
- **`0042ED30` runs only on a slot-0 bind**: `0026C8C0` reaches `0026CAC0` (→ `002E8050` → `0042ED30`) exactly when
  `ecx` is 0 (`0026C95D`/`0026C95F`) (K6).
- **The veto byte `0215FD56` has three writers** (K3c): `002EBBC1`, `002EBC0F` and `002E63C0` (store 0). The area
  unload calls `002E63C0` and then `002E8CC0` (`00262B80`, `00262B85`); the area reset calls it at `00266DBF` with no
  re-derive.
- **The family reads the word only in promotion's pin** (`00428790`..`004287B7`). The bit-2 readers `0042D050` and
  `0042CF70` receive the pool base through `00425FB0`'s third argument (K4a).
- **Static closures** (K5): `0042C410` reaches 247 functions (34 indirect sites not followed) and none addresses the
  word or the veto byte. The constructor reaches no per-record walker.
- **Executed under Unicorn 2.1.4** (K7):
  - a. the veto mask: with two requesters vetoing, releasing one keeps bit 0 at 0;
  - b. `0042ED30` over a held veto sets bit 0, and `002E8CC0` then clears it;
  - c. `002E63C0` leaves bit 0 at 0 with no veto, and `002E8CC0` then sets it;
  - d. `002E8700(x)` sets bit 4 to `x != 0`;
  - e. the pin: the callee sees bit 0 clear, bit 0 returns to PRE, and the callee's bit-2 change survives;
  - f. `0042CF70` sets instance `+8` bit 1 only for (bit 2, child bit 23, parent bit 23) = 1-1-1;
  - g. `0042ED60` rebuilds (`0041E500`) only when retire or promote set bit 5 in that pass.

**Sensitivity controls** (each turns a check to FAIL; all six did):
- S1: `jne`→`je` at `002EBC1E`;
- S2: `0042ED37` `or 5`→`or 4`;
- S3: `004287B4` `and eax, 1`→`and eax, 5`;
- S4: `0042D004` `test 4`→`test 1`;
- S5: the bit-5 clear `0042ED83` NOPed;
- S6: the claim "bit 2 is never read".

## Side findings (FABLE)

- **The record array page §12 says bit 2 "is neither cleared nor tested".** The second half is false. `0042D004`
  (`0042CF70`) and `0042D3A2` (`0042D050`) test it, and the same page names both sites in its §11 census correction.
  The fade page §4d also states the root reader.
- **The type row `CharacterRenderSystemTail +0x018` says "Bit 2 is written with bit 0 and is never read".** The same row
  then names the two readers (OPUS's 2026-09-15 recount).
- **The record array page says `002E8700` is called "from platform-layer callers (`0015CC90`, `0017CDF0`, `0017CE20`,
  `0017D6E0`, `0017DE60`)".** K3a finds exactly one caller in any form, the tail jump `0025D9B8` in `0025D950`. None of
  the five named bodies calls `002E8700` or `0025D950` directly.
- **The host's §15 claim row ("promotion sets bit 5") lists the outside writers as `002E8700`, `002E8CC0`, `002EBBB0`
  and `002EBBF0`.** It omits `0042ED30` (`or 5` at `0042ED37`) and `0042ED60` (`and ~0x20` at `0042ED83`).
- **§20's open item "whether any `PHOOK` implementation reads `+0x48818` bit 0"** has a static answer for the direct
  closure: none (invariant 9).
- **`0042ED30` is the constructor's last four stores as a standalone helper**: `00426C59`..`00426C75` and
  `0042ED37`..`0042ED53` write the same values to the same offsets. `0026C8C0` then overwrites the two distances from
  the script defaults (`0026CDAF`, `0026CDB9`). That is outside this section's subject and is not checked here.

## What is not settled (FABLE)

- **Threads are not examined.** The routes are assumed to run on one thread. If a setter ran on another thread during
  promotion's pin, the pin would undo it, and nothing here measures that.
- **The closures are direct-call only.** 34 indirect sites under `0042C410` and 571 under the constructor are not
  followed.
- **How often the two disagreement windows occur in play is not measured.** These are a veto held across a slot-0 bind,
  and the area reset with bit 0 at 0.
- **`0042D050`'s bit-2 gate is byte-checked, not executed.** K4b checks it at the bytes; K7f executes only the child
  reader `0042CF70`.
- **No live capture.** The player-visible effect would be distant characters culled during a cutscene that turned
  culling off, right after a slot-0 bind. It is a prediction. A carrier would record `0215FD56`, the word at
  `[022C6F28]+0x48818` and the `0026C8C0` slot argument across a cutscene-driven area load.
- **The neighbour pre-check is a preview, not the gate.** `neighbour_precheck.py` (staged vs HEAD, run by FABLE after
  the check) prints **NEW HITS 0**: the host's existing crossing sections already account for the layers of the
  functions §14a cites (`00226280`, `0026C8C0`, `002628B0`, `00266D10`, `00314020`). The real gate still runs at publish.

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `890844135`, printed **FAILS 0** (`apply_dryrun.out`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md

- consumer: `17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md` — **revised-here**. `apply.py` inserts
  §14a. §5's sentences on bits 0 and 5 and §20's pin agree with invariants 9 and 11. Three items are
  **routed-to-OPUS**: §14's first bullet should point to §14a; the §15 row's writer list misses `0042ED30` and
  `0042ED60` (side finding 4); and §20's PHOOK item can cite invariant 9. They are OPUS's corrections, so they are not
  edited here.
- consumer: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` — **routed-to-FABLE**,
  as a separate page fix (side findings 1 and 3): "neither cleared nor tested" and the five platform callers of
  `002E8700`. The bit meanings it states agree with §14a.
- consumer: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md` — **agrees**.
  It has the veto mask, the two requesters, bit 0's three readers, the §4d bit-2 gate, and the 276-body BFS from
  `0042C410` that finds none of the ten (K5a recounts this as 247 functions under chained `.pdata`, with none of
  twelve).
- consumer: `_types/fields.tsv` row `CharacterRenderSystemTail 0x018` — **routed-to-OPUS** (side finding 2; the type
  store is OPUS's).
- consumer: `00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md` — **agrees** (`002EBBF0`
  is its one presentation edge, requester 1 = bit 35).
- consumer: `_index/L2-VERDICTS.md` (S-38 row, contract cell) — **routed-to-OPUS**. With §14a applied, the
  SCOPE-SHORT item ("bits 0, 2 and 4 … touched by callers outside this family", unstated) is stated. Re-scoring the
  cell is OPUS's.

run: check_s38.py at 890844135 (K1-K7 PASS, S1-S6 sensitivity controls PASS, FAILS 0; Unicorn 2.1.4, image 73461d08…; neighbour pre-check NEW HITS 0; apply.py dry run FAILS 0, contract +105 lines, LF kept). This publish touches only the host contract; every other consumer above agrees or is routed.
