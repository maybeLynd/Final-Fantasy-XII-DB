import importlib.util,json,re,sys
spec=importlib.util.spec_from_file_location('subject',sys.argv[1]);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
c=json.load(open(sys.argv[3]));kw=dict(names=('obj',),exits=tuple(c['exits']))
if c['mode']=='tagged':
 kw['tags']=c['tags']
 if c.get('separator')=='tab':kw['line']=re.compile(r'^(PASS|FAIL)\t(\S+)(?:\t|$)')
else:
 def validate(m):
  x=m.obj
  return None if isinstance(x,dict) and x.get('complete') is True and x.get('rows')==[7,9] else 'incomplete required data object'
 kw['validate']=validate
m,why=p.run(sys.argv[2],[sys.argv[2]],**kw)
if why:
 print('COMPOSER_FAIL',why);sys.exit(1)
print('COMPOSER_PASS',json.dumps(m.obj));sys.exit(0)
