# Transition duration: low32 product and signed quotient

Question: is `Widget+0x90` transition duration computed by the same bounded unsigned operation as the deferred `+0x70` timer? The current type description compares the conversions. Source shows a material domain distinction. Consumers: OPUS Widget duration/comparison rows, FABLE transition contract, SPEC independent review.

Method **A** reads the complete 364-byte starter `002468A0..00246A0B` from shipping SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Raw source, instruction listing, reader/tool identities, current field/contract/producer preimages and immutable prior37 manifest/source are retained. **No original-code, emulator, native or live test was run.** Selected host integer calculations illustrate the instruction-defined domain; they are not new observations from the game.

On the selected start path, widget is nonnull, `+0x80` bits1..3 are clear and requested pair differs from the current signed16-expanded pair. `PUSH RBX; SUB RSP,40h` makes local `[rsp+70h]` the entry stack's `[rsp+28h]`, a dword argument. There is exactly one direct access to that slot: `00246971 IMUL ECX,dword[rsp+70h],60`. No duration-range clamp occurs before this load on the selected path. This assumes stable argument/widget storage and normal ABI separation; aliasing or normal caller ranges are not inferred.

The product keeps **low32 bits**. `0024699A IMUL ECX` forms the signed product with `0x10624DD3`; `SAR EDX,6` and `SHR EAX,31; ADD EDX,EAX` implement negative quotient truncation toward zero. The dword bits are stored at `+0x90`. Thus neither unsigned storage width nor the phrase “milliseconds to frames” makes this equivalent to an unbounded or unsigned multiplication/division.

| Conditional source-calculated milliseconds | Low32 product bits | Signed frame result |
|---:|---|---:|
| 1000 ordinary control | `0000EA60` | 60 |
| 17 positive control | `000003FC` | 1 |
| −17 | `FFFFFC04` | −1 (`FFFFFFFF` stored), versus mathematical floor −2 |
| 35,791,394 | `7FFFFFF8` | 2,147,483 |
| 35,791,395 | `80000034` | −2,147,483, versus unbounded positive quotient 2,147,483 |

A labelled private source/model intervention changes signed `IMUL` to unsigned `MUL`, retaining the subsequent arithmetic shift/sign correction. The selected negative case changes result and the original source-binding predicate rejects the bytes. No altered code ran. Positive control plus negative truncation and first positive product-sign overflow distinguish the competing arithmetic interpretations without a sweep or expensive setup.

Prior37's `+0x70` writer instead uses unsigned `MUL`/logical shift and selected u16/ten-bit durations. Its nonnegative bounded domain guarantees a product ≤3,932,100. “Same conversion” is valid only with a suitable shared nonnegative/nonoverflow domain; that prior selection, exact floor proof and limits remain unchanged. This package concerns only starter `002468A0`; other starters need their own source reads before family-wide extrapolation.

Required consumer change: preserve low32 multiply, signed reciprocal and truncation semantics, and qualify the comparison with the bounded deferred timer. A source-level type/sign declaration is not inferred solely from storage width or these operations. Original caller constraints may make the exceptional inputs unreachable; they remain unproved here. No field-wide value range, actual long/negative UI delay, clock/cadence, callback effects, visible transition or malformed-input safety is established. Later callbacks/cookie checks are retained source but not executed or certified by this arithmetic result.

`check.py` binds original operands/branches/argument width and validates each retained integer stage; it does not rerun the starter. Consumer incorporation and independent acceptance remain pending. Cleanup is read-only source/peer preimages and disposable host calculations; PC/game/save/configuration untouched. S19 remains parked with spent allowance/unapproved extension. Full L1+L2 is NOT_MET.

Learned precondition: don't transfer the u16/ten-bit bounds from the deferred writer to this dword argument. Don't repeat these cases after the width/signedness question is settled; the next discriminator concerns an actual caller domain or a different starter, with ownership checked first.
