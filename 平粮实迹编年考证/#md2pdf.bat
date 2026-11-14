@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo Generating PDF from input_files...

:: 使用 PowerShell 获取纯数字时间戳
for /f %%i in ('powershell -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set timestamp=%%i
set output_file=平粮实迹编年考证_%timestamp%.pdf

pandoc --defaults=config.yaml ^
  -o "%output_file%" ^
  --standalone ^
  --pdf-engine=xelatex ^
  --listings

echo PDF generated: %output_file%
pause