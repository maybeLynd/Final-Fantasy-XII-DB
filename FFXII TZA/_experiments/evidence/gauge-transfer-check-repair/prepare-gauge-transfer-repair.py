"""Build an additive successor from the pinned reviewed producer, never edit it."""
import hashlib
from pathlib import Path
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
OLD = ROOT/'Database/FFXII TZA/_experiments/evidence/ov42-gauge-callback-binding/prove.py'
D = W/'gauge-transfer-check-repair'
D.mkdir()
raw = OLD.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '91033a449df208020e106e9fe64629736075f4afa6c643e4414f5c674fd4435a'
(D/'producer-v1.preimage.py').write_bytes(raw)
s = OLD.read_text()
def replace(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
replace('P=Path(__file__).resolve().parent', "OUT=Path(__file__).resolve().parent\nP=next(p for p in OUT.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())/'Database/FFXII TZA/_experiments/evidence/ov42-gauge-callback-binding'")
replace('def derive(ix):', '''def checked_transfers(rows, start, end, allowed_calls, *, internal_branches=True):
    """Check all local calls and branches; indirect or unproved exits fail closed."""
    pcs={int(i['pc'],16) for i in rows}
    seen=[];calls=[]
    for i in rows:
        m=i['mnemonic']
        if not(m.startswith('call') or m.startswith('j') or m in ('loop','loope','loopne')):continue
        try:target=int(i['args'],0)
        except (TypeError,ValueError):raise ValueError('unproved indirect transfer '+i['pc'])
        row=dict(pc=i['pc'],mnemonic=m,target=hex(target))
        seen.append(row)
        if m.startswith('call'):
            calls.append((i['pc'],hex(target)))
            need((i['pc'],hex(target)) in allowed_calls,'unexpected direct call '+i['pc'])
        else:
            need(internal_branches and start<=target<end and target in pcs,'unproved branch exit or target '+i['pc'])
    need(calls==allowed_calls,'complete direct call set changed')
    return seen

def derive(ix):''')
replace("need(not any(i['mnemonic'].startswith('call') for i in tail),'matching-row tail unexpectedly calls initializer')", "tail_transfers=checked_transfers(tail,0x297ce2,0x297d04,[],internal_branches=False)")
replace("need(calls==[('0x297414','0x271960'),('0x297430','0x272730'),('0x297450','0x2726c0'),('0x297498','0x2727c0')],'complete consumer call set changed')", "consumer_transfers=checked_transfers(consumer,0x2973e0,0x2974d7,[('0x297414','0x271960'),('0x297430','0x272730'),('0x297450','0x2726c0'),('0x297498','0x2727c0')])")
replace('direct_calls=calls,own_consumer_writes=own,', 'direct_calls=calls,local_transfer_checks=dict(consumer=consumer_transfers,matched_tail=tail_transfers),own_consumer_writes=own,')
replace("out=P/sys.argv[1];need(not out.exists(),'fresh output required')", "out=OUT/sys.argv[1];need(not out.exists(),'fresh output required')\n    manifest=P/'manifest.json'\n    need(sha(manifest)=='03ce4f39f2222feb7b1d3671b13fd03c86cdca9df1f79daf1f8cc07aa7116d0e','reviewed predecessor manifest changed')\n    members=json.loads(manifest.read_text())['members']\n    need(len(members)==65,'reviewed predecessor member count changed')\n    for x in members:\n        f=P/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'reviewed predecessor member changed '+x['path'])")
start=s.index('    for label,pc,key,value in [')
end=s.index("    with out.open('x')",start)
s=s[:start]+'''    tests=[
      ('secondary-handler-memory-identity',0x2963e7,'memory','rip_target','0x29b7d0','actual LEA callback identity changed'),
      ('callback-store-memory-offset',0x3f89f4,'memory','displacement',0x40,'actual callback store role/layout changed'),
      ('consumer-tail-to-handler',0x297435,'row','args','0x29b7d0','unproved branch exit or target'),
      ('consumer-indirect-jump',0x297435,'row','args','rax','unproved indirect transfer'),
      ('matched-tail-to-initializer',0x297cfe,'jump','args','0x3f89c0','unproved branch exit or target')]
    for case_id,pc,kind,key,value,marker in tests:
        z=copy.deepcopy(ix)
        if kind=='memory':z[pc]['memory'][0][key]=value
        else:
            z[pc][key]=value
            if kind=='jump':z[pc]['mnemonic']='jmp'
        try:derive(z)
        except ValueError as e:
            need(marker in str(e),'wrong detector for '+case_id+': '+str(e))
            controls.append(dict(id=case_id,pc=hex(pc),mutation=dict(kind=kind,key=key,value=value),refused=str(e),method='Synthetic source-record mutation, not original execution'))
        else:raise ValueError('source control accepted '+case_id)
''' + s[end:]
replace("driver_sha256=sha(Path(__file__)),exe_sha256=PIN,", "driver_sha256=sha(Path(__file__)),predecessor_driver_sha256=sha(P/'prove.py'),review_commit='95d495604a3994a0fe0078e4b0620a168c9137b7',input_manifest_sha256=sha(manifest),exe_sha256=PIN,")
replace("print('PROVED conditional prescribed handlers, existing-row no-reinitialize, exact local consumer call/write boundary; transitive/live state OPEN')", "print('PROVED retained local facts with all call/jump/conditional transfer checks; five targeted synthetic counterexamples refused; no new native/live observations')")
compile(s,str(D/'prove-transfers-v2.py'),'exec')
(D/'prove-transfers-v2.py').write_text(s)
(D/'QUESTION.md').write_text('Question: does the actual callback-boundary producer reject jump-form exits and semantic-only operand changes identified in independent review95d495604? MethodA retained original822B, no recapture/execution. Shipping facts remain independently accepted; producer-v1 is insufficient alone for transfer absence under changed records. Preserve all original65 committed members. Successor must accept the same valid inputs, reject the three previously missed transfers using the transfer detector, reject two memory-only changes using semantic detectors, and keep full initialization/lifetime/scheduling/presentation/transitive effects OPEN. No current-value or natural-reachability conclusion.\n')
print(D)
print('successor',hashlib.sha256((D/'prove-transfers-v2.py').read_bytes()).hexdigest())
