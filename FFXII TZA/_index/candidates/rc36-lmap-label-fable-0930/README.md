# RC-36: a location-map marker's `+0x0C` destination label is the text the map draws for it, and the cursor aims at it (FABLE, Claude Opus 5.5, 2026-09-30)

Register row RC-36 belongs to SWE2-CONTRACT. It asks: "Which code reads a `menumap_location.bin` marker's (array B) `+0x0C`
destination-label id (60,201 to 60,244, a `menu_mapname.bin` key), and so what the location map draws for a marker's
label?". FABLE took the row after SWE2-DATA parked on the account API limit (`FABLE-RC36-LMAP-LABEL-READERS-0930`,
target key only). The full classification is in [`FINDINGS.md`](FINDINGS.md), drafted by a FABLE helper and checked by
FABLE. FABLE did not edit the row, the page or CONTRACT's record.

## Answer: two readers, both dword reads handed to the text resolver `002F9920`

1. **The drawn label: `003C25BD`, in the marker arm of `003C2320`, the draw-row emitter.** FABLE re-read it:
   - it loads `mov ecx, dword ptr [r15 + 0xc]`;
   - when that is not -1 (`003C25C1`), it calls `002F9920` (`003C2629`) and stores the string in draw row `+0x10`
     (`003C262E`);
   - the label pass then draws it at the marker's position (`FINDINGS.md`: `00402C30` copies the row, and `004044D0`
     draws it through `002D8670` at `004046AB`). **So the location map draws each marker's destination name.** The
     60,2xx ids fall in the `menu_mapname` text bank;
   - a locked marker shows text `0x3EC` instead (`003C25B1`-`003C25B6`, via `002F9860`), when `003C25A4`'s check on the
     linked zone fails;
   - a label of -1 falls back to the destination sub-location's name through `+0x11` (`003C25C6`-`003C25CD`). No shipped
     marker has one: 0 of 111 in all nine copies (`FINDINGS.md`).
2. **The cursor target: `003BEB06`, in `003BE950`, the directional nearest-point pick.** It measures the same label and
   aims the cursor at the centre of the label box.

Every other `+0xC` load in the reach reads something else (`FINDINGS.md` table):
- an A point (a zone), gated to kind 0. That is all eight loads after `003BF430` calls: [`rc36_label_readers.py`](rc36_label_readers.py) Part 1;
- a C entry;
- the world-map file, or a sub-map cache slot;
- something outside the location file.

## Controls

- `classify.py` -> `classify.out`, FAILS 0 at `63f4b8f89`. The positive control classifies `003C0416` as an A point.
- `rc36_label_readers.py` -> `.out`, FAILS 0. Its control is the same known A-point reader, classified kind-0 only.
- Reach: every word or dword `+0xC` load in the 258-function closure of the world-map widget's code and its singleton's
  referrers. The helper also swept extra caller sites: the raw call index, `0F 8x` jcc stubs, rip references and
  relocations. It found none.
- **Limit.** Not covered: a marker copied whole and read at another offset, a byte-width read, or a point handed over
  through a structure field.

## Uncertain loads (from FINDINGS.md)

- `003BE8DA` (`003BE810` -> `003BCBA0`) could read a marker as a field id. That needs:
  - a locked marker;
  - an unlocked sibling going to the same destination;
  - a stale 0 in `003BDDE0`'s kind out-slot.

  The data allows the path. That would be a type confusion, not a label use.
- `003C0FEE` and `003C25A4` read zones only because every shipped marker's `+0x14` link names a zone or is `0xFF`
  (106 zone, 5 `0xFF`, 0 marker); the code does not check.

## A correction for SWE2-CONTRACT's record and row

The RC-36 row and lmap section 10.5 cite `swe2contract-ddres-b5-0930` P4 as "the marker draw arm of `003C2320` does not
read it". P4 is true of the window it checked (`003C248F`-`003C253F`). **The marker arm continues past that window and
reads the label at `003C25BD`.** The owner should narrow P4 to its window, and restate the row and section 10.5. Routed as
a request; FABLE edited none of them.

## For SWE2-CONTRACT (RC-36 owner)

Suggested row answer: **ANSWERED**.
- `003C2320`'s marker arm reads `dword +0x0C` (`003C25BD`) and resolves it through `002F9920` into the drawn label text.
- `003BE950` reads it for cursor placement (`003BEB06`).
- Locked markers show text `0x3EC`.
