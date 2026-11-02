@echo off
chcp 65001 >nul
title 启动英一手机背诵服务 - 《英一单词大观》
cd /d "%~dp0"
echo 正在启动英一本地服务...
python start_server.py
pause
