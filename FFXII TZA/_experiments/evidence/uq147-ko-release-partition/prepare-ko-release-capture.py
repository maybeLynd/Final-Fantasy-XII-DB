"""Configure one bounded target using the existing checked metadata/capture path."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
source=P/'capture-defeat-boundary.py';raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='e318100b6f9582028bbdd4206d4c8643f351b270841b3a8a924d070b824be784':raise ValueError('Original template changed')
lookup=P/'lookup-ko-release-01.json'
if hashlib.sha256(lookup.read_bytes()).hexdigest()!='3573d5eef9848ae420f895b45d4a233140178dc1d8595d9480a7eb1dc3291919':raise ValueError('Lookup changed')
x=json.loads(lookup.read_text())
if x.get('complete') is not True or x.get('requested')!=['0x310780','0x310861'] or x.get('decision')!='NO_COVERING_MAP_IN_SEARCHED_CORPUS' or x.get('matches'):raise ValueError('Consume existing source instead')
s=raw.decode()
def replace(a,b):
    global s
    if s.count(a)!=1:raise ValueError('Template boundary changed')
    s=s.replace(a,b)
replace('Exact UQ147 defeat/recompute boundary and designated-unit lookup, STATIC_ONLY.','Exact UQ147 earlier KO local release body, STATIC_ONLY; transitive effects open.')
replace("['preview-defeat-01','preview-combatant-lookup-01']","['preview-ko-release-01']")
start=s.index("    for tag,wanted in ")
end=s.index("    raw=EXE.read_bytes()",start)
old=s[start:end]
replace(old,"    lookup=P/'lookup-ko-release-01.json'\n    if sha(lookup)!='3573d5eef9848ae420f895b45d4a233140178dc1d8595d9480a7eb1dc3291919':raise ValueError('lookup changed')\n    x=json.loads(lookup.read_text())\n    if x.get('complete') is not True or x.get('requested')!=['0x310780','0x310861'] or x.get('exe_sha256')!=PIN or x.get('matches') or x.get('decision')!='NO_COVERING_MAP_IN_SEARCHED_CORPUS':raise ValueError('lookup incomplete or retained evidence available')\n")
replace('for entry in [0x300fc0,0x31b770]:','for entry in [0x310780]:')
replace('Complete local shipping bodies and actual reviewed role controls, not callee effects, command acceptance, cleanup timing, natural state/reachability or presentation. Current exact previews are feasibility only. Retained native fixtures disclose scripted recompute; this source capture is not their rerun or natural KO reachability.','Complete original local body and reviewed store/LEA/RMW role controls; not transitive callee effects, command acceptance, natural KO, lifetime or timing. Preview/lookup only enable selection. No native/game execution or old fixture rerun.')
out=P/'capture-ko-release-boundary.py'
with out.open('x',encoding='utf-8') as f:f.write(s)
print(json.dumps(dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),reused_template_sha256=hashlib.sha256(raw).hexdigest())))
