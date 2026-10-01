#!/usr/bin/env python3
"""Bounded, conservative fixed-offset provenance check for SECTION-04.

Requires Capstone 5.0.9. NOT a replacement for missing Tools/hop_scan.py or a
whole-game alias analysis. Caller-supplied entry identities and explicit switch
successors are evidence assumptions, pinned/checked by run_review.py. Unknown
joins, overwritten register aliases and pointee loads discard provenance.
"""
from __future__ import annotations
from collections import deque
from typing import Any
import capstone as cs
from capstone import x86 as x
REGS=('rax','rbx','rcx','rdx','rsi','rdi','rbp','rsp',*(f'r{i}' for i in range(8,16)))
VOLATILE=('rax','rcx','rdx','r8','r9','r10','r11')
Value=tuple[str,int]|None

def canonical(name:str)->str|None:
    if name in REGS:return name
    for root,aliases in {'rax':('eax','ax','al','ah'),'rbx':('ebx','bx','bl','bh'),
      'rcx':('ecx','cx','cl','ch'),'rdx':('edx','dx','dl','dh'),
      'rsi':('esi','si','sil'),'rdi':('edi','di','dil'),'rbp':('ebp','bp','bpl'),
      'rsp':('esp','sp','spl')}.items():
        if name in aliases:return root
    for i in range(8,16):
        if name in (f'r{i}d',f'r{i}w',f'r{i}b'):return f'r{i}'
    return None

def analyze(raw:bytes,entry:int,seeds:dict[str,Value],globals_:dict[int,str]|None=None,
            switches:dict[int,list[int]]|None=None,mutant:str='')->dict[str,Any]:
    decoder=cs.Cs(cs.CS_ARCH_X86,cs.CS_MODE_64);decoder.detail=True
    instructions=list(decoder.disasm(raw,entry));by={i.address:i for i in instructions}
    if not instructions or sum(i.size for i in instructions)!=len(raw):
        raise ValueError('incomplete instruction decode')
    globals_=globals_ or {};switches=switches or {};limit=entry+len(raw)
    for site,targets in switches.items():
        if site not in by or any(t not in by for t in targets):raise ValueError('switch target outside selected body or not an instruction')
    initial={r:None for r in REGS};initial.update(seeds)
    states={entry:initial};queue=deque([entry]);iterations=0
    def reg(i:Any,o:Any,st:dict[str,Value])->Value:
        key=canonical(i.reg_name(o.reg));v=st.get(key)
        if v is not None and o.size!=8:
            return ('const',v[1]&((1<<(8*o.size))-1)) if v[0]=='const' else None
        return v
    def addr(i:Any,o:Any,st:dict[str,Value])->Value:
        m=o.mem
        if m.segment not in (0,x.X86_REG_DS,x.X86_REG_SS):return None
        if m.base==x.X86_REG_RIP:return ('const',i.address+i.size+m.disp)
        base=st.get(canonical(i.reg_name(m.base))) if m.base else ('const',0)
        if base is None:return None
        if m.index:
            index=st.get(canonical(i.reg_name(m.index)))
            if index is None or index[0]!='const':return None
            return (base[0],base[1]+index[1]*m.scale+m.disp)
        return (base[0],base[1]+m.disp)
    def value(i:Any,o:Any,st:dict[str,Value])->Value:
        if o.type==cs.CS_OP_IMM:return ('const',o.imm)
        if o.type==cs.CS_OP_REG:return reg(i,o,st)
        if o.type==cs.CS_OP_MEM:
            a=addr(i,o,st)
            if o.size==8 and a and a[0]=='const' and a[1] in globals_:return (globals_[a[1]],0)
        return None
    def write(st:dict[str,Value],i:Any,o:Any,v:Value)->None:
        key=canonical(i.reg_name(o.reg))
        if key is None:return
        if o.size<4:
            if mutant!='ignore_partial_write':st[key]=None
            return
        if o.size==4:
            st[key]=('const',v[1]&0xffffffff) if v and v[0]=='const' else None
        else:st[key]=v
    def step(i:Any,st:dict[str,Value])->dict[str,Value]:
        out=dict(st);ops=i.operands;m=i.mnemonic
        # Invalidate all explicitly/implicitly written GPR aliases, including partial ones.
        for r in i.regs_access()[1]:
            key=canonical(i.reg_name(r))
            if key and not (mutant=='ignore_partial_write' and any(o.type==cs.CS_OP_REG and canonical(i.reg_name(o.reg))==key and o.size<4 for o in ops)):
                out[key]=None
        if i.group(cs.CS_GRP_CALL):
            if mutant!='keep_volatile':
                for r in VOLATILE:out[r]=None
            else:
                for r in VOLATILE:out[r]=st[r]
            out['rsp']=st['rsp'];return out
        if len(ops)>1 and ops[0].type==cs.CS_OP_REG:
            d=ops[0];key=canonical(i.reg_name(d.reg))
            if m in ('mov','movabs'):write(out,i,d,value(i,ops[1],st))
            elif m=='lea':write(out,i,d,addr(i,ops[1],st))
            elif m in ('xor','sub') and ops[1].type==cs.CS_OP_REG and canonical(i.reg_name(ops[1].reg))==key:
                write(out,i,d,('const',0))
                if mutant=='xor_keeps_pointer' and m=='xor':out[key]=st.get(key)
            elif m in ('add','sub','and','or'):
                a=reg(i,d,st);b=value(i,ops[1],st);v=None
                if a and b and b[0]=='const':
                    if m in ('add','sub'):v=(a[0],a[1]+(b[1] if m=='add' else -b[1]))
                    elif a[0]=='const':v=('const',a[1]&b[1] if m=='and' else a[1]|b[1])
                write(out,i,d,v)
            elif m.startswith('cmov'):
                a=reg(i,d,st);b=value(i,ops[1],st);write(out,i,d,a if a==b else None)
        if m in ('push','pop'):
            sp=st['rsp'];out['rsp']=(sp[0],sp[1]+(-8 if m=='push' else 8)) if sp else None
        return out
    def successors(i:Any)->list[int]:
        if i.group(cs.CS_GRP_RET):return []
        if i.group(cs.CS_GRP_JUMP):
            o=i.operands[0];dest=o.imm if o.type==cs.CS_OP_IMM else None
            if i.mnemonic in ('jmp','ljmp'):
                return [dest] if dest in by else switches.get(i.address,[])
            return [t for t in (dest,i.address+i.size) if t in by]
        return [i.address+i.size] if i.address+i.size<limit else []
    while queue:
        at=queue.popleft();iterations+=1
        if iterations>len(by)*80:raise ValueError('dataflow failed to converge within bounded limit')
        out=step(by[at],states[at])
        for dest in successors(by[at]):
            if dest not in by:raise ValueError('fallthrough is not an instruction boundary')
            if dest not in states:states[dest]=dict(out);queue.append(dest);continue
            old=states[dest];merged={r:(old[r] if old[r]==out[r] else None) for r in REGS}
            if mutant=='join_chooses_pointer':
                for r in REGS:
                    vals=[v for v in (old[r],out[r]) if v and v[0] not in ('const','stack')]
                    if vals:merged[r]=vals[0]
            if merged!=old:states[dest]=merged;queue.append(dest)
    accesses=[];expressions=[]
    for at,st in sorted(states.items()):
        i=by[at]
        for index,o in enumerate(i.operands):
            if o.type!=cs.CS_OP_MEM:continue
            a=addr(i,o,st)
            if i.mnemonic=='lea':
                expressions.append({'site':f'{at:08X}','instruction':i.mnemonic+' '+i.op_str,'value':list(a) if a else None})
                if mutant!='lea_is_memory':continue
            if i.mnemonic.startswith('nop'):continue
            access=o.access
            if i.mnemonic=='lea' and mutant=='lea_is_memory':access=cs.CS_AC_READ
            if a and a[0] not in ('const','stack') and access:
                accesses.append({'site':f'{at:08X}','root':a[0],'offset':a[1],'bytes':o.size,'mode':('R' if access&cs.CS_AC_READ else '')+('W' if access&cs.CS_AC_WRITE else ''),'operand':index,'instruction':i.mnemonic+' '+i.op_str})
    return {'accesses':accesses,'expressions':expressions,'reachable_instructions':len(states),'decoded_instructions':len(by),'iterations':iterations}

def regression(mutant:str='')->list[dict[str,Any]]:
    tests=[]
    def check(name:str,code:str,predicate:Any)->None:
        a=analyze(bytes.fromhex(code),0x1000,{'rcx':('asset',0),'rdx':('message',0),'rsp':('stack',0)},mutant=mutant)
        ok=bool(predicate(a));tests.append({'name':name,'pass':ok})
    roots=lambda a:[(r['root'],r['offset']) for r in a['accesses']]
    check('register_copy_and_flags_preserve_pointer','488bd94885db8b4308c3',lambda a:roots(a)==[('asset',8)])
    check('cmp_preserves_pointer','488bd983f9008b4308c3',lambda a:roots(a)==[('asset',8)])
    check('lea_is_not_a_memory_read','488bd98d5315c3',lambda a:not a['accesses'])
    check('xor32_kills_pointer','488bd933db8b4308c3',lambda a:not a['accesses'])
    check('partial_byte_write_kills_pointer','488bd9b3018b4308c3',lambda a:not a['accesses'])
    check('mov32_kills_pointer','488bd9bb010000008b4308c3',lambda a:not a['accesses'])
    check('call_clobbers_volatile_pointer','488bd1e8f80000008b4208c3',lambda a:not a['accesses'])
    check('call_preserves_nonvolatile_pointer','488bd9e8f80000008b4308c3',lambda a:roots(a)==[('asset',8)])
    check('join_discards_disagreeing_provenance','488bd985c07405bb000000008b4308c3',lambda a:not a['accesses'])
    check('pointee_is_not_parent','488bd9488b83c80000008b4840c3',lambda a:roots(a)==[('asset',0xc8)])
    check('lea_preserves_known_subobject_offset','488bd9488d83c00000008b08c3',lambda a:roots(a)==[('asset',0xc0)])
    check('dynamic_index_is_not_fixed_field','488bd98b040bc3',lambda a:not a['accesses'])
    check('message_receiver_not_conflated','488bda8b4308c3',lambda a:roots(a)==[('message',8)])
    check('constant_lea_folds_without_access','33db8d5315c3',lambda a:not a['accesses'] and a['expressions'][0]['value']==['const',21])
    check('read_modify_write_is_recorded','488bd9838bc000000001c3',lambda a:len(a['accesses'])==1 and a['accesses'][0]['mode']=='RW')
    check('store_is_not_a_read','488bd98983c0000000c3',lambda a:len(a['accesses'])==1 and a['accesses'][0]['mode']=='W')
    return tests

if __name__=='__main__':
    import json
    print(json.dumps(regression(),indent=2))
