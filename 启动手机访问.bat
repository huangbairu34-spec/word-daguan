@echo off
chcp 65001 >nul
title 启动手机背诵服务 - 《英二单词大观》
cd /d "%~dp0"
echo 正在启动本地服务...
python start_server.py
pause
