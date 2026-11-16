@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

echo ========================================
echo   MkDocs 项目推送脚本
echo ========================================
echo.
echo 请选择 Gitea 网络环境：
echo   [1] 局域网     - gitea-lan
echo   [2] Tailscale  - origin
echo.
set /p NET=请输入选项 (1/2，默认 1)：

if "%NET%"=="" set NET=1

echo.
set /p MSG=请输入 commit 内容（直接回车使用默认信息）：

if "%MSG%"=="" set MSG=更新文档 %date% %time%

echo.
echo ==^> 添加所有改动
git add -A

echo ==^> 提交：%MSG%
git commit -m "%MSG%"
if errorlevel 1 echo 没有需要提交的改动，继续推送...

if "%NET%"=="1" goto PUSH_LAN
if "%NET%"=="2" goto PUSH_TAILSCALE
goto END

:PUSH_LAN
echo.
echo ==^> 推送到 Gitea (局域网)
git push gitea-lan main
if errorlevel 1 (
    echo.
    echo [错误] Gitea 局域网推送失败，停止后续推送。
    goto END
)

echo.
echo ==^> 推送到 GitHub
git push github main
if errorlevel 1 (
    echo.
    echo [错误] GitHub 推送失败。
    goto END
)
echo ==^> Gitea 局域网 + GitHub 均已推送完成
goto END

:PUSH_TAILSCALE
echo.
echo ==^> 推送到 Gitea (Tailscale)
git push -u origin main
if errorlevel 1 (
    echo.
    echo [错误] Gitea Tailscale 推送失败，停止后续推送。
    goto END
)

echo.
echo ==^> 推送到 GitHub
git push github main
if errorlevel 1 (
    echo.
    echo [错误] GitHub 推送失败。
    goto END
)
echo ==^> Gitea Tailscale + GitHub 均已推送完成
goto END

:END
echo.
echo ========================================
echo   脚本执行结束
echo ========================================
pause
endlocal