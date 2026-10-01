"""A bounded caller/source proof; opaque returning calls use an explicit ABI assumption."""
import csv,datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking
ok,detail=team.board_status(team.BOARD);assert ok,detail
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-APPROACH-ANGLE-DIVISOR-DOMAIN')
assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'result.json').exists()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('reader',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd)
image,ss=rd.load_image()
assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
entry=0x339630;size=1061;target=0x339880;load=0x339723
raw=rd.img_rd(image,ss,entry,size)
assert sha(raw)=='8a75e847cb7520bb1e19c64607ac094482fb0ad6ba8c825c7a8f8c363478d1f6'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ii={i.address:i for i in cs.disasm(raw,entry)}
assert sum(i.size for i in ii.values())==size and ii[entry+size-1].mnemonic=='ret'
for pc,h in {0x33971A:'440f298c2420010000',load:'f3440f100d0c9a5b00',0x339735:'f3440f101512259b01',0x339871:'6bc35a',0x339874:'660f6ec0',0x339878:'0f5bc0',0x33987B:'f3410f59c2',target:'f3410f5ec1',0x339885:'e8e6320000',0x339958:'0f8c23feffff',0x339A02:'440f288c2420010000'}.items():
    assert ii[pc].bytes.hex()==h,(hex(pc),'original binding')
assert ii[target].op_str=='xmm0, xmm9' and ii[0x339885].operands[0].imm==0x33CB70
assert ii[0x339735].op_str.startswith('xmm10,')

# Direct bounded caller graph only. No callee traversal or computed-control guesses.
edges={};calls=[]
for pc,i in ii.items():
    nxt=pc+i.size
    if i.mnemonic=='ret':dest=[]
    elif i.mnemonic.startswith('j'):
        assert i.operands[0].type==capstone.CS_OP_IMM
        dest=[i.operands[0].imm] if i.mnemonic=='jmp' else [nxt,i.operands[0].imm]
    else:
        dest=[nxt]
        if i.mnemonic=='call':
            assert i.operands[0].type==capstone.CS_OP_IMM
            calls.append(dict(pc=hex(pc),target=hex(i.operands[0].imm),limits='Opaque conformingly returning call; XMM9/10 preserved by assumed ABI, not tested native effects'))
    assert all(d in ii for d in dest),(hex(pc),dest)
    edges[pc]=dest

def reachable(blocked=()):
    todo=[entry];seen=set()
    while todo:
        pc=todo.pop()
        if pc in seen or pc in blocked:continue
        seen.add(pc);todo.extend(edges[pc])
    return seen

seen=reachable()
assert target in seen and target not in reachable((load,))
assert target in reachable((0x339A02,)) # epilogue restore is not the reaching definition
write9=[pc for pc,i in ii.items() if 'xmm9' in reg_tracking.written(i)]
write10=[pc for pc,i in ii.items() if 'xmm10' in reg_tracking.written(i)]
assert write9==[load,0x339A02] and write10==[0x339735,0x3399F9]
assert target not in reachable((0x339735,))
assert ii[0x339958].operands[0].imm==0x339781 # loop stays after the definitions
focused=[]
for pc in (0x33971A,load,0x339735,0x339A02):
    i=ii[pc]
    for k,o in enumerate(i.operands):
        if o.type==capstone.CS_OP_MEM:
            kind=reg_tracking.op_kind(i,o,k)
            assert kind in ('r','w')
            focused.append(dict(pc=hex(pc),operand=k,kind=kind,width=o.size,base=i.reg_name(o.mem.base),disp=o.mem.disp))
assert [x['kind'] for x in focused]==['w','r','r','r']
pe=struct.unpack_from('<I',image,0x3C)[0];nsec=struct.unpack_from('<H',image,pe+6)[0];optsz=struct.unpack_from('<H',image,pe+20)[0]
def section(va):
    rva=va-0x120000
    for j in range(nsec):
        p=pe+24+optsz+j*40;vs,sva,rs,ra=struct.unpack_from('<IIII',image,p+8)
        if sva<=rva<sva+max(vs,rs):
            flags=struct.unpack_from('<I',image,p+36)[0]
            return dict(name=image[p:p+8].rstrip(b'\0').decode(),rva=hex(sva),virtual_bytes=vs,raw_bytes=rs,characteristics=f'{flags:08X}',write_flag=bool(flags&0x80000000))
    raise AssertionError(hex(va))
constants=[]
for pc,want,h in [(load,0x8F3138,'00003443'),(0x339735,0x1CEBC50,'db0f4940')]:
    i=ii[pc];assert i.operands[1].mem.base==capstone.x86.X86_REG_RIP and i.operands[1].size==4
    addr=pc+i.size+i.operands[1].mem.disp;assert addr==want
    data=rd.img_rd(image,ss,addr,4);assert data.hex()==h
    constants.append(dict(load=hex(pc),address=hex(addr),bytes_hex=data.hex(),f32=struct.unpack('<f',data)[0],section=section(addr),limits='Shipping image bytes, unchanged-reference-memory precondition. Not live value/lifetime proof'))
assert constants[0]['f32']==180.0 and 3<constants[1]['f32']<4
mut=bytearray(raw);mut[load-entry+4]=0x05 # XMM9 -> XMM8, same RIP/load width
mi={i.address:i for i in cs.disasm(mut,entry)}
assert len(mi)==len(ii) and mi[load].op_str.startswith('xmm8,') and mi[load].size==ii[load].size
assert mi[load].address+mi[load].size+mi[load].operands[1].mem.disp==0x8F3138
mutwrites=[pc for pc,i in mi.items() if 'xmm9' in reg_tracking.written(i)]
assert mutwrites==[0x339A02] and target in reachable((0x339A02,))
assert sha(mut)!=sha(raw)
R=W/'retained';R.mkdir(exist_ok=False)
for name,data in [('source.bin',raw),('degrees.bin',bytes.fromhex('00003443')),('pi.bin',bytes.fromhex('db0f4940')),('shipping-reader.py',rp.read_bytes()),('reg_tracking.py',Path(reg_tracking.__file__).read_bytes())]:
    (R/name).write_bytes(data)
cp=Path('Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md');cb=cp.read_bytes();(R/'maths-preimage.md').write_bytes(cb)
assert '00339880' in cb.decode() and '`divss` is the only shape that can grow without bound' in cb.decode()
fp=Path('Database/Tools/work/graph/functions.tsv');fb=fp.read_bytes();row=next(r for r in csv.DictReader(fb.decode().splitlines(),delimiter='\t') if r['entry']=='00339630');assert row['body_bytes']=='1061'
(R/'catalog-identity.json').write_text(json.dumps(dict(path=fp.as_posix(),sha256=sha(fb),row=row,limits='Bounded catalog span, not .pdata/logical-body certification'),indent=2)+'\n')
abi=dict(source='https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170',section='Caller/callee saved registers',assumption='Returning calls preserve low128 XMM6-XMM15 including XMM9/10. Standard ABI requirement read from primary Microsoft source, not proof every actual callee/session conforms. No YMM upper-lane preservation inferred.')
dll=Path(capstone._cs._name)
result=dict(question='Variable/near-zero register divisor versus literal180 conversion in approach-angle caller',method='A exact1061B bounded caller source/directgraph + originalconstants + explicit nonvolatileABI assumption; zero original/native/emulator/live executions',
    reference=dict(exe_sha256=sha(image),entry=hex(entry),bytes=size,body_sha256=sha(raw),reader_sha256=sha(rp.read_bytes()),policy_sha256=sha(Path(reg_tracking.__file__).read_bytes())),
    tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),sha256=sha(dll.read_bytes()))),driver_sha256=sha(Path(__file__).read_bytes()),abi=abi,
    instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()],edges={hex(pc):[hex(x) for x in dest] for pc,dest in edges.items()},calls=calls,
    local_flow=dict(target=hex(target),definition=hex(load),target_reachable=True,target_reachable_without_definition=False,target_reachable_without_epilogue_restore=True,xmm9_writes=[hex(x) for x in write9],xmm10_writes=[hex(x) for x in write10],loopback='0x339958->0x339781',limits='All direct conditional outcomes in bounded source; normalentry assumed, opaque calls return conformingly. Not actual game trigger/caller trace/completecallee proof'),
    focused_memory_roles=focused,constants=constants,
    mutation_control=dict(name='Private source constant-load destination XMM9-to-XMM8',offset=load-entry+4,original_byte=raw[load-entry+4],mutant_byte=mut[load-entry+4],mutant_body_sha256=sha(mut),xmm9_writes=[hex(x) for x in mutwrites],constant_reaching_definition_missing=True,original_body_binding_rejected=True,limits='Decode/role/source mutation only; no altered machine instructions executed or originalhashguard bypass'),
    interpretation='XMM9 is literal180 from shippingreference not unknownregister divisor, under unchangedconstants/conforming-returningcallees. Preserve sourceorder: IMULEAX,EBX,90 low32; MOVDXMM0,EAX; CVTDQ2PS signed32; MULSSXMM0,XMM10(pi); DIVSSXMM0,XMM9(180); CALL33CB70. Variable-denominator/nearzero/unbounded-growth rationale refuted for thissite, not allfastpathreachability.',
    coarse_bound='Under completed standardISA operations/conformingcallee/unchangedfinitepi<4 and180>1, degree originates signed32 so absCVTDQ2PS<=2^31; multiply has finite coarsebound2^33 and division cannot exceed that coarsebound. No realnumber rewrite or bitexact quotient claimed. This weak finitebound does not establish angle<=4pi or exclude fastpath.',
    consumer=dict(path=cp.as_posix(),sha256=sha(cb),retained_name='maths-preimage.md',change='Correct specific00339880 registerdivisor/unbounded-growth residue rationale; retain40 unresolvedoperand producers and actualCRT/FP/input/normalreachability questions, do not close53-site question'),
    limits='No original/native/emulator/live, acosf/callee semantics, nativeMXCSR/rounding/exceptions, bitexactconversion, actualinputrange or observedfastpath, wholelogicalfunction .pdata extent, all53callers, scheduler, ownership or combatconsequence proved. ABIassumption does not certifycallees; intervention/exceptional/nonconforming execution outofsourceproof. Source/model/manifestchecks are not independentacceptance.',
    cleanup='PC OFF/no game/input/instruments/process/save/config/reference/peerwrites. Onlyreadonlysource/consumerpreimage and Python boundedgraph/control calculations; owner/reviewer incorporation pending.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('Derived fixed180 approach divisor dominates339880 under explicitreturningcalleeABI; sourceonly, no actualangle/fastpath proof',flush=True)
