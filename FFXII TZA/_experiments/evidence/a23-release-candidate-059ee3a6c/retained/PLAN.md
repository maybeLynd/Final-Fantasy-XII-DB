# Independent check of FRONTIER's named A23 candidate

Target: deployment-owner commit `059ee3a6ccf9f4d5b49ef52deb61d1be75bde1e9`,
generation `g20260929T213407Z-9c7238`, manifest
`865299843d417576c56167c3375db3f3a17e5a2abde61f128b5fdd24b9adc66e`,
ZIP `23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7`.

Question: does this exact portable snapshot equal the retained generation and
the producer's captured served view objects, with source identities checked
through successful Git calls? H1 all match at this release window; H2 a
generation/member/source difference invalidates the stated matching snapshot.
Current has already advanced; do not compare that new generation to this ZIP
or infer that the candidate was mismatched at its own release window.

Method: independent read-only file/ZIP/hash/JSON comparison, actual supported
verify-zip command with checked exit/output, pinned Git source bytes and
explicit CRLF treatment. Retained HTTP belongs to FRONTIER, not ASTRA live
capture. A private same-count member change must fail the equality control.
No export, rebuild, server restart, launcher or peer write. ASTRA's current
HTTP status read showed g20260929T221107Z-ac8914 with no problems; this proves
movement, not failure of the earlier frozen release.

Acceptance is bounded snapshot/source receipt checking only. Actual loaded
module attestation, current-code suite gaps, launcher/restart and rollback
verification remain separate A23 requirements. Producer rollback/process
receipts are evidence to review, not tests ASTRA performed. Keep whole A23 and
M0-M5/database acceptance unawarded unless their own requirements are proven.
