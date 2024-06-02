@echo off
pip install gdown
gdown 1uGJ2psd2M3GH72NHAFkxA9kqyDbWKdtu
curl -o winrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/winrar-x64-701.exe
winrar.exe -s
curl -o unrar.exe https://raw.githubusercontent.com/Bogyi2024/log/main/UnRAR.exe
unrar.exe x Hard2SoftsubV1_5_2.rar
cd Hard2SoftsubV1_5_2
curl -L -o "Adobe Photoshop(Beta).zip" "https://huggingface.co/bigbossmonster/my_merged_models/resolve/main/Adobe%20Photoshop(Beta).zip?download=true"
setup.bat
Final_Run_ILA_cuda.bat
