"""Read-only source feasibility; no normal-path proof or native execution."""
import hashlib
import json
import sys
from pathlib import Path
import capstone

sys.dont_write_bytecode = True
DEP = Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
POLICY = Path('Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py')
members = {m['path']: m for m in json.loads((DEP/'manifest.json').read_bytes())['members']}
for name in ('retained/functions.tsv', 'python-deps/pefile.py'):
    assert hashlib.sha256((DEP/name).read_bytes()).hexdigest() == members[name]['sha256']
assert hashlib.sha256(POLICY.read_bytes()).hexdigest() == members['retained/reg_tracking.py']['sha256']
sys.path.insert(0, str(POLICY.parent.resolve()))
import reg_tracking as roles
assert Path(roles.__file__).resolve() == POLICY.resolve()
sys.path.insert(0, str((DEP/'python-deps').resolve()))
import pefile
image = Path('Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
assert hashlib.sha256(image).hexdigest() == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
lines = (DEP/'retained/functions.tsv').read_text().splitlines()
row = next(l for l in lines if l.split('\t')[0].lower().lstrip('0x').lstrip('0') == '533b20')
size = int(row.split('\t')[2])
assert size == 9526
pe = pefile.PE(data=image, fast_load=True)
assert pe.OPTIONAL_HEADER.ImageBase == 0x120000
code = pe.get_data(0x533B20 - 0x120000, size)
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True
ins = list(cs.disasm(code, 0x533B20))
assert sum(i.size for i in ins) == size


def shown(i):
    return {'pc': f'{i.address:08X}', 'bytes': i.bytes.hex(),
            'instruction': i.mnemonic + ' ' + i.op_str,
            'written': sorted(roles.written(i))}


selected = [i for i in ins if set(roles.written(i)) & {'r13', 'rbx', 'rsi'}]
returns = [i for i in ins if i.mnemonic.startswith('ret')]
indirect = [i for i in ins if i.mnemonic == 'jmp' and
            i.operands[0].type != capstone.x86.X86_OP_IMM]
tails = [i for i in ins if i.mnemonic == 'jmp' and
         i.operands[0].type == capstone.x86.X86_OP_IMM and
         not 0x533B20 <= i.operands[0].imm < 0x533B20 + size]
print(json.dumps({'status': 'STATIC_FEASIBILITY_ONLY_NOT_ABI_PROOF',
                  'catalogue': row, 'body_bytes': size, 'body_sha256': hashlib.sha256(code).hexdigest(),
                  'adapter_path': str(Path(roles.__file__).resolve()),
                  'adapter_sha256': hashlib.sha256(POLICY.read_bytes()).hexdigest(),
                  'provider_sha256': hashlib.sha256(Path(pefile.__file__).read_bytes()).hexdigest(),
                  'capstone': capstone.__version__, 'instruction_count': len(ins),
                  'entry': [shown(i) for i in ins[:23]],
                  'last_instructions': [shown(i) for i in ins[-23:]],
                  'tracked_writes': [shown(i) for i in selected],
                  'returns': [shown(i) for i in returns],
                  'indirect_jumps': [shown(i) for i in indirect],
                  'external_tails': [shown(i) for i in tails]}, indent=2))
