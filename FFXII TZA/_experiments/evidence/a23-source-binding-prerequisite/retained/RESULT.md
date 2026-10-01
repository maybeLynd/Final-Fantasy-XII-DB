# A23 prepared source lookup silently drops failed Git exits

Bounded source-level evidence, not deployed A23 acceptance or a full-release
false-PASS claim. FRONTIER owns the release capture and repair. One supported
board note at revision 40474 routed this finding into its existing delivery
task; no duplicate owner task or peer file edit was made.

The captured `a23-release/release.py` source hash is
`838d4882e545c353061888ba5d06eae76514f1a219a73fff400df51dc9948469`.
Its `headsha` function calls `git show` and `git log`, takes their stdout,
and never checks either exit status. AST extraction executes this exact
function with real Git, without invoking release.py's top level, server,
export or publication workflow. It is deliberately a function-level test.

The valid current repository/server.py control has both Git exits 0; its
returned digest agrees with a separately checked HEAD blob, and the returned
last commit is 40 characters. A confirmed nonexistent Git `-C` directory
produces exits **128 and 128**, with zero stdout bytes and retained error
text. Despite this actual upstream failure, the helper returns the normal
tuple `{SHA256(empty stdout), empty commit}`:
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, `""`.
There is no exit/failure status in its returned value.

This cannot justify a source-binding success. It also does **not** prove
that a real nonempty manifest matches this empty hash, that the complete
release verdict passes, or that its otherwise valid source binding is wrong.
The narrow defect is failure propagation at this lookup. FRONTIER should
check Git exits and required nonempty/blob identity before equality, retain
stderr/exit receipts, and test the actual failure path. ASTRA's own existing
source-identity helper already checks all Git return codes; do not build a
competing repair or erase the owner's current release evidence.

The initial peer-source invocation's driver/source/result/terminal are
preserved unchanged in `initial-peer-source-run/`. The final probe defaults
to the captured, hash-pinned source receipt and prints output only, so
reproduction does not overwrite published evidence or depend on the peer
keeping its defect. Both invocations have checked exit 0; the second changes
reproduction input handling, not the tested Git-failure conclusion.
Raw subprocess argv/exits/stdout sizes and hashes/stderr are in `result.json`.
The source and Python driver identities are pinned there. No mocked Git,
live FF12, instrumentation, save/config/reference or peer write occurred.
Independent acceptance and repair verification remain pending.
