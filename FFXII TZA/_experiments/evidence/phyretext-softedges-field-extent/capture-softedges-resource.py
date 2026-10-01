"""Bounded original text initializer + one shipping shader resource.

Reuse the reviewed actual capture adapter and existing selective extractor.
File schema is not live native storage; DXBC string matches are not descriptors.
Usage: python capture-softedges-resource.py FRESH_OUTPUT_DIRECTORY
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable output directory already exists')
sha=lambda z:hashlib.sha256(z).hexdigest()
extractor=ROOT/'agent_flow/tools/vbfextract.py'
if sha(extractor.read_bytes())!='1841f666b28fb737bf02ab3bb0ea90a7515273f74533a772e7f7131c0e0de611':
    raise ValueError('selective extractor identity changed')
spec=importlib.util.spec_from_file_location('existing_selective_extractor',extractor)
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
archive=pathlib.Path(r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf')
with archive.open('rb') as f:
    before=archive.stat();magic,hlen,nfiles=struct.unpack('<4sIQ',f.read(16))
    if magic!=b'SRYK' or nfiles!=89414 or not 16<hlen<=16*1024*1024:
        raise ValueError('archive index/control scope changed')
    f.seek(0);index=f.read(hlen)
    if len(index)!=hlen:raise ValueError('incomplete archive index')
    f.seek(0);names,blocks=V.load_index(f)
    selected=[n for n in names if n.lower().endswith('/phyretext.fx.phyre')]
    if len(selected)!=1 or names[selected[0]][1]>1024*1024:raise ValueError('unique bounded shader identity missing')
    name=selected[0];data=V.read_entry(f,names,blocks,name);entry=names[name]
    after=archive.stat()
if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
    raise ValueError('archive moved during capture')
if len(data)!=44634 or sha(data)!='f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf':
    raise ValueError('shipping shader differs from feasibility source')
hdr=struct.unpack_from('<21I',data);hs,ns=hdr[1:3]
if hdr[0]!=0x50485952 or hs!=84 or hdr[3]!=0x44583131 or hs+ns>len(data):
    raise ValueError('exact shader container header control')
b=data[hs:hs+ns];bom,size,nt,nc,nm,pooln,u6,u7=struct.unpack_from('<8I',b)
if bom!=0x01020304 or size!=ns or 32+4*nt+36*nc+24*nm+pooln!=ns:
    raise ValueError('accepted namespace layout/size equation failed')
start=32+4*nt;classes=[struct.unpack_from('<9I',b,start+36*i) for i in range(nc)]
start+=36*nc;members=[struct.unpack_from('<6I',b,start+24*i) for i in range(nm)]
start+=24*nm;pool=b[start:]
def text(off):
    if off>=len(pool) or (off and pool[off-1]!=0):raise ValueError('name is not a pool string start')
    end=pool.find(b'\0',off)
    if end<0:raise ValueError('unterminated pool name')
    return pool[off:end].decode('ascii')
if sum(c[3] for c in classes)!=nm:raise ValueError('class/member ownership equation')
decoded=[];cursor=0
for i,c in enumerate(classes):
    count=c[3];fields=members[cursor:cursor+count];cursor+=count
    decoded.append(dict(class_id=i+1,name=text(c[2]),raw=list(c),members=[
        dict(name=text(m[0]),type_ref=m[1],file_offset=m[2],file_width=m[3],attributes=m[4],array_bound=m[5],raw=list(m)) for m in fields]))
lists=[]
for i in range(hdr[4]):
    off=hs+ns+36*i
    if off+36>len(data):raise ValueError('truncated instance-list headers')
    row=struct.unpack_from('<9I',data,off);cid=row[0]
    if not 1<=cid<=len(decoded):raise ValueError('instance class identity/control failed')
    lists.append(dict(index=i,file_offset=off,class_id=cid,class_name=decoded[cid-1]['name'],raw=list(row)))
out.mkdir();(out/'phyretext.fx.phyre').write_bytes(data)
spec=importlib.util.spec_from_file_location('reviewed_original_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
# Two exact normal pdata fragments and two explicit six-byte import thunks.
# No full-pdata inline table decode, direct-memory role bypass or runtime effect.
C.RANGES=[(0x1ea3c0,0x1ea6bb),(0x18d240,0x18d311),(0x861eba,0x861ec6)]
raw=out/'original-code-raw-01.json';sys.argv=[sys.argv[0],str(raw)];C.main()
r=json.loads(raw.read_text());r.update(wrapper_complete=True,invocation_driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
    limits='Original source spans only; neither initialization nor natural callback/resource binding observed.')
raw.write_text(json.dumps(r,indent=2)+'\n')
result=dict(status='CAPTURED_SOURCE_AND_FILE_SCHEMA_ONLY',method='A',driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
    archive=str(archive),archive_bytes=before.st_size,archive_index_bytes=hlen,archive_index_sha256=sha(index),
    extractor_sha256=sha(extractor.read_bytes()),selected_entry=name,entry_tuple=list(entry),asset_bytes=len(data),asset_sha256=sha(data),
    header=list(hdr),namespace=dict(types=nt,classes=nc,members=nm,string_pool_bytes=pooln,sha256=sha(b)),
    selected_classes=[x for x in decoded if x['name'] in ['PMaterial','PShaderParameterDefinition','PParameterBuffer']],
    instance_headers=lists,softedges_string_offsets=[i for i in range(len(data)) if data.startswith(b'softEdges',i)],
    limits='File-side packed member widths and string offsets are not runtime descriptors or copy sizes. Instance object/fixup layout, exact softEdges record, material list membership and loader binding must be proved before accepting copy extent. No whole archive hash, live game, native execution or constructor-return closure.')
(out/'source-schema-01.json').write_text(json.dumps(result,indent=2)+'\n')
print('CAPTURED exact44,634-byte shader and bounded original-code/schema source; runtime extent unproved')
for x in result['selected_classes']:print(x['class_id'],x['name'],[(m['name'],m['file_offset'],m['file_width']) for m in x['members']])
for x in lists:print('instance',x['class_name'],x['raw'])
