"""A bounded static feasibility probe, not accepted source label semantics."""
import hashlib,json,re,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-named-entry-line-convention');sha=lambda b:hashlib.sha256(b).hexdigest();U=lambda b,o:struct.unpack_from('<I',b,o)[0]
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-EVCTRL-JUMP-BINDING');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'feasibility.json').exists()
pr=json.loads((P/'raw.json').read_text());bind=next(x for x in pr['bindings'] if x['module']=='evctrl' and x['scope']==1)
files={}
for ext in ['dbg','sbn','ebp']:
 data=(P/'retained'/('evctrl.'+ext)).read_bytes();i=next(i for i in pr['reference']['files'] if i['module']=='evctrl' and i['extension']==ext);assert sha(data)==i['sha256'];files[ext]=data
b,s,e=files['dbg'],files['sbn'],files['ebp'];g={'struct':struct};exec((P/'retained/selected-sbn-functions.py').read_text(),g)
blocks=[]
for o,end in g['sbn_blocks'](s):
 L,bases,starts,tail=g['sbn_group_read'](s,o);blocks.append([dict(index=j,offset=a,hex=s[a:s.index(b'\0',a,end)].hex(),text=s[a:s.index(b'\0',a,end)].decode('cp932')) for j,a in enumerate(starts)])
ent=struct.unpack_from('<IHHIIIIIIHH',bytes.fromhex(bind['entry_hex']));base=bind['base'];np=bind['name_pool'];q0=bind['q0'];q1=bind['q1'];heap=U(b,8)
def name(data,o):assert data[o-1]==0;return data[o:data.index(b'\0',o)].decode('cp932')
names=[name(b,heap+U(b,q1+4+4*k)) for k in range(U(b,q1))]
jt=bind['jump_table'];pcs=[U(e,jt+4+4*k) for k in range(U(e,jt))]
fun=base+ent[5];nf=U(e,fun);functions=[]
for k in range(nf):
 no,pc=struct.unpack_from('<II',e,fun+4+8*k);functions.append(dict(index=k,name=name(e,np+no),pc=pc,record_hex=e[fun+4+8*k:fun+12+8*k].hex()))
targets=[]
for k,pc in enumerate(pcs):
 assert pc<=bind['validated_code_bytes']
 line,block,flag=struct.unpack_from('<HBB',b,q0+4*pc)
 targets.append(dict(index=k,pc=pc,line=line,block=block,flag=flag,within_body=pc<bind['validated_code_bytes'],source=blocks[block][line-1] if line and block<len(blocks) and line<=len(blocks[block]) else None,code_prefix_hex=e[bind['code_start']+pc:bind['code_start']+min(pc+12,bind['validated_code_bytes'])].hex()))
labels=[]
for row in [x for x in pr['rows'] if x['module']=='evctrl']:
 lab=[x for x in row['occurrences'] if re.fullmatch(r'\s*'+re.escape(row['name'])+r'\s*:\s*',x['source']['text'])];assert len(lab)==1
 source_index=lab[0]['index'];block=lab[0]['block'];neighborhood=blocks[block][source_index:source_index+9]
 candidates=[x for x in targets if x['block']==block and source_index+1<=x['line']-1<=source_index+8]
 labels.append(dict(name=row['name'],q1_index=row['jump_index'],same_index_candidate=targets[row['jump_index']],source_label=lab[0],source_neighborhood=neighborhood,target_neighborhood_candidates=candidates,limit='Near source line is candidate only; neither mapping nor compiler attribution established'))
result=dict(status='FEASIBILITY_ONLY_NOT_SEMANTIC_ACCEPTANCE',method='A retained original parent61 inputs, no source installation/game/native/VM execution',parent=P.as_posix(),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),input_sha256={ext:sha(data) for ext,data in files.items()},validated_code_bytes=bind['validated_code_bytes'],q1_count=len(names),jt_count=len(pcs),q1_names=names,jump_targets=targets,functions=functions,labels=labels,limits='Only already validated6130-byte directory body. Shared144-byte debug tail is not read as actual code. Source proximity and a table target do not establish label semantics. Exact function/jump opcode identity and discriminating control needed before closure; cause unknown. PC OFF/S19 parked/fullL1+L2 NOT_MET.')
(W/'feasibility.json').write_text(json.dumps(result,indent=2)+'\n')
print('PROBE63',[(x['name'],x['q1_index'],[(c['index'],c['pc'],c['line']) for c in x['target_neighborhood_candidates']]) for x in labels], 'functions',functions,flush=True)
