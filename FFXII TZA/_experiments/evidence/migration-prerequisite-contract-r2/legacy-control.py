import hashlib, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
R = W / 'run-01'
L = W / 'legacy-corrected'
assert not L.exists(), 'Preserve retained legacy control; no overwrite/replay'
L.mkdir()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw = json.loads((R / 'raw.json').read_text())
source = R / raw['sources']['legacy']['retained']
assert sha(source) == raw['sources']['legacy']['sha256']
composer = L / 'composer.py'
composer.write_text('''import importlib.util,inspect,json,re,sys
spec=importlib.util.spec_from_file_location('subject',sys.argv[1]);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
assert tuple(inspect.signature(p.run).parameters)==('path','argv','tags','names','line'), 'legacy API precondition failed'
c=json.load(open(sys.argv[3]));assert c['mode']=='tagged' and c['separator']=='tab' and c['exits']==[0]
m,why=p.run(sys.argv[2],[sys.argv[2]],tags=c['tags'],names=('obj',),line=re.compile(r'^(PASS|FAIL)\\t(\\S+)(?:\\t|$)'))
if why:
 print('COMPOSER_FAIL',why);sys.exit(1)
print('COMPOSER_PASS',json.dumps(m.obj));sys.exit(0)
''')
items = []
for case in ('custom-tab-fail', 'custom-tab-pass'):
    d = R / ('legacy--' + case)
    args = [str(Path(sys._base_executable)), '-B', str(composer), str(source), str(d / 'upstream.py'), str(d / 'declaration.json')]
    p = subprocess.run(args, capture_output=True, text=True, timeout=5)
    items.append({'name': case, 'invocation': args, 'returncode': p.returncode, 'stdout': p.stdout,
                  'stderr': p.stderr, 'timed_out': False, 'child_reaped': True,
                  'upstream_sha256': sha(d / 'upstream.py'), 'declaration_sha256': sha(d / 'declaration.json')})
result = {'method': 'A: corrected actual legacy composer; identical retained tab inputs',
          'driver_sha256': sha(__file__), 'composer_sha256': sha(composer),
          'original_failed_raw_sha256': sha(R / 'raw.json'), 'source_sha256': sha(source),
          'source_commit': raw['source_commit'], 'composer_path': str(composer),
          'cases': items, 'finished': True,
          'correction': 'Original two legacy attempts failed before reaching helper: generic-only exits keyword caused TypeError. No legacy semantics were accepted; original attempts retained. Correct composer checks exact legacy signature before using supported tags/names/line. Generic sixteen controls are not repeated.'}
(L / 'raw.json').write_text(json.dumps(result, indent=2) + '\n')
print('LEGACY_CORRECTED_CONTROL_FINISHED', flush=True)
