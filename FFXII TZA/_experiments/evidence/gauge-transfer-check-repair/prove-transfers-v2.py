"""Exact per-path callback binding and local consumer effects, STATIC_ONLY.

This checks original bytes and reviewed access roles before deriving bounded
facts. Normal ABI returns/private stack and valid non-overlapping record state
are premises. Opaque helper effects and natural initialized reach remain open.
"""
import copy, hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
P=next(p for p in OUT.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())/'Database/FFXII TZA/_experiments/evidence/ov42-gauge-callback-binding'
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def module(name,file):
    s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def checked_transfers(rows, start, end, allowed_calls, *, internal_branches=True):
    """Check all local calls and branches; indirect or unproved exits fail closed."""
    pcs={int(i['pc'],16) for i in rows}
    seen=[];calls=[]
    for i in rows:
        m=i['mnemonic']
        if not(m.startswith('call') or m.startswith('j') or m in ('loop','loope','loopne')):continue
        try:target=int(i['args'],0)
        except (TypeError,ValueError):raise ValueError('unproved indirect transfer '+i['pc'])
        row=dict(pc=i['pc'],mnemonic=m,target=hex(target))
        seen.append(row)
        if m.startswith('call'):
            calls.append((i['pc'],hex(target)))
            need((i['pc'],hex(target)) in allowed_calls,'unexpected direct call '+i['pc'])
        else:
            need(internal_branches and start<=target<end and target in pcs,'unproved branch exit or target '+i['pc'])
    need(calls==allowed_calls,'complete direct call set changed')
    return seen

def derive(ix):
    ops=[
      (0x2963c1,'lea','rax, [rip + 0x5408]'),(0x2963ce,'mov','r9, rbx'),(0x2963d1,'mov','qword ptr [rsp + 0x20], rax'),(0x2963d6,'xor','r8d, r8d'),(0x2963e0,'xor','edx, edx'),(0x2963e2,'call','0x3f89c0'),
      (0x2963e7,'lea','rax, [rip + 0x5422]'),(0x2963ee,'mov','r9, rbx'),(0x2963f4,'mov','qword ptr [rsp + 0x20], rax'),(0x296402,'call','0x3f89c0'),
      (0x297c45,'je','0x297ce2'),(0x297c7e,'lea','rax, [rip + 0x3b4b]'),(0x297c8a,'mov','r9, rsi'),(0x297c8d,'mov','qword ptr [rsp + 0x20], rax'),(0x297c9a,'call','0x3f89c0'),
      (0x297c9f,'lea','rax, [rip + 0x3b6a]'),(0x297ca6,'mov','r9, rsi'),(0x297cac,'mov','qword ptr [rsp + 0x20], rax'),(0x297cb3,'lea','rcx, [rdi + 0x58]'),(0x297cb7,'call','0x3f89c0'),
      (0x297ce8,'mov','qword ptr [rdi + 0x48], rsi'),(0x297cec,'mov','qword ptr [rdi + 0xa0], rsi'),(0x297cf8,'mov','dword ptr [rdi + 0xb0], ecx'),
      (0x3f89cf,'push','rdi'),(0x3f89d0,'sub','rsp, 0x20'),(0x3f89d4,'mov','ebp, edx'),(0x3f89d6,'mov','ebx, r8d'),(0x3f89d9,'xor','edx, edx'),(0x3f89db,'mov','rdi, r9'),(0x3f89de,'mov','rsi, rcx'),(0x3f89e1,'lea','r8d, [rdx + 0x58]'),(0x3f89e5,'call','0x861ec0'),
      (0x3f89ea,'mov','rax, qword ptr [rsp + 0x50]'),(0x3f89ef,'or','word ptr [rsi + 0x26], 1'),(0x3f89f4,'mov','qword ptr [rsi + 0x38], rax'),(0x3f89f8,'mov','dword ptr [rsi + 0x40], ebx'),(0x3f89fb,'mov','qword ptr [rsi + 0x48], rdi'),(0x3f89ff,'test','rax, rax'),(0x3f8a02,'je','0x3f8a0e'),(0x3f8a04,'mov','r8, rbp'),(0x3f8a07,'xor','edx, edx'),(0x3f8a09,'mov','rcx, rsi'),(0x3f8a0c,'call','rax'),
      (0x2973f8,'cmp','edx, r9d'),(0x2973fb,'je','0x2974c5'),(0x297401,'test','r8d, r8d'),(0x297404,'je','0x2974c5'),(0x29740a,'test','byte ptr [rcx + 0x26], 1'),(0x29740e,'jne','0x297437'),
      (0x29749f,'mov','word ptr [rbx + 0x14], ax'),(0x2974a3,'mov','eax, dword ptr [rbx]'),(0x2974a5,'sar','eax, 4'),(0x2974a8,'mov','dword ptr [rbx + 0x50], eax'),(0x2974c0,'or','word ptr [rbx + 0x26], 1')]
    for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'required binding/effect instruction changed '+hex(pc))
    handlers=[]
    for pc,target in [(0x2963c1,0x29b7d0),(0x2963e7,0x29b810),(0x297c7e,0x29b7d0),(0x297c9f,0x29b810)]:
        row=ix[pc];mem=row['memory']
        need(len(mem)==1 and mem[0]['role']=='addr' and int(mem[0]['rip_target'],16)==target,'actual LEA callback identity changed '+hex(pc))
        handlers.append(dict(lea=hex(pc),handler=hex(target)))
    m=ix[0x3f89f4]['memory'][0]
    need(m['role']=='w' and m['size']==8 and m['base']=='rsi' and m['displacement']==0x38,'actual callback store role/layout changed')
    m=ix[0x3f89ea]['memory'][0]
    need(m['role']=='r' and m['size']==8 and m['base']=='rsp' and m['displacement']==0x50,'actual fifth-argument load changed')
    # Windows x64 call pushes8, this body pushes8 and subtracts32.
    need(0x50-8-0x20-8==0x20,'caller-to-callee fifth argument stack identity wrong')
    tail=[i for pc,i in sorted(ix.items()) if 0x297ce2<=pc<0x297d04]
    tail_transfers=checked_transfers(tail,0x297ce2,0x297d04,[],internal_branches=False)
    writes=[(int(i['pc'],16),m['base'],m['displacement'],m['size']) for i in tail for m in i['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']
    need(writes==[(0x297ce8,'rdi',0x48,8),(0x297cec,'rdi',0xa0,8),(0x297cf8,'rdi',0xb0,4)],'matching-row callback preservation own footprint changed')
    consumer=[i for pc,i in sorted(ix.items()) if 0x2973e0<=pc<0x2974d7]
    calls=[(i['pc'],i['args']) for i in consumer if i['mnemonic']=='call']
    consumer_transfers=checked_transfers(consumer,0x2973e0,0x2974d7,[('0x297414','0x271960'),('0x297430','0x272730'),('0x297450','0x2726c0'),('0x297498','0x2727c0')])
    own=[dict(pc=i['pc'],memory=m) for i in consumer for m in i['memory'] if m['role'] in ['w','rw'] and m['base'] not in ['rsp']]
    need([(x['pc'],x['memory']['displacement'],x['memory']['size']) for x in own]==[('0x29749f',0x14,2),('0x2974a8',0x50,4),('0x2974c0',0x26,2)],'complete consumer own nonstack writes changed')
    return dict(callback_sources=handlers,
      constructor='3F89C0 reads fifth argument from its currentSP+50h (callerSP+20h), writes QWORDview+38, DWORD+40 and QWORDcontext+48; nonNULL callback is called synchronously with (view,event0,incomingEDX). Normal ABI/private disjoint storage and canonical memory-fill semantics are premises, not natural initialization proof.',
      default='296360 registration leg prescribes29B7D0 at0209C240 and29B810 at0209C298 with the incoming object as context. Entry guards/unregistration occur before that leg; registration is conditional.',
      slot='297C10 free-entry initialization prescribes the same two handlers at row androw+58. Existing matching row jumps to297CE2, writes context+48/+A0 and id+B0 only, and does not call initializer or write callback+38/+90. Thus this call cannot universally re-establish handler identity; prior state remains a premise.',
      consumer='Complete2973E0 has only four direct calls to271960/272730/2726C0/2727C0, no indirect call and no direct handler call. Its own writes are WORDview+14, DWORDview+50 and RMW WORDview+26. The canonical callback table already states handlers call2973E0; the opposite claimed direct edge is not supported by this body.',
      synchronous_limit='A caller reaching3F8980(event1) with a valid nonNULL installed handler can synchronously reach2973E0 and its view updates/helpers before resource code continues. Existing EXP243 zero dispatcher hits do not test this initialized boundary. Opaque animation helper effects, transitive callbacks, actual handler field state and resource-binding preservation remain open.',
      direct_calls=calls,local_transfer_checks=dict(consumer=consumer_transfers,matched_tail=tail_transfers),own_consumer_writes=own,
      remaining='No native execution, actual initialization, scheduling, lifetime, full resource-window invariance or presentation result. Do not interpret direct call-set completeness as transitive no-callback/no-global-write proof.')
def main():
    out=OUT/sys.argv[1];need(not out.exists(),'fresh output required')
    manifest=P/'manifest.json'
    need(sha(manifest)=='03ce4f39f2222feb7b1d3671b13fd03c86cdca9df1f79daf1f8cc07aa7116d0e','reviewed predecessor manifest changed')
    members=json.loads(manifest.read_text())['members']
    need(len(members)==65,'reviewed predecessor member count changed')
    for x in members:
        f=P/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'reviewed predecessor member changed '+x['path'])
    C=module('capture_prerequisites','capture_prerequisites.py')
    qualified=[C.check(P,'prepare-extents.py','capture.py','extents-01','capture-01','extents-01.json','source-01.json',['0x296360','0x297c10','0x3f89c0']),C.check(P,'prepare-target-extents.py','capture-target.py','target-extents-01','capture-target-01','target-extents-01.json','target-source-01.json',['0x2973e0'])]
    need(sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    V=module('roles','validate-title-source-annotations.py');ix={};annotations=[]
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed')
    pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0]
    secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    for file in ['source-01.json','target-source-01.json']:
        s=json.loads((P/file).read_text());need(s['exe_sha256']==PIN,'source image differs');annotations.append(V.validate(s))
        for r in s['ranges']:
            a,b=int(r['start'],16),int(r['end_exclusive'],16)
            ranges=[raw[off+a-0x120000-rva:off+b-0x120000-rva] for _,rva,sz,off in secs if 0x120000+rva<=a and b<=0x120000+rva+sz]
            need(len(ranges)==1 and ranges[0]==bytes.fromhex(''.join(i['bytes'] for i in r['instructions'])),'not original physical bytes')
            ix.update({int(i['pc'],16):i for i in r['instructions']})
    facts=derive(ix);controls=[]
    tests=[
      ('secondary-handler-memory-identity',0x2963e7,'memory','rip_target','0x29b7d0','actual LEA callback identity changed'),
      ('callback-store-memory-offset',0x3f89f4,'memory','displacement',0x40,'actual callback store role/layout changed'),
      ('consumer-tail-to-handler',0x297435,'row','args','0x29b7d0','unproved branch exit or target'),
      ('consumer-indirect-jump',0x297435,'row','args','rax','unproved indirect transfer'),
      ('matched-tail-to-initializer',0x297cfe,'jump','args','0x3f89c0','unproved branch exit or target')]
    for case_id,pc,kind,key,value,marker in tests:
        z=copy.deepcopy(ix)
        if kind=='memory':z[pc]['memory'][0][key]=value
        else:
            z[pc][key]=value
            if kind=='jump':z[pc]['mnemonic']='jmp'
        try:derive(z)
        except ValueError as e:
            need(marker in str(e),'wrong detector for '+case_id+': '+str(e))
            controls.append(dict(id=case_id,pc=hex(pc),mutation=dict(kind=kind,key=key,value=value),refused=str(e),method='Synthetic source-record mutation, not original execution'))
        else:raise ValueError('source control accepted '+case_id)
    with out.open('x') as f:json.dump(dict(producer_complete=True,method='A STATIC_ONLY original byte/dataflow/local footprint analysis',driver_sha256=sha(Path(__file__)),predecessor_driver_sha256=sha(P/'prove.py'),review_commit='95d495604a3994a0fe0078e4b0620a168c9137b7',input_manifest_sha256=sha(manifest),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['source-01.json','target-source-01.json']],capture_prerequisites=qualified,annotation_prerequisites=annotations,facts=facts,source_controls=controls,acceptance='Producer validity only; project independent review and consumer incorporation pending.'),f,indent=2)
    print('PROVED retained local facts with all call/jump/conditional transfer checks; five targeted synthetic counterexamples refused; no new native/live observations')
if __name__=='__main__':main()
