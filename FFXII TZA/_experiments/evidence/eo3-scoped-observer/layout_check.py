"""Recheck retained CONTEXT layout without importing the native helper."""
import ast
import ctypes
import ctypes.wintypes as w
import hashlib
import json
from pathlib import Path
from project import OFFSETS

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
record=json.loads((W/'layout.json').read_text())
source=ROOT/record['type_source'];sdk=Path(record['sdk_path'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==record['type_source_sha256']
assert sha(sdk)==record['sdk_sha256']
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.ClassDef) and n.name in ('M128A','CONTEXT')]
assert {n.name for n in nodes}=={'M128A','CONTEXT'}
namespace={'ctypes':ctypes,'w':w}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),namespace)
assert ctypes.sizeof(namespace['CONTEXT'])==record['context_size']==1232
assert namespace['CONTEXT'].ContextFlags.offset==0x30
fields={'rax':'Rax','rcx':'Rcx','rdx':'Rdx','rbx':'Rbx','rsp':'Rsp','rdi':'Rdi','r8':'R8','r9':'R9','r10':'R10','rip':'Rip'}
for field,name in fields.items():assert getattr(namespace['CONTEXT'],name).offset==record['offsets'][field]==OFFSETS[field]
lines=sdk.read_text().splitlines()
for row in record['sdk_excerpt']:assert lines[row['line']-1]==row['text']
print('CONTEXT size/offsets and pinned SDK excerpt agree; class declarations only, no native calls.')
