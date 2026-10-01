ENTRY,END,SENTINEL=0x4690B0,0x46919D,0x60000200
RECT,CIRCLE,STACK,RSP=0x40000100,0x40000200,0x60001000,0x60001808
bits=lambda f:struct.unpack('<I',struct.pack('<f',f))[0]
to_float=lambda b:struct.unpack('<f',struct.pack('<I',b))[0]
def run(name,x,z,r_bits,mutated=False,rect_bits=(0,0,0x41200000,0x41200000)):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 for page in [ENTRY&~4095,0x40000000,STACK,0x60000000]:u.mem_map(page,4096)
 running=bytearray(code)
 if mutated:running[0x469147-ENTRY]=0x73 # JA -> JAE, explicitly private intervention.
 u.mem_write(ENTRY,bytes(running));rectangle=bytearray(b'\xa5'*32);circle=bytearray(b'\xa5'*24)
 for off,val in zip([0,8,0x10,0x18],rect_bits):struct.pack_into('<I',rectangle,off,val)
 for off,val in [(0,x),(8,z)]:struct.pack_into('<f',circle,off,val)
 struct.pack_into('<I',circle,0x10,r_bits)
 u.mem_write(RECT,bytes(rectangle));u.mem_write(CIRCLE,bytes(circle));stack=bytearray(b'\xa4'*80);struct.pack_into('<Q',stack,0,SENTINEL);u.mem_write(RSP,bytes(stack))
 regs=[(UC_X86_REG_RSP,RSP),(UC_X86_REG_RCX,RECT),(UC_X86_REG_RDX,CIRCLE),(UC_X86_REG_RAX,0xA5A5A5A5A5A5A5A5),(UC_X86_REG_EFLAGS,2),(UC_X86_REG_MXCSR,0x1F80)]
 for r,v in regs:u.reg_write(r,v)
 for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5]:u.reg_write(r,0xA5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5)
 initial=dict(rcx=hex(RECT),rdx=hex(CIRCLE),rsp=hex(RSP),sentinel=hex(SENTINEL),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),rax=hex(u.reg_read(UC_X86_REG_RAX)),rectangle=bytes(u.mem_read(RECT,32)).hex(),circle=bytes(u.mem_read(CIRCLE,24)).hex(),stack=bytes(u.mem_read(RSP,80)).hex(),xmm0_5=[hex(u.reg_read(r)) for r in [UC_X86_REG_XMM0,UC_X86_REG_XMM1,UC_X86_REG_XMM2,UC_X86_REG_XMM3,UC_X86_REG_XMM4,UC_X86_REG_XMM5]])
 visits=[];reads=[];writes=[];comparisons=[];branch_flags=[]
 compare_regs={'xmm0':UC_X86_REG_XMM0,'xmm1':UC_X86_REG_XMM1,'xmm2':UC_X86_REG_XMM2,'xmm3':UC_X86_REG_XMM3,'xmm4':UC_X86_REG_XMM4,'xmm5':UC_X86_REG_XMM5}
 def oncode(uc,pc,size,_):
  assert pc in by_pc and size==by_pc[pc].size,('Unexpected execution',hex(pc),size)
  visits.append(hex(pc));i=by_pc[pc]
  if i.mnemonic in ['jb','ja','jae','seta']:branch_flags.append(dict(pc=hex(pc),eflags=hex(uc.reg_read(UC_X86_REG_EFLAGS))))
  if i.mnemonic=='comiss':
   operands=[]
   for o in i.operands:
    if o.type==capstone.CS_OP_REG:operands.append(f'{uc.reg_read(compare_regs[i.reg_name(o.reg)])&0xFFFFFFFF:08x}')
    else:
     base=RECT if i.reg_name(o.mem.base)=='rcx' else CIRCLE if i.reg_name(o.mem.base)=='rdx' else None;assert base is not None
     operands.append(bytes(uc.mem_read(base+o.mem.disp,4)).hex())
   comparisons.append(dict(pc=hex(pc),args=i.op_str,operands=operands,eflags_before=hex(uc.reg_read(UC_X86_REG_EFLAGS))))
 def onread(uc,typ,a,size,value,_):
  assert (RECT<=a and a+size<=RECT+32) or (CIRCLE<=a and a+size<=CIRCLE+24) or (a==RSP and size==8),('Unexpected read',hex(a),size)
  reads.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=size,bytes=bytes(uc.mem_read(a,size)).hex()))
 def onwrite(uc,typ,a,size,value,_):writes.append(dict(pc=hex(uc.reg_read(UC_X86_REG_RIP)),address=hex(a),size=size,value=value));raise AssertionError('Predicate unexpectedly wrote memory')
 u.hook_add(unicorn.UC_HOOK_CODE,oncode);u.hook_add(unicorn.UC_HOOK_MEM_READ,onread);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,onwrite)
 failure=None
 try:u.emu_start(ENTRY,SENTINEL,count=128)
 except Exception as error:failure=repr(error)
 after=dict(stop_pc=hex(u.reg_read(UC_X86_REG_RIP)),rsp=hex(u.reg_read(UC_X86_REG_RSP)),rax=hex(u.reg_read(UC_X86_REG_RAX)),eax=u.reg_read(UC_X86_REG_EAX),mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)),eflags=hex(u.reg_read(UC_X86_REG_EFLAGS)),rectangle=bytes(u.mem_read(RECT,32)).hex(),circle=bytes(u.mem_read(CIRCLE,24)).hex(),stack=bytes(u.mem_read(RSP,80)).hex())
 return dict(name=name,method='B full original237B leaf in isolated disposable guest' if not mutated else 'B private JA->JAE detector intervention, not shipping code',mutated=mutated,x_bits=f'{bits(x):08x}',z_bits=f'{bits(z):08x}',radius_bits=f'{r_bits:08x}',running_hex=bytes(running).hex(),running_sha256=sha(running),initial=initial,visits=visits,reads=reads,writes=writes,comparisons=comparisons,after=after,failure=failure,branch_flags=branch_flags)
