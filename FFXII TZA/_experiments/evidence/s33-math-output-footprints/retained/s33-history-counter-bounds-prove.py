"""Original-byte-bound counter induction; no machine-code/game execution."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def i32(n):
    n &= 0xffffffff
    return n-0x100000000 if n & 0x80000000 else n
def transition(s):
    incremented=i32(s+1)
    stored=6 if incremented>=6 else incremented
    decremented=i32(stored-1)
    return incremented,stored,max(decremented,0)
def main(src,out):
    if out.exists():raise RuntimeError('immutable result exists')
    status=json.loads((src/'capture-01.status.json').read_text())
    if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
    v=json.loads((src/'source-01.json').read_text())
    if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('capture wrapper incomplete/mixed')
    roles=load('history_roles',T/'validate-title-source-annotations.py').validate(v)
    if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph identity changed')
    G=load('history_graph',T/'prove_owner_reload_order.py')
    expected={0x3fc170:(0x3fc3e2,'300218cc875eb19462bfea57a8c3b410a4e43d627b32f3639f4428f28c1bed08'),0x3fbe90:(0x3fc16a,'17dc1493443b353347e0c573bf8d574925227261416ce81b83f2437b65e63743'),0x3fa160:(0x3fa4d6,'99c3786dc8adeebe41cf149b3a7cee29446a754db3d15403d62bc6052295df1b'),0x275550:(0x27556c,'771237f175402fe6087bc10ab8c25a8724402467f8ff9a656d0a33d3fdc6844f'),0x202c90:(0x202c97,'1d6b940f3d67615ccf56ea1aa1bc0ed6bbf1694ec9b888a6340b0894065ad514')}
    bodies={int(r['start'],16):r for r in v['ranges']};ix={};graphs=[]
    if set(bodies)!=set(expected):raise RuntimeError('required body population changed')
    for lo,(hi,pin) in expected.items():
        b=bodies[lo];raw=bytes.fromhex(''.join(i['bytes'] for i in b['instructions']))
        if b['end_exclusive']!=hex(hi) or len(raw)!=hi-lo or sha_bytes(raw)!=pin or b['sha256']!=pin:raise RuntimeError('required complete body changed')
        local={int(i['pc'],16):i for i in b['instructions']};ix.update(local);g=G.graph(local,lo,hi)
        graphs.append({'entry':hex(lo),'returns':[hex(x) for x in sorted(g['returns'])],'visited':len(g['visited']),'calls':[{'pc':hex(pc),'target':target} for pc,target in g['calls']]})
    parent=src/'retained/parent-manifest.json';pinned_parent='10529734543712b86f86c24453c8b01f468e21f3d1abb9afe69c067e65072502'
    if sha(parent)!=pinned_parent:raise RuntimeError('retained parent identity failed')
    manifest=json.loads(parent.read_text());member=next(m for m in manifest['members'] if m['path']=='source-01.json')
    manager=src/'retained/manager-source-01.json'
    if sha(manager)!=member['sha256'] or manager.stat().st_size!=member['bytes']:raise RuntimeError('retained manager member changed')
    previous=json.loads(manager.read_text())
    if previous['exe_sha256']!=v['exe_sha256'] or previous['image_base']!=v['image_base']:raise RuntimeError('mixed original image')
    parent_roles=load('history_parent_roles',T/'validate-title-source-annotations.py').validate(previous)
    mb=next(b for b in previous['ranges'] if b['start']=='0x3fa790')
    mix={int(i['pc'],16):i for i in mb['instructions']};ix.update(mix)
    pins=[(0x3fa801,'lea','rcx, [rbx + 0x20]'),(0x3fa805,'mov','rdx, rbx'),(0x3fa808,'call','0x3fc170'),
      (0x3fa3ee,'mov','edx, 0x2a0'),(0x3fa3f3,'mov','rcx, rbx'),(0x3fa3f6,'call','0x275550'),(0x3fa43f,'lea','rcx, [rbx + 0x20]'),(0x3fa44b,'mov','rdx, rbx'),(0x3fa465,'call','0x3fbe90'),
      (0x275555,'sar','edx, 2'),(0x275558,'mov','rdi, rcx'),(0x27555b,'test','edx, edx'),(0x27555d,'jle','0x275566'),(0x27555f,'movsxd','rcx, edx'),(0x275562,'xor','eax, eax'),(0x275564,'rep stosd','dword ptr [rdi], eax'),
      (0x3fbed8,'lea','rbx, [rcx + 0x10]'),(0x3fbee5,'xor','r14d, r14d'),(0x3fbee8,'mov','edi, r14d'),(0x3fbef0,'mov','dword ptr [rbx + 0x70], r14d'),(0x3fc11b,'inc','edi'),(0x3fc11d,'add','rbx, 0x90'),(0x3fc124,'cmp','edi, 4'),(0x3fc127,'jb','0x3fbef0'),
      (0x3fc1bf,'lea','r14, [rcx + 0x80]'),(0x3fc1ce,'xor','r12d, r12d'),(0x3fc1d9,'mov','rbx, rdx'),(0x3fc1e2,'mov','r13, rcx'),(0x3fc1ed,'mov','esi, r12d'),(0x3fc1f6,'lea','edi, [r12 + 6]'),(0x3fc266,'cmp','r12d, 4'),(0x3fc26a,'jge','0x3fc271'),
      (0x3fc294,'inc','dword ptr [r14]'),(0x3fc297,'mov','ebx, dword ptr [r14]'),(0x3fc29a,'cmp','ebx, 6'),(0x3fc29d,'cmovge','ebx, edi'),(0x3fc2a0,'mov','dword ptr [r14], ebx'),(0x3fc2a3,'dec','ebx'),(0x3fc2a5,'test','ebx, ebx'),(0x3fc2a7,'jle','0x3fc2ee'),
      (0x3fc2a9,'add','rsi, 2'),(0x3fc2ad,'movsxd','rdi, ebx'),(0x3fc2b0,'sub','rdi, 6'),(0x3fc2b4,'lea','eax, [rbx - 1]'),(0x3fc2b7,'shl','rdi, 4'),(0x3fc2bb,'movsxd','rcx, eax'),(0x3fc2be,'add','rdi, r14'),(0x3fc2c1,'add','rsi, rcx'),(0x3fc2c4,'shl','rsi, 4'),(0x3fc2c8,'add','rsi, r13'),(0x3fc2d0,'mov','rdx, rsi'),(0x3fc2d3,'mov','rcx, rdi'),(0x3fc2d6,'call','0x202c90'),(0x3fc2db,'dec','ebx'),(0x3fc2dd,'sub','rsi, 0x10'),(0x3fc2e1,'sub','rdi, 0x10'),(0x3fc2e5,'test','ebx, ebx'),(0x3fc2e7,'jg','0x3fc2d0'),
      (0x3fc2e9,'mov','rsi, qword ptr [rsp + 0x20]'),(0x3fc2ee,'lea','rcx, [r14 - 0x60]'),(0x3fc2f2,'lea','rdx, [r14 - 0x80]'),(0x3fc2f6,'call','0x202c90'),(0x3fc381,'mov','rbx, qword ptr [rsp + 0x28]'),(0x3fc386,'add','rsi, 9'),(0x3fc38a,'inc','r12d'),(0x3fc38d,'mov','qword ptr [rsp + 0x20], rsi'),(0x3fc396,'add','r14, 0x90'),(0x3fc39d,'mov','edi, 6'),(0x3fc3a2,'cmp','r12d, 4'),(0x3fc3a6,'jb','0x3fc221'),
      (0x202c90,'movups','xmm0, xmmword ptr [rdx]'),(0x202c93,'movups','xmmword ptr [rcx], xmm0'),(0x202c96,'ret','')]
    for pc,m,a in pins:
        if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('required transfer changed: '+hex(pc))
    # Only these explicit object-address writes occur in the update body.
    direct=[i['pc'] for i in bodies[0x3fc170]['instructions'] if any(m['role'] in ['w','rw'] and m['base'] not in ['rsp','rbp','rax'] for m in i['memory'])]
    if direct!=['0x3fc294','0x3fc2a0']:raise RuntimeError('direct object write population changed')
    normal=[]
    for before in range(7):
        inc,n,steps=transition(before)
        if not 1<=n<=6 or steps!=n-1 or steps>5:raise RuntimeError('normal counter induction failed')
        destinations=[0x80+(steps-6)*16-k*16 for k in range(steps)]
        sources=[(n)*16-k*16 for k in range(steps)]
        if any(d!=s+16 or d<0x30 or d+16>0x80 for d,s in zip(destinations,sources)):raise RuntimeError('copy address interval failed')
        normal.append({'before':before,'after_increment':inc,'stored':n,'shift_copy_count':steps,'copy_intervals_relative_to_channel':[{'dst':[d,d+16],'src':[s,s+16]} for d,s in zip(destinations,sources)],'latest_copy_dst':[0x20,0x30]})
    # All signed32 states split into five exhaustive symbolic intervals.
    partitions=[{'before':[-0x80000000,-2],'increment':'before+1, signed negative','stored':'increment','loop_count':0},
      {'before':[-1,-1],'increment':0,'stored':0,'loop_count':0},
      {'before':[0,4],'increment':'before+1','stored':'before+1','loop_count':'before'},
      {'before':[5,0x7ffffffe],'increment':'before+1 >= 6','stored':6,'loop_count':5},
      {'before':[0x7fffffff,0x7fffffff],'increment':-0x80000000,'stored':-0x80000000,'loop_count':0x7fffffff}]
    if partitions[0]['before'][0]!=-0x80000000 or partitions[-1]['before'][1]!=0x7fffffff or any(a['before'][1]+1!=b['before'][0] for a,b in zip(partitions,partitions[1:])):raise RuntimeError('signed partition gap')
    boundaries=[-0x80000000,-2,-1,0,4,5,6,0x7ffffffe,0x7fffffff]
    observations=[{'before':s,'after_increment':transition(s)[0],'stored':transition(s)[1],'loop_count':transition(s)[2]} for s in boundaries]
    if transition(0x7fffffff)!=(-0x80000000,-0x80000000,0x7fffffff) or transition(0x7ffffffe)!=(0x7fffffff,6,5):raise RuntimeError('signed wrap discriminator failed')
    counters=[0x20+0x80+j*0x90 for j in range(4)]
    result={'producer_complete':True,'method':'A STATIC_ONLY byte-bound integer/address induction','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(src/'source-01.json')},{'path':'retained/manager-source-01.json','sha256':sha(manager)}],'parent_manifest_sha256':pinned_parent,'annotation_prerequisite':roles,'parent_annotation_prerequisite':parent_roles,'graphs':graphs,'instruction_assertions':len(pins),'direct_object_write_pcs':direct,
      'manager_binding':'003FA801/805: RCX=visual+20, RDX=visual. 3FC170 is the four-channel sinusoidal transform-history update, not a direct pixel renderer.',
      'creation_reset':'3FA3EE/F3/F6 supplies record/2A0 to original275550, which clears A8 DWORDs with REP STOSD. Then3FA465 calls3FBE90(record+20,record). Its four-iteration reset writes zero at each channel+80; normal nested returns/nonvolatile ABI required. Later nested effects not assumed universally bounded.',
      'counter_offsets_relative_to_visual':[hex(x) for x in counters],'normal_counter_domain':[0,6],'normal_cases':normal,'exhaustive_signed32_partitions':partitions,'algebraic_boundary_controls':observations,
      'normal_footprint':'Direct counter writes and verified16B copy sites stay within each channel[0,84), four channels atvisual20+90*j. Highestendvisual254 < phase260/flags272/list278. This is NOT the entire callee-composed write footprint; other native math callees need their own output/no-alias contracts.',
      'counterexample':'Initial signedcounter INTMAX: INC wraps toINTMIN, signedCMOVGE doesnotcap, storedINTMIN, DEC wraps toINTMAX and JLE doesnotexit. Nominal shiftloop2147483647copycalls undercontinuednormalreturns, firstaddresses faroutsideinitializedhistory. No actualunsafe read/write/crash/native/game run ornaturalreachability is claimed.',
      'limits':['Initialized0..6 preservation is conditional on no interfering counter writes, normal nonvolatile ABI and nested callees not overwriting counters/record control.','Only explicit counter stores and original202C90 copy effects are closed here. Other mathematicalcallee destination/global effects remain separate; no wholemanager-nextcall guarantee.','Creator reset calls and setter normal initialized domain are source facts, not observation of a naturally loaded/live object, allocator placement, scheduler orpresentation.','Five integer partitions/seven normal witnesses/nine boundary witnesses are source/algebraic checks, not machine-code executions.','Earlier s33 clock packet remains immutable; its conservative unclosed3FC170 boundary stands, terminology is refined additively.'],
      'consumer':'OPUS add four counters/initializedrange/signoverflow guard precondition and exactRCX=record+20 binding; FABLE correct draw-only shorthand and preserve real cadence/visual effects/wholemanager limits. Do not broaden R7 sampled51 lifetime.'}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'closed_bodies':len(graphs),'instruction_assertions':len(pins),'normal_cases':len(normal),'signed_partitions':len(partitions),'native_runs':0,'game_runs':0}))
def sha_bytes(raw):return hashlib.sha256(raw).hexdigest()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output)
