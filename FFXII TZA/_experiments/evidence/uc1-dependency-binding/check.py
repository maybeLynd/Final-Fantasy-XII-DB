"""Read-only, selected-generation dependency evidence reducer; no build/import."""
import ast, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_bytes())

def check(root):
    root = Path(root); r = root / 'run-02'
    terminal = load(root / 'capture-terminal.json')
    assert terminal['terminal'] is True and terminal['returncode'] == 0 and not terminal['stderr'], 'Capture did not finish successfully'
    assert sha(root / 'capture.py') == terminal['driver_sha256']
    identity = load(r / 'identity.json'); pre = load(r / 'pre-declaration-identity.json')
    assert identity['driver_sha256'] == terminal['driver_sha256'] == pre['driver_sha256']
    assert identity['source'] == pre['source']
    assert identity['generation'] == 'g20260929T135626Z-00f775'
    assert sha(r / 'MANIFEST.json') == identity['manifest_sha256'] == 'a53cf5955380b47267028b8b2221bbdb1eb0b622686cf6579354c6efd7443df8'
    man = load(r / 'MANIFEST.json'); view = load(r / 'view-executable.json')
    assert man['generation'] == identity['generation']
    assert sha(r / 'view-executable.json') == man['outputs']['view-executable.json']['sha256']
    assert len(identity['source']) == 3
    for s in identity['source']:
        assert sha(r / s['copy']) == s['sha256']
    builder, helper, generation = identity['source']
    assert builder['path'] == 'Database/Tools/dashboard/build_views.py'
    assert helper['path'] == 'Database/Tools/analysis-kit/gfz-scripts/uc1_band.py'
    assert generation['path'] == 'Database/Tools/analysis-kit/gfz-scripts/generation.py'
    assert builder['sha256'] == man['generator']['sha256']
    assert generation['sha256'] == man['verifier']
    assert len(identity['snapshot_controls']) == 3
    assert {s['key'] for s in identity['snapshot_controls']} == {'uc1_1_64', 'uc1_65_256', 'build_views.py'}
    for s in identity['snapshot_controls']:
        assert sha(r / s['copy']) == s['sha256'] == man['inputs'][s['key']]['sha256']
    text = (r / builder['copy']).read_text('utf-8'); tree = ast.parse(text)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    selected = load(r / 'selected-original-functions.json')
    assert set(selected) == {'text_intervals', 'declare_inputs', '_build'}
    for name, code in selected.items(): assert code == ast.get_source_segment(text, funcs[name])
    ti = funcs['text_intervals']
    assert any(isinstance(n, ast.Import) and any(a.name == 'uc1_band' for a in n.names) for n in ast.walk(ti))
    calls = {ast.unparse(n.func) for n in ast.walk(ti) if isinstance(n, ast.Call)}
    assert {'uc1_band.load', 'uc1_band.apply', 'uc1_band.describe'} <= calls
    assert 'uc1_band' not in selected['declare_inputs']
    declarations = load(r / 'original-declarations.json')
    assert sorted(declarations) == sorted(man['inputs']) and len(declarations) == 25
    assert not any(str(s['path']).replace('\\', '/').endswith('/uc1_band.py') for s in declarations.values())
    for key in ('uc1_1_64', 'uc1_65_256', 'build_views.py'):
        assert Path(declarations[key]['path']) == Path(man['inputs'][key]['path'])
    gtree = ast.parse((r / generation['copy']).read_text('utf-8'))
    module_sha = next(n for n in gtree.body if isinstance(n, ast.FunctionDef) and n.name == '_module_sha')
    assert any(isinstance(n, ast.Name) and n.id == '__file__' for n in ast.walk(module_sha))
    assert 'uc1_band' not in ast.get_source_segment((r / generation['copy']).read_text('utf-8'), module_sha)
    assert 'uc1_band.apply' in view['source']['instrument']
    metadata = json.dumps(man, sort_keys=True) + json.dumps(view, sort_keys=True)
    assert helper['sha256'] not in metadata and 'uc1_band.py' not in metadata
    observation = load(r / 'observation.json')
    assert json.loads(terminal['stdout']) == observation
    assert observation['original_declarations_bind_helper'] == []
    assert observation['manifest_input_keys'] == observation['declared_input_keys'] == sorted(declarations)
    assert all(observation[k] is True for k in ('generator_binds_builder', 'verifier_binds_generation_module', 'table_snapshots_bound', 'view_names_uc1_apply'))
    assert observation['helper_hash_or_path_in_manifest_or_view'] is False
    assert observation['helper_current_sha256'] == helper['sha256']
    return {'result': 'SCOPED_DEPENDENCY_BINDING_GAP', 'generation': man['generation'],
            'declarations': len(declarations), 'positive_bound_snapshots': 3,
            'actual_dependency': ['uc1_band.load', 'uc1_band.apply', 'uc1_band.describe'],
            'unbound_helper': helper,
            'limits': 'Retained selected manifest/output and static dependency path only. Extracted original declaration function with supplied path globals, not a full build. Current helper bytes do not identify the helper loaded by the historical generation. No mutation/drift/skip/export or FF12 execution observed; no whole archive certification.'}

if __name__ == '__main__':
    print(json.dumps(check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent), indent=2))
