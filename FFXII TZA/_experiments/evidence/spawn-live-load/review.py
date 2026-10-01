"""Review retained live captures only; never opens a process or modifies saves."""
from pathlib import Path
import hashlib,json,struct
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]; raw_states={}
for label in ('fresh-title','old-complete','old-field'):
 p=E/(label+'-memory.json');j=json.loads(p.read_text())
 assert j['status']=='OBSERVED' and j['pid']==46768 and j['read_handle_closed']
 assert j['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert j['module_verdict']=='clean' and j['modules'] and not j['watched_modules']
 assert j['image_base']==0x120000 and j['known_read_control']=='19930d0a1a0a' and j['null_read_rejected']
 assert len(j['code_identity'])==1 and j['code_identity'][0]['matches']
 assert j['code_identity'][0]['bytes']==7996981
 assert j['code_identity'][0]['disk_sha256']==j['code_identity'][0]['live_sha256']=='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
 assert len(j['samples'])==2
 for index,s in enumerate(j['samples']):
  assert s['binding_stable'] and s['keep_bindings_stable'] and s['binding_matches_active_image']
  assert s['battle_binding']==0x21B290C and s['keep_bindings']==[0x6752FF80,0x67526B40]
  assert len(s['reads'])==14 and len({x['name'] for x in s['reads']})==14
  r={x['name']:bytes.fromhex(x['bytes']) for x in s['reads']}
  for x in s['reads']:assert len(r[x['name']])==x['size'] and sha(r[x['name']])==x['sha256']
  b=r['bound_battle_block'];im=r['active_save_image'];legacy=im[0x2200:0x8200]
  assert len(b)==0x7410 and len(im)==0x56690 and b==im[0x4E68C:0x4E68C+0x7410]
  bank0_matches=[b[0x5B10+i*0x9C:0x5B44+i*0x9C]==b[0x90+i*0x1C8:0xC4+i*0x1C8] for i in range(40)]
  old_matches=[b[0x5B10+i*0x9C:0x5B44+i*0x9C]==legacy[0x90+i*0x1C8:0xC4+i*0x1C8] for i in range(40)]
  def history(name):
   window,last,previous,stamp=struct.unpack('<IHHI',r[name]);return dict(window_seconds=window,last_field=last,previous_field=previous,transition_stamp=stamp)
  def clock(name):return dict(parity=r[name][4],raw_tick=struct.unpack_from('<I',r[name],12)[0])
  row=dict(label=label,sample=index,start_unix=s['start_unix'],end_unix=s['end_unix'],source_sha256=sha(p.read_bytes()),module_count=len(j['modules']),block_sha256=sha(b),legacy_sha256=sha(legacy),pre_gambit_prefix_matches_legacy=b[:0x5B10]==legacy[:0x5B10],stamp=hex(struct.unpack_from('<I',b)[0]),block_flags=hex(struct.unpack_from('<I',b,4)[0]),levels_first_six=[b[8+i*0x1C8+0x1C2] for i in range(6)],selected_banks=list(struct.unpack_from('<40i',b,0x7370)),bank0_matches_local_old_record=sum(bank0_matches),bank0_matches_saved_compatibility_record=sum(old_matches),member0_gambit_banks=[b[0x5B10+k*0x34:0x5B44+k*0x34].hex() for k in range(3)],field_id=struct.unpack_from('<H',im,0x1244)[0],history_before=history('history_window_stamp_before'),history_after=history('history_window_stamp_after'),clock_before=clock('clock_parity_before'),clock_after=clock('clock_parity_after'),keep_banks=[dict(bank=k,sha256=sha(r['keep_bank_'+str(k)]),nonzero_bytes=sum(v!=0 for v in r['keep_bank_'+str(k)])) for k in (1,2)])
  rows.append(row);raw_states[(label,index)]=r
assert len(rows)==6
for row in rows:
 assert row['stamp']=='0x5071901' and row['selected_banks']==[0]*40
 assert row['history_before']==row['history_after']
 assert all(x['nonzero_bytes']==0 for x in row['keep_banks'])
 if row['label']!='fresh-title':
  assert row['pre_gambit_prefix_matches_legacy'] and row['bank0_matches_saved_compatibility_record']==40
  assert row['levels_first_six']==[21]*6 and row['field_id']==0x132
title=raw_states[('fresh-title',0)]['bound_battle_block'];loaded=raw_states[('old-complete',0)]['bound_battle_block']
assert title!=loaded
delta=[i for i,(a,b) in enumerate(zip(title,loaded)) if a!=b]
bad=json.loads((E/'fresh-title-first-attempt-memory.json').read_text())
assert bad['status']=='INVALID' and bad['module_verdict']=='unreadable' and not bad['samples']
before=json.loads((E/'save-before.json').read_text());cleanup=json.loads((E/'cleanup.json').read_text())
assert len(before['files'])==26 and before['files']==cleanup['files'] and cleanup['status']=='RESTORED'
assert cleanup['changed_keys']==['LUIDLow'] and cleanup['processes']==[] and cleanup['backup_unchanged']
inputs=json.loads((E/'save-inputs.json').read_text());old=next(x for x in inputs if x['name']=='FFXII_004')
assert old['declared_size']==0x4E690 and old['EXP015_identical'] and old['sha256']=='8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc'
ns={};exec((E/'clock-primary.py').read_text().split('for a in (')[0],ns)
cb=json.loads((E/'clock-primary.json').read_text())['bodies'];assert len(cb)==1
cb=cb[0];assert cb['address']=='0x32a160' and cb['bytes']==11
offset=ns['off'](0x32A160-ns['ib']);assert sha(ns['raw'][offset:offset+11])==cb['sha256']=='341fefc95f92b91553bba7849a9993eae55b49f0f801a48a3627554493d4a845'
assert [(i['mnemonic'],i['operands']) for i in cb['instructions']]==[('mov','dword ptr [rip + 0x1d632f2], 0'),('ret','')]
assert cb['instructions'][0]['rip_targets'][0]['address']=='0x208d45c'
out=dict(status='PASS_BOUNDED_OBSERVATIONS',method='C: ordinary launch/manual004 load with read-only process snapshots; no calls, hooks, writes or suspension',observed_states=3,samples=rows,complete_full_span_reads=84,block_changes_title_to_complete=dict(bytes=len(delta),first=hex(delta[0]),last=hex(delta[-1])),old_input=old,invalid_attempt_preserved=True,cleanup_verified=True,limits=['Three observed states, not a completed current-versus-old or same-session comparison.','Sequential reads are not atomic. Matching binding/duplicate reads do not establish intermediate writers or native call order.','Both keep banks were entirely zero in all six samples, so bank preservation, copying, swapping and wiping cannot be distinguished here.','Selected sets were already0 at title. Their zero after load cannot independently prove a selector-reset write. Exact bank0/compatibility equality and differing content support the source-derived import interpretation.','The menu metadata showed gil9999999 and six level21 portraits; loaded block independently establishes six level21 records. Live inventory/gambit menu presentation was not inspected.','No claim that every keyboard method fails: Down,k,R produced no observed game response; mouse wheel/confirm and OS exit did. Existing input delivery receipts require review before expanding this method.','Native233C10/235AF0/2EF4A0 execution is inferred by composition, not directly traced. No player-visible enemy respawn consequence observed.'])
(E/'review.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(out['status'],'3 states,6 samples,84 full-span reads,26 restored files; INVALID attempt excluded.')
print('Block changed bytes:',len(delta),'first/last',hex(delta[0]),hex(delta[-1]))
for row in rows:print(row['label'],row['sample'],'levels',row['levels_first_six'],'bank0 legacy matches',row['bank0_matches_saved_compatibility_record'],'field',hex(row['field_id']),'history',row['history_before'],'clock',row['clock_before'])
