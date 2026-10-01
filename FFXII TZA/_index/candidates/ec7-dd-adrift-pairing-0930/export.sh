#!/bin/bash
# export.sh DIR [REV] - clean export of REV (default HEAD) DB + kit under a short root, work/ junctioned to the live work dir
set -e
R=/c/Users/Kristian/source/repos/XIIOnline
X=$1; REV=${2:-HEAD}
cd "$R"
if [ -e "$X/Database/Tools/work" ]; then
  powershell -NoProfile -Command "cmd /c rmdir '$(cygpath -w $X)\Database\Tools\work'"
fi
[ -e "$X/Database/Tools/work" ] && { echo "junction still present"; exit 1; }
rm -rf "$X" && mkdir -p "$X"
git archive $REV "Database/FFXII TZA" "Database/Tools/analysis-kit/gfz-scripts" | tar -x -C "$X"
powershell -NoProfile -Command "New-Item -ItemType Junction -Path '$(cygpath -w $X)\Database\Tools\work' -Target 'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work' | Out-Null"
echo "exported $(git rev-parse --short=9 $REV) to $X"
