"""Normalize the modern-state portion of the incomplete same-session reload attempt. No process access or native execution."""
from pathlib import Path
import hashlib,json,struct
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
q=lambda b,o=0:struct.unpack_from('<Q',b,o)[0]
d=lambda b,o=0:struct.unpack_from('<I',b,o)[0]
w=lambda b,o=0:struct.unpack_from('<H',b,o)[0]
result=dict(status='INCOMPLETE',method='A: offline review of preserved C observations',samples=[],
            reviewer_sha256=sha(Path(__file__).read_bytes()),raw_inputs={})
spans=0
for label in ['current-complete','current-field']:
 p=E/(label+'-memory.json');record=json.loads(p.read_text())
 result['raw_inputs'][p.name]=sha(p.read_bytes())
 assert record['status']=='OBSERVED' and record['pid']==50736
 assert record['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert record['image_base']==0x120000 and record['modules'] and record['module_verdict']=='clean'
 assert record['known_read_control']=='19930d0a1a0a' and record['null_read_rejected'] and record['read_handle_closed']
 assert len(record['code_identity'])==1
 code=record['code_identity'][0]
 assert code['matches'] and code['bytes']==7996981 and code['disk_sha256']==code['live_sha256']=='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
 assert len(record['samples'])==2
 for s in record['samples']:
  reads={r['name']:r for r in s['reads']};assert len(reads)==len(s['reads']) and reads
  data={}
  for name,r in reads.items():
   b=bytes.fromhex(r['bytes']);assert len(b)==r['size'] and sha(b)==r['sha256']
   data[name]=b;spans+=1
  for a,b in [('registry_before','registry_after'),('pool_keep_capacity_before','pool_keep_capacity_after'),('image_address_base_before','image_address_base_after')]:assert data[a]==data[b]
  assert s['registry_stable'] and s['pool_keep_stable'] and s['base_stable'] and s['unit_bindings_stable']
  registry=data['registry_before'];base=q(data['image_address_base_before'])
  B=q(registry,0x70);assert B==s['battle_binding']
  assert q(data['pool_keep_capacity_before'])==s['pool'] and d(data['pool_keep_capacity_before'],24)==s['capacity']==32
  assert [q(data['pool_keep_capacity_before'],8),q(data['pool_keep_capacity_before'],16)]==s['keep_bindings']
  tables={}
  for name,off in [('enemy',0),('party',0x10),('class',0x30)]:
   desc=q(registry,off);assert desc==s['tables'][name]['descriptor']
   t=dict(descriptor=desc);tables[name]=t
   if not desc:continue
   h=data[name+'_table_header'];assert reads[name+'_table_header']['address']==desc
   count,stride,reference=d(h,4),w(h,8),d(h,12)
   start=(base+reference)&0xffffffffffffffff
   assert count and stride and len(data[name+'_table_rows'])==count*stride
   assert reads[name+'_table_rows']['address']==start
   t.update(count=count,stride=stride,start=start,end=start+count*stride,header_hex=h.hex())
  def member(ptr,t):
   if not t.get('count') or not t['start']<=ptr<t['end']:return None
   delta=ptr-t['start']
   return delta//t['stride'] if delta%t['stride']==0 else None
  raw_units=data['battle_unit_pool'];after=data['battle_unit_pool_after']
  assert len(raw_units)==len(after)==32*0xF50
  units=[]
  for slot in range(32):
   u=raw_units[slot*0xF50:(slot+1)*0xF50];v=after[slot*0xF50:(slot+1)*0xF50]
   assert (bool(u[0]&1),u[8:0x18],u[0x698:0x6A8],u[0xE60:0xE70],u[0xEA9])==(bool(v[0]&1),v[8:0x18],v[0x698:0x6A8],v[0xE60:0xE70],v[0xEA9])
   name='unit_'+str(slot)+'_stats'
   if not (u[0]&1 and q(u,0x10) and q(u,0x698)):
    assert name not in data;continue
   assert name in data and u[0xEA9]==slot
   stats=data[name];ptr,spawn,definition,cls=[q(u,o) for o in (0x698,0x6A0,0xE60,0xE68)]
   assert reads[name]['address']==ptr and len(stats)==0x1C8
   kind,selector=stats[5],stats[4]
   row=dict(slot=slot,unit=s['pool']+slot*0xF50,actor=q(u,0x10),stats=ptr,spawn=spawn,
            definition=definition,class_row=cls,definition_id=w(stats,4),kind=kind,hp=d(stats,0x48),
            class_is_stats=cls==ptr,class_in_keep_banks=any(p<=cls<p+0x9400 for p in s['keep_bindings']),
            stats_in_battle_block=B<=ptr<B+0x7410)
   if kind==0:
    table=tables['party'];idx=member(definition,table)
    delta=ptr-B-8
    row.update(party_slot=delta//0x1C8 if delta>=0 and delta%0x1C8==0 else None,
      stats_matches_party_slot=ptr==B+8+selector*0x1C8 and selector<40,
      definition_table_row=idx,definition_matches_selector=idx==selector,
      spawn_null=spawn==0,class_null=cls==0,
      stats_bytes_match_bound_block=stats==data['bound_battle_block'][8+selector*0x1C8:8+(selector+1)*0x1C8])
   elif kind==1:
    idx=member(definition,tables['enemy']);class_idx=member(cls,tables['class'])
    authored_class=w(data['enemy_table_rows'],idx*tables['enemy']['stride']) if idx is not None else None
    keep_slot=(spawn-s['keep_bindings'][0])//0x250 if s['keep_bindings'][0]<=spawn<s['keep_bindings'][0]+0x9400 and (spawn-s['keep_bindings'][0])%0x250==0 else None
    delta=ptr-s['keep_bindings'][0]
    row.update(stats_spawn_delta=ptr-spawn,stats_is_embedded=ptr==spawn+0x80,
      primary_keep_slot=keep_slot,definition_table_row=idx,definition_matches_selector=idx==selector,
      class_table_row=class_idx,authored_class_index=authored_class,class_matches_definition=class_idx is not None and class_idx==authored_class,
      stats_bytes_match_keep=0<=delta and delta+0x1C8<=0x9400 and stats==data['keep_bank_1'][delta:delta+0x1C8])
   units.append(row)
  image=data['active_save_image'];block=data['bound_battle_block']
  n=dict(label=label,index=s['index'],start_unix=s['start_unix'],end_unix=s['end_unix'],spans=len(reads),
     image_address_base=base,battle_binding=B,pool=s['pool'],tables=tables,keep_bindings=s['keep_bindings'],units=units,
     loaded_field=w(image,0x1244),history_before=list(struct.unpack('<IHHI',data['field_history_stamp_before'])),
     history_after=list(struct.unpack('<IHHI',data['field_history_stamp_after'])),
     clock_before=d(data['clock_parity_before'],12),clock_after=d(data['clock_parity_after'],12),
     parity_before=data['clock_parity_before'][4],party_levels_first_six=[block[8+i*0x1C8+0x1C2] for i in range(6)],
     keep_nonzero_bytes=[sum(x!=0 for x in data['keep_bank_'+str(i)]) for i in (1,2)],
     keep_sha256=[sha(data['keep_bank_'+str(i)]) for i in (1,2)],
     bound_block_matches_active_image=block==image[B-0x2164280:B-0x2164280+0x7410])
  result['samples'].append(n)
assert spans==88 and len(result['samples'])==4
field=[s for s in result['samples'] if s['label']=='current-field'];assert len(field)==2
assert all(sum(u['kind']==0 for u in s['units'])>0 and sum(u['kind']==1 for u in s['units'])>0 for s in field),'zero-case binding comparison cannot pass'
assert all(s['bound_block_matches_active_image'] for s in result['samples'])
result.update(status='NORMALIZED_SETUP_ONLY',intended_question_status='INCOMPLETE: no older save was loaded in this process',total_spans=spans,
  limits=['Sequential non-atomic reads; identity brackets constrain but do not eliminate temporal gaps.',
          'No native installer/caller trace; observed bindings agree with the original-source paths.',
          'One loaded field and one process; no general lifetime/reuse guarantee.',
          'No combat command, damage, death or group consequence tested.',
          'All observed modules retained; unchanged game text does not certify all modules/data.',
          'No same-session modern-to-old load, inventory/gambit menu, or isolated original-code case here.'])
(E/'observation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
for s in result['samples']:
 print(s['label'],s['index'],'units',len(s['units']),'keep nonzero',s['keep_nonzero_bytes'],'history',s['history_before'],'clock',s['clock_before'])
 for u in s['units']:print(json.dumps(u))
print('Normalized',len(result['samples']),'samples',spans,'full-span reads; preserved C evidence, no new live run.')
