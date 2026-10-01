"""Isolated original-code / native CRT experiment in a bounded owned child.

Reuses the prior owned-native-run Win32 allocation and Popen cleanup conventions.
No FF12 process discovery/control, debugger, Steam access or save/config writes.
"""
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
import capstone
from fixture import make, absolute_jump, SENTINEL

E = Path(__file__).resolve().parent
ROOT = E.parents[4]
EXE = ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ID = '76561198045890736'
PREFIX = r'C:\FF12'
RANGES = [(0x1f3ed0,159), (0x197ee0,273), (0x194ef0,89),
          (0x16d670,8), (0x808c40,33)]
sha = lambda b: hashlib.sha256(b).hexdigest()


def write(p, value):
    with p.open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2); f.write('\n')


def pe():
    raw = EXE.read_bytes(); assert sha(raw) == EXE_SHA
    p = struct.unpack_from('<I',raw,60)[0]; o = p+24
    base = struct.unpack_from('<Q',raw,o+24)[0]; assert base == 0x120000
    size = struct.unpack_from('<I',raw,o+56)[0]
    table = o+struct.unpack_from('<H',raw,p+20)[0]
    sections = []
    for i in range(struct.unpack_from('<H',raw,p+6)[0]):
        q=table+40*i; virtual,rva,n,offset=struct.unpack_from('<IIII',raw,q+8)
        flags=struct.unpack_from('<I',raw,q+36)[0]
        sections.append((virtual,rva,n,offset,flags))
    image=bytearray(size)
    for virtual,rva,n,offset,flags in sections: image[rva:rva+n]=raw[offset:offset+n]
    return base, image, sections


def decode(raw, address):
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    ins=list(md.disasm(raw,address)); assert ins and sum(i.size for i in ins)==len(raw)
    return [dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]


def kernel():
    k=C.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_uint32,C.c_uint32];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_uint32]
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_uint32,C.POINTER(C.c_uint32)]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    k.GetModuleFileNameW.argtypes=[C.c_void_p,C.c_wchar_p,C.c_uint32]
    return k


def child(folder, stable, shim, options):
    k=kernel(); k.SetErrorMode(0x0001|0x0002|0x8000)
    crt=C.WinDLL('ucrtbase'); path=C.create_unicode_buffer(32768)
    assert k.GetModuleFileNameW(crt._handle,path,len(path))
    crtpath=Path(path.value); crthash=sha(crtpath.read_bytes())
    crtfn=C.cast(crt.__stdio_common_vswprintf_s,C.c_void_p).value
    base,image,sections=pe(); allocations=[]; normal=False; result={}
    try:
        mapped=k.VirtualAlloc(base,len(image),0x3000,4)
        assert mapped==base, ('shipping base unavailable', mapped, C.get_last_error())
        allocations.append(mapped); C.memmove(mapped,bytes(image),len(image))
        data=k.VirtualAlloc(None,0x2000,0x3000,4); assert data; allocations.append(data)
        code=k.VirtualAlloc(None,0x4000,0x3000,4); assert code; allocations.append(code)
        C.memmove(data+0x100,(PREFIX+'\0').encode('utf-16le'),(len(PREFIX)+1)*2)
        C.memmove(data+0x200,(ID+'\0').encode('utf-16le'),(len(ID)+1)*2)
        parts=make(code,data,crtfn,stable)
        for offset,b in parts.items():
            C.memmove(code+offset,b,len(b)); (folder/f'fixture-{offset:04x}.bin').write_bytes(b)
        # Injected end boundary prevents the next original directory-creation call.
        patch=absolute_jump(code+0x1000); C.memmove(0x197f93,patch,len(patch))
        C.c_uint64.from_address(0x8c2e88).value=code+0x3000 if shim else crtfn
        C.c_uint64.from_address(0x2eba3d0).value=options
        old=C.c_uint32()
        for virtual,rva,n,offset,flags in sections:
            if flags & 0x20000000: assert k.VirtualProtect(base+rva,max(virtual,n),0x20,C.byref(old))
        assert k.VirtualProtect(code,0x4000,0x20,C.byref(old))
        assert k.FlushInstructionCache(k.GetCurrentProcess(),base,len(image))
        assert k.FlushInstructionCache(k.GetCurrentProcess(),code,0x4000)
        expected={}
        for a,n in RANGES:
            original=bytes(image[a-base:a-base+n]); expected[a]=C.string_at(a,n)
            if a==0x197ee0:
                exp=bytearray(original);exp[0x197f93-a:0x197f93-a+len(patch)]=patch
                assert expected[a]==bytes(exp)
            else: assert expected[a]==original
        assert C.string_at(0x8f38c0,12)==('%s\\%s\0').encode('utf-16le')
        proof=dict(pid=os.getpid(),started_unix=time.time(),executable_sha256=EXE_SHA,
                   python=sys.version,python_path=sys.executable,python_sha256=sha(Path(sys.executable).read_bytes()),
                   windows=list(sys.getwindowsversion()),crt_path=str(crtpath),crt_sha256=crthash,
                   crt_export=crtfn,mapped_base=base,image_size=len(image),code=code,data=data,
                   stable=stable,shim=shim,printf_options=options,
                   fixture={str(o):decode(b,code+o) for o,b in parts.items()},
                   originals=[dict(address=a,bytes=bytes(image[a-base:a-base+n]).hex(),
                                   instructions=decode(bytes(image[a-base:a-base+n]),a)) for a,n in RANGES],
                   interventions=['Supplied post-format ID at original helper return tail; Steam and logging omitted.',
                                  'Supplied caller prefix and printf options; preceding filesystem work omitted.',
                                  'End jump at197F93 prevents following directory call.',
                                  'IAT8C2E88 bound to native host CRT, optionally through stack-neutral entry observer.',
                                  'Stable control replaces returned alias with retained input pointer.'],
                   debugger_present=bool(k.IsDebuggerPresent()))
        write(folder/'before.json',proof)
        returned=C.CFUNCTYPE(C.c_uint64,C.c_void_p)(code)(data)
        raw=C.string_at(data,0xe00)
        with (folder/'native.bin').open('xb') as f:f.write(raw)
        assert returned==SENTINEL
        assert all(C.string_at(a,len(b))==b for a,b in expected.items())
        assert sha(crtpath.read_bytes())==crthash and sha(EXE.read_bytes())==EXE_SHA
        result=dict(returned=returned,raw_sha256=sha(raw),source_and_code_unchanged=True,
                    crt_sha256_after=crthash,debugger_present=bool(k.IsDebuggerPresent()))
        normal=True
    finally:
        freed=[dict(address=a,freed=bool(k.VirtualFree(a,0,0x8000))) for a in reversed(allocations)]
        write(folder/'cleanup.json',dict(normal_return=normal,allocations=freed,**result))
    assert normal and all(a['freed'] for a in freed)


def main():
    p=argparse.ArgumentParser();p.add_argument('--child',action='store_true');p.add_argument('--name',required=True)
    p.add_argument('--stable',action='store_true');p.add_argument('--shim',action='store_true');p.add_argument('--options',type=int,default=0)
    a=p.parse_args(); folder=E/a.name
    if a.child: child(folder,a.stable,a.shim,a.options);return
    folder.mkdir(exist_ok=False)
    cmd=[sys.executable,str(Path(__file__).resolve()),'--child','--name',a.name,'--options',str(a.options)]
    if a.stable:cmd.append('--stable')
    if a.shim:cmd.append('--shim')
    write(folder/'plan.json',dict(method='B - isolated original return/caller/formatter with native host CRT',
          live_game=False,command=cmd,sources={p.name:sha(p.read_bytes()) for p in (E/'run.py',E/'fixture.py')},
          timeout_seconds=15,question='Does native formatting preserve the supplied returned-stack ID in this exact state?',
          limit='No actual Steam initialization, original startup reachability, filesystem creation or universal CRT claim.'))
    with (folder/'stdout.txt').open('xb') as out,(folder/'stderr.txt').open('xb') as err:
        proc=subprocess.Popen(cmd,stdout=out,stderr=err,creationflags=0x08000000)
        timeout=False
        try:rc=proc.wait(timeout=15)
        except subprocess.TimeoutExpired:timeout=True;proc.kill();rc=proc.wait(timeout=5)
    write(folder/'process.json',dict(pid=proc.pid,exit_code=rc,timed_out=timeout,owned_child_reaped=True))
    print(json.dumps(dict(name=a.name,exit_code=rc,timed_out=timeout)))
    assert rc==0 and not timeout, (folder/'stderr.txt').read_text(errors='replace')


if __name__=='__main__':main()
