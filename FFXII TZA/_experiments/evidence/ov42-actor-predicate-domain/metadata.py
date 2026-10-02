"""Additive source map and the actual publication prerequisite invocation."""
import ast,copy,hashlib,importlib.util,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((P/'result-01.json').read_text());new=json.loads((P/'result-02.json').read_text())
def derive_ast(p):
 t=ast.parse(p.read_text());return ast.dump(next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='derive'),include_attributes=False)
if derive_ast(P/'prove.py')!=derive_ast(P/'prove-before-source-map-metadata-02.py'):raise RuntimeError('scientific derive changed')
keys=set(old)|set(new)
if any(old.get(k)!=new.get(k) for k in keys-{'driver_sha256','source_pins'}):raise RuntimeError('scientific result changed')
if len(new['source_pins'])!=2 or new['source_pins'][0]!=old['source_pins'][0]:raise RuntimeError('additive second-source map not exact')
s=importlib.util.spec_from_file_location('actual_curated_publisher',W/'prepare-residue-packet-publication.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
positive=M.verify_packet_annotations(P,'result-02.json')
if len(positive.get('source_checks',[]))!=2:raise RuntimeError('actual publication did not check both required source maps')
F=P/'metadata-controls-01';F.mkdir(exist_ok=False)
d=F/'changed-class-memory-width';d.mkdir()
for x in new['source_pins']:
 dest=d/x['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/x['path'],dest)
alt=copy.deepcopy(new);file=d/alt['source_pins'][1]['path'];raw=json.loads(file.read_text())
inst=next(i for q in raw['ranges'] for i in q['instructions'] if i['memory'])
inst['memory'][0]['size']=4 if inst['memory'][0]['size']!=4 else 8
file.write_text(json.dumps(raw));alt['source_pins'][1]['sha256']=sha(file)
(d/'result-02.json').write_text(json.dumps(alt))
try:M.verify_packet_annotations(d,'result-02.json')
except ValueError as e:negative=dict(refused=True,diagnostic=str(e))
else:raise RuntimeError('actual publication accepted changed class memory annotation')
z=dict(complete=True,derive_unchanged=True,scientific_fields_unchanged=True,
 source_map_correction='result01 has availability map; additive result02 also declares the class20 map already checked by the producer',
 actual_publication_positive=positive,negative=negative,publisher_sha256=sha(W/'prepare-residue-packet-publication.py'),
 limits='Metadata/prerequisite invocation controls, not an extra original-code or game experiment')
with (P/'metadata-correction-01.json').open('x') as f:json.dump(z,f,indent=2)
print('VERIFIED metadata-only source-map addition and actual two-source publication prerequisite/refusal')
