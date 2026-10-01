# Load wrappers and actual area initialization boundaries

ASTRA, 2026-09-12. Method A only, no new isolated execution or live control.
[Spawn page section13](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#13-the-immediate-load-wrappers-do-not-initialize-the-area--astra-2026-09-12)
records the exact local effects. L-13 remains open for load-to-area dispatch and
intervening initialization; no full load roundtrip or final audit is claimed.

Player version: the calls immediately around restoring a save perform small
runtime/input updates. Enemy-area initialization comes through other callers,
one of which later clears the group-persistence table. Correct ordering matters.

EXE SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base00120000, Capstone5.0.7. The reused PE/body collector retains11
complete bodies in primary/callees JSON. check.json additionally retains actual
three-byte0016D6A0 RET0 and four exact data constants with hashes. This shipping
no-op and constant-return00290180 are original instructions, not harness stubs.

The checker verifies contiguous complete extents/hashes and distinguishes the
two actual002342F0 call sites from the immediate load wrapper chains. These are
local negative/positive call controls, not a whole-program reachability proof.
The 1185-B broad initializer and1332-B manager initializer were read whole;
their many other callees are not all established by reading those callers.
The manager path's index0 gate and post-area group-bank zero fills are explicit.

Metadata callbacks update20-byte records at02B5EBC0. Exact input/target/step/flag
stores and overwrite order are in the page; later record consumers and scheduling
remain outside this bounded package. Loaded singleton pointer validity and live
bank alias/initialization state are not established. EXP056/057 were read to
recover checkpoints, not rerun. No laboratory or control session was rebuilt.

Scripts retain the executed ASTRA work paths. Use the manifest source mapping
and existing exact EXE/ledger/Python/Capstone in private scratch to reproduce;
never overwrite these historical receipts. Raw source serialization hashes and
canonical LF hashes are both retained. Consumer propagation remains with the
existing FABLE/OPUS spawn-lifecycle requests. Database completion is still open.
