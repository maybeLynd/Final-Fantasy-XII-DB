"""Independent actual original-function re-review; never open device paths."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='ec45e3f6d4bbc0c0e42d7f869cf6a8e76b31dc7121be0fd1c03dd3ac354bdff6'
S=P/'generation.py';old=P/'prior-generation.py';out=P/'result-01.json'
if out.exists():raise RuntimeError('immutable result exists')
if sha(S)!=expected or sha(old)!='033c37bd65cf4e9b5f33c94af14ad867877ac32cf992ad1515d4c230a6597dec':raise RuntimeError('required original source identity failed')
for label in ['source','diff']:
    r=json.loads((P/(label+'.receipt.json')).read_text())
    if r['exit']!=0 or r['terminal'] is not True or r['exception'] is not None or not(P/(label+'.stdout')).read_bytes() or(P/(label+'.stderr')).read_bytes() or sha(P/(label+'.stdout'))!=r['stdout_sha256']:
        raise RuntimeError('upstream Git acquisition failed/incomplete')
spec=importlib.util.spec_from_file_location('astra_device_stems_06d',S);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
# Compare complete modules after ONLY the declared set addition and docstring change.
def normalized(path):
    tree=ast.parse(path.read_text(encoding='utf-8'))
    tree.body=[n for n in tree.body if not(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['_DEVICES','_SUPERSCRIPT'] for t in n.targets))]
    f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='windows_key')
    if not(isinstance(f.body[0],ast.Expr) and isinstance(f.body[0].value,ast.Constant) and isinstance(f.body[0].value.value,str)):raise RuntimeError('windows_key docstring absent')
    f.body[0].value.value='declared scope placeholder'
    return ast.dump(tree,include_attributes=False)
rows=[]
for stem in ['COM','LPT']:
    for digit in ['\u00b9','\u00b2','\u00b3']:
        for name in [stem+digit,stem.lower()+digit+'.json']:
            mapped=G.snapshot_name(name)
            rows.append({'name':name,'mapped':mapped,'expected_mapping':'%%%02X'%ord(name[0])+name[1:],'reason':G.portable_component(name),'mapped_reason':G.portable_component(mapped),'key':G.windows_key(mapped)})
ordinary=[{'name':n,'mapped':G.snapshot_name(n),'reason':G.portable_component(n)} for n in ['ASTRA-plain.md','COM10.txt','LPT10.txt','COM0','LPT0']]
ascii_controls=[{'name':n,'mapped':G.snapshot_name(n),'reason':G.portable_component(n),'mapped_reason':G.portable_component(G.snapshot_name(n))} for n in ['CON','nul.json','COM1.txt','LPT9']]
percent_control={'name':'%43OM\u00b9','mapped':G.snapshot_name('%43OM\u00b9'),'other':G.snapshot_name('COM\u00b9')}
doc=G.windows_key.__doc__
checks={'declared_changes_only_restore_reader_unchanged':normalized(S)==normalized(old),
 'twelve_former_failures_now_exactly_mapped_and_refused':len(rows)==12 and all(r['mapped']==r['expected_mapping'] and r['reason']=='is a Windows device name' and r['mapped_reason'] is None for r in rows),
 'twelve_mapped_keys_distinct':len({r['key'] for r in rows})==12,
 'ordinary_controls_unchanged':all(r['mapped']==r['name'] and r['reason'] is None for r in ordinary),
 'ascii_device_controls_correct':all(r['mapped']!=r['name'] and r['reason']=='is a Windows device name' and r['mapped_reason'] is None for r in ascii_controls),
 'encoded_looking_logical_name_kept_distinct':percent_control['mapped']=='%2543OM\u00b9' and percent_control['mapped']!=percent_control['other'],
 'key_docstring_explicit_scope':all(x in doc for x in ['two Windows aliasing rules','NOT a complete theory','8.3 short names','alternate data streams','Unicode normalization','device names']) and 'exactly when' not in doc}
result={'source_commit':'06d817762e31d05bfe5db91f572576102143cd50','source_sha256':sha(S),'prior_source_sha256':sha(old),'driver_sha256':sha(Path(__file__)),'python':sys.version,'interpreter_sha256':sha(Path(sys.executable)),'platform':platform.platform(),'method':'Actual exact original host Python pure functions plus complete AST equivalence outside declared changes','rows':rows,'ordinary_controls':ordinary,'ascii_controls':ascii_controls,'percent_control':percent_control,'windows_key_docstring':doc,'checks':checks,'complete':True,'verdict':'ACCEPT_BOUNDED_DEVICE_REPAIR' if all(checks.values()) else 'REJECT','no_device_path_opened':True,'no_restore_cli_or_game_run':True,'limits':['Twelve selected names and scoped original code, not all Windows namespace/alias behavior.','Prior physical restore acceptance retained; seven native restores not rerun.','No deployed host/archive/full M0-M5/FF12 evidence. Producer32-test campaign not ours.']}
out.write_text(json.dumps(result,indent=2,ensure_ascii=True)+'\n')
print(json.dumps({'verdict':result['verdict'],'checks':checks,'restore_runs':0,'game_runs':0}))
raise SystemExit(0 if all(checks.values()) else 1)
