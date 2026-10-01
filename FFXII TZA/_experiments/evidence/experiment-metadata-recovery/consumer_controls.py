"""Exercise the two existing readers on private fixtures; preserve canonical disagreements."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path('Database/FFXII TZA')
OUT = ROOT / '_experiments/evidence/experiment-metadata-recovery'
SCRIPTS = Path('Database/Tools/analysis-kit/gfz-scripts')
WORK = Path('Database/Tools/work/ASTRA').resolve()
fixture = WORK / ('metadata-reader-control-' + str(time.time_ns()))
assert fixture.parent == WORK
(fixture / '_experiments').mkdir(parents=True)
(fixture / '18-Audio').mkdir()
contract = fixture / '18-Audio/CONTRACT-field-music-selection.md'
record = fixture / '_experiments/EXP-001-control.md'
contract.write_text('# Private control\n\n## 13. Runtime validation\n\n**None**. EXP-001 is prepared only.\n', encoding='utf-8')
record.write_text('---\nexperiment: EXP-001\nstatus: PREPARED - private reader control\ncontract: ../18-Audio/CONTRACT-field-music-selection.md\n---\n\n# Control\n', encoding='utf-8')
results=[]


def run(script, *args, expected, contains):
    p = SCRIPTS / (script + '.py')
    cp = subprocess.run([sys.executable, str(p), *map(str, args)], text=True, encoding='utf-8', capture_output=True)
    results.append(dict(script=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                        arguments=list(map(str,args)), exit_code=cp.returncode, stdout=cp.stdout, stderr=cp.stderr))
    assert cp.returncode == expected, results[-1]
    assert all(s in cp.stdout for s in contains), results[-1]


run('check_experiments','--db',fixture, expected=0, contains=['experiments : 1'])
run('check_contract_runtime','--db',fixture, expected=0, contains=['records naming one by path 1','UNDERSTATED - section 13 denies validation a RAN record reports (0)'])
run('check_experiments','--db',fixture,'--control', expected=0, contains=['CONTROL: FOUND'])
dead=fixture/'_experiments/EXP-998-dead.md'
dead.write_text('---\nexperiment: EXP-998\nstatus: COMPLETE - private dead-link control\ncontract: ../18-Audio/CONTRACT-absent.md\n---\n',encoding='utf-8')
run('check_experiments','--db',fixture, expected=1, contains=['EXP-998-dead.md  ->  ../18-Audio/CONTRACT-absent.md'])
dead.unlink()
record.write_text(record.read_text(encoding='utf-8').replace('PREPARED - private reader control','COMPLETE - isolated original-code control'),encoding='utf-8')
run('check_contract_runtime','--db',fixture, expected=1, contains=['UNDERSTATED - section 13 denies validation a RAN record reports (1)','isolated original-code control'])

# Canonical runs are read-only. A nonzero disagreement is retained, not forced green.
for script in ('check_experiments','check_contract_runtime'):
    p=SCRIPTS/(script+'.py')
    cp=subprocess.run([sys.executable,str(p),'--db',str(ROOT)],text=True,encoding='utf-8',capture_output=True)
    assert cp.returncode in (0,1), (script,cp.stdout,cp.stderr)
    results.append(dict(script=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),arguments=['--db',str(ROOT)],
                        exit_code=cp.returncode,stdout=cp.stdout,stderr=cp.stderr))
(OUT/'consumer-checks.json').write_text(json.dumps(dict(scope='Reader behavior and discoverability; existing disagreements retained, not a semantic or live validation campaign.',runs=results),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Private reader controls passed:',len(results)-2)
for row in results[-2:]:
    print(row['script'],row['exit_code'])
    print(row['stdout'])
