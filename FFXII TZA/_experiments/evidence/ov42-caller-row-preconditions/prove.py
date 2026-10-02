"""Terminal-phase row carriers and a bounded stock-row helper control.

This consumes the already accepted phase breakdown; no new phase census or
natural-state claim. Opaque calls have ordinary return/ABI edges, not mocked
native success. Descriptor binding remains an explicit premise.
"""
import copy,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def checked(tag,driver):
 x=json.loads((P/(tag+'.status.json')).read_text())
 need(x.get('terminal') is True and x.get('exit')==0 and x.get('exception') is None and x.get('driver_sha256')==sha(P/driver) and bool((P/(tag+'.stdout')).read_bytes()) and not(P/(tag+'.stderr')).read_bytes(),'required successful current invocation '+tag)
def lineage(file):
 rows=json.loads((P/file).read_text());need(bool(rows),'missing retained lineage')
 for row in rows:
  q=P/row['copy'];need(sha(q)==row['sha256'],'retained member changed')
  t=subprocess.run(['git','ls-tree','-z',row['commit'],'--',row['member']],capture_output=True,timeout=15)
  need(t.returncode==0 and not t.stderr and t.stdout.count(b'\0')==1,'retained tree identity unavailable')
  meta,path=t.stdout[:-1].split(b'\t');_,kind,oid=meta.decode().split()
  need(kind=='blob' and path.decode()==row['member'],'wrong retained tree member')
  z=subprocess.run(['git','cat-file','blob',oid],capture_output=True,timeout=15)
  need(z.returncode==0 and not z.stderr and z.stdout==q.read_bytes(),'retained Git blob differs')
 return rows
def derive(ix,targets,table,G):
 ops=[(0x30488d,'movzx','r13d, word ptr [rsi + 0x64]'),(0x30491f,'mov','r15, rax'),(0x304929,'movzx','ecx, word ptr [rax + 8]'),(0x30492d,'movzx','eax, r13w'),(0x304931,'imul','ecx, eax'),(0x304934,'add','r15d, ecx'),(0x30493c,'movzx','eax, byte ptr [rsi + 4]'),(0x304940,'cmp','eax, 0xc'),(0x304950,'mov','ecx, dword ptr [rdx + rax*4 + 0x1e5044]'),(0x30495a,'jmp','rcx'),
 (0x304ec5,'mov','rcx, qword ptr [rdi + 0x698]'),(0x304ecc,'call','0x387090'),(0x304ed1,'mov','r8d, dword ptr [rsi + 0x60]'),(0x304ed5,'lea','r9, [rsi + 0xc8]'),(0x304edc,'movzx','edx, ax'),(0x304edf,'mov','rcx, rdi'),(0x304ee2,'call','0x30d160'),(0x304ee7,'movzx','edx, r13w'),(0x304eee,'call','0x305430'),(0x304ef3,'movabs','rax, 0x400000000000'),(0x304f3d,'test','dword ptr [r15 + 0xc], 0x40000000'),(0x304f47,'mov','rdx, r15'),(0x304f4d,'call','0x306760'),
 (0x30d184,'mov','ecx, r8d'),(0x30d187,'movzx','edi, dx'),(0x30d18a,'call','0x31b7e0'),(0x30d1d5,'mov','rsi, rax'),(0x30d1df,'movzx','ecx, word ptr [rax + 8]'),(0x30d1e3,'movzx','eax, di'),(0x30d1e6,'imul','ecx, eax'),(0x30d1e9,'add','esi, ecx'),
 (0x305446,'mov','eax, 0x115'),(0x30544d,'movzx','edi, dx'),(0x305453,'cmp','dx, ax'),(0x305456,'ja','0x305578'),(0x305578,'mov','ecx, 0x116'),(0x305580,'sub','ax, cx'),(0x305583,'mov','ecx, 0x108'),(0x305588,'cmp','ax, cx'),(0x30558b,'ja','0x305609'),(0x305590,'je','0x3055c2'),(0x30559e,'je','0x3055c2'),(0x3055b6,'movzx','ebx, word ptr [rcx + 8]'),(0x3055ba,'movzx','ecx, di'),(0x3055bd,'imul','ebx, ecx'),(0x3055c0,'add','ebx, eax'),(0x3055c2,'test','byte ptr [rbx + 0x2c], 0x40'),(0x3055c6,'je','0x305609'),(0x305609,'mov','eax, 0x113'),(0x30560e,'cmp','di, ax'),(0x305611,'jne','0x305623'),(0x305628,'xor','eax, eax'),(0x305634,'ret','')]
 for pc,m,args in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,args),'original operation changed '+hex(pc))
 need(targets==[0x30495c,0x3049fa,0x304a49,0x304a4c,0x304ba5,0x304d73,0x304da5,0x304e2c,0x304eb3,0x304ebe,0x304f62,0x304fe9,0x304ff3],'retained phase switch differs')
 graphs=[]
 for phase in [8,9]:
  a=copy.deepcopy(ix);a[0x30495a]['args']=hex(targets[phase])
  g=G.graph(a,0x304850,0x305042)
  need(0x304f4d in g['visited'] and G.dominates(g,0x304ee2,0x304f4d),'terminal target-builder boundary differs')
  calls=[(hex(pc),name) for pc,name in g['calls']]
  need(not any(n in ['0x30ca80','0x30cfb0'] for _,n in calls),'terminal entry reruns earlier slot admission')
  graphs.append(dict(entry_phase=phase,dispatch_target=hex(targets[phase]),visited=len(g['visited']),target_builder_dominates_sequence=True,earlier_slot_readiness_calls=[],limits='Local normal-return graph, not feasible/natural phase entry or transitive callee effects. Phase breakdown already canonical; not a new census.'))
 count,stride,offset=struct.unpack_from('<III',table,4)
 need((count,stride)==(543,60) and offset+count*stride==len(table),'stock table layout differs')
 rows=[]
 for ident in range(511,535):
  flags=table[offset+ident*stride+0x2c]
  need(not(flags&0x40),'stock row takes target side-effect branch')
  # Branch facts derived from the checked unsigned 16-bit bounds and original
  # row flag. Lookup-success/stock binding supplied explicitly, never observed.
  fixed={0x305456:ident>0x115,0x30558b:((ident-0x116)&0xffff)>0x108,0x305590:False,0x30559e:False,0x3055c6:not bool(flags&0x40),0x305611:ident!=0x113}
  g=G.graph(ix,0x305430,0x305635,fixed=fixed)
  need(g['returns']==[0x305634] and G.dominates(g,0x305628,0x305634),'stock bounded helper return differs')
  need(g['calls']==[(0x305596,'0x20e600'),(0x3055aa,'0x20e600')],'unexpected native side-effect boundary')
  writes=[hex(pc) for pc in g['visited'] for m in ix[pc]['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']
  need(not writes,'helper path writes non-stack state')
  rows.append(dict(id=ident,row_byte_2c=flags,helper_return=0,calls=['0x20e600','0x20e600'],own_nonstack_writes=[]))
 positive=G.graph(ix,0x305430,0x305635,fixed={0x305456:True,0x30558b:False,0x305590:False,0x30559e:False,0x3055c6:False,0x3055d6:False,0x3055e4:False})
 need((0x3055f2,'0x311f70') in positive['calls'],'positive flag control cannot detect intervention boundary')
 builder=G.graph(ix,0x30d160,0x30d54c)
 need(any(n=='rax' for _,n in builder['calls']),'original virtual callback omitted')
 return dict(terminal_entry=graphs,carriers=dict(current_row='R13W latched from entry unit+714; R15 = zeroextend32(second lookup base + latched ID * WORD(third descriptor+8)). The terminal sequence gets this R15.',target_builder='387090 receives unit+698; AX is zeroextended into EDX at304EDC.30D160 latches DX, constructs its separate row with its own descriptor/resolver loads. It is not passed caller R15.',helper='305430 receives the original latched R13W. Its EAX return is overwritten at304EF3, not tested by the terminal caller.'),stock_helper=dict(domain='IDs511..534, u16 entry; stable readable descriptor/resolver bound to the retained US table, valid ABI/stack, normal lookup return. This is a conditional original-source proof, not live binding.',cases=rows,positive_flag40_control='Supplied changed row bit6 reaches311F70 boundary, demonstrating the proof distinguishes the side-effect branch. Mathematical CFG control; not native execution.',limits='No callee20E600 side-effect guarantee. Normal lookup/initialized US binding is a premise; no actual storage pointer or owner lifetime proved.'),builder_opaque_boundaries=[dict(pc=hex(pc),target=n) for pc,n in builder['calls']],answer='The local terminal invocation does not re-establish earlier slot readiness or a shared classifier row. Its target builder and sequence use separately constructed action-row carriers. For the disputed511..534 band,305430 cannot itself enforce ownership through its target-side-effect branches under the exact stock-row binding premises: only two lookups and return0 remain. Natural pairing still requires phase/writer/scheduler and helper-interference evidence.',remaining=['387090 owner mapping/initialized descriptor consistency at phase9, not sampled pointer identity','unit714/phase6B4 writer continuity versus queued slot+1C classifier and global owner/kind persistence','opaque30D160 virtual/helper,303830 preview and305640 resource effects between row construction and sequence; no transitive absence claim','normal gameplay reachability, timing, lifetime and wholeOV42'])
def main():
 out=Path(sys.argv[1]);out=out if out.is_absolute() else P/out;need(not out.exists(),'immutable result exists')
 for tag,driver in [('helper-extents-01','prepare-helper-extents.py'),('helpers-capture-01','capture-helpers.py')]:checked(tag,driver)
 need(sha(P/'capture-index-path.py')=='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497' and sha(P/'validate-title-source-annotations.py')=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13' and sha(P/'prove_owner_reload_order.py')=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed dependency moved')
 origins=lineage('retained-lineage-01.json')+lineage('carrier-lineage-01.json')
 mf=json.loads((P/'carrier-manifest.json').read_text());members={m['path']:m for m in mf['members']}
 need(sha(P/'carrier-manifest.json')=='56100abc27fc97e1fdcd85e7488dc1f712365a4296c3ad819f2622800caed1dd','retained carrier manifest moved')
 for name,member in [('carrier-result-01.json','result-01.json'),('action_data_us.st2e','retained/action-selector-local-exclusions-special-action-frozen-ready--action-selectors-01--tables--action_data_us.st2e')]:need(sha(P/name)==members[member]['sha256'] and(P/name).stat().st_size==members[member]['bytes'],'retained parent membership differs')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'reference image changed')
 pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=load('annotations','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py');ix={};annotations=[]
 files=['current-row-source-01.json','current-row-source-02.json','helper-source-01.json']
 helper=json.loads((P/files[-1]).read_text());need(helper.get('wrapper_complete') is True and helper.get('invocation_driver_sha256')==sha(P/'capture-helpers.py'),'helper capture wrapper incomplete')
 for name in files:
  x=json.loads((P/name).read_text());need(x['exe_sha256']==PIN,'wrong source image');annotations.append(V.validate(x))
  for r in x['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original instructions')
   for i in r['instructions']:
    pc=int(i['pc'],16);need(pc not in ix or ix[pc]==i,'source overlap disagrees');ix[pc]=i
 carrier=json.loads((P/'carrier-result-01.json').read_text());data=next(q for q in carrier['original_data'] if q['address']=='0x305044');z=bytes.fromhex(data['bytes'])
 need(len(z)==52 and z==read(0x305044,52) and hashlib.sha256(z).hexdigest()==data['sha256'],'retained switch data differs')
 targets=[0x120000+k for k in struct.unpack('<13I',z)]
 facts=derive(ix,targets,(P/'action_data_us.st2e').read_bytes(),G)
 with out.open('x') as f:json.dump(dict(producer_complete=True,method='A retained caller/switch/resource plus focused original helper analysis',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in files],retained_lineage=origins,annotation_prerequisites=annotations,facts=facts,novelty='New conditional helper branch/return and terminal ID-carrier composition. Existing phase census, resource bits census and caller no-direct-owner read are consumed, not new experiments.',limits='No native/emulator/live execution. No initialized table/owner binding, natural state, transitive helper effects or wholeOV42 closure. Source/CFG controls and independent acceptance remain separate.',cleanup='Finite offline children terminal; no PC/game/save/config/reference/peer-process mutation.'),f,indent=2)
 print('PROVED terminal separate ID carriers and conditional511..534 helper no-target-effect path; natural coherence OPEN')
if __name__=='__main__':main()
