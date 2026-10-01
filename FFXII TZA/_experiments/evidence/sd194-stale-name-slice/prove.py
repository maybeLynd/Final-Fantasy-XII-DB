"""Original branch/offset proof and finite interval classification; no execution."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
TOOLS = P.parent if (P.parent / 'validate-title-source-annotations.py').is_file() else P / 'dependencies'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def main(out, src):
    if out.exists(): raise RuntimeError('immutable result exists')
    status = json.loads((src / 'capture-01.status.json').read_text())
    if status.get('exit') != 0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256'] != sha(src / 'capture.py') or not (src / 'capture-01.stdout').read_bytes() or (src / 'capture-01.stderr').read_bytes():
        raise RuntimeError('required capture failed/incomplete')
    v = json.loads((src / 'source-01.json').read_text())
    if v.get('wrapper_complete') is not True or v['wrapper_sha256'] != sha(src / 'capture.py') or v['exe_sha256'] != '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':
        raise RuntimeError('capture identity/wrapper incomplete')
    roles = load('sd194_original_roles', TOOLS / 'validate-title-source-annotations.py')
    qualification = roles.validate(v)
    graph_helper = TOOLS / 'prove_owner_reload_order.py'
    if sha(graph_helper) != '43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':
        raise RuntimeError('reviewed graph helper changed')
    G = load('sd194_original_graph', graph_helper)
    required = [('0x377dc0', '0x37802a', '4ed6ee23865ccd80ca5907d4678998ea8d5ee1b8664bad0bfca8d911400d8c51'),
                ('0x2df880', '0x2df8d9', 'f71f6f4a0633fa327a47b23f16231e23be086270b133f30357e49520d74f9800'),
                ('0x861eba', '0x861ec0', '6965fae1bfbb53fa3e4494d863d249e4891b57d30473263173fea2f844ab6b03')]
    if len(v['ranges']) != 3: raise RuntimeError('required source population incomplete')
    for r, pin in zip(v['ranges'], required):
        raw = bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))
        if (r['start'], r['end_exclusive'], r['sha256']) != pin or len(raw) != int(r['end_exclusive'], 16)-int(r['start'], 16) or hashlib.sha256(raw).hexdigest() != pin[2]:
            raise RuntimeError('original full body identity changed/incomplete')
    ix = {int(i['pc'], 16): i for r in v['ranges'] for i in r['instructions']}
    ops = [(0x377dc0,'mov','r11, rsp'),(0x377dc8,'lea','rbp, [r11 - 0x1a8]'),(0x377dcf,'sub','rsp, 0x290'),
      (0x377dff,'lea','r8, [rbp + 0x60]'),(0x377e03,'mov','r9d, 0x103'),(0x377e09,'call','0x2df880'),
      (0x377e0e,'xor','r15d, r15d'),(0x377e11,'mov','edx, r15d'),
      (0x377e20,'movzx','eax, byte ptr [rbp + rdx + 0x60]'),(0x377e25,'mov','byte ptr [rsp + rdx + 0x50], al'),
      (0x377e29,'inc','rdx'),(0x377e2c,'test','al, al'),(0x377e2e,'jne','0x377e20'),
      (0x377e30,'lea','rcx, [rbp + 0x60]'),(0x377e34,'or','rax, 0xffffffffffffffff'),
      (0x377e40,'inc','rax'),(0x377e43,'cmp','byte ptr [rcx + rax], r15b'),(0x377e47,'jne','0x377e40'),
      (0x377e49,'lea','r8d, [rax - 1]'),(0x377e55,'movsxd','rcx, r8d'),(0x377e58,'mov','edi, r15d'),
      (0x377e5b,'test','r8d, r8d'),(0x377e5e,'js','0x377ef3'),(0x377e64,'movzx','edx, byte ptr [rbp + rcx + 0x60]'),
      (0x377e69,'cmp','dl, 0x5c'),(0x377e6c,'je','0x377e7e'),(0x377e6e,'cmp','dl, 0x2f'),(0x377e71,'je','0x377e7e'),
      (0x377e73,'dec','r8d'),(0x377e76,'sub','rcx, 1'),(0x377e7a,'jns','0x377e64'),(0x377e7c,'jmp','0x377ef3'),
      (0x377e7e,'mov','edi, eax'),(0x377e80,'sub','edi, r8d'),(0x377e83,'sub','edi, 5'),
      (0x377e86,'test','edi, edi'),(0x377e88,'jle','0x377ef3'),(0x377e9c,'add','edi, 0xc'),
      (0x377eae,'lea','eax, [r8 + 1]'),(0x377eb2,'movsxd','rcx, eax'),(0x377eb5,'add','rdx, rcx'),
      (0x377eb8,'movsxd','rbx, edi'),(0x377ebb,'lea','rcx, [rsp + 0x5c]'),(0x377ec6,'mov','r8, rbx'),(0x377ec9,'call','0x861eba'),
      (0x377ece,'inc','edi'),(0x377ed0,'mov','byte ptr [rsp + rbx + 0x50], 0x2e'),
      (0x377ed8,'inc','edi'),(0x377eda,'mov','byte ptr [rsp + rax + 0x50], 0x65'),
      (0x377ee2,'inc','edi'),(0x377ee4,'mov','byte ptr [rsp + rax + 0x50], 0x66'),
      (0x377eec,'inc','edi'),(0x377eee,'mov','byte ptr [rsp + rax + 0x50], 0x62'),
      (0x377ef3,'movsxd','rax, edi'),(0x377efb,'mov','rdi, qword ptr [rsp + 0x280]'),
      (0x377f12,'mov','byte ptr [rsp + rax + 0x50], r15b'),
      (0x377f7a,'lea','rcx, [rsp + 0x50]'),(0x377f82,'call','0x32e7b0'),
      (0x377feb,'lea','rcx, [rsp + 0x50]'),(0x377ff3,'call','0x32e7b0'),(0x378029,'ret',''),
      (0x2df89b,'test','rax, rax'),(0x2df89e,'jne','0x2df8a4'),(0x2df8a0,'or','eax, 0xffffffff'),(0x2df8a3,'ret',''),
      (0x2df8c4,'cmp','rcx, r9'),(0x2df8c7,'jge','0x2df8ce'),(0x2df8d1,'mov','byte ptr [rax + r11], 0'),
      (0x861eba,'jmp','qword ptr [rip + 0x60ba8]')]
    for pc, mnemonic, args in ops:
        if pc not in ix or (ix[pc]['mnemonic'], ix[pc]['args']) != (mnemonic, args):
            raise RuntimeError('operation changed ' + hex(pc))
    if ix[0x377f12]['memory'][0]['role'] != 'w' or ix[0x861eba]['memory'][0]['rip_target'] != '0x8c2a68':
        raise RuntimeError('terminal-store/import role changed')
    if v['static_copy_import'].get('name') != 'memcpy' or v['static_copy_import'].get('dll') != 'VCRUNTIME140.dll':
        raise RuntimeError('declared copy boundary changed')
    whole = G.graph(ix, 0x377dc0, 0x37802a)
    lookup = G.graph(ix, 0x2df880, 0x2df8d9)
    null = G.graph(ix, 0x2df880, 0x2df8d9, fixed={0x2df89e: False})
    if whole['returns'] != [0x378029] or sorted(lookup['returns']) != [0x2df8a3, 0x2df8d8] or null['returns'] != [0x2df8a3] or any(m['role'] in ('w','rw') for pc in null['visited'] for m in ix[pc]['memory']):
        raise RuntimeError('closed lookup/body or null-write boundary changed')
    no_sep = G.graph(ix, 0x377dc0, 0x37802a, fixed={0x377e6c: False, 0x377e71: False})
    short = G.graph(ix, 0x377dc0, 0x37802a, fixed={0x377e5e: False, 0x377e6c: True, 0x377e88: True})
    if any(target == '0x861eba' for g in (no_sep, short) for pc, target in g['calls']):
        raise RuntimeError('nonpositive/no-separator copy boundary unexpectedly reached')
    if not G.dominates(whole,0x377e09,0x377f12) or not G.dominates(whole,0x377ef3,0x377f12):
        raise RuntimeError('lookup/index store order changed')
    rax_gap = [ix[p] for p in whole['visited'] if 0x377ef3 < p < 0x377f12]
    if any(i['args'].split(',')[0].strip() in ('rax','eax','ax','al','ah') and i['mnemonic'] not in ('cmp','test') for i in rax_gap):
        raise RuntimeError('signed store index clobbered after capture')
    counts = {'no_separator_empty':0,'negative_terminator_raw_copy':0,'zero_terminator_empty':0,'positive_copy_boundary':0}
    negative_offsets = {k:0 for k in range(-4,0)}
    overlaps = []
    trace = hashlib.sha256()
    for n in range(260):
        if not n+1 < 0x110: raise RuntimeError('copy/source disjoint premise failed')
        for j in range(-1,n):
            k = n-j-5 if j >= 0 else 0
            if j == -1:
                category='no_separator_empty';terminal=0;copy=None
            elif k < 0:
                category='negative_terminator_raw_copy';terminal=k;copy=None;negative_offsets[k]+=1
            elif k == 0:
                category='zero_terminator_empty';terminal=0;copy=None
            else:
                category='positive_copy_boundary';terminal=k+16
                copy={'destination_relative_output':12,'source_relative_output':0x110+j+1,'count':k+12,
                      'last_source_relative_input':n+7,'last_destination_relative_output':k+23}
                if copy['last_destination_relative_output'] >= copy['source_relative_output']:
                    overlaps.append({'n':n,'last_separator':j,'stem_length':k,**copy})
            counts[category]+=1
            trace.update(json.dumps([n,j,k,category,terminal,copy],sort_keys=True,separators=(',',':')).encode()+b'\n')
            if not -4 <= terminal <= 270: raise RuntimeError('store-offset bound disproved')
    if sum(counts.values()) != 33930 or len(overlaps) != 9 or any(counts[k] == 0 for k in counts):
        raise RuntimeError('nonempty finite-domain proof incomplete')
    result={'method':'A STATIC_ONLY disassembly + branch/interval proof; no original/native/game execution',
      'producer_complete':True,'driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(src/'source-01.json')}],
      'upstream_status_sha256':sha(src/'capture-01.status.json'),'annotation_prerequisite':qualification,
      'body_pins':required,'operation_assertions':len(ops),'graphs':[{'entry':hex(g['entry']),'visited':len(g['visited']),'returns':[hex(x) for x in g['returns']]} for g in (whole,lookup,null,no_sep,short)],
      'premise':'First NUL at n0..259; valid stack and normal ABI/noninterference; no claim failed lookup initializes that state.',
      'frame':{'input_relative_entry_rsp':-0x148,'output_relative_entry_rsp':-0x258,'input_minus_output':0x110},
      'finite_classification':{'n':[0,259],'last_separator':[-1,'n-1'],'classes':counts,'negative_offsets':negative_offsets,'partitions':33930,'digest_sha256':trace.hexdigest(),
        'no_separator':'EDI remains0, output[0]=NUL', 'short_basename':'k=n-j-5; k<0 terminator at output+k, copied C string retained; k0 output cleared',
        'positive_stem':'Declared memcpy RCX=output+12,RDX=input+j+1,R8=k+12; normal ABI suffix at output+k+12..15 and NUL+k+16'},
      'hypothetical_copy_overlap_states':overlaps,'static_copy_import':v['static_copy_import'],
      'affected_claims':['SD194 stack-dependent request wording','FieldEffects source-name builder short/absent separator preconditions','OPUS stack/ABI/copy count and negative store offsets'],
      'limitations':['No actual inherited stack contents or natural missing-name field reachability.','No loaded memcpy implementation, copy effects, allocation/scheduling/request acceptance or game consequence observed.','Nine long/early-separator overlap states are arithmetic countermodels, not shipped names or evidence of native overlap behavior.','Negative offset is outside copied output but inside allocated frame; no crash/stack-frame corruption claim.','No-NUL, length>259, invalid pointers/ABI/interference/Unicode semantics outside admitted proof.']}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'producer_complete':True,'classes':counts,'partitions':33930,'hypothetical_copy_overlap_states':len(overlaps),'operation_assertions':len(ops),'native_or_live_runs':0}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('out',type=Path);parser.add_argument('--src',type=Path,default=P);args=parser.parse_args();main(args.out,args.src)
