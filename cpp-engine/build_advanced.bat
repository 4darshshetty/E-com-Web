@echo off
echo Building Advanced C++ Graphics Engine for Windows...
echo.

echo Building discount.dll...
g++ -shared -o discount.dll discount.cpp -fPIC -O3
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to build discount.dll
    pause
    exit /b 1
)

echo Building graphics_engine.dll...
g++ -shared -o graphics_engine.dll graphics_engine.cpp -fPIC -O3 -march=native
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to build graphics_engine.dll
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All C++ modules built successfully!
echo   - discount.dll (Discount Engine)
echo   - graphics_engine.dll (3D Graphics Engine)
pause

