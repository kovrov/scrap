@echo off

set PATH=c:\soft\DigitalMars\dmd2\bin;%PATH%
set GUI=-L/EXETYPE:NT/SUBSYSTEM:WINDOWS:4.0
@rem set GUI=-L/EXETYPE:NT/SUBSYSTEM:CONSOLE


dmd %GUI% event.d sys.d -run test_gdi.d

IF ERRORLEVEL 1 GOTO ERROR
GOTO END

:ERROR
pause

:END
