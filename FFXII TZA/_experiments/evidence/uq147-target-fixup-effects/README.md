# UQ147: target-fixup conditional effects and a retained fixture gap

## What the player would know

When cleanup removes a unit from another unit's contributor list, the later
helper can update a combat flag without rewriting that unit's command or battle
mode. Its decision also consults a global roster condition: a qualifying action
against any party member can matter, rather than only an action against this
particular receiver. This is a code-level result under stated assumptions; the
actual timing and visible outcome of a summoner being KO'd while an Esper is
active are still unobserved.

## Question and method

Does original `002FEAD0`, called after contributor removal, have command/mode
effects hidden in its callees, or only the bit52 update? Is `0030C0E0` a
receiver-specific predicate? Method A suffices: use already retained shipping
body identities, recheck original bytes, close all direct calls/tail calls and
inspect every persistent memory-write site. No new native/emulated/live run.
No repeated EXP091/102 native suite or sampled gameplay. A live session would
add cost without establishing a stronger complete conditional effect set.

## Identity and starting evidence

EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `0x120000`. `source-target-fixup-01.json` binds thirteen retained
bodies and exact byte hashes: EXP091 supplies complete 172B `002FEAD0` and 290B
`0030C0E0`; EXP102 supplies the seven resolver/count/getter bodies; the earlier
mode-query source supplies four field-query leaves. EXP102's `0031B7E0` stops
at `0031B80A`; the longer EXP091 identity includes later padding and is not used
as its semantic instruction domain. Earlier new mode-query independent review
is still pending; here those bytes are checked directly, not accepted by label.
The actual capture path uses the reviewed access-role adapter, including real
store/LEA/read-modify-write controls, and the validator re-decodes this source.
Raw inputs, original producers, status/stdout/stderr and normalized results are
frozen together. Historical native case/mutation counts are not ours.

## Result

`result-target-fixup-effects-02.json` closes the complete normal local CFGs and
all reachable direct/tail callees: twelve helpers are read-only outside private
stack storage. Six persistent write sites in `002FEAD0` touch only DWORD+4;
they clear/set bit20, QWORD flag52. They preserve its other bits. No direct or
transitive command+714/pending+BA0/separate-mode write remains in this bounded
closure. This does not cover preceding notify `00313B30` or the other KO callees.
NULL receiver changes no object. Separate AND/OR writes are not atomic.

The global predicate does not consume incoming receiver RCX: roster index
starts at zero, argument-independent COUNT runs, and ECX is overwritten with
the roster index before GET. It can return true for a qualifying action toward
any party-kind0 target. The contributor scan separately compares indices0..31
against the full EA9 byte. No natural EA9<32 invariant is asserted.

Under readable, no-interference state the read-only closure leaves roster count
N fixed. Signed N<=0 returns immediately; positive N<=INT32_MAX bounds iteration
by N without EDI overflow. The contributor loop is bounded by32. Counts and
action/base pointers are nevertheless read again: this is no live snapshot or
scheduling guarantee. Row addressing truncates the second resolved base to
32bits, adds stride*WORD+714 in 32bits, and reads byte+6. NULL table/first resolver
sets row0 and then reads address6: missing binding can fault, not return false.

## Concrete retained producer gap

The actual EXP091 `World` constructor writes HEAP to `G_IMGB=0x1F85D30` (not only
a comment). Shipping resolver `0020E602` reads `0x1F83530`. The addresses differ
by0x2800. The pinned retained result has87 baseline and10 mutant rows,97 total;
it contains zero recorded `imgadd` entries and only `canc-fixup` enters `tvalid`.
That record does not positively exercise the affected action-row path.

This is a preparation/control gap, not a blanket rejection of87 prior tests.
The direct bit22/copy observations remain separately supported. ORACLE must
repair the producer's actual initialization and add the smallest positive
original resolver/action-row control; new raw receipts must keep old ones.
New independent review and canonical consumer agreement are pending.

## Controls and failure handling

Five explicitly labelled source-record detector controls reject a helper store,
opaque callee, wrong flag mask, wrong null-table successor and new dependence
on incoming receiver. They are not byte mutants executed on a CPU. Actual CLI
negative control supplies a failed qualification receipt: exit1 and no result.
The successful qualifier and producer runs are required, not inferred from an
empty file. An earlier qualifier failed before output because EXP091 bodies
uses `real_bodies_executed`, not a top-level list; its exact source/receipt are
preserved. It was repaired with explicit schema/EXE binding. The first attempted
relative runner path failed before starting the child; the supported runner
requires absolute driver/tag paths. No failed run is counted as valid.

Reproduce the current invocation with the absolute argv in the receipts. For
an independent immutable reduction, import the frozen prover and call `derive`
on the frozen source, and `validate` from the frozen validator against the shared
pinned adapter. The original main also verifies pinned repository inputs; if a
producer has since been repaired it must refuse changed inputs. The retained
old producer/result let reviewers independently check the exact AST constants,
initializer and trace count without rerunning the historical suite.

## Limits, consumers and cleanup

Conditional original-code effect proof needs valid BattleUnit/table identity,
readable inputs, separate private Win64 stack/home space, normal ABI and no
external interference. Fault/exception paths are not successful completion;
volatile register/flags and stack effects are not being called absent. This
does not prove live initialization, target/action natural reachability,
ownership/lifetime, KO/Esper pending113 coexistence, timing/presentation or full
UQ147. It does not establish global absence from a retained trace.

Consumer roles: independent SPEC review; FABLE/OPUS consume the effect boundary
and global-versus-receiver predicate through their existing UQ147 correction
tasks; ORACLE owns the actual EXP091 fixture repair/control. No claimed peer
page or historical raw result was edited. One bounded effect question has a
producer answer without gameplay; no whole formerly-runtime row is declared
closed before independent acceptance and canonical incorporation.

No FF12 process, PC control, native/emulator session, instrument, save/config or
reference write was started. Finite producer/control shells returned terminal.
Parked menu allowance remains spent/extension unapproved; EXP127 remains invalid
with crash cause unknown; K14 accepted/closed. Full L1+L2/M0-M5 goal ACTIVE/NOT_MET.
