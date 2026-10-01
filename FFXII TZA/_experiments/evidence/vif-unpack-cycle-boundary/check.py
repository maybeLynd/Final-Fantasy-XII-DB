import copy, hashlib, importlib.util, json, struct, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
EXPECTED={'0x22bff0':'c88b16447482201c1627caf6e2ae1f61dbdcba1bb8f1ac9e2fd1f6f0252890ce',
 '0x22c970':'6f08de7d67b7ead7557bb05c85f0a2fbe8b244a46514a37f151c19e3e19d41dd'}
def check_source(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 assert {b['entry']:b['sha256'] for b in s['bodies']}==EXPECTED
 for b in s['bodies']:
  raw=bytes.fromhex(b['raw_hex']);assert sha(raw)==b['sha256'] and len(raw)==b['size']
  pc=int(b['entry'],16)
  for i in b['instructions']:
   assert int(i['pc'],16)==pc
   ib=bytes.fromhex(i['bytes']);assert raw[pc-int(b['entry'],16):pc-int(b['entry'],16)+len(ib)]==ib
   pc+=len(ib)
  assert pc==int(b['entry'],16)+b['size'] and b['instructions'][-1]['op']=='ret'
 for p in s['consumer_preimages']:
  data=(HERE/p['retained']).read_bytes();assert sha(data)==p['sha256'] and len(data)==p['bytes']
 assert sha((HERE/s['retained_reader']).read_bytes())==s['reader_sha256']
 for b,g in zip(s['bodies'],s['pe_runtime_function_groups']):
  assert b['entry']==g['entry'] and int(g['end'],16)==int(b['entry'],16)+b['size']
  assert len(g['contiguous_entries'])==3
  cursor=int(b['entry'],16)
  first=g['contiguous_entries'][0]
  parent=[int(first[k],16)-0x120000 for k in ['begin','end','unwind']]
  for i,p in enumerate(g['contiguous_entries']):
   assert int(p['begin'],16)==cursor;cursor=int(p['end'],16)
   assert p['chain_parent']==(None if i==0 else parent)
def source_reads(r,only_v45=False):
 src=int(r['source_address'],16)
 return [e for e in r['events'] if e['kind']=='read' and src<=int(e['address'],16)<src+128
  and (not only_v45 or e['pc'] in ['0x22c840','0x22c852','0x22c863','0x22c874'])]
def verify_results(rs):
 names=[f'{fmt}-CL{cl}' for fmt in ['V2-32','V4_5','V4-32'] for cl in [1,2,3]]+['V4_5-decoder-CL2','V4_5-guard-CL1','V4_5-guard-CL2']
 assert [r['name'] for r in rs]==names and len(rs)==12
 normalized=[]
 for r in rs:
  src=int(r['source_address'],16);dst=int(r['destination_address'],16)
  assert int(r['entry_rsp'],16)%16==8 and 0<r['instruction_count']<5000 and len(r['steps'])==r['instruction_count']
  assert r['stubs']==[] and r['before']['source']==r['after']['source']
  assert struct.unpack_from('<II',bytes.fromhex(r['before']['globals']))==(r['cycle'],r['cycle'])
  before=bytes.fromhex(r['before']['destination']);after=bytes.fromhex(r['after']['destination'])
  assert len(before)==len(after)==128 and before[:16]==after[:16] and before[64:]==after[64:]
  if r['name']=='V4_5-guard-CL2':
   assert not r['returned'] and r['failure']=='Invalid memory read (UC_ERR_READ_UNMAPPED)'
   assert r['faults']==[{'access':19,'pc':'0x22c840','address':hex(src+8),'size':2}]
   assert after[32:]==before[32:] and len([e for e in r['events'] if e['kind']=='write' and dst<=int(e['address'],16)<dst+48])==4
   normalized.append({'name':r['name'],'status':'CONTROLLED_GUEST_FAULT','fault_source_offset':8,'limits':'Partial operation, no return; not a live crash.'});continue
  assert r['returned'] and not r['faults'] and not r['failure'] and r['nonvolatile_preserved']
  assert int(r['final_rsp'],16)==int(r['entry_rsp'],16)+8 and r['final_rip']=='0x62000000'
  assert r['return_eax']==(20 if r['decoder'] else {'V2-32':24,'V4_5':8,'V4-32':48}[r['format']])
  assert r['calls']==([] if not r['decoder'] else [{'pc':'0x22cac7','bytes':'e824f5ffff','op':'call','args':'0x22bff0'}])
  cl=r['cycle']
  if r['format']=='V2-32':offsets={1:[0,4,8,12,16,20],2:[0,4,4,8,16,20],3:[0,4,4,8,8,12]}[cl];width=4;repeats=1
  elif r['format']=='V4_5':offsets={1:[0,2,4],2:[0,8,4],3:[0,8,16]}[cl];width=2;repeats=4
  else:offsets=list(range(0,48,4));width=4;repeats=1
  reads=source_reads(r,r['format']=='V4_5');payload_shift=8 if r['decoder'] else 0
  expected=[x+payload_shift for x in offsets for _ in range(repeats)]
  assert [(int(e['address'],16)-src,e['size']) for e in reads]==[(x,width) for x in expected]
  data=bytes.fromhex(r['before']['source'])
  for e in reads:
   at=int(e['address'],16)-src;assert e['value_hex']==data[at:at+e['size']].hex()
  # Reconstruct actual stores from observed source bytes, independently of final snapshot.
  expected_dest=bytearray(before)
  if r['format']=='V4_5':
   for j,at in enumerate(offsets):
    w=struct.unpack_from('<H',data,at+payload_shift)[0]
    struct.pack_into('<4I',expected_dest,16+16*j,(w&31)<<3,(w>>2)&248,(w>>7)&248,(w>>8)&128)
  elif r['format']=='V2-32':
   for j in range(3):expected_dest[16+16*j:24+16*j]=data[offsets[j*2]:offsets[j*2]+4]+data[offsets[j*2+1]:offsets[j*2+1]+4]
  else:expected_dest[16:64]=data[:48]
  assert after==expected_dest
  writes=[e for e in r['events'] if e['kind']=='write' and dst<=int(e['address'],16)<dst+48]
  assert len(writes)==(6 if r['format']=='V2-32' else 12)
  expected_write_offsets=[j*16+k*4 for j in range(3) for k in range(2 if r['format']=='V2-32' else 4)]
  assert [(int(e['address'],16)-dst,e['size']) for e in writes]==[(x,4) for x in expected_write_offsets]
  for e in writes:
   at=int(e['address'],16)-dst;assert e['value_hex']==after[16+at:20+at].hex()
  if r['decoder']:
   assert [(int(e['address'],16)-src,e['value_hex']) for e in source_reads(r) if e['pc']=='0x22c9d6']==[(0,'02020001'),(4,'0000036f'),(16,'05050001')]
   g=bytes.fromhex(r['after']['globals']);assert struct.unpack_from('<II',g)==(5,5)
   # The halfword at relative16 was read as payload before the same address was parsed as the next command.
   payload_hit=next(i for i,e in enumerate(r['events']) if e['pc']=='0x22c840' and int(e['address'],16)==src+16)
   header_hit=next(i for i,e in enumerate(r['events']) if e['pc']=='0x22c9d6' and int(e['address'],16)==src+16)
   assert payload_hit<header_hit
  normalized.append({'name':r['name'],'status':'ORIGINAL_RETURN','source_element_offsets':offsets,
   'nominal_return_bytes':r['return_eax'],'actual_payload_read_end':max(offsets)+width,
   'destination_written_bytes':sum(e['size'] for e in writes),
   'next_command_also_read_as_payload':r['decoder'],'instruction_count':r['instruction_count']})
 return normalized
def main():
 s=json.loads((HERE/'source.json').read_text());rs=json.loads((HERE/'raw-results.json').read_text())
 check_source(s);norm=verify_results(rs)
 controls=[]
 def reject(name,fn):
  try:fn()
  except (AssertionError,KeyError,ValueError):controls.append({'name':name,'rejected':True});return
  raise AssertionError('INVALID_CONTROL accepted '+name)
 x=copy.deepcopy(rs);x[3]['events']=[];reject('missing-source-observer',lambda:verify_results(x))
 x=copy.deepcopy(rs);x[1]['return_eax']=12;reject('actual-read-end-substituted-for-return',lambda:verify_results(x))
 x=copy.deepcopy(rs);x[3]['after']['destination']=x[4]['after']['destination'];reject('universal-stride-error-at-CL1',lambda:verify_results(x))
 x=copy.deepcopy(rs);x[9]['events']=[e for e in x[9]['events'] if not(e['pc']=='0x22c9d6' and int(e['address'],16)==int(x[9]['source_address'],16)+16)];reject('next-header-not-observed',lambda:verify_results(x))
 x=copy.deepcopy(rs);x[-1]['returned']=True;x[-1]['failure']=None;reject('guard-fault-promoted-to-completion',lambda:verify_results(x))
 x=copy.deepcopy(rs);x[6]['after']['destination']=x[7]['before']['destination'];reject('positive-format-control-broken',lambda:verify_results(x))
 x=copy.deepcopy(s);x['bodies'][0]['raw_hex']='90'+x['bodies'][0]['raw_hex'][2:];reject('changed-original-body',lambda:check_source(x))
 reject('zero-case-run',lambda:verify_results([]))
 (HERE/'observation.json').write_text(json.dumps({'cases':norm,'limits':s['limits'],'semantic_status':'SUPPORTED BOUNDED B; canonical propagation and independent review pending'},indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS','valid_original_returns':11,'controlled_guest_faults':1,'cases':12,'controls':controls,'reran_original_code':False},indent=2)+'\n')
 print('PASS: 11 original returns, 1 labeled guard fault, 8 corruption controls. Reducer only; no execution repeated.')
if __name__=='__main__':main()
