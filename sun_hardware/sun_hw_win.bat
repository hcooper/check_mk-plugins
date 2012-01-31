@echo off
set COUNT=
C:\ipmiutil.exe sunoem sbled get 2> nul | find /C "ON" > C:\nrpe_nt\sun.txt
for /F %%A in (C:\nrpe_nt\sun.txt) do set COUNT=%%A
IF %COUNT% EQU 2 (echo 0 Sun_Hardware - OK: 0 Alarms Detected) ELSE (echo 2 Sun_Hardware - CRITICAL: Alarms Detected)
