@echo off
color 0E
title Binance Trading Bot Launcher

echo ========================================================
echo         Binance Testnet Trading Bot Launcher
echo ========================================================
echo.
echo Please select how you want to run the bot:
echo.
echo [1] Run Web GUI (Flask App)  - Opens in your browser
echo [2] Run CLI  (Command Line)  - Opens an interactive shell
echo [3] Exit
echo.
echo ========================================================
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" (
    echo.
    echo Starting Local Web Server...
    echo The UI will automatically open in your default browser.
    timeout /t 2 >nul
    start http://127.0.0.1:5000
    python app.py
    pause
    exit
)

if "%choice%"=="2" (
    echo.
    echo --------------------------------------------------------
    echo Starting Interactive CLI Mode...
    echo --------------------------------------------------------
    python cli.py
    pause
    exit
)

if "%choice%"=="3" (
    exit
)

echo Invalid selecton. Exiting...
pause
