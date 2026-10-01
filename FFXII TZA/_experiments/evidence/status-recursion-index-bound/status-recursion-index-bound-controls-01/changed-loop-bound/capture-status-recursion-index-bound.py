"""Bounded original recursive status-index loop, not a game observation."""
import hashlib,importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def main():
 out=pathlib.Path(sys.argv[1])
 if out.exists():raise ValueError('immutable output exists')
 s=importlib.util.spec_from_file_location('verified_recursive_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
 C.RANGES=[(0x30e360,0x30e395),(0x30e645,0x30e6e7)]
 C.main();v=json.loads(out.read_text());v.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Bounded recursion loop/dataflow only; not full0030E360 normalCFG, nativeeffects, naturalbranch entry/resource state or exception behavior')
 out.write_text(json.dumps(v,indent=2)+'\n');print('Original recursion initialization/loop/argument and savedentrybyte captured; file-only')
if __name__=='__main__':main()
