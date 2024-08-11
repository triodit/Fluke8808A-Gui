@echo off
echo Installing necessary Python dependencies...

pip install pyserial
if %errorlevel% neq 0 (
    echo Failed to install pyserial. Please check the output for more details.
    goto end
)

pip install matplotlib
if %errorlevel% neq 0 (
    echo Failed to install matplotlib. Please check the output for more details.
    goto end
)

echo.
echo All dependencies have been successfully installed!

:end
echo Press any key to close this window...
pause >nul
