"""CLI boundary around original repository functions; no replacement implementation."""
import argparse,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--input',type=Path,required=True)
ap.add_argument('--kind',choices=['measure','view'],required=True);ap.add_argument('--subsystems',type=Path,required=True);a=ap.parse_args()
sys.path.insert(0,str(a.source/'Database/Tools/analysis-kit/gfz-scripts'))
sys.path.insert(0,str(a.source/'Database/Tools/dashboard'))
import requirements as R,server as S,generation as G
obj=json.loads(a.input.read_text());receipt={'kind':a.kind,'result':None,'exception':None,
 'modules':{m.__name__:str(Path(m.__file__).resolve()) for m in (R,S,G)}}
try:
 if a.kind=='measure':receipt['result']=R.measure(obj['facts_doc'],obj['map'],obj['board'],obj['reporter'],obj['gate'],str(a.subsystems))
 else:receipt['result']=S.check_progress(obj)
except BaseException as e:receipt['exception']={'type':type(e).__name__,'detail':str(e)}
print(json.dumps(receipt))
sys.exit(1 if receipt['exception'] else 0)
