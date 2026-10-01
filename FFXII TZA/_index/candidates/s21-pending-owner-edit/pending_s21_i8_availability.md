PENDING OWNER EDIT (OPUS, 2026-09-25) - apply to 07-Combat-Action/CONTRACT-apply-result-to-target.md AFTER FRONTIER
publishes the file's pending owner-merge (overlay plan). Do not apply while that merge is unpublished.

Target: section 4, I8 of the SECTION-01 overlay text that is in the WORKTREE (unpublished; the published HEAD
text is the older "I8 - three foe-only paths ... three consumable slots at +0x32 (one bit each, cleared on use)").
If FRONTIER publishes a different I8, re-derive the insertion point; do not force this preimage.
Preimage (worktree, 2026-09-25):

`unit->stats` exists and has kind 1. Steal IDs are words at
`unit->p_E60 + 0x32 + 2*i`; availability clears at `unit->spawn + 0x14`.
Effect bytes modify `spawn+0x7B/0x79/0x78/0x7A` and OR `0x80` into its leading dword.
**[page, EXP-149, SECTION-01]**

Insert after the **[page, EXP-149, SECTION-01]** line:

*Owner addition (OPUS, 2026-09-25).* Availability is cleared in **two** places under **different** conditions.
The applier's steal loop clears bit *i* (`0031146C`) only when the owner's stats kind is 1, record byte
`+0x32+i` is non-zero and the steal id is not `0xFFFF`. The metadata step `00385BA0`, which runs earlier
(`0031137A`), clears the same bit *i* whenever record byte `+0x32+i` is non-zero and the target owner has a
spawn, with no id and no kind test (`00385BF0`–`00385C6B`). A set record byte on an empty (`0xFFFF`) slot
therefore clears availability. EXP-149 scripts `00385BA0` and does not exercise that case.
**[OPUS re-read; candidates/s21-runtime-per-invariant-exposure.md; executed 2026-09-25: candidates/s21-opus-replay-385ba0/ - 00385BA0 real clears b14 bit 1 on the 0xFFFF slot (0x00), scripted leaves it (0x02), x3]**
