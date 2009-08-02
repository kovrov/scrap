@echo off

set PATH=C:\soft\digitalmars\dmd2\bin;%PATH%
set GUI=-L/EXETYPE:NT/SUBSYSTEM:WINDOWS:4.0
set VER=-version=WindowsXP

dmd %GUI% %VER% -g -debug test_gdi.d sys.d ui.d widget.d -run gdi.d

IF ERRORLEVEL 1 GOTO ERROR
GOTO END

:ERROR
pause

:END
