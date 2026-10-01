import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text())
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256'] and capstone.__version__==raw['tools']['capstone']
for provider in raw['tools']['provider_files']:assert sha(Path(provider['path']).read_bytes())==provider['sha256'],'Actual decoder provider identity mismatch'
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
parent=json.loads((R/'parent81-raw.json').read_text());assert sha((R/'parent81-raw.json').read_bytes())==raw['reference']['parent81_raw_sha256'] and parent['reference']['exe_sha256']==raw['reference']['exe_sha256']
filterbytes=(R/'parent81-filter240.bin').read_bytes();assert sha(filterbytes)==raw['reference']['parent81_filter_sha256'] and filterbytes[0x79ade0-0x79ad50:0x79ade5-0x79ad50].hex()=='b937780000'
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed access policy','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
allins={};traps=[]
for f in raw['functions']:
 entry=int(f['entry'],16);code=(R/(f['name']+'.bin')).read_bytes();assert len(code)==f['bytes'] and sha(code)==f['sha256'];todo=[entry];seen={};term=[]
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  assert entry<=pc<entry+len(code);i=next(cs.disasm(code[pc-entry:pc-entry+15],pc));assert pc+i.size<=entry+len(code);seen[pc]=i
  if i.mnemonic in ('ret','int3','ud2'):
   term.append(dict(pc=hex(pc),kind=i.mnemonic))
   if i.mnemonic=='int3':traps.append(pc)
   continue
  if i.mnemonic.startswith('j'):
   assert i.operands[0].type==capstone.CS_OP_IMM;todo.append(i.operands[0].imm)
   if i.mnemonic=='jmp':continue
  todo.append(pc+i.size)
 rows=sorted(seen.values(),key=lambda i:i.address);assert len(rows)==len(f['instructions']) and sorted(term,key=lambda t:t['pc'])==sorted(f['terminals'],key=lambda t:t['pc'])
 for i,row in zip(rows,f['instructions']):
  assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(row['pc'],row['hex'],row['mnemonic'],row['args'])
  assert sorted(roles.written(i))==row['written'] and [roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]==row['memory']
 allins.update(seen)
assert set(traps)=={0x80c597} and 0x80c598 not in allins and 0x80c5a0 not in allins
for b,index,want in [('8900',0,'w'),('8d00',1,'addr'),('830001',0,'rw')]:
 i=next(cs.disasm(bytes.fromhex(b),0));assert roles.op_kind(i,i.operands[index],index)==want
for pc,want in [(0x19a524,'8be9'),(0x19a52f,'33db'),(0x19a544,'7546'),(0x19a548,'448d4306'),(0x19a54c,'c1e804'),(0x19a552,'66ffc0'),(0x19a555,'0fb7d0'),(0x19a60a,'83e70f'),(0x19a615,'0fb703'),(0x19a618,'488d1c43'),(0x19a61c,'4883c302'),(0x19a630,'663903'),(0x19a633,'480f44d8'),(0x80c542,'3b5e58'),(0x80c550,'488b7e10'),(0x80c578,'488b4650'),(0x80c57c,'488b3cd8')]:assert allins[pc].bytes.hex()==want
assert allins[0x19a528].address+allins[0x19a528].size+allins[0x19a528].operands[1].mem.disp==0x2eaf320
imports={int(r['slot'],16):r for r in raw['imports']};slots={i.address+i.size+i.operands[0].mem.disp for i in allins.values() if i.mnemonic=='call' and i.operands[0].type==capstone.CS_OP_MEM};assert set(imports)==slots
symbols={r['symbol'] for r in imports.values()};assert symbols=={'FindResourceW','LoadResource','LockResource','SizeofResource','EnterCriticalSection','LeaveCriticalSection','RaiseException'} and all(r['dll']=='KERNEL32.dll' and r['ordinal'] is None for r in imports.values())
root=raw['resource'];assert root['type']==6 and int(root['block'],16)==((0x7837>>4)+1)&0xffff and root['entry']==(0x7837&15)==7
dirs={d['offset']:d for d in root['directories']}
def entries(off):
 d=dirs[off];b=(R/d['copy']).read_bytes();assert sha(b)==d['sha256'];named,ids=struct.unpack_from('<HH',b,12);assert len(b)==16+8*(named+ids)
 return [struct.unpack_from('<II',b,16+8*j) for j in range(named+ids)]
typeset=entries(0);ty=[t for k,t in typeset if k==6];assert len(ty)==1 and ty[0]>>31
blocks=entries(ty[0]&0x7fffffff);bl=[t for k,t in blocks if k==0x784];assert len(bl)==1 and bl[0]>>31
langs=entries(bl[0]&0x7fffffff);assert len(langs)==len(root['strings'])==9
observations=[]
for s in root['strings']:
 lang=int(s['language'],16);assert (lang,s['data_entry_offset']) in langs
 data=bytes.fromhex(s['data_entry_hex']);rva,n,cp,res=struct.unpack('<4I',data);assert (hex(rva),n,cp,res)==(s['data_rva'],s['size'],s['codepage'],0)
 b=(R/s['copy']).read_bytes();assert len(b)==n and sha(b)==s['sha256'];pos=0;strings=[]
 for j in range(16):
  assert pos+2<=n;start=pos;count=struct.unpack_from('<H',b,pos)[0];pos+=2;assert pos+2*count<=n;text=b[pos:pos+2*count].decode('utf-16le');pos+=2*count
  strings.append(dict(index=j,prefix_offset=start,u16_length=count,utf16_hex=b[start+2:pos].hex(),text=text))
 assert pos==n and strings[7]['u16_length']>0 and strings[6]['prefix_offset']<strings[7]['prefix_offset']<strings[8]['prefix_offset']
 observations.append(dict(language=s['language'],rva=s['data_rva'],selected=strings[7],previous=strings[6],following=strings[8],all16_lengths=[x['u16_length'] for x in strings],parsed_bytes=pos))
english=next(o for o in observations if o['language']=='0x409');assert english['selected']['text']=='Fatal error encountered.' and english['selected']['u16_length']==24 and english['selected']['prefix_offset']==346
assert english['previous']['text']!=english['selected']['text'] and english['following']['text']!=english['selected']['text']
if '--fault-index-six' in sys.argv:assert english['previous']['text']=='Fatal error encountered.','Original id7837 selects entry7, not neighboring entry6'
if '--fault-terminator' in sys.argv:assert english['selected']['utf16_hex'].endswith('0000'),'RT_STRING stores counted UTF16; no included nul terminator for this entry'
if '--fault-trap-fallthrough' in sys.argv:assert 0x80c5a0 in allins,'INT3 is a terminal boundary; adjacent routine is not local CFG evidence'
result=dict(status='STATIC_EMBEDDED_ERROR_RESOURCE_AND_LOOKUP_PRECONDITIONS',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),strings=observations,
 interpretation='Input7837 requests RT_STRING type6 block784, entry7. Selected embeddedEXE entry409 is Fatal error encountered. (24 UTF16 codeunits, counted prefix, no included nul). Nine original language variants individually retained. Lookup enumerates registry2EAF320 via80C51C, FindResourceW on nonnull module then LoadResource/LockResource/SizeofResource selector; returns pointer to nonempty selected length prefix, not text+2 and not owned allocation. Module initialization/order/language selection/load success/lifetime/visiblemessage unobserved. Getter source uses signed index bounds, +58 bound, +10 at equal bound, +50 indexed pointer otherwise; traps stop local graph. Current pointer-end checks are not complete malformed-resource safety.',
 consumer_change='Add exact embedded CV3 body with module/language/borrowed-prefix qualifiers; do not call it captured displayed text or explain EXP127. Connect helper counted string to filter leadingu16/pointer+2, preserve API/callback/native ownership limits. Exclude trap fallthrough/adjacent-function source.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS82 original selected resource/lookup/trap-boundary controls, no native/live execution',flush=True)
