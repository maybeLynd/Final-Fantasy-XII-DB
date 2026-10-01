# S-41 runtime: per-invariant stub exposure for EXP-096 / EXP-105 (OPUS, 2026-09-25, block 299)

**Row:** S-41, sound request to voice. The runtime cell is MIXED with the qualifier "no per-invariant stub-exposure
analysis yet". The binding gap reads "types PARTIAL … and nothing executed". This note scores nothing.

**S-41 has three contracts, and both named records cover only one of them.**
- `18-Audio/Audio-Boundary/CONTRACT-sound-request.md`: EXP-096 and EXP-105.
- `18-Audio/CONTRACT-spatial-source-objects.md`: its §13 says **"None. No experiment executes these bodies."**
- `18-Audio/Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md`: its §13 says the same.

## Substitutions per record

| record | real | substituted |
|---|---|---|
| **EXP-096** request path | the verb `00357040`, the VM pop `00267E10` / push `0026B4E0`, wrappers `00249C60` / `00249CA0` / `00271500` / `0024A1A0`, resolvers `003A1180` / `003A11F0` / `003A1070` / `003A1100`, the liveness / mute predicates `00267330` / `00267310`, the play call `002DF220`, the gate reader `003603C0`, the reshape tail `002DF0F0` | the dispatchers `001DBDB0` and `001DBE90` are scripted **at entry**, with their entry arguments logged (the contract's central observable). The **readiness test `002DEE80`** is scripted, and so is the VM-pop type>2 error path `008620C0` |
| **EXP-105** fork and dispatch | fork `00210C00`, SEB dispatch `0021B5B0`, SEP dispatch `00219EA0`, the receipt counter `00212950`, both voice workers (`00224540` / `00224570`, `00223160` / `00223190`), the grow path, lock / unlock, the cookie check | the mixer-wait fences `005CC930` / `005CCB80`; the shared_ptr / refcount carriers `007A6DB0` …; the `0x7a*` PAN / VOL tail carriers; the bus-attach arms `00221940` / `00221C70` (a separate contract's subject); the STL pool bookkeeping `0016D6D0` / `0016DA60` / `00199DB0`. The worker vtail and the list-allocator function pointers are planted |

## Per invariant (`CONTRACT-sound-request.md` §4)

| inv. | executed by | can a substitution reach it? |
|---|---|---|
| **1** a receipt does not mean a sound is playing | EXP-105: the receipt counter and both bank dispatches, including the match rules, are real | **no**. Whether a voice then plays is below the carriers and fences, and invariant 1 claims only the receipt / no-match independence |
| **2** several independent refusers, none reporting which | EXP-096: gate, liveness and mute are real. EXP-105: bank no-match is real | **partly.** The **readiness-test refusal (`002DEE80`) is scripted in EXP-096**, so that refuser's own behaviour is not executed; it is **application-stub exposure** on invariant 2 |
| **3** wrappers pass `0x40` / `0x7F`; the verb passes script pan and volume | EXP-096: wrappers and verb real, dispatch arguments logged | **no** |
| **4** a bank owns a 512-entry id block | EXP-105: SEB bucketing `sar((id + (id<0 ? 0x1FF : 0)), 9)` real | **no** |
| **5** the gate protects three functions, not the path | EXP-096: the gate reader and the play call are real | **no** |
| postcondition: the request carries pan / volume; a receipt returns | EXP-096 (logged dispatch arguments) + EXP-105 (fork masking `vol &= 0x7F`, `pan` zero-extended) | **no**. The contract itself (corrected 2026-09-21) confines the claim to the request record; voice initialisation is live-only by its own statement |

## For the scorer

- **One application-stub exposure:** invariant 2's readiness-test refuser `002DEE80`, scripted in EXP-096.
- The other invariants and the postcondition run on shipped code.
- **Two of S-41's three contracts have no execution record at all.** That is coverage, not exposure; their §13 says so.
- **Stale text:** the binding gap says "types PARTIAL … nothing executed", but the types cell is MET and EXP-096 / 105
  execute the request contract.
- `live_game` is false.
