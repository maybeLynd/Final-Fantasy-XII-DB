"""Bounded static effect closure and retained EXP091 setup discrepancy; no emulation."""
import ast, copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def index(r):return {int(i['pc'],16):i for i in r['instructions']}
def expect(a,pc,m,args):need(pc in a and (a[pc]['mnemonic'],a[pc]['args'])==(m,args),'specific dataflow changed '+hex(pc))

def derive(s):
    rs={int(r['start'],16):r for r in s['ranges']}
    expected={0x2fead0:53,0x30c0e0:78,0x236820:12,0x236850:2,0x31b7e0:12,0x20e600:3,0x3588b0:46,0x263ff0:5,0x263e30:2,0x377c20:23,0x3148f0:8,0x2ef2b0:5,0x2ef640:2}
    need(set(rs)==set(expected),'missing/extra closure body')
    edges=[];graphs=[];writes=[]
    for entry,r in rs.items():
        a=index(r);need(len(a)==expected[entry],'incomplete instruction domain')
        succ={}
        for pc,i in a.items():
            m=i['mnemonic'];nxt=pc+len(bytes.fromhex(i['bytes']))
            if m=='call':
                need(i['args'].startswith('0x'),'unknown callee')
                target=int(i['args'],16);need(target in rs,'unknown callee '+hex(target));edges.append((entry,pc,target,'call'));v=[nxt]
            elif m.startswith('j'):
                need(i['args'].startswith('0x'),'unresolved jump')
                target=int(i['args'],16)
                if m=='jmp' and target not in a:
                    need(target in rs,'unknown tail callee');edges.append((entry,pc,target,'tail'));v=[]
                else:v=[target]+([] if m=='jmp' else [nxt])
            elif m=='ret':v=[]
            else:v=[nxt]
            need(all(z in a for z in v),'missing normal CFG successor '+hex(pc));succ[pc]=v
            for mem in i['memory']:
                if mem['role'] in ('w','rw') and mem['base']!='rsp':writes.append((entry,pc,mem['base'],mem['displacement'],mem['size'],mem['role']))
        seen=set();todo=[entry]
        while todo:
            pc=todo.pop()
            if pc not in seen:seen.add(pc);todo.extend(succ[pc])
        need(seen==set(a),'unreachable/extra body instructions')
        graphs.append(dict(entry=hex(entry),instructions=len(a),returns=[hex(pc) for pc,i in a.items() if i['mnemonic']=='ret']))
    expected_writes=[(0x2fead0,pc,'rbx',4,4,'rw') for pc in [0x2feb0c,0x2feb1b,0x2feb54,0x2feb5e,0x2feb69,0x2feb73]]
    need(writes==expected_writes,'nonstack effect census changed')
    adj={entry:[] for entry in rs}
    for entry,pc,target,kind in edges:adj[entry].append(target)
    reached=set();todo=[0x2fead0]
    while todo:
        entry=todo.pop()
        if entry not in reached:reached.add(entry);todo.extend(adj[entry])
    need(reached==set(rs),'unconsumed/opaque closure body')
    # This graph is acyclic between bodies. Local roster/bit loops remain
    # subject to explicit readable/finite state and no-interference premises.
    def visit(x,path):
        need(x not in path,'recursive callee closure')
        for y in adj[x]:visit(y,path|{x})
    visit(0x2fead0,set())
    a=index(rs[0x2fead0]);b=index(rs[0x30c0e0])
    for pc,m,args in [(0x2feade,'mov','rbx, rcx'),(0x2feae1,'mov','rcx, qword ptr [rcx + 0x698]'),(0x2feaf3,'test','eax, 0x80000003'),(0x2feb01,'je','0x2feb67'),(0x2feb0a,'je','0x2feb24'),(0x2feb13,'mov','ecx, 1'),(0x2feb24,'mov','r8d, dword ptr [rbx + 0xea4]'),(0x2feb2b,'xor','ecx, ecx'),(0x2feb30,'je','0x2feb69'),(0x2feb34,'bt','r8d, edx'),(0x2feb3a,'movzx','eax, byte ptr [rbx + 0xea9]'),(0x2feb41,'cmp','edx, eax'),(0x2feb43,'jne','0x2feb0c'),(0x2feb45,'cmp','byte ptr [rbx + 0x6b6], cl'),(0x2feb4b,'je','0x2feb0c'),(0x2feb4f,'cmp','edx, 0x20'),(0x2feb52,'jl','0x2feb34'),(0x2feb67,'xor','ecx, ecx')]:expect(a,pc,m,args)
    for pc in [0x2feb0c,0x2feb54,0x2feb69]:expect(a,pc,'and','dword ptr [rbx + 4], 0xffefffff')
    for pc in [0x2feb18,0x2feb5b,0x2feb70]:expect(a,pc,'shl','ecx, 0x14')
    for pc,m,args in [(0x30c17b,'movzx','ebx, word ptr [rbx + 0x714]'),(0x30c182,'cmp','bx, si'),(0x30c185,'ja','0x30c1cc'),(0x30c191,'je','0x30c1c4'),(0x30c19e,'je','0x30c1c4'),(0x30c1aa,'call','0x20e600'),(0x30c1b6,'movzx','edx, word ptr [rcx + 8]'),(0x30c1bd,'imul','ecx, edx'),(0x30c1c0,'add','ecx, eax'),(0x30c1c4,'xor','ecx, ecx'),(0x30c1c6,'cmp','byte ptr [rcx + 6], 0'),(0x30c1ce,'call','0x236850')]:expect(b,pc,m,args)
    resolver=index(rs[0x20e600]);mem=resolver[0x20e602]['memory']
    need(len(mem)==1 and mem[0]['role']=='r' and mem[0]['rip_target']=='0x1f83530','original resolver global changed')
    return dict(graphs=graphs,call_edges=[dict(source=hex(x),pc=hex(pc),target=hex(t),kind=k) for x,pc,t,k in edges],
        nonstack_writes=[dict(body=hex(e),pc=hex(pc),base=base,offset=off,bytes=n,role=role) for e,pc,base,off,n,role in writes],
        facts=[
         'Conditional complete original 2FEAD0 closure: all twelve other reachable helper bodies are read-only outside the private Win64 stack. No indirect/opaque callee remains in this closure. Original implicit CALL/PUSH/RET writes are confined to the disjoint private stack.',
         'For a valid BattleUnit receiver with readable inputs and normal finite execution/no interference, only DWORD[unit+4] bit20 (QWORD flag bit52) is modified; other bits of that DWORD are preserved. No command714/pendingBA0 or separate mode field is written by this closure. NULL receiver writes no object. The AND then OR are separate writes, not an atomic flag update.',
         'After the status/field gate passes, a positive global roster predicate sets bit52; otherwise set bits0..31 of contributorEA4 are compared to the full EA9 byte. An unequal index sets bit52; equal index sets it when byte6B6==0. No general EA9<32 bound follows.',
         'Global30C0E0 is read-only: initial COUNT<=0 returns0; other guarded roster/target/kind/action paths can return1 from action row byte6. Count is re-read each loop, not a stable snapshot. Current714<=21E is a fixed command bound, not a dynamic table row-count check.',
         'Action table/global/base resolver reads repeat. Row address uses u32(stride*command + low32(second resolved base)), zero-extended intoRCX. First resolver nonNULL is not a full-width or second-result validity promise. Table NULL or first resolve NULL setsRCX0, then reads[RCX+6]; absent binding can fault instead of returning false.'
        ],limits='Method A full bounded original code effect closure, not native execution or natural reachability. Ordinary valid object/table identity, readable inputs, disjoint private writable Win64 stack/home space, normal ABI, no external concurrent/intervention mutation, finite stable roster for termination. Exception/fault paths are not successful returns. Does not close preceding313B30 effects, other KO callees, natural KO/Esper113 coexistence, initialization/ownership/lifetime/timing/presentation or wholeUQ147.')

def legacy_setup(s):
    f=ROOT/'Database/FFXII TZA/_experiments/evidence/commit-callees-exec/check.py'
    rp=f.with_name('result.json')
    need(sha(f)=='3a8028419796303e1c9cc27d15440b786eddea5a0be54009600958917be64068','legacy producer moved')
    need(sha(rp)=='e74106aadbaa76260fdb3405d0c4116604759dec9ec96c90f6d869c54821f5ea','legacy results moved')
    tree=ast.parse(f.read_text());defs=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='G_IMGB' for t in n.targets)]
    need(len(defs)==1 and isinstance(defs[0].value,ast.Constant),'legacy global constant ambiguous')
    world=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='World'];need(len(world)==1,'World constructor missing')
    writes=[n for n in ast.walk(world[0]) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='gm' and n.func.attr=='w' and n.args and isinstance(n.args[0],ast.Name) and n.args[0].id=='G_IMGB']
    need(len(writes)==1 and ast.unparse(writes[0])=='gm.w(G_IMGB, qw(HEAP))','actual legacy initializer changed')
    actual=int(index(next(r for r in s['ranges'] if r['start']=='0x20e600'))[0x20e602]['memory'][0]['rip_target'],16)
    configured=defs[0].value.value;need(configured==0x1f85d30 and actual==0x1f83530 and configured!=actual,'concrete mismatch no longer present')
    results=json.loads(rp.read_text());need(results['cases']==87 and results['mutants_total']==10 and len(results['results'])==97,'legacy selected result domain changed')
    traces=[z for z in results['results'] if any(t[0]=='tvalid' for t in z.get('trace',[]))]
    need(len(traces)==1 and traces[0]['name']=='canc-fixup','legacy predicate observations changed')
    need(not any(t[0]=='imgadd' for z in results['results'] for t in z.get('trace',[])),'legacy resolver observation exists; re-evaluate extent')
    return dict(status='CONCRETE_SETUP_MISMATCH',producer_sha256=sha(f),result_sha256=sha(rp),configured_global=hex(configured),original_read_global=hex(actual),initializer_line=writes[0].lineno,configured_line=defs[0].lineno,
        retained_results=97,baseline_cases=87,mutant_cases=10,observed_imgadd_entries=0,observed_tvalid_cases=[z['name'] for z in traces],
        implication='EXP091 explicit image-base initialization does not prepare the address read by shipping20E600. Retained traces do not contain an imgadd entry, so they do not provide a positive control for30C0E0 action-row byte6 path. Preserve the other measured cases; do not use overall87PASS as row-binding or complete effect proof.',
        next='ORACLE owns fixture correction and smallest actual resolver-address/positive action-row control, no blanket rerun or raw result overwrite.',
        limits='Static producer/setup discrepancy and deterministic retained trace reduction. No new native tests run; zero recorded imgadd entries is not global absence or a live negative observation. Exact old assertions must be adjudicated by owning producer/reviewer.')

def main():
    out=P/sys.argv[1];need(not out.exists(),'fresh output required')
    sp=P/'source-target-fixup-01.json';st=P/(sys.argv[2] if len(sys.argv)>2 else 'qualify-target-fixup-03.status.json')
    status=json.loads(st.read_text())
    need(status.get('terminal') is True and status.get('exit')==0 and status.get('exception') is None and status.get('driver_sha256')==sha(P/'qualify-target-fixup-retained.py'),'required qualifier failed/incomplete')
    need(sha(sp)=='4b303e3629b8d360b4192c9f242d90d6a83266f5e88c77af7e58b0d6b9b27215','qualified source moved')
    s=json.loads(sp.read_text());need(s.get('wrapper_complete') is True and s.get('exe_sha256')==PIN,'source incomplete')
    validator=W/'validate-title-source-annotations.py';need(sha(validator)=='7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13','reviewed validator changed')
    spec=importlib.util.spec_from_file_location('reviewed_validator',validator);V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    annotation=V.validate(s);facts=derive(s);legacy=legacy_setup(s);controls=[]
    for name,body,pc,kind,value,diagnostic in [
      ('helper-store',0x236820,0x236820,'memory',None,'nonstack effect census changed'),
      ('opaque-callee',0x30c0e0,0x30c196,'args','0x333333','unknown callee'),
      ('wrong-flag-bit',0x2fead0,0x2feb54,'args','dword ptr [rbx + 4], 0xffdfffff','specific dataflow changed'),
      ('wrong-null-branch',0x30c0e0,0x30c191,'args','0x30c1cc','specific dataflow changed')]:
        z=copy.deepcopy(s);i=index(next(r for r in z['ranges'] if int(r['start'],16)==body))[pc]
        if kind=='memory':i['memory'].append(dict(base='rbx',index=None,scale=1,displacement=0x714,size=2,role='w',rip_target=None))
        else:i[kind]=value
        try:derive(z)
        except ValueError as e:need(diagnostic in str(e),'wrong detector');controls.append(dict(name=name,diagnostic=str(e),method='Labelled source-record detector control, not coherent instruction patch or native execution'))
        else:raise ValueError('control missed '+name)
    with out.open('x') as f:json.dump(dict(producer_complete=True,method='A retained-code normalization, full conditional call/effect closure and primary producer inspection',driver_sha256=sha(Path(__file__)),exe_sha256=PIN,source_sha256=sha(sp),required_status_sha256=sha(st),annotation_prerequisite=annotation,facts=facts,legacy_setup=legacy,controls=controls,acceptance='Producer-valid only, independent review and owning consumption pending; wholeUQ147 OPEN'),f,indent=2)
    print('Conditional target-fixup closure writes only flag52; legacy EXP091 initializes resolver base at wrong address, with no retained action-row positive control.')
if __name__=='__main__':main()
