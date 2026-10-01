"""EO3 adapter for the retained, native-controlled pending-event abort.

No launcher, process discovery, debugger attach or native API calls at import.
The caller supplies the independently prepared designated-game lifetime.
"""
import ast
import ctypes as C
import hashlib
import ntpath
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
SOURCE_SHA='4e1157eadeccd6446321deec53790cbd668b20db33e53f589af9f662f225abb9'
ABORT_AST_SHA='a72af2d2fa1a2680688d28a4d2d245aaeaee163389c213e060eee72077da8209'
EXE=r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe'
EXE_SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def validate_expected(expected):
    """Validate a supplied identity's scope; this does not prove its provenance."""
    assert set(expected)=={'pid','creation','image','image_sha256'}
    assert type(expected['pid']) is int and 0<expected['pid']<=0xffffffff
    assert type(expected['creation']) is int and expected['creation']>0
    assert isinstance(expected['image'],str) and ntpath.normcase(expected['image'])==ntpath.normcase(EXE)
    assert expected['image_sha256']==EXE_SHA
    return dict(expected)


def make_abort(expected,*,identity_reader=None,clock=time):
    """Bind the exact previously controlled abort body to the prepared lifetime.

    identity_reader/clock may be supplied for explicitly synthetic controls.
    Production uses the retained native identity query and monotonic clock.
    The caller must configure the same native ABI and preserve its Audit.
    """
    expected=validate_expected(expected)
    source=HERE/'native_stop_control.py';assert sha(source)==SOURCE_SHA
    tree=ast.parse(source.read_text())
    query=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='identity')
    debug=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='debugger')
    abort=next(n for n in debug.body if isinstance(n,ast.FunctionDef) and n.name=='abort')
    assert hashlib.sha256(ast.dump(abort,include_attributes=False).encode()).hexdigest()==ABORT_AST_SHA
    ns=dict(C=C,sha=sha,time=clock,owned={'identity':expected},ABORT_CODE=0xea03)
    exec(compile(ast.Module(body=[query,abort],type_ignores=[]),str(source),'exec'),ns)
    if identity_reader is not None:ns['identity']=identity_reader
    native=ns['abort']
    def bound(m,pid,handle,tid,audit):
        assert pid==expected['pid'],'supplied PID is not the prepared lifetime'
        return native(m,pid,handle,tid,audit)
    return bound
