"""Bounded original-source proof of rig owner producer and rebinder preconditions.

STATIC_ONLY. Fixed-width calculations below are not execution of FF12 code.
"""
import hashlib, importlib.util, json, struct, sys
from pathlib import Path
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = next(q for q in P.parents if (q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
PIN = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'

def load(name, file):
    s = importlib.util.spec_from_file_location(name, P/file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

for file, pin in [
    ('capture-index-path.py','cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497'),
    ('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),
    ('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
    if sha(P/file) != pin: raise RuntimeError('reviewed dependency changed')
V = load('roles','validate-title-source-annotations.py')
G = load('graph','prove_owner_reload_order.py')

def checked_capture(prefix):
    d = P/prefix
    status = json.loads((d/'capture-01.status.json').read_text())
    if status.get('terminal') is not True or status.get('exit') != 0 or status.get('exception') is not None or status['driver_sha256'] != sha(d/'capture.py') or not (d/'capture-01.stdout').read_bytes() or (d/'capture-01.stderr').read_bytes():
        raise RuntimeError('required capture status failed '+prefix)
    x = json.loads((d/'source-01.json').read_text())
    if x.get('wrapper_complete') is not True or x.get('driver_sha256') != sha(P/'capture-index-path.py') or x.get('invocation_driver_sha256') != sha(d/'capture.py') or x['exe_sha256'] != PIN:
        raise RuntimeError('actual capture incomplete '+prefix)
    return x, V.validate(x)

# These are concrete top-level prerequisite calls, before semantic output.
x, roles = checked_capture('')
lineage = json.loads((P/'lineage.json').read_text())
expected_parents = {
    'retained/rig':'49f2d7af98080cdde1a4ba3fa36fa7ec4f44439e7f8f40d3d3d95f6b3daf37f7',
    'retained/factory':'d4927fd135f97861ee64af294f75f898acf6c654da660d3b50d8324a16d8783c'}
if {r['retained_prefix']:r['manifest_sha256'] for r in lineage} != expected_parents:
    raise RuntimeError('retained population changed')
for row in lineage:
    d = P/row['retained_prefix']; m = d/'manifest.json'
    if sha(m) != row['manifest_sha256']: raise RuntimeError('retained manifest changed')
    members = json.loads(m.read_text())['members']
    for r in row['retained_files']:
        q = d/r['path']
        if sha(q) != r['sha256'] or q.stat().st_size != r['bytes']: raise RuntimeError('retained input changed')
        if r['path'] != 'manifest.json' and not any(v['path'] == r['path'] and v['sha256'] == r['sha256'] for v in members):
            raise RuntimeError('unbound retained input')
y, rig_roles = checked_capture('retained/rig')
z, decoder_roles = checked_capture('retained/rig/retained')
w, encoder_roles = checked_capture('retained/rig/retained/retained')
f, factory_roles = checked_capture('retained/factory')
sources = [('source-01.json',x),('retained/rig/source-01.json',y),
           ('retained/rig/retained/source-01.json',z),
           ('retained/rig/retained/retained/source-01.json',w),
           ('retained/factory/source-01.json',f)]
required = [('0x372350','0x3723a4'),('0x3e3ca0','0x3e3d64'),
            ('0x3e3d70','0x3e4131'),('0x4215a0','0x421892')]
if [(r['start'],r['end_exclusive']) for r in x['ranges']] != required:
    raise RuntimeError('required new source population changed')
raw = (ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(raw).hexdigest() != PIN: raise RuntimeError('original image changed')
pe = struct.unpack_from('<I',raw,60)[0]; opt = struct.unpack_from('<H',raw,pe+20)[0]
secs = [struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
def read(a,n):
    for vs,rva,size,offset in secs:
        if 0x120000+rva <= a and a+n <= 0x120000+rva+size:
            return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
    raise RuntimeError('unbacked original range')
ix = {}; by_entry = {}; graphs = []
selected = {0x372350,0x3e3ca0,0x3e3d70,0x4215a0,0x421d20,0x20e600,0x20e620,0x41f340}
for path, source in sources:
    for r in source['ranges']:
        a,b = int(r['start'],16),int(r['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in r['instructions'])) != read(a,b-a):
            raise RuntimeError('original byte mismatch')
        local = {int(i['pc'],16):i for i in r['instructions']}
        for pc, i in local.items():
            if pc in ix and ix[pc] != i: raise RuntimeError('inconsistent original source')
        ix.update(local)
        if a in selected:
            g = G.graph(local,a,b,tail='0x20e600' if a == 0x421d20 else None)
            if g['visited'] != set(local): raise RuntimeError('unaccounted selected CFG')
            by_entry[a] = g
            graphs.append({'entry':hex(a),'source':path,'instructions':len(local),
                           'calls':g['calls'],'returns':[hex(v) for v in g['returns']],
                           'tails':[hex(v) for v in g['tails']]})
if set(by_entry) != selected: raise RuntimeError('missing selected CFG')
ops = '''37235a|cmp|dword ptr [rcx + 0x90], 0
372361|mov|edi, edx
372363|mov|rbx, rcx
372366|jle|0x372399
372368|mov|ecx, dword ptr [rcx + 0x94]
37236e|call|0x20e600
372373|test|rax, rax
372376|je|0x372399
372378|mov|ecx, dword ptr [rbx + 0x94]
37237e|call|0x20e600
372383|mov|dword ptr [rax + 0x68], edi
372386|mov|ecx, dword ptr [rbx + 0x94]
37238c|call|0x20e600
372391|mov|rcx, rax
372394|call|0x3e3d70
3e3ca0|test|rcx, rcx
3e3ca3|je|0x3e3d63
3e3cae|movzx|eax, word ptr [rcx + 0x68]
3e3cb2|mov|rbx, rcx
3e3cba|xor|edi, edi
3e3cbc|cmp|ax, -1
3e3cc0|jne|0x3e3cc6
3e3cc2|mov|ecx, edi
3e3cc4|jmp|0x3e3ce2
3e3cc6|movsx|rax, ax
3e3cca|imul|rcx, rax, 0x740
3e3cd1|add|rcx, qword ptr [rip + 0x1ee3250]
3e3cd8|cmp|dword ptr [rcx + 0x284], edi
3e3cde|cmove|rcx, rdi
3e3ce2|call|0x20e620
3e3ce7|mov|ecx, eax
3e3ce9|mov|dword ptr [rbx + 0x70], eax
3e3cec|call|0x20e600
3e3cf1|mov|rcx, rax
3e3cf4|call|0x421d20
3e3cfc|call|0x20e620
3e3d01|cmp|dword ptr [rbx + 0x6c], -1
3e3d05|mov|dword ptr [rbx + 0x78], eax
3e3d08|je|0x3e3d59
3e3d0a|movzx|eax, word ptr [rbx + 0x6c]
3e3d0e|cmp|ax, -1
3e3d12|je|0x3e3d34
3e3d14|movsx|rax, ax
3e3d18|imul|rdx, rax, 0x740
3e3d1f|add|rdx, qword ptr [rip + 0x1ee3202]
3e3d26|cmp|dword ptr [rdx + 0x284], 0
3e3d2d|cmove|rdx, rdi
3e3d31|mov|rdi, rdx
3e3d34|mov|rcx, rdi
3e3d37|call|0x20e620
3e3d3e|mov|dword ptr [rbx + 0x74], eax
3e3d41|call|0x20e600
3e3d46|mov|rcx, rax
3e3d49|call|0x421d20
3e3d56|mov|dword ptr [rbx + 0x7c], eax
3e3d70|test|rcx, rcx
3e3d73|je|0x3e4130
3e3d7e|movzx|eax, word ptr [rcx + 0x68]
3e3d82|mov|rbx, rcx
3e3d8a|xor|edi, edi
3e3d8c|cmp|ax, -1
3e3d90|jne|0x3e3d96
3e3d92|mov|ecx, edi
3e3d94|jmp|0x3e3db2
3e3d96|movsx|rax, ax
3e3d9a|imul|rcx, rax, 0x740
3e3da1|add|rcx, qword ptr [rip + 0x1ee3180]
3e3da8|cmp|dword ptr [rcx + 0x284], edi
3e3dae|cmove|rcx, rdi
3e3db2|call|0x20e620
3e3db9|mov|dword ptr [rbx + 0x70], eax
3e3dbc|call|0x20e600
3e3dc1|mov|rcx, rax
3e3dc4|call|0x421d20
3e3dd1|cmp|dword ptr [rbx + 0x6c], -1
3e3dd5|mov|dword ptr [rbx + 0x78], eax
3e3dd8|je|0x3e3e28
3e3dda|movzx|eax, word ptr [rbx + 0x6c]
3e3dde|cmp|ax, -1
3e3de2|jne|0x3e3de9
3e3de4|mov|rcx, rdi
3e3de7|jmp|0x3e3e06
3e3de9|movsx|rax, ax
3e3ded|imul|rcx, rax, 0x740
3e3df4|add|rcx, qword ptr [rip + 0x1ee312d]
3e3dfb|cmp|dword ptr [rcx + 0x284], 0
3e3e02|cmove|rcx, rdi
3e3e06|call|0x20e620
3e3e0d|mov|dword ptr [rbx + 0x74], eax
3e3e10|call|0x20e600
3e3e15|mov|rcx, rax
3e3e18|call|0x421d20
3e3e25|mov|dword ptr [rbx + 0x7c], eax
3e3e28|mov|rcx, rbx
3e3e2b|call|0x3e3c30
4215b8|mov|rsi, rcx
4215c3|mov|rdi, r8
4215c6|movzx|ebp, dx
421637|test|r14, r14
42163a|je|0x421879
421640|test|rbx, rbx
421643|je|0x421879
421649|test|byte ptr [r14], 0x80
421652|je|0x421838
421658|cmp|bp, ax
42165b|jne|0x4216f7
4216cc|mov|ecx, dword ptr [r14 + 0x94]
4216d3|movsx|ebx, word ptr [rsi]
4216d6|call|0x20e600
4216db|mov|dword ptr [rax + 0x6c], ebx
4216de|mov|ecx, dword ptr [r14 + 0x94]
4216e5|call|0x20e600
4216ea|mov|rcx, rax
4216ed|call|0x3e3ca0
41f361|mov|r14, rcx
41f608|movsx|edx, word ptr [r14]
41f60c|mov|rcx, rsi
41f60f|call|0x372350
421d20|push|rbx
421d22|sub|rsp, 0x20
421d26|mov|ebx, dword ptr [rcx + 0x18]
20e600|mov|eax, ecx
20e602|add|rax, qword ptr [rip + 0x1d74f27]
20e620|sub|ecx, dword ptr [rip + 0x1d74f0a]
20e626|mov|eax, ecx'''
for line in ops.splitlines():
    pc,m,args = line.split('|'); pc = int(pc,16)
    if (ix[pc]['mnemonic'],ix[pc]['args']) != (m,args): raise RuntimeError('required operation changed '+hex(pc))

import capstone
cs = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); cs.detail = True
for regs,lo,hi in [({'rdi','edi','di','dil'},0x372363,0x372383),
                   ({'rsi','esi','si','sil'},0x4215bb,0x4216d3),
                   ({'r14','r14d','r14w','r14b'},0x41f364,0x41f608)]:
    for pc in sorted(q for q in ix if lo <= q < hi):
        i = next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc)); _,wr = i.regs_access()
        if {i.reg_name(r) for r in wr} & regs: raise RuntimeError('owner carrier changed '+hex(pc))
for entry,primary,secondary,skip in [(0x3e3ca0,0x3e3cf4,0x3e3d49,0x3e3d59),
                                      (0x3e3d70,0x3e3dc4,0x3e3e18,0x3e3e28)]:
    g = by_entry[entry]
    # Restrict only the outer rig NULL guard. Primary is mandatory on non-NULL entry.
    lo,hi = next((int(r['start'],16),int(r['end_exclusive'],16)) for r in x['ranges'] if int(r['start'],16)==entry)
    local = {pc:i for pc,i in ix.items() if lo <= pc < hi}
    nonnull = G.graph(local,lo,hi,fixed={entry+3:False})
    if not G.dominates(nonnull,primary,skip): raise RuntimeError('primary lookup not mandatory')
    branch = 0x3e3d08 if entry==0x3e3ca0 else 0x3e3dd8
    if g['edges'][branch][0] != skip: raise RuntimeError('secondary sentinel skip changed')
    q = branch
    # The taken full-DWORD sentinel edge reaches skip without secondary stores/call.
    skipped = G.graph(local,lo,hi,fixed={entry+3:False,branch:True})
    if secondary in skipped['visited']: raise RuntimeError('secondary skip still calls lookup')
    for pc in skipped['visited']:
        if any(m['base']=='rbx' and m['role'] in ('w','rw') and m['displacement'] in (0x74,0x7c) for m in ix[pc]['memory']):
            raise RuntimeError('secondary sentinel path clears cached links')
for pc,size,role in [(0x372383,4,'w'),(0x4216db,4,'w'),(0x3e3d01,4,'r'),
                     (0x3e3dd1,4,'r'),(0x3e3d0a,2,'r'),(0x3e3dda,2,'r'),(0x421d26,4,'r')]:
    m = ix[pc]['memory'][0]
    if (m['size'],m['role']) != (size,role): raise RuntimeError('required width/role changed')

def sign16(v): return (v&0x7fff)-(v&0x8000)
def store32(v): return v&0xffffffff
if not all(sign16(store32(sign16(v)))==sign16(v) and
           (store32(sign16(v))==0xffffffff)==(v==0xffff) for v in range(1<<16)):
    raise RuntimeError('signed16 producer representation invariant failed')
examples = [{'stored_dword':hex(v),'full_dword_skip':v==0xffffffff,
             'reader_signed_index':sign16(v),'low_word_missing':(v&0xffff)==0xffff}
            for v in [0xffffffff,0xffff,0x7fff,0xffff8000]]
if examples[0]['full_dword_skip'] is not True or examples[1]['full_dword_skip'] or not examples[1]['low_word_missing']:
    raise RuntimeError('sentinel representation discriminator failed')

result = {
 'producer_complete':True,'method':'A STATIC_ONLY original rig owner rebinder proof',
 'driver_sha256':sha(Path(__file__)),
 'source_pins':[{'path':path,'sha256':sha(P/path)} for path,_ in sources],
 'annotation_prerequisites':[roles,rig_roles,decoder_roles,encoder_roles,factory_roles],
 'instruction_assertions':len(ops.splitlines()),'graphs':graphs,
 'primary_producer':'372350 stores incoming EDX as DWORD rig68 after signed-positive resource90 and decoded rig94 non-NULL gates. The retained factory passes MOVSX(WORD owner0). The rebinder reads WORD68 then sign-extends it for the 740h table. This preserves the factory signed16 value, but is not a bound or active-owner consistency proof.',
 'secondary_producer':'4215A0 keeps first argument in RSI and third in RDI. On its qualified branch, MOVSX EBX,WORD[RSI] is stored as DWORD rig6C, then the link-only refresher 3E3CA0 is called. This producer sign-extends FFFF to FFFFFFFF; it cannot produce the distinct 0000FFFF sentinel representation under unchanged source/private-state assumptions.',
 'primary_lookup':'Both 3E3CA0 and 3E3D70 return for an outer NULL rig. For a non-NULL rig they refresh primary70 and call421D20 without a derived-owner NULL guard. Missing68 or inactive indexed owner selects Encode(0). At stable B0 its next Decode passes RCX0 to the helper first DWORD[RCX+18h] read. This differs from parent3E1C50 initial70 skip; no natural failure or EXP127 cause inferred.',
 'secondary_skip':'The full DWORD rig6C==FFFFFFFF branch skips the secondary74/7C refresh. It does not directly clear those fields. The low-WORD reader is reached only when the full-DWORD skip is false. Low WORD FFFF or inactive indexed owner then selects Encode(0) and still calls421D20. At B0 the conditional first-read address is18h. For nonzero B use low64(Decode(Encode0)+18h).',
 'reset_order':'3E3D70 calls configured-bone reset3E3C30 only after both applicable owner/core refresh paths. 3E3CA0 is a link-only refresh and has no such reset call in its complete body. Core writes require normal native return and valid input preconditions.',
 'representation_control':{'domain':'All 65536 signed16 source representations, Python fixed-width arithmetic only','property':'Sign-extended DWORD producer and signed low-WORD reader agree; full-DWORD FFFFFFFF skip iff original WORDFFFF. No native/emulated/live execution credit.','examples':examples},
 'consumer_change':'Qualify staged-look/rig prose: outer rig NULL guard is not derived-owner safety; absent full-DWORD secondary skips refresh rather than clearing cached pointers. State signed16-producing caller contracts and valid active indexed-owner premises; preserve source-only/natural-reachability/opaque-effect limits.',
 'limits':[
   'No execution of FF12 instructions, live gameplay, process observation, fault, or natural invalid-state reachability.',
   'Complete local CFG for eight selected bodies, exact retained source verification for all supplied ranges; not an all-caller/all-writer closure or opaque callee semantic proof.',
   'Stable decoder base, valid original objects/table/private frames, ordinary native ABI, no aliasing/interference, and normal callee returns are conditional premises.',
   'Actual owner0=index consistency, table extent/index bounds and active state at each lookup require separate proof; earlier factory flag write cannot prove survival across opaque calls.',
   'A counterrepresentation 0000FFFF distinguishes predicates, but this known secondary writer cannot produce it. No gameplay bug inferred.',
   'Lifetime/reuse/native reset effects, original copy/default count and current authored inputs remain separate; UQ220 not repeated.',
   'Producer controls and owner consumption are distinct from independent acceptance. EXP127 remains invalid; menu allowance remains spent/unapproved; K14 closed; wholeOV rows not closed.']}
out = Path(sys.argv[1] if len(sys.argv)>1 else 'result-01.json'); out = out if out.is_absolute() else P/out
if out.exists(): raise RuntimeError('immutable output exists')
out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
print('PROVED exact rig owner producer widths, rebinder NULL boundaries and secondary skip semantics; STATIC_ONLY')
