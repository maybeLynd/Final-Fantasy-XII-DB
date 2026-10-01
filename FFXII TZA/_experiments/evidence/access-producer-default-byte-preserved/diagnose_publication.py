import hashlib,json,re,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;pub=W/'publication';pkg='Database/FFXII TZA/_experiments/evidence/access-producer-default'
sha=lambda b:hashlib.sha256(b).hexdigest()
log=(pub/'publish-output.txt').read_text();match=re.search(r'--- committed ---\s*\n([0-9a-f]{7,40})\s',log);assert match
c=subprocess.check_output(['git','rev-parse',match.group(1)],text=True).strip()
m=json.loads(subprocess.check_output(['git','show',c+':'+pkg+'/manifest.json']))
rows=[]
for x in m['members']:
 disk=(Path(pkg)/x['path']).read_bytes();committed=subprocess.check_output(['git','show',c+':'+pkg+'/'+x['path']])
 assert len(disk)==x['bytes'] and sha(disk)==x['sha256'],'Lost original disk preimage: '+x['path']
 rows.append(dict(path=x['path'],manifest_bytes=x['bytes'],manifest_sha256=x['sha256'],committed_bytes=len(committed),committed_sha256=sha(committed),matches=committed==disk,only_crlf_to_lf=committed==disk.replace(b'\r\n',b'\n')))
r=dict(commit=c,verdict='INVALID_CANONICAL_MANIFEST_BYTES',rows=rows,changed=[x['path'] for x in rows if not x['matches']],cause='Determine from exact byte comparison; only_crlf_to_lf per row is tested, not assumed',limits='Does not invalidate retained actual producer control result; canonical manifest integrity cannot pass. Do not rerun settled controls or republish actual commit.')
(W/'publication-failure.json').write_text(json.dumps(r,indent=2)+'\n')
print(c);print('MISMATCHES',[(x['path'],x['only_crlf_to_lf']) for x in rows if not x['matches']])
