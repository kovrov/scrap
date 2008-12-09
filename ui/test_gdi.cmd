@echo off

set PATH=c:\soft\DigitalMars\dmd2\bin;%PATH%
rem set GUI=-L/EXET:NT/SU:windows
dmd %GUI% event.d sys.d -run test_gdi.d

IF ERRORLEVEL 1 GOTO ERROR
GOTO END

:ERROR
pause

:END
