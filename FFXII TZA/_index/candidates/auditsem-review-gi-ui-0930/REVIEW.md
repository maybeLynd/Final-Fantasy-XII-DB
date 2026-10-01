# SWE2-AUDIT-SEM review — GI-1, GI-3, GI-5, GI-6 UI screen answers and the fifteen page corrections (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GI-UI` |
| reviewed | `4e32dd8df` (author **FABLE**) — [`gi-0929-ui/consumer-check.md`](../gi-0929-ui/consumer-check.md) and its four scripts |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT**, scoped: GI-6's table is re-derived (shared with GI-4); GI-3's message-285 traffic and one GI-5 typing are spot-checked; GI-1 and the rest of GI-5 are accepted on the producer's re-run checks. One limit is recorded for GI-5 (§2). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`gi1_tabstrip_marker.py`, `gi3_dialog_reply_and_wheel_layers.py`, `gi5_shop_panel_e4.py`, `gi6_handbook_category.py`: exit 0,
`FAILS 0`, outputs identical to the committed ones ([`producer_rerun.out`](producer_rerun.out)).

## 2. Independent checks (SWE2-AUDIT-SEM)

- **GI-6.** The handbook category keys 4 Traveler's Tips, 5 Bestiary, 6 Hunts, 7 Sky Pirate's Den come from the same
  `00D23688` records re-derived for GI-4 ([`gi_dlg_own.out`](gi_dlg_own.out), D1): menu row 0 carries key 6 (Hunts).
- **GI-3, message 285** ([`gi3_own.py`](gi3_own.py), [out](gi3_own.out)). Every `…, 0x11D` immediate image-wide sits in
  12 functions. Three **post** it as a message word on the stack (`002C2899`, `002CE103`, `002CE417`); the license
  board and its chooser **compare** it (`00558598 cmp ecx, 0x11D`, `0055CD53 cmp eax, 0x11D`). That is the shape of a
  reply posted by shared boxes and consumed by an opener, as the answer says; which box each poster is was not re-read.
- **GI-1.** The create record's `+0x14` read the checks name is `00566F4E mov eax, dword [rdi + 0x14]`, in `00566EE0`,
  a separate body from the marker procedure `00566C10` (720 bytes; its calls are `00242B90`, `00248F40`, `002CC8D0`,
  `002DD7E0`) ([`gi1_own.out`](gi1_own.out)). The sine-alpha and picker-kind readings (`0x22`/`0x23`) were not rebuilt.
- **GI-5, the "17 panel writes in five functions".** The producer's own sweep lists 251 `+0xE4` writes image-wide and
  types 17 as the trade panel's. The strongest counterexample is the "other shop-region" writes that set bits inside the
  row-variant field (bits 14–21: `0x20000`, `0x40000`, `0x100000`, `0x4000`). Spot-read `005641F0`: its writes go through
  `rax = [owner + 0xD8]` (`00564237`), a child list reached from the owner, with the list-flag pattern (`4`,
  `0x20000`, `0x40000`) — not the trade panel. The other 30-odd "other" writes were not typed here. **Limit:** the
  17-writer completeness rests on the producer's typing of those writes.

## 3. Not re-derived here (SWE2-AUDIT-SEM)

GI-1 corrections 1, 2, 4, 5 (picker sides, list-move keys, tree direction, tab-strip container); GI-3 corrections 8–11
(the chooser, its draw children, arms, the face rows); GI-5's kind tables and Buy / Sell / Bazaar sets.
