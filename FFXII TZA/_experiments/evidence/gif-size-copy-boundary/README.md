# Original GIF size helper / collector qualification

The existing GIF tag-size formulas are correct. What needs qualification is the
**width of their accumulated result** and the conditions for treating that result
as a buffer extent. Method A suffices; no FF12, emulator or native harness ran.

## Primary evidence and observations

`primary.json` retains verified shipping executable identity, exact PE RuntimeFunction
entries, 197 bytes at 0020F310 and 358 at 001DB660, full decoded instructions and the
current semantic consumer preimage. `check.py` reduces those bytes and rejects
disassembly/width changes; `observation.json` retains normalized conclusions.

Enabled helper reads an eight-byte header at 0020F350. It derives the already-known
GIF formulas with NREG0 becoming16. Each tag's step fits32 bits (maximum8,388,368).
0020F3B8 adds EDX to R10D: accumulated total wraps modulo2^32. For a nonfinal tag,
0020F3C0 zeroextends EDX into RAX and 0020F3C2 adds that individual step to the64-bit
R9 pointer. Total wrap therefore does not wrap the header cursor to the buffer start.
EOP terminates after including the final size; it does not read that final payload.
Gate01E027C0=0 returns16 without a packet read. There is no supplied buffer length
or total-overflow guard in this helper.

The collector calls the helper at001DB687. It passes EAX via EDX to001A1470 and
saves it in EBX;001DB69C puts EBX into R8D for00861EBA (the existing memcpy site).
Both are zeroextended arguments, with no size/overflow check between measurement
and copying. The downstream callees are not executed or independently requalified.

## Discriminators and limits

Small mathematical witnesses preserve PACKED, odd REGLIST and IMAGE branches.
257 maximum PACKED tags give0x807F0F10: high signed bit set, but caller forwarding
still zeroextends. 513 give0x1007E1F10 declared bytes with return0x7E1F10.
512 maximum nonfinal PACKED tags plus final IMAGE NLOOP7679 yield exactly2^32
declared bytes and a zero return. These are **symbolic declared layouts**, never
allocated or executed; they do not prove that any shipped resource contains them.
They do not imply that the helper reads every payload byte or a zero return faults.

For enabled return to represent the complete copied extent, producers/callers must
provide an EOP-terminated readable header sequence, a sufficient backing source
extent and total below2^32, with valid address arithmetic. Local measurement does
not prove those preconditions. No universal game vulnerability or actual crash is
asserted. Ordinary reachability, gate initialization, producer bounds and downstream
effects remain unresolved. Static controls are not original-code execution or an
independent semantic review.

Affected consumers: FABLE's legacy VIF/GIF §2.1a, OPUS helper ABI/length/precondition
descriptions. Owner edits and independent review are pending; no peer file changed.
No types or contracts are invented merely to count coverage.

Player version: the renderer follows graphics-packet headers until an end marker.
Its copy-size counter is32 bits even though its addresses are64 bits. Mods producing
these packets must keep the complete size within that counter and provide readable
data. This finding does not show a faulty packet in the original game.

Cleanup: PC control remained off; only original-file reads and local artifacts.
No game/save/config/reference writes, instruments or fresh restoration receipt.
Full L1+L2 database goal and required final audit remain NOT_MET.
