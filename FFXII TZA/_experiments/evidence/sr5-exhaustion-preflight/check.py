"""Replay original decoded branches; no emulation or game execution."""
import copy,hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent
def reduce(r):
    assert r['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    code=bytes.fromhex(r['code_hex']);assert len(code)==138 and hashlib.sha256(code).hexdigest()==r['code_sha256']
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    decoded=list(md.disasm(code,0x21b5b0));assert sum(i.size for i in decoded)==138
    assert [{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in decoded]==r['instructions']
    d={i.address:i for i in decoded}
    expected={0x21b5e2:('call','0x212950'),0x21b5e7:('mov','rcx, qword ptr [rbx + 8]'),
      0x21b5eb:('add','rbx, 8'),0x21b5ef:('mov','esi, eax'),0x21b5f1:('cmp','rcx, rbx'),
      0x21b5f4:('je','0x21b621'),0x21b5fa:('cmp','dword ptr [r10 + 0x3c], edi'),
      0x21b5fe:('je','0x21b60a'),0x21b600:('mov','rcx, qword ptr [rcx]'),
      0x21b603:('cmp','rcx, rbx'),0x21b606:('jne','0x21b5f6'),
      0x21b608:('jmp','0x21b621'),0x21b61a:('call','0x224540'),0x21b61f:('mov','eax, esi'),0x21b639:('ret','')}
    for a,v in expected.items():assert (d[a].mnemonic,d[a].op_str)==v,hex(a)
    def path(decisions):
        a=0x21b5e7;visited=[]
        for _ in range(80):
            i=d[a];visited.append(a)
            if i.mnemonic=='ret':return visited
            if i.mnemonic=='jmp':a=int(i.op_str,16)
            elif i.mnemonic in ('je','jne'):
                assert a in decisions,'unspecified branch predicate'
                a=int(i.op_str,16) if decisions[a] else a+i.size
            else:a+=i.size
        raise AssertionError('unbounded CFG witness')
    routes={'empty_after_receipt':path({0x21b5f4:True}),
      'one_nonmatching_node':path({0x21b5f4:False,0x21b5fe:False,0x21b606:False}),
      'first_node_matches':path({0x21b5f4:False,0x21b5fe:True})}
    assert 0x21b608 not in routes['empty_after_receipt'] and 0x21b608 in routes['one_nonmatching_node']
    assert 0x21b61a in routes['first_node_matches'] and all(0x21b621 in p for p in routes.values())
    assert all(0x21b61a not in routes[k] for k in ('empty_after_receipt','one_nonmatching_node'))
    for k in ('empty_after_receipt','one_nonmatching_node'):
        assert all(not(d[a].mnemonic=='mov' and d[a].op_str.split(',')[0] in ('rax','eax','ax','al','ah')) for a in routes[k])
    return {'result':'TRIGGER_COVERAGE_CORRECTION; NO_LIVE_OCCURRENCE_RESULT',
      'receipt_call':'0x212950 at0x21B5E2','proposed_trigger':'0x21b608',
      'static_cfg_witnesses':{k:[hex(a) for a in v] for k,v in routes.items()},
      'trigger_covers':['nonempty exhausted lookup'],'trigger_does_not_cover':['empty list after receipt','matched lookup'],
      'shared_epilogue':'0x21b621 reached by all3; its hit alone cannot distinguish match/miss',
      'additional_candidate':'0x21b5f1 before initial empty comparison: RCX loaded head, RBX controller+8 sentinel, EDI signed block quotient; RCX==RBX is empty-list discriminator. Actual normal callers/identity/control and health remain required.',
      'receipt_limits':'Local code preserves supplied receipt on the two miss paths and restores it after matched callback. Actual receipt producer effects/playback/liveness/ordering are not executed or established here.',
      'limits':'Finite static original-code branch witnesses, not emulator/native traces. External calls opaque. Non-hit cannot prove no sound miss ever occurs. Shared return address alone insufficient.'}
def require_all_misses_trigger(o):
    assert all(o['proposed_trigger'] in o['static_cfg_witnesses'][k] for k in ('empty_after_receipt','one_nonmatching_node'))
def main():
    r=json.loads((HERE/'reference.json').read_text());o=reduce(r)
    (HERE/'observation.json').write_text(json.dumps(o,indent=2)+'\n')
    tests=[]
    def reject(name,f):
        try:f()
        except AssertionError:tests.append({'name':name,'rejected':True})
        else:raise AssertionError('invalid accepted: '+name)
    q=copy.deepcopy(r);q['exe_sha256']='0'*64;reject('wrong binary identity',lambda:reduce(q))
    q=copy.deepcopy(r);b=bytearray.fromhex(q['code_hex']);b[0x21b5f5-0x21b5b0]=0x12;q['code_hex']=b.hex();q['code_sha256']=hashlib.sha256(b).hexdigest()
    # Re-decoded text must independently agree, so mutation changes both data and transcript.
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    q['instructions']=[{'a':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in md.disasm(b,0x21b5b0)]
    reject('empty branch redirected to proposed trigger',lambda:reduce(q))
    q=copy.deepcopy(r);q['instructions'][0]['args']='fake';reject('transcript differs from bytes',lambda:reduce(q))
    reject('one trigger proves every miss',lambda:require_all_misses_trigger(o))
    assert o['proposed_trigger'] in o['static_cfg_witnesses']['one_nonmatching_node']
    receipt={'result':'PASS_STATIC_PREFLIGHT_ONLY','cases':len(tests),'controls':tests,
      'positive':'nonempty one-node miss includes608, matching path includes callback61A, empty path bypasses both',
      'live_semantic_closure':[],'external_call_effects_executed':False}
    (HERE/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS',len(tests),'rejecting controls; trigger608 misses empty branch; NO LIVE OCCURRENCE RESULT')
if __name__=='__main__':main()
