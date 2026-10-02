"""Source-bound ordinal prefix invariant, descriptor binding and row6 preset.

No FF12 instructions are executed. The model is an induction over the checked
shipping loops. Calls use normal native ABI/returns and stable disjoint inputs;
later callback effects, natural scene binding and final live flags remain open.
"""
import copy,hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
RAW='e92d26899e523429695a97686732abdc46b518487f2870e4ba258fef16977a15'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def receipt(tag,driver):
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/driver) or not(P/(tag+'.stdout')).read_bytes() or(P/(tag+'.stderr')).read_bytes():raise ValueError('required actual invocation failed '+tag)
 return s
def parse(b):
 if len(b)!=80000:raise ValueError('unexpected retained member length')
 length=struct.unpack_from('<I',b,132)[0];d=b[128:128+length]
 if len(d)!=length or length!=61152:raise ValueError('invalid retained section bounds')
 u16=lambda o:struct.unpack_from('<H',d,o)[0]
 u32=lambda o:struct.unpack_from('<I',d,o)[0]
 version=u16(0);ct=struct.unpack_from('<i',d,20)[0];di=struct.unpack_from('<i',d,24)[0]
 if not version>=8 or not 0<=ct<len(d)-18 or not 0<=di<len(d)-4:raise ValueError('unsupported version/count/directory offset')
 n=u16(ct);total=u32(di)
 if n!=8 or di+4+48*total>len(d):raise ValueError('invalid kind-count/directory extent')
 counts=[u16(ct+2+2*k) for k in range(n)]
 if sum(counts)!=total or not total>25:raise ValueError('type-count sum and directory population disagree')
 eoff=di+4+48*25;e=d[eoff:eoff+48];pool=u32(76);no=u32(eoff);start=pool+no
 if not 0<=start<len(d):raise ValueError('name outside section')
 end=d.find(b'\0',start)
 if end<0:raise ValueError('unterminated actor name')
 name=d[start:end].decode('cp932',errors='strict')
 if name!='ラバナ_通常_NPC01' or d[start:end].hex()!='8389836f83695f92ca8fed5f4e50433031':raise ValueError('exact CP932 actor identity disagrees')
 prefixes=[0]
 for count in counts:prefixes.append(prefixes[-1]+count)
 row=next((k for k in range(n) if prefixes[k]<=25<prefixes[k+1]),None)
 if row is None:raise ValueError('ordinal has no native carve row')
 boundaries=[]
 for k in range(n):
  if counts[k]:boundaries.append(dict(row=k,first_ordinal=prefixes[k],last_ordinal=prefixes[k+1]-1))
 return dict(section_bytes=length,section_sha256=hashlib.sha256(d).hexdigest(),version=version,type_count_offset=hex(ct),counts=counts,directory_offset=hex(di),directory_count=total,ordinal=25,entry_offset=hex(eoff),entry_hex=e.hex(),raw_name_hex=d[start:end].hex(),name=name,descriptor_script_type=u16(eoff+4),row=row,prefixes=prefixes,boundaries=boundaries)
def derive(sources,tables,region,b,G):
 ix={int(i['pc'],16):i for x in sources for r in x['ranges'] for i in r['instructions']}
 def need(pc,m,a):
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('required actor binding operation changed '+hex(pc))
 for op in [
  (0x267a0c,'mov','r12, qword ptr [rcx]'),(0x267a0f,'xor','ebp, ebp'),(0x267a11,'mov','r11d, dword ptr [rcx + 0x20]'),
  (0x267a20,'movsxd','rax, dword ptr [r12 + 0x14]'),(0x267a25,'movzx','r13d, word ptr [rax + r12]'),
  (0x267a94,'mov','ebx, ebp'),(0x267a99,'mov','r10d, ebp'),(0x267ab8,'mov','rdi, rbp'),
  (0x267ac2,'movsxd','rax, dword ptr [r12 + 0x14]'),(0x267ac7,'add','rax, rdi'),(0x267aca,'movzx','ecx, word ptr [rax + r12 + 2]'),
  (0x267add,'test','ecx, ecx'),(0x267adf,'jle','0x267b2a'),(0x267ae1,'movzx','r9d, r10b'),(0x267ae5,'mov','r11d, ecx'),(0x267ae8,'and','r9b, 0x1f'),
  (0x267af0,'movsxd','rax, ebx'),(0x267af3,'inc','ebx'),(0x267af5,'mov','qword ptr [r14 + rax*8 + 8], rdx'),
  (0x267afa,'movzx','ecx, byte ptr [rdx + 3]'),(0x267afe,'and','cl, 0xe0'),(0x267b01,'or','cl, r9b'),(0x267b04,'mov','byte ptr [rdx + 3], cl'),
  (0x267b07,'and','cl, 0x1f'),(0x267b0a,'movzx','eax, byte ptr [r8]'),(0x267b0e,'shl','al, 5'),(0x267b11,'or','cl, al'),(0x267b13,'mov','byte ptr [rdx + 3], cl'),
  (0x267b16,'movzx','eax, word ptr [r8 + 2]'),(0x267b1b,'add','eax, 0xf'),(0x267b1e,'and','eax, 0xfffffff0'),(0x267b21,'add','rdx, rax'),
  (0x267b24,'sub','r11, 1'),(0x267b28,'jne','0x267af0'),(0x267b2a,'inc','r10d'),(0x267b2d,'add','rdi, 2'),(0x267b31,'add','r8, 4'),(0x267b35,'cmp','r10d, r13d'),(0x267b38,'jl','0x267ac2'),
  (0x267b63,'mov','ebx, dword ptr [rsp + 0x50]'),(0x267b70,'mov','r8d, ebp'),(0x267b73,'mov','rdx, r14'),(0x267b76,'mov','rcx, r15'),(0x267b79,'call','0x266530'),(0x267b7e,'inc','ebp'),(0x267b80,'cmp','ebp, ebx'),(0x267b82,'jl','0x267b70'),
  (0x26654c,'mov','rsi, qword ptr [rcx]'),(0x266556,'movsxd','r10, r8d'),(0x266564,'mov','rdi, r10'),(0x26656a,'mov','rbx, qword ptr [rdx + r10*8 + 8]'),
  (0x2665a6,'mov','rcx, rbx'),(0x2665a9,'call','0x266ad0'),(0x2665ae,'mov','rcx, rbx'),(0x2665b1,'call','0x266bd0'),
  (0x266710,'movsxd','rcx, dword ptr [rsi + 0x18]'),(0x266714,'movzx','eax, word ptr [rsi]'),(0x266717,'add','rcx, rsi'),(0x26671a,'cmp','eax, 8'),(0x26671d,'jb','0x266729'),
  (0x26671f,'lea','rdi, [r10 + r10*2]'),(0x266723,'shl','rdi, 4'),(0x266729,'shl','rdi, 5'),(0x26672d,'add','rdi, 4'),(0x266731,'add','rdi, rcx'),(0x266734,'mov','qword ptr [rbx + 0x40], rdi'),
  (0x266ad0,'mov','rdx, rcx'),(0x266ad3,'movzx','ecx, byte ptr [rcx + 3]'),(0x266ad9,'and','eax, 0x1f'),(0x266ae7,'lea','r9, [rip - 0x146aee]'),(0x266aee,'mov','eax, dword ptr [r9 + rax*4 + 0x146ba4]'),(0x266af6,'add','rax, r9'),(0x266af9,'jmp','rax'),
  (0x266bd0,'movzx','r8d, byte ptr [rcx + 3]'),(0x266bd8,'and','eax, 0x1f'),(0x266bdb,'cmp','eax, 7'),(0x266be0,'lea','r9, [rip - 0x146be7]'),(0x266be9,'mov','edx, dword ptr [r9 + rax*4 + 0x146c30]'),(0x266bf1,'add','rdx, r9'),(0x266bf4,'jmp','rdx'),
  (0x266c0e,'and','r8b, 0x1f'),(0x266c12,'mov','dword ptr [rcx + 0x1c], 0x30004'),(0x266c19,'cmp','r8b, 5'),(0x266c1d,'jne','0x266c2f'),
  (0x268edc,'test','dword ptr [rcx + 0x1c], 0x20000'),(0x268f2b,'test','dword ptr [rdi + 0x1c], 0x10000')
 ]:need(*op)
 if ix[0x267abb]['memory'][0]['rip_target']!='0x1e0c328' or ix[0x267a3a]['memory'][0]['rip_target']!='0x1e0c32a':raise ValueError('kind size table identity changed')
 table=bytes.fromhex(tables['spans'][0]['hex']);switch=bytes.fromhex(tables['spans'][1]['hex']);regions=bytes.fromhex(region['hex'])
 if [(q['address'],q['bytes']) for q in tables['spans']]!=[('0x1e0c328',32),('0x266c30',32)] or(region['address'],region['bytes'])!=('0x266ba4',32):raise ValueError('native kind/switch table identity changed')
 if len(table)!=32 or len(switch)!=32 or len(regions)!=32:raise ValueError('missing switch/type table')
 kinds=[dict(kind=table[k*4],sub=table[k*4+1],size=struct.unpack_from('<H',table,k*4+2)[0]) for k in range(8)]
 data=parse(b);row=data['row']
 if row!=6 or data['counts']!=[9,11,0,0,0,4,72,0]:raise ValueError('this retained actor no longer has row6 premise')
 full=G.graph(ix,0x2679f0,0x267ba4)
 g=G.graph(ix,0x2679f0,0x267ba4,fixed={0x267a2d:False,0x267ab2:False})
 if not G.dominates(g,0x267a94,0x267af5) or not G.dominates(g,0x267b38,0x267b79):raise ValueError('carve zero state/complete outer loop no longer dominates initializer')
 if full['edges'][0x267b28]!=[0x267af0,0x267b2a] or any(ix[a]['mnemonic'] in ['call','ret','jmp'] for a in full['visited'] if 0x267af0<=a<0x267b2a):raise ValueError('unexpected carve side effect/exit boundary')
 ig=G.graph(ix,0x266530,0x266acf,tail='0x3db280')
 if ig['tails']!=[0x266aca]:raise ValueError('initializer tail boundary changed')
 if not G.dominates(ig,0x2665b1,0x266734):raise ValueError('preset not on descriptor binding entry path')
 for entry,end,pc,tablebytes in [(0x266ad0,0x266ba3,0x266af9,regions),(0x266bd0,0x266c30,0x266bf4,switch)]:
  target=0x120000+struct.unpack_from('<I',tablebytes,4*row)[0]
  if not entry<=target<end:raise ValueError('row6 original switch target outside body')
  resolved=copy.deepcopy(ix);resolved[pc]['args']=hex(target)
  fixed={0x266adf:False,0x266b91:True} if entry==0x266ad0 else {0x266bde:False,0x266c1d:True}
  branch=G.graph(resolved,entry,end,fixed=fixed)
  if branch['calls']:raise ValueError('pre-preset source has unchecked native callback')
  for a in branch['visited']:
   i=ix[a]
   if i['args'].split(', ',1)[0] in ['r10','r10d','r10w','r10b','rdi','edi','di','dil','r11','r11d'] and i['mnemonic'] not in ['cmp','test','push']:raise ValueError('volatile ordinal/image-base carrier changed before directory binding')
   if entry==0x266ad0 and any(m['base']=='rdx' and m['displacement']<=3<m['displacement']+m['size'] and m['role'] in ['w','rw'] for m in i['memory']):raise ValueError('pre-preset helper overwrites category byte')
  if entry==0x266bd0 and (0x266c12 not in branch['visited'] or not G.dominates(branch,0x266c12,0x266c2f)):raise ValueError('row6 preset store not proved')
 writes=[]
 for r in sources[0]['ranges']:
  if r['start']!='0x266530':continue
  for i in r['instructions']:
   for m in i['memory']:
    if m['base']=='rbx' and m['role'] in ['w','rw'] and m['displacement']<0x20 and m['displacement']+m['size']>0x1c:
     if (m['size'],m['displacement'])!=(4,0x1c) or i['mnemonic'] not in ['and','or']:raise ValueError('unchecked initializer request-word write')
     mask=int(i['args'].split(', ')[1],0)&0xffffffff
     if (mask if i['mnemonic']=='or' else (~mask&0xffffffff))&0x30000:raise ValueError('direct initializer store changes talk gates')
     writes.append(dict(pc=i['pc'],mnemonic=i['mnemonic'],mask=hex(mask)))
 if len(writes)!=6:raise ValueError('unexpected direct request-word writer population')
 # Induction certificate for the actual two nested loops; a mathematical model
 # is not a synthetic original-code execution or normal game-reachability proof.
 certificate=dict(basis='EBX=R10D=RDI=0 before carve; R8=kind table row0',inner='For row k with count c[k], exactly c[k] iterations: old EBX is pointer slot; EBX++, stamp low5=k/top3=table[k].kind; advance by rounded size; R11-- until0.',outer='After row k, EBX=S[k+1], R10D=k+1, RDI=2(k+1), R8=table+4(k+1). Zero-count row skips inner and still increments k; S[k]=sum(c[:k]).',consequence='Ordinal i in [S[k],S[k+1]) maps to carve rowk. Initializer gets same pool, i; RBX=pool[1+i]; directory=desc+signedDWORD18+4+48*i for version>=8 (32*i for older).',bounds='This member N8 and96 counts, valid nonnegative signed count/offsets, directory extent61152B and stable disjoint descriptors/pool/frame required; normal native ABI/returns. No malformed/all-corpus safety claim.')
 return dict(data=data,native_kind=kinds[row],actor_byte3=hex((kinds[row]['kind']<<5)|row),preset_at_266c12='0x30004',talk_gate_bits=[16,17],direct_initializer_request_word_writes=writes,
  ordinal_invariant=certificate,initializer_tail={'pc':'0x266aca','target':'0x3db280','effects':'outside this proof'},claim_established='This exact asp_a03 ordinal25 is carve row6 and descriptor ordinal25 on the valid allocator/initializer path; original row6 preset writes request bits16/17.',
  label_limit='Descriptor WORD+4 agrees with6 in this member, but this binding/stamp/preset path does not use it as a selector. Category assignment follows header count prefixes and ordinal, not an independent runtime read of scriptType.',
  callback_limit='Later direct initializer AND/OR stores preserve bits16/17. The original initializer exits through a tail to3DB280; transitive callback/tail effects, final returned/live flags and natural scene reachability are not proved here.',
  unresolved=['natural initialize/load of this scene and runtime pointer identity','native later callback effects/final flags','OV16 talkterm cancellation/reentry timing/end-notification consumption','all-corpus correspondence between descriptor labels and prefix rows'])
def main():
 for name,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/name)!=pin:raise ValueError('reviewed dependency changed')
 sources=[]
 for tag,driver,name in [('capture-01','capture.py','source-01.json'),('binding-01','capture-binding.py','source-binding-01.json'),('setup-01','capture-setup.py','source-setup-01.json')]:
  receipt(tag,driver);x=json.loads((P/name).read_text())
  if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/driver) or x['driver_sha256']!=sha(P/'capture-index-path.py') or x['exe_sha256']!=PIN:raise ValueError('capture invocation/reference mismatch')
  sources.append(x)
 receipt('archive-01','archive-member.py');a=json.loads((P/'archive-member-01.json').read_text())
 if a.get('complete') is not True or a['driver_sha256']!=sha(P/'archive-member.py') or a['member']['sha256']!=RAW or a['member']['bytes']!=80000 or len(a['blocks'])!=2:raise ValueError('archive member provenance incomplete')
 A=load('strict_archive','archive-member.py');chunks=[]
 for q in a['blocks']:
  raw=(P/q['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=q['sha256']:raise ValueError('retained archive block changed')
  value,mode=A.decode(raw,q['expected_bytes'])
  if mode!=q['mode'] or hashlib.sha256(value).hexdigest()!=q['decoded_sha256']:raise ValueError('block decode identity changed')
  chunks.append(value)
 b=(P/'asp_a03-US-original-01.ebp').read_bytes()
 if b!=b''.join(chunks) or sha(P/'asp_a03-US-original-01.ebp')!=RAW:raise ValueError('raw actor input differs')
 tables=json.loads((P/'native-tables-01.json').read_text());region=json.loads((P/'region-switch-01.json').read_text())
 if tables['driver_sha256']!=sha(P/'capture.py') or region['driver_sha256']!=sha(P/'capture-setup.py'):raise ValueError('unchecked native table producer')
 V=load('annotation','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py');annotations=[V.validate(x) for x in sources]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('wrong original EXE')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
 secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original span')
 expected=[(0x2679f0,0x267ba4),(0x266530,0x266acf),(0x266bd0,0x266c30),(0x268ea0,0x269057),(0x266ad0,0x266ba3),(0x26ce60,0x26d394)]
 ranges=[r for x in sources for r in x['ranges']]
 if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in ranges]!=expected:raise ValueError('source extent/population changed')
 for r in ranges:
  lo,hi=int(r['start'],16),int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise ValueError('source differs from exact original EXE')
 for t in tables['spans']+[region]:
  q=bytes.fromhex(t['hex'])
  if t.get('exe_sha256',tables['exe_sha256'])!=PIN:raise ValueError('table image pin changed')
  if q!=read(int(t['address'],16),t['bytes']) or hashlib.sha256(q).hexdigest()!=t['sha256']:raise ValueError('original table bytes changed')
 facts=derive(sources,tables,region,b,G)
 result=dict(producer_complete=True,method='A STATIC_ONLY source-bound induction and one retained exact archive member',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['source-01.json','source-binding-01.json','source-setup-01.json']],annotation_prerequisites=annotations,facts=facts,
  limits=['No native/emulated/game execution.','Archive header/selected compressed/member identity only, no full archive digest or install-authenticity assertion.','Valid stable disjoint native inputs, adequate allocation, normal ABI/returns and positive manager count covering ordinal25; actual scene setup remains separate.',facts['callback_limit']],cleanup='Finite offline source reads/proofs only; all own handles/children closed. No PC/game/save/config/reference or peer changes.')
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise ValueError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED exact ordinal25 to row6 and descriptor binding/preset; scriptType label is not the native selector; live scheduling OPEN')
if __name__=='__main__':main()
