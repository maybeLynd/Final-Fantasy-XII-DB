"""Focused prerequisite CLI refusals and full-width access-role regression.

Synthetic decoder/classifier controls are not original FF12 execution.
"""
import ast,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P/'controls-01';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((P/'prove-01.status.json').read_text());v=json.loads((P/'result-01.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'prove.py') or v.get('producer_complete') is not True or v['driver_sha256']!=sha(P/'prove.py'):
    raise RuntimeError('missing checked actual positive')
tree=ast.parse((P/'prove.py').read_text())
outputs=[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='out' and n.func.attr=='write_bytes']
gates=[n.lineno for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Tuple) for t in n.targets) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='checked_capture']
if len(outputs)!=1 or len(gates)!=2 or max(gates)>=outputs[0]:raise RuntimeError('actual capture calls do not precede output')
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='checked_capture')
if not any(isinstance(n,ast.Raise) for n in ast.walk(function)) or not all(t in ast.unparse(function) for t in ["status.get('terminal')","status.get('exit')","status.get('exception')","x.get('wrapper_complete')"]):
    raise RuntimeError('actual checked capture implementation lacks required guards')

# Extract the exact functions used by the checked positive producer, rather
# than introducing a rival memory-role classifier or testing helper existence.
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['write_spans','protected_hits']]
if len(functions)!=2:raise RuntimeError('missing concrete footprint functions')
calls={name:[n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name] for name in ['write_spans','protected_hits']}
if any(not rows or max(rows)>=outputs[0] for rows in calls.values()):raise RuntimeError('footprint classifier not used before output')
ns={};exec(compile(ast.Module(body=functions,type_ignores=[]),'checked-producer-functions','exec'),ns)
spec=importlib.util.spec_from_file_location('reviewed_roles_validator',P/'validate-title-source-annotations.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
if sha(V.ADAPTER)!=V.ADAPTER_SHA:raise RuntimeError('reviewed role adapter changed')
spec=importlib.util.spec_from_file_location('reviewed_roles_adapter',V.ADAPTER);A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
import capstone
from capstone.x86_const import X86_OP_MEM
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
fixtures=[]
for name,blob,role,hit in [
    ('wide-store-crossing-active','0f118378020000','w',True),
    ('address-only-same-start','488d8378020000','addr',False),
    ('read-modify-write-active','838b8402000001','rw',True),
    ('adjacent-store-ends-at-active','c7838002000000000000','w',False)]:
    raw=bytes.fromhex(blob);ins=list(cs.disasm(raw,0x1000))
    if len(ins)!=1 or ins[0].size!=len(raw):raise RuntimeError('invalid bounded decoder control')
    i=ins[0];memory=[]
    for k,o in enumerate(i.operands):
        if o.type!=X86_OP_MEM:continue
        m=o.mem;memory.append({'base':i.reg_name(m.base),'index':i.reg_name(m.index),'scale':m.scale,'displacement':m.disp,'size':o.size,'role':A.op_kind(i,o,k),'rip_target':None})
    rec={'pc':hex(i.address),'bytes':blob,'mnemonic':i.mnemonic,'args':i.op_str,'memory':memory}
    capture={'adapter_sha256':V.ADAPTER_SHA,'capstone':capstone.__version__,'ranges':[{'start':'0x1000','end_exclusive':hex(0x1000+len(raw)),'sha256':hashlib.sha256(raw).hexdigest(),'instructions':[rec]}]}
    validation=V.validate(capture);spans=ns['write_spans']([rec],'rbx');hits=ns['protected_hits'](spans)
    if len(memory)!=1 or memory[0]['role']!=role or bool(hits['active284'])!=hit:raise RuntimeError('width/address/RMW regression '+name)
    fixtures.append({'name':name,'synthetic_capture':capture,'validation':validation,'write_spans':spans,'protected_hits':hits,'expected_active_overlap':hit})
(P/'width-role-controls-01.json').write_bytes((json.dumps({'method':'Synthetic decoder/exact producer function controls, no original-code execution','producer_sha256':sha(P/'prove.py'),'actual_classifier_call_lines':calls,'fixtures':fixtures},indent=2)+'\n').encode())

rows=[]
for name,diag in [('failed-capture','required capture status failed'),
                  ('exception-with-zero-exit','required capture status failed'),
                  ('incomplete-wrapper','actual capture incomplete'),
                  ('missing-helper-source','source-01.json'),
                  ('coherent-index-store-address-mutation','original byte mismatch')]:
    q=D/name;q.mkdir()
    for f in P.iterdir():
        if f.name in ['controls-01','__pycache__','result-01.json'] or f.name.startswith('control-'):continue
        if f.is_dir():shutil.copytree(f,q/f.name)
        else:shutil.copy2(f,q/f.name)
    if name in ['failed-capture','exception-with-zero-exit']:
        f=q/'capture-01.status.json';x=json.loads(f.read_text())
        if name=='failed-capture':x['exit']=1
        else:x['exception']='labelled synthetic captured exception despite exit0'
        f.write_bytes((json.dumps(x)+'\n').encode())
    elif name=='incomplete-wrapper':
        f=q/'source-01.json';x=json.loads(f.read_text());x['wrapper_complete']=False;f.write_bytes((json.dumps(x)+'\n').encode())
    elif name=='missing-helper-source':(q/'source-01.json').unlink()
    else:
        f=q/'source-01.json';x=json.loads(f.read_text());found=0
        for r in x['ranges']:
            for i in r['instructions']:
                if i['pc']=='0x3e5d0f':
                    if i['bytes']!='66428984c1c0040000' or i['args']!='word ptr [rcx + r8*8 + 0x4c0], ax':raise RuntimeError('mutation preimage changed')
                    i['bytes']='66428984c180020000';i['args']='word ptr [rcx + r8*8 + 0x280], ax';i['memory'][0]['displacement']=0x280;found+=1
            r['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))).hexdigest()
        if found!=1:raise RuntimeError('zero/ambiguous mutation')
        f.write_bytes((json.dumps(x,indent=2)+'\n').encode())
    argv=[sys.executable,'-B',str(q/'prove.py'),'refused-result.json']
    receipt={'name':name,'argv':argv,'terminal':False,'exit':None,'exception':None,'driver_sha256':sha(q/'prove.py')}
    try:
        r=subprocess.run(argv,capture_output=True,timeout=25,stdin=subprocess.DEVNULL)
        (q/'stdout.raw').write_bytes(r.stdout);(q/'stderr.raw').write_bytes(r.stderr)
        receipt.update(terminal=True,exit=r.returncode,diagnostic=diag,diagnostic_matched=diag.encode() in r.stderr,refused_result_absent=not(q/'refused-result.json').exists(),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest())
    except Exception as e:
        receipt['exception']=repr(e);(q/'stdout.raw').write_bytes(b'');(q/'stderr.raw').write_bytes(repr(e).encode())
    (q/'receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    if receipt['terminal'] is not True or receipt['exception'] is not None or receipt['exit']==0 or not receipt['diagnostic_matched'] or not receipt['refused_result_absent']:raise RuntimeError('invalid/incomplete refusal '+name)
    rows.append(receipt)
if len(rows)!=5 or len(fixtures)!=4:raise RuntimeError('incomplete/zero controls')
result={'producer_complete':True,'driver_sha256':sha(Path(__file__)),'positive_producer_sha256':sha(P/'prove.py'),
 'source_order_control':{'actual_checked_capture_call_lines':gates,'output_line':outputs[0],'gate_before_output':True},
 'cases':rows,'count':len(rows),'width_role_controls_sha256':sha(P/'width-role-controls-01.json'),
 'limits':'Five actual disposable producer refusals and four synthetic decoder/classifier controls. Checked producer positive is static original-source proof, not native/live execution or independent acceptance.'}
(P/'control-result-01.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('PASS five actual CLI refusals and full-width store/LEA/RMW/adjacency controls; no FF12 execution')
