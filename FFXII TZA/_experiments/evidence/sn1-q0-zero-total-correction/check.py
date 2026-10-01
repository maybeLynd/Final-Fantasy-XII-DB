import hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());p=Path(raw['parent'])
for n,key in [('manifest.json','parent_manifest_sha256'),('raw.json','parent_raw_sha256'),('result.json','parent_result_sha256'),('check.py','original_checker_sha256')]:assert sha((p/n).read_bytes())==raw[key]
actual=json.loads((p/'result.json').read_text());assert actual['coordinate_counts']['zero-line-convention-unresolved']==sum(raw['by_module'].values())==raw['actual_zero_total']==59 and raw['incorrect_text_total']==61
r=subprocess.run([sys.executable,str(W/'corrected60-check.py'),*sys.argv[1:]],capture_output=True,text=True,timeout=30)
sys.stdout.write(r.stdout);sys.stderr.write(r.stderr)
assert r.returncode==0,r.returncode
corrected=json.loads((W/'corrected-result.json').read_text());assert corrected['coordinate_counts']==actual['coordinate_counts'] and corrected['unresolved_physical_coordinates']==actual['unresolved_physical_coordinates'] and corrected['zero_suffixes']==actual['zero_suffixes']
assert 'All59 line0' in corrected['interpretation'] and '59 all-zero' in r.stdout
print('PASS62 additive original59 total, corrected derived producer; original raw/numeric/EOF+1/suffix findings unchanged',flush=True)
