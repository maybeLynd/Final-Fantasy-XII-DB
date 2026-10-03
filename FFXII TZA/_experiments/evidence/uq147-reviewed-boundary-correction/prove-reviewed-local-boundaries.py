"""Additive response to SPEC: caller effects and checked lookup calls.

Original published sources/producers/results remain immutable. This current
invocation consumes them with the shared byte/role validator, and rejects an
unsuccessful prerequisite before producing any result.
"""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
W = P.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise ValueError(message)

def derive(source):
    ranges = {r['start']: r for r in source['ranges']}
    need(set(ranges) == {'0x317e60', '0x25aad0'}, 'complete two-body domain changed')
    caller = ranges['0x317e60']['instructions']
    ix = {int(i['pc'], 16): i for i in caller}
    expected = [
        (0x317e60, 'sub', 'rsp, 0x28'), (0x317e64, 'call', '0x3590d0'),
        (0x317e69, 'test', 'byte ptr [rip + 0x1d714d0], 0x10'),
        (0x317e70, 'je', '0x317ea9'), (0x317e72, 'mov', 'ecx, eax'),
        (0x317e74, 'call', '0x3588b0'), (0x317e79, 'test', 'rax, rax'),
        (0x317e7c, 'je', '0x317ea9'), (0x317e7e, 'mov', 'rcx, rax'),
        (0x317e81, 'call', '0x263e30'), (0x317e86, 'test', 'rax, rax'),
        (0x317e89, 'je', '0x317ea9'), (0x317e8b, 'test', 'byte ptr [rax], 8'),
        (0x317e8e, 'je', '0x317ea9'), (0x317e90, 'movabs', 'rcx, 0x100000000'),
        (0x317e9a, 'or', 'qword ptr [rax], rcx'),
        (0x317e9d, 'lea', 'rcx, [rax + 0x80]'), (0x317ea4, 'call', '0x33c9b0'),
        (0x317ea9, 'xor', 'edx, edx'), (0x317eab, 'lea', 'ecx, [rdx + 1]'),
        (0x317eae, 'add', 'rsp, 0x28'), (0x317eb2, 'jmp', '0x25aad0')]
    need([(int(i['pc'],16), i['mnemonic'], i['args']) for i in caller] == expected,
         'caller instruction/branch/mask domain changed')
    def memory(pc, base, displacement, size, role, target=None):
        m = ix[pc]['memory']
        need(len(m) == 1 and
             (m[0]['base'], m[0]['index'], m[0]['displacement'], m[0]['size'], m[0]['role'], m[0]['rip_target']) ==
             (base, None, displacement, size, role, target), 'caller memory effect/identity changed')
    memory(0x317e69, 'rip', 30872784, 1, 'r', '0x2089340')
    memory(0x317e8b, 'rax', 0, 1, 'r')
    memory(0x317e9a, 'rax', 0, 8, 'rw')
    memory(0x317e9d, 'rax', 0x80, 8, 'addr')
    writes = [dict(pc=i['pc'], memory=m) for i in caller for m in i['memory']
              if m['role'] in ('w','rw') and m['base'] != 'rsp']
    need([i['pc'] for i in writes] == ['0x317e9a'], 'caller persistent-write census changed')
    tail = {int(i['pc'],16): i for i in ranges['0x25aad0']['instructions']}
    for pc, mnemonic, args in [(0x25aad6,'mov','ebx, ecx'), (0x25aad8,'mov','ecx, edx'),
                               (0x25aada,'call','0x3588b0'), (0x25aadf,'test','ebx, ebx'),
                               (0x25aae1,'jne','0x25ab1c')]:
        need(pc in tail and (tail[pc]['mnemonic'], tail[pc]['args']) == (mnemonic,args),
             'notification argument leg changed')
    writes_excluded = [i['pc'] for i in tail.values() for m in i['memory']
                       if m['role'] in ('w','rw') and m['base'] != 'rsp']
    need(writes_excluded == ['0x25aaf2','0x25aaf8','0x25ab00','0x25ab06','0x25ab15'],
         'notification persistent-write census changed')
    return dict(caller_own_writes=writes, notification_writes_excluded=writes_excluded,
        caller_gates=['byte[02089340]&0x10', '3588B0 result non-NULL',
                      '263E30 result non-NULL', 'unit byte+0 bit3 set'],
        caller_effect='Conditional own QWORD flag32 RMW at317E9A precedes33C9B0(unit+80) and the(1,0) notification tail; neither is excluded.',
        scope='Only25AAD0 publication block/2F1710 excluded on this leg. Earlier calls and conditional unit write persist; opaque helper effects, natural admission, lifetime and mode preservation OPEN.')

def lookup_calls(source):
    body = next(r for r in source['ranges'] if r['start'] == '0x31b770')
    calls = [(i['pc'],i['mnemonic'],i['args']) for i in body['instructions']
             if i['mnemonic'] in ('call','jmp')]
    need(calls == [('0x31b79c','call','0x236850'), ('0x31b7a7','call','0x236820'),
                   ('0x31b7bc','call','0x236850')], 'lookup helper transfer identity changed')
    return calls

def main():
    output = P/sys.argv[1]
    need(not output.exists(), 'fresh output required')
    qualifier = P/(sys.argv[2] if len(sys.argv)>2 else 'capture-request-tail-01.status.json')
    st = json.loads(qualifier.read_text())
    need(st.get('terminal') is True and st.get('exit') == 0 and st.get('exception') is None,
         'successful prerequisite required')
    specs = [('source-request-tail-01.json', '7536b76bfaabfee9319268822c1463df39550d0516f17f22c580ea14e4889454',
              'capture-request-tail.py', 'capture-request-tail-01.status.json',
              '89796185513456c9faffc1bea6cfe1f6aaaf492eab7215fd9c7114d4a9f497e1'),
             ('source-defeat-boundary-01.json', 'a4febab7a65d9eb7e3b27524ca69f6906b80715e6291c946a03fd39ab27afb95',
              'capture-defeat-boundary.py', 'capture-defeat-boundary-01.status.json',
              'e318100b6f9582028bbdd4206d4c8643f351b270841b3a8a924d070b824be784')]
    validator = W/'validate-title-source-annotations.py'
    need(sha(validator) == '7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13',
         'reviewed validator changed')
    spec = importlib.util.spec_from_file_location('reviewed_annotations', validator)
    v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
    sources, agreement = [], []
    for name,pin,driver,status,dpin in specs:
        path = P/name; need(sha(path) == pin, 'retained source changed')
        st = json.loads((P/status).read_text())
        need(st.get('terminal') is True and st.get('exit') == 0 and st.get('exception') is None
             and st.get('driver_sha256') == dpin == sha(P/driver), 'exact successful capture required')
        s = json.loads(path.read_text())
        need(s.get('wrapper_complete') is True and s.get('invocation_driver_sha256') == dpin and
             s.get('exe_sha256') == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8',
             'complete exact original-code binding required')
        agreement.append(v.validate(s)); sources.append(s)
    facts = derive(sources[0]); calls = lookup_calls(sources[1]); controls = []
    for name,pc,field,value,marker in [
        ('caller-store-role-omitted','0x317e9a','role','r','caller memory effect/identity changed'),
        ('caller-store-offset-changed','0x317e9a','displacement',8,'caller memory effect/identity changed'),
        ('caller-mask-changed','0x317e90','args','rcx, 0x200000000','caller instruction/branch/mask domain changed'),
        ('extra-caller-store','0x317e8b','role','rw','caller memory effect/identity changed')]:
        changed = copy.deepcopy(sources[0])
        inst = next(i for r in changed['ranges'] for i in r['instructions'] if i['pc']==pc)
        if field == 'args': inst[field]=value
        else: inst['memory'][0][field]=value
        try: derive(changed)
        except ValueError as e:
            need(marker in str(e), 'wrong control refusal'); controls.append(dict(id=name,refused=str(e)))
        else: raise ValueError('counterexample accepted '+name)
    changed = copy.deepcopy(sources[1])
    next(i for r in changed['ranges'] for i in r['instructions'] if i['pc']=='0x31b7a7')['args']='0x263750'
    try: lookup_calls(changed)
    except ValueError as e:
        need('lookup helper transfer identity changed' in str(e), 'wrong lookup refusal')
        controls.append(dict(id='lookup-helper-redirected',refused=str(e)))
    else: raise ValueError('lookup counterexample accepted')
    result = dict(producer_complete=True, driver_sha256=sha(Path(__file__)),
        method='A retained shipping bytes + additive source-record controls; no original instruction execution',
        sources=[dict(path=name,sha256=pin) for name,pin,*_ in specs],
        reviewed_adapter_agreement=agreement, facts=facts, checked_lookup_calls=calls,
        controls=controls, control_limits='Synthetic labelled record mutants, not coherent byte/native mutants.',
        accepted_scope='SPEC original verdict ACCEPT-WITH-NARROWING; this producer repair independently pending.',
        unresolved='Natural KO/Esper113, opaque helpers, ownership/lifetime, scheduling/presentation/fullUQ147 OPEN.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('Caller flag32 write/callback retained; notification exclusion narrowed; lookup helper calls checked. Five focused controls refused.')

if __name__ == '__main__': main()
