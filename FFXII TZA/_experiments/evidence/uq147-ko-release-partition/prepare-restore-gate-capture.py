"""Reuse the same checked body-capture procedure for the connecting gate."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
p=P/'capture-ko-release-boundary.py';raw=p.read_bytes()
if hashlib.sha256(raw).hexdigest()!='6375809a6b6465f574bd79d5bc1ed0aa360ebfee10c64aaec2d1dd39fd8b54d5':raise ValueError('Existing path changed')
lookup=P/'lookup-restore-gate-01.json';x=json.loads(lookup.read_text())
st=json.loads((P/'lookup-restore-gate-01.status.json').read_text())
if st.get('terminal') is not True or st.get('exit')!=0 or st.get('exception') is not None or x.get('complete') is not True or x.get('requested')!=['0x308270','0x3082e8'] or x.get('matches') or x.get('decision')!='NO_COVERING_MAP_IN_SEARCHED_CORPUS':raise ValueError('Selection prerequisite failed or retained map available')
s=raw.decode()
for a,b in [('Exact UQ147 earlier KO local release body','Connecting original bit22-gated action restore body'),('preview-ko-release-01','preview-restore-gate-01'),('lookup-ko-release-01.json','lookup-restore-gate-01.json'),('3573d5eef9848ae420f895b45d4a233140178dc1d8595d9480a7eb1dc3291919',hashlib.sha256(lookup.read_bytes()).hexdigest()),("['0x310780','0x310861']","['0x308270','0x3082e8']"),('for entry in [0x310780]:','for entry in [0x308270]:')]:
    if s.count(a)!=1:raise ValueError('Template boundary changed '+a)
    s=s.replace(a,b)
out=P/'capture-restore-gate-boundary.py'
with out.open('x',encoding='utf-8') as f:f.write(s)
print(json.dumps(dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),lookup_sha256=hashlib.sha256(lookup.read_bytes()).hexdigest())))
