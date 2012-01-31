GOTO EndComment
This script was written to get the status of Sun Hardware via IPMI in Window Server 2003.
The output is returned in a format which check_mk can understand. It's a bit of a hack
but it works!
Hereward Cooper - Sometime 2011
:EndComment
@echo off
set COUNT=

:: Retrieve every "ON" alarm from sunoem
C:\ipmiutil.exe sunoem sbled get 2> nul | find /C "ON" > C:\nrpe_nt\sun.txt

:: Count the alarms, and if there are more than 2 print an alert, otherwise print an OK.
:: (this vaule of 2 will depend on specific IPMI/Sun configuration, but on the server here
:: there are two 'alarms' which are set to ON when in a fault-free state).
for /F %%A in (C:\nrpe_nt\sun.txt) do set COUNT=%%A
IF %COUNT% EQU 2 (echo 0 Sun_Hardware - OK: 0 Alarms Detected) ELSE (echo 2 Sun_Hardware - CRITICAL: Alarms Detected)
