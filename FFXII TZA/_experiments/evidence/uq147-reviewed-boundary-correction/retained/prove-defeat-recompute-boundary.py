"""Conditional same-call boundary, not natural admission or mode preservation."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def derive(ix):
    pins=[(0x3010f6,'test','edi, edi'),(0x3010f8,'jne','0x301128'),(0x3010fa,'call','0x30d9a0'),(0x3010ff,'cmp','eax, 1'),(0x301102,'jne','0x301128'),(0x301104,'mov','rax, qword ptr [rip + 0x2bbe085]'),(0x30110b,'movzx','ecx, byte ptr [rax + 0x5ad5]'),(0x301112,'call','0x31b770'),(0x301117,'cmp','rbx, rax'),(0x30111a,'jne','0x301128'),(0x30111c,'xor','ecx, ecx'),(0x30111e,'call','0x3138d0'),(0x301123,'call','0x23b040')]
    for pc,m,a in pins:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'conditional same-call boundary changed '+hex(pc))
    m=ix[0x30110b]['memory'];need(len(m)==1 and(m[0]['base'],m[0]['displacement'],m[0]['size'],m[0]['role'])==('rax',0x5ad5,1,'r'),'designated member identity changed')
    m=ix[0x301104]['memory'];need(len(m)==1 and(m[0]['rip_target'],m[0]['size'],m[0]['role'])==('0x2ebf190',8,'r'),'state-slot identity changed')
    m=ix[0x31b7b1]['memory'];need(len(m)==1 and(m[0]['base'],m[0]['displacement'],m[0]['size'],m[0]['role'])==('rax',0x698,8,'r'),'lookup comparison identity changed')
    sequence=[i for pc,i in sorted(ix.items()) if 0x30111c<=pc<0x301128]
    need([i['pc'] for i in sequence]==['0x30111c','0x30111e','0x301123'],'unexpected intervening transfer/instruction')
    lookup=[i for pc,i in sorted(ix.items()) if 0x31b770<=pc<0x31b7da]
    own_writes=[dict(pc=i['pc'],memory=m) for i in lookup for m in i['memory'] if m['role'] in ('w','rw') and m['base']!='rsp']
    need(not own_writes,'lookup own effects changed')
    transfers=[dict(pc=i['pc'],mnemonic=i['mnemonic'],args=i['args']) for i in lookup if i['mnemonic'].startswith(('call','j'))]
    return dict(gates='Only after reaching003010F6: flag==0, queried mode==1, and designated-member lookup equals the defeat receiver. Prior teardown/party-condition branches are separate.',
      boundary='The original straight-line0030111C..00301128 sets ECX0, calls003138D0, then calls0023B040 immediately after normal return, with no intervening dispatcher/world-tick instruction. Dismiss refusal/success does not alter this local call sequence.',
      lookup='0031B770 locally compares QWORDunit+698 with stateBase+8+u8CID*1C8, bounds CID<=27h and iterates through236850/236820. No local nonstack writes or direct health/status check; helper filters, pointer validity, lifetime and natural admission are not proved here.',
      lookup_transfers=transfers,remaining='Mode/state/status preservation across Dismiss and earlier helpers, actual KO admission and mask7 remain OPEN. No original-code/native/live execution; existing scripted recompute fixture is not proof of the real recompute or natural scheduling.')
def main():
    out=P/sys.argv[1];need(not out.exists(),'fresh output required')
    cap=P/'capture-defeat-boundary.py';st=json.loads((P/'capture-defeat-boundary-01.status.json').read_text())
    cp='e318100b6f9582028bbdd4206d4c8643f351b270841b3a8a924d070b824be784'
    need(st['terminal'] is True and st['exit']==0 and st['exception'] is None and st['driver_sha256']==cp==sha(cap),'successful exact capture required')
    source=P/'source-defeat-boundary-01.json';raw=source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='a4febab7a65d9eb7e3b27524ca69f6906b80715e6291c946a03fd39ab27afb95','exact certified original source changed')
    s=json.loads(raw);need(s.get('wrapper_complete') is True and s.get('invocation_driver_sha256')==cp and len(s['ranges'])==2,'complete actual wrapper required')
    vfile=W/'validate-title-source-annotations.py';need(sha(vfile)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed role validator changed')
    spec=importlib.util.spec_from_file_location('reviewed_roles',vfile);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);annotation=v.validate(s)
    ix={int(i['pc'],16):i for r in s['ranges'] for i in r['instructions']};need(ix,'nonempty original instructions required')
    facts=derive(ix);cases=[]
    for cid,pc,kind,value,marker in [('recompute-redirected',0x301123,'args','0x3138d0','conditional same-call boundary changed'),('designated-member-byte-changed',0x30110b,'memory',0x5ad4,'designated member identity changed'),('lookup-pointer-field-changed',0x31b7b1,'memory',0x6a0,'lookup comparison identity changed')]:
        z=copy.deepcopy(ix)
        if kind=='args':z[pc]['args']=value
        else:z[pc]['memory'][0]['displacement']=value
        try:derive(z)
        except ValueError as e:
            need(marker in str(e),'wrong refusal detector');cases.append(dict(id=cid,pc=hex(pc),field=kind,value=value,refused=str(e),method='Synthetic source-record control, not original instruction execution'))
        else:raise ValueError('counterexample accepted '+cid)
    result=dict(producer_complete=True,method='A complete shipping bytes/local dataflow, conditional normal-return boundary',driver_sha256=sha(Path(__file__)),source_pins=[dict(path=source.name,sha256=hashlib.sha256(raw).hexdigest())],exe_sha256=s['exe_sha256'],capture_driver_sha256=cp,annotation_prerequisites=annotation,physical_bodies=s['physical_bodies'],facts=facts,source_controls=cases,acceptance='Producer-valid only; independent review/canonical consumption pending. No full UQ147 or formerly-runtime closure.')
    with out.open('x') as f:json.dump(result,f,indent=2)
    print('Confirmed conditional same-call Dismiss->recompute, designated-member byte/pointer identity; natural KO/mode/status preservation OPEN')
if __name__=='__main__':main()
