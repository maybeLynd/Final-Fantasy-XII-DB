"""Original cost-helper input widths and conditional special-counter identity.

No callee effect/reachability inference from a normal-return local call graph.
"""
import hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def need(x,m):
 if not x:raise ValueError(m)
def module(n,file):
 s=importlib.util.spec_from_file_location(n,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G):
 ops=[(0x304f2c,'mov','r8d, 1'),(0x304f32,'mov','rdx, r15'),(0x304f35,'mov','rcx, rdi'),(0x304f38,'call','0x305640'),(0x305665,'mov','rbp, rcx'),(0x305668,'mov','r12d, r8d'),(0x30566b,'mov','r14, rdx'),
 (0x305671,'call','0x20e600'),(0x30567f,'mov','r11d, r14d'),(0x305685,'sub','r11d, eax'),(0x305688,'mov','eax, r11d'),(0x30568b,'movzx','r10d, word ptr [r9 + 8]'),(0x305690,'div','r10d'),(0x305693,'mov','edi, eax'),
 (0x305695,'test','rbp, rbp'),(0x305698,'je','0x3056c1'),(0x3056b3,'mov','dword ptr [rbp + 0xe58], r15d'),(0x3056ba,'mov','word ptr [rbp + 0xdc8], ax'),
 (0x3056c1,'movzx','edx, di'),(0x3056c4,'mov','rcx, rbp'),(0x3056c7,'call','0x309110'),(0x3056cc,'movzx','edx, di'),(0x3056cf,'mov','rcx, rbp'),(0x3056d4,'call','0x308ff0'),(0x3056d9,'mov','rcx, qword ptr [rbp + 0x698]'),
 (0x3056e0,'mov','esi, r15d'),(0x305682,'xor','r15d, r15d'),(0x3056e3,'test','r12d, r12d'),(0x3056e8,'setne','sil'),(0x3056ec,'neg','ebx'),(0x3056ee,'mov','edx, ebx'),(0x3056f0,'lea','r8d, [rsi + 0x10]'),(0x3056f4,'call','0x300ce0'),
 (0x3056f9,'mov','rcx, qword ptr [rbp + 0x698]'),(0x305700,'lea','r8d, [rsi + 0x10]'),(0x305704,'movsx','edx, word ptr [rcx + 0x28]'),(0x305708,'imul','edx, edi'),(0x30570b,'neg','edx'),(0x30570d,'call','0x300bc0'),
 (0x305718,'neg','ebx'),(0x30571a,'call','0x253690'),(0x30571f,'lea','edx, [rax + rbx]'),(0x305722,'test','edx, edx'),(0x305724,'cmovns','r15d, edx'),(0x305728,'mov','ecx, r15d'),(0x30572b,'call','0x254ee0'),
 (0x305744,'movzx','ecx, byte ptr [r14 + 0x1e]'),(0x30574d,'sub','ecx, 1'),(0x305750,'je','0x305795'),(0x305752,'sub','ecx, 1'),(0x305755,'je','0x30578e'),(0x305757,'cmp','ecx, 8'),(0x30575a,'jne','0x3057aa'),(0x30575c,'call','0x316440'),
 (0x30576b,'call','0x20e600'),(0x305770,'sub','r14d, eax'),(0x305773,'xor','edx, edx'),(0x30577c,'movzx','ecx, word ptr [rax + 8]'),(0x305780,'mov','eax, r14d'),(0x305783,'div','ecx'),(0x305785,'mov','ecx, 0xd'),(0x30578a,'mov','edx, eax'),(0x30578c,'jmp','0x3057a5'),(0x3057a5,'call','0x253770'),(0x3057c8,'ret','')]
 for pc,m,a in ops:need(pc in ix and(ix[pc]['mnemonic'],ix[pc]['args'])==(m,a),'cost operation changed '+hex(pc))
 need(all(ix[p]['memory'][0]['rip_target']=='0x2ebf138' for p in [0x30565e,0x305676,0x305761,0x305775]),'cost helper action descriptors differ')
 g=G.graph(ix,0x305640,0x3057c9)
 need(g['returns']==[0x3057c8] and all(t.startswith('0x') for _,t in g['calls']),'unclosed/indirect helper boundary')
 need(G.dominates(g,0x305690,0x3056c7) and G.dominates(g,0x305690,0x3056d4),'cost quotient bypass')
 need(G.dominates(g,0x3056e8,0x3056f4) and G.dominates(g,0x3056e8,0x30570d),'mode normalization bypass')
 # Local graph permits normal callee returns. This is not proof of NULL fault
 # or callee safety; the early branch does not skip later own dereferences.
 nullprefix=G.graph(ix,0x305640,0x3057c9,fixed={0x305698:True})
 need(0x3056d9 in nullprefix['visited'] and 0x305704 in nullprefix['visited'],'early null branch bypasses all subsequent reads')
 need(0x3056b3 not in nullprefix['visited'] and 0x3056ba not in nullprefix['visited'],'null prefix reset gating changed')
 counter=G.graph(ix,0x305744,0x3057c9,fixed={0x30574b:False,0x305750:False,0x305755:False,0x30575a:False})
 need(G.dominates(counter,0x305783,0x3057a5) and G.dominates(counter,0x30578a,0x3057a5),'type10 counter quotient transfer bypass')
 supplied_q=65536+208;need((supplied_q&65535)==208 and supplied_q!=208,'width discriminator invalid')
 writes=[dict(pc=hex(pc),args=ix[pc]['args']) for pc in sorted(g['visited']) for m in ix[pc]['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']
 need([x['pc'] for x in writes]==['0x3056b3','0x3056ba'],'unexpected own non-stack store')
 return dict(cost_id='First unsigned32 quotient is latched EDI; both309110 and308FF0 receive zeroextended low16(DI) inEDX, with unitRBP inRCX. Ordinary callee ABI retention required.',counter_id='Under valid unit/stat class0 and original row+1E==10, the helper recomputes unsigned32 quotient after earlier calls and passes fullEAX to253770 EDX withECX13. The two descriptor loads/base reads are independent;316440 return not tested here.',countermodel=dict(first_full_quotient=supplied_q,cost_input_word=208,second_full_quotient=supplied_q,counter_input_dword=supplied_q,executed=False,limits='Supplied mathematical width discriminator, not naturally admitted action or native counter invocation'),mode='Saves entryR8D, normalizes it to0/1 by TEST/SETNE into clearedESI, forwards16+(R8D!=0) to300CE0 and300BC0. Exact caller304F2C supplies1, hence17; all negative/nonzero low32 values also normalize to17, not the raw original flag.',null_limit='Early NULLunit branch skips reset ofE58/DC8 only. After normal earlier callee returns, original code still reads unit+698 and then WORDstats+28. It is not evidence of a NULL-safe whole helper; no observed fault or normalNULL reachability.',own_nonstack_writes=writes,callee_boundaries=[dict(pc=hex(pc),target=t) for pc,t in g['calls']],gil_request='Caller performs low32(oldgil-unitE54) and signed-nonnegative selection via CMOVNS before254EE0. Setter clamp/meter behavior already canonical and is not re-tested here.',binding_implication='Same first/second quotient below65536 makes these ID inputs agree. Prior caller bound<=542/equal binding supplies that only conditionally. No universal identical-ID assumption across narrowed cost inputs and later full counter quotient.',remaining='Opaque cost/stats/gil/achievement/counter callees may have additional effects. No transitive callback/table-writer/lifetime/concurrency exclusion, natural initialized binding or normal action reachability established. This packet replaces the vague helper boundary with exact arguments and remaining callees; does not close wholeOV42.')
def main():
 out=P/sys.argv[1];need(not out.exists(),'immutable output exists')
 for tag,driver in [('extents-01','prepare-extents.py'),('capture-01','capture.py')]:
  s=json.loads((P/(tag+'.status.json')).read_text());need(s.get('terminal') is True and s.get('exit')==0 and s.get('exception') is None and s.get('driver_sha256')==sha(P/driver),'required successful '+tag);need((P/(tag+'.stdout')).read_bytes() and not(P/(tag+'.stderr')).read_bytes(),'required clean nonempty '+tag)
 x=json.loads((P/'lineage.json').read_text());z=subprocess.run(['git','cat-file','blob',x['blob']],capture_output=True,timeout=15);need(z.returncode==0 and not z.stderr and z.stdout==(P/x['copy']).read_bytes() and sha(P/x['copy'])==x['sha256'],'retained caller bytes differ')
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'wrong executable');pe=struct.unpack_from('<I',raw,60)[0];os=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+os+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for _,rva,sz,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+sz:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise ValueError('unbacked original bytes')
 V=module('roles','validate-title-source-annotations.py');G=module('cfg','prove_owner_reload_order.py');ix={};annotations=[];files=['source-01.json','caller-source-01.json']
 for f in files:
  s=json.loads((P/f).read_text());need(s.get('exe_sha256')==PIN,'wrong source image');annotations.append(V.validate(s))
  for r in s['ranges']:
   a,b=int(r['start'],16),int(r['end_exclusive'],16);need(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))==read(a,b-a),'not original bytes');ix.update({int(i['pc'],16):i for i in r['instructions']})
 facts=derive(ix,G)
 with out.open('x')as f:json.dump(dict(producer_complete=True,method='A STATIC_ONLY original instruction dataflow',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_pins=[dict(path=f,sha256=sha(P/f)) for f in files],annotation_prerequisites=annotations,retained_lineage=[x],facts=facts,limits='No native/emulator/live execution. Supplied quotient discriminator is not normal state. Opaque callee effects, actual table consistency and wholeOV42 remain open.',cleanup='No PC/game/instrument/save/config/reference/peer changes. Finite offline children terminal.'),f,indent=2)
 print('PROVED terminal cost inputs low16 versus fresh full32 counter; caller mode17; earlyNULL check notwholehelper safety')
if __name__=='__main__':main()
