#!/usr/bin/env python3
"""Repo-relative path constants derived from this file's location.

Fleet rule (OPUS-REQ-FRONTIER-KIT-SCRIPTS-HARDCODE-ONE-MACHINES-WORKING-TREE):
a kit script run with no arguments from inside a detached worktree must
measure THAT worktree, not the machine's primary checkout. Every constant
here derives from __file__, so a script sitting in the worktree resolves
into the worktree and the same script in the primary checkout resolves
into the primary checkout.

Import as `import kit_paths as KP` - the caller's script directory is on
sys.path automatically when invoked as `python script.py`.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
# Database/Tools/analysis-kit/gfz-scripts -> the repository root is four
# parents up.
ROOT = os.path.normpath(os.path.join(_HERE, os.pardir, os.pardir,
                                     os.pardir, os.pardir))
DATABASE = os.path.join(ROOT, "Database")
DB = os.path.join(DATABASE, "FFXII TZA")
TOOLS = os.path.join(DATABASE, "Tools")
WORK = os.path.join(TOOLS, "work")
GFZ_SCRIPTS = _HERE

# The shipping image, which seventeen scripts each located for themselves as
# os.path.join("..", "..", "work", "exe", "FFXII_TZA.exe") - a path relative to
# the CURRENT DIRECTORY, so they ran only when invoked from inside this folder
# and raised FileNotFoundError everywhere else. Three of them are gates, and a
# gate that crashes reports nothing, which is worse than one that reports a
# defect: check_route_extents, check_span_access and check_taken_address_writes
# were all silent for that reason until 2026-09-20. Derived from __file__ like
# everything else here, which is what the rule in the docstring above asks for.
EXE = os.path.join(WORK, "exe", "FFXII_TZA.exe")
