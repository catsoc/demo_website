
@echo off
title Google Index Monitor
echo ========================================
echo    Google 收錄監控系統
echo ========================================
echo.

:monitor_loop
echo [%date% %time%] 執行收錄檢查...
python google_index_checker.py

echo.
echo 等待 24 小時後再次檢查...
echo 按 Ctrl+C 可停止監控
timeout /t 86400 /nobreak > nul

goto monitor_loop
