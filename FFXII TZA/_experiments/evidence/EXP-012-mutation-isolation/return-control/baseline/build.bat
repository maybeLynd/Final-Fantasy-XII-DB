@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
cl /nologo /W4 /O2 /Brepro /D_CRT_SECURE_NO_WARNINGS /Fe:"group_completion_mut.exe" "group_completion_driver.c" "C:\Users\Kristian\AppData\Local\Temp\ffxii-mutation-cases\case-ktc0ohzt\Game\Spawn\group_completion.c" /link /Brepro
