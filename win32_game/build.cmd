@echo off

rem PATH=C:\soft\digitalmars\dmd2\bin;%PATH%
@set PATH=C:\soft\digitalmars\dmd\bin;%PATH%
make

IF ERRORLEVEL 2 GOTO END

test.exe

:END
pause
