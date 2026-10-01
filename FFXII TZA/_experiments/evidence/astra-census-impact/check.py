"""Test the retained census as-is with disposable code/catalog input, NOT FF12.

These are instrument controls, not shipping-instruction or live-game evidence.
The tested source is preserved unchanged. Unicorn independently records each
synthetic fixture's writes; the original scanner receives those same bytes.
"""
import contextlib, hashlib, io, json, struct, sys, types
from pathlib import Path
from unittest.mock import patch
import capstone
import unicorn
from unicorn import x86_const as U

HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
source=(HERE/'sources/aq18_span_write_census.py').read_bytes()
LO=0x2165176
cases=[]
def add(name,seed,tail,expected,reported):
    entry=0x100000+len(cases)*0x100
    # Synthetic LEA of the exact address the scanner calls its contested span.
    lea=bytes.fromhex('488d05' if seed=='rax' else '488d1d')+struct.pack('<i',LO-entry-7)
    body=lea+bytes.fromhex(tail)
    cases.append(dict(name=name,entry=entry,body=body,expected=expected,reported=reported))
add('direct-positive','rax','c60001',LO,LO)
add('call-kills-volatile','rax','e8f47f0000c60001',0,None)
add('call-preserves-nonvolatile','rbx','e8f47e0000c60301',LO,LO)
add('eax-zero-kills-full-rax','rax','31c0c60001',0,None)
add('al-zero-moves-outside-span','rax','30c0c60001',LO&~0xff,LO)
add('ax-zero-moves-outside-span','rax','6631c0c60001',LO&~0xffff,LO)
add('al-write-changes-exact-target','rax','b090c60001',(LO&~0xff)|0x90,LO)
add('add-index-base-zero-index','rax','31c94801c1c60101',LO,None)
add('add-base-index-zero-index','rax','31c94801c8c60001',LO,None)
add('add-immediate-positive','rax','4883c001c60001',LO+1,LO+1)
assert len(cases)==10

class Image:
    def __init__(self,*args): pass
    def read(self,address,count):
        for c in cases:
            off=address-c['entry']
            if 0<=off<len(c['body']):return c['body'][off:off+count]
        raise AssertionError(hex(address))
catalog='entry\tbody_bytes\n'+''.join(f"{c['entry']:08X}\t{len(c['body'])}\n" for c in cases)
kp=types.ModuleType('kit_paths');kp.EXE='DISPOSABLE_FIXTURE';kp.WORK='DISPOSABLE_CATALOG'
df=types.ModuleType('disasm_fn');df.Image=Image
stdout=io.StringIO();ns={'__name__':'__census_instrument_control__'}
def fake_open(path,*args,**kwargs):
    assert str(path).replace('\\','/')=='DISPOSABLE_CATALOG/graph/functions.tsv',path
    return io.StringIO(catalog)
with patch.dict(sys.modules,{'kit_paths':kp,'disasm_fn':df}),patch.object(io,'open',fake_open),contextlib.redirect_stdout(stdout):
    exec(compile(source.decode('utf-8'),str(HERE/'sources/aq18_span_write_census.py'),'exec'),ns)
assert len(ns['fns'])==10 and ns['resolved_sites']>0
observations=[]
for c in cases:
    machine=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
    machine.mem_map(0x100000,0x10000)
    machine.mem_map(0x2160000,0x10000)
    machine.mem_map(0,0x1000)
    machine.mem_map(0x200000,0x10000)
    machine.reg_write(U.UC_X86_REG_RSP,0x208000)
    machine.mem_write(c['entry'],c['body'])
    # Both synthetic calls reach108100, where a legal test callee destroys RAX.
    machine.mem_write(0x108100,bytes.fromhex('31c0c3'))
    writes=[]
    def write(uc,access,address,size,value,user):
        if not 0x200000<=address<0x210000:
            writes.append(dict(address=address,size=size,value=value))
    machine.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
    machine.emu_start(c['entry'],c['entry']+len(c['body']),count=40)
    assert machine.reg_read(U.UC_X86_REG_RIP)==c['entry']+len(c['body'])
    assert writes==[dict(address=c['expected'],size=1,value=1)],(c['name'],writes)
    hits=[h for h in ns['span_hits'] if h[1]==c['entry']]
    actual=[h[2] for h in hits]
    assert actual==([] if c['reported'] is None else [c['reported']]),(c['name'],actual)
    dis=list(capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64).disasm(c['body'],c['entry']))
    assert sum(i.size for i in dis)==len(c['body'])
    observations.append(dict(name=c['name'],entry=hex(c['entry']),synthetic_code_hex=c['body'].hex(),
        instructions=[f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in dis],
        actual_write=writes[0],scanner_addresses=actual,
        hit_is_accurate=actual==([c['expected']] if ns['LO']<=c['expected']<ns['HI'] else [])))
assert sum(not r['hit_is_accurate'] for r in observations)==5
out=dict(method='Synthetic instrument regression controls only; no original FF12 execution or live test',
         source_sha256=sha(source),checker_sha256=sha(Path(__file__).read_bytes()),
         python_version=sys.version,capstone_version=capstone.__version__,unicorn_version=unicorn.__version__,
         cases=observations,source_stdout=stdout.getvalue(),
         limits=['Not evidence that these byte sequences occur in shipping FF12.',
                 'No whole-executable census rerun; historical totals have not been recalculated.',
                 'Known-address tracking differs from base provenance; retaining an unknown indexed address as exact would be unsound.',
                 'No change to peer-owned scanner or canonical type rows.'])
dest=HERE/'observation.json'
if '--write' in sys.argv:
    assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n')
else:
    assert json.loads(dest.read_text())==out
print('PASS: 10 bounded instrument cases executed; original scanner source unchanged.')
print('3 partial-register controls expose false target attribution; 2 register-add controls expose missed known writes.')
print('Call-clobber, nonvolatile preservation, EAX kill, direct and immediate-add controls behaved as expected.')
