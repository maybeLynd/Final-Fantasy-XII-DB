"""Bounded source reducer. Conditional values are NOT FF12 execution."""
import capstone
def decode(code,a):
 c=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);c.detail=True
 ii={i.address:i for i in c.disasm(code,a)};assert sum(i.size for i in ii.values())==len(code);return ii
def target(i,j):
 o=i.operands[j];assert o.type==capstone.CS_OP_MEM and i.reg_name(o.mem.base)=='rip';return i.address+i.size+o.mem.disp
def facts(code):
 ii=decode(code,0x392740)
 assert ii[0x392777].mnemonic=='mov' and target(ii[0x392777],0)==0x2AEE0BC
 assert ii[0x392761].op_str=='esi, esi' and ii[0x392777].reg_name(ii[0x392777].operands[1].reg)=='esi'
 assert ii[0x39275A].mnemonic=='mov' and target(ii[0x39275A],1)==0x2AEE0A0
 assert ii[0x39277D].op_str=='rcx, rcx' and ii[0x392780].mnemonic=='je' and ii[0x392780].operands[0].imm==0x3929E8
 assert ii[0x3927E0].mnemonic=='lea' and target(ii[0x3927E0],1)==0x2AEE0C0
 assert ii[0x3927E7].op_str=='r8d, 0x400' and ii[0x3927ED].operands[0].imm==0x861EC0
 assert ii[0x3927FF].mnemonic=='mov' and ii[0x3927FF].reg_name(ii[0x3927FF].operands[0].reg)=='ebp'
 limit=ii[0x3927FF].operands[1].imm
 assert target(ii[0x39285E],1)==0x2AEE0BC and ii[0x392865].op_str=='eax, ebp'
 assert ii[0x392867].mnemonic=='jge' and ii[0x392867].operands[0].imm==0x3928BF
 st=ii[0x39286E];o=st.operands[0];assert st.mnemonic=='mov' and o.size==8 and st.reg_name(o.mem.base)=='rsi' and st.reg_name(o.mem.index)=='rax' and o.mem.scale==8
 assert target(ii[0x392839],1)==0x2AEE0C0 and target(ii[0x3928B9],0)==0x2AEE0BC and ii[0x3928B9].mnemonic=='inc'
 assert ii[0x3928AE].reg_name(ii[0x3928AE].operands[0].reg)=='ecx' and target(ii[0x3928AE],1)==0x2AEE0BC
 assert ii[0x3928B4].mnemonic=='call' and ii[0x3928B4].operands[0].imm==0x392200
 assert ii[0x392904].op_str=='edx, 0x20' and ii[0x392909].op_str=='dword ptr [rax + 0x24], edx'
 assert ii[0x39290C].mnemonic=='cmovb' and ii[0x39290C].op_str=='edx, dword ptr [rax + 0x24]'
 assert ii[0x392917].op_str=='ebx, ebp' and ii[0x392955].op_str=='ecx, ebx'
 assert ii[0x392957].operands[0].imm==0x392200 and ii[0x39295C].op_str=='ebx'
 assert ii[0x392962].op_str=='r14, 1' and ii[0x392966].mnemonic=='jne' and ii[0x392966].operands[0].imm==0x392920
 assert ii[0x392968].mnemonic=='call' and ii[0x392968].operands[0].imm==0x32A6B0
 assert ii[0x39298D].op_str=='eax, ebp' and ii[0x39298F].mnemonic=='jge' and ii[0x39298F].operands[0].imm==0x392998
 second=ii[0x392991].mnemonic=='call'
 if second:assert ii[0x392991].operands[0].imm==0x32A6B0
 else:assert [ii[a].mnemonic for a in range(0x392991,0x392996)]==['nop']*5
 assert ii[0x392996].op_str=='ebp, eax' and ii[0x392998].op_str=='ebp, ebp'
 assert ii[0x39299A].mnemonic=='jle' and ii[0x39299A].operands[0].imm==0x3929E0
 assert ii[0x3929BD].op_str=='ecx, [rsi + 0xa0]' and ii[0x3929D5].operands[0].imm==0x392200
 assert ii[0x3929DA].op_str=='esi' and ii[0x3929DC].op_str=='esi, ebp' and ii[0x3929DE].mnemonic=='jl' and ii[0x3929DE].operands[0].imm==0x3929A0
 return dict(pointer_count_cell='0x2aee0bc',heap_cell='0x2aee0a0',pointer_head='0x2aee0c0',pointer_clear_bytes=0x400,pointer_limit=limit,authored_base=limit,authored_unsigned_min_limit=0x20,registry_base=0xA0,first_getter='0x392968',conditional_second_getter=second,second_getter_site='0x392991',second_result_use='0x392996',guard_signed=True)
def conditional_tail(f,first,second):
 assert -(1<<31)<=first<(1<<31) and -(1<<31)<=second<(1<<31)
 use_second=first<f['pointer_limit'] and f['conditional_second_getter']
 bound=f['pointer_limit'] if first>=f['pointer_limit'] else (second if use_second else first)
 n=max(0,bound)
 return dict(first=first,second=second,second_getter_taken=use_second,positive_loop_bound=n,first_id=f['registry_base'] if n else None,last_id=f['registry_base']+n-1 if n else None)
