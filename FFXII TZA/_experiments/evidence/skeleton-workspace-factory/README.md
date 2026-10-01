# Skeleton workspace sizing, forwarding and failed-slot boundary

## Question and method

How does the original instance factory supply the skeleton workspace, does its
size formula match the binder, and does a failed record-slot request return
safely? Consumers: OPUS's skeleton/workspace types and contracts, FABLE's
external-source ownership and lifetime page.

Method A is sufficient for the exact arguments, fixed-width calculation and
conditional branch. Fresh live observation cannot strengthen those facts
without separately establishing natural reachability. Actual allocator extent,
resource stability, scheduling and lifetime remain separate obligations.

Competing explanations: the caller could omit the skeleton-copy bytes from its
request or compute a different offset; the forwarding wrapper could alter the
workspace or length; the failed-slot branch could return without accessing a
record. The verified original instructions distinguish these explanations.

## Established source facts

`003712E0` queries the `52544640` section and computes the same offset as the
retained binder `00372820`. Its instruction order is:

1. DWORD header `+C` times `149h`, plus zero-extended WORD `+38`, in 32 bits.
2. `t = low32(2*x+15)`; CDQ uses the sign of this actual result.
3. Add 15 if that sign bit is set, then mask with `FFFFFFF0`, in 32 bits.
4. Add the caller's DWORD length, in 32 bits.

The binder's ADD operands are reversed and its corrected sum uses LEA rather
than ADD. Those operations have the same low-32 result. Equality requires the
same unchanged header at the two queries; opaque calls do not prove stability.

`0041F340` saves that component in EBP, adds its other workspace components,
and sends the low-32 total in ECX with EDX=1 to `003AB8B0`. That adapter selects
`0036B160` and zero-extends its EAX result. Existing allocator documentation
identifies kind 1 as a handle; this package does not re-prove its native effects.
The factory encodes the adapter's returned representation into instance `+2FC`,
decodes it again, and passes it as argument 5 to `0046E4D0`. The wrapper forwards
that representation, source blob and DWORD length to `00372820`.

The factory frame is 120 bytes, putting incoming argument 5 (source blob) at
current RSP+A0 and argument 6 (DWORD length) at RSP+A8. The wrapper frame is 88
bytes: its incoming arguments 5–8 are at RSP+80/88/90/98. These are distinct
call boundaries; the binder's retained 72-byte frame remains unchanged.

For the same header, nonnegative offset O, length L and other components S/Q,
with required arithmetic free of wrap, the first component is E=O+L and the
request is N=E+S+Q. Therefore `[O,O+L)` fits E and N. This is a conditional
request-size proof, not an observation of usable allocation bytes or lifetime.
The allocator request is 32 bits, while the zero-fill total and copy length are
sign-extended from DWORD to 64 bits. High-bit or overflowing inputs are outside
the safety claim. There is no failure-result check before the factory's encode,
resolve/zero-fill and binder sequence; normal opaque-call returns are premises.

If `0051FBB0` returns `FFFFFFFF`, `0046E4D0` skips the binder and returns that
value. `OR EAX,EAX` at `0046E4FC` does not change it. The caller then takes:

`0041F57F compare -1 → 0041F584 XOR ESI,ESI → 0041F586 jump →
0041F595 DWORD read [RSI+4]`.

RSI is zero and there is no intervening call, so the effective read address is
4. This refutes a safe-return interpretation of that conditional path. It does
not establish natural bank exhaustion, successful completion of the preceding
allocation path, an observed crash, or an executed OS fault.

## Additive codec qualification

The frozen parent calls its zero-input encoder result “encoded NULL.” That
means `Encode(0)`; it is not a universal assertion that decoding it gives zero.
For base B:

`Encode(0)=low32(-B_low)` and
`Decode(Encode(0))=low64(B+low32(-B_low))`.

At B=1000h, the encoded value is FFFFF000h and the decoded result is 100000000h.
These are mathematical counterexamples over verified original instructions,
not process samples. Retained base-zero evidence and OPUS's accepted ruling are
not repeated. The parent remains immutable; this qualification is additive.

## Provenance and controls

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New source: four complete bodies, 1,340 bytes. Binder/decoder and encoder/reader
source is retained under the parent manifest and original capture receipts.
The parent was producer-valid and waiting for publication when read; neither a
commit nor independent acceptance is invented for that state.

The actual capture uses the shared reviewed access-role adapter. The producer
checks upstream terminal/exit/exception status, current drivers, EXE hash,
retained manifest membership, annotations, original bytes, complete local CFG,
exact argument/formula operations, dominance and nonvolatile carriers. All
prerequisite gates precede semantic output. The checked positive producer and
four actual CLI refusals cover failed capture, incomplete invocation metadata,
missing source and a coherently annotated mutation of the address-4 read. Those
controls validate the producer, not native FF12 behavior or project acceptance.

No game, native harness, PC-control session, instrument, save, configuration,
reference binary or peer file/process was changed. All child commands are
terminal. Independent review and canonical owner consumption remain required.
Whole OV questions, internal skeleton arrays, resource/header stability,
allocator success/extent, ownership/reuse, cleanup and natural failure remain
open. EXP127 stays invalid; the parked menu allowance stays spent/unapproved.
