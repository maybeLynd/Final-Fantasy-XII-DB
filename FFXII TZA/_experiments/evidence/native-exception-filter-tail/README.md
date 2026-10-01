# Original native exception-filter continuation — ASTRA (SOL), 2026-09-28

Question: CV-3 had not followed `0079AD50` beyond its `0x7837` text request. Does
the local tail return a disposition, resume execution or request termination?
Method A is sufficient for the instruction order, arguments and local return.
Callbacks, OS dispatch and presentation require separate evidence.

The verified shipping image hashes to
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Retained `filter240.bin` starts at `0079AD50`, ends at `RET 0079AE3F` and has two
validated local branches. The shipping reader and reviewed access-role adapter
are pinned to the original store-package commit. The adapter is actually called
for decoded memory roles, with store/LEA/read-modify-write controls in the checker.
Import descriptors, lookup bytes, DLL names and selected slot identities are
retained rather than substituting host-module bindings. Current canonical primary
and dirty/current hash are distinct in raw reference metadata.

The local source establishes:

- Gate zero branches to `MOV EAX,1` / epilogue / `RET`. It still calls
  `GetCurrentThreadId` before testing the gate. No universal live gate value is
  established here.
- Enabled paths request text `0x7837` at `0079ADE5`, **before** `ShowCursor(1)`
  at `0079AE0E`, correcting the existing page's order.
- Nonnull text sends its leading u16 and `pointer+2` to OLEAUT32 ordinal 4 at
  `0079AE00`; the returned pointer becomes RBX. Null text skips that call and
  retains RBX zero. DLL/ordinal identities do not prove names or native effects.
- `MessageBoxW` at `0079AE26` is supplied HWND zero, RBX text, the original UTF-16
  caption **error** at `008F3DC0`, and flags `0x10`. The displayed body and even
  successful display are unobserved.
- OLEAUT32 ordinal 6 receives RBX afterward (`0079AE2F`); a prior call at
  `0079ADDA` receives zero. Its name/effect is not established by this capture.
- All three local paths converge on return value **1**, assuming encountered
  calls return normally. There is no local return-zero/resume instruction.

The Windows filter API assigns return 1 to `EXCEPTION_EXECUTE_HANDLER`; its
associated handler usually ends the process. That API contract is not an observed
native FF12 outcome. [Microsoft's filter contract](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-setunhandledexceptionfilter).
An unknown callback could fail or not return; no claim of universal termination,
full-handler exception safety, actual filter installation, real exception arrival
or normal gameplay reachability follows. EXP-127 remains INVALID_POST_TRACE with
unknown fatal-error cause. No game was started or crashed for this package.

`raw.json` preserves exact identity/source/import/caption bytes; `result.json`
contains normalized conditional paths and limitations. Paths are source
calculations, not three execution tests. `capture.py` default checks retained raw
through the actual checker and propagates failure; it does not recapture. Three
private checker alternatives reject return zero, reversed cursor/text order and
invented named ordinal imports. These are producer controls, not independent
project acceptance.

The attached concrete prerequisite-control receipt exercises the actual80
retained-only producer without guest replay: baseline reproduces its result;
upstream exit7 despite PASS text, exception, missing checker/member/raw and empty
cases all reject without a result. It covers that invocation path, not every
runner. Source inputs remain unchanged. OPUS owns the separate SN1 partition
repair; FRONTIER's existing repair/review requests are not duplicated. Returned
SN1 and consumer reconciliation is a dated source/queue receipt, not a new
progress reporter or automatic acceptance.

First missing-pefile and named-only ordinal-preparation failures are recorded in
PLAN. The latter's original complete driver/output receipt was not captured before
correction; no fabricated original hash or semantic conclusion is supplied.

Consumers: FABLE owns CV-3 semantic prose; OPUS owns exact ABI/exception contract;
DATA incorporation and independent SPEC review remain separate requests. Replace
the unread tail with qualified source behavior/order and retain live/callback
gaps. PC OFF, no process instruments/save/config/reference changes. S19's spent
allowance and unapproved extension persist. Full L1+L2 goal remains NOT_MET.
