@echo off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do     rem"') do (
  set "DEL=%%a"
)
cls

cd C:\Users\Maver\AppData\Local\Programs\Python\Python35-32\Scripts

pip install --upgrade https://github.com/Rapptz/discord.py/archive/async.zip


if errorlevel 0 call :colorEcho 2 "If it show that it is succesfully download. You are done!"
echo.
pause
exit


:colorEcho
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1i