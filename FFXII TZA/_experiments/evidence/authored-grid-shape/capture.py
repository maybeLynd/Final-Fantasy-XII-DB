"""Exact original loader and one authored section; static only, no native run."""
import hashlib,importlib.util,json,struct,sys,capstone
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
w=Path(__file__).resolve().parent;w.mkdir(exist_ok=True)
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
spec=importlib.util.spec_from_file_location('shipping_reader',reader)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw,secs=m.load_image()
def body(entry,size):
 b=m.img_rd(raw,secs,entry,size)
 ii=list(Cs(CS_ARCH_X86,CS_MODE_64).disasm(b,entry))
 assert ii and ii[0].address==entry and ii[-1].mnemonic=='ret' and ii[-1].address+ii[-1].size==entry+size
 return {'entry':hex(entry),'size':size,'sha256':hashlib.sha256(b).hexdigest(),'raw_hex':b.hex(),
         'instructions':[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii]}
loader=body(0x384160,372);decoder=body(0x20e600,10);encoder=body(0x20e620,9)
prior=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-quantization/source.json')
prior_bytes=prior.read_bytes();j=json.loads(prior_bytes)
assert j['exe_sha256']==m.SHA
assert {int(b['entry'],0) for b in j['bodies']} >= {0x3924b0,0x383740,0x20e600}
mpk=Path('D:/FFXII_TZA_extract/ps2data/plan_master/map_ctrl/alc01/alc0102/bin/alc0102.mpk')
d=mpk.read_bytes();n=struct.unpack_from('<I',d,0)[0];assert 4<n<128
sizes=struct.unpack_from('<%dI'%n,d,4)
pos=((n+1)*4+0x3f)&~0x3f
for i,z in enumerate(sizes):
 if not z:continue
 pos+=0x40;assert pos+z<=len(d)
 if i==4:
  section=d[pos:pos+z];section_pos=pos;break
 pos+=z
else:raise AssertionError('missing slot4')
assert len(section)==3200 and struct.unpack_from('<I',section,0)[0]==1
offsets=[struct.unpack_from('<I',section,o)[0] for o in (0xC,0x10,0x14,0x18,0x1C,0x20)]
assert all(0<o<len(section) for o in offsets)
grid=offsets[-1];assert grid+16<=len(section)
cw,ch,cols,rows=struct.unpack_from('<4B',section,grid)
ox,oz=struct.unpack_from('<hh',section,grid+4)
table,pool=struct.unpack_from('<II',section,grid+8)
assert (cw,ch,cols,rows)==(5,5,10,10) and (ox,oz)==(63,13)
assert 0<table and table+2*cols*rows<=len(section) and 0<pool<len(section)
regions=struct.unpack_from('<H',section,10)[0];assert 0<regions<=128
nonempty=0
for k in range(cols*rows):
 off=struct.unpack_from('<H',section,table+2*k)[0]
 if off==0xffff:continue
 nonempty+=1;q=pool+off;assert 0<=q<len(section)
 while q<len(section) and section[q]!=0xff:
  assert section[q]<regions
  q+=1
 assert q<len(section)
assert nonempty>0
(w/'slot4.bin').write_bytes(section)
out={'method':'A static/captured original image and one extracted authored copy, no execution','exe_sha256':m.SHA,
     'capstone_version':capstone.__version__,'python_version':sys.version,'python_executable':sys.executable,
     'python_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
     'reader_path':reader.as_posix(),'reader_sha256':hashlib.sha256(reader.read_bytes()).hexdigest(),
     'bodies':[loader,decoder,encoder],'prior_constructor_source':prior.as_posix(),
     'prior_constructor_source_sha256':hashlib.sha256(prior_bytes).hexdigest(),
     'map_pack':{'path':str(mpk),'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d),'slot':4,
                 'slot_offset':section_pos,'slot_size':len(section),'slot_sha256':hashlib.sha256(section).hexdigest(),
                 'grid_offset':grid,'grid_header_hex':section[grid:grid+16].hex(),'origin':[ox,oz],
                 'cell_size':[cw,ch],'counts':[cols,rows],'rectangle_size':[cw*cols,ch*rows],
                 'cell_table_offset':table,'list_pool_offset':pool,'region_count':regions,'nonempty_cells':nonempty,
                 'positive_controls':'valid MPK slot bounds, nav section marker/offsets, nonzero grid, all 100 table entries terminate valid region lists'},
     'limits':'Shipped extracted copy occurrence, not live initialized grid or builder call. Reference and map pack read only.'}
(w/'source.json').write_text(json.dumps(out,indent=2)+'\n')
print('Captured exact loader/codec and alc0102 slot4; rectangle',cw*cols,ch*rows,'valid nonempty',nonempty,flush=True)
