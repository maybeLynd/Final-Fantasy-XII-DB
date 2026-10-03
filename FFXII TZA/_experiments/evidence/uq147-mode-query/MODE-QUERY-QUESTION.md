# UQ147 local mode-query and Dismiss early-return discriminator

Question: does calling3138D0(0) necessarily clear battle mode1 before the same-call23B040 recomputation? Competing explanations: unconditional cleanup/reset versus a closed no-cleanup early-return path. This is a local implementation proposition, separate from naturally initialized KO reachability.

Known: original300FC0 conditionally calls3138D0(0) then23B040;3138D0 has NULL roster-unit and pending/committed113 early returns. Selector31B8C0/263750/263E30 is already closed/read-only. Mode getter30D9A0 has one377C20 helper; effects of that helper chain were not previously qualified. Do not replay selector/EXP198/S20.

MethodA is sufficient to determine the complete helper writes and branch prerequisites. Close377C20->3148F0->2EF2B0->2EF640 from exact shipping bytes, then compose only validated early-return boundaries. Existing-source search in the named corpus found no covering qualified map for these four spans; it is not global absence. Reuse reviewed role adapter/capture and physical metadata.

Controls: original-byte/current-role/extent/terminal prerequisites, specific helper-call/memory-field mutations and known-positive Dismiss request path with writes. Acceptance: exact effects/order and a conditional branch counterexample under explicit readable-state/private-stack/normalABI/noninterference conditions. No natural reachability, full lifecycle or live-state closure from constructed premises. Invalidation: incomplete body, unresolved transfer, bad annotation/source identity or failed upstream status. No game, save/config/reference or peer-process writes. FABLE capability UQ147 and OPUS command seam are the canonical consumers.
