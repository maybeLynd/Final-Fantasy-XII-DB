"""Pin the exact original exception-directory fragment behind the extent lesson."""
import hashlib,json,struct
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();pin='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(raw).hexdigest()!=pin:raise ValueError('wrong original image')
pe=struct.unpack_from('<I',raw,60)[0];optsize=struct.unpack_from('<H',raw,pe+20)[0];opt=pe+24
if struct.unpack_from('<H',raw,opt)[0]!=0x20b:raise ValueError('not original PE32+')
secs=[struct.unpack_from('<IIII',raw,pe+32+optsize+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
 for vs,rva,size,off in secs:
  if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
 raise ValueError('unbacked original range')
directory=raw[opt+112+3*8:opt+112+4*8];rva,n=struct.unpack('<II',directory)
if not n or n%12:raise ValueError('missing/malformed exception directory')
data=read(0x120000+rva,n)
rows=[(k,struct.unpack_from('<III',data,k),data[k:k+12]) for k in range(0,n,12) if struct.unpack_from('<I',data,k)[0]==0x3db420-0x120000]
if len(rows)!=1:raise ValueError('missing/ambiguous exact entry fragment')
k,(begin,end,uw),record=rows[0]
if (begin,end)!=(0x3db420-0x120000,0x3db43c-0x120000):raise ValueError('original fragment changed')
out=P/'unwind-fragment-result-01.json'
if out.exists():raise ValueError('immutable result exists')
out.write_bytes((json.dumps(dict(complete=True,method='A original PE metadata; not whole function extent or runtime unwind observation',exe_sha256=pin,driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),directory_bytes=directory.hex(),record_va=hex(0x120000+rva+k),record_bytes=record.hex(),begin_va=hex(0x120000+begin),end_va_exclusive=hex(0x120000+end),unwind_info_va=hex(0x120000+uw),fragment_bytes=28,fragment_sha256=hashlib.sha256(read(0x3db420,28)).hexdigest(),limits='One original runtime-function entry covers entry fragment only. Actual full local CFG proof is separate; no census, chained-unwind semantic or live behavior claim.'),indent=2)+'\n').encode())
print('VERIFIED exact first runtime-function entry is28B, insufficient for the closed304B local CFG')
