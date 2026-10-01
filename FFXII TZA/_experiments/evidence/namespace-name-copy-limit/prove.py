"""Signed-limit and NEXT-byte induction from retained complete shipping code."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
TOOLS=P.parent if (P.parent/'validate-title-source-annotations.py').is_file() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(out,src):
    if out.exists():raise RuntimeError('immutable result exists')
    rdir=src/'retained'
    manifest=rdir/'parent-manifest.json'
    if sha(manifest)!='b9f212c1d22eb7398d16d5c2d184ce7c0bca4b6900e2cc0f94af5662605b82c1':raise RuntimeError('retained parent manifest identity failed')
    m=json.loads(manifest.read_text());members={x['path']:x for x in m['members']}
    if len(members)!=60:raise RuntimeError('retained parent population incomplete')
    for name in ['source-01.json','capture.py','capture-01.status.json','capture-01.stdout','capture-01.stderr']:
        if name not in members or sha(rdir/name)!=members[name]['sha256'] or (rdir/name).stat().st_size!=members[name]['bytes']:
            raise RuntimeError('retained member identity failed: '+name)
    status=json.loads((rdir/'capture-01.status.json').read_text())
    if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(rdir/'capture.py') or not(rdir/'capture-01.stdout').read_bytes() or(rdir/'capture-01.stderr').read_bytes():
        raise RuntimeError('retained source capture failed/incomplete')
    v=json.loads((rdir/'source-01.json').read_text())
    V=load('copylimit_reviewed_roles',TOOLS/'validate-title-source-annotations.py');roles=V.validate(v)
    G=load('copylimit_reviewed_graph',TOOLS/'prove_owner_reload_order.py')
    if sha(TOOLS/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('reviewed graph helper identity changed')
    body=next(r for r in v['ranges'] if r['start']=='0x2df880')
    raw=bytes.fromhex(''.join(i['bytes'] for i in body['instructions']))
    if body['end_exclusive']!='0x2df8d9' or len(raw)!=89 or hashlib.sha256(raw).hexdigest()!='f71f6f4a0633fa327a47b23f16231e23be086270b133f30357e49520d74f9800':raise RuntimeError('required complete original copier identity failed')
    expected=[(0x2df880,'movsxd','rax, ecx'),(0x2df883,'mov','r11, r8'),(0x2df886,'lea','r8, [rip + 0x1e7f773]'),
      (0x2df88d,'movsxd','rcx, edx'),(0x2df890,'xor','r10d, r10d'),(0x2df893,'mov','rax, qword ptr [r8 + rax*8]'),
      (0x2df897,'mov','rax, qword ptr [rax + rcx*8]'),(0x2df89b,'test','rax, rax'),(0x2df89e,'jne','0x2df8a4'),
      (0x2df8a0,'or','eax, 0xffffffff'),(0x2df8a3,'ret',''),(0x2df8a4,'mov','rdx, r11'),(0x2df8a7,'movsxd','r9, r9d'),
      (0x2df8aa,'sub','rdx, rax'),(0x2df8ad,'mov','r8, rax'),(0x2df8b0,'neg','r8'),(0x2df8b3,'movzx','ecx, byte ptr [rax]'),
      (0x2df8b6,'inc','r10d'),(0x2df8b9,'mov','byte ptr [rdx + rax], cl'),(0x2df8bc,'lea','rax, [rax + 1]'),
      (0x2df8c0,'lea','rcx, [r8 + rax]'),(0x2df8c4,'cmp','rcx, r9'),(0x2df8c7,'jge','0x2df8ce'),
      (0x2df8c9,'cmp','byte ptr [rax], 0'),(0x2df8cc,'jne','0x2df8b3'),(0x2df8ce,'movsxd','rax, r10d'),
      (0x2df8d1,'mov','byte ptr [rax + r11], 0'),(0x2df8d6,'xor','eax, eax'),(0x2df8d8,'ret','')]
    got=[(int(i['pc'],16),i['mnemonic'],i['args']) for i in body['instructions']]
    if got!=expected:raise RuntimeError('complete instruction sequence changed')
    ix={int(i['pc'],16):i for i in body['instructions']}
    full=G.graph(ix,0x2df880,0x2df8d9)
    null=G.graph(ix,0x2df880,0x2df8d9,fixed={0x2df89e:False})
    nonnull=G.graph(ix,0x2df880,0x2df8d9,fixed={0x2df89e:True})
    writes=[(i['pc'],i['memory']) for i in body['instructions'] if any(x['role'] in ('w','rw') for x in i['memory'])]
    if sorted(full['returns'])!=[0x2df8a3,0x2df8d8] or full['calls'] or [pc for pc,_ in writes]!=['0x2df8b9','0x2df8d1'] or any(x['role'] in ('w','rw') for pc in null['visited'] for x in ix[pc]['memory']):raise RuntimeError('write/return/call population changed')
    for a,b in [(0x2df8b3,0x2df8c4),(0x2df8b9,0x2df8c4),(0x2df8bc,0x2df8c9),(0x2df8c4,0x2df8c9),(0x2df8d1,0x2df8d8)]:
        if not G.dominates(nonnull,a,b):raise RuntimeError('mandatory copy/next-byte/return order changed')
    # Induction is attached to the original operations above, not inferred from witness outputs.
    certificate={
      'entry':'After nonNULL setup: RAX=S,R11=D,RDX=D-S,R8=-S,R9=sign_extend_i32(argR9),R10D=0.',
      'iteration_start':'At B3 before iteration i+1, RAX=S+i,R10D=i,RDX=D-S,R8=-S; accessible disjoint memory keeps original future source bytes.',
      'copy':'B3 loads source[i]; B6 increments count; B9 writes destination[i]; BC advances source pointer. No first/current-byte NUL test precedes copy.',
      'count':'C0 computes i+1 via (-S)+(S+i+1); C4/C7 compare that positive offset against signed c. If i+1>=c, exit before any next-byte read.',
      'next_byte':'Only when i+1<c, C9 reads source[i+1]; CC continues iff nonzero. Therefore the earliest examined zero is q>=1, regardless source[0].',
      'bound':'M=max(1,c),1<=M<=INT32_MAX. Either next-byte zero stops at q<M or count stops at M; I=min(q,M). If no q before M, I=M. Counter stays1..INT32_MAX, so signed count never wraps.',
      'exit':'CE signextends copied count, D1 writes destination[I]=0, D6 zeroes EAX (rawRAX0), D8 returns. NULL branch A0 zeroextends EAXFFFFFFFF to rawRAX00000000FFFFFFFF and A3 returns without destination writes.'}
    partitions=[{'c':'INT32_MIN..1','I':1,'next_byte_read':False,'destination_bytes_written':2},
      {'c':'2..INT32_MAX','q':'1..c-1','I':'q','last_source_index_read':'q (zero)','destination_bytes_written':'q+1'},
      {'c':'2..INT32_MAX','q':'c..infinity or no zero before c','I':'c','last_source_index_read':'c-1','destination_bytes_written':'c+1'}]
    witnesses=[]
    for raw_input,c in [(b'ABC\0',2),(b'ABC\0',0),(b'ABC\0',-1),(b'\0A\0',259),(b'\0\0',259),(b'\0A\0',1)]:
        q=next(k for k in range(1,len(raw_input)) if raw_input[k]==0);I=min(q,max(1,c))
        witnesses.append({'source_bytes':raw_input.hex(),'signed_limit':c,'copied':I,'destination_bytes':(raw_input[:I]+b'\0').hex(),'next_NUL_examined':q<I+1 and I<c,'method':'Algebraic illustration of the source-derived invariant; not native/isolated/live execution'})
    result={'method':'A STATIC_ONLY retained original-code induction','producer_complete':True,'driver_sha256':sha(Path(__file__)),
      'source_pins':[{'path':'retained/source-01.json','sha256':sha(rdir/'source-01.json')}],
      'external_parent':{'path':'_experiments/evidence/sd194-stale-name-slice/manifest.json','sha256':sha(manifest),'commit':'d7ff30672166c95f2533a144d55e1346e447482d','scope':'Original source identity only; builder semantic review not assumed accepted'},
      'body_sha256':hashlib.sha256(raw).hexdigest(),'body_bytes':len(raw),'instruction_assertions':len(expected),'annotation_prerequisite':roles,
      'graphs':[{'entry':hex(g['entry']),'visited':len(g['visited']),'returns':[hex(x) for x in g['returns']]} for g in (full,null,nonnull)],
      'induction':certificate,'symbolic_partitions':partitions,'algebraic_witnesses':witnesses,
      'new_propositions':['R9D is signextended; <=1 limits still copy one byte and write a second-byte terminator.','The initial source byte is copied without testing it for NUL; a nonempty next byte may be read/copied after an empty-string first byte.'],
      'preserved_existing_propositions':['NULL returns signed32-1 without destination writes.','For positive c/nonempty normal source, copied=min(firstNUL,c) and destination requires copied+1 (worst c+1).'],
      'limitations':['Valid namespace/table/index and accessible sufficiently large disjoint source/destination memory assumed.','No natural empty source or nonpositive limit reachability established; current named field caller uses259.','General aliasing, invalid pointer/index memory, unavailable bytes after first NUL and native faults excluded.','No original/native/game code executed; witnesses are not independent behavior observations.']}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'producer_complete':True,'new_propositions':result['new_propositions'],'instruction_assertions':len(expected),'symbolic_partitions':len(partitions),'native_or_live_runs':0}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--src',type=Path,default=P);a=p.parse_args();main(a.out,a.src)
