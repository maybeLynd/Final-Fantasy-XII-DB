"""Method A only: original bytes and calculated representation/boundary controls."""
import hashlib,json,struct
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=(HERE.parents[4]/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
assert sha(raw)==EXE
pe=struct.unpack_from('<I',raw,0x3c)[0];opt=pe+24
base=struct.unpack_from('<Q',raw,opt+24)[0];assert base==0x120000
table=opt+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<IIII',raw,table+i*40+8) for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(va,n):
    for _,rva,size,offset in sections:
        if rva<=va-base and va-base+n<=rva+size:return raw[offset+va-base-rva:offset+va-base-rva+n]
    raise AssertionError('unmapped original body')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
instructions={};bodies=[]
for va,n in [(0x32E7C0,173),(0x32E870,285),(0x32E070,605),(0x2DF6C0,192),(0x1D6D90,225)]:
    b=read(va,n);ins=list(md.disasm(b,va));assert ins and sum(i.size for i in ins)==n
    rows=[dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]
    bodies.append(dict(address=hex(va),bytes=n,sha256=sha(b),raw=b.hex(),instructions=rows))
    instructions.update({i.address:i for i in ins})
anchors={
 0x32E846:('mov','edx, edi'),0x32E848:('mov','ecx, 0xff'),0x32E84D:('call','0x32e870'),
 0x32E897:('mov','ebp, edx'),0x32E902:('mov','dword ptr [r10 + 0x24], ebp'),
 0x32E965:('mov','dword ptr [r10 + 0x64], eax'),0x32E983:('add','rsp, 0x20'),
 0x32E0CA:('mov','r8d, dword ptr [rbx + 0x28]'),0x32E0CE:('test','r8d, r8d'),
 0x32E0D3:('movzx','eax, byte ptr [rbx + 0x21]'),0x32E0D7:('cmp','al, 0xff'),
 0x32E105:('movsxd','rcx, dword ptr [rbx + 0x24]'),0x32E111:('call','0x2df6c0'),
 0x2DF6DE:('mov','rbx, rcx'),0x2DF774:('mov','rcx, rbx'),0x2DF777:('call','0x1d6d90'),
 0x1D6DAE:('mov','rbx, rcx'),0x1D6E20:('movzx','ecx, byte ptr [rbx]'),0x1D6E27:('lea','rbx, [rbx + 1]')}
for a,expected in anchors.items():
    i=instructions[a];assert (i.mnemonic,i.op_str)==expected,(hex(a),i.mnemonic,i.op_str)
assert instructions[0x32E846].address+instructions[0x32E846].size==0x32E848
assert instructions[0x32E848].address+instructions[0x32E848].size==0x32E84D
examples=[]
for p in (0x7FFFFFFF,0x80000000,0x8BC13000,0xFFFFFFFF,0x100000000,0x100001000,0x180000000,0x18BC13000):
    low=p&0xFFFFFFFF
    q=struct.unpack('<i',struct.pack('<I',low))[0]&0xFFFFFFFFFFFFFFFF
    examples.append(dict(pointer=f'{p:016X}',low32=f'{low:08X}',issued=f'{q:016X}',
                         sign_bit=bool(low&0x80000000),pointer_preserved=p==q,
                         old_above2gb_predicate=p>=0x80000000))
assert len(examples)==8 and examples[0]['pointer_preserved']
assert examples[5]['old_above2gb_predicate'] and not examples[5]['sign_bit'] and examples[5]['issued']=='0000000000001000'
assert examples[2]['issued']==examples[7]['issued']=='FFFFFFFF8BC13000'
assert not any(e['pointer_preserved'] for e in examples[1:])
out=dict(status='CORRECTED_OBSERVATION_SPEC_NOT_LIVE_CAUSE_CLOSURE',method='A',live_game=False,
         executable_sha256=EXE,capstone_version=capstone.__version__,bodies=bodies,
         anchors_checked=len(anchors),boundary_examples=examples,
         limits=['No emulator/native execution performed.','No current allocator placement or actual raw-path trigger observed.',
                 'Unknown historical crash cause remains unknown.','No original functions modified; original static narrowing mechanism remains valid.'])
(HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
print(f'PASS:{len(bodies)} complete original bodies,{len(anchors)} exact anchors; pre-assignment vs delivered-argument sites distinguished.')
print('8calculated representation boundaries; above4GB with low bit31 clear refutes the overbroad sign-filled-address predicate.')
