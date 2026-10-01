# Render accounting byte: two positive upper-nibble producers

## Result

Both published CharacterRenderRecord `+C1` writers derive their value from the
upper nibble of a source byte. The original conditional writes produce 0–15,
not an unconstrained signed byte. They do not establish a shipped 0/1 domain.

This complements the separate accounting-dispatch package: its negative-value
countermodels remain mathematical, but these two supplied writes exclude
negative values on their paths. Neither packet proves all writers, all natural
states or the accounting table's extent. Independent acceptance and OPUS/FABLE
canonical consumption remain pending.

For the player: the game copies a small bookkeeping value from a packed state
byte into the character's render record. We can prove which bits it copies;
which values the game's setup actually supplies is the next question.

## Exact source flow and identity

`002E28E0` loads entry object's `+C0` state into RSI. At `002E29A4` it reads
`BYTE[RSI+10]` with MOVZX into EDX; `002E29B6` shifts EDX right four bits.
The guarded record write at `002E29E9` stores DL at `[RCX+C1]`.

`002E3110` works with a selected state slot in RBX. At `002E3367` it reads
`BYTE[RBX+10]` with MOVZX; `002E3380` shifts EDX right four bits. Its guarded
write at `002E33B3` stores DL at `[RCX+C1]`. The selected slot is not necessarily
the root state, so do not collapse their source objects into one field.

Each destination uses a signed-16 word index from the object's `+C0` state,
stride `740h`, and the global at `022C6F28`. There are NULL, -1, zero-address
and record `+284` guards. Those checks do not prove a nonnegative, in-range
index or correct object initialization. Valid objects/table entries and normal
execution are premises for the semantic store interpretation.

The complete local graphs cover 470 and 247 original instructions. Both source
loads and shifts dominate their respective store. No intervening call or EDX
write changes the loaded value. The actual source/store memory roles and byte
widths, exact table addresses, operations and reference bytes are checked.

For every possible source byte B, `C1=B>>4`, so `0<=C1<=15`. The factory's
subsequent MOVSX byte read is nonnegative for these produced values. It is 0 or
1 exactly when `B & E0h == 0` (equivalently B<=1Fh). Boundary calculations:
1Fh→1, 20h→2, FFh→15. The 256-byte invariant calculation is not 256 native
calls or sampled live states. No source-bit 5–7 exclusion is proved here.

## Evidence and limits

Method A; no game or isolated machine-code execution was needed. Reference EXE
SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New source is the two complete 2,026/997-byte bodies (3,023 bytes), captured
through the shared reviewed access-role adapter. Current identity/terminal/
exit/exception gates precede semantic output. Raw source, normalized result,
driver receipts and consumer field preimage are preserved.

The checked positive producer and four actual CLI refusals cover failed
capture, incomplete wrapper, missing source and a coherent SHR-4→SHR-3
mutation. Those tests validate the producer; they are not native-game tests or
independent project acceptance. No repeated live setup or runtime sampling.

These are two positive writes within the supplied complete bodies. Constructor
clears, bulk copies, aliases, other writers, source-state initialization,
scheduling, actual storage extent and lifetime require separate evidence.
The current field's neutral-copy census remains historical; producer arithmetic
and downstream accounting use justify a qualified owner update after review.

No PC/game/instrument/native harness/save/configuration/reference/peer file or
peer process changed. All own child tools are terminal. EXP127 stays invalid;
the parked menu budget stays spent and unapproved. Full L1+L2 is not complete.
