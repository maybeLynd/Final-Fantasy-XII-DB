"""Additive producer qualification for the independently accepted title packet.

The old published checker/result stay immutable. REVIEW 2e88ecee found that an
unwitnessed fast-arm CALL with a rebuilt span hash passed that old checker.
Default execution now redecodes every byte with the reviewed adapter, pins all
seven shipping ranges, derives the complete normal CFG and checks the actual
upstream CLI exit/result before issuing the qualified receipt. No game runs.
"""
import importlib.util,json,pathlib,struct,subprocess,sys

W=pathlib.Path(__file__).resolve().parent
def mod(name,file):
    spec=importlib.util.spec_from_file_location(name,W/file)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=mod('retained_cfg','prove-title-queue-consumption.py')
S=mod('actual_shared_annotations','validate-title-source-annotations.py')
EXPECTED={
 '0x1fb660':('0x1fb6b7','2f91d8a54491defe7bab106b316e8390db3ecd036558497673732786653a5ae6'),
 '0x1fb6b7':('0x1fb6f1','db9a63d121dc966f7191f9154f0a2de03bcbb2294d90a6b1b4892a0fe209832f'),
 '0x1fb6f1':('0x1fb71c','b0e465706655e32682744a927ca6e4df2865126d0cff74392f665dd0a3ac3784'),
 '0x183720':('0x183754','e0f17ce40a9578b288bd13b493abbb45ad62e4e8510b6668703e4d38e5e38211'),
 '0x189120':('0x189128','b02fbb2973e16dbb84c98a083df86088e8bf9ed44f9acb18380d73344cdd193e'),
 '0x17ecc0':('0x17ecdb','4f250822cedaccbe624302de3f7031ad13ae57cd23e368f38558b1e120548876'),
 '0x185a90':('0x185ae6','9ad28a1df654ee9682528401ff7ab9e45b1897a8d29541b399c502786a13ebb5'),
}

def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    intermediate=out.with_name(out.stem+'-retained-producer.json')
    if out.exists() or intermediate.exists():raise ValueError('immutable result exists')
    tools={
      'prove-title-tracker-callback-boundary.py':'43087aae78f87cf254fd786779bd976dfd3e73955fb3e5c8b76bd2100ae0b04e',
      'prove-title-queue-consumption.py':'041769e937b7f8fe03315ee522c77ca7774cd918cb428ef0a2de717b2d99e344',
      'validate-title-source-annotations.py':'7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13',
    }
    for name,sha in tools.items():
        if P.sha(W/name)!=sha:raise ValueError('required producer dependency changed '+name)
    pins=[]
    raw,t=P.load(src,'title-tracker-cleanup-source-01.json',pins)
    qr,q=P.load(src,'title-cleanup-callback-queue-source-01.json',pins)
    annotations=[S.validate(raw),S.validate(qr)]
    ranges=raw['ranges']+qr['ranges']
    if len(ranges)!=len(EXPECTED) or {r['start'] for r in ranges}!=set(EXPECTED):raise ValueError('missing/extra original body')
    for r in ranges:
        if (r['end_exclusive'],r['sha256'])!=EXPECTED[r['start']]:raise ValueError('original full body identity changed '+r['start'])
    entries=[[0x1fb660,0x1fb6b7,0x1da8448],[0x1fb6b7,0x1fb6f1,0x1d60c28],[0x1fb6f1,0x1fb71c,0x1d60c3c],[0x183720,0x183754,0x1d53f68]]
    if raw.get('pdata_entries')!=entries:raise ValueError('normal root/fragment metadata changed')
    chains=raw.get('verified_unwind_chains',[])
    if len(chains)!=2:raise ValueError('missing chained fragments')
    for record,entry,header in zip(chains,entries[1:3],['21050200','21000000']):
        z=bytes.fromhex(record['raw_unwind']);at=(4+2*z[2]+3)&~3
        root=[v+0x120000 for v in struct.unpack_from('<III',z,at)]
        if z[:4].hex()!=header or z[0]>>3!=4 or record['fragment']!=entry or record['root']!=entries[0] or root!=entries[0]:raise ValueError('unwind chain/root changed')
    gt=P.closed(t,0x1fb660,0x1fb71c)
    derived=dict(entry=gt['entry'],end_exclusive=gt['end_exclusive'],reachable_instructions=gt['instructions'],returns=gt['returns'],opaque_calls=gt['calls'])
    if raw.get('normal_cfg')!=derived:raise ValueError('recorded CFG differs from computed original CFG')
    gc=P.closed(t,0x183720,0x183754);gg=P.closed(q,0x189120,0x189128);gq=P.closed(q,0x185a90,0x185ae6)
    if gq['calls']!=[dict(pc='0x185adc',target='0x1858a0')] or gq['returns']!=['0x185ad6','0x185ae5']:raise ValueError('queue call/return boundaries changed')
    # Choose the unsigned write<end arm at185ABB; preserve both NULL/nonNULL
    # cursor subbranches. Every reached instruction is byte-qualified above.
    todo=[0x185abd];fast=set();fast_returns=[]
    while todo:
        pc=todo.pop()
        if pc in fast:continue
        if pc not in q or not 0x185abd<=pc<0x185ae6 or pc in (0x185ad7,0x185adc):raise ValueError('fast branch escapes its qualified boundary')
        fast.add(pc);i=q[pc];n=pc+len(bytes.fromhex(i['bytes']))
        if i['mnemonic']=='call':raise ValueError('fast branch contains a call')
        if i['mnemonic']=='ret':fast_returns.append(hex(pc));continue
        if i['mnemonic'].startswith('j'):
            todo.append(int(i['args'],16))
            if i['mnemonic']=='jmp':continue
        todo.append(n)
    if sorted(fast_returns)!=['0x185ad6','0x185ae5']:raise ValueError('fast branch return coverage changed')
    # This callback terminates in an external tail. Keep that boundary opaque.
    callback=[i for r in qr['ranges'] if r['start']=='0x17ecc0' for i in r['instructions']]
    if len(callback)!=8 or callback[-1]['pc']!='0x17ecd6' or callback[-1]['mnemonic']!='jmp' or callback[-1]['args']!='0x19c590':raise ValueError('callback tail boundary changed')
    if any(i['mnemonic'].startswith('j') or i['mnemonic']=='ret' for i in callback[:-1]):raise ValueError('unchecked callback branch')
    command=[sys.executable,'-B',str(W/'prove-title-tracker-callback-boundary.py'),str(intermediate),str(src)]
    run=subprocess.run(command,capture_output=True,text=True,timeout=60)
    execution=dict(command=command,exit=run.returncode,stdout=run.stdout,stderr=run.stderr,result_present=intermediate.is_file())
    if run.returncode!=0 or not intermediate.is_file():raise ValueError('required retained producer failed '+json.dumps(execution))
    r=json.loads(intermediate.read_text())
    if r.get('producer_complete') is not True or r.get('source_pins')!=pins or r.get('checker_sha256')!=tools['prove-title-tracker-callback-boundary.py']:raise ValueError('retained producer result prerequisite failed')
    execution['result_sha256']=P.sha(intermediate)
    r.update(status='PRODUCER_CHECKED_FULL_BYTE_CFG_QUALIFICATION_INDEPENDENT_PENDING',
      checker_sha256=P.sha(pathlib.Path(__file__)),retained_checker_sha256=tools['prove-title-tracker-callback-boundary.py'],
      qualification_question='Does the actual producer reject an unwitnessed fast-path call and forged CFG instead of trusting self-rehashed ranges/recorded metadata?',
      annotation_prerequisites=annotations,computed_normal_cfgs=[gt,gc,gg,gq],
      fast_branch=dict(condition='unsigned old writecursor<end',instructions=sorted(hex(p) for p in fast),returns=sorted(fast_returns),calls=[]),
      prerequisite_execution=execution,tool_pins=tools,
      qualification='Additive producer repair for review2e88ecee. Original facts independently ACCEPTED; old gate incompleteness is not evidence that original shipping facts were false. No new semantic closure, live/harness run or reviewer-test credit.',
      consumer_action='Use this02 qualification CLI/result for future producer validation; preserve original01/checker and independent review. Existing FABLE semantic adoption remains on its original route.')
    out.open('x',encoding='utf-8').write(json.dumps(r,indent=2)+'\n')
    print('Full byte/annotation/CFG qualification and checked upstream CLI: PASS; original semantic scope unchanged')

if __name__=='__main__':main()
