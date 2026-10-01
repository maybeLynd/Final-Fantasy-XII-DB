import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_bytes())

def check(w):
    r = w/'run-02'; terminal = load(w/'capture-terminal.json')
    if '--fault-upstream-failed' in sys.argv: terminal['returncode'] = 1
    assert terminal['terminal'] is True and terminal['returncode'] == 0 and not terminal['stderr'], 'Required upstream run failed/incomplete'
    assert terminal['driver_sha256'] == sha(w/'capture.py')
    i = load(r/'identity.json'); result = load(r/'result.json')
    assert result == json.loads(terminal['stdout']) and i['driver_sha256'] == sha(w/'capture.py')
    assert i['repair'] == 'cdbf25a5d711654ccbb883f472309c3f42df290f' and i['exe']['sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    for s in i['sources']:
        p, c = r/s['copy'], r/s['commit_copy']
        assert sha(p) == s['sha256'] and sha(c) == s['commit_sha256']
        assert p.read_bytes().replace(b'\r\n',b'\n') == c.read_bytes().replace(b'\r\n',b'\n')
    for s in i['providers']: assert sha(r/s['copy']) == s['sha256']
    old = load(w/'capture-terminal-before-line-ending-preflight.json')
    assert old['terminal'] and old['returncode'] != 0 and 'Selected repair source moved' in old['stderr']
    assert old['driver_sha256'] == sha(w/'capture-before-line-ending-preflight.py')
    diagnostic = load(w/'source-identity-diagnostic.json')
    assert len(diagnostic) == 3 and all(x['equal_after_CRLF_to_LF_only'] for x in diagnostic)
    helper = next(s for s in i['sources'] if s['path'].replace('\\','/').endswith('/uc1_band.py'))
    assert helper['sha256'] == '746b6fabbee735e74b33a052da9088de8680743407ed601605100d2d8bdac86b'
    current = (r/helper['copy']).read_bytes(); committed = (r/helper['commit_copy']).read_bytes()
    assert committed.replace(b'\r\n',b'\n') != current.replace(b'import os',b'import io',1).replace(b'\r\n',b'\n'), 'Semantic-change control'
    pop = load(r/'population-controls.json')
    assert len(pop) == 40 and {x['case'] for x in pop} == {'disjoint','double','triple','clipped','three-real-extents'}
    for x in pop:
        # Independent per-byte enumerator; does not reuse producer depth transition.
        depth = [sum(int(a) <= p < int(a)+z for a,z in x['pop'].items()) for p in range(x['origin'], x['origin']+x['size'])]
        unique, extra = sum(d >= 2 for d in depth), sum(max(0,d-1) for d in depth)
        assert (x['unique'],x['extra']) == (unique,extra) and x['oracle'] == [unique,extra]
        if '--fault-additional-cover-is-unique' in sys.argv: assert extra == unique, 'Triple cover != unique overlap'
    for name, expected in [('disjoint',0),('double',8),('triple',8),('three-real-extents',33)]:
        v = load(r/name/'view.json'); m = next(x for x in v['measures'] if x['id']=='bytes-overlap')
        assert m['numerator'] == expected and 'each such byte once' in m['label'] and 'additional covers' in m['limits']
    delta = load(r/'definition-transition.json')['raw_delta']
    assert delta == result['definition_change_delta'] and delta['na'] == 'N/A - definition changed' and 'pp' not in delta
    assert (delta['old']['numerator'],delta['new']['numerator']) == (12,8)
    if '--fault-v1-comparable' in sys.argv: assert 'pp' in delta, 'Definition change must not be numeric progress'
    same = load(r/'same-version-control.json'); assert same['pp'] == 0 and same == result['same_definition_delta']
    decl = load(r/'declarations.json'); assert decl['uc1_band.py']['path'] == i['loaded']['helper']
    store = r/'store'; pointer = load(store/'CURRENT'); d = store/pointer['generation']; man = load(d/'MANIFEST.json')
    assert sha(d/'MANIFEST.json') == pointer['manifest_sha256']
    assert man['inputs']['uc1_band.py']['sha256'] == helper['sha256'] and sha(d/'inputs/uc1_band.py') == helper['sha256']
    if '--fault-unbound-helper-is-valid' in sys.argv: assert 'uc1_band.py' not in man['inputs'], 'Actual committed helper binding required'
    view = load(d/'outputs/view-executable.json');m = next(x for x in view['measures'] if x['id']=='bytes-overlap')
    assert view['definition'] == 'v2' and m['direction'] == 'down' and m['numerator'] == 8
    assert sha(d/'outputs/view-executable.json') == man['outputs']['view-executable.json']['sha256']
    controls = load(r/'strict-helper-controls.json'); assert controls == result['strict_helper_controls'] and len(controls) == 2
    for x in controls:
        assert x['terminal'] and x['exception']['type']=='GenerationError' and 'uc1_band.py' in x['exception']['message'] and x['current_and_success_history_unchanged']
        assert x['failure']['current_unchanged'] == pointer['generation']
    assert controls[0]['helper_before_sha256'] != controls[0]['helper_after_sha256'] and 'inputs moved' in controls[0]['exception']['message']
    assert 'required input not usable' in controls[1]['exception']['message']
    # Verification is scoped to preserved reduced original invocation, not full deployment.
    return {'verdict':'ACCEPT scoped overlap/helper repair', 'repair':i['repair'], 'population_controls':40, 'actual_adapter_cases':4, 'definition_change':'N/A, both sides retained', 'strict_helper':'bound; same-size-mid-build and missing-begin refuse, CURRENT/history unchanged', 'limits':result['limits']}

if __name__=='__main__':
    root = Path(sys.argv[sys.argv.index('--root')+1]) if '--root' in sys.argv else Path(__file__).resolve().parent
    print(json.dumps(check(root),indent=2))
