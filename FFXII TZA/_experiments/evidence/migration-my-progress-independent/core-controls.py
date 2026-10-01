import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;D=W/'core-01';assert not D.exists(),'Preserve prior phase'
D.mkdir();commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
rel='Database/Tools/dashboard/requirements.py';src=D/'requirements.py';data=subprocess.check_output(['git','show',commit+':'+rel]);src.write_bytes(data)
(D/'requirements-requested622.py').write_bytes(subprocess.check_output(['git','show','622c0866d:'+rel]))
spec=importlib.util.spec_from_file_location('original_requirements',src);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
tsv=D/'subsystems.tsv';tsv.write_text('id\tcategory\tname\towner\tpages\nS-001\t04\tLabelled fixture\tASTRA\t04-Actor-Entity/fixture.md\n')
cmap={'folder':{'04':['E','P']}}
facts={'facts':[{'k':f+':fixture','f':f,'ok':True,'st':'ANSWERED' if f=='Q' else 'labelled accepted fixture',
 'doc':'04-Actor-Entity/fixture.md','h':[['folder','04']],'o':'ASTRA','e':'labelled fixture, not canonical closure','n':''}
 for f in R.FAMILIES if f not in ('L2','T')],'failed':{},'gaps':{},'excluded':[]}
reporter={'levels':{'L2_reconstruction_grade':{'systems':[dict(system='S-001',**{k:'MET' for k in ('contract','types','relationships','runtime','script_data')})]},
 'terminal_certification':{'required_consecutive':30,'final_audits_declared':30}}}
gate={'verdict':'MET','detail':['acceptance: OK labelled synthetic input, NOT an actual audit'],'remaining':''};board={'tasks':[]}
raw={'phase':'initial pure-measure control only; whole request INCOMPLETE','method':'A actual original Python tooling with pre-resolved synthetic fixtures; not FF12/live',
 'source_tree_commit':commit,'source_last_commit':subprocess.check_output(['git','log','-1','--format=%H',commit,'--',rel],text=True).strip(),
 'source_sha256':hashlib.sha256(data).hexdigest(),'source_blob':subprocess.check_output(['git','rev-parse',commit+':'+rel],text=True).strip(),
 'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'cases':[],'phase_finished':False}
for name in ('all-accepted-final30','open-Q-with-all-L2-MET','missing-bucket-family','invalid-terminal-required0'):
 f=copy.deepcopy(facts);rep=copy.deepcopy(reporter);g=copy.deepcopy(gate)
 if name=='open-Q-with-all-L2-MET':next(x for x in f['facts'] if x['f']=='Q').update(ok=False,st='OPEN')
 elif name=='missing-bucket-family':f['gaps']['X']='labelled missing member-format declaration'
 elif name=='invalid-terminal-required0':rep['levels']['terminal_certification'].update(required_consecutive=0,final_audits_declared=0)
 inp={'facts_doc':f,'map':cmap,'board':board,'reporter':rep,'gate':g,'subsystems_sha256':hashlib.sha256(tsv.read_bytes()).hexdigest()}
 out=R.measure(f,cmap,board,rep,g,str(tsv))
 (D/(name+'-input.json')).write_text(json.dumps(inp,indent=2)+'\n');(D/(name+'-output.json')).write_text(json.dumps(out,indent=2)+'\n')
 if name=='all-accepted-final30':assert out['ready'] and out['terminal']=={'accepted':30,'required':30}
 elif name=='open-Q-with-all-L2-MET':assert not out['ready'] and out['families']['Q']=={'accepted':0,'total':1}
 elif name=='missing-bucket-family':assert not out['measured'] and not out['ready'] and out['gaps']['X']
 else:assert out['ready'] and out['terminal']=={'accepted':0,'required':0}
 raw['cases'].append({'name':name,'input_sha256':hashlib.sha256((D/(name+'-input.json')).read_bytes()).hexdigest(),
 'output_sha256':hashlib.sha256((D/(name+'-output.json')).read_bytes()).hexdigest(),'ready':out['ready'],'measured':out['measured'],
 'terminal':out['terminal'],'union':out['scopes']['union']})
raw['phase_finished']=True
raw['observation']='With pre-resolved synthetic reporter required_consecutive0 and MET/acceptanceOK fixture gate, original measure returns readyTrue/terminal0of0. Initial admission boundary only; actual caller/schema/generation/server/deployed path unresolved.'
raw['next']='Trace original build_views validation/caller and server refusal paths; fixed30 governing contract must be retained. Finish other independently derived cases then exact authored suite/deployed drilldown; do not infer native/live/full task closure.'
(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('INITIAL_MEASURE_PHASE_FINISHED_WHOLE_REVIEW_INCOMPLETE',[(x['name'],x['ready']) for x in raw['cases']],flush=True)
