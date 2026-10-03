"""Original local bit22 partition; consumes the already accepted copy domain."""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
E=ROOT/'Database/FFXII TZA/_experiments/evidence/suspend-restore-copy-origin'
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def ix(s):return {int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']}
def instruction(a,pc,m,args):need(pc in a and (a[pc]['mnemonic'],a[pc]['args'])==(m,args),'branch/call/dataflow changed '+hex(pc))
def graph(s):
    a=ix(s);nodes=set(a);entry=int(s['ranges'][0]['start'],16);edges={}
    for pc,i in a.items():
        nxt=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if m=='ret':v=[]
        elif m.startswith('j'):
            need(i['args'].startswith('0x'),'unresolved local transfer')
            v=[int(i['args'],16)]+([] if m=='jmp' else [nxt])
        else:v=[nxt] # opaque calls are required to return normally
        need(all(z in nodes for z in v),'missing normal successor '+hex(pc));edges[pc]=v
    seen=set();pending=[entry]
    while pending:
        x=pending.pop()
        if x not in seen:seen.add(x);pending.extend(edges[x])
    need(seen==nodes,'unreachable/extra local instructions')
    return dict(entry=hex(entry),instructions=len(nodes),normal_return_sites=[hex(pc) for pc,i in a.items() if i['mnemonic']=='ret'],limits='Finite normal local CFG; opaque returning calls, no exception/callback/native-effect model')
def derive(release,restore):
    a,b=ix(release),ix(restore)
    need(len(a)==53 and len(b)==25,'incomplete instruction domain')
    instruction(a,0x310796,'mov','rbx, rcx');instruction(a,0x3107b4,'mov','rdi, rax')
    for pc,m,args in [(0x310780,'test','rcx, rcx'),(0x310783,'je','0x310860'),(0x31078e,'cmp','qword ptr [rcx + 0x698], 0'),(0x310799,'je','0x31085b'),(0x3107af,'call','0x31b7e0'),(0x3107b7,'test','rax, rax'),(0x3107ba,'je','0x310803'),(0x3107be,'bt','rcx, 0x16'),(0x3107c3,'jb','0x310803'),(0x3107c5,'movzx','ecx, byte ptr [rbx + 0xea9]'),(0x3107d7,'shl','edx, cl'),(0x3107d9,'test','edx, eax'),(0x3107db,'je','0x310803'),(0x310806,'call','0x308270'),(0x31084d,'cmp','word ptr [rbx + 0x714], ax'),(0x310854,'jne','0x31085b'),(0x310856,'call','0x317e50')]:instruction(a,pc,m,args)
    writes=[(int(i['pc'],16),m['base'],m['displacement'],m['size'],m['role']) for i in a.values() for m in i['memory'] if m['role'] in ('w','rw') and m['base']!='rsp']
    expected=[(0x3107dd,'rdi',0xea8,1,'rw'),(0x3107ea,'rdi',0xea4,4,'w'),(0x31080b,'rbx',0,8,'rw'),(0x310825,'rbx',0x694,1,'w')]
    need(writes==expected,'local object-write census changed')
    calls=[(int(i['pc'],16),i['args']) for i in a.values() if i['mnemonic']=='call']
    need(calls==[(0x3107af,'0x31b7e0'),(0x3107f6,'0x313b30'),(0x3107fe,'0x2fead0'),(0x310806,'0x308270'),(0x310819,'0x30c970'),(0x31082c,'0x319420'),(0x310839,'0x319140'),(0x310856,'0x317e50')],'opaque boundary census changed')
    for pc,m,args in [(0x308276,'mov','eax, dword ptr [rcx]'),(0x308278,'mov','rbx, rcx'),(0x30827b,'bt','rax, 0x16'),(0x308280,'jae','0x3082e2'),(0x308290,'call','0x30c970'),(0x3082bd,'mov','rcx, rbx'),(0x3082c6,'call','0x30eda0')]:instruction(b,pc,m,args)
    return dict(graphs=[graph(release),graph(restore)],local_writes=[dict(pc=hex(pc),base=base,offset=hex(off),bytes=size,role=role) for pc,base,off,size,role in writes],calls=[dict(pc=hex(pc),target=t) for pc,t in calls],facts=[
      '310780: with nonNULL receiver/stats/target, BT bit22 -> JB skips target contributor decrement/mask clear when bit22 SET. CLEAR plus target mask bit present admits the block. The DWORD SHL uses CL modulo32; a byte slot index alone is not a proven 0..31 natural bound.',
      '310780 directly writes only target EA8/EA4, acting flags0 and acting byte694. It has no direct committed714/pendingBA0/battle-mode store, under private separated stack/ordinary object field identity. Callee effects are not excluded.',
      '308270 separately reads acting flags: BT bit22 -> JAE returns when CLEAR; SET reaches 30C970 and, after normal return, 30EDA0. Earlier calls/interference may change bit22; no atomic first/second observation invariant.',
      'Accepted d7500f9f/49d0564f2 copy-domain result is reused, not rerun: 30EDA0 copies [unit+6B0,unit+BA0), including committed714 at saved offset64, excluding pendingBA0. Thus supplied valid snapshot can replace current action; it need not clear it. Native helper31B7E0/313B30/2FEAD0/30C970/319420/319140 and natural reachable states remain qualified separately.'
    ],limits='Original local code/normal ABI/valid readable and writable state/private separated stack/returning opaque helpers/no interference during each branch. No complete transitive effect, preserved bit22 across calls, natural KO-Dismiss coexistence, live initialization, lifetime, scheduling, presentation or wholeUQ147 proof.')
def main():
    out=P/sys.argv[1];need(not out.exists(),'fresh result required')
    sp=P/'source-ko-release-01.json';rp=P/'source-restore-gate-01.json'
    need(sha(sp)=='119783a71346a83977bb0cd7081988d6ec8f6631e5b3cd169153d1966ffafbda' and sha(rp)=='b80601120e4d34f64e2567610a0f7c3b2f9f9d520575baee513fe9d5dbda83ff','source identity moved')
    statuses=[P/'capture-ko-release-01.status.json',P/'capture-restore-gate-01.status.json']
    if len(sys.argv)>2:statuses[0]=Path(sys.argv[2]) # labelled disposable upstream-failure control
    for p,pin in zip(statuses,['6375809a6b6465f574bd79d5bc1ed0aa360ebfee10c64aaec2d1dd39fd8b54d5','da9c7dbeb60c98c773494243275597297b421b22ddbe9437ce7df0d2514f0464']):
        s=json.loads(p.read_text());need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==pin,'required capture failed/incomplete')
    source,restore=json.loads(sp.read_text()),json.loads(rp.read_text())
    vf=W/'validate-title-source-annotations.py';need(sha(vf)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    spec=importlib.util.spec_from_file_location('reviewed_access_roles',vf);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    annotations=[v.validate(x) for x in [source,restore]]
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed')
    pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0]
    def original(a,n):
        for j in range(struct.unpack_from('<H',raw,pe+6)[0]):
            _,rva,size,off=struct.unpack_from('<IIII',raw,pe+32+os+40*j)
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
        raise ValueError('unbacked byte range')
    for x,start,end in [(source,0x310780,0x310861),(restore,0x308270,0x3082e8)]:
        need(x.get('wrapper_complete') is True and x['exe_sha256']==PIN and len(x['ranges'])==1 and len(x['physical_bodies'])==1,'incomplete original capture')
        b=x['physical_bodies'][0];r=x['ranges'][0];z=original(start,end-start)
        need(b['entry']==hex(start) and b['end_exclusive']==hex(end) and b['bytes']==len(z) and b['physical_bytes']==z.hex() and ''.join(i['bytes'] for i in r['instructions'])==z.hex(),'physical/code extent disagreement')
        for m in b['records']:
            for c in m['chain']:
                need(original(int(c['header_address'],16),4).hex()==c['header_bytes'],'unwind header changed')
                if 'chain_footer' in c:need(original(int(c['chain_footer'],16),12).hex()==c['chain_bytes'],'unwind chain changed')
    cp=E/'result-01.json';cs=E/'source-01.json'
    need(sha(cp)=='3d07f53b92b6543177a47d895734edc872e044f6355af1be9b641536f11fec7d' and sha(cs)=='31c27aa8b2da192db7c62c62420ef2f44d2cc5cabe79b1149d90dcd782ded67d','accepted copy dependency moved')
    copy_result=json.loads(cp.read_text());copy_source=json.loads(cs.read_text())
    need(copy_result.get('producer_complete') is True and copy_result.get('driver_sha256')=='7f9968296398a8b9a1ef6a76ae7584593fcdb97457d3d9cd2b171d92a3e08afd' and copy_result.get('source_pins')==[dict(path='source-01.json',sha256=sha(cs))] and copy_source.get('exe_sha256')==PIN,'accepted copy result/source binding incomplete')
    old_status=json.loads((E/'proof-01.status.json').read_text())
    need(old_status.get('terminal') is True and old_status.get('exit')==0 and old_status.get('exception') is None and old_status.get('driver_sha256')==copy_result['driver_sha256'],'accepted upstream proof failed/incomplete')
    annotations.append(v.validate(copy_source))
    facts=derive(source,restore);controls=[]
    for id,which,pc,field,value,diagnostic in [('release-bit22-reversed',0,0x3107c3,'mnemonic','jae','branch/call/dataflow changed'),('restore-bit22-reversed',1,0x308280,'mnemonic','jb','branch/call/dataflow changed'),('restore-target-replaced',1,0x3082c6,'args','0x3105d0','branch/call/dataflow changed'),('command-store-retarget',0,0x310825,'memory',0x714,'local object-write census changed')]:
        z=[copy.deepcopy(source),copy.deepcopy(restore)];i=ix(z[which])[pc]
        if field=='memory':i['memory'][0]['displacement']=value
        else:i[field]=value
        try:derive(*z)
        except ValueError as e:need(diagnostic in str(e),'wrong semantic detector');controls.append(dict(id=id,diagnostic=str(e),method='Labelled static source-record control, not original-byte alteration/native execution'))
        else:raise ValueError('detector missed '+id)
    result=dict(producer_complete=True,method='A complete local original CFG/bit22 partition plus accepted copy-domain dependency',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=sp.name,sha256=sha(sp)),dict(path=rp.name,sha256=sha(rp)),dict(path='retained-copy/source-01.json',sha256=sha(cs))],annotation_prerequisites=annotations,facts=facts,controls=controls,retained_copy=dict(commit='d7500f9f91183c3f48f749d345fb8a35bdb16644',independent_acceptance='49d0564f2',source_sha256=sha(cs),result_sha256=sha(cp),limits='Existing accepted bounded result consumed, no repeated 79-pair reduction/native regression or external run credit'),acceptance='Producer-valid only; new bit22 correction independent review/owning consumption pending, fullUQ147 OPEN')
    with out.open('x') as f:json.dump(result,f,indent=2)
    print('Original bit22 set skips relation bookkeeping; separate set-bit restore can replace committed714. No natural/transitive closure.')
if __name__=='__main__':main()
