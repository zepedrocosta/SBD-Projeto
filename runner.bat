@echo off
setlocal

:: Set container names
set HAMMER_CONTAINER=HammerDB_SBD

set TCL_SCRIPT=scripts/tcl-scripts/largeTestPG.tcl

:: Start the stats logging in a new window using the temp file
@REM start "PCStats" cmd /c PCStats.bat "%TCL_SCRIPT%"
start "PCStats" cmd /c PCStats.bat

timeout /t 5 >nul

docker exec -i %HAMMER_CONTAINER% /home/HammerDB-4.10/hammerdbcli auto %TCL_SCRIPT%

for /f "tokens=2 delims=," %%i in ('tasklist /v /fo csv ^| findstr /i "PCStats"') do (
    taskkill /PID %%~i /F
)

echo Benchmark and monitoring complete.
endlocal