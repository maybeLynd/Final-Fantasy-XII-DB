"""Closed read-only roster selector; not natural KO or lifetime evidence."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)

def status(st,pin):
    need(st.get('terminal') is True and st.get('exit')==0 and st.get('exception') is None and st.get('driver_sha256')==pin,'actual upstream capture incomplete/failed')

def derive(s,caller):
    ranges=s['ranges'];ix={int(i['pc'],16):i for r in ranges for i in r['instructions']}
    expected=[
      (0x31b8c0,'sub','rsp, 0x28'),(0x31b8c4,'call','0x263750'),(0x31b8c9,'test','rax, rax'),(0x31b8cc,'jne','0x31b8d3'),(0x31b8ce,'add','rsp, 0x28'),(0x31b8d2,'ret',''),(0x31b8d3,'mov','rcx, rax'),(0x31b8d6,'add','rsp, 0x28'),(0x31b8da,'jmp','0x263e30'),
      (0x263750,'cmp','ecx, 3'),(0x263753,'ja','0x263764'),(0x263755,'movsxd','rax, ecx'),(0x263758,'lea','rcx, [rip + 0x1e36a91]'),(0x26375f,'mov','rax, qword ptr [rcx + rax*8]'),(0x263763,'ret',''),(0x263764,'xor','eax, eax'),(0x263766,'ret',''),(0x263e30,'mov','rax, qword ptr [rcx + 0x30]'),(0x263e34,'ret','')]
    need(len(ix)==len(expected) and set(ix)=={x[0] for x in expected},'incomplete/extra selector instruction span')
    for pc,m,a in expected:
        need((ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'selector instruction/transfer changed '+hex(pc))
    c={int(i['pc'],16):i for r in caller['ranges'] for i in r['instructions']}
    for pc,m,a in [(0x3138dd,'cmp','eax, 1'),(0x3138e0,'jne','0x31398d'),(0x3138e6,'lea','ecx, [rax + 2]'),(0x3138e9,'call','0x31b8c0')]:
        need(pc in c and (c[pc]['mnemonic'],c[pc]['args'])==(m,a),'Dismiss slot3 caller changed')
    mem=ix[0x263758]['memory'];need(len(mem)==1 and (mem[0]['rip_target'],mem[0]['role'])==('0x209a1f0','addr'),'roster base identity changed')
    mem=ix[0x26375f]['memory'];need(len(mem)==1 and (mem[0]['base'],mem[0]['index'],mem[0]['scale'],mem[0]['displacement'],mem[0]['size'],mem[0]['role'])==('rcx','rax',8,0,8,'r'),'roster pointer read changed')
    mem=ix[0x263e30]['memory'];need(len(mem)==1 and (mem[0]['base'],mem[0]['displacement'],mem[0]['size'],mem[0]['role'])==('rcx',0x30,8,'r'),'actor unit-pointer identity changed')
    need(not any(m['role'] in ('w','rw') for i in ix.values() for m in i['memory']),'selector object write introduced')
    transfers=[dict(pc=i['pc'],mnemonic=i['mnemonic'],args=i['args']) for i in ix.values() if i['mnemonic'].startswith(('call','j'))]
    need(len(transfers)==4,'selector transfer census incomplete')
    return dict(
      selection='3138D0 mode-query result1 -> ECX=1+2 ->31B8C0(3). This is roster slot index3, not ActorStorage class3.',
      function='Unsigned32 index>3 returnsNULL without table read. Accepted0..3 readsQWORD0209A1F0+8*index.31B8C0 returnsNULL if that actor pointer isNULL; otherwise returnsQWORDactor+30 through closed tail263E30.',
      dismiss='Under the actual slot3 caller: readsQWORD0209A208; if nonNULL, readsQWORDactor+30. No local health/status read, object write, allocation or opaque callback in this complete composed selector.',
      stack='Selector subtracts40bytes/restores40 before both ownRET and tail; leaf spans leaveRSP unchanged except ordinaryRET. Implicit CALL/RET private stack accesses remain validity/ABI premises.',
      transfers=transfers,
      interpretation='A status/KO filter or cleanup is not implemented by this selector. It cannot itself clear the mode/member or make a KO unit disappear; prior/later roster writers and command processing remain separate.',
      limits='Intactcode/readabletable/nonNULLactor+30/private valid return-stack/normal ABI/noninterference. No naturally populated roster, unitKO/aliveness/status persistence, pointer lifetime, mode preservation through the later command helper, scheduling or fullUQ147 reachability.')

def main():
    out=P/sys.argv[1];need(not out.exists(),'fresh output required')
    cap=P/'capture-dismiss-selector-boundary.py';cap_pin='4dde5e091a8c95718fc21f2003718552bc7c241faf7e2dcabd61205b7ae70737'
    st=json.loads((P/'capture-selector-01.status.json').read_text());status(st,cap_pin);need(sha(cap)==cap_pin,'capture source changed')
    sp=P/'source-selector-01.json';need(sha(sp)=='d788aa2956d6c8c47e9d630e0e9321861d61541b3c6648fdd81c16ecbbf8d9ba','certified selector source changed')
    s=json.loads(sp.read_text());need(s.get('wrapper_complete') is True and s.get('invocation_driver_sha256')==cap_pin and len(s['ranges'])==3,'complete exact wrapper required')
    bodies=s['physical_bodies'];need(len(bodies)==3 and len(bodies[0]['records'])==1 and not bodies[1]['records'] and not bodies[2]['records'],'.pdata-bounded selector vs declared leaf identities changed')
    for b,lo,hi in zip(bodies,[0x31b8c0,0x263750,0x263e30],[0x31b8df,0x263767,0x263e35]):
        need((int(b['entry'],16),int(b['end_exclusive'],16))==(lo,hi),'physical bounded span changed')
    cp=P/'source-boundary-01.json';need(sha(cp)=='7ff80975a29c048ec08a1915669cf1d62ffd1eb5d6878503e0330a059e0f2b25','certified caller source changed')
    caller_pin='b84224cf1d15ad3ea2d96356d8d68e26c8064358886682cbf7383ffdbf8f738e'
    status(json.loads((P/'capture-boundary-01.status.json').read_text()),caller_pin)
    need(sha(P/'capture-dismiss-boundary.py')==caller_pin,'caller capture driver changed')
    caller=json.loads(cp.read_text())
    need(caller.get('wrapper_complete') is True and caller.get('invocation_driver_sha256')==caller_pin,'complete actual caller capture required')
    vfile=W/'validate-title-source-annotations.py';need(sha(vfile)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    spec=importlib.util.spec_from_file_location('current_reviewed_roles',vfile);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    annotations=[v.validate(s),v.validate(caller)]
    facts=derive(s,caller);controls=[]
    for cid,pc,kind,value,marker in [('roster-base-field-changed',0x263758,'target','0x209a208','roster base identity changed'),('actor-unit-offset-changed',0x263e30,'offset',0x38,'actor unit-pointer identity changed'),('selector-tail-changed',0x31b8da,'args','0x263750','selector instruction/transfer changed')]:
        z=copy.deepcopy(s);i=next(i for r in z['ranges'] for i in r['instructions'] if int(i['pc'],16)==pc)
        if kind=='target':i['memory'][0]['rip_target']=value
        elif kind=='offset':i['memory'][0]['displacement']=value
        else:i['args']=value
        try:derive(z,caller)
        except ValueError as e:
            need(marker in str(e),'wrong control detector');controls.append(dict(id=cid,diagnostic=str(e),method='Synthetic source-record control, not machine-code execution'))
        else:raise ValueError('changed selector accepted '+cid)
    z=copy.deepcopy(st);z['exit']=1
    try:status(z,cap_pin)
    except ValueError as e:controls.append(dict(id='failed-upstream-status',diagnostic=str(e),method='In-process status-guard control; not actual CLI refusal'))
    else:raise ValueError('failed upstream accepted')
    result=dict(producer_complete=True,method='A original complete local selector/leaf CFG and access composition',driver_sha256=sha(Path(__file__)),
      source_pins=[dict(path=sp.name,sha256=sha(sp)),dict(path=cp.name,sha256=sha(cp))],capture_driver_sha256=cap_pin,exe_sha256=s['exe_sha256'],
      annotation_prerequisites=annotations,physical_bodies=bodies,facts=facts,controls=controls,
      acceptance='Producer-valid only. Independent review/canonical consumption pending; fullUQ147 and formerly-runtime residue remain open.')
    with out.open('x') as f:json.dump(result,f,indent=2)
    print('Closed Dismiss slot3 read-only selector; no KO/status filter or object writes. Natural admission/lifetime/UQ147 remain OPEN.')
if __name__=='__main__':main()
