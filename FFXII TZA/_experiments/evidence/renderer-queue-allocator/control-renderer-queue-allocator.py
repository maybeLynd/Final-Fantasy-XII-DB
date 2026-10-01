"""Focused actual CLI prerequisite/import/alignment refusals; synthetic inputs.

Retain the positive once. These controls are not FF12/native failure tests.
"""
import copy, hashlib, json, pathlib, shutil, subprocess, sys
W=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out=pathlib.Path(sys.argv[1]);out.mkdir()
    base=json.loads((W/'renderer-queue-allocator-source-01.json').read_text())
    receipt=json.loads((W/'renderer-queue-allocator-capture-01.status.json').read_text())
    rows=[]
    for tag,error in [('failed-upstream','upstream capture failed or missing exit'),
                      ('wrong-alignment','source operation mismatch 0x1edfc6'),
                      ('wrong-native-import','named import binding changed'),
                      ('missing-reserve-body','retained bank/reserve prerequisite incomplete')]:
        c=out/tag;c.mkdir()
        raw=copy.deepcopy(base);r=copy.deepcopy(receipt)
        if tag=='failed-upstream':r['exit']=1
        if tag=='wrong-alignment':
            q=next(q for q in raw['ranges'] if q['start']=='0x1edf80')
            i=next(i for i in q['instructions'] if i['pc']=='0x1edfc6')
            if i['bytes']!='ba10000000':raise ValueError('alignment mutation preimage moved')
            i.update(bytes='ba20000000',args='edx, 0x20')
            q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
        if tag=='wrong-native-import':
            e=next(e for e in raw['import_boundaries'] if e['iat']=='0x8c2b60')
            e['name']='free';e['hint']=24;e['name_bytes']='18006672656500'
            e['lookup_bytes']=e['original_iat_bytes']='80eecc0100000000'
        raw['synthetic_fixture']='Intentionally invalid bounded producer input; not shipping/native/live evidence'
        src=c/'renderer-queue-allocator-source-01.json';src.write_text(json.dumps(raw,indent=2)+'\n')
        r['source_sha256']=sha(src)
        st=c/'capture-status.json';st.write_text(json.dumps(r,indent=2)+'\n')
        for f in ['capture-renderer-queue-allocator.py','renderer-queue-allocator-external-contract-01.json']:
            shutil.copyfile(W/f,c/f)
        prior=json.loads((W/'renderer-queue-initialization-source-02.json').read_text())
        if tag=='missing-reserve-body':prior['ranges']=[q for q in prior['ranges'] if q['start']!='0x188640']
        (c/'renderer-queue-initialization-source-02.json').write_text(json.dumps(prior,indent=2)+'\n')
        result=c/'result.json';argv=[sys.executable,str(W/'prove-renderer-queue-allocator.py'),str(c),str(st),str(result)]
        z=subprocess.run(argv,capture_output=True,timeout=45)
        (c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
        row=dict(case=tag,argv=argv,exit=z.returncode,expected_error=error,
            expected_error_seen=error.encode() in z.stderr,result_absent=not result.exists(),
            checker_sha256=sha(W/'prove-renderer-queue-allocator.py'))
        (c/'status.json').write_text(json.dumps(row,indent=2)+'\n')
        if not z.returncode or not row['expected_error_seen'] or not row['result_absent']:
            raise ValueError('invalid/zero-case/nondiscriminating control '+tag)
        rows.append(row)
    (out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_FOUR_REFUSALS_INDEPENDENT_PENDING',
        cases=rows,limits='Synthetic inputs exercised actual reducer CLI; not original-code execution, native heap failure or independent acceptance'),indent=2)+'\n')
    print('Four actual specific refusals; failed prerequisites cannot emit a semantic result')

if __name__=='__main__':main()
