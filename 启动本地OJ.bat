@echo off
chcp 65001 >nul
title 本地 OJ - 从语法到算法
cd /d "%~dp0"
echo.
echo   正在启动本地 OJ ...
echo   题库：《从语法到算法：C++ 算法设计与 ACM 竞赛入门》
echo   地址：http://127.0.0.1:8765/  （浏览器会自动打开）
echo.
echo   提示：这个黑窗口就是 OJ 服务本身，关掉它就等于停止 OJ。
echo.
set "PY=py -3"
py -3 -c "import sys" >nul 2>nul
if errorlevel 1 set "PY=python"
%PY% server.py --open
if errorlevel 1 (
  echo.
  echo   启动失败：没有找到可用的 Python，或者 g++ 不在 PATH 里。
  echo   可以先在命令行里输入  python --version  看看能不能打印出版本号，
  echo   具体解决办法见同目录下的 README.md。
  pause
)
