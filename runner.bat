@echo off
setlocal

:: Set container names
set HAMMER_CONTAINER=HammerDB_SBD

echo Starting HammerDB benchmark runner...

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Setup containers
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Compose down to ensure a clean start
echo Stopping and removing existing containers and volumes...
docker compose down -v

timeout /t 5

:: Compose up to start the containers
echo Starting containers...
docker compose up -d

timeout /t 10

echo Containers are up and running!

echo Starting HammerDB benchmark...

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: POSTGRESQL
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo Starting up PostgreSQL benchmark...

:: Start the stats logging in a new window using the temp file
start "PCStats" cmd /c PCStats.bat "postgres"

timeout /t 5 >nul

docker exec -i %HAMMER_CONTAINER% /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestPG.tcl

for /f "tokens=2 delims=," %%i in ('tasklist /v /fo csv ^| findstr /i /c:"PCStats"') do (
    taskkill /PID %%~i /F >nul 2>&1
)

echo Benchmark and monitoring complete for PostgreSQL.

timeout /t 30

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: MYSQL
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo Starting up MySQL benchmark...

:: Start the stats logging in a new window using the temp file
start "PCStats" cmd /c PCStats.bat "mysql"

timeout /t 5 >nul

docker exec -i %HAMMER_CONTAINER% /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestMySQL.tcl

for /f "tokens=2 delims=," %%i in ('tasklist /v /fo csv ^| findstr /i /c:"PCStats"') do (
    taskkill /PID %%~i /F >nul 2>&1
)

echo Benchmark and monitoring complete for MySQL.

timeout /t 30

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: MARIADB
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo Starting up MariaDB benchmark...

:: Start the stats logging in a new window using the temp file
start "PCStats" cmd /c PCStats.bat "mariadb"

timeout /t 5 >nul

docker exec -i %HAMMER_CONTAINER% /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestMariaDB.tcl

for /f "tokens=2 delims=," %%i in ('tasklist /v /fo csv ^| findstr /i /c:"PCStats"') do (
    taskkill /PID %%~i /F >nul 2>&1
)

echo Benchmark and monitoring complete for MariaDB.

echo Stopping and removing existing containers and volumes...

docker compose down -v

echo Benchmark and monitoring complete.
endlocal