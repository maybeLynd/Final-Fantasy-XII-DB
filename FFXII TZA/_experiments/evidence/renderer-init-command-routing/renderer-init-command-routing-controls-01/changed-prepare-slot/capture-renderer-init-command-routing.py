"""Selected normal prepare/submit boundaries, Method A; no game/native run."""
import hashlib, importlib.util, json, pathlib, struct, sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
def module(n,f):
 s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 out=pathlib.Path(sys.argv[1])
 if out.exists():raise ValueError('immutable output exists')
 d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong reference')
 p=struct.unpack_from('<I',d,60)[0];o=p+24;bs=struct.unpack_from('<Q',d,o+24)[0]
 if bs!=0x120000:raise ValueError('wrong base')
 ns=struct.unpack_from('<H',d,p+6)[0];os=struct.unpack_from('<H',d,p+20)[0]
 ss=[struct.unpack_from('<IIII',d,o+os+40*k+8) for k in range(ns)]
 def read(a,n):
  for vs,va,rs,ro in ss:
   if va+bs<=a and a+n<=va+bs+rs:return d[ro+a-bs-va:ro+a-bs-va+n]
  raise ValueError('unbacked original range')
 r,n=struct.unpack_from('<II',d,o+112+3*8)
 if not n or n%12:raise ValueError('incomplete pdata')
 pd=[tuple(v+bs for v in struct.unpack('<III',read(r+bs+12*k,12))) for k in range(n//12)]
 roots=[(0x1f16c0,0x1f1733,0x1d6b7c8),(0x1fb840,0x1fb86b,0x1d529d0),(0x1a1850,0x1a1920,0x1d57588)]
 if any(pd.count(e)!=1 for e in roots):raise ValueError('exact normal root changed')
 leaves=[(0x1fb830,0x1fb83f),(0x16d6a0,0x16d6a3)]
 if any(any(e[0]<b and e[1]>a for e in pd) for a,b in leaves):raise ValueError('leaf overlap with pdata')
 table=read(0x902f28,16)
 if struct.unpack('<QQ',table)!=(0x16d6a0,0x1f16a0):raise ValueError('physical prepare/execute slot changed')
 if read(0x16d6a0,3)!=bytes.fromhex('c20000'):raise ValueError('original prepare RET0 changed')
 C=module('capture','capture-index-path.py');C.RANGES=[e[:2] for e in roots]+leaves
 sys.argv=[sys.argv[0],str(out)];C.main();raw=json.loads(out.read_text())
 S=module('annotations','validate-title-source-annotations.py')
 raw.update(wrapper_complete=True,pdata_entries=roots,unwind_headers=[dict(pdata=e,bytes=read(e[2],4).hex()) for e in roots],
   leaves=[dict(start=hex(a),end_exclusive=hex(b),basis='Exact original terminating tail/RET; no pdata overlap') for a,b in leaves],
   physical_table=dict(address='0x902f28',bytes=table.hex(),sha256=hashlib.sha256(table).hexdigest(),slots=['0x16d6a0','0x1f16a0']),
   annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
   limits='Original local normal ABI/CFG only, not exception/unwind handler behavior, loaded vtable, valid arena, natural initialization, opaque dispatch effects or timing.')
 out.write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURED384B original selected prepare/submit roots and leaves, plus physical16B table')
if __name__=='__main__':main()
