# The two effect requests use different name-buffer addresses

For the player: loading an area can make two effect-file requests. They pass through the same code, but that does not mean they reuse exactly the same temporary name buffer. This source proof checks that assumption without loading the game.

**Method A / STATIC_ONLY, producer controls complete; independent acceptance pending.** Let S be the stack pointer on entry to331990. Its first mode0 request CALLs378A60 while its own40-byte stack frame is present; CALL adds another8 bytes. Before mode1,331990 restores that frame and tail-JMPs378A60. The wrapper itself pushes8/subtracts48, then CALLs377DC0. Under normal private-frame ABI and if each leg reaches this loader:

| address | mode0 relative to S | mode1 relative to S |
|---|---:|---:|
| 378A60 entry RSP | -48 | 0 |
| 377DC0 entry RSP | -112 | -64 |
| name input (loader entry−328) | -440 | -392 |

The second name input is **48 bytes above** the first. A same-address inheritance model is refuted at these boundaries. The admitted260-byte spans overlap by212 bytes; different buffers do not imply disjoint storage, and arithmetic overlap is not observation of surviving old bytes.

This proof captures only two previously uncovered complete bodies:331990..3319C4 (52bytes) and378A60..378B71 (273bytes), using original physical PE/unwind records and the shared reviewed access-role adapter. The loader's−328 input offset is consumed from the already SPEC-accepted SD194 packet; its builder and field census are not rerun. Every CFG path's stack delta is accounted for. Actual decoded register effects identify all RSP writers; an empty/nonexistent regs_write field is not used as a guard. CALLs are modeled by **normal return restores RSP**, not by absence of native effects.

The wrapper can skip mode0 and has other gates and opaque helpers. Thus reaching both377DC0 calls is an explicit premise. Other intervening calls and former stack use can overwrite the overlapping region. No current filename, actual inherited bytes, natural field entry, resource scheduling, request acceptance, allocator/lifetime or visible consequence is established.

Reference EXE SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000. Full caller body hashes f53af247e513ecc2fd4d39798d3a52fd375e4a4fa777982c90ff54f4ae1771ce and86831f5483b73fd348be8482c65cd86363f4082711c07a5f9dd0b633807f8ea2 are pinned in the current producer. Metadata completion, wrapper identity, actual upstream terminal/exit/exception, raw bytes and reviewed annotations are required. Three actual CLI controls reject an upstream failure, incomplete metadata and a coherent same-size stack SUB change. These are producer tests, not original-code or game executions.

Current result02/producerbe8c4760 and controller7ae4714b govern. Original result01/driver preimage remains immutable; the additive version strengthens full-body identity and packages the retained source for portability. It does not add another scientific sample. The same-size change alters source and metadata consistently and is still rejected against shipping bytes.

Consumers DATA/OPUS should remove same-address inheritance assumptions and make future read collectors derive the input from each377DC0 entry. Keep SD194 inherited contents/reachability OPEN. Independent SPEC review is required; package integrity and controls alone are not semantic acceptance.

Reproduce the reducer with the repository interpreter: python -B prove.py <fresh-result>. Controls require the retained current positive and a fresh directory. Missing prerequisites are invalid, never empty successes. No game/PC/native/emulator/instrument/save/config/reference or peer process changed; own helper children exited. Goal ACTIVE/NOT_MET; menu extension unapproved and spent budget persists; EXP127 remains invalid.
