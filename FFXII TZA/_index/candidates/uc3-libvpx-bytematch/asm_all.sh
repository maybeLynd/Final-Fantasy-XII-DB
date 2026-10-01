#!/bin/sh
# Assemble every x86 .asm file of libvpx 1.6.0 for win64 with yasm 1.3.0 (extracted into scratch).
S=/mnt/c/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/uc3
SRC=/mnt/c/Users/Kristian/AppData/Local/Temp/libvpx-1.6.0
Y=$S/root/usr/bin/yasm
mkdir -p $S/obj
cd $SRC
find . -name "*.asm" | grep -v -E "/(arm|mips|ppc)/|third_party|x86inc.asm|x86_abi_support.asm|vpx_config" | sort | while read f; do
  o=$S/obj/$(echo $f | sed 's#^\./##; s#/#__#g; s#\.asm$#.obj#')
  if $Y -f win64 -I$SRC/ -I$S/build/ -I$(dirname $f)/ -o $o $f 2> $o.err; then echo "OK $f"; else echo "FAIL $f"; head -3 $o.err; fi
done
