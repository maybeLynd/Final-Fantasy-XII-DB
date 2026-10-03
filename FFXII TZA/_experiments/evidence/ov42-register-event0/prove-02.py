"""Bounded constant-event path proof over retained original handler bytes.

Registers and memory payloads remain symbolic except concrete event and relative
stack bookkeeping. This is static interpretation, not instruction execution.
"""
import argparse,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86_const import X86_OP_REG,X86_OP_IMM,X86_OP_MEM
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ASH='5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def tracer(instructions,event):
    table={i.address:i for i in instructions};pc=instructions[0].address
    registers={'rcx':'view','rdx':event&0xffffffff,'r8':'payload','rsp':0}
    aliases={'eax':'rax','edx':'rdx','ecx':'rcx','esp':'rsp'}
    zf=None;path=[];memory=[]
    def key(ins,reg):
        name=ins.reg_name(reg)
        return aliases.get(name,name[:-1] if name.startswith('r') and name[-1:] in ['d','w','b'] else name)
    def value(ins,op):
        if op.type==X86_OP_IMM:return op.imm
        if op.type==X86_OP_REG:
            k=key(ins,op.reg)
            v=registers.get(k,'unresolved register '+ins.reg_name(op.reg))
            # RSP stores a signed displacement from the entry stack, not a
            # concrete machine address. Masking it destroys balanced SUB/ADD.
            if k=='rsp':
                if op.size!=8:raise ValueError('unsupported partial stack register')
                return v
            return v&((1<<(op.size*8))-1) if isinstance(v,int) else v
        if op.type==X86_OP_MEM:return 'unobserved memory '+ins.op_str
        raise ValueError('unsupported operand')
    for step in range(64):
        if pc not in table:raise ValueError('path outside complete body')
        i=table[pc];path.append(hex(pc));ops=i.operands;name=i.mnemonic;nextpc=pc+i.size
        for index,op in enumerate(ops):
            if op.type==X86_OP_MEM:
                role=ROLES.op_kind(i,op,index)
                memory.append(dict(pc=hex(pc),base=i.reg_name(op.mem.base),displacement=op.mem.disp,size=op.size,role=role))
                if role in ['w','rw'] and i.reg_name(op.mem.base) not in ['rsp','rbp']:
                    return dict(boundary='OBJECT_WRITE',pc=hex(pc),path=path,memory=memory)
        if name=='call':
            if ops[0].type!=X86_OP_IMM:raise ValueError('unresolved call target')
            return dict(boundary='CALL',pc=hex(pc),target=hex(ops[0].imm),path=path,memory=memory)
        if name=='ret':return dict(boundary='RETURN',eax=registers.get('rax'),pre_ret_rsp_delta=registers['rsp'],rdx=registers.get('rdx'),path=path,memory=memory)
        if name in ['mov','movzx']:
            if ops[0].type!=X86_OP_REG:raise ValueError('unhandled memory destination')
            registers[key(i,ops[0].reg)]=value(i,ops[1])
        elif name=='xor' and ops[0].type==X86_OP_REG and ops[1].type==X86_OP_REG and ops[0].reg==ops[1].reg:
            registers[key(i,ops[0].reg)]=0;zf=True
        elif name in ['sub','add','shl']:
            if ops[0].type!=X86_OP_REG:raise ValueError('unhandled arithmetic destination')
            a,b=value(i,ops[0]),value(i,ops[1]);k=key(i,ops[0].reg)
            if isinstance(a,int) and isinstance(b,int):
                v=a-b if name=='sub' else a+b if name=='add' else a<<b
                registers[k]=v if k=='rsp' else v&((1<<(ops[0].size*8))-1)
                zf=None if k=='rsp' else registers[k]==0
            else:registers[k]='unobserved arithmetic';zf=None
        elif name in ['cmp','test']:
            a,b=value(i,ops[0]),value(i,ops[1])
            zf=(a==b if name=='cmp' else (a&b)==0) if isinstance(a,int) and isinstance(b,int) else None
        elif name in ['je','jne']:
            if zf is None:raise ValueError('unknown predicate: no path claim')
            if zf if name=='je' else not zf:nextpc=ops[0].imm
        elif name=='jmp':nextpc=ops[0].imm
        else:raise ValueError('unsupported selected path instruction '+name)
        pc=nextpc
    raise ValueError('bounded path did not finish')

def main(source,out):
    global ROLES
    if out.exists() or (out.parent/('normalized-'+out.stem+'.json')).exists():raise ValueError('existing output: never replace')
    status=json.loads((source/'handler-extents-01.status.json').read_bytes())
    if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None:
        raise ValueError('required physical producer failed or incomplete')
    if status.get('driver_sha256')!=sha(source/'prepare-handler-extents.py') or (source/'handler-extents-01.stderr').read_bytes() or not(source/'handler-extents-01.stdout').read_bytes():
        raise ValueError('physical producer invocation identity/status missing')
    e=json.loads((source/'handler-extents-01.json').read_bytes())
    if e.get('complete') is not True or e.get('exe_sha256')!=PIN or e.get('driver_sha256')!=status['driver_sha256']:
        raise ValueError('physical extent prerequisite incomplete')
    for row in e['lookups']:
        if sha(source/row['path'])!=row['sha256']:raise ValueError('retained lookup changed')
    raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('reference image changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
    sections=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def original(a,n):
        for _,rva,size,off in sections:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
        raise ValueError('unbacked source')
    directory=raw[pe+24+136:pe+24+144]
    if directory.hex()!=e.get('directory_bytes'):raise ValueError('exception directory identity changed')
    rva,n=struct.unpack('<II',directory)
    if not n or n%12:raise ValueError('invalid exception directory')
    pdata=original(0x120000+rva,n)
    runtime_rows=[struct.unpack_from('<III',pdata,k) for k in range(0,n,12)]
    adapter=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
    if sha(adapter)!=ASH:raise ValueError('reviewed adapter changed')
    spec=importlib.util.spec_from_file_location('reviewed_roles',adapter);ROLES=importlib.util.module_from_spec(spec);spec.loader.exec_module(ROLES)
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    controls=[]
    for blob,expected in [('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:
        i=next(cs.disasm(bytes.fromhex(blob),0x1000));o=next((k,op) for k,op in enumerate(i.operands) if op.type==X86_OP_MEM)
        observed=ROLES.op_kind(i,o[1],o[0]);controls.append(dict(bytes=blob,expected=expected,observed=observed))
        if observed!=expected:raise ValueError('actual adapter detection control failed')
    traces=[];bodies={};ranges=[]
    if [b['entry'] for b in e['bodies']]!=['0x29b7d0','0x29b810']:raise ValueError('wrong body identities')
    for b in e['bodies']:
        a,z=int(b['entry'],16),bytes.fromhex(b['physical_bytes'])
        roots=[r for r in runtime_rows if r[0]==a-0x120000]
        records=b.get('records')
        if len(roots)!=1 or len(records or [])!=1:raise ValueError('ambiguous physical body identity')
        root=roots[0];record=records[0];chain=record.get('chain')
        if root[1]+0x120000!=int(b['end_exclusive'],16) or record.get('begin')!=b['entry'] or record.get('end_exclusive')!=b['end_exclusive'] or len(chain or [])!=1:
            raise ValueError('incomplete physical body extent')
        h=original(0x120000+root[2],4)
        if h[0]!=1 or chain[0].get('record_bytes')!=struct.pack('<III',*root).hex() or chain[0].get('header_address')!=hex(0x120000+root[2]) or chain[0].get('header_bytes')!=h.hex():
            raise ValueError('unsupported or altered physical unwind identity')
        if len(z)!=b['bytes'] or hashlib.sha256(z).hexdigest()!=b['sha256'] or original(a,len(z))!=z:raise ValueError('retained original body differs')
        ins=list(cs.disasm(z,a));points={i.address for i in ins}
        if sum(i.size for i in ins)!=len(z) or a+len(z)!=int(b['end_exclusive'],16):raise ValueError('incomplete body decode')
        for i in ins:
            if i.mnemonic.startswith('j') and (i.operands[0].type!=X86_OP_IMM or i.operands[0].imm not in points):raise ValueError('nonclosed branch CFG')
        bodies[a]=ins;trace=tracer(ins,0)
        if trace['boundary']!='RETURN' or trace['eax']!=0 or trace['pre_ret_rsp_delta']!=0:raise ValueError('event0 return contract failed')
        nonstack=[m for m in trace['memory'] if m['base'] not in ['rsp','rbp']]
        if len(nonstack)!=1 or any((m['base'],m['displacement'],m['size'],m['role'])!=('rcx',0x48,8,'r') for m in nonstack):raise ValueError('event0 explicit receiver footprint changed')
        traces.append(dict(entry=hex(a),event=0,**trace))
        records=[]
        for i in ins:
            memory=[]
            for k,op in enumerate(i.operands):
                if op.type==X86_OP_MEM:
                    mm=op.mem;memory.append(dict(base=i.reg_name(mm.base),index=i.reg_name(mm.index),scale=mm.scale,displacement=mm.disp,size=op.size,role=ROLES.op_kind(i,op,k),rip_target=hex(i.address+i.size+mm.disp) if i.reg_name(mm.base)=='rip' else None))
            records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,memory=memory))
        ranges.append(dict(start=b['entry'],end_exclusive=b['end_exclusive'],sha256=b['sha256'],instructions=records))
    call=tracer(bodies[0x29b7d0],1);store=tracer(bodies[0x29b810],2)
    if call.get('boundary')!='CALL' or call.get('target')!='0x2973e0' or store.get('boundary')!='OBJECT_WRITE' or store.get('pc')!='0x29b82c':raise ValueError('real call/store positive control failed')
    # Compose only the exact retained call boundary, not its earlier opaque fill.
    caller=json.loads((source/'source-01.json').read_bytes())
    wanted={0x3f89f4:('mov','qword ptr [rsi + 0x38], rax'),0x3f89fb:('mov','qword ptr [rsi + 0x48], rdi'),0x3f8a04:('mov','r8, rbp'),0x3f8a07:('xor','edx, edx'),0x3f8a09:('mov','rcx, rsi'),0x3f8a0c:('call','rax')}
    witnesses={int(i['pc'],16):i for r in caller['ranges'] for i in r['instructions']}
    for pc,pair in wanted.items():
        i=witnesses.get(pc)
        if not i or (i['mnemonic'],i['args'])!=pair or original(pc,len(bytes.fromhex(i['bytes'])))!=bytes.fromhex(i['bytes']):raise ValueError('registration boundary witness changed')
    normalized=dict(method='A retained physical-byte normalization, not new capture/execution',exe_sha256=PIN,image_base='0x120000',adapter_sha256=ASH,capstone=capstone.__version__,driver_sha256=sha(Path(__file__)),controls=controls,ranges=ranges)
    normalpath=out.parent/('normalized-'+out.stem+'.json');normalpath.write_text(json.dumps(normalized,indent=2)+'\n')
    result=dict(producer_complete=True,question='Can the prescribed registration event0 invoke animation/write object state?',method='A bounded constant-path proof on retained132B original bytes',exe_sha256=PIN,driver_sha256=sha(Path(__file__)),
       inputs=[dict(path=p.relative_to(P).as_posix() if p.is_relative_to(P) else str(p),sha256=sha(p)) for p in sorted(source.iterdir()) if p.is_file()],
       source_pins=[dict(path=normalpath.name,sha256=sha(normalpath)),dict(path='retained/source-01.json',sha256=sha(source/'source-01.json'))],
       paths=traces,positive_controls=dict(event1_call=call,event2_store=store),
       conclusion='Both prescribed event0 paths explicitly read QWORD view+48, do not dereference that context or payload, make no call or explicit nonstack write, and return EAX0 with pre-RET frame restored. Secondary handler leaves EDX=FFFFFFFF; primary leaves event0EDX0.',
       limitations='Valid code/body/entryABI, readableview+48/private40Bstack/returnaddress and noninterference required. Static interpretation, no original execution, no observed register/memory values. Implicit RET stack access is not omitted from validity premises. Only3F89C0 conditional prescribed-handler event0 composition; existing-row callback identity, event1 cost updates/transitive effects/nativefill/lifetime/scheduling/actualreach/presentation remain OPEN.')
    out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED: prescribed event0 context-read-only, EAX0; event1 call/event2 store controls detected')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--src',type=Path,default=P/'retained');a=p.parse_args();main(a.src.resolve(),a.out.resolve())
