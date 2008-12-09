@echo off

set PATH=c:\soft\DigitalMars\dmd2\bin;%PATH%
dmd event.d sys.d -run test_gdi.d

IF ERRORLEVEL 1 GOTO ERROR
GOTO END

:ERROR
pause

:END
