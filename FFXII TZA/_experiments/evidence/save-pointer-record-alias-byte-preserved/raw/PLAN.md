# Save's pointer record can alter its own source

Question: does Save's snapshot mean entry-state target bytes, or target bytes after earlier bookkeeping writes? H1: target bytes are loaded before writing their pointer record. H2: pointer record is stored first and can overlap the target.

Method A is sufficient: exact retained shipping 89-byte Save and 66-byte Restore are call-free. `0036D969` pointer store precedes `0036D974` target load, so controlled source-level byte transfers discriminate without another isolated run. Consumer: OPUS/SWE2-CONTRACT save/restore preconditions and FABLE workbench explanation. This is distinct from ORACLE's ordinary S05 pair execution and the earlier depth-counter loop-bound alias.

State/controls: count1, initial depth0, valid mapped pointer/value/target ranges, no counter overlap or outside interference. Target=pointer slot02EC0A00; disjoint target positive; target=value slot02EC0800 self-copy negative. Compare target bytes at entry, captured bytes and bytes after immediate Restore. Verify actual record-store/target-load ordering and exact bodies before interpreting conditional examples. Do not infer an ordinary caller uses this target, general alias safety, live initialization or scheduling.

Stop on source identity/extent/operand mismatch, missing controls, or unexplained byte transfer. Evidence: dependency pins and raw source, conditional observations, source obligation checker and retained canonical preimage. Protect published24/28, no reference/save/config/game changes. PC OFF, S19 spent budget unchanged. Claim only this new edge and own files; canonical consumers stay peer-owned.
