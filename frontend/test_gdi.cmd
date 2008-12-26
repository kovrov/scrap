@echo off

set PATH=c:\soft\DigitalMars\dmd2\bin;%PATH%
set GUI=-L/EXETYPE:NT/SUBSYSTEM:WINDOWS:4.0
@rem set GUI=-L/EXETYPE:NT/SUBSYSTEM:CONSOLE


dmd %GUI% -g -debug test_gdi.d sys.d ui.d widget.d -run gdi.d

IF ERRORLEVEL 1 GOTO ERROR
GOTO END

:ERROR
pause

:END
