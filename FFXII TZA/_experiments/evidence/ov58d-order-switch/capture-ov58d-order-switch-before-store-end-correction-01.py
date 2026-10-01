"""Original compressed order switch; bounded static source/data capture only."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in W.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def module(name,f):
 s=importlib.util.spec_from_file_location(name,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 out=pathlib.Path(sys.argv[1])
 if out.exists():raise ValueError('immutable output exists')
 d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong reference image')
 pe=struct.unpack_from('<I',d,60)[0];opt=pe+24;base=struct.unpack_from('<Q',d,opt+24)[0]
 if base!=0x120000:raise ValueError('wrong image base')
 ss=[struct.unpack_from('<IIII',d,opt+struct.unpack_from('<H',d,pe+20)[0]+40*i+8) for i in range(struct.unpack_from('<H',d,pe+6)[0])]
 def read(pc,n):
  for _,va,rs,ro in ss:
   if base+va<=pc and pc+n<=base+va+rs:return d[ro+pc-base-va:ro+pc-base-va+n]
  raise ValueError('unbacked source')
 er,en=struct.unpack_from('<II',d,opt+112+3*8)
 if not en or en%12:raise ValueError('incomplete exception directory')
 pd=[tuple(x+base for x in struct.unpack('<III',read(base+er+12*i,12))) for i in range(en//12)]
 selected=[x for x in pd if 0x2fdda0<=x[0]<0x2fe534]
 if not selected or selected[0]!=(0x2fdda0,0x2fddd3,0x1d5331c) or selected[-1][1]!=0x2fe534 or any(a[1]!=b[0] for a,b in zip(selected,selected[1:])):
  raise ValueError('normal code partition not contiguous')
 root=selected[0];unwinds=[]
 def parent(e):
  h=read(e[2],4);count=h[2];flags=h[0]>>3
  if flags&4:
   n=(4+2*count+3)&~3;raw=read(e[2],n+12);chain=tuple(x+base for x in struct.unpack_from('<III',raw,n));return chain,raw
  if flags:raise ValueError('unexpected handler flags in normal-code partition')
  return None,read(e[2],(4+2*count+3)&~3)
 for e in selected:
  seen=set();cur=e
  while True:
   if cur in seen or cur not in pd:raise ValueError('unwind chain missing/cyclic')
   seen.add(cur);par,blob=parent(cur)
   if par is None:
    if cur!=root:raise ValueError('different unwind root')
    break
   cur=par
  par,blob=parent(e);unwinds.append({'pdata':[hex(x) for x in e],'unwind_bytes':blob.hex(),'chain_to':[hex(x) for x in par] if par else None})
 # Padding NOPs at2FE531..534 are code-partition bytes; inline lookup data begins534.
 C=module('verified_switch_capture','capture-index-path.py')
 C.RANGES=[(0x2fdda0,0x2fe534),(0x305080,0x30510f),(0x30e360,0x30e395),(0x30e588,0x30e5b3)]
 sys.argv=[sys.argv[0],str(out)];C.main();v=json.loads(out.read_text())
 tables=[]
 for pc,n,label in [(0x2fe534,24,'six first-switch image-relative arm RVAs'),(0x2fe54c,76,'bounded first-switch selector bytes'),(0x2fe598,0xc0,'remaining inline tables/padding; no implicit whole-domain interpretation'),(0x1eec6a8,16,'outer handler slots for4049/404A')]:
  blob=read(pc,n);tables.append({'address':hex(pc),'bytes':blob.hex(),'sha256':hashlib.sha256(blob).hexdigest(),'label':label})
 S=module('reviewed_switch_annotations','validate-title-source-annotations.py')
 v.update(wrapper_complete=True,pdata_normal_partition=unwinds,normal_code_extent={'start':'0x2fdda0','end_exclusive':'0x2fe534','inline_data_start':'0x2fe534','limits':'Code partition and unwind roots verified; no automatic semantic full-CFG or EH execution guarantee'},tables=tables,annotation_prerequisite=S.validate(v),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='STATIC_ONLY source/lookup proof; no native effects, actual units/order/ownership or universal other caller bounds')
 out.write_text(json.dumps(v,indent=2)+'\n');print('Original compressed switch code/table identity and chained normal partition captured; no game')
if __name__=='__main__':main()
