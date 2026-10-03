"""Original gauge callback registration; original physical metadata only.

Read the retained lookup and caller lineage before preparing these bodies. The decoder and current-action caller are retained; do not recapture them.
"""
import hashlib,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
BASE=0x120000;PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 out=P/sys.argv[1]
 if out.exists():raise ValueError('fresh output required')
 lookups=['lookup-registry-binding-01.json','lookup-default-binding-01.json','lookup-view-initializer-01.json']
 for n in lookups:
  x=json.loads((P/n).read_text())
  if x.get('complete') is not True or x.get('exe_sha256')!=PIN or x.get('matches')!=[] or x.get('driver_sha256')!='3ee7b1d08a9857dba896f77a3ba3bd238e850d6a4fb5bfe556cfcb78b37008dd' or x.get('requested')!=({'lookup-registry-binding-01.json':['0x297c10','0x297c11'],'lookup-default-binding-01.json':['0x296360','0x296361'],'lookup-view-initializer-01.json':['0x3f89c0','0x3f89c1']}[n]):
   raise ValueError('preparation lookup missing or retained source available')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('reference image changed')
 pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;os=struct.unpack_from('<H',raw,pe+20)[0]
 if struct.unpack_from('<H',raw,opt)[0]!=0x20b:raise ValueError('not PE32+')
 secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,size,off in secs:
   if BASE+rva<=a and a+n<=BASE+rva+size:return raw[off+a-BASE-rva:off+a-BASE-rva+n]
  raise ValueError('unbacked original bytes')
 directory=raw[opt+136:opt+144];rva,n=struct.unpack('<II',directory)
 if not n or n%12:raise ValueError('malformed exception directory')
 data=read(BASE+rva,n);rows=[struct.unpack_from('<III',data,k) for k in range(0,n,12)];known=set(rows)
 def chain(row):
  seen=set();steps=[]
  while True:
   if row in seen or row not in known:raise ValueError('cyclic or unlisted chain')
   seen.add(row);h=read(BASE+row[2],4);v=h[0]&7;flags=h[0]>>3
   if v!=1:raise ValueError('unhandled unwind version')
   step=dict(record_bytes=struct.pack('<III',*row).hex(),header_address=hex(BASE+row[2]),header_bytes=h.hex())
   if flags&4:
    if flags&3:raise ValueError('mixed chain/handler flags')
    footer=BASE+row[2]+((4+h[2]*2+3)&~3);triple=read(footer,12)
    step.update(chain_footer=hex(footer),chain_bytes=triple.hex());row=struct.unpack('<III',triple);steps.append(step)
   else:steps.append(step);return row,steps
 bodies=[]
 for entry in [0x296360,0x297c10,0x3f89c0]:
  roots=[r for r in rows if r[0]==entry-BASE]
  if len(roots)!=1:raise ValueError('ambiguous root')
  root=roots[0];members=[]
  for row in rows:
   if entry-BASE<=row[0]<entry-BASE+4096:
    target,steps=chain(row)
    if target==root:members.append(dict(begin=hex(BASE+row[0]),end_exclusive=hex(BASE+row[1]),chain=steps))
  end=entry
  for m in members:
   if int(m['begin'],16)!=end or int(m['end_exclusive'],16)<=end:raise ValueError('noncontiguous metadata')
   end=int(m['end_exclusive'],16)
  if not entry<end<=entry+4096:raise ValueError('bounded extent unavailable')
  z=read(entry,end-entry);bodies.append(dict(entry=hex(entry),end_exclusive=hex(end),bytes=len(z),sha256=hashlib.sha256(z).hexdigest(),physical_bytes=z.hex(),records=members))
 with out.open('x') as f:json.dump(dict(complete=True,method='A STATIC_ONLY original physical metadata',exe_sha256=PIN,driver_sha256=sha(Path(__file__)),directory_bytes=directory.hex(),lookups=[dict(path=n,sha256=sha(P/n)) for n in lookups],bodies=bodies,limits='Physical extents only. Code/data distinction, helper effects and natural reachability not established by metadata.'),f,indent=2)
 print(json.dumps([dict(entry=b['entry'],bytes=b['bytes'],end=b['end_exclusive']) for b in bodies]))
if __name__=='__main__':main()
