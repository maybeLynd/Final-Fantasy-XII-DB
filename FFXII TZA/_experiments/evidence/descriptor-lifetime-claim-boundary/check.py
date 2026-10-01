import ast,copy,hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def node_integrity(r):
 assert r['variant']=='original' and r['normal_native_return'] and r['end']=='0x62000000'
 assert int(r['entry_rsp'],16)&15==8 and int(r['final_rsp'],16)==int(r['entry_rsp'],16)+8 and 0<r['instruction_count']<1000
 head=int(r['head'],16);assert r['head_after']==[hex(head),hex(head)]
 assert len(r['nodes'])==2 and r['calls_or_stubs']==0
 for addr in r['nodes']:
  n=int(addr,16);before=bytes.fromhex(r['before'][addr]);after=bytes.fromhex(r['after'][addr]);assert len(before)==len(after)==56
  expected=bytearray(before);expected[8:24]=struct.pack('<QQ',n+8,n+8);assert after==bytes(expected)
 allowed={int(r['head'],16),int(r['head'],16)+8,*[int(n,16)+off for n in r['nodes'] for off in [8,16]]}
 assert len(r['write_events'])==8 and all(e['bytes']==8 and int(e['address'],16) in allowed for e in r['write_events'])
 assert len(r['sequence'])==r['instruction_count'] and r['sequence'][-1]=='0x6b6746'
def main():
 s=json.loads((HERE/'source.json').read_text());assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 for ref in s['refs']:
  b=(HERE/ref['retained']).read_bytes();assert len(b)==ref['bytes'] and sha(b)==ref['sha256']
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ins={}
 for body in s['bodies']:
  b=bytes.fromhex(body['raw_hex']);assert len(b)==body['bytes'] and sha(b)==body['sha256']
  decoded=list(md.disasm(b,int(body['entry'],16)));assert sum(i.size for i in decoded)==len(b)
  actual=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in decoded];assert actual==body['instructions'];ins.update({i.address:(i.mnemonic,i.op_str) for i in decoded})
 assert ins[0x6B673D]==('mov','qword ptr [rdx], rdx') and ins[0x6B6740]==('mov','qword ptr [rdx + 8], rdx')
 assert not any(i['op'] in ['call','syscall'] for i in s['bodies'][1]['instructions'])
 assert ins[0x633419]==('je','0x633449')
 assert ins[0x6334F1]==('mov','rcx, qword ptr [rdx]')
 assert ins[0x6334F8]==('mov','qword ptr [rcx + 8], rax')
 assert ins[0x633557]==('lea','rcx, [r15 + 0x60]')
 assert ins[0x63355B]==('call','0x6b6700')
 driver=(HERE/'retained/00-check.py').read_text();tree=ast.parse(driver)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_case')
 obs=next(n.value for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='obs' for t in n.targets))
 keys=[k.value for k in obs.keys];assert keys==['vtbl','counter','reg_head','subnode','objnode','objreg','heads']
 old=json.loads((HERE/'retained/01-result.json').read_text());by={r['name']:r for r in old['cases']}
 for name in ['l90-unowned','la0-mixed','l80-drain','lb0-drain','l60-drain','all-lists']:
  r=by[name];assert r['ok'] and not r['faults'] and set(r['obs'])==set(keys)
  for off in [0x60,0x80,0x90,0xA0,0xB0]:assert r['obs']['heads'][f'{off:x}']==[0x40000000+off]*2
 rows=json.loads((HERE/'raw-results.json').read_text());assert len(rows)==2
 original,mutant=rows;assert original['code_sha256']==s['bodies'][1]['sha256'];node_integrity(original)
 assert mutant['variant']=='node-prev-selflink-NOP-control' and mutant['normal_native_return'] and mutant['head_after']==original['head_after']
 mutation=bytearray.fromhex(s['bodies'][1]['raw_hex']);assert mutation[0x40:0x44].hex()=='48895208';mutation[0x40:0x44]=b'\x90'*4
 assert mutant['code_sha256']==sha(mutation)
 controls=[]
 def reject(name,f):
  try:f()
  except AssertionError:controls.append({'name':name,'rejected':True})
  else:raise AssertionError('control not rejected: '+name)
 bad=copy.deepcopy(mutant);bad['variant']='original';reject('actual NOP control masquerades as intact node state despite equal heads',lambda:node_integrity(bad))
 bad=copy.deepcopy(original);bad['after'][bad['nodes'][0]]=bad['after'][bad['nodes'][0]][:-2];reject('short node span',lambda:node_integrity(bad))
 bad=copy.deepcopy(original);bad['normal_native_return']=False;reject('missing normal native return',lambda:node_integrity(bad))
 original_map={int(i['pc'],16):i for body in s['bodies'] for i in body['instructions']}
 def intended_store(a,n):
  i=original_map[a];assert i['op']=='mov' and i['args']=='qword ptr [rdx + 8], rdx' and len(bytes.fromhex(i['bytes']))==n
 intended_store(0x6B6740,4)
 reject('historical m-selflink four-byte patch at6334F1 is the stated selflink store',lambda:intended_store(0x6334F1,4))
 reject('historical633557 anchor is the helper CALL',lambda:need(ins[0x633557][0]=='call'))
 observation={'result':'MEMBERSHIP_RELEASE_PROVENANCE_SEPARATED; OWNER_REVIEW_PENDING',
 'whole_teardown':'Borrowed +90/+A0 nodes skipped in free-walk are later drained. Current paragraph describing final membership contradicts complete original flow and retained EXP097 head evidence.',
 'native_observer_gap':'EXP097 driver/results retain heads/registry/embedded nodes, not individual list-member spans. Preserve its accepted scope; do not call that full node-heap comparison.',
 'historical_mutation_gap':'EXP097 m-selflink NOP4 at6334F1 begins at a3-byte pointer load and removes first byte of next instruction. Retain recorded kill, but it is not an isolated selflink-store mutation. Intended semantic mutation coverage pending owner repair; original unmodified cases are not retracted.',
 'focused_B':'Original no-call71-byte drain self-links both raw node links and preserves other56-byte-span bytes; one supplied node above4GiB. Labeled NOP leaves heads identical but member prev links wrong, detected by raw-node reducer.',
 'provenance':'No free in this teardown does not distinguish static from external/pool/arena ownership. Actual +B0/+60 allocation sources and cross-state population remain open. Established static field census not retracted.',
 'limits':'Controlled guest nodes and exact entry, no actual initializer/allocator/FF12/live population or free effects. EXP097 allocator remains scripted; historical15/10 campaign not replayed. New B only71-byte helper/original plus labeled mutation.',
 'cleanup':'Guest instances ended with exact return and restored stack. No native OS child, PC/runtime/input/debugger/save/config/reference write or restoration.'}
 (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'result':'PASS_ORIGINAL_AND_OBSERVER_FALSIFICATION','original_cases':1,'labeled_mutation_cases':1,'controls':controls,'fresh_live_runs':0,'independent_acceptance':False},indent=2)+'\n')
 print('PASS original raw-node drain; actual heads-only blind spot demonstrated by one labeled mutation;',len(controls),'controls. Provenance/live unknowns remain.',flush=True)
def need(x):assert x
if __name__=='__main__':main()
