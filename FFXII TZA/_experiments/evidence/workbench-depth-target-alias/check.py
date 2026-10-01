"""Check exact source obligations. Conditional calculations are NOT original runs."""
import hashlib,json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'source.json').read_text());assert s['method'].startswith('A ')
assert s['reference']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
bb={x['name']:x for x in s['bodies']}
for name,n,h in [('save',89,'ebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda'),('restore',66,'5bb9d143a12bf8959ae1c75d5f7245c4b1081d9ae3432095ebfd253953ec253b')]:
 x=bb[name];raw=bytes.fromhex(x['raw_hex']);assert len(raw)==n and sha(raw)==h==x['sha256']
 assert b''.join(bytes.fromhex(i['bytes']) for i in x['instructions'])==raw
 assert sum(len(bytes.fromhex(i['bytes'])) for i in x['instructions'])==n
for x in s['consumers']:assert sha((W/'retained'/x['retained']).read_bytes())==x['sha256']
ii={int(i['pc'],16):i for b in bb.values() for i in b['instructions']}
def at(pc,raw,mn):
 x=ii[pc];assert x['bytes']==raw and x['mnemonic']==mn,(hex(pc),x);return x
assert at(0x36D953,'4c8d0da62eb502','lea')['rip_targets']==['0x2ec0800']
assert at(0x36D95A,'4c8d059f30b502','lea')['rip_targets']==['0x2ec0a00']
at(0x36D969,'498900','mov');at(0x36D974,'0f1000','movups');at(0x36D977,'410f1141f0','movups')
assert at(0x36D982,'890d80b5f601','mov')['rip_targets']==['0x22d8f08']
assert at(0x36D8E6,'39151cb6f601','cmp')['rip_targets']==['0x22d8f08']
at(0x36D8EC,'762c','jbe');at(0x36D8FC,'ffc2','inc')
at(0x36D8FE,'498b84c1000ada02','mov');at(0x36D906,'410f1084c90008da02','movups')
at(0x36D90F,'0f1100','movups')
assert at(0x36D912,'3b15f0b5f601','cmp')['rip_targets']==['0x22d8f08']
assert at(0x36D918,'72db','jb')['args']=='0x36d8f5'
assert at(0x36D91A,'448905e7b5f601','mov')['rip_targets']==['0x22d8f08']
assert ii[0x36D8EE]['rip_targets']==['0x120000']
contract=(W/'retained/contract.md').read_text()
assert '**Precondition: no save may be outstanding.**' in contract
assert 'for each item the last Save recorded' in contract
assert 'target must not overlap' not in contract.lower() # Scope check, not global semantic search.
DEPTH=0x22D8F08;ROW=0x22D8F90
def conditional_case(name,targets):
 # Source-level transfer, justified by the pinned opcodes above. This is not a
 # reconstructed implementation agreeing with its own fixture as native proof.
 mem={}
 def put(p,b):mem.update({p+i:x for i,x in enumerate(b)})
 def get(p,n):return bytes(mem[p+i] for i in range(n))
 for p in set(targets)|{DEPTH}:put(p,b'\x00'*16 if p==DEPTH else b'\x37'*16)
 put(DEPTH,struct.pack('<I',0))
 saved=[get(p,16) for p in targets] # Save copies before its final depth=count.
 put(DEPTH,struct.pack('<I',len(targets)));put(ROW,b'\xa5'*16)
 visited=[];i=0
 while i<struct.unpack('<I',get(DEPTH,4))[0]:
  assert i<len(targets),'This proof does not classify reads beyond valid saved slots'
  put(targets[i],saved[i]);visited.append(i);i+=1
 put(DEPTH,struct.pack('<I',0))
 return dict(name=name,method='conditional source calculation, not execution',initial_depth=0,targets=[hex(p) for p in targets],saved_hex=[b.hex() for b in saved],restored_indices=visited,row_after=get(ROW,16).hex(),final_depth=struct.unpack('<I',get(DEPTH,4))[0])
cases=[conditional_case('depth-first-skips-later-row',[DEPTH,ROW]),conditional_case('ordinary-disjoint-rows',[0x22D8F30,ROW]),conditional_case('depth-last-restores-both',[ROW,DEPTH])]
assert cases[0]['restored_indices']==[0] and cases[0]['row_after']=='a5'*16
assert cases[1]['restored_indices']==[0,1] and cases[1]['row_after']=='37'*16
assert cases[2]['restored_indices']==[0,1] and cases[2]['row_after']=='37'*16
assert all(x['final_depth']==0 for x in cases)
result=dict(verdict='PASS_STATIC_CONDITIONAL',source_sha256=sha((W/'source.json').read_bytes()),cases=cases,established='Restore rereads depth after each target write; published no-outstanding-Save alone is insufficient for its all-items postcondition under the conditional valid count2 alias layout.',sufficient_precondition='Saved destinations do not overlap the 4B depth counter, and saved pointer/value records remain valid and unchanged until their reads; other ABI/validity/count/noninterference obligations remain.',limits='Nonalias is sufficient, not necessary: depth-last control restores both. No claim that shipped callers use the counter as a target, no whole alias partition, no new runtime/native/live execution or scheduling proof.')
encoded=json.dumps(result,indent=2)+'\n'
if '--derive' in sys.argv:
 assert '/Tools/work/ASTRA/' in W.as_posix() and not (W/'result.json').exists(),'Derivation only in private work with no prior result'
 (W/'result.json').write_text(encoded)
else:
 assert (W/'result.json').exists(),'Missing result is an invalid package, not a pass'
 assert (W/'result.json').read_text()==encoded,'Retained result disagrees with source obligations; preserve it and investigate'
print('PASS_STATIC_CONDITIONAL: post-store depth reload; depth-first versus disjoint/depth-last source controls. No B/C.',flush=True)
