#!/bin/bash
# opx_export.sh up|down - a clean extract of HEAD at /c/w/opx (Tools/work junctioned) for OPUS's A-drift repair runs
R=/c/Users/Kristian/source/repos/XIIOnline
X=/c/w/opx
if [ "$1" = up ]; then
  cd "$R"
  if [ -e $X ]; then echo "exists $X"; exit 1; fi
  mkdir -p $X
  git archive HEAD "Database/FFXII TZA" "Database/Tools/analysis-kit/gfz-scripts" | tar -x -C $X
  powershell -NoProfile -Command "New-Item -ItemType Junction -Path 'C:\w\opx\Database\Tools\work' -Target 'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work' | Out-Null"
  echo "HEAD $(git rev-parse --short=9 HEAD)"
elif [ "$1" = down ]; then
  powershell -NoProfile -Command "cmd /c rmdir 'C:\w\opx\Database\Tools\work'"
  [ -e $X/Database/Tools/work ] && { echo "junction still present - not deleting"; exit 1; }
  rm -rf $X
  echo removed
fi
