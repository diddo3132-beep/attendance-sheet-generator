@echo off
chcp 65001 >nul
echo ============================================
echo   考勤表生成助手 - 打包工具
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.8 以上版本
    echo 下载地址：https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/3] 安装依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo 使用清华源失败，尝试官方源...
    pip install -r requirements.txt
)

echo.
echo [2/3] 开始打包...

pyinstaller --noconfirm --onefile --windowed ^
    --name "考勤表助手" ^
    --add-data "template;template" ^
    --hidden-import pdfplumber ^
    --hidden-import pdfminer ^
    --hidden-import pdfminer.high_level ^
    --hidden-import pdfminer.layout ^
    --hidden-import pdfminer.pdfpage ^
    --hidden-import cffi ^
    app.py

if errorlevel 1 (
    echo.
    echo 打包失败！请检查上面的错误信息
    pause
    exit /b 1
)

echo.
echo [3/3] 整理文件...

REM 复制必要文件到 dist 目录
if not exist "dist\template" mkdir "dist\template"
if not exist "dist\data" mkdir "dist\data"
if not exist "dist\output" mkdir "dist\output"

if exist "template\考勤表模板.docx" (
    copy "template\考勤表模板.docx" "dist\template\" >nul
)
if exist "data\courses.json" (
    copy "data\courses.json" "dist\data\" >nul
)

echo.
echo ============================================
echo   打包完成！
echo   程序位置：dist\考勤表助手.exe
echo   请将 dist 文件夹中的所有内容复制到目标电脑
echo ============================================
echo.

explorer dist

pause
