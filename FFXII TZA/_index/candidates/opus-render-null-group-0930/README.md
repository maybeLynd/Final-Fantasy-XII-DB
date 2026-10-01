# The payload reset's null-group call is not reached: bit 0x1000 is set only after a real group id is stored (OPUS, 2026-09-30)

DD prose residue on [render event selection evidence](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md)
section 10. That section showed a hazard in `0041CF00`, the reset of a render payload: when flag `+0xC` bit `0x1000` is
set and the payload's group id `+0x338` is -1, it skips the group lookup and calls `00372280` with a zero `rcx`, and
`00372280` dereferences it at once. The section ended *"Valid construction/flag writers and native caller reachability
remain to be established."* This record establishes both.

Static, the certified image. The checker is [`null_group_check.py`](null_group_check.py) (output
[`null_group_check.out`](null_group_check.out), **`FAILS 0`**).

## The answer (OPUS)

| step | what the image shows | check |
|---|---|---|
| the hazard | `0041CF00` zeroes `rcx` at `0041CF09`. Only the `+0x338 != -1` branch (`0041CF98`-`0041CFA4`) and the tail-call argument write it after that, so bit `0x1000` with `+0x338 == -1` calls `00372280(0)`. `00372280`'s first access is `mov ecx, [rcx+0x84]` (`0037228D`), with no test before it | N1, N2 |
| who sets the bit | image-wide, the only OR that sets bit `0x1000` of a dword at `+0xC` is `0041D4D0`'s (`0041D4D9`), and its only caller is `00424550`. The other immediate `mov`s carrying the bit are -1 or float constants. `0051F202` is the container node's own field, and none of the other functions calls the payload getter `0051B9E0` | N3 |
| what precedes it | `00424550` calls `0041D4D0(payload, 1)` (`004247FA`) right after the admission `0051BA80` (`004247AD`). That admission's definition `+0x14` is `[rdi+0x18]` (`00424722`), and this whole path runs only when `[rdi+0x18] != -1` (`00424653`) | N4 |
| the group id | the admission's builder `0041D220` stores definition `+0x14` into `+0x338` (`0041D270`). The only -1 store, the reset `0041CB90`, runs before `0041D220` inside the admission, or at `0041CF00`'s tail after the bit has been cleared (`0041CFAC`) | N5 |

So a payload has bit `0x1000` only after `00424550` has stored a group id that is not -1. `0041CF00` therefore always takes
the lookup branch, and the zero-`rcx` call is not reached by any shipped writer of the bit.

**In player terms:** a crash path in the character-render reset is dead code. It would need a character render record
flagged as "has per-bone state" with no model group, and the only code that sets that flag sets it right after binding a
real model group.

## Owner re-status of the page (OPUS)

With this sentence answered, the page's other prose residue is stale, and each instance gets a dated pointer in place:
- §4's "other resource/native effects are not established" is answered by UQ-194's census of both callers.
- §7's "native cleanup effects are not read" is answered by §9 (`0041CB90`) and §10 (`00372280`, a per-bone reset with
  no release).
- §8's "initialization semantics remain open" is answered by §9.
- §9's "native ownership and scheduling remain open" is answered by UQ-193 and UQ-194.
- The falsification pass's "remain unread" was true at the time of that pass.

The status line names UQ-192's disposition word, NOT A QUESTION (condition P). The page moves **PARTIAL → DOCUMENTED**:
`documented_rule.py` gives READY-WITH-POINTER 1 of 1 ([`documented_rule.out`](documented_rule.out)).

**A-drift, paired:** the re-status makes `00417530` A (NativeDispatch.GlobalHandlerSlotTailCall, 25 declared, via
`@00417546`). The report is `Tools/work/OPUS/adrift-report-0930-rend-after.out`, and it is routed to SWE2-EC7.

## Limits (OPUS)

- **N3 is a census of immediate stores.** A register store to a payload's `+0xC` is not enumerated. The admission copies
  the whole `0x3A0` template over the node, and that template's `+0xC` comes from `0041CB90`, which zeroes it, and from
  `0041D220`'s OR of `0x00100001`. Neither of those sets bit `0x1000`.
- **Other `+0x338` stores in the image** belong to objects not shown to be payloads: `003D9040` writes 0, `0026F470`
  writes a record whose `+0x368` is a word (a payload's `+0x368` is a pointer), and `003B2F50` writes through a
  `0x28`-stride global table. None calls the payload getter.
- Static only. Nothing is executed.

## Consumers (OPUS)

- **consumer:** the render-event evidence page, section 10's last sentence: answered in place with a dated note, and the page
  re-statused (this publish).
- **consumer:** SWE2-CONTRACT / SWE2-STRUCT's DD batch 12 brief (`Tools/work/OPUS/lane_brief_dd_b12.md`): the page is
  done here and removed from that batch.

## Review (OPUS)

Reviewed by SWE2-AUDIT-SPEC (request filed at publish).
