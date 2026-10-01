import copy,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def identity(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert len(s['tables'])==36 and len(s['bodies'])==10
 targets=set()
 for i,t in enumerate(s['tables']):
  assert int(t['address'],16)==0xD61E50+i*0x50
  q=struct.unpack('<10Q',bytes.fromhex(t['raw_hex']))
  assert q[4]==0x6571C0 and t['slot4']==hex(q[4]) and t['slot5']==hex(q[5]) and t['slot6']==hex(q[6])
  targets.add(q[6])
 assert targets=={0x65B8F0,0x65B270,0x65B340,0x65B400,0x65B4C0,0x65B590,0x65B650,0x65B750,0x65B820,0x65B920}
 assert {int(b['entry'],16) for b in s['bodies']}==targets
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert len(raw)==b['bytes']==int(b['PE_end'],16)-int(b['entry'],16) and sha(raw)==b['sha256']
  i=next(md.disasm(raw,int(b['entry'],16)));assert b['entry_instruction']=={'size':i.size,'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str}
def retained(arm,result,audit,control,ready):
 assert result['status']==control['status']=='PASS' and result['detach'] and not result['errors']
 assert result['cleanup']['status']=='PASS' and control['capture_exit']==0 and control['final_exits']==[0,1]
 assert all(ok for _,ok in result['cleanup']['clears']+result['cleanup']['verified'])
 assert len(control['post'])==4 and all(p['exit'] is None and p['debugger'] is False for p in control['post'])
 assert all(b['beats']>a['beats'] for a,b in zip(control['post'],control['post'][1:]))
 stacks=[(i,e) for i,e in enumerate(audit) if e['operation']=='stopped_stack_read']
 assert len(stacks)==len(result['hits'])==control['hits']==(41 if arm=='positive' else 0)
 assert ready['entry']==ready['address']+32 and ready['return_address']==ready['address']+9
 for j,(pos,e) in enumerate(stacks):
  hit=result['hits'][j];raw=bytes.fromhex(e['raw'])
  assert e['status']=='READ' and len(raw)==e['bytes_read']==64 and hit['stack']['raw']==e['raw']
  assert e['qwords']==list(struct.unpack('<8Q',raw)) and e['top_qword']==e['qwords'][0]==ready['return_address']
  prev=next(x for x in reversed(audit[:pos]) if x['operation'] in ['WaitForDebugEvent','ContinueDebugEvent'])
  nxt=next(x for x in audit[pos+1:] if x['operation'] in ['WaitForDebugEvent','ContinueDebugEvent'])
  assert prev['operation']=='WaitForDebugEvent' and prev['exception']==0x80000004 and nxt['operation']=='ContinueDebugEvent' and nxt['result']
  assert e['tid']==hit['tid']==prev['tid']==nxt['tid'] and e['rip']==hit['rip']==ready['entry']
 return len(stacks)
def main():
 s=json.loads((HERE/'source.json').read_text());identity(s)
 for ref in s['refs']:
  b=(HERE/ref['retained']).read_bytes();assert len(b)==ref['bytes'] and sha(b)==ref['sha256']
 load=lambda n:json.loads((HERE/'retained'/n).read_text())
 arms={a:[load(a+'-'+n) for n in ['capture-result.json','capture-api.json','control.json','target-ready.json']] for a in ['positive','cold']}
 count={a:retained(a,*data) for a,data in arms.items()}
 controls=[]
 def reject(name,f):
  try:f()
  except (AssertionError,StopIteration):controls.append({'name':name,'rejected':True})
  else:raise AssertionError('control not rejected: '+name)
 bad=copy.deepcopy(s);bad['tables'][0]['slot6']=bad['tables'][0]['slot5'];reject('pass-query slot substituted for render target',lambda:identity(bad))
 bad=copy.deepcopy(arms['positive']);bad[0]['hits']=[];reject('positive zero-case label',lambda:retained('positive',*bad))
 bad=copy.deepcopy(arms['positive']);next(e for e in bad[1] if e['operation']=='stopped_stack_read')['top_qword']+=1;reject('wrong stopped return address',lambda:retained('positive',*bad))
 bad=copy.deepcopy(arms['positive']);next(e for e in bad[1] if e['operation']=='stopped_stack_read')['bytes_read']=8;reject('incomplete stack read',lambda:retained('positive',*bad))
 bad=copy.deepcopy(arms['positive']);pos=next(i for i,e in enumerate(bad[1]) if e['operation']=='stopped_stack_read');prev=next(i for i in reversed(range(pos)) if bad[1][i]['operation'] in ['WaitForDebugEvent','ContinueDebugEvent']);bad[1][prev]['operation']='ContinueDebugEvent';reject('read after continuation',lambda:retained('positive',*bad))
 observation={'result':'A_PREFLIGHT; ACTUAL_C_CALLER_OPEN','original_tables':36,'original_render_entries':10,'historical_stopped_stack_reads':count,
 'instrument_gap':'Accepted EXP038 stack reader resides in old foreign-step-defective duration-only capture; accepted corrected EXP127 dispatch has no stack capture or first-hit cap. Qualifications do not compose automatically.',
 'state_gap':'No exact save/scene/preset instantiating selected effect or current consumer acceptance supplied.',
 'acceptance_limit':'One verified receiver/caller observation is state-specific; not per-frame cadence or pass-list traversal. Actual slot-6 ABI required before argument interpretation.',
 'cleanup':'Offline file reads only; no native child, FF12 process, PC control, input, debugger or save/config/reference writes.'}
 (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'result':'PASS_BOUNDED_SOURCE_AND_RETAINED_RECEIPTS','rejecting_controls':controls,'fresh_native_runs':0,'fresh_live_runs':0,'independent_acceptance':False},indent=2)+'\n')
 print('PASS original entry identities /41 retained stopped reads and cold0;',len(controls),'rejecting controls; actual C remains open',flush=True)
if __name__=='__main__':main()
