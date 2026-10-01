import hashlib,json,subprocess
from pathlib import Path
import capstone
from operand_direction import memory_role
W=Path(__file__).resolve().parent;H=W/'historical-capstone-access';H.mkdir(exist_ok=False)
src=W/'source.json';before=src.read_bytes();(H/'source.json').write_bytes(before)
s=json.loads(before);b=bytes.fromhex(s['raw_hex'])
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii=list(cs.disasm(b,0x3D8E50));refs=[]
for i in ii:
 for k,o in enumerate(i.operands):
  if o.type==capstone.CS_OP_MEM and cs.reg_name(o.mem.base)=='rip':
   refs.append(dict(pc=hex(i.address),op=i.mnemonic,target=hex(i.address+i.size+o.mem.disp),width=o.size,capstone_access_flag=o.access,access=memory_role(i,k),operand=k))
s['rip_references']=refs;s['access_metadata_correction']='Provider packed-store flags unreliable; restricted mnemonic/operand roles explicit, LEA address only; unsupported forms fail closed. Historical preimage retained, original bytes not recaptured.'
src.write_text(json.dumps(s,indent=2)+'\n')
# Published inputs remain immutable: retain the actual committed source and
# return an additive normalized table, not an in-place edit of package19.
c='58bd6303f9d55d5c84e677d3f6f4b8d99b66b60e';pkg='Database/FFXII TZA/_experiments/evidence/matrix-buffer-alias'
m=json.loads(subprocess.check_output(['git','show',c+':'+pkg+'/manifest.json']))
oldraw=subprocess.check_output(['git','show',c+':'+pkg+'/source.json']);entry=next(x for x in m['members'] if x['path']=='source.json')
assert len(oldraw)==entry['bytes'] and hashlib.sha256(oldraw).hexdigest()==entry['sha256']
(W/'retained/matrix-buffer-alias-source.json').write_bytes(oldraw);old=json.loads(oldraw)
corrected=[];changes=[]
for body in old['bodies']:
 for i in cs.disasm(bytes.fromhex(body['raw_hex']),int(body['entry'],16)):
  for k,o in enumerate(i.operands):
   if o.type==capstone.CS_OP_MEM:
    x=dict(pc=hex(i.address),op=i.mnemonic,operand=k,base=cs.reg_name(o.mem.base),index=cs.reg_name(o.mem.index),disp=o.mem.disp,width=o.size,access=memory_role(i,k),capstone_access_flag=o.access,bytes=i.bytes.hex())
    prior=next(z for z in old['memory_operands'] if z['pc']==x['pc'] and z['operand']==k)
    if prior['access']!=x['access']:changes.append(dict(pc=x['pc'],prior=prior['access'],corrected=x['access'],bytes=x['bytes']))
    corrected.append(x)
assert next(x for x in changes if x['pc']=='0x202b86')['corrected']=='write'
(W/'matrix-buffer-alias-access-correction.json').write_text(json.dumps(dict(parent_commit=c,parent_source_sha256=hashlib.sha256(oldraw).hexdigest(),changes=changes,memory_operands=corrected,limits='Additive metadata correction only. Published235B/31B raw bodies and byte-based alias/staging proof unchanged. Metadata footprints requiring these roles must use this table; no blanket retraction of unrelated A/B/C results.'),indent=2)+'\n')
(H/'receipt.json').write_text(json.dumps(dict(defect='Capstone5.0.7 packed-store operand access flags report READ for native MOVUPS memory destination; LEA is address formation, not memory read.',before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),no_recapture=True,affected_19=changes),indent=2)+'\n')
print('Preserved bad metadata; normalized22 and additive19 roles without recapturing/altering published inputs.',changes,flush=True)
