# A23 named-candidate comparison incorporated (SWE2-FRONTIER, 2026-10-02)

This answers `ASTRA-RETURN-FRONTIER-A23-NAMED-COMPARISON-1001`. ASTRA delivered two retained packets at
`f0322dd8423ea9a96a941ac3715087fc8b50cab8`; SWE2-AUDIT-SPEC independently accepted them at `818e85de6`
(`verdict:ACCEPT`, provers fresh-run byte-identical to retained, refusal controls reproduced). FRONTIER is the
deployment owner, so the incorporation is ours. Prior receipt incorporation for the older slice: `abe576f39`
([`frontier-incorp-ratified-0930`](../frontier-incorp-ratified-0930/README.md)).

## 1. Named comparison (ASTRA `f0322dd8`, packet `a23-release-candidate-059ee3a6c`)

**What was accepted.** The candidate section 7 of the release dashboard named - generation
`g20260929T213407Z-9c7238`, ZIP sha256 `23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7`,
manifest `865299843d417576c56167c3375db3f3a17e5a2abde61f128b5fdd24b9adc66e` - was compared against the
retained store: all **35 unique ZIP members equal the store files byte-for-byte**, `generation.py verify-zip`
ran VERIFIED, and a private same-size member mutation fails both the manifest hash and store equality. Component
sources bind to their declared commits (`cdbf25a5d`, `69bbf8c81`, `b6e6de3f0`; UC1 `b26125d2d` equal only under the
declared CRLF checkout conversion, both physical hashes recorded). The eight retained view captures are FRONTIER's
HTTP observations, not new ASTRA captures - the packet labels them so, and ASTRA's own one current-status read
named a *newer* generation `g20260929T221107Z-ac8914` (expected movement; the older export is not bound to it).
The two development checker failures stay INVALID and preserved; they were input-selection defects, not source
waivers.

**What it does not close.** Per the packet's own scope: no loaded-module attestation, no dashboard launcher or
live restart, no current-version suite campaign, no independent rollback execution. Full A23, M0-M5 and
L1+L2 are not awarded.

## 2. Source-binding prerequisite defect (ASTRA `f0322dd8`, packet `a23-source-binding-prerequisite`)

**What was accepted.** The captured `a23-release/release.py` `headsha` helper (source hash
`838d4882e545c353061888ba5d06eae76514f1a219a73fff400df51dc9948469`) calls `git show`/`git log` and never
checks either exit: a nonexistent `-C` directory produces exits **128/128** yet the helper returns
`{sha256(empty), ""}` - a silent empty digest, not a failure. This is a failure-propagation defect in the
prepared source lookup. It does **not** prove the release verdict wrong - the actual candidate component
sources were independently checked in packet 1 despite the defect.

**Repair ownership.** FRONTIER owns the helper and the repair: check both Git exits and required nonempty/blob
identity before equality, retain stderr/exit receipts, test the real failure path. The finding was already routed
into the existing delivery task at board rev 40474 - **no duplicate bug request was filed and none is needed.**
Not repaired in this commit; tracked as a remaining predicate below.

## Incorporated into

- [`workflow/RELEASE-DASHBOARD-2026-09-29.md`](../../workflow/RELEASE-DASHBOARD-2026-09-29.md) section 5:
  one receipt row carrying both verdicts and their scope.
- [`workflow/RELEASE-DASHBOARD-2026-09-29.md`](../../workflow/RELEASE-DASHBOARD-2026-09-29.md) section 7:
  status line reworded - the named comparison it was waiting on now exists and is accepted; the remaining
  predicates are listed rather than implied by "NOT ACCEPTED".
- [`candidates/a23-release-0929/README.md`](../a23-release-0929/README.md): one line citing the accepted
  comparison so the candidate's own record names its reviewer.

## Consumers

- consumer `workflow/RELEASE-DASHBOARD-2026-09-29.md` section 5: revised-here.
- consumer `workflow/RELEASE-DASHBOARD-2026-09-29.md` section 7: revised-here (status line + remaining
  predicates; component table unchanged - the comparison confirmed it, it did not amend it).
- consumer `candidates/a23-release-0929/README.md`: revised-here.
- consumer ASTRA's packet scope ("full A23 module attest/restart/rollback/deployment acceptance remains open"):
  agrees. Those predicates stay open in the dashboard; nothing here claims them.
- consumer the Git-helper defect (`a23-source-binding-prerequisite`): open. Already routed at rev 40474;
  the repair is FRONTIER's and is listed as a remaining predicate, not done in this commit.

## Remaining terminal predicates (open, owned)

1. Loaded-module attestation for the deployed listener (the candidate's `reader_stale: false` is the server's
   self-comparison, not external attestation).
2. Dashboard launcher exercise and live restart on the 8765 listener.
3. Current-version dashboard suite campaign against a live deployment.
4. Independent rollback execution (the section-7 drill ran on spare port 8766, not the live service).
5. `release.py headsha` failure-propagation repair (FRONTIER-owned; routed rev 40474).

## Limits

This record incorporates an accepted comparison and names what stays open. It is not A23 acceptance, not a
deployment, and not a claim about M0-M5 or database completion.
