"""Bound the actual native math destinations, keeping imported effects explicit."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import capstone
from capstone.x86_const import X86_OP_MEM
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
    if out.exists():raise RuntimeError('immutable result exists')
    status=json.loads((src/'capture-01.status.json').read_text())
    if status.get('exit')!=0 or status.get('terminal') is not True or status.get('exception') is not None or status['driver_sha256']!=sha(src/'capture.py') or not(src/'capture-01.stdout').read_bytes() or(src/'capture-01.stderr').read_bytes():raise RuntimeError('upstream capture failed/incomplete')
    v=json.loads((src/'source-01.json').read_text())
    if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/'capture.py'):raise RuntimeError('capture wrapper incomplete/mixed')
    V=load('math_roles_validator',T/'validate-title-source-annotations.py');roles=V.validate(v)
    G=load('math_local_cfg',T/'prove_owner_reload_order.py')
    if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph identity changed')
    parents={'matrix-buffer-alias':'f4f460958fbc47c7c1d841663afad3011601df5ceb0ce54f8ef25f94d6c97fc0','s33-history-counter-bounds':'eccff61b054257998fe40886c59f76c8cb70b55152a568b78c586c03a2b07be1'}
    retained={}
    for name,pin in parents.items():
        m=src/'retained'/(name+'-manifest.json')
        if sha(m)!=pin:raise RuntimeError('retained parent identity failed')
        members={m['path']:m for m in json.loads(m.read_text())['members']}
        for p in (src/'retained').glob(name+'-*'):
            if p==m:continue
            local=p.name[len(name)+1:];member=members[local]
            if sha(p)!=member['sha256'] or p.stat().st_size!=member['bytes']:raise RuntimeError('retained member identity failed')
            if p.suffix=='.json':retained[name+'/'+local]=json.loads(p.read_text())
    # Reuse exact legacy matrix bytes; re-annotate with the actual reviewed policy.
    old=retained['matrix-buffer-alias/source.json']
    if old['exe_sha256']!=v['exe_sha256'] or old['image_base']!=v['image_base']:raise RuntimeError('mixed retained image')
    spec=importlib.util.spec_from_file_location('math_reviewed_adapter',V.ADAPTER);adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    derived={'method':'A retained original matrix bytes re-annotated; no new source capture/native execution','exe_sha256':v['exe_sha256'],'image_base':v['image_base'],'adapter_sha256':v['adapter_sha256'],'capstone':capstone.__version__,'ranges':[]}
    for b in old['bodies']:
        lo=int(b['entry'],16);raw=bytes.fromhex(b['raw_hex'])
        if hashlib.sha256(raw).hexdigest()!=b['sha256'] or len(raw)!=b['size']:raise RuntimeError('legacy body mismatch')
        ins=[]
        for i in cs.disasm(raw,lo):
            memory=[]
            for index,operand in enumerate(i.operands):
                if operand.type==X86_OP_MEM:
                    m=operand.mem;base=i.reg_name(m.base)
                    memory.append({'base':base,'index':i.reg_name(m.index),'scale':m.scale,'displacement':m.disp,'size':operand.size,'role':adapter.op_kind(i,operand,index),'rip_target':hex(i.address+i.size+m.disp) if base=='rip' else None})
            ins.append({'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'memory':memory})
        if sum(len(bytes.fromhex(i['bytes'])) for i in ins)!=len(raw):raise RuntimeError('legacy decode incomplete')
        derived['ranges'].append({'start':hex(lo),'end_exclusive':hex(lo+len(raw)),'sha256':b['sha256'],'instructions':ins})
    if {b['start'] for b in derived['ranges']}!={'0x217060','0x202b70'}:raise RuntimeError('retained matrix population changed')
    legacy_roles=V.validate(derived)
    history=retained['s33-history-counter-bounds/source-01.json'];history_roles=V.validate(history)
    hresult=retained['s33-history-counter-bounds/result-01.json']
    if hresult.get('producer_complete') is not True or hresult['normal_counter_domain']!=[0,6]:raise RuntimeError('history prerequisite incomplete')
    hstatus=retained['s33-history-counter-bounds/proof-01.status.json']
    hdriver=src/'retained/s33-history-counter-bounds-prove.py'
    if hstatus.get('exit')!=0 or hstatus.get('terminal') is not True or hstatus.get('exception') is not None or hstatus['driver_sha256']!=sha(hdriver) or hresult['driver_sha256']!=sha(hdriver) or not(src/'retained/s33-history-counter-bounds-proof-01.stdout').read_bytes() or(src/'retained/s33-history-counter-bounds-proof-01.stderr').read_bytes():raise RuntimeError('required history proof failed/incomplete')
    # Destination aliases established by the original prologues and unchanged on
    # normal call paths; imported math/cookie side effects remain a stated premise.
    receiver={0x202b10:'rcx',0x202de0:'rbx',0x203080:'rcx',0x270720:'rdi',0x203170:'rcx',0x270a10:None,0x270cf0:'rdi',0x270b40:'rdi',0x216660:'rbx',0x202e90:'rcx',0x202f00:'rcx',0x217790:'rcx',0x217880:'rcx',0x217060:'rcx',0x202b70:'rbx'}
    bounds={lo:64 if lo in [0x270720,0x203170,0x202e90,0x202f00,0x217790,0x217880] else 16 for lo in receiver}
    graphs=[];write_sets=[];ix={}
    external={'0x861f02','0x861f08','0x861f0e','0x861f14','0x861f56','0x808c40','qword ptr [rip + 0x6ac5c7]','qword ptr [rip + 0x6ac5c2]'}
    native={hex(a) for a in receiver}|{'0x202c90'}
    for b in v['ranges']+derived['ranges']:
        lo=int(b['start'],16);hi=int(b['end_exclusive'],16)
        if lo not in receiver:raise RuntimeError('unplanned helper')
        local={int(i['pc'],16):i for i in b['instructions']};ix.update(local)
        tail={0x202e90:'0x217790',0x202f00:'0x217880'}.get(lo);g=G.graph(local,lo,hi,tail=tail)
        if any(target not in external|native for pc,target in g['calls']):raise RuntimeError('unclosed new callee')
        graphs.append({'entry':hex(lo),'visited':len(g['visited']),'returns':[hex(x) for x in g['returns']],'tails':[{'pc':hex(x),'target':tail} for x in g['tails']],'calls':[{'pc':hex(pc),'target':target} for pc,target in g['calls']]})
        stores=[]
        for i in b['instructions']:
            if int(i['pc'],16) not in g['visited']:continue
            for m in i['memory']:
                if m['role'] not in ['w','rw']:continue
                if m['base'] in ['rsp','rbp']:continue
                if lo==0x270a10 and m['base']=='rax' and m['displacement'] in [-0x18,-0x28,-0x38] and m['size']==16 and not m['index']:continue
                # normalize/copy wrappers write entry RCX before saving/reusing it.
                allowed={receiver[lo]}|({'rcx'} if lo==0x202de0 else set())|({'rbx'} if lo in [0x202e90,0x202f00] else set())
                if m['base'] not in allowed or m['displacement']<0:raise RuntimeError('unproved store receiver')
                if m['index']:
                    if lo!=0x270b40 or m['index'] not in ['r15','rsi','r14'] or m['scale']!=4 or m['size']!=4 or m['displacement']!=0:raise RuntimeError('unproved store index')
                    end=12
                else:end=m['displacement']+m['size']
                if end>bounds[lo]:raise RuntimeError('store exceeds output')
                stores.append({'pc':i['pc'],'memory':m,'bounded_end':end})
        write_sets.append({'entry':hex(lo),'output_bound':bounds[lo],'direct_output_stores':stores})
    if len(graphs)!=15 or sum(len(w['direct_output_stores']) for w in write_sets)==0:raise RuntimeError('missing/zero helper population')
    pins=[(0x202de9,'mov','rbx, rcx'),(0x27072d,'mov','rdi, rcx'),(0x270a10,'mov','rax, rsp'),(0x270d27,'mov','rdi, rcx'),(0x270b67,'mov','rdi, rcx'),(0x21666b,'mov','rbx, rcx'),(0x202b76,'mov','rbx, rcx'),(0x270be3,'xor','edx, edx'),(0x270bed,'mov','eax, 1'),(0x270bfc,'cmova','edx, eax'),(0x270bff,'mov','eax, 2'),(0x270c0c,'cmova','edx, eax'),(0x270c0f,'lea','rax, [rip + 0x6a4dc2]'),(0x270c16,'mov','r15d, edx'),(0x270c19,'movsxd','rsi, dword ptr [rax + rdx*4]'),(0x270c26,'movsxd','r14, dword ptr [rax + rsi*4]'),(0x202eea,'add','rsp, 0x40'),(0x202eef,'jmp','0x217790'),(0x202f5a,'add','rsp, 0x40'),(0x202f5f,'jmp','0x217880')]
    for pc,m,a in pins:
        if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('receiver/index/tail transfer changed: '+hex(pc))
    caller=next(b for b in history['ranges'] if b['start']=='0x3fc170')
    cix={int(i['pc'],16):i for i in caller['instructions']}
    caller_pins=[(0x3fc1bf,'lea','r14, [rcx + 0x80]'),(0x3fc1e2,'mov','r13, rcx'),(0x3fc284,'lea','rcx, [rsp + 0x60]'),(0x3fc289,'call','0x202b10'),(0x3fc2ff,'lea','rcx, [rbp - 0x70]'),(0x3fc303,'call','0x270720'),(0x3fc311,'lea','rcx, [rbp - 0x80]'),(0x3fc315,'call','0x202b70'),(0x3fc323,'lea','rcx, [rsp + 0x40]'),(0x3fc328,'call','0x203080'),(0x3fc33a,'lea','rcx, [rsp + 0x40]'),(0x3fc33f,'call','0x202de0'),(0x3fc351,'lea','rcx, [rsp + 0x70]'),(0x3fc356,'call','0x270a10'),(0x3fc367,'lea','rcx, [r14 - 0x70]'),(0x3fc36b,'call','0x270cf0'),(0x3fc378,'lea','rcx, [r14 - 0x80]'),(0x3fc37c,'call','0x202b10')]
    for pc,m,a in caller_pins:
        if(cix[pc]['mnemonic'],cix[pc]['args'])!=(m,a):raise RuntimeError('caller destination changed: '+hex(pc))
    # Verify the only table-indexed destination selector from the actual image.
    raw=(G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=v['exe_sha256']:raise RuntimeError('table reference identity failed')
    pe=struct.unpack_from('<I',raw,0x3c)[0];count=struct.unpack_from('<H',raw,pe+6)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
    sections=[struct.unpack_from('<IIII',raw,pe+24+opt+k*40+8) for k in range(count)]
    def at(a,n):
        for vs,va,rs,ro in sections:
            if 0x120000+va<=a and a+n<=0x120000+va+rs:return raw[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise RuntimeError('unbacked bounded table')
    expected_sizes={0x202b10:81,0x202de0:33,0x203080:81,0x270720:340,0x203170:44,0x270a10:295,0x270cf0:597,0x270b40:420,0x216660:186,0x202e90:100,0x202f00:100,0x217790:236,0x217880:234,0x217060:235,0x202b70:31}
    for body in v['ranges']+derived['ranges']+[caller]:
        lo=int(body['start'],16);n=int(body['end_exclusive'],16)-lo;blob=bytes.fromhex(''.join(i['bytes'] for i in body['instructions']))
        if n!=(626 if lo==0x3fc170 else expected_sizes[lo]) or blob!=at(lo,n):raise RuntimeError('source differs from exact original body')
    table=at(0x9159d8,12);cycle=list(struct.unpack('<iii',table))
    if cycle!=[1,2,0]:raise RuntimeError('quaternion index cycle changed')
    indices=[{'selected':n,'r15':n,'rsi':cycle[n],'r14':cycle[cycle[n]]} for n in range(3)]
    if any(sorted([c['r15'],c['rsi'],c['r14']])!=[0,1,2] for c in indices):raise RuntimeError('index bound failed')
    derived_path=out.with_name('retained-matrix-reannotation-01.json')
    if derived_path.exists():raise RuntimeError('immutable reannotation exists')
    derived_path.write_text(json.dumps(derived,indent=2)+'\n')
    result={'producer_complete':True,'method':'A STATIC_ONLY native output-footprint composition','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':'source-01.json','sha256':sha(src/'source-01.json')},{'path':derived_path.name,'sha256':sha(derived_path)},{'path':'retained/s33-history-counter-bounds-source-01.json','sha256':sha(src/'retained/s33-history-counter-bounds-source-01.json')}],'parent_manifests':parents,'annotation_prerequisites':[roles,legacy_roles,history_roles],'graphs':graphs,'writes':write_sets,'transfer_assertions':len(pins)+len(caller_pins),'index_table':{'address':'0x9159d8','bytes':table.hex(),'values':cycle,'finite_index_cases':indices},
      'native_effects':'Vector/copy/quaternion outputs within16B; matrix identity/rotation/conversion within64B. Normalize216660 includes16B zero fallback. Two rotation wrappers compose64B tail effects217790/217880. 270A10 produces16B through270B40 and uses private64B matrix scratch. Imported math/cookie effects excluded under named normal contracts.',
      'caller_composition':'3FC170 uses output record destinations only H+0 (202B10,16B), H+10 (270CF0,16B), and prior verified copy/counter sites. Other vector/quaternion/matrix outputs use valid private stack. With initialized0..6 counters, ordinarynonvolatileABI, record/frames nonaliasing and no outside/foreign record writes, composed recordwrites endatvisual254 and do nottouchphase260/flags272/links278/280. No pixel/scheduling/elapsedframe guarantee.',
      'limits':['Normal imported atan2f/cosf/sinf/sqrtf/acosf/_isnan/_finite and cookie boundaries are not executed or proven as loaded-module effects here. Declare their no-record-write/ABI/return contract; this is not a stub proving native effects.','Whole manager release across another invocation still requires valid finite list, normal updater effects, no outside interference, identity/lifetime and actual scheduling; these are not established by this footprint.','Output bounds establish memory regions, not bit-exact numeric outputs, arbitrary matrix/vector overlap safety, FP exception behavior or presentation.','Parent source/counter proofs are independently pending; integrity alone doesnotaccept theirsemantics. Matrixalias source facts reused with sharedadapter reannotation; prior samples/reviewer runs notrepeated/credited.'],
      'consumer':'OPUS can refine math/caller effects after scoped independent review and declared library/stack premises, closing explicit native output-width gap. FABLE preserve initialized/scheduling/presentation gaps and correct transformhistory terminology. No wholeS33/runtime-row closure.'}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'closed_native_bodies':len(graphs),'tail_compositions':2,'object_store_sites':sum(len(w['direct_output_stores']) for w in write_sets),'transfer_assertions':len(pins)+len(caller_pins),'native_runs':0,'game_runs':0}))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output)
