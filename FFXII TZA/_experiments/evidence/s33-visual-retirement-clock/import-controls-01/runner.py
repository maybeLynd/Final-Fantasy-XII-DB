import contextlib,io,json,os,sys
BASE=sys.argv[1]
sys.path.insert(0,BASE)
try:
    exec(compile(open(sys.argv[2]).read(),sys.argv[2],'exec'))
except Exception as e:
    print(json.dumps({'prefix_returned':False,'exception':repr(e)}));raise SystemExit(2)
print(json.dumps({'prefix_returned':True,'upstream_allok':C.allok,'upstream_rows':C.results,'exception':None}))
