"""Emit fields.tsv: one row per preset-block field of each eps class with a non-zero stride.
Field semantics are from the static read recorded in notes.md; the shipped value column is read from
sead.win.config here (not typed by hand). kind: f = f32, i = s32 (applier does movd+cvtdq2ps)."""
import struct
CFG = r"D:\FFXII_TZA_extract\ps2data\sound\sead.win.config"
d = open(CFG, "rb").read()
CH = 0x250
STRIDE = [0, 0x80, 0x20, 0x10, 0x10, 0x10, 0, 0x10, 0, 0x10, 0x20]
tbl = CH + struct.unpack_from("<H", d, CH + 2)[0]
SEC = {}
for cid in range(11):
    so = CH + struct.unpack_from("<I", d, tbl + cid * 4)[0]
    SEC[cid] = so
SEC_END = {c: (SEC[c + 1] if c < 10 else None) for c in range(11)}


def shipped(cid, ofs, kind):
    so = SEC[cid]
    dofs = struct.unpack_from("<H", d, so + 2)[0]
    cnt = d[so + 4]
    if cnt == 0:
        return "no preset"
    vals = []
    for k in range(cnt):
        po = so + dofs + k * STRIDE[cid] + ofs
        v = struct.unpack_from("<i" if kind == "i" else "<f", d, po)[0]
        raw = struct.unpack_from("<I", d, po)[0]
        note = ""
        if SEC_END[cid] is not None and po >= SEC_END[cid]:
            note = " [OVERRUN: byte file+%#x lies in class %d's section header]" % (po, cid + 1)
        vals.append(("%d" % v if kind == "i" else "%.6g" % v) + " (0x%08X)" % raw + note)
    return "; ".join(vals)


H = ["class", "classId", "preset_ofs", "kind", "paramId", "member", "transform", "role", "evidence", "shipped", "confidence"]
R = []


def row(cls, cid, ofs, kind, pid, member, transform, role, ev, conf):
    R.append([cls, str(cid), "+0x%02X" % ofs, kind, pid, member, transform, role, ev, shipped(cid, ofs, kind), conf])


# ---- SurroundReverb (1): apply 007D5F50, setParam 007D5BD0 (jump table 007D5E70), commit 007D76E0, EQ 007D6CD0, process 007D3CB0 (state = obj+0x7D0)
S = "SurroundReverb"
row(S, 1, 0x00, "f", "0x00", "DV obj+0x18 -> [obj+0xBE0][i]", "x * 0.6^(len_i/len_0) per FDN line (007D7D8B..007D7DB0)",
    "late-reverb (FDN) input injection gain", "STATIC(code): 007D5F80; 007D5C07; 007D7D4B-007D7DB0; process 007D4DB2-007D4DF2 (line_in = gain_i * diffused input + matrix out)", "medium-high")
row(S, 1, 0x04, "f", "0x05", "DV obj+0x198", "max(v,1.0) (007D5C48); commit: x/30 (007D7CFB) scales every FDN line length: len_i = fs*tbl01CB7100[i]ms*0.001*x/30 (007D7D10-007D7D36)",
    "room size (delay-length scale; 30 = table lengths)", "STATIC(code): 007D5FED; 007D5C48; 007D7CA9-007D7D36; also in RT exponent 007D8005", "high")
row(S, 1, 0x08, "f", "0x01", "DV obj+0x48 -> [obj+0x7D0]", "none (linear)", "wet (reverb) output level",
    "STATIC(code): 007D5F92; 007D5C59; 007D7766; process 007D5502/007D5509 (EQ'd wet * x) + dry term", "high")
row(S, 1, 0x0C, "f", "0x02", "DV obj+0x78 -> [obj+0x7D4]", "none (linear)", "dry (direct) output level",
    "STATIC(code): 007D5FA8; 007D5C5F; 007D77B9; process 007D5529/007D5535 * input frame saved at 007D4805/007D480C", "high")
row(S, 1, 0x10, "f", "0x08", "DV obj+0xA8", "max(v,10) (007D5C65); commit 1/x (007D7FB5); g_i = 0.25*10^(-3*len_i_ms*size/30/x) (007D7FF3-007D802C) -> [obj+0xBE8][i]",
    "decay time RT60 in milliseconds (FDN feedback gains)", "STATIC(code): 007D6029; 007D5C65; 007D7ED4-007D802C", "high")
row(S, 1, 0x14, "f", "0x09", "DV obj+0xD8", "min(v,0.99) (007D5C76); alpha=0.4+0.6*(1-x) (007D7F96-007D7FCF); b_i=log10(g_i)*ln10/4*(1-1/alpha^2) (007D7FDC-007D8027) -> [obj+0x924+4i], 1-b -> [obj+0x964+4i]; tone-correction [obj+0x9A8] (007D8064-007D80C0)",
    "HF damping amount (0 = none; sets HF/LF decay ratio alpha from 1.0 down to 0.406)", "STATIC(code): 007D603F; 007D5C76; 007D7F26-007D80C0; process one-pole per line 007D4CD0-007D4D1E", "medium-high")
row(S, 1, 0x18, "f", "0x0A", "DV obj+0x108 -> [obj+0x8DC]/[0x8EC]/[0x8FC]", "x*0.88, x*0.85, x*0.78 (007D7E0E/007D7E69/007D7EC4)",
    "input diffusion (coefficients of 3 series Schroeder all-passes, fixed delays 367/512/1179 samples)", "STATIC(code): 007D605B; 007D5C87; 007D7DC3-007D7ECC; process 007D4B9D-007D4C86; delays 007D41DD/007D41EA/007D42AC", "high")
row(S, 1, 0x1C, "f", "0x04", "DV obj+0x168 -> [obj+0x80C]", "none", "early-reflection level (scales the ER tap-network signal into the wet sum)",
    "STATIC(code): 007D5FD7; 007D5C93; 007D780C; process 007D3D18 -> [rbp+0x560]; 007D4BF8/007D4C56", "medium")
row(S, 1, 0x20, "f", "0x07", "DV obj+0x1F8 -> [obj+0x920]", "none", "late-reverb level (scales the diffused path and the FDN sum)",
    "STATIC(code): 007D6019; 007D5C9F; 007D78C0; process 007D3D33 -> [rbp+0x150]; 007D4CAC/007D4CB8, 007D4D4F/007D4D53", "medium")
row(S, 1, 0x24, "f", "0x06", "DV obj+0x1C8 -> int [obj+0x7D8]", "x*fs*0.001, clamped < 24000 -> 23999 (007D5CAB-007D5CD4); cvttss2si (007D785F)",
    "pre-delay in milliseconds (read = write - x samples in the 24000-frame input buffer)", "STATIC(code): 007D6003; 007D5CAB; 007D7863; process 007D42BA-007D42C7 (wrap 0x5DC0)", "high")
bands = [(0x28, 0x2C, 0x30, 0x34, "0x0C", "0x0D", "0x0E", "0x0F", "0x228", "0x258", "0x288", "007D0EA0 high-pass", "007D6D63-007D6DC0", 1),
         (0x38, 0x3C, 0x40, 0x44, "0x10", "0x11", "0x12", "0x13", "0x2B8", "0x2E8", "0x318", "007D1330 peaking", "007D6DC5-007D6EC8", 2),
         (0x48, 0x4C, 0x50, 0x54, "0x14", "0x15", "0x16", "0x17", "0x348", "0x378", "0x3A8", "007D1330 peaking", "007D6ECD-007D6FD0", 3),
         (0x58, 0x5C, 0x60, 0x64, "0x18", "0x19", "0x1A", "0x1B", "0x3D8", "0x408", "0x438", "007D1330 peaking", "007D6FD5-007D70D8", 4),
         (0x68, 0x6C, 0x70, 0x74, "0x1C", "0x1D", "0x1E", "0x1F", "0x468", "0x498", "0x4C8", "007D1080 low-pass", "007D70DD-007D718B", 5)]
for t, f, q, g, pt, pf, pq, pg, df, dq, dg, design, ev, n in bands:
    if n == 5:
        row(S, 1, t, "i", "(none)", "-", "NOT READ: the applier sends paramId 0x1C from +0x58 (007D61ED), a copy-paste slip; moot because 0x1C is a no-op",
            "EQ band 5 type code (ignored; band 5 is hardwired low-pass)", "STATIC(code): 007D61ED reads [rbx+0x58] for 0x1C; no load of [rbx+0x68] in 007D5F50", "high")
    else:
        row(S, 1, t, "i", pt, "-", "setParam case is the no-op epilogue 007D5E5F (jump table 007D5E70)",
            "EQ band %d type code (ignored; design is hardwired: %s)" % (n, design), "STATIC(code): apply movd+cvtdq2ps; 007D5E70[%s] -> 007D5E5F" % pt, "high")
    row(S, 1, f, "f", pf, "DV obj+%s" % df, "w = x * 2pi/fs (007D6D08-007D6D18, mulss xmm10)", "EQ band %d frequency Hz (%s)" % (n, design),
        "STATIC(code): %s" % ev, "high")
    row(S, 1, q, "f", pq, "DV obj+%s" % dq, "passed as the design's xmm2: alpha = sin(w)*0.5*x", "EQ band %d bandwidth as 1/Q (1.414 -> Q 0.707)" % n,
        "STATIC(code): %s; 007D10E1/007D0EFF/007D138F" % ev, "high")
    if n in (1, 5):
        row(S, 1, g, "f", pg, "DV obj+%s" % dg, "ramped by update 007D6270 only; never passed to a design", "EQ band %d gain slot - value never consumed (HP/LP designs take no gain)" % n,
            "STATIC(code): update 007D658C/007D689C read its duration; no consumer in 007D6CD0/007D76E0/007D3CB0", "high (unused)")
    else:
        row(S, 1, g, "f", pg, "DV obj+%s" % dg, "passed as xmm3 = A of the RBJ peaking design (1/A at 007D138A, A at 007D13C7)", "EQ band %d peak gain A (linear, 1.0 = flat)" % n,
            "STATIC(code): %s" % ev, "high")
row(S, 1, 0x78, "i", "0x03", "int [obj+0x7C8] -> [obj+0x7EC]", "cvttss2si (007D5C2E); commit indexes 01CB7180 (ER tap ms, 2x19 per type, *fs*0.001) and 01CB73F0 (19 ER gains per type)",
    "early-reflection pattern selector (room type index)", "STATIC(code): 007D5FB8; 007D5C2E; 007D78B4-007D7C93; taps read 007D4840-007D49D7", "high (selector); per-type meaning not determined")
row(S, 1, 0x7C, "f", "0x0B", "DV obj+0x138", "stored by 007D5CE0; not ramped by update; read only by getParam 007D36EB",
    "role not determined (no DSP consumer: dead parameter)", "STATIC(code): 007D6071; 007D5CE0; sweep of 007D2150..007D80D1 finds no other access", "high (unused)")

# ---- Compressor (2): apply 007D8F70, setParam 007D8E40 (jt 007D8F44), commit 007D9200, process 007D8BE0 (state obj+0x148)
C = "Compressor"
row(C, 2, 0x00, "f", "0x100", "DV obj+0x18 -> [obj+0x148]", "dB->lin: expf(x*0.1151293=ln10/20) (007D8E79/007D8E81)", "threshold (dB)",
    "STATIC(code): 007D8FA0; 007D9252; process xmm9 007D8C3A, over=g|x|-T 007D8CFD", "high")
row(C, 2, 0x04, "f", "0x101", "DV obj+0x48 -> [obj+0x14C]", "none", "static-curve slope S above threshold (= 1/ratio): y=|x|+min((S-1)(g|x|-T),0); S>1 expands below threshold",
    "STATIC(code): 007D8FB5; 007D8EA8; 007D9292; process 007D8CDD-007D8D1C", "high (math); name inferred from the curve")
row(C, 2, 0x08, "f", "0x102", "DV obj+0x78 -> [obj+0x150]", "dB->lin (007D8ECA)", "input gain (dB): scales the detector level, and the output too when no side-chain is bound",
    "STATIC(code): 007D8FCB; 007D92E7; process 007D8CEF/007D8CF6 (detector), 007D8C81 (output, no side-chain)", "high")
row(C, 2, 0x0C, "f", "0x103", "DV obj+0xA8 -> [obj+0x154]", "dB->lin (007D8EDD)", "make-up / output gain (dB)",
    "STATIC(code): 007D8FE1; 007D933C; process 007D8C31, out=in*gain*env 007D8DBA-007D8DD4", "high")
row(C, 2, 0x10, "f", "0x104", "DV obj+0xD8 -> [obj+0x158]", "ms*0.001 (007D8EF3); coef=expf(-2/(t*fs)) or 0 if t<=0 (007D93E8-007D9401); fs=[obj+0x138] from ctor arg (007AC94E-007AC95D)",
    "attack time (ms): coefficient used while gain is falling (G<env)", "STATIC(code): 007D8FF7; 007D9344-007D9401; process 007D8D6E-007D8DB2", "high")
row(C, 2, 0x14, "f", "0x105", "DV obj+0x108 -> [obj+0x15C]", "ms*0.001 (007D8F04); coef=expf(-1/(t*fs)) or 0 (007D94A8-007D94C1)",
    "release time (ms): coefficient used while gain is rising", "STATIC(code): 007D900D; 007D9409-007D94D1; process 007D8D6E-007D8DB2", "high")
row(C, 2, 0x18, "i", "0x106", "int [obj+0x13C]", "cvttss2si (007D8F18)", "side-chain source bus index",
    "STATIC(code): 007D901D; 007D94CB -> 007AC3E0(mixer 02EAD0A8, bus, slot): [[mixer+8]+bus*8]", "high")
row(C, 2, 0x1C, "i", "0x107", "int [obj+0x140]", "cvttss2si (007D8F24)", "side-chain source insert slot (0..3); bound only if that insert's classId is 4 (SideChainInput)",
    "STATIC(code): 007D9036; 007D94C4; 007AC3E9 (slot<=3); 007D9500 cmp eax,4 -> [obj+0x168]; process reads it via 007D8210", "high")

# ---- Filter (3): apply 007D1970, setParam 007D1840, type 007D16C0, commit 007D1C80 (jt 007D1EB0)
F = "Filter"
row(F, 3, 0x00, "i", "0x203", "int [obj+0x18] (staged [obj+0x1C])", "cvttss2si (007D1882) -> 007D16C0 (cross-fades a type change)",
    "biquad design selector: 0 identity, 1 LP, 2 HP, 3 BP, 4 notch, 5 low shelf, 6 gain-taking design 007D0F60 (not classified), 7 peaking, 8 all-pass",
    "STATIC(code): 007D19A0; 007D1882; commit switch 007D1CF2 -> 007D1CFE/007D1080/007D0EA0/007D0DD0/007D1280/007D1140/007D0F60/007D1330/007D0D30", "high")
row(F, 3, 0x04, "f", "0x200", "DV obj+0x38", "commit: w = x*2pi*(1/fs) (007D1CCE/007D1CDA, 1/fs at 01F41D18)", "cutoff / centre frequency (Hz)",
    "STATIC(code): 007D19B8; 007D1904-007D1932; 007D1C86-007D1CDA", "high")
row(F, 3, 0x08, "f", "0x201", "DV obj+0x68", "reciprocal: 1/x, x==0 -> 1 (007D18BF-007D18D4)", "Q (stored as 1/Q; alpha = sin(w)*0.5/Q)",
    "STATIC(code): 007D19CE; 007D18D4; 007D10BB-007D10E1", "high")
row(F, 3, 0x0C, "f", "0x202", "DV obj+0x98", "none", "shelf/peak gain A (linear RBJ A, 1.0 = flat); used by types 5-7 only",
    "STATIC(code): 007D19E4; 007D18A3; 007D1DD0-007D1E7F; 007D119B (sqrt A), 007D138A (1/A)", "high")

# ---- SideChainInput (4): apply 007D8540, setParam 007D8500, commit 007D8580, process 007D82E0 (state obj+0x48)
SC = "SideChainInput"
row(SC, 4, 0x00, "f", "0x300", "DV obj+0x18 -> [obj+0x54]", "none", "side-chain capture gain (sc = in*x + [obj+0x58])",
    "STATIC(code): 007D8557; 007D851E; 007D8596-007D85CA; process 007D83A9/007D83FA", "high")
for o in (0x04, 0x08, 0x0C):
    row(SC, 4, o, "f", "(none)", "-", "not read by the applier 007D8540", "padding (no applier read)", "STATIC(code): 007D8540 reads only [rdx]", "high")

# ---- SimpleFilter (5): apply 007D9870 (shared with Flanger's slot), setParam 007D97F0, commit 007D98F0, process 007D9770
SF = "SimpleFilter"
row(SF, 5, 0x00, "i", "0x401", "int [obj+0x48]", "cvttss2si (007D980E)",
    "one-pole mode: 0 bypass (a=0,b=1), 1 low-pass a=exp(-2pi f/fs), 2 a=exp(2pi f/fs - pi) (role not determined), other: coefficients left unchanged",
    "STATIC(code): 007D98A0; 007D9812; commit 007D9939-007D9992; process y=(1-a)x+a*y1 007D97A0-007D97C5", "high (0/1); mode 2 not determined")
row(SF, 5, 0x04, "f", "0x400", "DV obj+0x18", "clamped to [fs/4800, fs/2] (007D9826-007D983B; ctor 007D95B0-007D95CF)", "cutoff frequency (Hz)",
    "STATIC(code): 007D98B8; 007D9826; commit 007D9931-007D9979", "high")
for o in (0x08, 0x0C):
    row(SF, 5, o, "f", "(none)", "-", "not read by the applier 007D9870", "padding (no applier read)", "STATIC(code): 007D9870 reads [rdx], [rdx+4]", "high")

# ---- GranularPitchShift (7): apply 007DA900 (shared with HilbertFilter's slot), setParam 007DA8A0, commit 007DAA00, process 007DA2E0 (state obj+0x78)
G = "GranularPitchShift"
row(G, 7, 0x00, "f", "0x600", "DV obj+0x18 -> [obj+0x78]", "none", "pitch ratio (read pointer advances x samples per sample; tap delay changes by 1-x per sample)",
    "STATIC(code): 007DA930; 007DA8C7; 007DAA46; process 007DA355, 007DA421-007DA444, 007DA48F", "high")
row(G, 7, 0x04, "f", "0x601", "DV obj+0x48 -> [obj+0x7C]", "x / fs (007DAA83-007DAA93)", "grain rate (Hz): phase increment per sample, wraps at 1.0; grain period = fs/x samples; two taps at phase 0.25/0.75 cross-faded by (sin(2pi phase)+1)/2",
    "STATIC(code): 007DA945; 007DA8C1; 007DAA93; process 007DA3E0-007DA3EB, 007DA393, 007DA501-007DA545", "high")
for o in (0x08, 0x0C):
    row(G, 7, o, "f", "(none)", "-", "not read by the applier 007DA900", "padding (no applier read)", "STATIC(code): 007DA900 reads [rdx], [rdx+4]", "high")

# ---- nop arm (9): no class; stride 0x10 but no insert object is ever built for it (bus insert jump table arm)
for o in (0x00, 0x04, 0x08, 0x0C):
    row("(nop arm)", 9, o, "f", "-", "-", "no insert class to apply it", "role not determined (no consumer class)", "page: classId 9 arm of 0x68CCF0 is a nop", "n/a")

# ---- BuildReverb (10): apply 007DC340 (flag = section byte +5 gates fields), setParam 007DC1F0 (jt 007DC318), process 007DB8D0 (this = obj+8)
B = "BuildReverb"
row(B, 10, 0x00, "f", "0x1000", "DV obj+0x490", "clamp [0,1] (007DC21D-007DC230)", "master scale 0..1: multiplies wet level, pre-delay, RT60 and the damping-cutoff term (0 = no wet path)",
    "STATIC(code): 007DC36E; process 007DB8EF-007DB97F -> xmm8; uses 007DBA2D, 007DBB4F, 007DBC18, 007DBCAF", "medium (composite role)")
row(B, 10, 0x04, "f", "0x1001", "DV obj+0x4C0", "clamp [0,1]; default 1.0 when flag==0 (007DC382-007DC396)", "dry level",
    "STATIC(code): 007DC38F; process 007DB984-007DB9DD -> [rsp+0x40]; 007DBEAD/007DBEB7 (dry frame * x) added 007DBF07", "high")
row(B, 10, 0x08, "f", "0x1002", "DV obj+0x4F0", "clamp [0,1]; default 1.0 when flag==0", "wet output level (times +0x00)",
    "STATIC(code): 007DC3AF; process 007DB9E2-007DBA39 -> [rsp+0x30]; 007DBEF7/007DBF0B", "high")
row(B, 10, 0x0C, "f", "0x1003", "DV obj+0x520", "clamp [0,1]; default 1.0", "early-reflection level (16 fixed taps, ctor tables 01CB7A40 s / 01CB7A80 gains)",
    "STATIC(code): 007DC3CF; process 007DBA3E-007DBA99 -> xmm15; 007DBEBD/007DBED5 on the tap sum 007DBD40-007DBD72", "high")
row(B, 10, 0x10, "f", "0x1004", "DV obj+0x550", "clamp [0,1]; default 0.2 (008F30F8)", "late (comb/all-pass tail) level",
    "STATIC(code): 007DC3F2; process 007DBA89-007DBAF5 -> [rsp+0x20] -> xmm13 (007DBCF8); 007DBED9/007DBEEB on the delayed tail", "high")
row(B, 10, 0x14, "f", "0x1005", "DV obj+0x580", "clamp [0,0.1]; default 0.08 (0090035C); samples = x*(+0x00)*fs (007DBB4F-007DBB5F)", "late-tail pre-delay in seconds (buffer 0.11*fs, ctor 007DB600)",
    "STATIC(code): 007DC417; process 007DBADD-007DBB7F", "high")
row(B, 10, 0x18, "f", "0x1006", "DV obj+0x5B0", "max(x,0); default 2.0 (01CEBC08); g_i = 10^(-3*d_i/(x*(+0x00))) with d_i = 01CB7A00[i] s (0.050..0.078) (007DBC5A-007DBCC1)", "reverb time RT60 in seconds (6 comb feedback gains)",
    "STATIC(code): 007DC43C; process 007DBC5A-007DBCD7; comb loop 007DBDE1/007DBDE5", "high")
row(B, 10, 0x1C, "f", "0x1007", "DV obj+0x5E0", "clamp [2000,20000]; needs flag>=2 else 2000 (007DC45C-007DC469); a_i = exp(-2pi*(x-01CB7A18[i])*(+0x00)/fs) (007DBBC0-007DBC35)", "comb-feedback low-pass (damping) cutoff in Hz",
    "STATIC(code): 007DC462; process 007DBBC0-007DBC56; comb loop 007DBDC7-007DBDED", "high")

with open(__file__.rsplit("\\", 1)[0] + "\\fields.tsv", "w", encoding="utf-8", newline="\n") as fo:
    fo.write("\t".join(H) + "\n")
    for r in R:
        fo.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
print("rows", len(R))
from collections import Counter
print(Counter(r[0] for r in R))
