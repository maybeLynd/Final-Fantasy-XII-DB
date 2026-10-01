# Save's count gate is zero, not signed-positive

**A / static original code, bounded conditional prefix.** Original Save89B at `0036D930`, SHA `ebabe24f…`, reference image `73461d08…21f8`. Exact source/parent manifest/canonical consumer preimage retained. No FF12/emulator/native code was executed.

Original `TEST ECX,ECX` at `0036D948`, `JE` at `0036D94A` skips to the depth store only when the low32 count bits are zero. Nonzero enters the loop. `MOV R10D,ECX` at `0036D950` zero-extends the raw32 bits into R10, then `SUB R10,1`/`JNE` at `0036D97C`/`0036D980` controls the unchecked countdown. This is not a signed `count > 0` gate.

For zero, the snapshot loop is skipped and depth still assigned zero. One enters with R10=1 and its first decrement produces0. `80000000` and `FFFFFFFF` enter with R10=2147483648 and4294967295, respectively. Their first decrement is computed in64bit R10. In contrast, the contract §11 illustration `for (int i=0; i<count; i++)` performs zero iterations for a negative signed interpretation of those same bits.

The result records these source-level prefixes, not an enormous loop run. A disposable source-obligation control changes the zero JE into signed JLE at the same TEST gate and is rejected; it directly tests the competing signed interpretation. No reference binary is modified.

**Implication:** the signed pseudocode is a sketch on the valid count domain, not a literal model of native invalid-count behavior. The existing structural safe boundary (32, unenforced) remains in force. Consumers can state raw zero/nonzero/zero-extension behavior and its validity precondition; do not infer the original C parameter's declared signedness from this generated code. No guarantee of whole-loop completion, fault onset, memory safety or handling of arbitrary malformed inputs is established. Argument/array accesses can fail or interfere long before a nominal countdown ends. No normal caller is claimed to supply these counts.

Consumer: OPUS ABI/procedure and SWE2-CONTRACT `CONTRACT-transform-workbench-save-restore.md` §11/interface. This is independent of the already answered32item layout and EXP070 disabled-mode results, and distinct from the preceding pointer-record alias. No peer source or ordinary S05 fixture modified. Independent review and canonical consumer agreement remain pending.

Byte delivery follows the existing evidence `* -text` policy, tested against actual Git filtered/unfiltered blobs. Read-only check.py validates original byte anchors and retained conditional prefixes, not native effects. PC OFF; no processes/instruments/input/save/config/reference changes. S19 consumed two attempts/ten minutes, extra recovery unapproved; bounded live authorization remains active. Full L1+L2/final audit NOT_MET.
