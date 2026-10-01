"""Retain only the original archive index/name prefix and external inputs.

No archive payloads, peer scripts, native code or game executed. Strict count,
range, UTF-8/ASCII and unique-name gates fail closed before the final receipt.
"""
import ast,hashlib,json,pathlib,shutil,struct,zlib
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'ov33-e2-key-inputs-01'
if out.exists():raise ValueError('immutable input snapshot exists')
archive=pathlib.Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf')
sha=lambda b:hashlib.sha256(b).hexdigest()
expected={('US',129),('US',130),('US',131),('UK',131),('UK',132),('CN',127)}
peerfiles={
 'fable-e2-census.py':'Database/FFXII TZA/_index/candidates/ov33-no-status-exits-fable-0929/e2_path_census.py',
 'fable-e2-census.out':'Database/FFXII TZA/_index/candidates/ov33-no-status-exits-fable-0929/e2_path_census.out',
 'contract-b14-checks.py':'Database/FFXII TZA/_index/candidates/swe2contract-ddres-b14-0930/b14_checks.py',
 'contract-b14-checks.out':'Database/FFXII TZA/_index/candidates/swe2contract-ddres-b14-0930/b14_checks.out'}
blobs={name:(ROOT/p).read_bytes() for name,p in peerfiles.items()}
rows=[]
for line in blobs['fable-e2-census.out'].decode('utf-8').splitlines():
 if not line.strip().startswith('('):continue
 row=ast.literal_eval(line.strip())
 if len(row)==5 and row[2]==1 and (row[0],row[3]) in expected:rows.append(row)
if len(rows)!=12 or {(q[0],q[1],q[3]) for q in rows}!={(l,e,n) for l,n in expected for e in (0,1)}:raise ValueError('missing/duplicate selected retained E2 rows')
paths={}
for lang,mode,kind,num,path in rows:
 if not isinstance(path,str) or path=='NULL' or not path.isascii():raise ValueError('invalid/nonASCII selected source path')
 key=(lang,num)
 if key in paths and paths[key]!=path:raise ValueError('two retained modes disagree')
 paths[key]=path
with archive.open('rb') as f:
 before=archive.stat();head=f.read(16)
 if len(head)!=16:raise ValueError('truncated archive header')
 magic,headerlen,count=struct.unpack('<4sIQ',head)
 if magic!=b'SRYK' or count!=89414:raise ValueError('wrong/empty original archive-name population')
 entries_offset=16+count*16;strings_offset=16+count*48
 f.seek(strings_offset);lengthbytes=f.read(4)
 if len(lengthbytes)!=4:raise ValueError('missing string length')
 stringlen=struct.unpack('<I',lengthbytes)[0];end=strings_offset+stringlen
 if stringlen<4 or end>headerlen or end>before.st_size or end>64*1024*1024:raise ValueError('invalid original index-prefix bounds')
 f.seek(0);prefix=f.read(end);after=archive.stat()
 if len(prefix)!=end or (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('truncated or changed original archive input')
 strings=prefix[strings_offset+4:end];names=[]
 for k in range(count):
  noff=struct.unpack_from('<Q',prefix,entries_offset+k*32+24)[0]
  if noff>=len(strings):raise ValueError('name offset outside original string table')
  stop=strings.find(b'\0',noff)
  if stop<0:raise ValueError('unterminated original archive name')
  name=strings[noff:stop].decode('ascii')
  if not name:raise ValueError('empty archive name')
  names.append(name)
 if len(set(names))!=count:raise ValueError('duplicate archive name would be hidden by dictionary')
 if 'ps2data/cdi/in/system.cnf' not in {n.lower() for n in names}:raise ValueError('known archive membership control absent')
compressed=zlib.compress(prefix,9);out.mkdir();(out/'archive-name-index-prefix.bin.zlib').write_bytes(compressed)
for name,b in blobs.items():(out/name).write_bytes(b)
receipt=dict(status='RETAINED_NONEMPTY_INDEX_AND_SELECTED_PEER_INPUTS',archive=dict(path=str(archive),bytes=before.st_size,mtime_ns=before.st_mtime_ns,header_length=headerlen,file_count=count,index_prefix_end=end,index_prefix_sha256=sha(prefix),compressed_path='archive-name-index-prefix.bin.zlib',compressed_sha256=sha(compressed),compressed_bytes=len(compressed),limits='Exact retained index/name prefix, not a full VBF/payload hash or initialized cache'),
 peer_inputs=[dict(path=name,original_path=peerfiles[name],sha256=sha(b)) for name,b in blobs.items()],
 selected_rows=[dict(language=l,edx_mode=e,kind=k,index=n,path=p) for l,e,k,n,p in rows],
 controls=dict(nonempty_count=count,unique_names=count,ascii_names=count,known_present='ps2data/cdi/in/system.cnf'),
 collector_sha256=sha(pathlib.Path(__file__).read_bytes()),limits='External source/census inputs retained, not our executions or automatic independent acceptance. No archive payload or game state read.')
(out/'inputs.json').open('x',encoding='utf-8').write(json.dumps(receipt,indent=2)+'\n')
print('Retained',count,'unique ASCII archive names; prefix',len(prefix),'compressed',len(compressed),'; six selected paths under both modes, no payload/game run')
