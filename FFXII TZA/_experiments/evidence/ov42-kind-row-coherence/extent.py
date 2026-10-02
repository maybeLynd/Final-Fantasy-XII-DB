"""Original PE chained metadata for this one special-sequence entry only."""
import hashlib,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();BASE=0x120000;ENTRY=0x306bd0
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('wrong original image')
pe=struct.unpack_from('<I',raw,60)[0];opt=pe+24;optsize=struct.unpack_from('<H',raw,pe+20)[0]
if struct.unpack_from('<H',raw,opt)[0]!=0x20b:raise ValueError('not PE32+')
secs=[struct.unpack_from('<IIII',raw,pe+32+optsize+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if BASE+rva<=a and a+n<=BASE+rva+size:return raw[off+a-BASE-rva:off+a-BASE-rva+n]
 raise ValueError('unbacked original range')
directory=raw[opt+136:opt+144];rva,n=struct.unpack('<II',directory)
if not n or n%12:raise ValueError('missing/malformed exception directory')
data=read(BASE+rva,n);rows=[struct.unpack_from('<III',data,k) for k in range(0,n,12)];known=set(rows)
roots=[r for r in rows if r[0]==ENTRY-BASE]
if len(roots)!=1:raise ValueError('missing/ambiguous entry record')
root=roots[0]
def chain(row):
 seen=set();steps=[]
 while True:
  if row in seen or row not in known:raise ValueError('cyclic/unlisted chain record')
  seen.add(row);h=read(BASE+row[2],4);version=h[0]&7;flags=h[0]>>3
  if version!=1:raise ValueError('unhandled unwind version')
  count=h[2];footer=BASE+row[2]+((4+count*2+3)&~3)
  step=dict(record=[hex(BASE+a) for a in row],header_bytes=h.hex(),flags=flags)
  if flags&4:
   if flags&3:raise ValueError('invalid mixed chained/handler flags')
   triple=read(footer,12);row=struct.unpack('<III',triple);step.update(chain_footer_va=hex(footer),chain_footer_bytes=triple.hex());steps.append(step)
  else:steps.append(step);return row,steps
selected=[]
for row in rows:
 if ENTRY-BASE<=row[0]<0x306d90-BASE:
  target,steps=chain(row)
  if target!=root:raise ValueError('interposed different function in selected physical interval')
  selected.append(dict(begin=hex(BASE+row[0]),end_exclusive=hex(BASE+row[1]),record_bytes=struct.pack('<III',*row).hex(),chain=steps))
if not selected:raise ValueError('zero extent members')
end=ENTRY
for q in selected:
 if int(q['begin'],16)!=end or int(q['end_exclusive'],16)<=end:raise ValueError('metadata extent not contiguous')
 end=int(q['end_exclusive'],16)
blob=read(ENTRY,end-ENTRY);out=P/'extent-01.json'
with out.open('x') as f:json.dump(dict(complete=True,method='A original chained PE metadata; not execution or semantic reachability',exe_sha256=PIN,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),directory_bytes=directory.hex(),entry=hex(ENTRY),end_exclusive=hex(end),bytes=len(blob),body_sha256=hashlib.sha256(blob).hexdigest(),records=selected,limits='Physical chained extent only; decoded CFG, indirect targets and source dataflow require separate verification.'),f,indent=2)
print(json.dumps(dict(chained_records=len(selected),bytes=len(blob),end_exclusive=hex(end))))
