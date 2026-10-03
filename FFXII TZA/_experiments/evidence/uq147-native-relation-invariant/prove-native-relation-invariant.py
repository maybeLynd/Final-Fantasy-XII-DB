"""Method A: shipping branch constraints and closed cache-effect boundaries.

Equality partitions exhaust the relevant uint32 comparisons. They are not
native executions or gameplay samples. Original bytes are independently
qualified before this reduction; explicit receiver/packet/node coherence is
a precondition, not observed live initialization.
"""
import copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def index(s):return {int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
def pin(ix,pc,m,args):need(pc in ix and (ix[pc]['mnemonic'],ix[pc]['args'])==(m,args),'required native dataflow changed '+hex(pc))
def mem(ix,pc,base,offset,size,role,target=None):
    ms=ix[pc]['memory']
    need(len(ms)==1 and (ms[0]['base'],ms[0]['displacement'],ms[0]['size'],ms[0]['role'],ms[0]['rip_target'])==(base,offset,size,role,target),'required cache memory identity/effect changed '+hex(pc))
def closure(a,b):
    rows=[(0x512f30,a),(0x512cd0,b)];calls=[];graphs=[];writes=[]
    for entry,ix in rows:
        succ={}
        for pc,i in ix.items():
            m=i['mnemonic'].split()[-1];nxt=pc+len(bytes.fromhex(i['bytes']))
            if m=='call':
                need(i['args']=='0x512cd0','opaque native callee');calls.append((pc,'call'));v=[nxt]
            elif m.startswith('j'):
                need(i['args'].startswith('0x'),'opaque native branch')
                target=int(i['args'],16)
                if m=='jmp' and target not in ix:
                    need(target==0x512cd0,'opaque native tail');calls.append((pc,'tail'));v=[]
                else:v=[target]+([] if m=='jmp' else [nxt])
            elif m=='ret':v=[]
            else:v=[nxt]
            need(all(x in ix for x in v),'incomplete normal native successor');succ[pc]=v
            writes += [dict(body=hex(entry),pc=i['pc'],memory=m) for m in i['memory'] if m['role'] in ('w','rw') and m['base']!='rsp']
        seen=set();pending=[entry]
        while pending:
            pc=pending.pop()
            if pc not in seen:seen.add(pc);pending.extend(succ[pc])
        need(seen==set(ix),'unreachable/extra native source nodes')
        graphs.append(dict(entry=hex(entry),instructions=len(ix),returns=[hex(pc) for pc,i in ix.items() if i['mnemonic']=='ret']))
    need(calls==[(0x513005,'call'),(0x513022,'tail')],'native call boundary changed')
    return graphs,writes
def partitions(n):
    def extend(v):
        if len(v)==n:yield tuple(v);return
        for value in range(max(v)+2):yield from extend(v+[value])
    yield from extend([0])
def branch(ix,pc,equal):
    i=ix[pc];need(i['mnemonic'] in ('je','jne'),'unsupported equality branch')
    return equal if i['mnemonic']=='je' else not equal
def hit(ix,values,flag):
    u,actor,target,node_u,node_a,node_target=values
    # This is the exact matched kind2 arm, not a synthetic full interpreter.
    first=not branch(ix,0x512ff5,flag==1) and not branch(ix,0x512ffd,node_target==target)
    second=not branch(ix,0x513010,u==target)
    removed=int(first)+int(second)
    return dict(remove_call=first,remove_tail=second,remove_count=removed,
                final_live=removed==0,new_target=target if not second else node_target)
def derive(event,leaf):
    a,b=index(event),index(leaf)
    need(len(a)==161 and len(b)==47,'complete native instruction domains changed')
    graphs,writes=closure(a,b)
    expected_event={0x512fc6:('rip',41505827,1,'w'),0x513027:('rbx',8,4,'w'),0x513035:('rip',43676742,1,'rw'),
        0x51303d:('r11',14,1,'rw'),0x513049:('rip',41505697,1,'w'),0x513060:('rip',43676697,1,'w'),
        0x51306a:('rax',0,4,'w'),0x51306f:('rax',4,4,'w'),0x513075:('rax',8,4,'w'),
        0x513081:('rax',14,1,'w'),0x513085:('rax',15,1,'rw'),0x51308d:('rax',13,1,'w'),
        0x51309b:('r11',12,1,'w'),0x5130b3:('r10',14,1,'w'),0x5130c1:('r11',13,1,'w'),
        0x5130dc:('r11',0,4,'w'),0x5130e2:('r11',4,4,'w'),0x5130e9:('r11',15,1,'rw'),
        0x5130ee:('r11',15,1,'rw'),0x5130f3:('r11',8,4,'w'),0x513110:('r11',15,1,'rw'),
        0x513123:('r11',0,4,'w'),0x513129:('r11',4,4,'w'),0x513130:('r11',15,1,'rw'),
        0x513135:('r11',15,1,'rw'),0x51313a:('r11',8,4,'w')}
    actual_event={int(i['pc'],16):(m['base'],m['displacement'],m['size'],m['role']) for i in a.values() for m in i['memory'] if m['role'] in ('w','rw') and m['base']!='rsp'}
    need(actual_event==expected_event,'event persistent-write envelope changed')
    expected_leaf={0x512cf5:('rax',0xd,1,'w'),0x512cfd:('rcx',0xc,1,'w'),0x512d02:('rcx',0xc,1,'w'),
                   0x512d1e:('rax',0xe,1,'w'),0x512d26:('rcx',0xd,1,'w'),0x512d2b:('rcx',0xd,1,'w'),
                   0x512d52:('r10',0xe,1,'w'),0x512d5d:('r10',0xd,1,'w'),0x512d62:('r8',0xf,1,'rw'),
                   0x512d67:('r9',0xe,1,'rw'),0x512d6b:('rip',0x29a7710,1,'rw')}
    actual={int(i['pc'],16):(m['base'],m['displacement'],m['size'],m['role']) for i in b.values() for m in i['memory'] if m['role'] in ('w','rw')}
    need(actual==expected_leaf,'remover footprint/value-preservation premise changed')
    for pc,m,args in [(0x512f36,'mov','r11, rcx'),(0x512f39,'mov','rdi, rdx'),(0x512f3c,'movzx','edx, byte ptr [rdx]'),
        (0x512f41,'sub','ecx, 1'),(0x512f44,'je','0x5130fd'),(0x512f4a,'cmp','ecx, 2'),(0x512f4d,'je','0x5130cb'),
        (0x512f70,'movzx','ebx, al'),(0x512f73,'shl','rbx, 4'),(0x512f77,'add','rbx, r10'),
        (0x512f7e,'and','al, 0xf'),(0x512f80,'cmp','al, dl'),(0x512f82,'jne','0x512f8c'),
        (0x512f84,'mov','eax, dword ptr [rdi + 8]'),(0x512f87,'cmp','dword ptr [rbx + 4], eax'),(0x512f8a,'je','0x512ff1'),
        (0x512f94,'cmp','byte ptr [rdi + 1], 0'),(0x512f98,'jne','0x512fe6'),(0x512f9a,'mov','eax, dword ptr [rdi + 0xc]'),
        (0x512f9d,'cmp','dword ptr [rdi + 4], eax'),
        (0x512ff1,'cmp','byte ptr [rdi + 1], 1'),(0x512ff7,'mov','eax, dword ptr [rdi + 0xc]'),
        (0x512ffa,'cmp','dword ptr [rbx + 8], eax'),(0x512fff,'mov','rdx, rbx'),(0x513002,'mov','rcx, r11'),
        (0x51300a,'mov','eax, dword ptr [rdi + 0xc]'),(0x51300d,'cmp','dword ptr [rdi + 4], eax'),
        (0x513012,'mov','rdx, rbx'),(0x513015,'mov','rcx, r11'),(0x513027,'mov','dword ptr [rbx + 8], eax'),
        (0x513067,'mov','ecx, dword ptr [rdi + 4]'),(0x51306a,'mov','dword ptr [rax], ecx'),
        (0x51306c,'mov','ecx, dword ptr [rdi + 8]'),(0x51306f,'mov','dword ptr [rax + 4], ecx'),
        (0x513072,'mov','ecx, dword ptr [rdi + 0xc]'),(0x513075,'mov','dword ptr [rax + 8], ecx'),
        (0x51307c,'xor','cl, byte ptr [rdi]'),(0x51307e,'and','cl, 0xf'),(0x513085,'xor','byte ptr [rax + 0xf], cl'),
        (0x512cdb,'mov','r8, rdx'),(0x512cde,'mov','r9, rcx'),(0x512d62,'and','byte ptr [r8 + 0xf], 0xf0'),
        (0x512d67,'dec','byte ptr [r9 + 0xe]'),(0x512d6b,'dec','byte ptr [rip + 0x29a7710]')]:pin(a if pc>=0x512f30 else b,pc,m,args)
    for pc,target in [(0x512fa0,'0x512fe6'),(0x512ff5,'0x51300a'),(0x512ffd,'0x51300a'),(0x513010,'0x513027')]:
        need(a[pc]['args']==target and a[pc]['mnemonic'] in ('je','jne'),'equality branch identity changed')
    mem(a,0x512f58,'rip',0x2795291,8,'addr','0x2ca81f0')
    mem(b,0x512cd4,'rip',0x2795515,8,'addr','0x2ca81f0')
    mem(b,0x512d6b,'rip',0x29a7710,1,'rw','0x2eba481')
    for pc,off in [(0x51306a,0),(0x51306f,4),(0x513075,8)]:mem(a,pc,'rax',off,4,'w')
    mem(a,0x513027,'rbx',8,4,'w')
    # The leaf never changes R11/RDI, packet values, or DWORD row+8 in normal
    # valid disjoint node/receiver/packet state. Its address bases are pinned
    # above; global pool indices must be valid0..31 or FF as appropriate.
    need(not any(i['args'].split(',')[0].strip() in ('r11','r11d','r11b','rdi','edi','dil') and
                 i['mnemonic'] not in ('cmp','test') for i in b.values()),'remover preserves required caller registers')
    values=list(partitions(6));need(len(values)==203,'equality-domain enumeration invalid')
    coherent=[];counter=[];broken=[];creation_violations=[]
    for v in values:
        u,actor,t,nu,na,nt=v
        for flag in (0,1):
            admitted_creation=not branch(a,0x512f98,flag==0) and not branch(a,0x512fa0,u==t)
            if admitted_creation and u==t:creation_violations.append(dict(values=v,flag=flag))
            if u==nu and actor==na and nt!=nu:
                x=hit(a,v,flag);coherent.append(dict(values=v,flag=flag,**x))
                if x['remove_count']>1 or (x['final_live'] and x['new_target']==nu):counter.append(coherent[-1])
            elif u==nu and actor==na and flag==1 and nt==nu:
                x=hit(a,v,flag)
                if x['remove_count']==2:broken.append(dict(values=v,flag=flag,**x))
    need(not creation_violations,'creation target-recipient invariant refuted')
    need(coherent and not counter,'coherent live-row double-remove/preservation counterexample '+str(counter[:1]))
    need(broken,'required violating-state double-remove detection control absent')
    return dict(graphs=graphs,nonstack_writes=writes,equality_domain=dict(variables=['packet_uid','packet_actor','packet_target','node_uid','node_actor','node_target'],partitions=203,flag_domain=[0,1],coherent_cases=len(coherent),counterexamples=counter,creation_counterexamples=creation_violations),
        coherent_transitions=coherent,positive_broken_premise_witness=broken[0],
        fact='Kind2 creation requires packetUid!=packetTarget; coherent live rows preserve target!=recipient. Under packet/node UID coherence the matching-target removal and UID==target tail removal cannot both execute. A broken live-row target==recipient premise can execute both; the leaf unconditionally decrements counts on each call.',
        effect='Closed two-body native cache handler/remover. Flags/free-row and owner-head/tail/count effects remain; released row IDs/links are not cleared. Updates after a remove can touch an inactive row. No unknown native callee, imported callback or heap free in these two bodies.',
        premises='Valid disjoint16B receiver/node/packet identities, fixed pool2CA81F0 with32 slots, index fields consistent0..31/FF, coherent list ownership, packetUid=nodeUid for matching owner, initial live target!=recipient, normal ABI/private stack/normal returns/no interference. Initial/global/row defaults and actual live binding/reuse are not established.',
        limits='Source/equality constraint proof, not game/harness execution or all malformed-state safety. Does not close other KO helpers or naturalKO/Esper113, scheduling/presentation, lifetime, fullUQ147 or wholeOV rows.')
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh output required')
    override=P/(sys.argv[2] if len(sys.argv)>2 else 'capture-native-event-boundary-01.status.json')
    st=json.loads(override.read_text());need(st.get('terminal') is True and st.get('exit')==0 and st.get('exception') is None,'successful upstream qualification required')
    specs=[('source-native-event-boundary-01.json','e954c611838d373bafde92d6b4118fb22695ee0b26a6fbf3d6476907f5a04215','capture-native-event-boundary.py','capture-native-event-boundary-01.status.json'),
           ('source-relation-remove-leaf-01.json','974aec9544ed4837a248d4c4f669435c6bbd24e232beb4906cef3037d64f911a','capture-relation-remove-leaf.py','capture-relation-remove-leaf-01.status.json')]
    validator=W/'validate-title-source-annotations.py';need(sha(validator)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    spec=importlib.util.spec_from_file_location('reviewed_roles',validator);V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    sources=[];checks=[]
    for name,pin_hash,driver,status in specs:
        source=P/name;need(sha(source)==pin_hash,'exact original source changed')
        q=json.loads((P/status).read_text());s=json.loads(source.read_text())
        need(q.get('terminal') is True and q.get('exit')==0 and q.get('exception') is None and q.get('driver_sha256')==sha(P/driver)==s.get('invocation_driver_sha256') and s.get('wrapper_complete') is True,'current complete qualified source required')
        checks.append(V.validate(s));sources.append(s)
    facts=derive(*sources);controls=[]
    for name,pc,kind,value,marker in [('reverse-match-target',0x512ffd,'mnemonic','je','coherent live-row double-remove'),('ignore-creation-inequality',0x512fa0,'mnemonic','jne','creation target-recipient invariant refuted'),('remover-writes-target',0x512d62,'memory',8,'remover footprint/value-preservation premise changed'),('native-write-outside-cache',0x513123,'memory',0x714,'event persistent-write envelope changed')]:
        z=copy.deepcopy(sources);i=next(i for s in z for r in s['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc)
        if kind=='memory':i['memory'][0]['displacement']=value;i['memory'][0]['size']=4
        else:i[kind]=value
        try:derive(*z)
        except ValueError as e:
            need(marker in str(e),'control failed at wrong detector '+str(e));controls.append(dict(id=name,refused=str(e),limits='Labelled source-record semantic control, not native byte mutation'))
        else:raise ValueError('known defect accepted '+name)
    result=dict(producer_complete=True,driver_sha256=sha(Path(__file__)),method='A verified original-byte CFG/effect boundaries + exhaustive equality-pattern constraints',sources=[dict(path=n,sha256=h) for n,h,*_ in specs],annotation_checks=checks,facts=facts,controls=controls,acceptance='Producer-valid only; independent review/canonical incorporation required. No native/game sample or whole runtime-row credit.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('Closed native cache effects; coherent-state double removal excluded, broken-premise witness retained. No native/game execution.')
if __name__=='__main__':main()
