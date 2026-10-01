"""Attach phase/flag/release invariants to complete original instructions."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
TOOLS=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
    if out.exists():raise RuntimeError('immutable result exists')
    status=json.loads((src/'capture-01.status.json').read_text())
    if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
    v=json.loads((src/'source-01.json').read_text())
    if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('capture wrapper incomplete/mixed')
    roles=load('s33phase_roles',TOOLS/'validate-title-source-annotations.py').validate(v)
    G=load('s33phase_graph',TOOLS/'prove_owner_reload_order.py')
    if sha(TOOLS/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph helper identity changed')
    expected={0x3fa820:(0x3fa900,'f6bc9f1844901aea72408529e9905c0184d29b0f1ac5d96685c24921638f4ccf'),0x3fc510:(0x3fc8fd,'6b1ad8d59dfa3d6b608b41cb344f8ff38803d4a4a9709387c7fa3852569e1fcd'),0x3fa790:(0x3fa81f,'f2c8008dda3771dabadb08a81bf33d78054560f88168e0e1349880726d365ee6'),0x3fa4e0:(0x3fa567,'0c7d7665c7816062cbb199e1b1b703a8fd50684fa76e9a1c2e5c5ea6918790f0'),0x1ede80:(0x1edebd,'41ba827c866d989629f556addefe4d246f84b8c12bca5613628732ca0fb28fa5')}
    bodies={int(r['start'],16):r for r in v['ranges']};graphs=[];ix={}
    if set(bodies)!=set(expected):raise RuntimeError('complete source population changed')
    for lo,(hi,pin) in expected.items():
        body=bodies[lo];raw=bytes.fromhex(''.join(i['bytes'] for i in body['instructions']))
        if body['end_exclusive']!=hex(hi) or len(raw)!=hi-lo or hashlib.sha256(raw).hexdigest()!=pin or body['sha256']!=pin:raise RuntimeError('required original body identity failed')
        local={int(i['pc'],16):i for i in body['instructions']};ix.update(local)
        graph=G.graph(local,lo,hi);graphs.append({'entry':hex(lo),'visited':len(graph['visited']),'returns':[hex(x) for x in sorted(graph['returns'])],'calls':[{'pc':hex(pc),'target':target} for pc,target in graph['calls']]})
    pins=[(0x3fa82f,'movzx','ebx, word ptr [rcx + 0x272]'),(0x3fa836,'mov','esi, edx'),(0x3fa83b,'test','bl, 1'),(0x3fa844,'test','bl, 2'),(0x3fa84d,'or','bx, 2'),(0x3fa851,'mov','word ptr [rcx + 0x272], bx'),(0x3fa858,'test','bl, 8'),(0x3fa85d,'test','edx, edx'),(0x3fa8e0,'mov','dword ptr [rdi + 0x290], esi'),(0x3fa8e6,'mov','dword ptr [rdi + 0x294], 0'),
      (0x3fa7b1,'mov','rbx, qword ptr [rdx + 0x278]'),(0x3fa7b8,'cmp','dword ptr [rdx + 0x260], esi'),(0x3fa7c3,'mov','word ptr [rdx + 0x272], si'),(0x3fa7ca,'call','0x3fa4e0'),(0x3fa7cf,'mov','rdx, rbx'),(0x3fa7dc,'mov','rbx, qword ptr [rdi + 0x2490]'),(0x3fa7f3,'call','0x3fc510'),(0x3fa7f8,'call','0x1ede80'),(0x3fa7ff,'je','0x3fa80d'),(0x3fa808,'call','0x3fc170'),
      (0x3fa54b,'mov','qword ptr [rdx + 0x278], rax'),(0x3fa552,'mov','qword ptr [rdx + 0x280], rax'),(0x3fa559,'mov','word ptr [rdx + 0x272], ax'),(0x3fa560,'mov','dword ptr [rdx + 0x260], eax'),
      (0x3fc688,'mov','ecx, dword ptr [rbx + 0x260]'),(0x3fc68e,'sub','ecx, 1'),(0x3fc691,'je','0x3fc80f'),(0x3fc697,'sub','ecx, 1'),(0x3fc69a,'je','0x3fc7dd'),(0x3fc6a0,'cmp','ecx, 1'),(0x3fc6a3,'jne','0x3fc8ea'),(0x3fc6a9,'cmp','word ptr [rbx + 0x270], dx'),(0x3fc6b0,'jg','0x3fc6b8'),(0x3fc6b2,'mov','dword ptr [rbx + 0x260], edx'),(0x3fc6b8,'mov','edx, dword ptr [rbx + 0x290]'),(0x3fc6c0,'je','0x3fc8ea'),
      (0x3fc7dd,'movzx','eax, word ptr [rbx + 0x272]'),(0x3fc7e4,'test','al, 2'),(0x3fc7e6,'je','0x3fc8ea'),(0x3fc7ec,'mov','dword ptr [rbx + 0x260], 3'),(0x3fc7f6,'cmp','dword ptr [rbx + 0x290], edx'),(0x3fc7fc,'jne','0x3fc8ea'),(0x3fc802,'mov','ecx, 0xffdf'),(0x3fc807,'and','ax, cx'),
      (0x3fc80f,'or','word ptr [rbx + 0x272], 0x20'),(0x3fc82e,'ucomiss','xmm3, xmm0'),(0x3fc831,'jp','0x3fc85e'),(0x3fc833,'jne','0x3fc85e'),(0x3fc839,'mov','dword ptr [rbx + 0x260], 2'),(0x3fc85e,'movss','xmm2, dword ptr [rbx + 0x264]'),(0x3fc879,'movss','xmm0, dword ptr [rip + 0x1a0183b]'),(0x3fc881,'mulss','xmm0, dword ptr [rip + 0x503a33]'),(0x3fc88d,'addss','xmm0, xmm2'),(0x3fc895,'movss','dword ptr [rbx + 0x264], xmm0'),(0x3fc8ad,'comiss','xmm5, xmm0'),(0x3fc8c2,'comiss','xmm4, xmm0'),(0x3fc8c7,'comiss','xmm1, xmm4'),(0x3fc8d5,'mov','dword ptr [rbx + 0x260], 2'),
      (0x3fc5ea,'mulss','xmm0, dword ptr [rip + 0x915a5a]'),(0x3fc5f2,'cvttss2si','eax, xmm0'),(0x3fc5f6,'add','word ptr [rbx + 0x270], ax'),(0x3fc5fd,'jns','0x3fc606'),(0x1edeb3,'mov','eax, 1')]
    for pc,m,a in pins:
        if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('semantic operation changed: '+hex(pc))
    neutral=G.graph(ix,0x3fa820,0x3fa900,fixed={0x3fa83e:False,0x3fa847:False,0x3fa85b:False,0x3fa85f:True})
    writes=[i for pc,i in ix.items() if pc in neutral['visited'] and any(m['role'] in ['w','rw'] and m['base'] in ['rcx','rdi'] for m in i['memory'])]
    if neutral['calls'] or [i['pc'] for i in writes]!=['0x3fa851','0x3fa8e0','0x3fa8e6']:raise RuntimeError('neutral retirement footprint changed')
    # All direct writes to flags in the local updater preserve bit0; verify the exact mask/dataflow sites.
    flagpcs=[int(i['pc'],16) for i in bodies[0x3fc510]['instructions'] if any(m['role'] in ['w','rw'] and m['base']=='rbx' and m['displacement']==0x272 for m in i['memory'])]
    if flagpcs!=[0x3fc549,0x3fc597,0x3fc5e1,0x3fc681,0x3fc756,0x3fc80f,0x3fc8e3]:raise RuntimeError('flag write population changed')
    masks=[(0x3fc545,'or','cx, 0x20'),(0x3fc58f,'mov','eax, 0xfedf'),(0x3fc594,'and','cx, ax'),(0x3fc5d1,'mov','eax, 0x200'),(0x3fc5de,'or','cx, ax'),(0x3fc64f,'mov','eax, 0xffef'),(0x3fc65c,'and','cx, ax'),(0x3fc676,'or','cx, 0x10'),(0x3fc756,'or','word ptr [rbx + 0x272], 0x40'),(0x3fc81f,'movzx','eax, word ptr [rbx + 0x272]'),(0x3fc8df,'or','ax, 4'),(0x3fc8e3,'mov','word ptr [rbx + 0x272], ax')]
    for pc,m,a in masks:
        if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('flag transfer changed')
    # No single-execution path does phase2->3 then phase3->0: handler chosen once.
    update=G.graph(ix,0x3fc510,0x3fc8fd)
    def reaches(a,b):
        seen=set();todo=[a]
        while todo:
            pc=todo.pop()
            if pc==b:return True
            if pc in seen:continue
            seen.add(pc);todo+=update['edges'][pc]
        return False
    if reaches(0x3fc7ec,0x3fc6b2):raise RuntimeError('phase2 can fall into phase3 handler')
    # Admitted fixed point: phase3,flags3,positive signedfade,mode290=0,stepScalar=0.
    fixed={0x3fc543:True,0x3fc5b2:True,0x3fc5fd:True,0x3fc610:True,0x3fc691:False,0x3fc69a:False,0x3fc6a3:False,0x3fc6b0:True,0x3fc6c0:True}
    fp=G.graph(ix,0x3fc510,0x3fc8fd,fixed=fixed)
    if 0x3fc6b2 in fp['visited'] or 0x3fc7ec in fp['visited'] or any(target!='0x808c40' for pc,target in fp['calls']):raise RuntimeError('fixed point has unexpected state/call effect')
    image=G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';raw=image.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=v['exe_sha256']:raise RuntimeError('constant image identity failed')
    pe=struct.unpack_from('<I',raw,60)[0];ns=struct.unpack_from('<H',raw,pe+6)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
    sections=[struct.unpack_from('<IIII',raw,pe+24+opt+k*40+8) for k in range(ns)]
    addr=0xd1204c
    for vs,va,rs,ro in sections:
        if 0x120000+va<=addr and addr+4<=0x120000+va+rs:constant=raw[ro+addr-0x120000-va:ro+addr-0x120000-va+4];break
    else:raise RuntimeError('unbacked decline constant')
    bits=struct.unpack('<I',constant)[0]
    if(bits&0x7f800000)==0x7f800000:raise RuntimeError('fixed-point multiplier not finite')
    result={'method':'A STATIC_ONLY original-code phase/flag induction','producer_complete':True,'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(src/'source-01.json')}],'annotation_prerequisite':roles,'graphs':graphs,'instruction_assertions':len(pins)+len(masks),'neutral_graph':{'visited':len(neutral['visited']),'calls':neutral['calls'],'object_writes':[i['pc'] for i in writes]},'flags_write_population':[hex(x) for x in flagpcs],
      'retirement':'Active,notretired,flag8clear,neutralarg0: setsflagbit1,stores290=0/294=0; preservesphase260/motion264/fade270. No callee effects on this path.',
      'phase_protocol':'Updater chooses handler once from phase260: phase1 motion/float predicates can write2; phase2 withretiredbit1 writes3 andmode290=0 clearsflag20; phase3 writes0 only when signedfade270<=0 after earlierfadeupdate. Local flag stores preserve occupiedbit0. This is not a universal elapsed-frame guarantee.',
      'manager_protocol':'First pass savesnext278 before testingphase260; phase0 flags cleared and target unlinked through3FA4E0; savednext survivesclearedlinks, so multiplephase0 slots canrelease. Onlythen secondpasscalls3FC510. A phase0 store bythatupdater happensafterthisinvocation firstpass. Rendering3FC170 andotherwrites remain separate, notassumed inert.',
      'gate_limit':'001EDE80 default branches return1, notret0. Therefore secondpassrendercall cannotbe excluded merelyfrom defaultzero globals. No conditional-nextpass guarantee is widenedto wholeoriginalrender/scheduling.',
      'fixed_point':{'method':'Source-derived symbolic invariant, not execution/sampling','domain':'local3FC510 repeatedly,validrecord/ABI/noninterference,phase3,flags3,0<signedword270<=0x4000,290=0,frameStep01DFE0BC=+0 or-0,ordinarymaskedFP','result':'Original MULSS byfiniteconstant yieldssignedzero; CVTTSS2SI gives0; ADD lowword0 preservespositivefade and JNS. Phase3positivefade skipsphase0store,mode0 bypassesapplicationcalls,flags/phase remainunchanged. No universal51local-call limit follows over thisadmitteddomain; naturalzero-step/reachability/render effects NOTproved.','decline_constant':{'address':hex(addr),'bytes':constant.hex(),'f32':struct.unpack('<f',constant)[0]},'visited':len(fp['visited'])},
      'prior_R7':'RetainedOPUS result/stdout reportsfive retiredslots releasedon51stupdate initsfixture. The48agedprobe is READMEprose only, notaseparate rawresult inthisrecord. No peer-native tests rerun/credited here.',
      'limits':['Natural initialized phase/motion/frameStep/cadence/dropinterleaving/consequence remainOPEN.','Firstpass andlocalupdater facts do not establishrender3FC170 effects,wholemanager invariants orliveelapsed timing.','Generalinvalidlist/pointer/alias/non-normalcallee/MXCSR exceptions outside the stateddomain. No fullfloattrajectory/bit-exact51 algebra claimed.'],
      'consumer':'Correctfixedretirement-window assumptions; collector mustbracket phase260,occupied/retireflags272,fade270,motion264/mode290/frameStep01DFE0BC andoriginalupdate/release stages. Keepnormaldrop->visualcreation->zerohandle->tick/consequence separate.'}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'instruction_assertions':result['instruction_assertions'],'closed_bodies':len(graphs),'method':'A STATIC_ONLY','native_runs':0,'game_runs':0}))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output)
