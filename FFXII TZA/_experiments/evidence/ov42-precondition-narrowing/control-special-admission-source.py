"""Exercise the actual repaired default CLI and demonstrate its old blind spots.

Only labelled synthetic input mutations. Retained tables are reused unchanged;
this is an affected producer regression check, not a new archive census.
"""
import copy, hashlib, json, pathlib, subprocess, sys
W=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv,c,stem):
    z=subprocess.run(argv,capture_output=True,timeout=45)
    (c/(stem+'.stdout')).write_bytes(z.stdout);(c/(stem+'.stderr')).write_bytes(z.stderr)
    r={'argv':argv,'exit':z.returncode,'terminal':True,'stdout_sha256':sha(c/(stem+'.stdout')),'stderr_sha256':sha(c/(stem+'.stderr'))}
    (c/(stem+'.status.json')).write_text(json.dumps(r,indent=2)+'\n')
    return z,r
def main():
    out=pathlib.Path(sys.argv[1]);out.mkdir();rows=[]
    rawpath=W/'special-admission-raw-01.json';base=json.loads(rawpath.read_text())
    receipt=W/'action-selectors-01/result.json';tables=W/'action-selectors-01/tables'
    for tag,error,old_pass in [
      ('bytes-with-stale-text','decoded annotation disagrees with bytes',True),
      ('coherent-kind5','retained source differs from shipping bytes',True),
      ('coherent-mode-range-reversal','retained source differs from shipping bytes',True),
      ('failed-role-control','upstream roles invalid',False),
      ('wrong-reference-image','shipping image identity mismatch',False)]:
        c=out/tag;c.mkdir();raw=copy.deepcopy(base)
        if tag in {'bytes-with-stale-text','coherent-kind5'}:
            q=next(q for q in raw['ranges'] if q['start']=='0x306bd0');i=next(i for i in q['instructions'] if i['pc']=='0x306c0a')
            if i['bytes']!='bb03000000':raise ValueError('kind-control preimage changed')
            i['bytes']='bb05000000'
            if tag=='coherent-kind5':i['args']='ebx, 5'
            q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        if tag=='coherent-mode-range-reversal':
            q=next(q for q in raw['ranges'] if q['start']=='0x30ce10');i=next(i for i in q['instructions'] if i['pc']=='0x30cefe')
            if i['bytes']!='7631':raise ValueError('mode-control preimage changed')
            i.update(bytes='7731',mnemonic='ja');q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        if tag=='failed-role-control':raw['controls'][0]['observed']='r'
        raw['synthetic_fixture']='Intentional invalid source/control, not shipping/native/live evidence'
        p=c/'raw.json';p.write_text(json.dumps(raw,indent=2)+'\n')
        common=[str(p),str(receipt),str(tables)]
        old=None
        if old_pass:
            oldout=c/'old-synthetic-result.json';z,old=run([sys.executable,str(W/'check-special-admission-before-returned-review-1001.py'),*common,str(oldout)],c,'old')
            if z.returncode!=0 or not oldout.is_file():raise ValueError('old blind spot not reproduced '+tag)
            old['result_sha256']=sha(oldout)
        result=c/'invalid-result.json';argv=[sys.executable,str(W/'check-special-admission.py'),*common,str(result)]
        if tag=='wrong-reference-image':
            ep=c/'invalid-exe.bin';ep.write_bytes(b'Labelled non-image fixture, never a modified reference EXE');argv+=['--exe',str(ep)]
        z,status=run(argv,c,'fixed')
        row={'case':tag,'expected_error':error,'expected_error_seen':error.encode() in z.stderr,'result_absent':not result.exists(),'fixed_invocation':status,'old_acceptance':old}
        if z.returncode==0 or not row['expected_error_seen'] or not row['result_absent']:raise ValueError('nondiscriminating/incomplete control '+tag)
        rows.append(row)
    report={'status':'PASS_FIVE_ACTUAL_DEFAULT_CLI_REFUSALS_THREE_OLD_FALSE_ACCEPTANCES','cases':rows,'driver_sha256':sha(pathlib.Path(__file__)),'checker_sha256':sha(W/'check-special-admission.py'),'source_gate_sha256':sha(W/'qualify-special-admission-source.py'),'native_runs':0,'live_runs':0,'limits':'Synthetic mutation controls through actual default invocation. Three old outputs demonstrate invalid acceptance only; not valid original source conclusions. Review independent acceptance remains pending.'}
    (out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print('Actual default checker: five refusals, three old false acceptances reproduced; no invalid fixed result')
if __name__=='__main__':main()
