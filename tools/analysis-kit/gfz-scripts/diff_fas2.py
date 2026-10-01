import sys,struct,json,hashlib
from pathlib import Path

def read_i32(f): return struct.unpack('>i',f.read(4))[0]
def read_i64(f): return struct.unpack('>q',f.read(8))[0]
def read_bool(f): return struct.unpack('>?',f.read(1))[0]
def read_s(f):
    n=read_i32(f)
    if n<0:return None
    return f.read(n).decode('utf-8')
def parse_rec(data):
    from io import BytesIO
    f=BytesIO(data); d={}
    d['entry']=read_i64(f); d['name']=read_s(f); d['namespace']=read_s(f); d['name_source']=read_s(f)
    d['comment']=read_s(f); d['repeatable_comment']=read_s(f); d['prototype']=read_s(f); d['signature_source']=read_s(f); d['calling_convention']=read_s(f)
    d['inline']=read_bool(f); d['noreturn']=read_bool(f); d['varargs']=read_bool(f); d['is_thunk']=read_bool(f); d['thunk_target']=read_i64(f)
    nr=read_i32(f); d['body_ranges']=[(read_i64(f),read_i64(f)) for _ in range(nr)]
    nt=read_i32(f); d['tags']=[(read_s(f),read_s(f)) for _ in range(nt)]
    if f.read(): raise ValueError('record trailing')
    return d

def parse(path):
    out={}
    with open(path,'rb') as f:
        if f.read(8)!=b'GFZANN2\0': raise ValueError('magic')
        ver=read_i32(f); n=read_i32(f)
        for _ in range(n):
            ln=read_i32(f); r=parse_rec(f.read(ln)); out[r['entry']]=r
        if f.read(): raise ValueError('file trailing')
    return ver,out

def diff(a,b,outfile=None):
    va,A=parse(a); vb,B=parse(b)
    fields=[k for k in next(iter(A.values())).keys() if k!='entry']
    add=sorted(set(B)-set(A)); rem=sorted(set(A)-set(B)); common=sorted(set(A)&set(B))
    changed=[]; field_counts={}
    tagadds={}; tagrem={}
    immutable=['name','namespace','name_source','repeatable_comment','prototype','signature_source','calling_convention','inline','noreturn','varargs','is_thunk','thunk_target','body_ranges']
    immutable_changed=[]
    for e in common:
        fs=[k for k in fields if A[e][k]!=B[e][k]]
        if not fs: continue
        changed.append({'entry':f'{e:08X}','fields':fs})
        for k in fs:field_counts[k]=field_counts.get(k,0)+1
        if any(k in immutable for k in fs): immutable_changed.append({'entry':f'{e:08X}','fields':[k for k in fs if k in immutable]})
        if 'tags' in fs:
            ta=set(x[0] for x in A[e]['tags']); tb=set(x[0] for x in B[e]['tags'])
            for t in sorted(tb-ta): tagadds[t]=tagadds.get(t,0)+1
            for t in sorted(ta-tb): tagrem[t]=tagrem.get(t,0)+1
    canon='\n'.join(x['entry']+':' + ','.join(x['fields']) for x in changed).encode()
    result={'from':str(a),'to':str(b),'from_functions':len(A),'to_functions':len(B),'added_functions':[f'{x:08X}' for x in add],'removed_functions':[f'{x:08X}' for x in rem], 'changed_common_functions':len(changed),'field_counts':field_counts,'tag_additions':tagadds,'tag_removals':tagrem,'immutable_changed_count':len(immutable_changed),'immutable_changed':immutable_changed[:100], 'changed_entries_fields_sha256':hashlib.sha256(canon).hexdigest()}
    if outfile: Path(outfile).write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    r=diff(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None)
    print(json.dumps(r,indent=2))
