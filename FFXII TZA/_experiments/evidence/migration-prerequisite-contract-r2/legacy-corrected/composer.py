import importlib.util,inspect,json,re,sys
spec=importlib.util.spec_from_file_location('subject',sys.argv[1]);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
assert tuple(inspect.signature(p.run).parameters)==('path','argv','tags','names','line'), 'legacy API precondition failed'
c=json.load(open(sys.argv[3]));assert c['mode']=='tagged' and c['separator']=='tab' and c['exits']==[0]
m,why=p.run(sys.argv[2],[sys.argv[2]],tags=c['tags'],names=('obj',),line=re.compile(r'^(PASS|FAIL)\t(\S+)(?:\t|$)'))
if why:
 print('COMPOSER_FAIL',why);sys.exit(1)
print('COMPOSER_PASS',json.dumps(m.obj));sys.exit(0)
