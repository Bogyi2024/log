@echo off
rem Installing
pip install gdown
gdown 1uGJ2psd2M3GH72NHAFkxA9kqyDbWKdtu
curl -o winrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/winrar-x64-701.exe
winrar.exe -s
curl -o unrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/UnRAR.exe
unrar.exe x Hard2SoftsubV1_5_2.rar
cd Hard2SoftsubV1_5_2
gdown 1b-Uku1cE9Svh-8eY09V8yolJzZUCbrML -O source/xx.mp4
del *.srt

