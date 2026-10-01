# Conditional owner deletion, waits and definition binding

**Producer-valid Method A; independent review and canonical incorporation pending.**
Reference image SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, preferred base `00120000`.
No native machine-code execution, FF12 process, gameplay, intervention or new whole runtime-row closure.

The question is whether manager resource replacement necessarily drains pending
resource requests after deleting old external owners and before resetting their
records in the new definition binder. The answer established here is narrower:
the named local unload barrier has both a live-bit and group/byte gate.

| Values at the original tests | Named `003DD380` deletion | Named `0032E520(0)` waits |
|---|---|---|
| Any valid group 0..4, live bit clear | skipped | none |
| Live group 1..4 | called | none |
| Live group 0, `003603C0()` returns zero | called | none |
| Live group 0, `003603C0()` returns nonzero | called before waits | `00262AF2`, `00262B0D`, `00262B1E`, on normal return |

These are eleven equivalence partitions of original local control flow, with
remaining state branches unconstrained. They are static computations, not
eleven game states or executed native tests. `003603C0` is the original
eight-byte `MOVSX EAX,BYTE[022CB726];RET`. The gate value is read at that point;
entry value, default initialization and natural combinations are not assumed.
The preceding repeated-read loop may fail to terminate. There is no deadline,
atomic emptiness or proof that opaque callees do not wait/submit elsewhere.

The retained `0032FCA0` normal local CFG calls `002628B0` before its reset
`0032ED80`, auxiliary request at `0032FF0B` and primary loader `00330310`.
This reuses immutable `bts-index-binding/index-path-raw-02.json` and its
manifest; it does not duplicate GR17's caller, reward-lifetime or effect census.
That preceding unload call alone cannot imply a universal local queue drain.

The exact primary-load callback chain is now explicit. On the normal positive
size request arm, `00330310` stages callback `003304A0` in descriptor `+0x10`
and packed `low32(allocation) OR group` in `+8`. The D4/non-null override arm
copies then calls `003304A0` directly. Queue admission, actual IO and callback
scheduling are separate obligations. The original callback uses its packed
first argument, with low four bits as slot and the cleared low-32 representation
as base. Section `+0x10` reaches `0032F850` only when count>0, offset nonzero
and computed pointer nonzero; low32/tag packing is retained. Exact pointer
identity requires the relevant low-address/alignment/valid-memory premises.
`0032F850` reaches binder `0026C8C0` only with nonzero first section byte and
a supported arena branch. The earlier owner-reset-barrier result separately
establishes that binder's normal tail to `003DD790` with the original group.

This does **not** prove a queued old owner survives naturally into that reset,
or that a universal lifetime invariant is absent. It narrows the prerequisite
that a stronger proof must establish. Next inspect existing original
`0032ED80` cleanup and accepted owner callback/cancellation/producer evidence
for a pending-request exclusion or guaranteed completion for this group.
Do not infer it from hours without a live hit or from a forced callback.

`prove_owner_reload_order.py` checks both capture exit/output/driver identities,
actually uses the shared reviewed access-role adapter via the validator,
re-reads the certified EXE and verifies every captured/retained byte. It closes
the bounded local CFGs, checks group/SIL provenance, computes the partitions
and proves the specified dominance. The same adapter's store/LEA/RMW controls
execute in both capture paths. Captured spans are selected local source,
not new universal function extents or instruction-coverage certification.

Four actual reducer CLI refusals preserve failed-capture status, a missing
definition range, a coherently annotated/rehash-changed group branch and a
missing retained source. Every refusal exits nonzero without result. Valid
empty wait sets remain distinct from missing/invalid source. The positive
result is `owner-reload-order-result-01.json`; no unchanged repeat was needed.

Reproduce the reducer with a **fresh** result path and this evidence directory
as its second argument, using repository Python/Capstone5.0.7 and the immutable
`bts-index-binding` dependency. Do not execute or replay administrative board
operations. All child processes are terminal; sources are read-only; no saves,
configuration, reference executable or peer files were modified.

Independent SPEC must review source/partitions/conditional callback scope.
FABLE owns indexed-owner prose; OPUS owns the ownership/type contracts.
Producer controls, external prior results and project acceptance remain separate.
