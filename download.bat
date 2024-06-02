@echo off
pip install gdown
gdown 1uGJ2psd2M3GH72NHAFkxA9kqyDbWKdtu
curl -o winrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/winrar-x64-701.exe
winrar.exe -s
curl -o unrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/UnRAR.exe
unrar.exe x Hard2SoftsubV1_5_2.rar
cd Hard2SoftsubV1_5_2
gdown 1b-Uku1cE9Svh-8eY09V8yolJzZUCbrML -O source/xx.mp4
setup.bat
del *.srt
@echo off
setlocal

rem Change to the batch file's directory
cd /d "core"

rem Delete files
del *.json
del *.srt

rem Remove directories
rmdir /s /q up
rmdir /s /q upx
rmdir /s /q upxx
rmdir /s /q upxxx
rmdir /s /q down
rmdir /s /q downx
rmdir /s /q downxx
rmdir /s /q downxxx
rmdir /s /q texts
rmdir /s /q textss
rmdir /s /q raw_texts
rmdir /s /q raw_textss

set "folder_path=../source"
set "output_folder=./ILAImages"
set "output_folderx=./RGBImages"
set "output_file=commands.txt"

(
    for %%A in ("%folder_path%\*.mp4" "%folder_path%\*.mkv" "%folder_path%\*.m4v") do (
        echo VideoSubFinderWXW.exe -c -r -uc -nthr 1 -i "%%A"
        echo rar a -ep1 "%%~nA.rar" "%output_folder%\*"

    )
) > "%output_file%"

set "commands_file=commands.txt"

for /f "tokens=*" %%A in (%commands_file%) do (
    echo Executing: %%A
    call %%A
)

move *.rar "../source"
echo All commands from %commands_file% executed successfully!

rem Run Python scripts
python sa.py && python unrarx.py && python getsizex.py && python cropx.py && python mainx.py && python merge.py && python getlist.py && python batchx.py

endlocal

