"""Actual selected producer refusals; synthetic copied canonical inputs."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
def main():
 out=pathlib.Path(sys.argv[1]);out.mkdir();rows=[]
 for tag,error in [('failed-prerequisite','retained producer prerequisite failed/missing'),
  ('wrong-store-role','actual retained memory-role mismatch'),
  ('changed-mask','original shift/mask/store sequence changed'),
  ('missing-class-gate','missing class gate input')]:
  c=out/tag;shutil.copytree(W/'flag-class-mask-input-01',c)
  if tag=='failed-prerequisite':
   p=c/'checks-effects-terminal.json';r=json.loads(p.read_text());next(x for x in r if x['case']=='positive')['returncode']=1;p.write_text(json.dumps(r,indent=2)+'\n')
  if tag in ['wrong-store-role','changed-mask']:
   p=c/'raw-object-state.json';r=json.loads(p.read_text());f=next(f for f in r['callees'] if f['entry']=='0x3e33e0')
   if tag=='wrong-store-role':next(i for i in f['instructions'] if i['pc']=='0x3e33f2')['memory'][0]['kind']='r'
   else:
    i=next(i for i in f['instructions'] if i['pc']=='0x3e33e8')
    if i['bytes']!='2500008000':raise ValueError('mask mutation preimage changed')
    i.update(bytes='2500000020',args='eax, 0x20000000')
    b=bytes.fromhex(''.join(i['bytes'] for i in f['instructions']));(c/f['code_file']).write_bytes(b);f['code_sha256']=hashlib.sha256(b).hexdigest()
   p.write_text(json.dumps(r,indent=2)+'\n')
  if tag=='missing-class-gate':
   p=c/'raw-position-effects.json';r=json.loads(p.read_text());r['callees']=[f for f in r['callees'] if f['entry']!='0x2e6000'];p.write_text(json.dumps(r,indent=2)+'\n')
  # Original input-manifest is retained to show the synthetic divergence; it
  # is not asserted to describe these deliberately invalid copies.
  result=c/'result.json';argv=[sys.executable,'-B',str(W/'prove-flag-class-mask.py'),str(c),str(result)]
  z=subprocess.run(argv,capture_output=True,timeout=45);(c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
  r=dict(case=tag,argv=argv,exit=z.returncode,expected_error=error,expected_error_seen=error.encode() in z.stderr,result_absent=not result.exists(),checker_sha256=hashlib.sha256((W/'prove-flag-class-mask.py').read_bytes()).hexdigest())
  (c/'status.json').write_text(json.dumps(r,indent=2)+'\n')
  if not z.returncode or not r['expected_error_seen'] or not r['result_absent']:raise ValueError('invalid/zero-case/nondiscriminating control '+tag)
  rows.append(r)
 (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_FOUR_FLAG_CLASS_REFUSALS_INDEPENDENT_PENDING',cases=rows,limits='Synthetic source/receipt defects through actual producer CLI; not native executions, original-source bit counts or independent acceptance'),indent=2)+'\n')
 print('Four actual prerequisite/store-role/mask/gate refusals; no invalid semantic result')
if __name__=='__main__':main()
