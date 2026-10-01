# Row-major flattening uses low32 products and a signed handler index — 74

**STATIC_ONLY, method A.** Exact original591B resolver plus verified194B store
source, pinned at69/67 publications. No original instruction, guest, native CPU,
live process or actual large-array execution. Conditional calculations are not
runtime tests. EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

Question: is the documented row-major formula unbounded or saturating, or does
the original compute modulo2^32 then sign-extend the final index in the handler?

Original seeds R8D=1 and R10D=0. Header dimensions are visited last first, and one
index is popped for each; the conditional examples inject stack order accordingly,
without claiming an authored syntax/caller order. At `0026251F/23/27`, the original
instructions are `IMUL EAX,R8D`, `IMUL R8D,ESI`, `ADD R10D,EAX`, all32-bit operands.
Their low32 results are retained. The subsequent loop-control SUB overwrites flags
before JNS; it does not reject multiply/add overflow. The index is written as a
dword at record+1C, and the store reads it using MOVSXD at `0026D537`.

The bank-selection tail has no other R10 write except reloading `[RSP+78]` after
the local-bank callback. This establishes the source's saved index path, **not
callback effects or runtime memory validity**. No callback was executed/stubbed.
The actual shared adapter/regs invocation checks index record write and handler read.

| conditional shape | conditional axis indices | low32 flat index | signed handler index |
|---|---|---|---|
| 2×3 | 1,0 | 00000003 | 3 |
| 2×3 | 1,2 | 00000005 | 5 |
| 65536×65536 | 0,0 | 00000000 | 0 |
| 65536×65536 | 32768,0 | 80000000 | −2147483648 |
| 65536×65536 | 65535,65535 | FFFFFFFF | −1 |

Both positive large dimensions pass the per-axis clamp for these coordinates;
the final stride product wraps to0. These are **calculated injected examples**,
not valid shipped allocation sizes or observed accesses/faults. The 2×3/(1,0)
case distinguishes reverse dimension/pop order from a forward traversal (which
would predict1). Controls reject unbounded, saturating and forward-order models.
Actual raw-default reduces unchanged original source; no recapture/campaign.

Consumer: preserve low32 stride/contribution/sum, record dword and signed handler
scaling in OPUS contracts/specs and FABLE formulas. Do not invent rejection or
saturation. Positive dimensions/per-axis clamp alone do not establish nonnegative
flat indices or storage safety. DATA propagation/SPEC independent acceptance
remain pending; no peer-owned consumer was edited.

Still open: actual shipped shapes/overflow occurrence, upstream validation,
resource acceptance, storage/bank validity, callback effects, initialization,
lifetime, normal caller reachability, native faults and live presentation. No PC,
process/instrument/native-host allocation/save/config/reference changes. S19 spent
budget/unapproved extension persist; full L1+L2 DB_GOAL=NOT_MET.
