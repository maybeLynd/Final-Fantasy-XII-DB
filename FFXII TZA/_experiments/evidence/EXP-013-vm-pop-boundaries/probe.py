"""Execute original VM pop bodies; observe error calls but stub the error handler."""
from pathlib import Path
import hashlib
import json
import struct
import sys
import time

root=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(root/'Database/Tools/work/ASTRA/python-libs'),str(root/'Reconstruction/Tests/Differential')]
import unicorn
from unicorn import Uc,UC_ARCH_X86,UC_MODE_64,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RSP,UC_X86_REG_RIP,UC_X86_REG_XMM0
from diff_group_completion import read_exe,REFERENCE_SHA256

exe=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
rd=read_exe(exe)
out=Path(__file__).resolve().parent
receipt=dict(start_unix=time.time(),status='INCOMPLETE',exe=str(exe),exe_sha256=REFERENCE_SHA256,
             probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             reader_sha256=hashlib.sha256((root/'Reconstruction/Tests/Differential/diff_group_completion.py').read_bytes()).hexdigest(),
             unicorn_version=unicorn.__version__,cases=[],scope='isolated original code; error handler 008620C0 is a ret stub')
ERROR,CTX,STACK,RET=0x8620C0,0x10000000,0x20000000,0x30000000
cases=[('empty',0,0,0),('negative-depth',-1,0,0),('tag-zero',1,0,42),
       ('tag-three',1,3,42),('tag-ff',1,255,42),('integer',1,1,42),
       ('float',1,2,struct.unpack('<I',struct.pack('<f',2.75))[0])]
try:
    receipt['code']={hex(va):dict(length=n,sha256=hashlib.sha256(rd(va,n)).hexdigest()) for va,n in [(0x267E10,78),(0x267DB0,84)]}
    for mode,va,n in [('int',0x267E10,78),('float',0x267DB0,84)]:
        for name,depth,tag,payload in cases:
            uc=Uc(UC_ARCH_X86,UC_MODE_64)
            for page in [va&~0xfff,ERROR&~0xfff,CTX,STACK,RET]:uc.mem_map(page,0x1000)
            uc.mem_write(va,rd(va,n));uc.mem_write(ERROR,b'\xc3');uc.mem_write(RET,b'\xf4')
            data=bytearray([0xA5]*0x284)
            struct.pack_into('<i',data,0,depth);data[4]=tag;struct.pack_into('<I',data,0x184,payload)
            before=bytes(data);uc.mem_write(CTX,before)
            rsp=STACK+0x800;uc.mem_write(rsp,struct.pack('<Q',RET))
            uc.reg_write(UC_X86_REG_RSP,rsp);uc.reg_write(UC_X86_REG_RCX,CTX)
            uc.reg_write(UC_X86_REG_RAX,0xBAD0BAD0);uc.reg_write(UC_X86_REG_XMM0,0xFFFFFFFFFFFFFFFF)
            trace=[];errors=[];writes=[]
            def instruction(u,address,size,user):
                trace.append(address)
                if address==ERROR:errors.append(dict(target=address,argument=u.reg_read(UC_X86_REG_RCX)&0xffffffff,
                                                     depth=struct.unpack('<i',u.mem_read(CTX,4))[0]))
            def write(u,access,address,size,value,user):
                if CTX<=address<CTX+len(before):writes.append(dict(offset=address-CTX,size=size,value=value))
            uc.hook_add(UC_HOOK_CODE,instruction);uc.hook_add(UC_HOOK_MEM_WRITE,write)
            uc.emu_start(va,RET,count=100)
            assert uc.reg_read(UC_X86_REG_RIP)==RET and uc.reg_read(UC_X86_REG_RSP)==rsp+8
            after=bytes(uc.mem_read(CTX,len(before)))
            result=(uc.reg_read(UC_X86_REG_RAX) if mode=='int' else uc.reg_read(UC_X86_REG_XMM0))&0xffffffff
            expected_depth=depth-1 if depth>0 else depth
            expected_errors=int((mode=='int' and depth>0 and tag not in (1,2)) or (mode=='float' and depth<=0))
            value=0 if depth<=0 or tag not in (1,2) else (42 if tag==1 else 2.75)
            expected_value=int(value) if mode=='int' else struct.unpack('<I',struct.pack('<f',float(value)))[0]
            expected=bytearray(before);struct.pack_into('<i',expected,0,expected_depth)
            observed=dict(mode=mode,case=name,depth_before=depth,tag=tag,payload_bits=payload,
                          return_bits=result,depth_after=struct.unpack('<i',after[:4])[0],errors=errors,
                          writes=writes,instructions=trace,before_hex=before.hex(),after_hex=after.hex(),
                          return_boundary=True,expected_return_bits=expected_value,expected_error_count=expected_errors)
            receipt['cases'].append(observed)
            assert result==expected_value and after==bytes(expected),(mode,name)
            assert len(errors)==expected_errors and all(e['argument']==1 for e in errors),(mode,name)
    assert len(receipt['cases'])==14
    assert any(c['errors'] for c in receipt['cases']), 'missing positive error-hook control'
    receipt['status']='OBSERVED_MATCHING_BOUNDARIES'
finally:
    receipt['end_unix']=time.time()
    (out/'observations.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(receipt['status'],len(receipt['cases']),'cases')
