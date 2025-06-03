@echo off
setlocal

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: MUDAR ISTO!!!!
set TCL_SCRIPT=scripts/tcl-scripts/largeTestPG.tcl
set DATABASE=postgres
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Set container names
set HAMMER_CONTAINER=HammerDB_SBD

:: Start the stats logging in a new window using the temp file
start "PCStats" cmd /c PCStats.bat "%DATABASE%"

timeout /t 5 >nul

docker exec -i %HAMMER_CONTAINER% /home/HammerDB-4.10/hammerdbcli auto %TCL_SCRIPT%

for /f "tokens=2 delims=," %%i in ('tasklist /v /fo csv ^| findstr /i "PCStats"') do (
    taskkill /PID %%~i /F
)

echo Benchmark and monitoring complete.
endlocal