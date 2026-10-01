# Widget deferred-delay selection: record or packed override

Question: is this start arm's `Widget+0x70` delay always selected from the record's u16 milliseconds, with a completed `00181C90` return of 1 forcing zero? Or is that choice superseded by a packed override? Consumers: OPUS's `timedFrames70`/`field7C` rows, FABLE's deferred-completion contract row, SPEC independent review. The published child-header migration is not repeated.

Method **A** binds the original 67 bytes at `00244E9C..00244EDE` (end exclusive `00244EDF`) to shipping executable SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Raw code, instruction list, reader/tool identity and current consumer/producer preimages are retained. No original-code, native, emulator or live FF12 execution was performed. Calculated cases and exact rational proof are source-backed reasoning, not native observations.

The original sequence is:

1. `00244E9C` zero-extends `word[record+2]` to EDI.
2. After the completed call at `00244EA0`, `CMP EAX,1` supplies flags for `CMOVE EDI,ECX`, with ECX zero. The intervening `MOV EAX,[widget+0x7C]` preserves those comparison flags.
3. `BT EAX,11`/`JAE 00244EC2` chooses the override. When set, the writer copies those flags to EDI, clears bit 11 with `BTR`, stores that result back to `+0x7C`, then shifts EDI right by 22. The selected duration is therefore **bits 22..31**, a ten-bit value. This selection occurs **after** the return-1 zero gate.
4. Selected duration is multiplied by 60, then unsigned `MUL` by `0x10624DD3`, high product shifted by 6: `frames = (ms*60*0x10624DD3) >> 38`. It is stored to `+0x70`. The following local lower-state update is also retained; this slice does not certify the eventual whole-function flag state.

| Source-calculated case | Selected duration | Frames |
|---|---:|---:|
| Ordinary record 1000, return !=1, no override | 1000 | 60 |
| Record 16 / 17, return !=1, no override | 16 / 17 | 0 / 1 |
| Maximum u16 record, no override | 65535 | 3932 |
| Return 1, no override | 0 | 0 |
| Return 1, bit11 set with payload17 | 17 | 1 |
| Return 1, high payload17 but bit11 clear | 0 | 0 |
| Maximum ten-bit override | 1023 | 61 |
| Bit11 set, payload zero | 0 | 0; bit11 still consumed at this store |

The reciprocal equals `ceil(2^38/1000)`. Its positive error at the maximum product `65535*60 = 3932100` is less than `1/50`; possible noninteger quotient fractions lie on a `1/50` grid because the product is a multiple of 60. It therefore cannot cross the next integer, and equals `floor(ms*60/1000)` throughout this selected domain. This proof avoids both a needless enumeration and a misleading arbitrary-u32 overflow experiment. The input's 16-bit/10-bit source bounds rule out that proposed overflow before execution. A labelled private source/model change `SHR 22→21` produces 2047/122 from all-one flags and is rejected by the original source-binding predicate. No altered game code ran.

Established: the return-1 zero choice is not final when bit11 is set; the packed delay payload is selected afterward. Bit11 is consumed by this specific writer, including a zero payload. Start-arm frames range to 3932 on the record route, or 61 on the override route. The source's packed domain and consumed flag should be carried into `field7C` and the deferred-delay contract, rather than describing `+0x70` solely as a record-u16 conversion.

Limits: assume the call completes with the stated return and preserves the caller's nonvolatile EDI under the ABI, with readable/stable record/widget state. Retained `00181C90` context calls `001EBA40` and reads returned object `+0x280`; it was not executed, and its actual mode/configuration meaning or native initialization is not certified here. This is **not a field-wide value range**: other writers reset/subtract `+0x70`. No whole widget, actual caller, scheduling cadence, visible animation/delay, clock interpretation beyond the source conversion, general flag lifetime or later state effects are proved. Source selection/bit consumption and live UI behavior remain distinct.

Required consumer change: record both duration sources and their selection order, bit11 consumption at this writer, and the bounded start-arm conversion domain. Preserve the published header/layout correction. Independent review must accept/narrow/reject the exact conditional source result. No general observer, alternate disposition system or new timer platform is needed.

Cleanup: read-only reference and peer preimages; disposable host calculations, PC control off, no FF12/save/config/process changes. S19 spent setup allowance and unapproved extension persist. Full L1+L2 is NOT_MET.

Learned preconditions: the failed overflow hypothesis must not be retried with arbitrary 32-bit inputs at this entry. All-output matrix sum order was likewise already established in the earlier postmultiply package and was not retested. Read PLAN before a retry; later work must name a different unresolved caller/state question.
