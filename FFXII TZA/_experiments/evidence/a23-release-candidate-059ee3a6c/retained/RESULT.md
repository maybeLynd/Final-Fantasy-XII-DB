# Named A23 candidate: snapshot and component-source receipt verified

**Scoped snapshot/source verification only; full A23 remains unaccepted.**
ASTRA independently checked the candidate delivered by FRONTIER at
`059ee3a6ccf9f4d5b49ef52deb61d1be75bde1e9`. This is the named historical
release window, not an assertion that CURRENT can never advance.

The ZIP for `g20260929T213407Z-9c7238`, SHA256
`23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7`,
has 35 unique members. Every member equals the corresponding retained store
file byte-for-byte. Manifest SHA256 is
`865299843d417576c56167c3375db3f3a17e5a2abde61f128b5fdd24b9adc66e`.
All declared input/output sizes and hashes verify, including the external
certified EXE. The supported `generation.py verify-zip` actually ran with
checked exit 0 and the exact generation/35-member JSON result. A private
same-size member change fails both manifest hash and store equality; no ZIP
or store was rewritten for this control.

The producer's before/after status and eight served view captures are
retained verbatim with their recorded status/size/SHA identities. All eight
parsed view objects equal the candidate ZIP outputs; both retained statuses
name the candidate with no problems and `reader_stale:false`. **Those HTTP
observations were FRONTIER's**, not eight new ASTRA live captures. ASTRA's
own one current-status read named `g20260929T221107Z-ac8914`, showing expected
movement. That new generation is not compared to the older export.

Source verification uses each component commit named by the original release
receipt, through successful nonempty `git show` results. The evidence-publication
commit does not define all deployed component versions: later code commits
can land while the release capture is being published. Builder `cdbf25a5d`,
requirements `69bbf8c81`, and verifier `b6e6de3f0` bytes match their manifest
identities exactly. UC1 `b26125d2d` is equivalent solely under the declared
CRLF checkout conversion; both physical hashes remain in the result. No
normalization is used to excuse a mismatch in the other source components.

Two development checker failures are preserved separately and remain
INVALID: the first incorrectly required CRLF checkout bytes to equal the
pinned Git receipt and guessed that raw captures were published at its root;
the second bound source to the evidence-delivery commit rather than declared
component commits. The repaired producer uses the pinned Git receipt,
retains raw bodies from the original run only after verifying every recorded
hash, and binds exact component sources. These are input-selection repairs,
not a waiver of source or raw-byte requirements. The final checked run is
the successful receipt; earlier partial checks never became an A23 verdict.

This closes the formerly missing **named snapshot comparison** at this scope.
It does not supply a new loaded-module attestation, dashboard launcher or
live restart, current-version dashboard suite campaign, or independent
rollback execution. The owner's process/rollback evidence remains available
for separate review and must not be counted as ASTRA execution. A distinct
source-helper finding shows its Git failures were not propagated; the actual
candidate component sources were independently checked here despite that
defect. FRONTIER owns its repair. Full A23, M0–M5 and FF12 L1+L2 are not
awarded by this result.

Raw body receipts, full member list, checked Git exits, component and tool
identities, supported verifier output and the private control are in
`result.json`/`retained-http`; final invocation exit is in `terminal.json`.
No export, rebuild, game/PC control, server restart, peer or reference write.
Reference archive hash remained unchanged. Independent acceptance of this
ASTRA-authored checker/package still requires a nonauthor reviewer.
