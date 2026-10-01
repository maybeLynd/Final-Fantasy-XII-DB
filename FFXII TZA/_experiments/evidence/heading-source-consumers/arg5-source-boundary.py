"""Source-only local argument proof; no native/live or whole class verdict."""
import hashlib, json, struct, sys, types
from pathlib import Path
import capstone
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
parent = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
published = Path('Database/FFXII TZA/_experiments/evidence/heading-class-effects-slice')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
pm = {m['path']: m for m in json.loads((parent/'manifest.json').read_bytes())['members']}
cm = {m['path']: m for m in json.loads((published/'manifest.json').read_bytes())['members']}
body = parent/'retained/intervening-body963.bin'; policy = parent/'retained/reg_tracking.py'
assert sha(body) == pm['retained/intervening-body963.bin']['sha256'] and len(body.read_bytes()) == 963
assert sha(policy) == pm['retained/reg_tracking.py']['sha256']
assert sha(published/'raw.json') == cm['raw.json']['sha256']
roles = types.ModuleType('roles'); exec(compile(policy.read_bytes(), str(policy), 'exec'), roles.__dict__)
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); cs.detail = True
ins = list(cs.disasm(body.read_bytes(), 0x2e45e0)); assert sum(i.size for i in ins) == 963 and sum(i.mnemonic=='call' for i in ins) == 21
rows = {i.address:i for i in ins}; zero = 0x2e4735; store = 0x2e474d; call = 0x2e4751
assert (rows[zero].mnemonic,rows[zero].op_str)==('xor','ebx, ebx')
local = [i for i in ins if zero < i.address <= call]
assert [i.address for i in local] == [0x2e4737,0x2e4739,0x2e473b,0x2e4740,0x2e4743,0x2e4748,0x2e474d,0x2e4751]
assert all(a.address+a.size==b.address for a,b in zip([rows[zero]]+local,local))
calls_before = [hex(i.address) for i in local if i.address < call and i.mnemonic=='call']
incoming = []
for i in ins:
    if i.group(capstone.CS_GRP_JUMP):
        assert i.operands[0].type == capstone.CS_OP_IMM, 'Unresolved parent transfer prevents local incoming-edge proof'
        if zero < i.operands[0].imm <= call: incoming.append((hex(i.address),hex(i.operands[0].imm)))
if '--fault-intervening-call' in sys.argv: calls_before.append('LABELLED_ANALYSIS_CALL_AFTER_ZERO')
if '--fault-mid-entry-edge' in sys.argv: incoming.append(('LABELLED_ANALYSIS_PREDECESSOR','0x2e474d'))
assert not calls_before and not incoming, 'Local zero proof cannot swallow an intervening call or mid-entry source edge'
assert all('rbx' not in roles.written(i) for i in local if i.address < call)
assert (rows[store].mnemonic,rows[store].op_str)==('mov','dword ptr [rsp + 0x20], ebx')
assert (rows[call].mnemonic,rows[call].op_str)==('call','0x26afe0')
assert (rows[0x2e4739].mnemonic,rows[0x2e4739].op_str)==('je','0x2e4756'), 'Predicate zero skips this call; do not claim unconditional execution'
raw = json.loads((published/'raw.json').read_bytes()); callee = next(f for f in raw['callees'] if f['entry']=='0x26afe0')
code = (published/callee['code_file']).read_bytes(); assert hashlib.sha256(code).hexdigest()==callee['code_sha256']
ci = list(cs.disasm(code,0x26afe0)); cr={i.address:i for i in ci}
assert (cr[0x26afe0].mnemonic,cr[0x26afe0].op_str)==('push','rbx') and (cr[0x26afe2].mnemonic,cr[0x26afe2].op_str)==('sub','rsp, 0x50')
assert (cr[0x26b014].mnemonic,cr[0x26b014].op_str)==('cmp','dword ptr [rsp + 0x80], 0')
assert 0x80-(8+8+0x50)==0x20
later = [i for i in ins if zero < i.address < 0x2e4924]
assert all('rbx' not in roles.written(i) for i in later)
targets = sorted({i.operands[0].imm for i in later if i.mnemonic=='call'}); assert targets == [0x264460,0x26afe0,0x3a1920,0x3a1d30,0x4686d0]
sources=[]
for a in targets:
    f=next(f for f in raw['callees'] if int(f['entry'],16)==a); bb=(published/f['code_file']).read_bytes(); assert hashlib.sha256(bb).hexdigest()==f['code_sha256']
    ii=list(cs.disasm(bb,a)); sources.append({'entry':hex(a),'extent_status':f['extent_status'],'explicit_RBX_writes':[{'pc':hex(i.address),'instruction':i.mnemonic+' '+i.op_str} for i in ii if 'rbx' in roles.written(i)],'external_jumps':f['external_jumps']})
    if a != 0x26afe0: assert not any('rbx' in roles.written(i) for i in ii)
assert (cr[0x26b0bc].mnemonic,cr[0x26b0bc].op_str)==('pop','rbx') and cr[0x26b0bd].mnemonic=='ret'
# Static PE import identity, not a running IAT target or provider-effects receipt.
sys.path.insert(0,str(parent/'python-deps')); import pefile
exe=Path('Database/Tools/work/exe/FFXII_TZA.exe'); exesha='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'; assert sha(exe)==exesha
pe=pefile.PE(str(exe),fast_load=False); image=exe.read_bytes();base=pe.OPTIONAL_HEADER.ImageBase;assert base==0x120000
off=pe.get_offset_from_rva(0x861f14-base);thunk=image[off:off+6];assert thunk[:2]==b'\xff\x25';slot=0x861f14+6+struct.unpack('<i',thunk[2:])[0]
imports=[{'dll':x.dll.decode(),'name':i.name.decode() if i.name else None,'iat_va':hex(i.address)} for x in pe.DIRECTORY_ENTRY_IMPORT for i in x.imports if i.address==slot]
assert imports==[{'dll':'api-ms-win-crt-math-l1-1-0.dll','name':'sqrtf','iat_va':'0x8c2bb8'}] and sha(exe)==exesha
print(json.dumps({'status':'FIRST_SELECTED_POSITION_CALL_ARG5_ZERO_STATIC','method':'A only; original retained/PE source, no machine-code/live execution','first_call':{'pc':hex(call),'arg5':0,'proof':'local XOR then no CALL/RBX write or internal incoming edge before DWORD stack store','selection':'Predicate nonzero arm only; normal parent entry/return and valid ABI frame, no arbitrary interior intervention'},'second_call':{'pc':'0x2e4928','source_register':'EBX','status':'Conditional on normal native/library ABI preservation and valid frame; not observed actual value','intervening_sources':sources,'declared_math_boundary':{'thunk':'0x861f14','bytes':thunk.hex(),'iat':hex(slot),'imports':imports,'limits':'Static name/slot only; current resolved module/native effects unobserved'}},'class_stability':'OPEN','driver_sha256':sha(Path(__file__)),'reference_sha256':exesha,'tool_identity':{'python':sys.version,'capstone':capstone.__version__,'pefile_path':pefile.__file__,'pefile_sha256':sha(Path(pefile.__file__)),'adapter_sha256':sha(policy)},'limits':'First call zero-argument branch can be analyzed when its callee class gate admits it. Do not prune the second nonzero branch without the stated ABI/state evidence; no class/lifetime/normal gameplay reachability closure.'},indent=2))
