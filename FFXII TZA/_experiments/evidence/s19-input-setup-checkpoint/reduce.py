"""Finite read-only occupancy reduction. Position bytes need not stay still.

Only list links, self indices, active bytes and heads are bracketed. No claim
of atomicity, actual pair callbacks, universal maximum, or body lifetime.
"""
import copy, hashlib, json, struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
N,STRIDE=128,0x130
def fail(condition,message):
    if not condition: raise ValueError(message)
def decode(pool,control):
    fail(len(pool)==N*STRIDE and len(control)==16,'complete pool/control required')
    nodes=[struct.unpack_from('<HHHB',pool,i*STRIDE) for i in range(N)]
    active=[pool[i*STRIDE+7] for i in range(N)]
    used,free=struct.unpack_from('<H',control)[0],struct.unpack_from('<H',control,4)[0]
    if all(v==0 for v in pool) and control==bytes(16):
        return {'status':'OBSERVED_UNINITIALIZED','used_head':used,'free_head':free},None
    fail(all(row[2]==i for i,row in enumerate(nodes)),'own index mismatch')
    def walk(head):
        found=[];previous=0xffff
        while head!=0xffff:
            fail(0<=head<N and head not in found,'out-of-range/cycle')
            prev,nxt,_,_=nodes[head]
            fail(prev==previous,'previous link mismatch')
            found.append(head);previous,head=head,nxt
            fail(len(found)<=N,'bounded list')
        return found
    u,f=walk(used),walk(free)
    fail(not set(u)&set(f) and set(u)|set(f)==set(range(N)),'used/free partition')
    structural=(tuple(row[:3] for row in nodes),tuple(active),used,free)
    return {'status':'INITIALIZED','used_head':used,'free_head':free,
            'used_indices':u,'free_indices':f,'used_count':len(u),
            'highest_used_index':max(u,default=None),
            'active_used_indices':[i for i in u if active[i]!=0],
            'active_used_count':sum(active[i]!=0 for i in u),
            'active_bytes':[active[i] for i in u],
            'free_active_indices':[i for i in f if active[i]!=0]},structural
def reduce(raw):
    fail(raw['status']=='RAW_READS_PENDING_STATE_HEALTH_AND_REDUCTION','observer failed')
    fail(raw.get('read_handle_closed') and raw.get('null_rejected'),'detection/cleanup controls')
    fail(raw.get('positive') and not raw.get('debugger_present'),'positive/debugger controls')
    fail(len(raw.get('text_identity',[]))==2 and all(x['matches'] for x in raw['text_identity']),'text controls')
    fail(raw.get('modules_before') and raw['modules_before']==raw['modules_after'],'module controls')
    fail(raw['module_verdict']==raw['module_verdict_after']=='clean','vanilla modules')
    fail(len(raw['samples'])==2,'nonzero exact sample count')
    result=[]
    for sample in raw['samples']:
        reads={}
        for read in sample['reads']:
            fail(read['name'] not in reads,'duplicate read')
            b=bytes.fromhex(read['hex']);fail(len(b)==read['size'],'truncated read')
            fail(hashlib.sha256(b).hexdigest()==read['sha256'],'raw SHA mismatch');reads[read['name']]=b
        fail(set(reads)=={'tick_before','tick_after','pool_control_before','pool_control_after','pool_before','pool_after'},'read set')
        before,bs=decode(reads['pool_before'],reads['pool_control_before'])
        after,as_=decode(reads['pool_after'],reads['pool_control_after'])
        fail(before['status']==after['status'] and bs==as_,'structure/active bracket changed')
        fail(before==after,'decoded bracket changed')
        result.append({'index':sample['index'],'seconds':sample['end_unix']-sample['start_unix'],
                       'tick_before_hex':reads['tick_before'].hex(),'tick_after_hex':reads['tick_after'].hex(),
                       'pool_bytes_identical':reads['pool_before']==reads['pool_after'],
                       'structure_and_active_stable':True,**before})
    return {'status':'REDUCED_PENDING_VISUAL_STATE_AND_SESSION_HEALTH','samples':result,
            'limits':'Sequential brackets are not atomic. Active bytes are sampled. Occupancy is not callback execution or visible consequences.'}
def controls():
    pool=bytearray(N*STRIDE);control=bytearray(16)
    # Synthetic initialized empty then nonempty list; these test the reducer,
    # not FF12 initialization, allocator semantics or live default values.
    for i in range(N):struct.pack_into('<HHH',pool,i*STRIDE,i-1 if i else 0xffff,i+1 if i<N-1 else 0xffff,i)
    struct.pack_into('<H',control,0,0xffff)
    empty,_=decode(pool,control);fail(empty['used_count']==0,'empty control')
    struct.pack_into('<H',control,0,0);struct.pack_into('<H',control,4,10)
    struct.pack_into('<H',pool,9*STRIDE+2,0xffff);struct.pack_into('<H',pool,10*STRIDE,0xffff)
    pool[9*STRIDE+7]=1
    positive,_=decode(pool,control);fail(positive['used_count']==10 and positive['highest_used_index']==9 and positive['active_used_indices']==[9],'positive control')
    failures=[]
    for name,change in [('wrong-self',lambda p,c:struct.pack_into('<H',p,4,5)),('cycle',lambda p,c:struct.pack_into('<H',p,9*STRIDE+2,0)),('out-of-range',lambda p,c:struct.pack_into('<H',c,0,128)),('overlap',lambda p,c:struct.pack_into('<H',c,4,0))]:
        p,c=bytearray(pool),bytearray(control);change(p,c)
        try:decode(p,c)
        except ValueError:failures.append(name)
        else:raise ValueError('mutation survived: '+name)
    uninitialized,_=decode(bytes(N*STRIDE),bytes(16));fail(uninitialized['status']=='OBSERVED_UNINITIALIZED','uninitialized != empty')
    return {'synthetic_controls':'PASS','positive_used_count':10,'rejected_mutations':failures,'uninitialized_distinguished_from_empty':True}
if __name__=='__main__':
    r={'controls':controls(),'phases':{}}
    for phase in ('title','field'):
        source=HERE/(phase+'-access-qualified-raw.json')
        if source.exists():r['phases'][phase]={'raw_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),**reduce(json.loads(source.read_text()))}
    (HERE/'reduction.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
