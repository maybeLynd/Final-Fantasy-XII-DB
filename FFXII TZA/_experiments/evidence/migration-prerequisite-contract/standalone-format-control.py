import hashlib,json,re,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;r=json.loads((W/'run-01/raw.json').read_text());case=next(x for x in r['cases'] if x['name']=='custom-tab-fail');p=W/'run-01/custom-tab-fail/upstream.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()==case['upstream_sha256']
z=subprocess.run([r['child_executable'],'-B',str(p)],capture_output=True,text=True,timeout=5)
lines=z.stdout.splitlines();assert z.returncode==0 and lines==['FAIL\tA\trequired failure','FAILS 0']
match=re.compile(r'^(PASS|FAIL)\t(\S+)(?:\t|$)').match(lines[0]);assert match and match.group(1)=='FAIL' and match.group(2)=='A'
receipt=dict(input_sha256=case['upstream_sha256'],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr,matched_verdict=match.group(1),matched_tag=match.group(2),literal_space_prefix=lines[0].startswith('FAIL '),composer_stdout=case['stdout'],composer_returncode=case['returncode'])
(W/'standalone-format-control.json').write_text(json.dumps(receipt,indent=2)+'\n');print('RECOGNIZED_FAIL_accepted_by_composer',case['actually_accepted'])
