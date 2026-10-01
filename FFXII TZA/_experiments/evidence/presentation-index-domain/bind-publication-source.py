"""Add the required publication map without rewriting a finished scientific run."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=P/'result-02.json';receipt=P/'source-binding-01.json'
if out.exists() or receipt.exists():raise RuntimeError('fresh binding output required')
st=json.loads((P/'proof-01.status.json').read_text());old=json.loads((P/'result-01.json').read_text())
if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(P/'prove.py') or old['driver_sha256']!=sha(P/'prove.py') or not(P/'proof-01.stdout').read_bytes() or(P/'proof-01.stderr').read_bytes() or old.get('producer_complete') is not True or old['source_sha256']!=sha(P/'source-01.json') or old['retained_callers_sha256']!=sha(P/'retained/selector-callers-raw-01.json'):raise RuntimeError('required actual proof/source failed/incomplete')
spec=importlib.util.spec_from_file_location('presentation_actual_publisher',W/'prepare-residue-packet-publication.py');publisher=importlib.util.module_from_spec(spec);spec.loader.exec_module(publisher)
# The real publication guard rejects the missing map before preparation/writes.
try:publisher.verify_packet_annotations(P,'result-01.json')
except ValueError as e:
 if str(e)!='missing/incomplete source prerequisite map':raise
 refused=str(e)
else:raise RuntimeError('missing-map guard unexpectedly accepted')
v=dict(old)
v['source_pins']=[{'path':n,'sha256':sha(P/n)} for n in ['source-01.json','retained/selector-callers-raw-01.json']]
v['publication_binding']={'original_proof_result_sha256':sha(P/'result-01.json'),'adapter_sha256':sha(Path(__file__)),'scope':'Additive publication source-map only; original scientific driver/result/receipt immutable, no semantic/native run repeated.'}
out.write_text(json.dumps(v,indent=2)+'\n')
checked=publisher.verify_packet_annotations(P,'result-02.json')
if checked['status']!='VERIFIED_PREREQUISITE' or len(checked['source_checks'])!=2:raise RuntimeError('actual publication guard incomplete')
if {k:v for k,v in v.items() if k not in ['source_pins','publication_binding']}!=old:raise RuntimeError('binding altered original scientific result')
receipt.write_text(json.dumps({'original_map_refusal':refused,'actual_positive_guard':checked,'old_result_sha256':sha(P/'result-01.json'),'new_result_sha256':sha(out),'publisher_sha256':sha(W/'prepare-residue-packet-publication.py'),'adapter_sha256':sha(Path(__file__)),'semantic_fields_unchanged':True,'limits':'Actual original-publication annotation path only, not independent semantic acceptance/new source experiment.'},indent=2)+'\n')
print(json.dumps({'source_binding':'verified actual guard','sources':len(checked['source_checks']),'old_semantics_unchanged':True}))
