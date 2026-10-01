"""Add one8B getter identity to retained716B, not another population capture."""
import hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained/trailer-binding';sha=lambda b:hashlib.sha256(b).hexdigest()
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
raw=json.loads((W/'raw-source.json').read_text())
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
sp=importlib.util.spec_from_file_location('rd',W/'retained/shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)==raw['reference']['exe_sha256']
sp=importlib.util.spec_from_file_location('roles',W/'retained/reg_tracking.py');roles=importlib.util.module_from_spec(sp);sp.loader.exec_module(roles)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
code=rd.img_rd(d,ss,0x383840,8);seq=list(cs.disasm(code,0x383840));assert len(seq)==2 and seq[-1].mnemonic=='ret'
i=seq[0];o=i.operands[1];assert i.mnemonic=='mov' and i.reg_name(i.operands[0].reg)=='rax' and o.size==8 and i.address+i.size+o.mem.disp==0x2AEDFB0 and roles.op_kind(i,o,1)=='r'
(R/'root-return-getter.bin').write_bytes(code)
body=(W/'retained/populator.bin').read_bytes();assert sha(body)==next(b['sha256'] for b in raw['bodies'] if b['name']=='populator')
ii={i.address:i for i in cs.disasm(body,0x392740)}
assert ii[0x3928E7].operands[0].imm==0x383840 and ii[0x3928F4].op_str=='r15, rax'
assert ii[0x3928FF].op_str=='rax, rax' and ii[0x392902].operands[0].imm==0x392968
assert ii[0x392909].op_str=='dword ptr [rax + 0x24], edx' and ii[0x392920].op_str=='ecx, dword ptr [r15 + 0x28]' and ii[0x392924].operands[0].imm==0x20E600
assert ii[0x392929].op_str=='edx, word ptr [rdi + rax]' and ii[0x39292D].op_str=='rcx, [rdi + rax]'
assert ii[0x392933].operands[0].imm==0x392946 and ii[0x392935].op_str=='edx, 1' and ii[0x392938].operands[0].imm==0x39295C
assert ii[0x392946].op_str=='xmm3, dword ptr [rcx + 0xc]' and ii[0x39293A].op_str=='xmm3, dword ptr [rcx + 0xc]' and ii[0x39293F].op_str=='xmm3, dword ptr [rcx + 0x10]'
assert ii[0x39294B].op_str=='xmm2, dword ptr [rcx + 8]' and ii[0x392950].op_str=='xmm1, dword ptr [rcx + 4]' and ii[0x39295E].op_str=='rdi, 0x20'
pre=[]
for path,keep,name in [('Database/FFXII TZA/_types/fields.tsv',lambda l:(l.startswith(b'NavRunStateBlock\t') and l.split(b'\t')[1] in [b'0x024',b'0x028']) or l.startswith(b'NavTrailerRecord28\t'),'trailer-fields-preimage.tsv'),('Database/FFXII TZA/_types/types.tsv',lambda l:l.startswith(b'NavTrailerRecord28\t'),'trailer-type-preimage.tsv')]:
 p=Path(path);b=p.read_bytes();lines=b.splitlines(keepends=True);k=lines[0]+b''.join(x for x in lines[1:] if keep(x));assert b'No code reads' in k or b'no code reads' in k;(R/name).write_bytes(k);pre.append(dict(path=path,full_source_sha256=sha(b),retained=name,retained_sha256=sha(k)))
correct=dict(method='A original8B getter plus already-retained702B source, no code execution',reference=raw['reference'],driver_sha256=sha(Path(__file__).read_bytes()),getter=dict(entry='0x383840',bytes=8,sha256=sha(code),returns_cell='0x2aedfb0',call_site='0x3928e7',preserved_register='r15'),reads=dict(header_count_pc='0x392909',header_count_offset='0x24',encoded_table_pc='0x392920',encoded_table_offset='0x28',decode_call='0x392924',record_stride='0x20',kind_u16_pc='0x392929',float4_pc='0x392950',float8_pc='0x39294b',floatC_kind0_pc='0x392946',floatC_kind1_pc='0x39293a',maxss_float10_kind1_pc='0x39293f',mark_call='0x392957'),consumers=pre,correction='Refutes no code reads +24 and no consumer of +28/NavTrailerRecord28. Actual bounded reads consume count<=32, encoded table reference, u16 kind, float slots+4/+8/+C (and+10 forkind1 maxss) passed to392200. Kind0/1 accepted, other kinds skip yet ID advances. Source alias is getter RAX->R15, which stated limited census did not cover; zero bounded access count cannot become universal no-reader claim.',limits='Actual loaded root/decoded table identity and validity, instruction-completion/FP state, native mark effects and scheduling not observed. Getter source gives identity conditional on reading current root; image is not initialized memory. Do not infer geometry names, full record layout, identity stability, all record kinds or native data lifetime. Existing reported limited census zero may remain as its bounded historical result; only universal absence and affected consumers/procedure must change.')
(W/'trailer-binding-result.json').write_text(json.dumps(correct,indent=2)+'\n')
for x in raw['tools']['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
print('BOUND_TRAILER_SOURCE getter383840 returns02AEDFB0; +24count/+28decoded0x20table actual consumer392740, prior universal no-reader claims refuted; record semantics/native effects limited')
