import ast,glob,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'run-02'
GEN='g20260929T135626Z-00f775';MAN_SHA='a53cf5955380b47267028b8b2221bbdb1eb0b622686cf6579354c6efd7443df8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr
 return p.stdout.strip()
def run():
 assert not R.exists(),'Write-once retained/static observation'
 R.mkdir();root=Path('Database/Tools/work/dashboard');d=root/GEN
 man=d/'MANIFEST.json';view=d/'outputs/view-executable.json';assert sha(man)==MAN_SHA
 m=json.loads(man.read_bytes());assert m['generation']==GEN and sha(view)==m['outputs']['view-executable.json']['sha256']
 assert (W/'run-01/MANIFEST.json').read_bytes()==man.read_bytes() and (W/'run-01/view-executable.json').read_bytes()==view.read_bytes()
 shutil.copyfile(W/'run-01/MANIFEST.json',R/'MANIFEST.json');shutil.copyfile(W/'run-01/view-executable.json',R/'view-executable.json')
 identity={'driver_sha256':sha(Path(__file__)),'python':sys.executable,'python_version':sys.version,'head':git('rev-parse','HEAD'),'generation':GEN,'manifest_sha256':MAN_SHA,'selection':'Earlier direct CURRENT-pointer read tool8c8207, now exact hash-bound retained generation; not a new current/latest claim','source':[],'snapshot_controls':[],'limits':'Selected manifest/output binding and static original source/declaration only; no full builder, semantic source mutation, drift outcome, export CLI, loaded process or guest execution.'}
 sources=['Database/Tools/dashboard/build_views.py','Database/Tools/analysis-kit/gfz-scripts/uc1_band.py','Database/Tools/analysis-kit/gfz-scripts/generation.py']
 for name in sources:
  p=Path(name);before=sha(p);target=R/'source'/p.name;target.parent.mkdir(exist_ok=True);retained=W/'run-01/source'/p.name;assert sha(retained)==before;shutil.copyfile(retained,target);assert sha(p)==sha(target)==before
  identity['source'].append({'path':name,'copy':target.relative_to(R).as_posix(),'sha256':before,'commit':git('log','-1','--format=%H','--',name),'blob':git('hash-object','--no-filters',name)})
 assert identity['source'][0]['sha256']==m['generator']['sha256'] and identity['source'][2]['sha256']==m['verifier']
 tree=ast.parse((R/'source/build_views.py').read_text('utf-8'))
 decl=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='declare_inputs')
 # Exact original declaration function, path globals supplied with their actual
 # original values. No adapters, captures, begin/commit or library code executed.
 module=ast.Module(body=[decl],type_ignores=[]);ns={'__file__':str(Path(sources[0]).resolve()),'os':os,'glob':glob,'DB':str(Path('Database/FFXII TZA').resolve()),'TOOLS':str(Path('Database/Tools').resolve()),'HERE':str(Path(sources[0]).resolve().parent)}
 identity['retry_limits']='Initial original declaration failed at missing __file__ supplied global; no declared result/positive snapshots or semantic closure. Original driver/terminal/raw retained; exact retained sources/manifest/view reused. Corrected namespace supplies actual original path value.'
 (R/'pre-declaration-identity.json').write_bytes((json.dumps(identity,indent=2)+'\n').encode())
 exec(compile(module,str(Path(sources[0]).resolve()),'exec'),ns)
 declarations=ns['declare_inputs'](str((root/'_capture').resolve()))
 (R/'original-declarations.json').write_bytes((json.dumps(declarations,indent=2)+'\n').encode())
 helper=Path(sources[1]).resolve()
 bound_paths=[n for n,c in declarations.items() if Path(c['path']).resolve()==helper]
 assert not bound_paths
 for name in ['uc1_1_64','uc1_65_256','build_views.py']:
  assert name in declarations and name in m['inputs']
  inp=d/'inputs'/name;assert sha(inp)==m['inputs'][name]['sha256']
  target=R/'bound-positive-inputs'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(inp,target)
  identity['snapshot_controls'].append({'key':name,'sha256':sha(target),'copy':target.relative_to(R).as_posix()})
 funcs={n.name:ast.get_source_segment((R/'source/build_views.py').read_text('utf-8'),n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['text_intervals','declare_inputs','_build']}
 (R/'selected-original-functions.json').write_bytes((json.dumps(funcs,indent=2)+'\n').encode())
 text=json.dumps(m,sort_keys=True)+json.dumps(json.loads(view.read_bytes()),sort_keys=True)
 helper_sha=identity['source'][1]['sha256']
 assert 'uc1_band.apply' in json.loads(view.read_bytes())['source']['instrument']
 assert helper_sha not in text and 'uc1_band.py' not in text
 obs={'question':'Does exact generation bind the UC1 helper code used by the executable adapter?','original_declarations_bind_helper':bound_paths,'manifest_input_keys':sorted(m['inputs']),'declared_input_keys':sorted(declarations),'generator_binds_builder':True,'verifier_binds_generation_module':True,'table_snapshots_bound':True,'view_names_uc1_apply':True,'helper_hash_or_path_in_manifest_or_view':False,'helper_current_sha256':helper_sha,'interpretation':'Explicit transitive helper-code binding is absent here, although builder and band-table bytes are bound. No inference of a specific source-change drift/skip or actual-loaded-helper version.'}
 for s in identity['source']:assert sha(Path(s['path']))==s['sha256']
 (R/'identity.json').write_bytes((json.dumps(identity,indent=2)+'\n').encode());(R/'observation.json').write_bytes((json.dumps(obs,indent=2)+'\n').encode());print(json.dumps(obs,indent=2))
if __name__=='__main__':
 try:run()
 except BaseException:
  if R.exists():(R/'failure.txt').write_text(traceback.format_exc())
  raise
