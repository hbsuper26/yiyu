@echo off
chcp 65001 >nul
title 以渔数媒 - 手动生成文章并打包
color 0B

echo.
echo ===================================================
echo     以渔数媒 AI Agent - 手动触发生成文章与打包
echo ===================================================
echo.

:: 激活 Python 环境 (如果需要的话，当前是在全局或特定环境下)
:: call python_env\Scripts\activate.bat

python generate_now.py

echo.
echo ===================================================
echo 操作结束。请打开 Sourcetree 将 dist 文件夹的改动推送上线。
echo ===================================================
echo.
pause
