@echo off
echo Building discount.dll for Windows...
g++ -shared -o discount.dll discount.cpp -fPIC
if %ERRORLEVEL% EQU 0 (
    echo Build successful! discount.dll created.
) else (
    echo Build failed! Make sure g++ is installed and in PATH.
    pause
)

