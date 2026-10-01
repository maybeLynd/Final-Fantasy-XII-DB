import hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;records=[]
for name,c in [('migration-dashboard-incident','51660c616f8fec23c7ae140a721be58cc54c38cc'),('migration-dashboard-cache-r2','dcc53dc222912b31d05205e15037b85b38493367')]:
 E=Path('Database/FFXII TZA/_experiments/evidence')/name;mbytes=(E/'manifest.json').read_bytes();q=subprocess.run(['git','show',c+':'+(E/'manifest.json').as_posix()],capture_output=True);assert q.returncode==0 and q.stdout==mbytes
 m=json.loads(mbytes)
 for x in m['members']:
  b=(E/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
 raw=E/'raw.json';r=json.loads(raw.read_text()) if raw.exists() else {}
 records.append(dict(package=E.as_posix(),commit=c,manifest_sha256=hashlib.sha256(mbytes).hexdigest(),members_verified=len(m['members']),cases=[{'name':x.get('name'),'passed':x.get('passed')} for x in r.get('cases',[])],limit='Exact prior captured scope; no new experiment credit or currentdeployment acceptance'))
(W/'retained-coverage.json').write_text(json.dumps(records,indent=2)+'\n');print('RETAINED_TWO_PACKAGES_BYTE_VALIDATED_NO_RECAPTURE')
