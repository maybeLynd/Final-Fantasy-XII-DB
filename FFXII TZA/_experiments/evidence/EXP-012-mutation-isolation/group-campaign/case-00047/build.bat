@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /W4 /O2 /Brepro /D_CRT_SECURE_NO_WARNINGS /Fe:"group_completion_mut.exe" "group_completion_driver.c" "C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\EXP-012-mutation-isolation\group-campaign\scratch\case-u9tikeku\Game\Spawn\group_completion.c" /link /Brepro
