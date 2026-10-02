"""Original slot admission is a capacity scan, not an action-ID range check."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(old,tail,G):
 ix={int(i['pc'],16):i for x in [old,tail] for r in x['ranges'] for i in r['instructions']}
 def need(pc,m,a):
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise ValueError('slot admission operation changed '+hex(pc))
 for op in [
  (0x30d075,'mov','r11d, ecx'),(0x30d07f,'mov','ecx, 0xffff'),(0x30d084,'movzx','r10d, dx'),(0x30d088,'xor','r8b, r8b'),
  (0x30d090,'cmp','r8b, 0x1f'),(0x30d094,'ja','0x30d0a7'),(0x30d096,'movsx','rax, r8b'),(0x30d09a,'lea','r9, [rax + rax*2]'),(0x30d09e,'shl','r9, 4'),(0x30d0a2,'add','r9, rdi'),
  (0x30d0aa,'cmp','word ptr [r9 + 0x1c], cx'),(0x30d0af,'je','0x30d0c2'),(0x30d0b1,'inc','r8b'),(0x30d0b4,'cmp','r8b, 0x20'),(0x30d0b8,'jl','0x30d090'),(0x30d0ba,'mov','al, 0xff'),(0x30d0c1,'ret',''),
  (0x30d0c2,'test','r8b, r8b'),(0x30d0c5,'jns','0x30d0cf'),(0x30d0cf,'cmp','r8b, 0x1f'),(0x30d0d3,'jg','0x30d0e6'),
  (0x30d0d5,'movsx','rax, r8b'),(0x30d0d9,'lea','rcx, [rax + rax*2]'),(0x30d0dd,'shl','rcx, 4'),(0x30d0e1,'add','rcx, rdi'),
  (0x30d0e8,'cmp','r8b, 0x1f'),(0x30d0ec,'jg','0x30d12d'),(0x30d0ee,'movsx','rax, r8b'),(0x30d0f2,'lea','rdx, [rax + rax*2]'),(0x30d0f6,'shl','rdx, 4'),(0x30d0fa,'add','rdx, rdi'),
  (0x30d132,'movzx','eax, r8b'),(0x30d136,'mov','dword ptr [rcx + 0x18], 1'),(0x30d13d,'mov','dword ptr [rcx + 0x14], 1'),(0x30d144,'mov','dword ptr [rcx + 0x10], 1'),
  (0x30d14b,'mov','dword ptr [rcx + 0x20], r11d'),(0x30d14f,'mov','word ptr [rcx + 0x1c], r10w'),(0x30d154,'ret',''),
  (0x30cfbf,'cmp','byte ptr [rcx + 4], 0xff'),(0x30cfc3,'movzx','ebx, r8w'),(0x30cfc7,'mov','esi, edx'),(0x30cfc9,'mov','rdi, rcx'),(0x30cfcc,'jne','0x30d059'),
  (0x30d011,'test','dword ptr [rcx + 0xc], 0x40000000'),(0x30d018,'je','0x30d04c'),(0x30d01a,'mov','ecx, 0xd0'),(0x30d01f,'movzx','eax, bx'),(0x30d022,'sub','ax, cx'),(0x30d025,'cmp','ax, 0x21'),(0x30d029,'ja','0x30d039'),
  (0x30d039,'mov','eax, dword ptr [rip + 0x1fb5119]'),(0x30d03f,'test','al, 2'),(0x30d041,'jne','0x30d059'),(0x30d04c,'movzx','edx, bx'),(0x30d04f,'mov','ecx, esi'),(0x30d051,'call','0x30d070'),(0x30d056,'mov','byte ptr [rdi + 4], al'),(0x30d068,'ret','')
 ]:need(*op)
 if ix[0x30d078]['memory'][0]['rip_target']!='0x22c17b0' or ix[0x30d039]['memory'][0]['rip_target']!='0x22c2158':raise ValueError('pool or wrapper gate identity changed')
 g=G.graph(ix,0x30d070,0x30d155)
 if g['calls'] or g['tails']:raise ValueError('allocator gains opaque admission boundary')
 carriers=[(i['pc'],i['mnemonic'],i['args']) for r in old['ranges'] if r['start']=='0x30d070' for i in r['instructions'] if any(v in i['args'].replace(',', ' ').split() for v in ['r10','r10d','r10w','r10b'])]
 if carriers!=[('0x30d084','movzx','r10d, dx'),('0x30d14f','mov','word ptr [rcx + 0x1c], r10w')]:raise ValueError('incoming action word is used in another operation')
 positive=G.graph(ix,0x30d070,0x30d155,fixed={0x30d094:False,0x30d0af:True,0x30d0c5:True,0x30d0d3:False,0x30d0ec:False,0x30d0fd:False})
 if positive['returns']!=[0x30d154] or not G.dominates(positive,0x30d14f,0x30d154):raise ValueError('valid first free slot does not reach exact action store')
 full=G.graph(ix,0x30d070,0x30d155,fixed={0x30d094:False,0x30d0af:False})
 if full['returns']!=[0x30d0c1] or 0x30d14f in full['visited']:raise ValueError('full pool incorrectly reaches action publication')
 for a in full['visited']:
  if any(m['role'] in ['w','rw'] and m['base']!='rsp' for m in ix[a]['memory']):raise ValueError('full scan writes nonframe object')
 wrapper=G.graph(ix,0x30cfb0,0x30d069)
 if (0x30d051,'0x30d070') not in wrapper['calls'] or not G.dominates(wrapper,0x30d04c,0x30d051) or not G.dominates(wrapper,0x30d051,0x30d056):raise ValueError('wrapper argument/result path changed')
 return dict(allocator='30D070, complete229B. ECX identity copied toR11D; DX zero-extended toR10D. No action-ID use except final WORD store and no native calls.',
  invariant='Scan R8B starts0 and increments1 through31; signed JL after CMP32 stops on32. Each slot is22C17B0+48*i; only WORD(slot+1C)==FFFF selects a free slot. Under stable valid backed array/frame/list globals there is no wrap/NULL scan access.',
  success='First free slotk0..31 receives DWORD1 at+10/+14/+18, originalECX at+20 and incomingDX at+1C. EAX iszero-extendedk. Valid disjoint queue tail/list/frame storage required for intervening linked-list writes.',
  full='If all32 markers differ fromFFFF, returnsALFF; no own nonframe write, no final action-ID store. AL is the relevant return; EAX upper bits are not promised on this arm.',
  wrapper='30CFB0 receives actionWORD inR8W, savesBX, and forwardsEDX=zeroextendBX/ECX=identityESI to30D070; returnedAL becomes unit+4 at30D056. Native WORD store30D14F belongs to30D070, not30CFB0.',
  wrapper_limits='Unit+4!=FF skips acquisition without defining a fresh AL. Bit30 row path may skip while22C2158 bit1 is set; D0..F1 special-state exception is separate. For511..534 WORDdiff303..326>33 reaches that flag gate. Readable stable resolved row and unchanged carriers required; resolver/descriptor/natural command state not proved.',
  candidates='The allocator has no class14/category/action-range exclusion. Given a valid free slot, supplied511..534 are copied unchanged. This settles a local gate, not proof any shipped AI/script supplies those words.',
  sentinel='A suppliedWORDFFFF is also copied, so occupancy marker remainsFFFF despite other initialization/list writes. Original helper has no special input-sentinel refusal. No natural FFFF submission or repeated-allocation/list consequence is claimed.',
  remaining='Upstream command/AI/authored VM producer domains, current descriptor/row identity, initialized pool/list ownership/reuse, normal control/command reachability and wholeOV42 natural rejection stay open.')
def main():
 s=json.loads((P/'capture-01.status.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture-tail.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise ValueError('required suffix capture failed')
 pins=json.loads((P/'retained-identities-01.json').read_text());m=json.loads((P/'retained/manifest.json').read_text());mf={q['path']:q for q in m['members']}
 for q in pins['files']:
  if sha(P/q['path'])!=q['sha256'] or(q['path']!='retained/manifest.json' and mf[q['path'].split('/',1)[1]]['sha256']!=q['sha256']):raise ValueError('committed retained source moved')
  z=json.loads((P/(q['path']+'.git.status.json')).read_text())
  if z.get('terminal') is not True or z.get('exit')!=0 or z.get('exception') is not None or(P/(q['path']+'.git.stderr')).read_bytes() or(P/(q['path']+'.git.stdout')).read_bytes()!=(P/q['path']).read_bytes():raise ValueError('retained Git prerequisite failed')
 old=json.loads((P/'retained/slot-action-id-raw-01.json').read_text());tail=json.loads((P/'source-tail-01.json').read_text())
 if tail.get('wrapper_complete') is not True or tail['invocation_driver_sha256']!=sha(P/'capture-tail.py') or tail['driver_sha256']!=sha(P/'capture-index-path.py'):raise ValueError('actual suffix invocation differs')
 for name,pin in [('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/name)!=pin:raise ValueError('reviewed dependency changed')
 V=load('annotations','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py');annotations=[V.validate(x) for x in [old,tail]]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN or any(x['exe_sha256']!=PIN for x in [old,tail]):raise ValueError('wrong original image')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 expected=[(0x30d070,0x30d155),(0x30cfb0,0x30d056),(0x30d056,0x30d069)]
 ranges=old['ranges']+tail['ranges']
 if [(int(r['start'],16),int(r['end_exclusive'],16)) for r in ranges]!=expected:raise ValueError('missing/truncated/source population differs')
 for r in ranges:
  a,z=int(r['start'],16),int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,z-a):raise ValueError('retained source differs from original EXE')
 facts=derive(old,tail,G);out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise ValueError('immutable result exists')
 result=dict(producer_complete=True,method='A STATIC_ONLY retained original admission/dataflow and finite scan invariant',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=n,sha256=sha(P/n)) for n in ['retained/slot-action-id-raw-01.json','source-tail-01.json']],annotation_prerequisites=annotations,facts=facts,limits=[facts['remaining'],facts['wrapper_limits'],'No original-code execution/emulator/live state. Stable valid disjoint slot/list/frame storage and normal native ABI/returns are premises.'],cleanup='Finite offline source reads, checked children/handles close; no PC/game/save/config/reference/peer mutation.')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED slot admission scans capacity, stores supplied WORD;511..534 not locally excluded; natural producers OPEN')
if __name__=='__main__':main()
