import hashlib,json,struct,sys
from pathlib import Path
import capstone
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
prior=ROOT/'Database/FFXII TZA/_experiments/evidence/status-watch-preflight'
meta=json.loads((prior/'source.json').read_text());table=(prior/'status-table.bin').read_bytes()
assert sha(table)==meta['table_sha256']
sys.path.insert(0,str(ROOT/'agent_flow/tools'));import vbfextract
with Path(meta['archive']).open('rb') as f:
 names,blocks=vbfextract.load_index(f);raw=vbfextract.read_entry(f,names,blocks,meta['entry'])
assert sha(raw)==meta['entry_sha256'] and len(raw)==meta['entry_bytes']
assert raw[meta['table_file_offset']:meta['table_file_offset']+len(table)]==table
section=struct.unpack_from('<I',raw,0xF8)[0]
count=struct.unpack_from('<I',raw,section)[0];assert count==15
offsets=struct.unpack_from('<16I',raw,section+4)
assert offsets[0]==68 and all(a<=b for a,b in zip(offsets,offsets[1:])) and section+offsets[-1]<=len(raw)
bank=raw[section+offsets[5]:section+offsets[6]]
(HERE/'bank5.bin').write_bytes(bank);(HERE/'directory.bin').write_bytes(raw[:0xFC]);(HERE/'status-table.bin').write_bytes(table)
image=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';exe=image.read_bytes()
assert sha(exe)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',exe,60)[0];opt=struct.unpack_from('<H',exe,pe+20)[0]
assert struct.unpack_from('<Q',exe,pe+24+24)[0]==0x120000
sections=[]
for i in range(struct.unpack_from('<H',exe,pe+6)[0]):
 o=pe+24+opt+i*40;vs,va,rs,ro=struct.unpack_from('<IIII',exe,o+8);sections.append((0x120000+va,min(vs,rs),ro))
def read(a,n):
 for va,size,off in sections:
  if va<=a and a+n<=va+size:return exe[off+a-va:off+a-va+n]
 raise AssertionError('unbacked image range')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
windows=[]
for start,end in [(0x31E1C0,0x31E2E7),(0x31C7B7,0x31C7FE)]:
 code=read(start,end-start);ins=list(md.disasm(code,start))
 assert sum(i.size for i in ins)==len(code),(hex(start),hex(end),ins[-1].address)
 windows.append({'start':hex(start),'end_exclusive':hex(end),'bytes':len(code),'hex':code.hex(),'sha256':sha(code),
 'instructions':[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
 print('WINDOW',hex(start),len(code))
 for i in ins:print(f'{i.address:08X} {i.mnemonic:8} {i.op_str}')
sources={'method':'A original resource/code; no native execution or live game',
 'prior_package':'Database/FFXII TZA/_experiments/evidence/status-watch-preflight',
 'prior_source_sha256':sha((prior/'source.json').read_bytes()),'prior_table_sha256':sha(table),
 'entry':meta['entry'],'entry_bytes':len(raw),'entry_sha256':sha(raw),'archive_index_sha256':meta['index_sha256'],
 'archive_entire_content_hashed':False,'text_section_offset':section,'text_bank_offsets':list(offsets),
 'bank5_bytes':len(bank),'bank5_sha256':sha(bank),'directory_sha256':sha(raw[:0xFC]),
 'exe_sha256':sha(exe),'capstone_version':capstone.__version__,'code_windows':windows}
(HERE/'source.json').write_text(json.dumps(sources,indent=2)+'\n')
print('RETAINED TABLE',len(table),'bank5',len(bank),'no process opened')
