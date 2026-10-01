"""Selected original RT_STRING resource feasibility, no broad export."""
import hashlib,json,struct,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
p=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained/shipping-reader.py');b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
rd=types.ModuleType('reader');rd.__file__=str(p.resolve());exec(compile(b,str(p),'exec'),rd.__dict__);image,ss=rd.load_image();assert hashlib.sha256(image).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
base=0x120000;pe=struct.unpack_from('<I',image,0x3c)[0];opt=pe+24;root,size=struct.unpack_from('<II',image,opt+128);assert root and size
read=lambda off,n:rd.img_rd(image,ss,base+root+off,n)
def directory(off):
 assert 0<=off<=size-16;header=read(off,16);named,ids=struct.unpack_from('<HH',header,12);count=named+ids;assert count<=4096 and off+16+8*count<=size
 return [dict(key=k,target=t,offset=off+16+8*j,hex=read(off+16+8*j,8).hex()) for j in range(count) for k,t in [struct.unpack('<II',read(off+16+8*j,8))]]
def selected(off,key):
 matches=[e for e in directory(off) if e['key']==key];assert len(matches)<=1
 return matches[0] if matches else None
typ=selected(0,6);out=dict(status='PREPARATION_ONLY',exe_sha256=hashlib.sha256(image).hexdigest(),resource_rva=hex(root),directory_bytes=size,id='0x7837',predicted_block='0x784',predicted_entry=7,type_found=bool(typ),limits='Original embedded resource feasibility only; no initialized module/normal runtime lookup/display/cause evidence')
if typ:
 assert typ['target']>>31;block=selected(typ['target']&0x7fffffff,0x784);out['block_found']=bool(block)
 if block:
  assert block['target']>>31;langs=directory(block['target']&0x7fffffff);assert len(langs)<=16;out['languages']=[]
  for lang in langs:
   assert not lang['key']>>31 and not lang['target']>>31 and lang['target']<=size-16
   data=read(lang['target'],16);rva,n,cp,res=struct.unpack('<4I',data);assert res==0 and 32<=n<=65536
   raw=rd.img_rd(image,ss,base+rva,n);pos=0;strings=[]
   for j in range(16):
    assert pos+2<=len(raw);length=struct.unpack_from('<H',raw,pos)[0];start=pos;pos+=2;assert pos+2*length<=len(raw);text=raw[pos:pos+2*length].decode('utf-16le');pos+=2*length;strings.append(dict(index=j,offset=start,u16_length=length,text=text))
   out['languages'].append(dict(language=hex(lang['key']),data_rva=hex(rva),data_size=n,codepage=cp,selected=strings[7],neighbor_lengths=[s['u16_length'] for s in strings],parsed_bytes=pos,trailing_bytes=len(raw)-pos))
(W/'resource-feasibility.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
