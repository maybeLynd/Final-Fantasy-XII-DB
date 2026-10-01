import importlib.util, json, os, sys, time
from pathlib import Path
sys.dont_write_bytecode=True
source,root,stage,gate=sys.argv[1:]
spec=importlib.util.spec_from_file_location('original_generation',source)
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
root=Path(root);s=G.Store(str(root/'store'))
b=s.begin({'data':{'path':str(root/'input')}})
Path(b.output_path('view.json')).write_text(json.dumps({'sentinel':'NEW'}))
replace=G.os.replace
def observed_replace(src,dst):
 if str(src)==b.dir and str(dst)==str(Path(s.root)/b.id):
  if stage=='after-rename':replace(src,dst)
  Path(gate).write_text(json.dumps({'pid':os.getpid(),'stage':stage,'build':b.id,'src':str(src),'dst':str(dst)}))
  time.sleep(60)
  if stage=='before-rename':return replace(src,dst)
  return None
 return replace(src,dst)
G.os.replace=observed_replace
s.commit(b,['view.json'])
