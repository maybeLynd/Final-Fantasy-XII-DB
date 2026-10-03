"""Configure the existing bounded capture for four specific mode-query targets."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
template=P/'capture-dismiss-selector-boundary.py'
if hashlib.sha256(template.read_bytes()).hexdigest()!='4dde5e091a8c95718fc21f2003718552bc7c241faf7e2dcabd61205b7ae70737':raise ValueError('Capture procedure preimage changed')
out=P/'capture-mode-query-boundary.py'
if out.exists():raise ValueError('Fresh producer required')
s=template.read_text()
changes=[
 ('"""Exact Dismiss roster-slot selector and two closed leaf spans, STATIC_ONLY."""','"""Closed field-mode query targets; original bytes only, not initialized gameplay."""'),
 ("['preview-class3-lookup-01','preview-class3-object-01','preview-unit-reader-01']","['preview-field-mode-01','preview-field-id-01']"),
 ("[('lookup-class3-lookup-01',['0x31b8c0','0x31b8df']),('lookup-index-table-01',['0x263750','0x263767']),('lookup-actor-unit-leaf-01',['0x263e30','0x263e35'])]","[('lookup-mode-field-mode-01',['0x377c20','0x377c6e']),('lookup-mode-field-id-01',['0x3148f0','0x31490b']),('lookup-mode-payload-access-01',['0x2ef2b0','0x2ef2c4']),('lookup-mode-image-access-01',['0x2ef640','0x2ef648'])]"),
 ('[0x31b8c0,0x263750,0x263e30]','[0x377c20,0x3148f0,0x2ef2b0,0x2ef640]'),
 ('{0x263750,0x263e30}','{0x2ef640}'),
 ('{0x263750:0x263767,0x263e30:0x263e35}','{0x2ef640:0x2ef648}'),
 ('One .pdata-bounded selector and two declared direct-target leaf spans without .pdata roots. Consumer must verify their complete local CFG/RET closure. Preview labels class3 refer to roster slot index3, NOT ActorStorage class3. Physical bytes/reviewed roles, not initialized roster, KO admission, lifetime, gameplay scheduling or presentation. No fixture/live rerun.','Three .pdata-bounded mode-query helper bodies and one declared direct-target leaf span without .pdata root. Consumer must verify complete CFG/RET and address composition. Read-only physical capture, not initialized image/field table, naturally reachable mode1/KO, lifetime or gameplay scheduling. No native/emulator/live execution.')]
for a,b in changes:
 if s.count(a)!=1:raise ValueError('Ambiguous configured procedure substitution '+a)
 s=s.replace(a,b)
out.write_text(s)
(P/'MODE-QUERY-QUESTION.md').write_text('''# UQ147 local mode-query and Dismiss early-return discriminator

Question: does calling3138D0(0) necessarily clear battle mode1 before the same-call23B040 recomputation? Competing explanations: unconditional cleanup/reset versus a closed no-cleanup early-return path. This is a local implementation proposition, separate from naturally initialized KO reachability.

Known: original300FC0 conditionally calls3138D0(0) then23B040;3138D0 has NULL roster-unit and pending/committed113 early returns. Selector31B8C0/263750/263E30 is already closed/read-only. Mode getter30D9A0 has one377C20 helper; effects of that helper chain were not previously qualified. Do not replay selector/EXP198/S20.

MethodA is sufficient to determine the complete helper writes and branch prerequisites. Close377C20->3148F0->2EF2B0->2EF640 from exact shipping bytes, then compose only validated early-return boundaries. Existing-source search in the named corpus found no covering qualified map for these four spans; it is not global absence. Reuse reviewed role adapter/capture and physical metadata.

Controls: original-byte/current-role/extent/terminal prerequisites, specific helper-call/memory-field mutations and known-positive Dismiss request path with writes. Acceptance: exact effects/order and a conditional branch counterexample under explicit readable-state/private-stack/normalABI/noninterference conditions. No natural reachability, full lifecycle or live-state closure from constructed premises. Invalidation: incomplete body, unresolved transfer, bad annotation/source identity or failed upstream status. No game, save/config/reference or peer-process writes. FABLE capability UQ147 and OPUS command seam are the canonical consumers.
''')
print(json.dumps(dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),method='Configure reused bounded original-byte capture; no execution of FF12 instructions')))
