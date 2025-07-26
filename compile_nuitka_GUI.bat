@echo off
REM Set Sig Identity
set "cert_identity=squashyhydra@gmail.com"
set "cert_issuer=https://github.com/login/oauth"

REM Base Path
set "base_path=F:\discord emoji rip\Discord Emoji Sticker Ripper"
set "env_name=.env"
set "file_name=gui"
set "output_dir=output"

REM Version
set "version=1.0.0"

REM Names
set "app_name=Discord Ripper PRO"

REM Company stuff
set "name=Gnogle"

REM Check for admin privileges
NET SESSION >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

REM Check env path exists
if not exist "%base_path%\%env_name%" (
    echo The virtual environment does not exist. Please create it first.
    exit /b
)

REM Check if Nuitka is installed
if not exist "%base_path%\%env_name%\Scripts\nuitka.cmd" (
    echo Nuitka is not installed in the virtual environment. Please install it first.
    exit /b
)

REM Use --include-data-dir for assets, but --include-data-files for recursive inclusion of compressors/*
call "%base_path%\%env_name%\Scripts\nuitka.cmd" --standalone --enable-plugin=pyqt6 ^
       --lto=no ^
       --include-qt-plugins=qml ^
       --nofollow-import-to=tests ^
       --include-data-files="%base_path%\assets\icon.ico=assets/" ^
       --include-data-files="%base_path%\assets\warning.png=assets/" ^
       --include-data-files="%base_path%\assets\info.png=assets/" ^
       --output-dir="%base_path%\%output_dir%" ^
       --windows-icon-from-ico="%base_path%\assets\icon.ico" ^
       --output-filename="%app_name%.exe" ^
       --windows-console-mode="disable" ^
       --company-name="%name%" ^
       --product-name="%app_name%" ^
       --file-version="%version%" ^
       --product-version="%version%" ^
       --file-description="%app_name%" ^
       --copyright="(c) %name%. All rights reserved." ^
       --trademarks="%app_name%" ^
       --show-anti-bloat-changes ^
       --remove-output ^
       --deployment ^
       "%base_path%\%file_name%.py"

REM Check if sigstore is installed
if not exist "%base_path%\%env_name%\Scripts\sigstore.exe" (
    echo Sigstore is not installed in the virtual environment. Please install it first.
    exit /b
)

set "sigstore_path=%base_path%\%env_name%\Scripts\sigstore.exe"
set "sig_file=%base_path%\%output_dir%\%app_name%.exe.sig"
set "cert_file=%base_path%\%output_dir%\%app_name%.exe.sigstore.crt"
set "bundle_file=%base_path%\%output_dir%\%app_name%.exe.sigstore.json"
set "executable_file=%base_path%\%output_dir%\%file_name%.dist\%app_name%.exe"

echo Signing the executable with Sigstore...
REM Sign the executable
"%sigstore_path%" sign ^
    --oidc-disable-ambient-providers ^
    --signature "%sig_file%" ^
    --certificate "%cert_file%" ^
    --bundle "%bundle_file%" ^
    --overwrite ^
    "%executable_file%"

echo Signing complete.
echo.
echo Verifying the signature...
REM Verify the signature
"%sigstore_path%" verify identity ^
    --bundle "%bundle_file%" ^
    --cert-identity "%cert_identity%" ^
    --cert-oidc-issuer "%cert_issuer%" ^
    "%executable_file%"

pause