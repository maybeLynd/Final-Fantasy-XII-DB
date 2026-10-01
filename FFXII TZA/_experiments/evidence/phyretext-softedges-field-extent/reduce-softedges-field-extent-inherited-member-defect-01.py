"""A bounded, retained-asset discriminator. No archive census or game execution.

QUESTION: what extent belongs to the named softEdges definition in the exact
PhyreText asset, and can a copy of that extent from outer+120 read AE0?
Reuse accepted EA-3 file parsing and CU-3 fixup decoding. Execute only their
explicit function declarations, never their census/main code. Native loaded-list
membership, alias destinations and whole-constructor effects remain open.
"""
import ast, hashlib, json, pathlib, struct, sys

W=pathlib.Path(__file__).resolve().parent
ROOT=W.parents[4]
ASSET_SHA='f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf'
EA3=ROOT/'Database/FFXII TZA/_index/candidates/ea3-shader-size-bits/ea3_census.py'
CU3=ROOT/'Database/FFXII TZA/_index/candidates/cu3-fixup-tables/cu3_fixup_tables.py'
PINS={EA3:'b4380cad43ad1ddfe69e753b64f2f7fdc5408c5c89d6e13ca00c72797530ddda',
      CU3:'360c17d33ee83125cd637da08f649c3be434c021aac71d335d2a8da478ca5435'}

def sha(b): return hashlib.sha256(b).hexdigest()

def declarations(path,names,env):
    text=path.read_bytes()
    if sha(text)!=PINS[path]:raise ValueError('dependency identity changed: '+str(path))
    tree=ast.parse(text,filename=str(path))
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise ValueError('missing/ambiguous dependency declarations')
    exec(compile(ast.Module(nodes,type_ignores=[]),str(path),'exec'),env)
    return dict(path=str(path.relative_to(ROOT)),sha256=sha(text),declarations=sorted(names),
                invocation='Only AST-selected declarations; no census/main/top-level execution')

def analyze(data):
    """Disclosed pure reduction. Controls may pass disposable mutated bytes."""
    if not 84<=len(data)<=1024*1024:raise ValueError('asset size budget')
    env={'struct':struct,'LIMIT':[1<<16]}
    dependencies=[declarations(EA3,{'parse'},env),declarations(CU3,
        {'Cur','Bad','guard','ror1','idx','excl','bitmask','dec_arr','ptail','dec_ptr'},env)]
    classes,lists,nt,data_start=env['parse'](data)
    h=struct.unpack_from('<21I',data)
    if h[1]!=84 or h[3]!=0x44583131 or len(lists)!=18:raise ValueError('selected cluster identity/layout')
    if sum(x[2] for x in lists)!=h[14]:raise ValueError('payload size closure')
    positions=[];p=data_start
    for l in lists:
        if not 1<=l[0]<=len(classes) or l[1]>4096 or l[3]+l[4]!=l[2]:
            raise ValueError('instance extent/count/class control')
        positions.append(p);p+=l[2]
    if p>len(data):raise ValueError('payload truncated')
    ids=[i for i,c in enumerate(classes) if c['name']=='PShaderParameterDefinition']
    if len(ids)!=1:raise ValueError('definition class identity')
    cid=ids[0];cl=classes[cid];fields=cl['members'];width=cl['w1']&0xfffffff
    if width!=13 or fields['m_name']['off']!=4 or fields['m_name']['width']!=1:
        raise ValueError('packed name/record layout')
    loc=fields['m_bufferLoc'];subid=loc['type']-nt-1
    if not 0<=subid<len(classes):raise ValueError('capture-location type reference')
    sub=classes[subid]
    if sub['name']!='PShaderParameterCaptureBufferLocationSize':raise ValueError('wrong nested field type')
    if (loc['off'],loc['width'],sub['members']['m_offset']['off'],sub['members']['m_offset']['width'],
        sub['members']['m_size']['off'],sub['members']['m_size']['width'])!=(5,4,0,2,2,2):
        raise ValueError('capture-location packed layout')
    target=[i for i,l in enumerate(lists) if l[0]==cid+1]
    if len(target)!=1:raise ValueError('definition list identity')
    ti=target[0];l=lists[ti];start=positions[ti]
    if l[1]!=12 or l[3]!=(l[1]*width+1)&~1:raise ValueError('definition objects extent')
    arrays=start+l[3];array_end=arrays+l[4]
    fixups_start=p+h[13]+12*h[12]+4*h[15]+16*h[16]
    if fixups_start>len(data):raise ValueError('fixup tables outside asset')
    tables={};p=fixups_start
    for name,size,col,fn in [('pointer-array',h[9],8,'dec_arr'),('pointer',h[7],7,'dec_ptr'),('array',h[5],6,'dec_arr')]:
        if p+size>len(data):raise ValueError('truncated packed table')
        # A separate bounded buffer makes a decoder over-read a failure even if
        # the next table would have supplied apparently usable bytes.
        c=env['Cur'](data[p:p+size],0);out=[]
        for i,v in enumerate(lists):
            if v[col]>4096:raise ValueError('fixup entry budget')
            entries=env[fn](c,v[col],v[1])
            if len(entries)!=v[col]:raise ValueError('fixup decoded count')
            out.append(entries)
        if c.p!=size:raise ValueError('fixup packed extent')
        tables[name]=dict(file_start=p,packed_bytes=size,entries_by_list=out);p+=size
    if p!=len(data):raise ValueError('unexpected shader tail')
    entries=tables['array']['entries_by_list'][ti]
    if len(entries)!=l[1]:raise ValueError('name fixup census')
    seen=set();records=[]
    for e in entries:
        key,index,extra,array_off=e
        if key!=(0x80000000|fields['m_name']['off']) or extra!=0 or index in seen or not 0<=index<l[1]:
            raise ValueError('name member/index fixup identity')
        seen.add(index)
        if not 0<=array_off<l[4]:raise ValueError('name array offset')
        a=arrays+array_off;z=data.find(b'\0',a,array_end)
        if z<0:raise ValueError('unterminated bounded descriptor name')
        name=data[a:z].decode('ascii')
        if not name or len(name)>64:raise ValueError('name control')
        r=start+index*width;off,size=struct.unpack_from('<HH',data,r+loc['off'])
        records.append(dict(index=index,name=name,name_file_start=a,name_array_offset=array_off,
            array_fixup=list(e),record_file_start=r,record_bytes=data[r:r+width].hex(),
            capture_offset=off,size_word=size,masked_size=size&0x1fff))
    records.sort(key=lambda x:x['index'])
    selected=[r for r in records if r['name']=='softEdges']
    if len(selected)!=1:raise ValueError('missing/ambiguous softEdges definition')
    # Distinct positive names/sizes detect a constant-size or DXBC-string reader.
    control={r['name']:r['masked_size'] for r in records}
    if control.get('textColor')!=16 or control.get('alphaThreshold')!=4:
        raise ValueError('distinct named extent controls')
    r=selected[0];n=r['masked_size'];source=0x120;state=0xae0
    return dict(status='FILE_FIELD_EXTENT_REDUCED',method='A STATIC_ONLY',asset_sha256=sha(data),
      dependencies=dependencies,namespace=dict(class_id=cid+1,packed_width=width,nested_type_class_id=subid+1),
      list=dict(index=ti,data_start=start,objects_bytes=l[3],arrays_start=arrays,arrays_bytes=l[4],count=l[1]),
      fixup_tables=tables,records=records,selected=r,
      conditional_copy=dict(source_outer_offset=source,length=n,end_exclusive=source+n,
        reads_any_AE0=source+n>state,reads_whole_AE0=source+n>=state+4,
        reads_any_label=source+n>0xae4,first_AE0_byte_threshold=state-source+1,
        whole_AE0_threshold=state+4-source),
      limits='File-side named definition and conditional source extent only. This is not a captured live descriptor, loaded-list membership, native lookup execution, buffer alias exclusion, constructor return, lifetime or natural reachability proof.')

def validate_source(directory):
    out={}
    for name in ['original-code-raw-01.json','array-binding-code-01.json','member-bridge-code-01.json']:
        p=directory/name;r=json.loads(p.read_bytes())
        if r.get('exe_sha256')!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' or not r.get('wrapper_complete'):
            raise ValueError('missing/incomplete original source prerequisite')
        if [c.get('observed') for c in r.get('controls',[])]!=['w','addr','rw']:
            raise ValueError('actual capture access-role controls incomplete')
        for g in r['ranges']:
            raw=b''.join(bytes.fromhex(x['bytes']) for x in g['instructions'])
            if len(raw)!=int(g['end_exclusive'],16)-int(g['start'],16) or sha(raw)!=g['sha256']:
                raise ValueError('original source span integrity')
            for x in g['instructions']:out[int(x['pc'],16)]=(x['mnemonic'],x['args'])
    expected={0x1ea5b7:('call','0x18d240'),0x1ea5c1:('lea','r10, [rsi + 0x118]'),
      0x1ea5cd:('movzx','r9d, word ptr [rax + 0x10]'),0x1ea5d2:('movzx','edx, word ptr [rax + 0x12]'),
      0x1ea5d6:('mov','eax, 0x1fff'),0x1ea5db:('and','dx, ax'),0x1ea5e4:('cmp','ecx, dword ptr [rbx]'),
      0x1ea5e8:('cmp','r9w, 4'),0x1ea5fb:('movzx','r8d, dx'),0x1ea606:('mov','rdx, r10'),
      0x1ea609:('call','0x861eba'),0x18d278:('mov','r8, qword ptr [r9 + 8]'),
      0x18d2a7:('add','r9, 0x18'),0x59c4d9:('btr','ebx, 0x1f'),
      0x59c5a4:('mov','edi, dword ptr [r14 + 0xc]'),0x59c5a8:('add','rdi, qword ptr [rsp + 0x130]'),
      0x59bf58:('mov','r8d, dword ptr [rdx + 8]'),0x59bf6d:('imul','eax, dword ptr [rdx + 0xc]')}
    for pc,value in expected.items():
        if out.get(pc)!=value:raise ValueError('original consumer/binding instruction prerequisite '+hex(pc))
    return [dict(path=p.name,sha256=sha(p.read_bytes())) for p in [directory/n for n in
        ['original-code-raw-01.json','array-binding-code-01.json','member-bridge-code-01.json']]]

def main():
    if len(sys.argv)!=3:raise ValueError('Usage: reducer SOURCE_DIRECTORY NEW_RESULT_JSON')
    directory=pathlib.Path(sys.argv[1]);output=pathlib.Path(sys.argv[2])
    if output.exists():raise ValueError('immutable result already exists')
    sources=validate_source(directory);data=(directory/'phyretext.fx.phyre').read_bytes()
    if sha(data)!=ASSET_SHA:raise ValueError('wrong original shader asset')
    r=analyze(data)
    r.update(driver_sha256=sha(pathlib.Path(__file__).read_bytes()),original_source_receipts=sources,
             producer_complete=True,independent_acceptance='PENDING')
    output.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print('REDUCED softEdges named record8: offset160, masked extent8; conditional outer+120..127 excludes AE0. Loaded binding/full effects remain OPEN.')

if __name__=='__main__':main()
