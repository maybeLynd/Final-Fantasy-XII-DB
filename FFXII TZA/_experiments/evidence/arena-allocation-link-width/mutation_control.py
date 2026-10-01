"""One targeted original-decoder mutation; do not replay the original seven cases."""
import hashlib,json
from pathlib import Path
p=Path('Database/Tools/work/ASTRA/arena_alloc_probe.py')
source=p.read_text()
ns={}
exec(compile(source[:source.index('predictions={')],str(p),'exec'),ns)
b=ns['B'][0x20E600]
assert b[:2]==bytes.fromhex('8bc1')
ns['B'][0x20E600]=bytes.fromhex('31c0')+b[2:] # zero every reference before the original base addition
c=ns['run']('zero-decoder-mutant','low-address')
steps=c['steps']
alloc=[s for s in steps if s['label'].startswith('allocation')]
assert len(alloc)==2 and all(s['returned'] and s['stack_ok'] and s['nonvolatile_ok'] for s in steps)
assert [s['rax'] for s in alloc]==['0x400102c0','0x40010340']
after=bytes.fromhex(alloc[1]['prefix'])
predecessor=int.from_bytes(after[0x30C:0x310],'little')
assert predecessor==0 # native original control has 0x40010280 here
out=dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),original_decoder_sha256=hashlib.sha256(b).hexdigest(),mutated_decoder_sha256=hashlib.sha256(ns['B'][0x20E600]).hexdigest(),mutation=dict(address='0x20e600',before='8bc1',after='31c0'),case=c,detected_by='second allocated block physical predecessor differs despite correct return pointers',expected_predecessor='0x40010280',actual_predecessor=hex(predecessor))
Path('Database/Tools/work/ASTRA/arena-allocation-mutant-result.json').write_text(json.dumps(out,indent=2)+'\n')
print('DETECTED original decoder zeroing mutation: returned both expected payloads but lost second allocation predecessor',hex(predecessor))
