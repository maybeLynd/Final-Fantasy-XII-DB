"""Configure existing bounded shipping capture, adding three exact branch tables."""
import hashlib,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
t=P/'capture-mode-query-boundary.py'
if hashlib.sha256(t.read_bytes()).hexdigest()!='05173bedcdc789bdfa04524460d77967f95ad31aefe04d453ff2186f68c32008':raise ValueError('Template changed')
s=t.read_text()
replacements=[
 ('Closed field-mode query targets; original bytes only, not initialized gameplay.','Complete special presentation/initializer bodies and exact branch tables; STATIC_ONLY.'),
 ("['preview-field-mode-01','preview-field-id-01']","['preview-special-presentation-01','preview-special-init-01']"),
 ("[('lookup-mode-field-mode-01',['0x377c20','0x377c6e']),('lookup-mode-field-id-01',['0x3148f0','0x31490b']),('lookup-mode-payload-access-01',['0x2ef2b0','0x2ef2c4']),('lookup-mode-image-access-01',['0x2ef640','0x2ef648'])]","[('lookup-special-presentation-01',['0x306760','0x306aef']),('lookup-special-init-01',['0x306bd0','0x306cec'])]"),
 ('[0x377c20,0x3148f0,0x2ef2b0,0x2ef640]','[0x306760,0x306bd0]'),
 ('Three .pdata-bounded mode-query helper bodies and one declared direct-target leaf span without .pdata root. Consumer must verify complete CFG/RET and address composition. Read-only physical capture, not initialized image/field table, naturally reachable mode1/KO, lifetime or gameplay scheduling. No native/emulator/live execution.','Two complete .pdata-bounded bodies and raw physical branch tables. Qualify branch/table and guarded effects/order separately; no natural KO, initialized owner/resource, live scheduling/presentation or transitive helper-effects proof. No native/emulator/live execution.')]
for a,b in replacements:
 if s.count(a)!=1:raise ValueError('Ambiguous template replacement')
 s=s.replace(a,b)
old="    out.write_text(json.dumps(x,indent=2)+'\\n')"
new="""    tables=[]
    for address,n in [(0x306af0,24),(0x306cec,28),(0x306d08,128)]:
        z=read(address,n)
        tables.append(dict(address=hex(address),bytes=n,physical_bytes=z.hex(),sha256=hashlib.sha256(z).hexdigest(),method='Original file-backed raw table, not decoded instructions or observed process state'))
    x['physical_tables']=tables
    out.write_text(json.dumps(x,indent=2)+'\\n')"""
if s.count(old)!=1:raise ValueError('Output site changed')
s=s.replace(old,new)
q=P/'capture-dismiss-stage-boundary.py'
with q.open('x') as f:f.write(s)
(P/'DISMISS-STAGE-QUESTION.md').write_text('''# Dismiss local stage ordering

Exact question: does the original kind2/Dismiss arm clear battle-mode bit0 before this routine publishes special-sequence state5, or only in later finishing states6/7? Canonical mode-ladder section2c says "when the sequence ends"; do not equate the code label with observed screen timing.

MethodA sufficient: full306BD0 and306760 shipping bodies/.pdata, physical kind/index jump tables, connected original memory roles and exact conditional order. No live/native/emulator execution. Match action113 via ORIGINAL initializer classification, not ActionDefinition+34 (text name). The earlier erroneous naming/handler plan is retained and corrected before any capture or consumer claim used it.

Controls: exact original image/tool/adapter, completed upstream capture/body/table identities, positive kind1/other-arm separation; source/table and selected write-order mutation detectors. Acceptance: conditional direct mode-clear before the same normal path's later direct state5 write, with opaque earlier/later helpers explicitly not summarized. Not first-ever state5, natural execution, resource success, lifetime, actual presentation, or wholeUQ147 closure. Invalidation: unbound dispatch/table, malformed metadata, unknown selected transfer, failed prerequisite or inconsistent bytes/roles.

Consumers: FABLE battle-runtime-mode-ladder and capability UQ147; OPUS existing mode/command/special-sequence contracts. No peer page edit, no duplicate naming census or EXP198/S20 controls. Stop a settled local discriminator and preserve the native/natural scheduling remainder.
''')
print(hashlib.sha256(q.read_bytes()).hexdigest())
