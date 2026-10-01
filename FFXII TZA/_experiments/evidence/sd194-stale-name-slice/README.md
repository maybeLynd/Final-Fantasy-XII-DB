# Missing field-effect name: exact builder boundaries

ASTRA, 2026-10-01; method **A, STATIC_ONLY**. Producer proof/control complete; independent review and canonical consumption pending. This resolves conditional implementation facts, not SD194's natural-field-entry or observed-stack question.

After the namespace lookup returns −1 on a null name slot, the source name is unchanged. The caller does not check that return. Its next steps are more specific than “request whatever the stack held”: it copies through the first NUL, scans the name backwards for byte0x5C or0x2F, and changes the copied output according to the separator and basename length.

Let n be the index of the first NUL,0≤n≤259. Let j be the final separator index, or−1 if there is none; let k=n−j−5 when j≥0. At the local boundary just after `00377F12`:

| admitted source class | exact original result |
|---|---|
| no separator, including empty text | EDI stays0; the final store clears output[0] |
| separator and k<0 (basename0–3bytes) | the signed index captured at377EF3 is−4..−1; the terminator goes before the copied output and the copied C string is retained |
| separator and k=0 (basename4bytes) | output[0] is cleared |
| separator and k>0 | call377EC9 reaches the declared memcpy boundary: RCX=output+12,RDX=input+j+1,R8=k+12; under normal return/ABI, suffix stores are at output+k+12..15 and the NUL at+k+16 |

These statements assume valid stack memory, a bounded first NUL and normal ABI/noninterference. A failed lookup supplies none of those initial byte values. They do not identify an actual requested filename or prove an ordinary field reaches this branch. Later opaque allocation/context helpers and queue acceptance/execution remain separate. The output address supplied to both named request calls is statically the same local output; actual caller flow and native effects are not observed.

The input is at entry-RSP−0x148, the copied output at entry-RSP−0x258:272bytes apart. The initial n+1-byte copy is disjoint over the admitted domain. The negative terminator is outside that copied output but within the allocated stack frame; no crash or stack-frame corruption is inferred. The positive branch's copy count includes12 beyond k. Its source interval extends through input byte n+7, and its destination through output byte k+23. Nine hypothetical long-string/early-separator length classes overlap those intervals (listed in result01). Microsoft's [memcpy contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/memcpy-wmemcpy?view=msvc-170) does not define overlapping copies; this is a contract limit, not observation of a loaded implementation or a shipped name. No general overlap safety follows.

The proof is original disassembly plus integer/interval reasoning. It pins69 operations and closes the full loader, lookup and conditional CFGs. The partition count is not a sample claim: `result-01.json` classifies all33,930 admitted (length,last-separator) pairs into260 no-separator,1,030 negative-offset,255 zero-offset and32,385 positive-copy-boundary cases, with a deterministic digest. These are finite source partitions, **not** game states, original-code executions or live tests. Last-separator induction covers all nonzero byte choices with those positions; byte separators do not establish Unicode source-character boundaries.

Source identity: reference executable SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000. Bodies377DC0..37802A (RET378029),2DF880..2DF8D9 (two returns),861EBA..861EC0 (six-byte import thunk). IAT8C2A68 declares VCRUNTIME140.dll memcpy. This is physical import identity, not loaded-module/implementation/effects evidence. The shared reviewed access-role adapter is invoked in the actual capture path and rechecked in the actual reducer; memory-store, LEA and atomicRMW controls pass.

Actual capture/proof invocation receipts preserve driver hashes, exit/exception/terminal state and raw stdout/stderr. The corrected controller02 requires the positive producer prerequisite and the exact failure diagnostic for each of four actual reducer CLI controls: upstream failure, incomplete body, coherent changed arithmetic bytes, and wrong final-store role. Original controller01 and results remain: its observed diagnostics were correct, but its general nonzero check could accept an unrelated failure. Controller02 fixes that producer cause; no semantic/native run was repeated. Synthetic changed bytes test refusal of non-original evidence, not changed FF12 behavior.

DATA/OPUS consumer changes, after independent scope acceptance: describe these conditional branches and buffer offsets/copy count; keep actual inherited bytes, absent-NUL/more-than259-byte cases, valid initialization, loaded memcpy behavior and natural missing-name field reachability OPEN. Do not repeat b14's census or count its native controls as ours. A/B cannot reveal unobserved naturally inherited bytes merely by composing a harness. Any future live SD194 request still needs a precise field/save/state/trigger and validated minimal collector; this package supplies its discriminator, not permission to retry the parked menu setup.

Reproduce the reducer with the repository interpreter: `python -B prove.py <fresh-result> --src <packet>`. Required shared tool copies are under dependencies in the published packet; original image/access adapter qualification remains an explicit reference requirement. Run the controllers only in fresh owned directories. Never overwrite retained/canonical results. Missing prerequisite/body/control is invalid or INCOMPLETE, not an empty pass.

All own capture/proof/controller children exited. No runtime/PC session, service, device/game process, save/config/reference or peer file/process was changed. The overall L1+L2 goal remains ACTIVE/NOT_MET; this producer package and review routing are not database completion.
