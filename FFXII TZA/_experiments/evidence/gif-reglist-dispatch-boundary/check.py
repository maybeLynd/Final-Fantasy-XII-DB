import hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def derive(s):
 assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 b=s['body'];raw=bytes.fromhex(b['raw_hex']);assert b['entry']=='0x210320' and b['size']==len(raw)==424 and sha(raw)==b['sha256']
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
 ii=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in cs.disasm(raw,0x210320)]
 assert ii==b['instructions'] and sum(len(bytes.fromhex(i['bytes'])) for i in ii)==424
 assert [(f['start'],f['end'],f['flags']) for f in b['fragments']]==[('0x210320','0x21033c',0),('0x21033c','0x2104c1',4),('0x2104c1','0x2104c8',4)]
 for f in b['fragments'][1:]:assert f['chain_parent']==['0x210320','0x21033c','0x1d643d0']
 x={i['pc']:i for i in ii}
 def ins(pc,op,args):assert (x[pc]['op'],x[pc]['args'])==(op,args),(pc,x[pc])
 for pc,op,args in [('0x210329','cmp','byte ptr [rip + 0x1bf2490], 0'),('0x210336','je','0x2104c1'),
  ('0x210390','movups','xmm1, xmmword ptr [r9]'),('0x21039f','shr','rdi, 0xf'),
  ('0x2103a3','and','edx, 0x7fff'),('0x2103a9','and','edi, 1'),('0x2103bb','test','dx, dx'),
  ('0x2103be','je','0x210418'),('0x2103dd','shr','rbx, 0x3a'),('0x2103e7','and','ebx, 3'),
  ('0x210418','add','r9, r15'),('0x21041b','mov','qword ptr [rsp + 0x88], r9'),
  ('0x210423','test','dx, dx'),('0x210426','je','0x210489'),('0x210432','test','bpl, bpl'),
  ('0x210435','je','0x210450'),('0x210437','test','bl, bl'),('0x210439','jne','0x210473'),
  ('0x21043b','call','0x20ec80'),('0x210442','call','0x20fe70'),('0x21044e','jmp','0x210454'),
  ('0x210450','test','bl, bl'),('0x210452','jne','0x210473'),('0x210464','call','0x20f3e0'),
  ('0x210469','mov','r9, qword ptr [rsp + 0x88]'),('0x210471','jmp','0x210489'),
  ('0x210473','cmp','bl, 1'),('0x210476','je','0x2104a0'),('0x210478','lea','eax, [rbx - 2]'),
  ('0x21047b','cmp','al, 1'),('0x21047d','ja','0x210495'),('0x21047f','movzx','eax, dx'),
  ('0x210482','shl','rax, 4'),('0x210486','add','r9, rax'),('0x210489','cmp','dil, 1'),
  ('0x21048d','jne','0x210390'),('0x210493','jmp','0x2104a0'),('0x210495','mov','dword ptr [0], 0'),
  ('0x2104a0','call','0x20ec80'),('0x2104c1','add','rsp, 0x60'),('0x2104c7','ret','')]:ins(pc,op,args)
 assert 0x210330+0x1BF2490==0x1E027C0
 # Exact complete local path after FLG1 match contains completion CALL/epilogue, no EOP test or payload-handler site.
 exit_tail=[i for i in ii if int(i['pc'],16)>=0x2104A0]
 assert [i['pc'] for i in exit_tail if i['op']=='call']==['0x2104a0']
 assert not any(i['op'].startswith('j') for i in exit_tail)
 assert [i['pc'] for i in ii if i['op']=='ret']==['0x2104c7']
 for p in s['refs']:
  d=(HERE/p['retained']).read_bytes();assert len(d)==p['bytes'] and sha(d)==p['sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 witnesses=[
  {'gate':0,'nloop':'unread','flg':'unread','eop':'unread','local_path':'210336->2104C1->RET; no input read/completion call'},
  {'gate':1,'nloop':1,'flg':1,'eop':0,'local_path':'mode check210473/476->completion2104A0->RET; EOP test bypassed'},
  {'gate':1,'nloop':1,'flg':1,'eop':1,'local_path':'same positive REGLIST completion path'},
  {'gate':1,'nloop':0,'flg':1,'eop':0,'local_path':'skip modeparse/handling2103BE/426, cursor+16, EOP0->next header'},
  {'gate':1,'nloop':0,'flg':1,'eop':1,'local_path':'skip modeparse/handling, EOP1->completion'},
  {'gate':1,'nloop':1,'flg':0,'eop':0,'pre':0,'local_path':'calls payloadhandler20F3E0; if it returns, EOP0 reaches next-header loop using returned cursor'},
  {'gate':1,'nloop':1,'flg':2,'eop':0,'local_path':'cursor+16 header/+16 NLOOP skip, EOP0->next header; no local payloadhandler'},
  {'gate':1,'nloop':1,'flg':3,'eop':1,'local_path':'cursor+16 header/+16 NLOOP skip, EOP1->completion; no local payloadhandler'}]
 return {'method':'A — complete original branch/dataflow; witnesses symbolic, not executed',
  'established':['With gate enabled and positive NLOOP, FLG1 goes straight to completion20EC80 and then epilogue. It does not call local PACKED payloadhandler20F3E0 and does not reach the EOP check.',
   'This REGLIST termination happens for EOP0 as well as EOP1; the local dispatcher does not continue into a following tag after that route if completion returns.',
   'Zero-NLOOP tags bypass both modeparse and handling. They advance past16-byte header then use EOP, so an EOP0 zero-loop REGLIST tag is not the same termination case.',
   'PACKED has a payloadhandler path; IMAGE2/3 skip NLOOP*16 before EOP. Universal all-modes replay support is not established by the common sizing formulas.',
   'Enabled dispatcher reads16-byte headers; sharedgate0 returns before input reads or completion call. Sizer gate0 flat16 is a distinct operation.'],
  'branch_witnesses':witnesses,'semantic_implication':'State REGLIST positive-NLOOP local termination separately from sizing and EOP-only traversal. Do not infer universal no-op, absence of authored REGLIST, or no rendering from this local dispatch boundary.',
  'unresolved':['Native completion/payload/register-handler effects and initialized pending state.','Actual authored mode population and ordinary call reachability.','Submission/replay/presentation consequences.'],
  'limits':s['limits'],'affected_consumers':['FABLE legacy VIF/GIF mode traversal/replay §2.1a','OPUS exact GIF input-domain/preconditions'],
  'propagation':'PENDING independent review and owner qualification'}
def main():
 s=json.loads((HERE/'primary.json').read_text());out=derive(s)
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_STATIC_ONLY','complete_original_bytes':424,
  'contiguous_chained_PE_fragments':3,'native_or_guest_or_live_cases':0,
  'controls':'Source NLOOP0/EOP0 continuation, PACKED payloadhandler and IMAGE branch distinguish positiveREGLIST early exit; gate0 entry control. No execution/mutation campaign acceptance.'},indent=2)+'\n')
 print('PASS_STATIC_ONLY: complete chained original REGLIST positive-NLOOP termination, zero-loop and other-mode controls.')
if __name__=='__main__':main()
