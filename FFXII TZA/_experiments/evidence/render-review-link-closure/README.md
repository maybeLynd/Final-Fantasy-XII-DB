# Additive repair of copied render review links

Ten links in three copied independent reviews omitted their destination files.
The old 76 members and original manifest remain byte-identical. Seven exact
reviewer script/output siblings and a navigation-only alias restore the paths.
See [the original packet](../render-review-phase-qualification/README.md).

[Preparation](prepare.py) validates all old members, equal shared-library bytes,
review text equality (two primary checkout copies differ only in newlines), and
projected link closure before any output. [Result](result.json) records both
byte identities and each destination. [The additive map](additive-paths.json)
pins the exact added bytes. Publication remains pending until its guarded commit.

The recurring procedure cause is corrected in the actual shared prepare() path:
copied-render-review link closure now runs before folder creation, copy or
handoff writes. [The private path control](publisher-path-control-01.json)
exercises that real function with a synthetic board and files: missing referent
refused before writes, positive referent detected. It does not acquire a real
publication reservation. [Three command-line controls](controls-result.json)
refuse missing referent, conflicting same-name library and changed old member.
These are publication controls, not FF12 experiments or extra semantic checks.

The copied FABLE scripts and outputs are earlier independent corroboration.
ASTRA did not run them here. No render claim, native effect, scheduling,
reachability, ownership or game-state conclusion changes. Existing acceptance
stays scoped; this repair needs its own delivery/check receipt.

Reproduce the preparation from the repository root using prepare.py --output
with a fresh ignored directory. For the path-control reproduction, place the
retained publisher-driver.py one directory above control-publisher-path.py,
named prepare-residue-packet-publication.py, in disposable scratch under this
repository; the original controller imports that exact dependency. Its hash is
pinned. Do not execute the retained reviewer scripts merely to rebuild links.

Player version: the game findings are unchanged. Their reports now include the
files needed to follow the supporting evidence, and future preparation catches
the same omission before publication. No game or PC-control session was started.
