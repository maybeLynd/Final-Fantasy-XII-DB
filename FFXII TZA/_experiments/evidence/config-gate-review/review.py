"""Bounded offline primary review; no execution or universal writer census."""
import hashlib,json,struct,sys
from pathlib import Path
import capstone
from capstone.x86 import X86_OP_MEM,X86_REG_RIP
E=Path(__file__).resolve().parent
exe=Path(r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe")
raw=exe.read_bytes(); sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=="73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe=struct.unpack_from("<I",raw,60)[0]; opt=pe+24
base=struct.unpack_from("<Q",raw,opt+24)[0]; assert base==0x120000
st=opt+struct.unpack_from("<H",raw,pe+20)[0]
sections=[struct.unpack_from("<IIII",raw,st+40*i+8) for i in range(struct.unpack_from("<H",raw,pe+6)[0])]
def read(va,n):
 for vs,rva,rs,off in sections:
  d=va-base-rva
  if 0<=d and d+n<=rs:return raw[off+d:off+d+n]
 raise ValueError(hex(va))
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);md.detail=True
out=dict(method="A: original bytes/disassembly only",reference_path=str(exe),reference_sha256=sha(raw),image_base=hex(base),capstone_version=capstone.__version__,python=sys.version,review_tool_sha256=sha(Path(__file__).read_bytes()),bodies=[])
# Getter and reset terminate at the stated RET, before the alignment padding.
# Requester extent reuses the existing complete original receipt, not a fresh census.
for va,n in [(0x408B00,8),(0x408BA0,131),(0x314440,233)]:
 data=read(va,n); ins=list(md.disasm(data,va));assert sum(i.size for i in ins)==n and ins[-1].mnemonic=="ret"
 rows=[]
 for i in ins:
  row=dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)
  refs=[dict(address=hex(i.address+i.size+o.mem.disp),width=o.size,access=o.access) for o in i.operands if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP]
  if refs:row['rip_operands']=refs
  rows.append(row)
 out['bodies'].append(dict(address=hex(va),size=n,sha256=sha(data),bytes=data.hex(),instructions=rows))
source=E.parent/'spawn-restore-request'/'primary.json'; old=json.loads(source.read_text(encoding='utf-8'))
b=next(b for b in old['bodies'] if b['address']=='0x314440'); fresh=out['bodies'][2]
assert b['sha256']==fresh['sha256'] and b['bytes']==fresh['size']
assert ''.join(i['bytes'] for i in b['instructions'])==fresh['bytes']
rows={int(i['address'],16):i for b in out['bodies'] for i in b['instructions']}
assert rows[0x408B00]['rip_operands']==[dict(address='0x2b62db9',width=1,access=1)]
assert rows[0x408BA0]['bytes']=='33c0'
assert rows[0x408BBC]['rip_operands']==[dict(address='0x2b62db9',width=1,access=2)]
assert rows[0x408BBC]['operands'].endswith(', al')
assert rows[0x31445E]['operands']=='0x408b00'
assert rows[0x314463]['bytes']=='85c0' and rows[0x314465]['operands']=='0x314471'
assert rows[0x314467]['bytes']=='85db' and rows[0x314469]['bytes']=='b80c000000' and rows[0x31446E]['bytes']=='0f44d8'
out['controls']=dict(full_reference_hash=True,three_complete_decodes=True,existing_whole_requester_bytes_match=True,getter_read_and_reset_write_same_byte=True,conditional_branch_bytes_match=True)
out['source']=dict(path=source.as_posix(),sha256=sha(source.read_bytes()))
out['observation']={'reset':'00408BA0 sets EAX=0; 00408BBC stores AL to 02B62DB9. No intervening EAX redefinition in the preserved body.', 'getter':'00408B00 zero-extends 02B62DB9 and returns it.', 'requester':'00314440 substitutes 12 for requested field 0 only if the getter returned 0.'}
out['interpretation']='The known reset establishes zero at that write. The shipping requester preserves a condition. A universal always-zero invariant is not established by an exact-target RIP-reference census alone.'
out['limits']=['No original instruction was executed.','No whole-image writer census was reproduced here.','No alternate writer is demonstrated by this review.','Alias stores, covering stores and initialization/caller ordering need coverage before an all-runs invariant can replace the condition.','Reset execution in every initialized path is not established by this static receipt.']
out['cleanup']='Read-only original file and prior evidence access; no FF12 process, input, save/config writes, hooks or handles.'
if len(sys.argv)!=2:raise SystemExit('usage: review.py <new-output.json>')
with Path(sys.argv[1]).open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,indent=2);f.write('\n')
print('Verified 3 bodies, 372 bytes,',sum(len(b['instructions']) for b in out['bodies']),'instructions; A only, no all-writer verdict')
