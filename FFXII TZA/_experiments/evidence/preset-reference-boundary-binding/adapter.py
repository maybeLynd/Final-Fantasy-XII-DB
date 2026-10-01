"""Scoped actual-producer replay; private repair binds byte scan and boundaries.

No original instructions execute. Never invoke the producer's whole-image R1.
The default invocation is the corrected path; unchanged path is a fault control.
"""
import ast,copy

def make(source, repaired=True):
    tree=ast.parse(source);nodes=[]
    for n in tree.body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets):break
        nodes.append(n)
    refs=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='refs')
    nodes.append(refs);nodes=copy.deepcopy(nodes)
    if repaired:
        boundary=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='boundary')
        changed=0
        for n in ast.walk(boundary):
            if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='d':
                n.value.id='img';changed+=1
        assert changed==1
        r=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='refs');changed=0
        for n in ast.walk(r):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='boundary':
                assert len(n.args)==1;n.args.append(ast.Name(id='img',ctx=ast.Load()));changed+=1
        assert changed==3
    module=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
    g={};exec(compile(module,'retained-actual-producer-scoped','exec'),g)
    return g,ast.unparse(module)+'\n'

def window(g, entry, length):
    # Explicit bounded input-window projection; unchanged actual function bodies.
    o=g['off'](entry);g['T0']=o;g['TV']=entry;g['TN']=length
    g['SECS']=[(b'.text',length,entry-0x120000,length,o)]
    return o

def observe(g, image, entry, candidate, target, length):
    # The actual refs invocation takes its image; the fixed path forwards it.
    o=g['T0'];ii=list(g['MD'].disasm(image[o:o+length],entry))
    return dict(refs=[[k,f'{a:08X}'] for k,a in g['refs'](target,image)],
                boundary_with_image=g['boundary'](candidate,image),
                decode=[dict(pc=f'{i.address:08X}',hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str,size=i.size) for i in ii],
                source_boundaries=[f'{i.address:08X}' for i in ii],
                candidate=f'{candidate:08X}')
