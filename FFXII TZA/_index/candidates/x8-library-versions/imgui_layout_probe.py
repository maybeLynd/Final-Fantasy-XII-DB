"""imgui_probe.py TAG... - export each upstream tag, generate a probe printing ImGuiIO / ImGuiStyle member
offsets and the context struct size, compile it with WSL g++ (x86_64 LP64; same layout rules as MSVC x64
for these PODs: no long, no bitfields) and print the result."""
import os, re, subprocess, sys
UP = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(UP, "imgui.git")
def wsl(p):
    p = p.replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:]
def members(src, name):
    m = re.search(r"struct\s+" + name + r"\s*\{(.*?)\n\};", src, re.S)
    if not m: return []
    body = m.group(1)
    body = re.sub(r"//[^\n]*", "", body)
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    out = []
    depth = 0; stmt = ""
    for ch in body:
        if ch == "{": depth += 1; stmt = ""; continue
        if ch == "}": depth -= 1; stmt = ""; continue
        if depth: continue
        if ch == ";":
            s = stmt.strip(); stmt = ""
            if not s or "(" in s and "(*" not in s: continue
            if s.startswith(("typedef", "friend", "enum", "static", "IMGUI_API", "public", "private")): continue
            fp = re.search(r"\(\s*\*\s*(\w+)\s*\)", s)
            if fp: out.append(fp.group(1)); continue
            s = re.sub(r"\[[^\]]*\]", "", s).split("=")[0]
            for part in s.split(","):
                w = re.findall(r"(\w+)\s*$", part.strip())
                if w: out.append(w[0])
        else:
            stmt += ch
    return out
for tag in sys.argv[1:]:
    d = os.path.join(UP, "imgui_" + tag)
    os.makedirs(d, exist_ok=True)
    import tarfile, io as _io
    data = subprocess.run(["git", "-C", REPO, "archive", tag], capture_output=True, check=True).stdout
    tarfile.open(fileobj=_io.BytesIO(data)).extractall(d)
    h = open(os.path.join(d, "imgui.h"), encoding="utf-8", errors="replace").read()
    io = members(h, "ImGuiIO"); st = members(h, "ImGuiStyle")
    cpp = open(os.path.join(d, "imgui.cpp"), encoding="utf-8", errors="replace").read()
    inter = os.path.join(d, "imgui_internal.h")
    allsrc = cpp + (open(inter, encoding="utf-8", errors="replace").read() if os.path.exists(inter) else "")
    ctx = "ImGuiContext" if re.search(r"struct\s+ImGuiContext\s*\{", allsrc) else "ImGuiState"
    lines = ['#define private public', '#define protected public', '#include "imgui.cpp"', '#include <cstdio>', '#include <cstddef>',
             'int main(){', 'printf("sizeof(ImGuiIO) 0x%zX\\n", sizeof(ImGuiIO));',
             'printf("sizeof(ImGuiStyle) 0x%zX\\n", sizeof(ImGuiStyle));',
             'printf("sizeof(%s) 0x%%zX\\n", sizeof(%s));' % (ctx, ctx),
             'printf("ImGuiCol_COUNT %d\\n", (int)ImGuiCol_COUNT);',
             'printf("ImGuiKey_COUNT %d\\n", (int)ImGuiKey_COUNT);']
    for f in io:
        lines.append('printf("IO.%s 0x%%zX\\n", offsetof(ImGuiIO, %s));' % (f, f))
    for f in members(allsrc, ctx):
        lines.append('printf("CTX.%s 0x%%zX\\n", offsetof(%s, %s));' % (f, ctx, f))
    for f in st:
        lines.append('printf("Style.%s 0x%%zX\\n", offsetof(ImGuiStyle, %s));' % (f, f))
    lines.append("return 0;}")
    open(os.path.join(d, "probe.cpp"), "w").write("\n".join(lines))
    r = subprocess.run(["wsl", "-e", "bash", "-c", "cd '%s' && g++ -w -fpermissive -std=gnu++11 -Wno-narrowing probe.cpp -Wl,--unresolved-symbols=ignore-all -o probe 2>&1 | grep -m5 error; ./probe" % wsl(d)],
                       capture_output=True, text=True)
    open(os.path.join(UP, "imgui_layout_%s.txt" % tag), "w").write(r.stdout)
    print("=== " + tag); print(r.stdout[:4000]); print(r.stderr[:500])
