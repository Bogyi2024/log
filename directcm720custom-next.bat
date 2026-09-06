@echo off
rem Installing
pip install gdown
pip install huggingface_hub
pip install --upgrade --no-cache-dir gdown
pip install git+https://github.com/Juvenal-Yescas/mediafire-dl
gdown 1q421vbzHgXv7cG7quC6YVQi4iW1ASvOY
curl -o winrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/winrar-x64-701.exe
winrar.exe -s
curl -o unrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/UnRAR.exe
unrar.exe x Hard2SoftsubV1_5_2.rar

cd /d "Hard2SoftsubV1_5_2" || (
    echo ERROR: Hard2SoftsubV1_5_2 folder was not found.
    exit /b 1
)

curl -o send_email_file-next.py https://raw.githubusercontent.com/Bogyi2024/log/main/send_email_file-next.py
curl -o aria2c.exe https://raw.githubusercontent.com/Bogyi2024/log/main/aria2c.exe

rem Download and run the download/configuration scripts.
curl -o cm720-next.py https://raw.githubusercontent.com/Bogyi2024/log/main/cm_download/cm720-next.py
python cm720-next.py
curl -o config.py https://raw.githubusercontent.com/Bogyi2024/log/main/config.py
python config.py

rem Enter core temporarily for setup, then return to the application folder.
pushd "core" || (
    echo ERROR: core folder was not found.
    exit /b 1
)

pip install -r requirements.txt
curl -O -L https://raw.githubusercontent.com/monsterhunters/sub/dev/sa.zip
tar -xf sa.zip
curl -O -L https://raw.githubusercontent.com/monsterhunters/sub/monsterhunters-patch-1/main.py
curl -O -L https://raw.githubusercontent.com/monsterhunters/sub/monsterhunters-patch-1/main2x.py

popd

del /q "*.srt" 2>nul

setlocal
pushd "core" || (
    echo ERROR: core folder was not found.
    endlocal
    exit /b 1
)

rem Delete old files.
del /q "*.json" 2>nul
del /q "*.srt" 2>nul

rem Remove old directories.
for %%D in (up upx upxx upxxx down downx downxx downxxx texts textss raw_texts raw_textss) do (
    if exist "%%D" rmdir /s /q "%%D"
)

set "folder_path=..\source"
set "output_folder=ILAImages"
set "output_folderx=RGBImages"
set "output_file=commands.txt"

if not exist "%folder_path%" (
    echo ERROR: Source folder "%folder_path%" was not found.
    popd
    endlocal
    exit /b 1
)

rem Build the same command list, but use a normalized absolute input path.
> "%output_file%" (
    for %%E in (mp4 mkv m4v) do (
        for %%A in ("%folder_path%\*.%%E") do (
            if exist "%%~fA" (
                echo VideoSubFinderWXW.exe -c -r -nthr 1 -i "%%~fA"
                echo rar a -ep1 "%%~nA.rar" "%output_folder%\*"
                echo rar a -ep1 "..\%%~nA_ILA.rar" "%output_folder%\*"
                echo rar a -ep1 "..\%%~nA_RGB.rar" "%output_folderx%\*"
            )
        )
    )
)

set "commands_file=commands.txt"

for /f "usebackq delims=" %%A in ("%commands_file%") do (
    echo Executing: %%A
    call %%A
    if errorlevel 1 echo WARNING: Command returned an error: %%A
)

move /y "*.rar" "..\source\" >nul 2>&1
echo Finished executing commands from %commands_file%.

rem Run the existing Python processing chain.
python sa.py && python unrarx.py && python getsizex.py && python cropx.py && python mainx.py && python merge.py && python getlist.py && python batchx.py

popd
endlocal

rem This script is stored in Hard2SoftsubV1_5_2, not in core.
python send_email_file-next.py
