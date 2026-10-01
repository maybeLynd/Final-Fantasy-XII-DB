"""Measure old/revised extractor behavior against the same bounded source snapshot."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types

root = Path(__file__).resolve().parent
repo = root.parents[4]
kit = repo / 'Database/Tools/analysis-kit/gfz-scripts'
db = repo / 'Database/FFXII TZA'
sys.path.insert(0, str(kit))

def load(name, old):
    path = root / ('baseline-' + name + '.bin') if old else kit / name
    module = types.ModuleType(('old_' if old else 'new_') + name[:-3])
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

names = ['gen_address_index.py', 'knowledge_db.py', 'program_coverage.py',
         'census_bin_signatures.py', 'gen_rules_index.py']
old = {name: load(name, True) for name in names}
new = {name: load(name, False) for name in names}
report = dict(sources={name: dict(old=hashlib.sha256((root / ('baseline-' + name + '.bin')).read_bytes()).hexdigest(),
                                new=hashlib.sha256((kit / name).read_bytes()).hexdigest()) for name in names})
text = '00265020abcdef0123456789 00265020'
guards = []
for name, attr in [('gen_address_index.py', 'ADDR_LONGHEX'), ('knowledge_db.py', 'ADDR_LONGHEX'),
                   ('program_coverage.py', 'LONGHEX')]:
    a, b = getattr(old[name], attr), getattr(new[name], attr)
    guards.append(dict(file=name, old_pattern=a.pattern, new_pattern=b.pattern,
                       input=text, old_result=a.sub('', text), new_result=b.sub('', text)))
    assert a.sub('', text) == text and b.sub('', text) == ' 00265020'
report['guard_controls'] = guards
report['nav_ast_identical'] = ast.dump(ast.parse((root / 'baseline-census_bin_signatures.py.bin').read_bytes())) == ast.dump(ast.parse((kit / 'census_bin_signatures.py').read_bytes()))
assert report['nav_ast_identical']
texts = {p.relative_to(db).as_posix(): p.read_bytes() for p in db.rglob('*')
         if p.is_file() and p.suffix in ('.md', '.tsv') and '__pycache__' not in p.parts}
report['corpus_hashes'] = {name: hashlib.sha256(data).hexdigest() for name, data in texts.items()}
deltas = []
for name, raw in texts.items():
    if not name.endswith('.md'):
        continue
    text = raw.decode('utf-8-sig')
    for module, function in [('knowledge_db.py', 'citation_forms'), ('program_coverage.py', 'cited_addresses')]:
        a, b = getattr(old[module], function)(text), getattr(new[module], function)(text)
        if a != b:
            deltas.append(dict(document=name, tool=module, old=sorted(a), new=sorted(b)))
report['current_citation_deltas'] = deltas
assert not deltas, deltas
with tempfile.TemporaryDirectory(prefix='astra-exp021-') as temporary:
    scratch = Path(temporary)
    frozen = scratch / 'db'
    for name, raw in texts.items():
        if len(name) > 2 and name[:2].isdigit() and name[2] == '-':
            target = frozen / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
    functions = repo / 'Database/Tools/work/graph/functions.tsv'
    frozen_functions = scratch / 'functions.tsv'
    frozen_functions.write_bytes(functions.read_bytes())
    report['functions_sha256'] = hashlib.sha256(frozen_functions.read_bytes()).hexdigest()
    runs = {}
    for label, source in [('old', root / 'baseline-gen_address_index.py.bin'), ('new', kit / 'gen_address_index.py')]:
        output = scratch / (label + '-address-index.md')
        command = [sys.executable, str(source), '--db', str(frozen), '--out', str(output), '--functions', str(frozen_functions)]
        run = subprocess.run(command, capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        (root / (label + '-address-index.md.bin')).write_bytes(output.read_bytes())
        runs[label] = dict(command=command, exit_code=run.returncode, stdout=run.stdout,
                           stderr=run.stderr, output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    assert runs['old']['output_sha256'] == runs['new']['output_sha256']
    report['actual_index_runs'] = runs
old_rules = dict(old['gen_rules_index.py'].script_rules(repo))
new_rules = dict(new['gen_rules_index.py'].script_rules(repo))
report['rules'] = dict(old_count=len(old_rules), new_count=len(new_rules),
    changes=[dict(file=name, old=old_rules.get(name), new=new_rules.get(name))
             for name in sorted(old_rules.keys() | new_rules.keys()) if old_rules.get(name) != new_rules.get(name)])
assert all(not value.endswith('"""') for value in new_rules.values())
report['verdict'] = 'GUARD_REPAIRED; CURRENT_CITATION_AND_INDEX_OUTPUTS_UNCHANGED; NAV_AST_IDENTICAL; MODULE_DOCSTRINGS_PARSED'
(root / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(report['verdict'])
print(json.dumps(report['rules'], indent=2))
