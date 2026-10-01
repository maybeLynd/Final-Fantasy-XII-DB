import json,sys
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'source'))
import activity as A
x=json.loads(Path(sys.argv[1]).read_text());placer=A.Placer({'folder':{'07':['C']}},{'facts':[]},{})
try:
 r=A.compute(x['board'],x['poll'],x['claude'],placer,x['now']);out={'result':r,'exception':None,'module_paths':{'activity':A.__file__}}
except BaseException as e:out={'result':None,'exception':{'type':type(e).__name__,'text':str(e)},'module_paths':{'activity':A.__file__}}
print(json.dumps(out));sys.exit(1 if out['exception'] else 0)
