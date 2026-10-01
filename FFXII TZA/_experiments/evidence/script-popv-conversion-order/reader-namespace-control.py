"""Small regression for the actual producer's direct reader-loading invocation."""
import ast,hashlib,json,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;src=(W/'capture.py').read_bytes();tree=ast.parse(src)
nodes=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and any((isinstance(t,ast.Name) and t.id=='rd') or (isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id=='rd' and t.attr=='__file__') for t in n.targets):nodes.append(n)
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec' and 'rd.__dict__' in ast.unparse(n):nodes.append(n)
assert len(nodes)==3,'Actual producer reader initialization path must be selected'
def invoke(selected):
 ns=dict(types=types,R=W/'retained');exec(compile(ast.fix_missing_locations(ast.Module(body=selected,type_ignores=[])),'actual selected producer reader loader','exec'),ns);return ns['rd']
rd=invoke(nodes);assert rd.__file__==str((W/'retained/shipping-reader.py').resolve()) and callable(rd.load_image)
failed=None
try:invoke([nodes[0],nodes[2]])
except NameError as ex:failed=str(ex)
assert failed and '__file__' in failed,'Omitted namespace precondition must fail before load_image/guestexecution'
receipt=dict(status='PASS_ACTUAL_READER_NAMESPACE_PRECONDITION',capture_sha256=hashlib.sha256(src).hexdigest(),selected_ast_sha256=hashlib.sha256(ast.dump(ast.Module(body=nodes,type_ignores=[]),include_attributes=True).encode()).hexdigest(),actual_default_loader=True,omitted_file_rejected=failed,limits='Actual producer selected reader module initialization only; no image load or original/guest/live execution. Initial failedcapture had no semantic conclusions.')
p=W/'reader-namespace-control.json';out=(json.dumps(receipt,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out
else:p.write_bytes(out)
print('PASS actual reader namespace path/omitted-file control',flush=True)
