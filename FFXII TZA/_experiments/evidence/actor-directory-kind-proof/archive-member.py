"""Read one exact archive member. Strict bounded block decode, no raw fallback.

Identifies this archive by size/header digest and retained selected compressed
bytes; does not claim a complete 31GB archive hash or unmodified installation.
"""
import hashlib,json,struct,sys,zlib
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
A=Path(r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf')
NAME='ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp'
PIN='e92d26899e523429695a97686732abdc46b518487f2870e4ba258fef16977a15'
sha=lambda b:hashlib.sha256(b).hexdigest()
def decode(blob,expected):
 if len(blob)==expected:return blob,'stored_raw'
 z=zlib.decompressobj();b=z.decompress(blob)+z.flush()
 if not z.eof or z.unused_data or z.unconsumed_tail or len(b)!=expected:raise ValueError('invalid/incomplete selected zlib block')
 return b,'zlib'
def main():
 if(P/'archive-member-01.json').exists():raise ValueError('immutable archive receipt exists')
 before=A.stat();blocks=[];selected=[]
 with A.open('rb') as f:
  h=f.read(16);magic,hlen,n=struct.unpack('<4sIQ',h)
  if magic!=b'SRYK' or not 16<hlen<16000000 or not 0<n<100000:raise ValueError('unexpected bounded SRYK archive')
  f.seek(0);header=f.read(hlen)
  if len(header)!=hlen:raise ValueError('incomplete archive header')
  eo=16+n*16;st=eo+32*n;slen=struct.unpack_from('<I',header,st)[0]
  bo=st+slen
  if not(st+4<=bo<=hlen) or (hlen-bo)%2:raise ValueError('invalid string/block table')
  # The format string offsets are relative to the bytes following the length.
  strings=header[st+4:bo];found=[]
  for k in range(n):
   record=header[eo+32*k:eo+32*(k+1)];sb,sb2,size,off,noff=struct.unpack('<IIQQQ',record)
   if noff>=len(strings):raise ValueError('invalid name offset')
   end=strings.find(b'\0',noff)
   if end<0:raise ValueError('unterminated archive name')
   name=strings[noff:end].decode('utf8')
   if name==NAME:found.append((k,record,sb,sb2,size,off,noff))
  if len(found)!=1:raise ValueError('exact member absent or duplicated')
  k,record,sb,sb2,size,pos,noff=found[0]
  if size!=80000:raise ValueError('unexpected member size')
  for j in range((size+65535)//65536):
   rawsize=struct.unpack_from('<H',header,bo+2*(sb+j))[0];length=rawsize or 65536
   expected=min(65536,size-j*65536)
   if pos+length>before.st_size:raise ValueError('member block outside archive')
   f.seek(pos);raw=f.read(length)
   if len(raw)!=length:raise ValueError('incomplete selected compressed block')
   b,mode=decode(raw,expected)
   dst=P/f'archive-block-{j:02d}.bin'
   if dst.exists():raise ValueError('immutable block exists')
   dst.write_bytes(raw);selected.append(b)
   blocks.append(dict(index=sb+j,offset=pos,compressed_bytes=length,table_u16=rawsize,expected_bytes=expected,mode=mode,path=dst.name,sha256=sha(raw),decoded_sha256=sha(b)))
   pos+=length
 after=A.stat();b=b''.join(selected);retained=(P/'asp_a03-US-original-01.ebp').read_bytes()
 if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('archive changed during bounded read')
 if b!=retained or sha(b)!=PIN:raise ValueError('archive member differs from retained control')
 controls=[]
 for label,blob,expected in [('truncated-zlib',b'x\x9c',4),('wrong-decompressed-length',zlib.compress(b'ab'),3)]:
  try:decode(blob,expected)
  except (ValueError,zlib.error):controls.append(label)
  else:raise ValueError('strict decode negative control accepted')
 out=dict(complete=True,method='A retained archive member',driver_sha256=sha(Path(__file__).read_bytes()),archive=dict(path=str(A),bytes=before.st_size,mtime_ns=before.st_mtime_ns,header_bytes=hlen,header_sha256=sha(header),members=n,full_archive_sha256=None),member=dict(path=NAME,index=k,index_record_offset=eo+32*k,index_record_hex=record.hex(),string_table_offset=st,name_offset=noff,raw_name_hex=NAME.encode().hex(),bytes=size,sha256=sha(b)),blocks=blocks,positive='strict selected block decode equals exact retained80KB bytes',negative_controls=controls,limits='Exact header/selected-member identity, no full archive digest, installation authenticity, live binding or all-corpus claim.',cleanup='Read-only source handle closed; only owned workspace receipts written.')
 (P/'archive-member-01.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
 print('VERIFIED one exact archive member against retained bytes; strict controls=2; no corpus extraction')
if __name__=='__main__':main()
