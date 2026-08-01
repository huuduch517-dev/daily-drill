@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 日课 · 本地服务

rem 取真实局域网地址（见 lanip.ps1）。ipconfig 取第一条会选中代理虚拟网卡，手机连不上。
for /f "usebackq delims=" %%i in (`powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0lanip.ps1"`) do set "IP=%%i"

echo.
echo   ============================================
echo      日课 · 本地服务已启动
echo   ============================================
echo.
echo      这台电脑:   http://localhost:8899
if defined IP (
  echo      手机访问:   http://%IP%:8899
) else (
  echo      手机访问:   没探到局域网地址，检查是否连着 WiFi
)
echo.
echo      手机要和电脑连同一个 WiFi。在手机浏览器打开
echo      上面那个地址，再点「添加到主屏幕」，就跟装了
echo      个 App 一样，图标会出现在桌面上。
echo.
echo      关掉这个黑窗口 = 停止服务。
echo   ============================================
echo.

start "" "http://localhost:8899"
python -m http.server 8899 --bind 0.0.0.0
echo.
echo   服务已停止。
pause
