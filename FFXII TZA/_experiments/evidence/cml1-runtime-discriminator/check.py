"""Method A: correct a queued runtime address/discriminator, no live/native execution."""
from pathlib import Path
import hashlib, json, struct
import capstone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda b:hashlib.sha256(b).hexdigest()
U=lambda b,o:struct.unpack_from('<I',b,o)[0]
I=lambda b,o:struct.unpack_from('<i',b,o)[0]
raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();assert sha(raw)==SHA
pe=U(raw,0x3c);opt=pe+24;base=struct.unpack_from('<Q',raw,opt+24)[0]
assert base==0x120000
table=opt+struct.unpack_from('<H',raw,pe+20)[0]
sections=[struct.unpack_from('<IIII',raw,table+i*40+8) for i in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(va,n):
    for _,rva,size,offset in sections:
        if rva<=va-base and va-base+n<=rva+size:return raw[offset+va-base-rva:offset+va-base-rva+n]
    raise ValueError(hex(va))
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
bodies={};instructions={}
for va,size in [(0x3DA330,59),(0x3DA400,206),(0x3DD230,225)]:
    b=read(va,size);ins=list(md.disasm(b,va));assert ins and sum(i.size for i in ins)==size
    rows=[dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]
    bodies[hex(va)]=dict(bytes=size,sha256=sha(b),raw=b.hex(),instructions=rows)
    instructions.update({i.address:(i.mnemonic,i.op_str) for i in ins})
anchors={
 0x3DA330:('mov','r9, qword ptr [rcx + 0xd8]'),
 0x3DA35B:('add','rax, rax'),0x3DA35E:('mov','edx, dword ptr [r9 + rax*8 + 0x14]'),
 0x3DA410:('mov','rcx, qword ptr [rcx + 0xd8]'),
 0x3DA44A:('add','rax, rax'),0x3DA456:('mov','edx, dword ptr [rcx + rax*8 + 0x14]'),
 0x3DD245:('mov','r14, qword ptr [rcx + 0xf0]'),
 0x3DD290:('add','rax, rax'),0x3DD29F:('mov','edx, dword ptr [r14 + rax*8 + 0x14]')}
for a,expected in anchors.items():assert instructions[a]==expected,(hex(a),instructions[a])

# Bound to the exact named existing authored file, not a broad recensus.
file=HERE/'byu_x0100.ebp';b=file.read_bytes()
assert b[:4]==b'EBP2' and U(b,4)==20
offsets=list(struct.unpack_from('<20I',b,0x10));o8,o9=offsets[8:10]
assert b[o8:o8+4]==b'CML1' and b[o9:o9+4]==b'CAM7'
assert U(b,o8+4)==15 and U(b,o9+4)==16
entry=o8+0x10+1*0x10;nameoff=o8+I(b,entry);name=b[nameoff:b.index(b'\0',nameoff)]
assert name==b'cut2_2' and I(b,entry+4)==14
recs=[];cur=o9+U(b,o9+0x1c)
for index in range(16):
    length=U(b,cur+4);assert length>=0x20 and cur+length<=len(b)
    rec=b[cur:cur+length];recs.append(dict(index=index,offset=cur,bytes=length,sha256=sha(rec),name=rec[8:0x20].split(b'\0')[0].decode('cp932'),raw=rec.hex()))
    cur+=length
matches=[r['index'] for r in recs if r['name']==name.decode()]
assert matches==[8,14]
payload_equal=bytes.fromhex(recs[8]['raw'])[8:]==bytes.fromhex(recs[14]['raw'])[8:]
assert payload_equal
wrong_column=o8+0x14+1*8
assert wrong_column==o8+0x1c and I(b,wrong_column)==0 and wrong_column!=entry+4
# Index0 is an inadequate stride control: both formulas coincide there.
assert 0x14+0*8==0x14+0*16
assert 0x14+1*8!=0x14+1*16

out=dict(status='PREPARED_CORRECTION_NOT_LIVE_CLOSURE',method='A: exact original instructions and existing authored file only',
    executable_sha256=SHA,capstone_version=capstone.__version__,bodies=bodies,
    effective_stride=16,cml1_manager_offset='0xD8',shake_list_manager_offset='0xF0',
    cml1_read_sites=['0x3DA35E','0x3DA456'],shake_read_site='0x3DD29F',
    file=dict(source='Database/Tools/work/repos-d2/ebp/ps2data/plan_master/us/event/byu_x/byu_x0100/byu_x0100.ebp',sha256=sha(b),bytes=len(b),section8_offset=o8,section9_offset=o9,entry=1,name=name.decode(),authored_index=14,first_name_match=8,correct_column_offset='0x24',wrong8byte_column_offset='0x1C',wrong_column_value=I(b,wrong_column),matching_records=[recs[8],recs[14]],payload_equal=payload_equal,full_record_equal=recs[8]['raw']==recs[14]['raw']),
    controls=['Complete nonempty function decodes and exact op/operand anchors','Section tags, counts, entry name and independently traversed CAM7 record lengths','Entry1 distinguishes strides; entry0 does not','Wrong8byte address lands on reserved zero, not14'],
    limits=['No initialized runtime object or actual scene entry observed.','No live write absence/universal never claim.','Matching asset payloads alone do not establish runtime presentation parity; visual-only evidence cannot identify which index was used.','Canonical section008 already documents16-byte stride; correction targets stale queue wording, not a new format discovery.'])
(HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
print('PREPARED_CORRECTION_NOT_LIVE_CLOSURE: 3 complete bodies; two CML1 readers + one shake reader; effective stride16.')
print('byu_x0100 entry1 cut2_2: authored14 vs first8; column blob+24, wrong8-stride blob+1C gives0.')
print('CAM7 duplicate payloads equal:',payload_equal,'full records equal:',out['file']['full_record_equal'])
