"""Controls for reg_tracking.op_kind (memory access direction) and written() (receiver kills).

OPUS, 2026-09-24. The field-access index shipped 238 reversed labels: 198 `movups [m], xmm`
stores labelled r and 40 `test byte ptr [m], reg` compares labelled w, because op_kind trusted
capstone's operand flags and fell back to operand position when there was none. The whole-image
comparison against a second decoder lives in opkind_vs_iced.py and
regwrites_vs_iced.py (this directory) (0 disagreements over 728,535 memory operands / 1,775,860 instructions after
the repair). These controls pin the classes that were wrong, in both directions, without iced.

    python -m unittest test_reg_tracking -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import capstone  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402

import reg_tracking as RT  # noqa: E402

MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
MD.detail = True


def one(hexbytes):
    return next(MD.disasm(bytes.fromhex(hexbytes), 0x1000))


def kinds(hexbytes):
    i = one(hexbytes)
    return [RT.op_kind(i, o, n) for n, o in enumerate(i.operands) if o.type == X86_OP_MEM]


class PositiveStores(unittest.TestCase):
    """Stores must read w - including the forms capstone flags READ."""
    CASES = {
        "0f1106": "movups [rsi], xmm0 (capstone: READ; 198 index rows)",
        "660f1106": "movupd [rsi], xmm0 (capstone: READ)",
        "c5f81106": "vmovups [rsi], xmm0 (capstone: READ)",
        "660fd606": "movq [rsi], xmm0 (capstone: READ)",
        "0f1706": "movhps [rsi], xmm0 (capstone: READ)",
        "0f1306": "movlps [rsi], xmm0 (capstone: READ)",
        "0f2b06": "movntps [rsi], xmm0 (capstone: READ)",
        "660f3a160601": "pextrd [rsi], xmm0, 1 (capstone: READ)",
        "660f3a170601": "extractps [rsi], xmm0, 1 (capstone: READ)",
        "0f9506": "setne [rsi]",
        "8906": "mov [rsi], eax",
        "0f2906": "movaps [rsi], xmm0",
        "f30f1106": "movss [rsi], xmm0",
    }

    def test_stores_are_writes(self):
        for h, what in self.CASES.items():
            with self.subTest(what):
                self.assertEqual(kinds(h), ["w"])


class NegativeReads(unittest.TestCase):
    """Loads and compares must read r - never w, whatever position the operand is in."""
    CASES = {
        "40847310": "test byte ptr [rbx+0x10], sil (capstone: no flag -> was w; 40 index rows)",
        "847310": "test byte ptr [rbx+0x10], dh (capstone: no flag)",
        "66854310": "test word ptr [rbx+0x10], ax (capstone: no flag)",
        "48854310": "test qword ptr [rbx+0x10], rax",
        "833e00": "cmp dword ptr [rsi], 0",
        "0fba2601": "bt dword ptr [rsi], 1",
        "0f1006": "movups xmm0, [rsi]",
        "8b06": "mov eax, [rsi]",
        "f30f7e06": "movq xmm0, [rsi]",
        "0f4506": "cmovne eax, [rsi]",
    }

    def test_reads_are_reads(self):
        for h, what in self.CASES.items():
            with self.subTest(what):
                self.assertEqual(kinds(h), ["r"])


class ReadModifyWrite(unittest.TestCase):
    """A writer query must include rw: these both read and write the field."""
    CASES = {
        "83604000": "and dword ptr [rax+0x40], 0",
        "ff06": "inc dword ptr [rsi]",
        "0fba3601": "btr dword ptr [rsi], 1",
        "8706": "xchg [rsi], eax",
        "f00fb10e": "lock cmpxchg [rsi], ecx (capstone: READ only)",
        "0fc106": "xadd [rsi], eax",
    }

    def test_rmw(self):
        for h, what in self.CASES.items():
            with self.subTest(what):
                self.assertEqual(kinds(h), ["rw"])


class AddressOnly(unittest.TestCase):
    def test_lea_nop_prefetch_touch_nothing(self):
        for h, what in {"488d4e10": "lea rcx, [rsi+0x10]",
                        "0f1f00": "nop dword ptr [rax]",
                        "0f1806": "prefetchnta [rsi]",
                        "0f0d4e10": "prefetchw [rsi+0x10]"}.items():
            with self.subTest(what):
                self.assertEqual(kinds(h), ["addr"])


class StringOps(unittest.TestCase):
    def test_rep_movs_reads_source_writes_destination(self):
        self.assertEqual(kinds("f348a5"), ["w", "r"])


class ReceiverOverwrite(unittest.TestCase):
    """written(): a missed kill credits accesses to an object the register no longer holds."""

    def test_cmpxchg_kills_rax(self):
        self.assertIn("rax", RT.written(one("f00fb10e")))

    def test_cmpxchg16b_kills_rdx_rax(self):
        self.assertTrue({"rax", "rdx"} <= RT.written(one("f0480fc70e")))

    def test_load_through_receiver_kills_it(self):
        self.assertIn("rcx", RT.written(one("488b4908")))   # mov rcx, [rcx+8]

    def test_byte_write_kills_parent(self):
        self.assertIn("r8", RT.written(one("41b003")))      # mov r8b, 3

    def test_cdq_cqo_do_not_kill_rax(self):
        for h in ("99", "4899"):
            w = RT.written(one(h))
            self.assertIn("rdx", w)
            self.assertNotIn("rax", w)

    def test_test_kills_no_gpr(self):
        for h in ("a9f3ffffff", "4885db", "40847310"):     # test eax,imm / test rbx,rbx / test [m],sil
            self.assertEqual(RT.written(one(h)) & RT._GPR64, set())


class NoPositionalGuess(unittest.TestCase):
    def test_unflagged_operand_is_unknown_not_write(self):
        class Op(object):
            access = 0
        i = one("8b06")
        i_mn = type("I", (), {"mnemonic": "fakeop"})()
        self.assertEqual(RT.op_kind(i_mn, Op(), 0), "?")
        self.assertEqual(RT.op_kind(i, i.operands[1], 1), "r")


if __name__ == "__main__":
    unittest.main()
