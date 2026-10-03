"""Bounded Method A: inline reset is not linked-pool release."""
import copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def derive(s):
    ix={int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
    graphs=[]
    for entry,upper in [(0x512c80,0x512cd0),(0x512ee0,0x512f30)]:
        nodes={pc:i for pc,i in ix.items() if entry<=pc<upper};edges={}
        need(nodes and all(i['mnemonic']!='call' for i in nodes.values()),'complete no-callee leaf required')
        for pc,i in nodes.items():
            m=i['mnemonic'];nxt=pc+len(bytes.fromhex(i['bytes']))
            if m=='ret':v=[]
            elif m.startswith('j'):
                need(i['args'].startswith('0x'),'direct leaf successor required')
                v=[int(i['args'],16)]+([] if m=='jmp' else [nxt])
            else:v=[nxt]
            need(all(x in nodes for x in v),'incomplete successor');edges[pc]=v
        seen=set();pending=[entry]
        while pending:
            pc=pending.pop()
            if pc not in seen:seen.add(pc);pending.extend(edges[pc])
        need(seen==set(nodes),'incomplete entry-reachable domain')
        graphs.append(dict(entry=hex(entry),instructions=len(nodes),returns=[hex(pc) for pc,i in nodes.items() if i['mnemonic']=='ret']))
    def footprint(lo,hi):return {pc:[(m['base'],m['index'],m['displacement'],m['size'],m['role'],m['rip_target']) for m in i['memory'] if m['role'] in ('w','rw')] for pc,i in ix.items() if lo<=pc<hi and any(m['role'] in ('w','rw') for m in i['memory'])}
    linked={0x512cad:[('rax',None,15,1,'rw',None)],0x512cb9:[('rip',None,0x29a77c2,1,'w','0x2eba481')],0x512cbf:[('rcx',None,15,1,'rw',None)],0x512cc3:[('rcx',None,12,2,'w',None)],0x512cc9:[('rcx',None,14,1,'w',None)]}
    simple={0x512ee0:[('rcx',None,15,1,'rw',None)],0x512ee4:[('rcx',None,12,2,'w',None)],0x512eea:[('rcx',None,14,1,'w',None)]}
    need(footprint(0x512c80,0x512cd0)==linked,'linked-release pool/count footprint changed')
    need(footprint(0x512ee0,0x512f30)==simple,'inline reset unexpectedly touches pool or count')
    pins=[(0x512c80,'movzx','eax, byte ptr [rcx + 0xc]'),(0x512c84,'cmp','al, 0xff'),(0x512c86,'je','0x512cbf'),
          (0x512c88,'movzx','edx, byte ptr [rip + 0x29a77f2]'),(0x512c8f,'lea','r8, [rip + 0x279555a]'),
          (0x512ca0,'movzx','eax, al'),(0x512ca3,'add','dl, 0xff'),(0x512ca6,'shl','rax, 4'),(0x512caa,'add','rax, r8'),
          (0x512cad,'and','byte ptr [rax + 0xf], 0xf0'),(0x512cb1,'movzx','eax, byte ptr [rax + 0xe]'),(0x512cb5,'cmp','al, 0xff'),(0x512cb7,'jne','0x512ca0'),
          (0x512cb9,'mov','byte ptr [rip + 0x29a77c2], dl'),(0x512cbf,'and','byte ptr [rcx + 0xf], 0xf0'),(0x512cc3,'mov','word ptr [rcx + 0xc], 0xffff'),(0x512cc9,'mov','byte ptr [rcx + 0xe], 0'),
          (0x512ee0,'and','byte ptr [rcx + 0xf], 0xf0'),(0x512ee4,'mov','word ptr [rcx + 0xc], 0xffff'),(0x512eea,'mov','byte ptr [rcx + 0xe], 0')]
    for pc,m,args in pins:need((ix[pc]['mnemonic'],ix[pc]['args'])==(m,args),'release/reset dataflow changed '+hex(pc))
    for pc,target in [(0x512c88,'0x2eba481'),(0x512c8f,'0x2ca81f0')]:need(ix[pc]['memory'][0]['rip_target']==target,'pool/counter identity changed')
    return dict(graphs=graphs,linked_write_sites=[hex(x) for x in linked],reset_write_sites=[hex(x) for x in simple],
        result='00512EE0 resets inline flags low nibble/headFF/tailFF/count0 only. It does not release pool slots or update global count. 00512C80 walks the original head/next chain, clears each visited occupancy low nibble and writes cached global count minus visited length (mod256) once at the end, then performs the same inline reset. Empty headFF skips global-counter read/write.',
        preservation='Neither body clears DWORD IDs. Linked clear does not clear node links or self-slot indices, reset high flags preserved. No native callback/heapfree; no allocation cursor/high-count update by either body.',
        ownership='Inline reset cannot substitute for linked release when active owned nodes must be reclaimed. Calling reset on a nonempty owner discards its owner links without clearing those nodes. This is a local effect under a forced premise, not evidence of an actual faulty caller.',
        premises='Valid disjoint16B owner and fixed32x16B pool, consistent indices0..31/FF, finite acyclic owned list, bytecounter initial state, no concurrent interference/normal returns. Under those premises n<=32 and final globalcount=(old-n)&FF; ownercount reset does not validate actual list length.',
        limits='MethodA verified source/dataflow only. Cached global-counter update is not atomic with individual slot clears. No live initialization, caller order, ownership uniqueness across owners, reuse, naturalKO/Esper113, malformed-list termination or wholeUQ147 claim.')
def main():
    output=P/sys.argv[1];need(not output.exists(),'fresh output required')
    st=json.loads((P/(sys.argv[2] if len(sys.argv)>2 else 'capture-relation-reset-leaves-01.status.json')).read_text())
    need(st.get('terminal') is True and st.get('exit')==0 and st.get('exception') is None,'successful upstream qualification required')
    source=P/'source-relation-reset-leaves-01.json';need(sha(source)=='ccf583cf77a01c2d9e043994e2d0d623c13c33515f7255c032ef4b3cec266f10','qualified source changed')
    s=json.loads(source.read_text());q=json.loads((P/'capture-relation-reset-leaves-01.status.json').read_text())
    need(q.get('terminal') is True and q.get('exit')==0 and q.get('exception') is None and q['driver_sha256']==sha(P/'capture-relation-reset-leaves.py')==s['invocation_driver_sha256'] and s['wrapper_complete'] is True,'actual complete source required')
    validator=W/'validate-title-source-annotations.py';need(sha(validator)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    spec=importlib.util.spec_from_file_location('reviewed_roles',validator);V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    roles=V.validate(s);facts=derive(s);controls=[]
    for name,pc,change,marker in [('drop-pool-release',0x512cad,'drop','linked-release pool/count footprint changed'),('reset-pool-write',0x512ee0,'alias','inline reset unexpectedly touches pool or count'),('wrong-global-counter',0x512cb9,'counter','linked-release pool/count footprint changed')]:
        z=copy.deepcopy(s);i=next(i for r in z['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc)
        if change=='drop':i['memory'][0]['role']='r'
        elif change=='alias':i['memory'][0]['base']='r8'
        else:i['memory'][0]['rip_target']='0x2eba480'
        try:derive(z)
        except ValueError as e:need(marker in str(e),'wrong control detector');controls.append(dict(id=name,refused=str(e),limits='Synthetic source-record defect, not native mutation'))
        else:raise ValueError('known ownership defect accepted '+name)
    output.write_text(json.dumps(dict(producer_complete=True,driver_sha256=sha(Path(__file__)),method='A original-byte CFG/write/dataflow proof',source_sha256=sha(source),annotation_check=roles,facts=facts,controls=controls,acceptance='Producer-valid; independent review/canonical consumption pending. No native/game execution.'),indent=2)+'\n')
    print('Inline reset != linked-pool release; conditional ownership effect proved without live execution.')
if __name__=='__main__':main()
