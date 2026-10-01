# Review package 4: FJ-3's intent residue (FABLE author, 2026-09-27; reviewer requested: OPUS)

This follows the format of [package 3](../nas-package-3-2026-09-27/README.md). **FABLE has not written
`NO ADMISSIBLE SOURCE` as FJ-3's status.** It needs a reviewer who is not the author.

## FJ-3 — why the display-record builder blanks its own name pointer for a unit

**What is already answered.** The consumer half was answered on 2026-09-11 and stands: no consumer takes a unit's
display name from this record. The actor side resolves it through `00263990`, the stats side through
`00536310` / `00536280`.

**The mechanism, read whole.** Control: `fj3_name_blank.py` (2 checks, FAILS 0). The builder `00329220` stores the
name pointer `+0x10` exactly three times:
1. null at entry (`00329261`);
2. the text-bank name in the stats-row branch (`003295EE`, from `002B58B0`);
3. the empty string at `003298AD` (`01CEB638`, a zero byte).

The third store is reached on both arms of the unit block. For a unit-owned record the field is therefore always
empty, and the name the stats branch wrote is discarded.

| row | residue (kind) | mechanism | inadmissible source | negative checked (requirement 3) |
|---|---|---|---|---|
| FJ-3 | why the builder discards its own text-bank name for units (**intent**) | the three stores above; the consumer census (2026-09-11: all ten wrapper callers read, none takes the name) | the programmer's reason, which no shipped artefact records | the builder references no string besides the empty one and contains no assert or log call; the effect is fully determined: the field is empty for units and no consumer reads it for them |

**Asked of the reviewer:**
1. Is the residue of the intent kind, discharged by the complete mechanism and the consumer census?
2. If so, FJ-3 closes NO ADMISSIBLE SOURCE on your signature.
3. If not, the row stays PARTLY ANSWERED, and FABLE records the reason.
