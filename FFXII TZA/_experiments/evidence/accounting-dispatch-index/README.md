# Resource tag dispatch does not bound the accounting index

## Result and scope

Method A answers one exact question: does `003AB910`'s boolean dispatch bound
the accounting new index to 0/1? It does not. That boolean selects a helper for
the storage representation. EDX carries a separate parameter unchanged.

The current allocator page's `OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY` section cites
this dispatch in its range argument. Preserve the accepted history. This
package refutes that inference; it does not establish a larger array or reject
an extent/domain conclusion supported by independent evidence. OPUS/FABLE must
supply the actual caller-domain/storage proof or qualify the affected claim.

For the player: the game is choosing which kind of memory record to update.
That choice does not automatically restrict the separate bookkeeping value it
passes along. This is an original-code analysis, not a live memory experiment.

## Original parameter flow

`003AB910` constructs R8D=0 for RCX=0 or an untagged representation, R8D=1
otherwise, and tail-jumps to `0036C620` or `0036C5D0`. It never writes EDX.

The first instruction of `0036C5D0` is `MOVSXD R8,EDX`. It replaces the boolean
with the signed-32 new index. Once its handle/record guards pass, it compares
the current byte index at record `+17` with R8D. If they differ, it debits the
DWORD at `022D8E10 + oldByte*4`, credits the DWORD at
`022D8E10 + signed32(newIndex)*4`, stores the low byte of the new index at `+17`,
and clears WORD `+3E`. The complete body has no new-index 0/1 guard or clamp.

`0036C620` replaces R8 with `payload-40h`, then compares the old byte with EDX.
Its credit address uses `MOVSXD RAX,EDX`. It likewise stores DL at `+17` and
clears WORD `+3E`, without a 0/1 bound. Valid headers/records, normal execution
and no interference are explicit premises.

The retained factory `0041F340` reads CharacterRenderRecord `+C1` with
`MOVSX EBX,BYTE[...]`, then forwards EBX through EDX to `003AB910`. The byte
representation permits -128..127; it does not prove the actual initialized
values. This is a concrete consumer of `paramByteC1` beyond neutral copying.
Its two published writers and their caller domains remain separate evidence.

Conditional examples with old index 1 and amount 32: new index -1 credits
`022D8E0C`, while new index 2 credits `022D8E18`. These are source calculations
over admitted hypothetical states. They are not observed writes, naturally
reachable bad states, an executed fault or a proof of either array extent.
The 256 signed-byte cases are exhaustive representation calculations, not
native calls. Only two represented values are 0/1; shipped-domain proof is
still required before treating that fact as a gameplay consequence.

## Provenance and controls

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New source is the complete 45/79/57-byte bodies (181 bytes). The factory source
is retained under commit `1fccf591e98a2975cc358a619fbb47a047cbb25a` and its
manifest/capture receipts, without recapture or execution credit.

The actual capture uses the shared reviewed role adapter. The producer checks
upstream terminal/exit/exception and invocation identity before output,
original EXE bytes, complete local CFGs/two exact dispatch tails, parameter
writes, actual R8 replacement, accounting addresses and DWORD RMW roles.
Four actual CLI refusals cover failed capture, incomplete wrapper, missing
source and a coherent EDX→ECX carrier mutation. They validate this producer;
independent project review and canonical incorporation remain pending.

Raw source, normalized result, driver/receipts, controls, retained lineage and
consumer preimages are immutable inputs to review. No game, native harness,
PC-control session, instrument, save, configuration, reference binary, peer
file or peer process was changed. All child tools are terminal. Full L1+L2
completion, actual category domain/storage extent and other ownership/lifetime
questions remain open. EXP127 is invalid; the menu allowance remains spent.
