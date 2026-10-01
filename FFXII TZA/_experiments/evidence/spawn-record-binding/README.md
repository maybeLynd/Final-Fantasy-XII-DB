# Spawn selection keeps the authored actor's script-register bank

Method A, conditional original-code dataflow. Producer valid; required
independent review and canonical consumption pending. Full database goal ACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000; no game, native or emulated execution.

Player version: one enemy script can contain several spawn/respawn routines.
Changing the spawn selection changes which routine the same actor record uses.
On the proved path those routines share the actor's script variables; a spawn
selection does not create a fresh bank of variables. This does not establish
which routines actually run, in what order, or what values gameplay leaves.

Returned RC16 already narrowed the old live-only question: a different authored
actor does not inherit this record within a pool. Its register persistence,
pool clear/release and read-before-write evidence are reused, not recounted.
The new discriminator is the identity passed from selection to the interpreter.

Original setentrygroup34FA70 passes the same actor to lists0,1,4,2,3 using one
popped selection.25AD10 reads that actor's function metadata, stores selection
at+F6 and maps spawn/respawn to override7/14.25AF60 resolves its self ordinal
through the current manager's owning pool. Under coherent manager/self identity,
valid metadata and normal ABI/no-interference premises, this returns the same
record. Do not generalize to corrupt/cross-manager/encoded-ID states.

The retained raw gol_b01 section has monster_00 at authored ordinal26, one
entry/function table containing spawn00..05 and respawn00..05. Raw CP932 names
are joined to IDs; decompiler labels are not used to identify the entries.
The six entry functions are a companion control; empty talk/touch lists remain
absent. This is one bounded authored control, not a repeated corpus census.

269860 reads that record's spawn/respawn override and submits a function request
to that record.3DB6E0 selects its active entry;3DBDC0 starts its PC from its
function table and bytecode base. Retained25DF00 supplies the same actor inRDX;
25E4C0 preserves it inR15, the established script-register bank base. Selecting,
submitting, starting and actually executing bytecode remain distinct stages.
Natural occurrence, repeated execution order/cause, interference and exact I1
values are not established. SpawnKeep's BattleStats block is a separate object.

Ten original bodies are qualified from retained regfile/SECTION12 evidence;
only seven missing spans are read afresh. The actual capture invokes the shared
reviewed memory-role adapter with store/LEA/RMW controls. Original bytes, full
image identity, source pins and required exit/result/exception status are checked.
SECTION12's external assertions/reviews and RC16 counts are not tests run here.

The first producer refused before creating a result: a flat address filter
counted an early failure-return POP RDI as if it could reach submission. The
producer now follows original normal CFG predecessors of the call; that POP and
RET cannot reach it. The failed invocation/preimage remain immutable. The actual
return-path control is recorded in the positive and reused by the control tool.
Four actual CLI refusals test failed capture, a coherently changed actor argument,
changed authored selector and missing retained input. No invalid/zero-case run
is counted as passing. Controls are producer checks, not project acceptance.

Reproduce with existing analysis Python into a fresh output:

    python <packet>/prove-regfile-spawn-record.py <fresh.json>

Consumer: FABLE semantic RC16; OPUS/SWE2-CONTRACT interpreter/register/selector
contracts; FRONTIER's AQ11 prepared-live premise. Canonical pages are peer-owned.
Retain accepted clear/persistence bounds and unproved takeover-reader reachability.
No claim that the whole OV16/AQ11 database obligation has completed from this
conditional packet. Menu allowance remains spent/unapproved; EXP127 remains
invalid. Cleanup: all finite children terminal; no PC/game/input/instrument,
save/config/reference writes or peer process changes.
