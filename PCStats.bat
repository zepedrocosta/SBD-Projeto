@echo off
setlocal enabledelayedexpansion

set DB=%1

:: Format date and time safely for filename
for /f "tokens=1-3 delims=/" %%a in ("%date%") do (
    set mm=%%a
    set dd=%%b
    set yyyy=%%c
)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set hh=%%a
    set min=%%b
    set ss=%%c
)
set "logfile=sys_usage_%mm%_%dd%_%hh%_%min%_%DB%.csv"

:: Set interval (in seconds)
set interval=10

:: Write CSV header
echo Timestamp,CPU_Usage_Percent,RAM_Used_MB > "%logfile%"

:loop
:: Get timestamp in ISO format using PowerShell
for /f %%x in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH:mm:ss"') do set timestamp=%%x

echo Current timestamp: %timestamp%

:: Get CPU usage
for /f "skip=1" %%x in ('wmic cpu get loadpercentage') do (
    if not "%%x"=="" (
        set cpu=%%x
        goto :gotCPU
    )
)
:gotCPU

:: Get RAM usage (in MB)
for /f "skip=1 tokens=1,2" %%a in ('wmic OS get FreePhysicalMemory^,TotalVisibleMemorySize /format:csv') do (
    set "free=%%a"
    set "total=%%b"
)
set /a usedMB=(%total% - %free%) / 1024

:: Write to CSV
echo %timestamp%,%cpu%,%usedMB% >> "%logfile%"

:: Wait and repeat
timeout /t %interval% >nul
goto loop
