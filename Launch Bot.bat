@echo off
:Start
cd "C:\Users\pokem\Desktop\FICSITFelix\Servo Skull 1137\Scripts"
"C:\Users\pokem\Desktop\FICSITFelix\Servo Skull 1137\venv\Scripts\python.exe" "C:\Users\pokem\Desktop\FICSITFelix\Servo Skull 1137\Scripts\Main.py"
:: Wait 30 seconds before restarting.
TIMEOUT /T 30
GOTO:Start