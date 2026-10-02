"""Affected actual publication-source contract, without repeating scientific cases."""
import ast,hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-03.status.json').read_text());x=json.loads((P/'result-02.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or x.get('producer_complete') is not True or x['driver_sha256']!=sha(P/'prove.py'):raise RuntimeError('required current positive failed')
# The only change to the six-refusal-tested producer is the source map schema.
old=(P/'prove-before-publication-map-02.py').read_text().replace("'sources':[{'source_file':'source-01.json'","'source_pins':[{'path':'source-01.json'").replace("{'source_file':'retained/'+name","{'path':'retained/'+name")
if ast.dump(ast.parse(old))!=ast.dump(ast.parse((P/'prove.py').read_text())):raise RuntimeError('scientific producer changed beyond metadata map')
t=importlib.util.spec_from_file_location('publisher',W/'prepare-residue-packet-publication.py');pub=importlib.util.module_from_spec(t);t.loader.exec_module(pub)
positive=pub.verify_packet_annotations(P,'result-02.json')
if positive['status']!='VERIFIED_PREREQUISITE' or len(positive['source_checks'])!=3:raise RuntimeError('actual publication-source positive failed')
D=P/'publication-controls-01';D.mkdir(exist_ok=False);rows=[]
for name,diag in [('missing-map','missing/incomplete source prerequisite map'),('stale-map-pin','current source preimage moved')]:
 q=D/name;q.mkdir();shutil.copyfile(P/'source-01.json',q/'source-01.json');shutil.copytree(P/'retained',q/'retained')
 y=json.loads((P/'result-02.json').read_text())
 if name=='missing-map':y.pop('source_pins')
 else:y['source_pins'][0]['sha256']='0'*64
 (q/'result-02.json').write_text(json.dumps(y,indent=2)+'\n')
 try:pub.verify_packet_annotations(q,'result-02.json')
 except ValueError as e:
  row={'case':name,'status':'EXPECTED_ACTUAL_GUARD_REFUSAL','exception':repr(e),'diagnostic_matched':diag in str(e),'guard_sha256':sha(W/'prepare-residue-packet-publication.py')}
 else:raise RuntimeError('actual guard accepted invalid source map')
 (q/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
 if not row['diagnostic_matched']:raise RuntimeError('unexpected publication guard failure')
 rows.append(row)
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'actual_guard_sha256':sha(W/'prepare-residue-packet-publication.py'),'positive':positive,'cases':rows,'count':2,'scientific_ast_unchanged_except_source_map':True,'limits':'Two calls into the actual publication prerequisite guard and one positive; not FF12 tests, publication/commit or independent acceptance. Six historical scientific CLI refusals remain exact older producer controls.'}
(P/'publication-control-result-01.json').write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PASS actual three-source publication map and two affected guard refusals; scientific samples not repeated')
