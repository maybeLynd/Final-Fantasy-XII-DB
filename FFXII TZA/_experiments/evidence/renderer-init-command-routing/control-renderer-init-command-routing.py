"""Actual scoped producer CLI refusals; synthetic fixtures, no native runs."""
import copy,hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=pathlib.Path(sys.argv[1]);out.mkdir();rows=[]
 base=json.loads((W/'renderer-init-command-routing-source-02.json').read_text())
 initial=json.loads((W/'renderer-init-command-routing-capture-02.status.json').read_text())
 for tag,error in [('failed-upstream','upstream capture failed or missing exit'),
   ('reversed-null-branch','source operation mismatch 0x1a1877'),
   ('missing-getter','retained getter prerequisite incomplete'),
   ('changed-prepare-slot','physical prepare-slot identity changed')]:
  c=out/tag;c.mkdir();raw=copy.deepcopy(base);st=copy.deepcopy(initial)
  if tag=='failed-upstream':st['exit']=1
  if tag=='reversed-null-branch':
   q=next(q for q in raw['ranges'] if q['start']=='0x1a1850');i=next(i for i in q['instructions'] if i['pc']=='0x1a1877')
   if i['bytes']!='7467':raise ValueError('branch mutation preimage changed')
   i.update(bytes='7567',mnemonic='jne');q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
  if tag=='changed-prepare-slot':
   t=raw['physical_table'];t['slots'][0]='0x1f16a0';t['bytes']='a0161f0000000000a0161f0000000000';t['sha256']=hashlib.sha256(bytes.fromhex(t['bytes'])).hexdigest()
  raw['synthetic_fixture']='Intentionally invalid reducer input, not original/native/live evidence'
  p=c/'renderer-init-command-routing-source-02.json';p.write_text(json.dumps(raw,indent=2)+'\n');st['source_sha256']=sha(p)
  status=c/'capture-status.json';status.write_text(json.dumps(st,indent=2)+'\n')
  for f in ['capture-renderer-init-command-routing.py','renderer-queue-initialization-source-02.json']:shutil.copyfile(W/f,c/f)
  g=json.loads((W/'title-cleanup-callback-queue-source-01.json').read_text())
  if tag=='missing-getter':g['ranges']=[q for q in g['ranges'] if q['start']!='0x189120']
  (c/'title-cleanup-callback-queue-source-01.json').write_text(json.dumps(g,indent=2)+'\n')
  result=c/'result.json';argv=[sys.executable,str(W/'prove-renderer-init-command-routing.py'),str(c),str(status),str(result)]
  z=subprocess.run(argv,capture_output=True,timeout=45);(c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
  r=dict(case=tag,argv=argv,exit=z.returncode,expected_error=error,expected_error_seen=error.encode() in z.stderr,result_absent=not result.exists(),checker_sha256=sha(W/'prove-renderer-init-command-routing.py'))
  (c/'status.json').write_text(json.dumps(r,indent=2)+'\n')
  if not z.returncode or not r['expected_error_seen'] or not r['result_absent']:raise ValueError('invalid/empty/nondiscriminating refusal '+tag)
  rows.append(r)
 (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_FOUR_ROUTING_REFUSALS_INDEPENDENT_PENDING',cases=rows,limits='Synthetic inputs exercised actual producer CLI, not original execution or independent acceptance'),indent=2)+'\n')
 print('Four actual prerequisite/branch/getter/prepare-identity refusals; invalid result absent')
if __name__=='__main__':main()
