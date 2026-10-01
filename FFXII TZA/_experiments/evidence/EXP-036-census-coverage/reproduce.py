"""Independent input-coverage fixtures; never modifies the shared tool or store."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[3]/'Tools/analysis-kit/gfz-scripts/check_census_widths.py'
raw=SOURCE.read_bytes()
assert not (HERE/'checker-snapshot.py').exists()
(HERE/'checker-snapshot.py').write_bytes(raw)
names=['save-header','save-payload','battle-unit','actor-storage-record','actor-manager-record',
       'battle-stats-record','battle-state-block','result-record']
results=[]
for mode in ['matching','mismatch','missing_census','malformed_rows','no_declared_fields']:
    with tempfile.TemporaryDirectory(prefix='astra-census-coverage-') as tmp:
        root=Path(tmp);db=root/'Database/FFXII TZA';(db/'_types').mkdir(parents=True)
        fields='type\toffset\tsize\tname\tctype\tdescription\treadiness\tconfidence\tevidence\n'
        if mode!='no_declared_fields':
            fields+='BattleUnit\t0x100\t%d\ttestField\tuint32\tfixture\tTEST\tTEST\tfixture\n'%(1 if mode=='mismatch' else 4)
        (db/'_types/fields.tsv').write_text(fields)
        for name in names:
            if mode=='missing_census' and name=='battle-unit':continue
            text='function\taddress\tmode\toffset\twidth\tinstruction\n'
            if name=='battle-unit':
                text+=('invalid\n' if mode=='malformed_rows' else
                       '00100000\t00100004\tread\t0x100\t4\tmov eax, dword ptr [rcx + 0x100]\n')
            (db/(name+'-accesses.tsv')).write_text(text)
        run=subprocess.run([sys.executable,str(HERE/'checker-snapshot.py')],cwd=root,capture_output=True,text=True)
        results.append(dict(case=mode,declared_fields=0 if mode=='no_declared_fields' else 1,
                            exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))
assert results[0]['exit_code']==0 and results[1]['exit_code']==1
assert 'MISMATCH BattleUnit' in results[1]['stdout']
assert all(r['exit_code']==0 for r in results[2:]),'candidate behavior changed; inspect evidence'
assert SOURCE.read_bytes()==raw,'source changed during review'
(HERE/'result.json').write_text(json.dumps(dict(status='REPRODUCED',scope='synthetic checker input coverage',
 source_path=str(SOURCE),source_sha256=hashlib.sha256(raw).hexdigest(),
 harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=results),indent=2)+'\n')
files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in HERE.iterdir() if p.is_file() and p.name!='manifest.json'}
(HERE/'manifest.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print([(r['case'],r['exit_code']) for r in results])
