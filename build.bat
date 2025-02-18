chcp 65001

@echo off
setlocal enabledelayedexpansion

echo zbWidgetLib打包工具
echo.

:: 设置相对路径
set "SCRIPT_DIR=%~dp0"
set "VENV_ACTIVATE=%SCRIPT_DIR%.venv\Scripts\activate.bat"

:: 检查虚拟环境是否存在
if not exist "%VENV_ACTIVATE%" (
    echo [错误] 虚拟环境未找到，请确认已创建.venv环境
    echo 预期路径: %VENV_ACTIVATE%
    pause
    exit /b 1
)

:: 激活虚拟环境
call "%VENV_ACTIVATE%" || (
    echo [错误] 激活虚拟环境失败！
    pause
    exit /b 1
)

:: 清理旧构建
if exist dist (
    rmdir /S /Q dist || (
        echo [错误] 清理旧构建失败！
        call "%SCRIPT_DIR%.venv\Scripts\deactivate.bat"
        pause
        exit /b 1
    )
    echo 已删除 dist 目录
) else (
    echo 未找到旧构建文件
)

:: 构建软件包
python -m build --wheel || (
    echo [错误] 构建过程失败！
    call "%SCRIPT_DIR%.venv\Scripts\deactivate.bat"
    pause
    exit /b 1
)
echo 构建成功！生成文件：
dir /b dist

:: 上传确认
echo.
set /p upload="是否要上传到PyPI？(y/n) "
if /i "%upload%" neq "y" (
    echo 已跳过上传步骤
    goto deactivate
)

:: 上传包
python -m twine upload dist/* || (
    echo [错误] 上传失败！
    call "%SCRIPT_DIR%.venv\Scripts\deactivate.bat"
    pause
    exit /b 1
)
echo 上传成功！

:deactivate
echo.
echo 正在退出虚拟环境...
call "%SCRIPT_DIR%.venv\Scripts\deactivate.bat"

echo.
echo 操作完成！按任意键退出...
pause