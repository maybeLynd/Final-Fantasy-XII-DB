# Cache allocation-zero versus lookup-miss contract

Method A, STATIC_ONLY. Complete original code and retained caller evidence
distinguish ordinary allocation failure from the negative lookup-miss sentinel.
No heap failure was induced, no original instructions executed, no game launched.

For the player: failing to create a cached file handle takes a different path
from not finding the file in cache. Reconstruction must preserve that distinction
and the bookkeeping done before allocation. This is not an observed game crash,
leak or proof that normal play exhausts memory.

## Question and competing hypotheses

H1: allocator-zero is equivalent to lookup-miss and automatically falls back to
archive loading or rolls accounting back. H2: the original routine increments
local counters before allocation, returns0 without local rollback on ordinary
NULL, and the selected caller tests only the negative sentinel for fallback.

The shipping branches, carriers and local effects distinguish H1/H2. A live
failure sample or forced native call would not prove a broader invariant and is
unnecessary for this contract. Natural allocation failure, actual ownership/
cardinality and later consequences remain separate open questions.

## Original reference and preparation

EXE SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000h. Source01:20C300..20C438(312B),210EC0..210ECB(11B),85E730..85E737(7B).
Source02:808C40..808C61(33B) security-cookie body. Both captures require checked
terminal/exit/exception/driver identity and actual reviewed access-role adapter.
`retained-identities.json` binds the published preprocessing wrapper and own
frozen, independently pending backfill packet. Selected retained code is again
compared to original EXE; reuse is not a new capture or acceptance.

The PE declaration identifies api-ms-win-crt-heap-l1-1-0.dll!malloc through IAT
8C2B40 and hint/name1DEEE88. This is shipping import identity, not the live bound
DLL or a sampled allocator return. Source qualification is explicitly feasibility
only; its checked result is required but cannot substitute for semantic proof.

## Established conditional result

- ManagerDWORD88 increments at20C328 before the16B allocation at20C400. Every
  local allocation path also has exactly one recordBYTE10 increment at20C354,
 20C38B or20C3F8. These local effect counts are not live handle cardinalities.
- On ordinary allocatorNULL,20C40D reaches20C423 XOREAX. The routine skips217A60,
  makes no subsequent own object writes, rollback or call, and returns0.
- The selected lookup-found path retains the zero return through RBX, normal
  unlock and the successful original cookie-return arm. The cookie body has no
  RAX writer; this is a checked original instruction fact, not an assumption
  that Win64 volatile RAX always survives arbitrary calls. Failure tail is opaque.
- Resolver59EFEA stores zero into QWORDrecord20.59EFF1 uses JS: negative results
  take archive fallback; zero follows the cache-success path, copies the size
  output and returns status0 without archive/fill calls on that postlookup path.

Therefore zero is not the-1 miss sentinel, and status0/counter increments do not
certify a constructed view. Premises include valid map/records/disjoint frames,
normal returns/nonvolatileABI, helper-returned valid records/no opaque field
interference and successful cookieRET. Native exception cleanup is a separate
path. No actual failure, leak, BYTEwrap, runtime import binding or natural reach.

## Failure-aware producer and controls

Producer01 refused with no result: a linear RAX-preservation interval accidentally
included the unvisited miss instruction20C2C7. Its driver/raw receipt remain
immutable. Current producer follows the actual reachable found-return CFG from
20C2B9 through20C2BC to20C2CB and excludes that miss arm. The carrier guard was
not weakened; original input bytes were unchanged. This procedure is reusable:
check reachable slices rather than treating all intervening addresses as one path.

Producer02 terminal0:
3d016099266d7413ad648331d64503e635cb03d4de02c322cd7cd7b9c334e4e9.
Five actual disposable CLI refusals, control01 terminal0:
61e09600b592221bdc96bd6c936983253f1d10bb053edb7ccdc5aea35f22ee0e.
Cases cover failed cookie capture, missing cookie source, failed source
qualification, missing retained lookup, coherent NULL-branch JE→JNE bytes.
Each requires nonzero, matching diagnostic and no result. All required
prerequisites are checked before emission; incomplete or zero-case output fails.
No native/emulated/FF12 executions are counted. Reproduce with the existing
analysis venv: `python -B prove.py fresh-result.json`, retaining fresh receipts.

## Canonical consumers and limits

OPUS: failure return ABI, counter-phase and selected lookup/resolver propagation
contracts, including normal-versus-exception paths. FABLE: file-cache/source
resolver semantics and fallback qualification. Existing Audio citations/reviews
remain peer-owned; this composed contract neither duplicates their census nor
changes their pages. Actual allocation failure, allwriter/cardinality/lifetime,
reuse/scheduling and later reader consequences remain open. Distinct manager
roots20C700→1F83438 and1DADA0→1F82CF0 are not conflated by equal field offsets.

Raw source, receipts, driver preimage, result and controls are immutable. Only
owned offline files changed; all owned helpers terminal. No game/PC/instrument/
save/config/reference or peer changes. Independent review/canonical consumption
required. Historical four accepted offline runtime-needs eliminations unchanged;
zero wholeOV closures. Full L1+L2 ACTIVE/NOT_MET, K14 closed, EXP127 invalid,
parked menu allowance spent/extension unapproved.
