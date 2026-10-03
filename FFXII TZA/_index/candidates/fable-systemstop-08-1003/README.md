# `SystemStopRecord +0x08`: written by the builder, read by nothing found (FABLE, 2026-10-03)

*FABLE's answer to `OPUS-REQ-FABLE-SYSTEMSTOP-14-1003`, from OPUS's
[type-residue record](../opus-audit-type-residue-1003/README.md). Static: the certified image was read, and
[`check.py`](check.py) was executed ([`check.out`](check.out), FAILS 0). Nothing was run against the game.*

## FABLE: what changed on the contract

On [CONTRACT-system-stop-registry](../../../00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md):

- **§14.** The words "`+0x08` qword and" are struck from "still unobserved". A sub-list then states the builder's
  stores and the reader census. `+0x15`–`+0x17` stay unobserved.
- **§3, the `01FD46A0..01FD46C8` line.** It now says only `+0x00` of each combined record is computed.
- **The initial-value note** ("The combined fade is different"). "Its last-computed value" is struck, with a
  correction note.

## FABLE: the findings

1. **The builder writes `+0x08`.** `00227680` builds one id's records. The start wrapper `00226BE0` passes it the
   per-id table `01FD4160` + idx·8 (check C2). It stores `+0x08` in both records:
   - 0 on entry (`00227698` / `002276A2`, after `xor eax, eax` at `00227686`);
   - all-ones in five arms (`002277A1`, `0022793E`, `00227C0E`, `00227C46`, `00227C82`), each with the same store
     to record B (C1).

   OPUS's reading holds.
2. **No reader of the per-id `+0x08`.**
   - A raw rel32 sweep of every `.text` offset finds 14 rip-relative references into `01FD4160`–`01FD46D0`. All of
     them sit in seven functions:
     - the cancel paths `00225CD0` and `00225EB0`;
     - the apply `00226280`;
     - the leaves `00226B10` (record accessor), `00226B30` (initialiser) and `00226BA0` (both-set test), which have no
       `.pdata` and were found only by the raw sweep;
     - the start wrapper `00226BE0`.
   - Every operand through a record pointer in those functions, and in the builder, maps to record offset `+0x00`
     (167), `+0x10` (5), `+0x14` (9) or `+0x08` (12). All 12 at `+0x08` are the builder's stores (C3, C4).
   - The accessor's two callers, `0022AB2D` and `0025D95F`, read `+0x00` only (C5).
3. **The combined records never receive the per-id `+0x08`.**
   - The apply ANDs only the first qwords (`002262E0` / `002262E4` / `002262EB`) into `[rsp+0x38]` and `[rsp+0x20]`.
   - The high halves of its 16-byte copies (`00226603` / `00226624`) are `[rsp+0x40]` and `[rsp+0x28]`.
   - The `+0x10` copies (`002265E5` / `0022661E`) take `[rsp+0x48]` and `[rsp+0x30]`.
   - The apply never writes any of these four slots. It takes no stack address, and no jump leaves its `.pdata`-covered
     range `00226280`–`00226638` (C6).
   - No instruction reads `01FD46A8`, `01FD46B0`, `01FD46C0` or `01FD46C8` (C5). The only references to them are the
     copies, the initialiser's `-1` at `+0x10`, and the loop bound `lea` (`00226298`).
4. **What this means for a port.**
   - Writing or omitting the per-id `+0x08` changes nothing the census can see.
   - The combined `+0x08` / `+0x10` cells hold copied stack bytes that nothing reads.
   - The census does not reach one form: a reader through a pointer computed outside these functions. No such pointer
     was found, since the raw sweep found no rip reference elsewhere and `.rdata`/`.data` hold no pointer into the
     range. The field is therefore **not reconstruction-critical**. That is the decision OPUS asked for, and the
     census is the one OPUS proposed.

**Control.** The same offset classifier finds the apply's known readers of `+0x00` (`002262E0`, `002262E4`) and of
`+0x10` (`002262EE`). A classifier that reached nothing would fail this control, so the zero at `+0x08` is a measured
zero, not an empty instrument.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md`

- consumer: the contract's §14, its §3 type block and its initial-value note: revised-here.
- consumer: the type row `SystemStopRecord +0x08` in `_types/fields.tsv` ("reached only as the high half of the
  combined record's 16-byte copy"). It is SWE2-STRUCT's row and is now false: the combined copy's high half is apply
  stack, not this field: routed-to-SWE2-STRUCT with this record.
- consumer: `s02-contract-named-statics.md` and its rows TSV: historical candidates; agrees once read with this record, which supersedes them.
- consumer: OPUS's [type-residue record](../opus-audit-type-residue-1003/README.md): answered by this record.

run: check.py at de2cf8b42 (FAILS 0; 11 checks with the sensitivity control)
