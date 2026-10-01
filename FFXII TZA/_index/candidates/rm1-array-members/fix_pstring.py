"""RM-1 close-out: PString +0 is one 8-byte tagged pointer, m_buffer, not a 1-byte `chars` field (OPUS, 2026-09-27).

The 2026-09-21 row came from the c_str script accessor's first instruction, `movzx edx, byte ptr [rcx]`, read as the
field's width. The whole adapter 006A77F0 is `movzx edx, byte [rcx] / mov rax, qword [rcx] / and edx, 1 / sub rax, rdx
/ ret`: it loads the full qword and subtracts its low bit, so the byte read is the pointer's tag bit and the field is
the 8-byte pointer. Three routes agree: the registrar 006A72B0 names the member at +0 `m_buffer`; the packed namespace
marks PString::m_buffer as the file's one pointer member (attribute bit 31); and FindShaderParameter 0018D240 strips
the same low bit from a PString (PShaderParameterDefinition::m_name) before dereferencing it (0018D270). The class is
8 bytes, so the member closes it. Idempotent; --check verifies without writing.
"""
import pathlib, sys

DB = pathlib.Path(__file__).resolve().parents[3]
F = DB / "_types" / "fields.tsv"
MARK = "TAGGED POINTER, RM-1 close-out 2026-09-27 (OPUS)"


def parse(l):
    b = l.rstrip("\r\n"); return b.split("\t"), l[len(b):] or "\n"


def main():
    check = "--check" in sys.argv
    lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
    rows = [(i, parse(l)[0]) for i, l in enumerate(lines) if l.startswith("PString\t")]
    if any(MARK in c[8] for _, c in rows):
        print("already applied"); return
    if not (len(rows) == 2 and rows[0][1][1] in ("0x0000", "0x000") and rows[0][1][2] == "1" and rows[0][1][3] == "chars"
            and rows[1][1][3] == "unobservedSpan0001" and rows[1][1][2] == "7"):
        print("REFUSED: PString rows are not the expected 1 + 7 pair", [c[:4] for _, c in rows]); sys.exit(1)
    if check:
        print("CHECK OK"); return
    (i0, c0), (i1, c1) = rows
    eol = parse(lines[i0])[1]
    c0[2], c0[3], c0[4] = "8", "m_buffer", "char* (tagged: bit 0)"
    c0[5] = ("THE STRING'S CHARACTER BUFFER, an 8-byte pointer whose bit 0 is a tag: c_str (006A77F0) returns the qword minus"
             " its low bit. The one-byte read that named this row 'chars' is that tag bit.")
    c0[6], c0[7] = "TYPE RESOLVED", "PROVEN"
    c0[8] = (MARK + ": widened from 1 byte ('chars', uint8) to the whole class and absorbs unobservedSpan0001 (7 bytes)."
             " 006A77F0 movzx edx,byte[rcx] / mov rax,qword[rcx] / and edx,1 / sub rax,rdx; registrar 006A72B0 names member"
             " +0 m_buffer; the packed namespace marks PString::m_buffer as a pointer (attribute bit 31); 0018D270 strips"
             " the same bit from PShaderParameterDefinition::m_name. || previous chars row: " + c0[8] +
             " || previous unobservedSpan0001 row: " + c1[8])
    lines[i0] = "\t".join(c0) + eol
    lines[i1] = ""
    F.write_bytes("".join(lines).encode("utf-8")); print("applied")


if __name__ == "__main__":
    main()
