@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /W4 /O2 /Brepro /D_CRT_SECURE_NO_WARNINGS /Fe:"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\ASTRA\group-validator\baseline-ohm0ja40\group-driver.exe" "C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\ASTRA\group-validator\baseline-ohm0ja40\Tests\Differential\group_completion_driver.c" "C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\ASTRA\group-validator\baseline-ohm0ja40\Game\Spawn\group_completion.c" /link /Brepro
