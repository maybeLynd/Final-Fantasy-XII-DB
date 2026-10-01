# SWE2-AUDIT-SEM review: SWE2-DATA's DD owner read batch 5, five Movement-and-Navigation pages (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by SWE2-DATA and assigned by OPUS.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-OWNER-READ-5-0930` |
| reviewed | `b92561451` (author **SWE2-DATA**). The five `06-Movement-And-Navigation` pages, the register's "SD (batch 5)" rows SD-180..SD-184 and SD-190..SD-193, and record [`dd-data-5-0930`](../dd-data-5-0930/README.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| checkers | [`dd5_sem.py`](dd5_sem.py), [out](dd5_sem.out): 26 PASS, `FAILS 0` (capstone on the image; census through `retool.py refs`). [`strike_check.py`](strike_check.py), [out](strike_check.out). [`sd_rows_check.py`](sd_rows_check.py), [out](sd_rows_check.out). [`producer_rerun.out`](producer_rerun.out). |
| **verdict** | **ACCEPT-WITH-NARROWING** (the record's own word would be ACCEPT-WITH-CORRECTIONS). The four named readings hold at the byte level, 25 of 25 strikes quote the parent verbatim, and the reconciliations agree. There are two corrections: one strike removed a true statement, and one SD row's gate omits a test. Two more SD rows state limits that one short read closes. |

## 1. Question 1: strikes and anchors (SWE2-AUDIT-SEM)

- **The strikes quote the parent.** `strike_check.py` compares each new `~~…~~` span with the parent page (whitespace
  normalised). 25 of 25 are verbatim: 4 on battle locomotion, 2 on 3D/flat, 8 on the movement mode page, 6 on
  clamping, 5 on the distance primitives.
- **The producer's checkers reproduce.** `mv_clamp_checks.py`, `mv_loco_checks.py` and `mm_checks.py` were re-run at
  `cb5b622f2`. Each output is identical to the committed `.out` (`FAILS 0`).
- **The anchors hold.** Checks L1-L4 in `dd5_sem.py` confirm:
  - `0033C956` is `addss` of 5.0 (`009146E4`);
  - `0033D747` multiplies by 0.5 (`01CEBB70`) and `0033D751` divides by 3.0 (`008F311C`);
  - `00339F00` sends modes 1/4, 2 and 6 to `0033CEF0`, `0033D200` and `0033BAA0`;
  - DecodeOrderGoal `00312730` is 965 B.

## 2. Question 2: the named readings (SWE2-AUDIT-SEM)

- **The `00363FD0` output (K1-K3, K7, K8).**
  - The arguments are copied to `022D92A0` / `B0` / `C0`, and the bounds are loaded from `01EF93F0` / `01EF93FC`.
  - The squared distance is stored to `022D92E4` (`003641D4`) and `022D92D4` (`003641DC`).
  - The only call site is `0036228A` in the 388-byte chain body `00362230`. That body walks `[r8+0x14]` segments of
    `0x20` bytes from `+0x40` and reads `022D92D4` after each call.
  - The walk `003631B0` is 512 B. It forms each record as a u16 offset plus `[022CBAF0]` (`00363263`) and dispatches
    on byte `+9` & `0x7F`: 0 ellipse, 1 box, 2 chain, and any other value copies the point unchanged (K4, K5).
- **The `02B40534` writer count (W1).** The image-wide rip-relative store census gives **8 store sites in 8
  functions**: `003B6ED0`, `003B6F30`, `003B7080`, `003B72F0`, `003B7BB0`, `003B7C60`, `003B7E00` and `003B7E20`.
  The corrected count holds.
- **The mode-5 setter (M2).** `002692E8` is `mov byte ptr [rcx+0x28], 5`, with `rcx = [[actor+0xB8]+0xF0]`, as UQ-101
  has it.
- **The EC7-105 kind correction (M1).** `00263CC0` computes `(byte[+3] >> 5) − 1`. When that is 0 (class 1) it reads
  `+0x38`; when it is 2 (class 3) it reads `+0xA4`. So the corrected text is right.
- **The integrator's one caller (M3).** `0025E3AA` passes `edx = ebp`. But see correction C2.
- **The modding constants (M4).** π/20 = `0x3E20D97C` is an immediate stored at `0026C224`. The 0.5° floor
  `0x3C0EFA35` is loaded at `002E5806` from `00D0F8DC` in `.rdata`, and compared by `comiss`. It is a constant but
  not an immediate. The page does not call it one.

## 3. Question 3: is each SD row real residue? (SWE2-AUDIT-SEM)

`sd_rows_check.py` lists, for each new row, the register rows and parent-commit candidate folders that share its
addresses. All nine rows are named on their page. Reading the overlaps gives:

| row | finding |
|---|---|
| SD-180 | Residue. **Narrowing N1, optional.** After the clamp the walk calls `00361810` with the `+0x38` / `+0x54` / `+0x58` floats, the global `022CBA8C` and the record, then calls `003638B0(record, …)`. It returns its own `r9d` argument, or `003638B0`'s result when `00361810` returns 0.0 (`003632D1`-`00363350`, K6). What those two bodies compute stays open. |
| SD-181 | **Its stated limit is one sweep from closed (correction C3).** The row says "the loader that fills that base is not traced". The base `022CBAF0` has exactly three writers (F4): `00362F70` zeroes it (called from `00266D10`), `00363730` zeroes it (from `00378230`), and `003635C0` stores `rcx` (from `003775D0`, which passes `[02ADD060]`). The open part is what fills `02ADD060`, and so which file. |
| SD-182 | Residue. |
| SD-183 | Residue. AM-7 gives the routing only; `U-4` and the pass-22 notes are census-level. |
| SD-184 | Residue. |
| SD-190 | **The gate is misstated, and the predicate is readable (correction C2).** See below. |
| SD-191 | Residue. BV-5 has the verb families, not which scripts use them. |
| SD-192 | Residue. |
| SD-193 | Residue. The worksheet's `003EC040` line was an open item, not a reading. |

**SD-190 in detail.** The row, and the page's §10 correction, say `ebp` is 1 only when actor `+0x0D` bit 1 is set, the
render record is live and `003E6A70`'s result has bit 0 set (`0025E328`-`0025E36E`).
- **A gate is left out.** Just before the cited range, `0025E31D` calls `003E68B0(record)` and puts the result in
  `ecx`. `ecx` is 0 (`ebp`, still 0 from `0025DF1F`) when the record is not live. The bit-1 test at `0025E328` only
  selects between `ecx` and 0 (`cmovne`), so `003E68B0` must also be non-zero (F2).
- **The predicate is 13 instructions deep and can be read.**
  - `003E6A70` returns 0 unless `003E6E60(record)` succeeds. Otherwise it tail-jumps to `003AEF50(record + 0x550)`, the
    embedded tween object (`_types/fields.tsv`).
  - `003AEF50` walks the list at `[obj+0x18]` (record `+0x568`) through `+0x48`. It sets bit 0 when any node's byte
    `+1` is non-zero and bit 1 when any node's byte `+2` is non-zero.
  - `003E68B0` is the same wrapper over `003AEF20`, which answers 1 when the object's first dword is non-zero and its
    list is non-empty (F3).
  - Bit 1 of `003E6A70`'s result is also used: it becomes `esi`, which sets `[rbx+0x10]` bit 2 and actor `+0x0C` bit
    4 and is passed to `002E5030`.
- **What stays open** is what a tween node's byte `+1` means.

## 4. Question 4: reconciliations (SWE2-AUDIT-SEM)

These agree with the register:
- AM-1 (45° / 120° / 20°), AM-2 (the arrival curve), AM-7 (the dispatcher);
- BV-1..BV-5, each an evidence row whose box and addresses match its row;
- DP-2 (SUPERSEDED 2026-09-26), UQ-101 (`002692E8`).

**CON-129.** `REQ-OPUS-NAV-RESIDUAL-BOUNDARY-FINDINGS` closed "ADOPTED in `aeb50a133`" and filed CON-129.
`aeb50a133` touched only `CONTRADICTIONS.tsv`, so the page's "its result was the ledger row CON-129 and it adopted
nothing here" is right. The adopted EXP-138 formulas are labelled MODEL-PROVEN for fixture parity, which is the right
tier.

## 5. Corrections (SWE2-AUDIT-SEM)

1. **C1: a true statement was struck. `01EF93F0` / `01EF93FC` are not constants.**
   - The clamping page struck "what the two clamp constants are (they are `.data` addresses, not immediates)" and now
     calls them "the clamp constants `0.0` (`01EF93F0`) and `1.0` (`01EF93FC`)", including in the Key addresses table.
   - The struck parenthesis was true. The cell is `.data` (F1): the x and w lanes of the software `vf00` image, which
     `00363FD0` loads live.
   - Its three writers are `0036D9A8`, `0036D9E8` and `0036DD87`, and all of them store `[0, 0, 0, 1]`. The file image
     holds the same four floats. CONTRACT-transform-primitives §15b records this and says outright "which is `.data`,
     not a constant".
   - Fix: restore the mechanism, e.g. "the bounds are live loads of the `vf00` cell's x and w lanes (`0.0` / `1.0`;
     every shipped writer stores `[0,0,0,1]`)". Link the contract.
2. **C2, SD-190 and the movement-mode page §10: the gate omits the `003E68B0` test.** Add "and `003E68B0` answers
   non-zero (`0025E31D`)". Narrow the residue to what a tween-list node's byte `+1` means, since `003E6A70` reduces to
   `003AEF50` over the record's embedded tween object (§3).
3. **C3, SD-181: the base's writers are traced.** The row should say that the setter is `003635C0(rcx)`, called from
   `003775D0` with `[02ADD060]`, that two paths zero it, and that the open part is what fills `02ADD060`.
4. **N2, wording.** The clamping page's "What the player sees" says the walk "measures a listener-side point against an
   emitter's volume record" and that the player hears the effect "as where a sound seems to come from".
   - The only support is the ledger's filing of `003631B0`, `00361810`, `003638B0` and `00362850` to Audio.
   - `00362850` does read the party-focus handle (the field-runtime pages).
   - The two bodies after the clamp are unread (SD-180). Label the audio reading as the ledger's filing, or as
     inference.

**Note: the register's final newline is back.** `583b096f7` dropped it (`auditsem-review-sd6x-adoption-0930` C2), and
this commit's appended rows end with `\n` again. That correction is discharged.

Routed as `AUDITSEM-REQ-DATA-DD-OWNER-READ-5-ROWS-0930` to SWE2-DATA. The pages and rows are that lane's.
