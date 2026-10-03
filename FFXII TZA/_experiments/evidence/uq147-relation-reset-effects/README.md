# Inline relation reset is not linked-pool release

Producer-valid Method A; non-author review/canonical consumption pending.
No native, emulator or game execution. Full UQ147 and database goal remain open.

Player view: clearing a character's relation markers is different from releasing
the shared records it owns. A reconstruction must preserve that distinction
when cleaning up or reusing a character. This does not establish when normal
gameplay invokes these routines.

Question/competing explanations: 00512EE0 and 00512C80 both release the linked
pool, or only the latter does? Verified original bytes and complete normal
write/dataflow boundaries suffice. No absence sampling or live session is needed.

Reference EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. source-relation-reset-leaves-01.json SHA
ccf583cf77a01c2d9e043994e2d0d623c13c33515f7255c032ef4b3cec266f10.
Two entry-reachable leaf spans: 512C80..512CCE (78B,
f5196e64877e4bd68bacdaede264974e38f96d16544aea43ef6e97ff7d39bb60) and
512EE0..512EEF (15B,
058bbd3fa9ba3fe8e9e235468dde875ef1b950b562a06579ae336e9f0c48de3f).
Neither has a covering .pdata row. The first is bounded by the independently
qualified512CD0 entry; the second by known physical512F30. All direct local
successors/no calls/RET boundaries are checked; no physical root invented.

Actual qualifier d1718ca9f3a337b68d57c541957b46ed281df337379bd3adc2cfbddc8fb09240
invokes reviewed capture-index-path.py cbfb9b43 (and its three access-role
controls) with adapter5fcc6484. Actual validator7c4ea9f6 rechecks original bytes
and roles. Producer5b616396914a61f0bcc0a226e476f451867291dfc8e35586126e9cfc70421ef0
has actual terminal0/result01 with three labelled source-record controls.

| original routine | persistent effects under valid disjoint owner/pool state |
|---|---|
| 512EE0 | AND owner+F,F0; WORD owner+C=FFFF (head/tail FF); BYTE owner+E=0. No pool or global-counter write. |
| 512C80 | If head!=FF, load byte2EBA481 into EDX, visit each head/next node in pool2CA81F0, ADD DL,FF and AND node+F,F0. At final nextFF, store DL once to2EBA481; then the same owner reset. HeadFF skips counter read/write. |

The node address is pool + zero-extended index*16 (512CA0/A6/AA). Next is read
from node+E at512CB1; none of the writes changes it. With a valid finite acyclic
owned list of n distinct pool slots, n<=32 and final counter=(old-n)&FF.
Owner count is set to0; this does not validate its previous value or list length.
Neither routine clears DWORD IDs, node links or self-slot indices. High flag
bits are preserved. Neither calls heapfree/callbacks or updates cursor/high count.

Thus simple reset cannot substitute for linked release when active rows must be
reclaimed. If reset is applied to a nonempty owner, its links are discarded
without clearing those nodes. That is a conditional local effect, not proof that
a natural caller leaks/orphans rows. Cached counter store occurs after individual
slot clears; the whole operation is not atomic. No live scheduling inference.

Three synthetic source-record defects are rejected by the intended detector:
missing pool release, added pool-base reset write, changed global-counter target.
They are producer controls, not native byte mutations. Actual current CLI given
the labelled failed qualification terminates exit1/exceptionnull with the specific
upstream marker and no result. The freeze procedure verifies its exact argv,
current driver identity and the matching positive status/result, not exit alone.

Limits: valid disjoint16B owner/fixed32x16B pool, consistent indices0..31/FF,
finite acyclic owned list, normal returns and no interference. Corrupted cycles,
indices, ownership across owners, initial self-slot values, caller ordering,
reuse/lifetime, natural KO/Esper113 and wholeUQ147 remain unproved. Physical
access/layout prior DATA credit is preserved. SPEC independently reviews effects
and controls; OPUS owns representation/ownership contracts; FABLE semantic
composition. No whole formerly-runtime row credited before acceptance.

Reproduce current proof to a fresh result in a fresh child of the existing ASTRA
runtime-residue-method-retriage directory, copying the pinned inputs/producer
and using its reviewed parent validator. No recapture or game needed. Never
overwrite the published receipt/result names. Qualification additionally needs
the authorized EXE and reviewed capture adapter; dependency identities retained.

Cleanup: no PC control, launch, attach, memory/native/emulator write or save/config/
reference modification. All scientific children/shells terminal. Peer files and
processes untouched. Parked menu consumed/unapproved; no setup attempt.

Next discriminator: verify actual callers and their release-before-reset/reuse
ordering from existing retained bytes/call relationships. Do not infer it from
these two local bodies or start gameplay just because lifetime is mentioned.
