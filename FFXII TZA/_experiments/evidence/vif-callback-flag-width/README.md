# VIF callback flag: byte write, dword truth test

**A zero flag byte does not ensure a false collected flag through this original
call chain.** This is an isolated-original-code finding, not an observation of
normal FF12 stack contents or a visible rendering effect.

Question and alternatives are in `PLAN.md`. Original static preflight exposed a
width mismatch; method B tested the actual composed ABI and collector memory
result. `source.json` retains exact executable identity, seven shipping bodies,
all decoded instructions, tool identities, consumer preimages and fixture/stubs.
`raw-results.json` retains every executed PC, source/argument/flag access event,
entry-boundary register trace, stub arguments and bounded return checks.
`check.py` derives the normalized observations without running the emulator again.

## Original mechanism

GiVmax slot0 caller001DB550 zeroes ESI at001DB56C and writes only SIL to
`[rsp+20]` at001DB5B9. Its fifth argument goes into wrapper0022C940, whose0022C944
reads **four** bytes at`[rsp+60]`, the same original slot. Wrapper0022C948 forwards
that dword into the decoder's sixth argument;0022C9BB imports it asR13D.
DIRECT/DIRECTHL0022CB27 putR13D inR8D; the callback001DB640 testsR8D at001DB643,
then SETNE R8B at001DB64C. Collector001DB67D extracts that byte intoR14D and
001DB729 stores it into the collected flag list. The three upper original slot
bytes have not been initialized by the caller's one-byte store.

These are physical widths and actual execution results. No source type spelling
or claim about why this convention ships is inferred from them.

## Results and controls

All cases entered original001DB550 with one20-byte backed DIRECT/DIRECTHL packet,
EOP GIF tag, pre-created pointer/flag chunks and supplied gate1. The original caller
reset counts, called the original wrapper/decoder/adapter/collector, and returned.

| supplied slot dword | after original zero-byte store | saved flag |
|---|---|---|
| 00000000 | 00000000 | 0 |
| 00000100 | 00000100 | 1 |
| 00000001 | 00000000 | 0 |
| 80000000 | 80000000 | 1 |

The first case is the retained feasibility/detection control. The low-byte case
proves the caller overwrite; nonzero upper and high-bit cases distinguish a full
dword nonzero test from byte-only or signed-positive interpretation. DIRECTHL
clean/upper cases produce the same0/1 split. Every case executes232 instructions,
preserves checked nonvolatile registers, copies the same16 payload bytes under
the disclosed stub, stores one pointer/one flag and returns within the bound.
Original guest code/source packet remain unchanged. Counts do not stand in for
semantic acceptance; the trace/access/result chain is the evidence.

## Limits and downstream changes

Native packet allocator001A1470 is stubbed to return disposable COPY;00861EBA
memcpy copies the requested guest bytes;0016D6A0 registration only records the
pointer and returns0. Pre-created chunks avoid further allocation. These stubs
do not prove native allocation, ownership or copy effects. They preserve the
specified boundaries for the tested flag chain; supplied object/state is not live
initialization. No rendering replay or screenshot is included.

Consumers should preserve the byte/dword distinction and state the upper-slot
initialization requirement if claiming the byte store determines the bool.
Actual normal upper bytes and any presentation consequence remain unresolved.
No normal false/true rate, game crash, source-level repair or L3 implementation
is claimed. FABLE/OPUS changes and independent SPEC acceptance are pending.

Player version: a rendering flag crosses a hand-off that reads more bytes than
the caller sets. In a small run of the original code, changing only the surrounding
bytes changed the saved flag. We know the mechanical requirement now; we have not
shown that ordinary gameplay uses those surrounding values or changes its picture.

PC stayed off. Only disposable emulator memory was changed; the game, saves,
configuration and reference executable were untouched. No fresh live cleanup
receipt is claimed. Whole L1+L2 database goal and required final audit remain NOT_MET.
