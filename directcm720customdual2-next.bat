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

rem Create the fixed downloader locally. It asks aria2c to honor Content-Disposition,
rem so API links are saved with the proper server-provided filename.
> "cm720-next.b64" (
    echo aW1wb3J0IG9zCmltcG9ydCBnZG93bgppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgcmUKaW1wb3J0
    echo IG1lZGlhZmlyZV9kbAppbXBvcnQgdGltZQppbXBvcnQgc3lzCgpkZWYgZXh0cmFjdF9nb29nbGVf
    echo ZHJpdmVfaWQodXJsKToKICAgICIiIgogICAgRXh0cmFjdHMgdGhlIEdvb2dsZSBEcml2ZSBmaWxl
    echo L2ZvbGRlciBJRCBmcm9tIHZhcmlvdXMgVVJMIGZvcm1hdHMuCiAgICAiIiIKICAgIGRyaXZlX2lk
    echo X3BhdHRlcm4gPSByZS5jb21waWxlKHInZHJpdmUuZ29vZ2xlLmNvbS8uKj8oPzpmaWxlL2QvfGRy
    echo aXZlL2ZvbGRlcnMvfG9wZW5cP2lkPXx1Y1w/aWQ9KShbXi8mP10rKScpCiAgICBtYXRjaCA9IGRy
    echo aXZlX2lkX3BhdHRlcm4uc2VhcmNoKHVybCkKICAgIGlmIG1hdGNoOgogICAgICAgIHJldHVybiBt
    echo YXRjaC5ncm91cCgxKQogICAgZWxzZToKICAgICAgICByZXR1cm4gTm9uZQoKIyBHZXQgdGhlIHJh
    echo dyBsaXN0IG9mIGxpbmtzIGZyb20gdGhlIGVudmlyb25tZW50IHZhcmlhYmxlCmxpbmtzX2NvbnRl
    echo bnQgPSBvcy5nZXRlbnYoJ0xJTktTX0NPTlRFTlQnKQoKaWYgbGlua3NfY29udGVudDoKICAgIHNp
    echo bmdsZV9saW5lX2JhdGNoX2xpbmtzID0gbGlua3NfY29udGVudC5zcGxpdGxpbmVzKCkKICAgIHBy
    echo aW50KGYiTG9hZGVkIHtsZW4oc2luZ2xlX2xpbmVfYmF0Y2hfbGlua3MpfSBsaW5rcyBmcm9tIGVu
    echo dmlyb25tZW50IHZhcmlhYmxlLiIpCmVsc2U6CiAgICBwcmludCgiRXJyb3I6IExJTktTX0NPTlRF
    echo TlQgZW52aXJvbm1lbnQgdmFyaWFibGUgbm90IGZvdW5kIG9yIGlzIGVtcHR5LiIpCiAgICBzaW5n
    echo bGVfbGluZV9iYXRjaF9saW5rcyA9IFtdCgoKaWYgc2luZ2xlX2xpbmVfYmF0Y2hfbGlua3M6CiAg
    echo ICBvdXRwdXRfcGF0aCA9ICJzb3VyY2UvIgogICAgb3MubWFrZWRpcnMob3V0cHV0X3BhdGgsIGV4
    echo aXN0X29rPVRydWUpCiAgICBjdXJyZW50X2RpciA9IG9zLmdldGN3ZCgpICMgR2V0IGN1cnJlbnQg
    echo ZGlyZWN0b3J5IHRvIHJldHVybiB0bwoKICAgIGZvciB1cmwgaW4gc2luZ2xlX2xpbmVfYmF0Y2hf
    echo bGlua3M6CiAgICAgICAgdXJsID0gdXJsLnN0cmlwKCkgIyBDbGVhbiB1cCB3aGl0ZXNwYWNlCiAg
    echo ICAgICAgaWYgbm90IHVybDogIyBTa2lwIGVtcHR5IGxpbmVzCiAgICAgICAgICAgIGNvbnRpbnVl
    echo CiAgICAgICAgICAgIAogICAgICAgIHByaW50KGYiXG4tLS0gUHJvY2Vzc2luZyBVUkw6IHt1cmx9
    echo IC0tLSIpCiAgICAgICAgICAgIAogICAgICAgIGZpbGVfaWQgPSBleHRyYWN0X2dvb2dsZV9kcml2
    echo ZV9pZCh1cmwpCiAgICAgICAgICAgIAogICAgICAgIGlmIGZpbGVfaWQ6CiAgICAgICAgICAgICMg
    echo LS0tIEdPT0dMRSBEUklWRSBMT0dJQyAoVXNlcyBnZG93biBQeXRob24gQVBJIHdpdGggZmlsZSBJ
    echo RCkgLS0tCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHByaW50KGYiQXR0ZW1wdGlu
    echo ZyBkb3dubG9hZCB2aWEgZ2Rvd24gKGZpbGUgSUQpOiB7ZmlsZV9pZH0iKQogICAgICAgICAgICAg
    echo ICAgCiAgICAgICAgICAgICAgICBnZG93bi5kb3dubG9hZChpZD1maWxlX2lkLCBvdXRwdXQ9b3V0
    echo cHV0X3BhdGgsIHF1aWV0PUZhbHNlKQogICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICBw
    echo cmludChmIlN1Y2Nlc3NmdWxseSBkb3dubG9hZGVkIGZpbGUgd2l0aCBJRDoge2ZpbGVfaWR9IikK
    echo ICAgICAgICAgICAgICAgIAogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAg
    echo ICAgICAgICAgICBwcmludChmImdkb3duIGZpbGUgZG93bmxvYWQgZmFpbGVkICh7c3RyKGUpfSku
    echo IEF0dGVtcHRpbmcgYXMgRk9MREVSLi4uIikKICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAg
    echo ICAgICAgICAgICAjIEZvbGRlciBkb3dubG9hZCBmYWxscyBiYWNrIHRvIHRoZSBQeXRob24gZ2Rv
    echo d24gZnVuY3Rpb24KICAgICAgICAgICAgICAgICAgICBnZG93bi5kb3dubG9hZF9mb2xkZXIoaWQ9
    echo ZmlsZV9pZCwgb3V0cHV0PW91dHB1dF9wYXRoLCBxdWlldD1GYWxzZSwgcmVzdW1lPVRydWUpCiAg
    echo ICAgICAgICAgICAgICAgICAgcHJpbnQoZiJTdWNjZXNzZnVsbHkgZG93bmxvYWRlZCBmb2xkZXIg
    echo d2l0aCBJRDoge2ZpbGVfaWR9IikKICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMg
    echo ZTI6CiAgICAgICAgICAgICAgICAgICAgcHJpbnQoZiJFcnJvciBkb3dubG9hZGluZyB7ZmlsZV9p
    echo ZH0gYXMgYm90aCBmaWxlIGFuZCBmb2xkZXI6IHtzdHIoZTIpfSIpCgogICAgICAgIGVsaWYgIm1z
    echo dWJiMi5uZXQiIGluIHVybDoKICAgICAgICAgICAgIyAtLS0gV0dFVCBMT0dJQyAoSGFuZGxlcyBt
    echo c3ViYjIubmV0IGxpbmtzKSAtLS0KICAgICAgICAgICAgcHJpbnQoZiJBdHRlbXB0aW5nIGRvd25s
    echo b2FkIHZpYSB3Z2V0IChtc3ViYjIubmV0KToge3VybH0iKQogICAgICAgICAgICB0cnk6CiAgICAg
    echo ICAgICAgICAgICBzdWJwcm9jZXNzLnJ1bigKICAgICAgICAgICAgICAgICAgICBbJ3dnZXQnLCAn
    echo LVAnLCBvdXRwdXRfcGF0aCwgdXJsXSwKICAgICAgICAgICAgICAgICAgICBjaGVjaz1UcnVlCiAg
    echo ICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBwcmludChmIlN1Y2Nlc3NmdWxseSBkb3du
    echo bG9hZGVkIG1zdWJiMi5uZXQgbGluayB2aWEgd2dldC4iKQogICAgICAgICAgICBleGNlcHQgc3Vi
    echo cHJvY2Vzcy5DYWxsZWRQcm9jZXNzRXJyb3IgYXMgZToKICAgICAgICAgICAgICAgIHByaW50KGYi
    echo d2dldCBkb3dubG9hZCBmYWlsZWQgKEV4aXQgQ29kZSB7ZS5yZXR1cm5jb2RlfSkuIEVycm9yOiB7
    echo ZX0iKQogICAgICAgICAgICBleGNlcHQgRmlsZU5vdEZvdW5kRXJyb3I6CiAgICAgICAgICAgICAg
    echo ICBwcmludCgiRXJyb3I6ICd3Z2V0JyBjb21tYW5kIG5vdCBmb3VuZC4gRW5zdXJlIHdnZXQgaXMg
    echo aW5zdGFsbGVkIGFuZCBpbiB5b3VyIHN5c3RlbSBQQVRILiIpCiAgICAgICAgICAgIGV4Y2VwdCBF
    echo eGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIHByaW50KGYiQW4gdW5leHBlY3RlZCBlcnJv
    echo ciBvY2N1cnJlZCBkdXJpbmcgd2dldCBkb3dubG9hZDoge3N0cihlKX0iKQoKICAgICAgICBlbGlm
    echo ICJ3b3JrZXJzIiBpbiB1cmw6CiAgICAgICAgICAgICMgLS0tIENVUkwgTE9HSUMgKE5FVzogSGFu
    echo ZGxlcyBhdXRvLW5hbWluZyB3aXRoIENvbnRlbnQtRGlzcG9zaXRpb24pIC0tLQogICAgICAgICAg
    echo ICBwcmludChmIkF0dGVtcHRpbmcgZG93bmxvYWQgdmlhIGN1cmwgKGF1dG8tbmFtZS9Db250ZW50
    echo LURpc3Bvc2l0aW9uKToge3VybH0iKQogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBv
    echo cy5jaGRpcihvdXRwdXRfcGF0aCkKICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgIyBX
    echo ZSB1c2UgLU8gdG8gc2F2ZSB0aGUgZmlsZSBhbmQgLUogdG8gdXNlIHRoZSBzZXJ2ZXIncyBDb250
    echo ZW50LURpc3Bvc2l0aW9uIGZpbGVuYW1lCiAgICAgICAgICAgICAgICBzdWJwcm9jZXNzLnJ1bigK
    echo ICAgICAgICAgICAgICAgICAgICBbJ2N1cmwnLCAnLU8nLCAnLUonLCB1cmxdLAogICAgICAgICAg
    echo ICAgICAgICAgIGNoZWNrPVRydWUKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIAog
    echo ICAgICAgICAgICAgICAgcHJpbnQoZiJTdWNjZXNzZnVsbHkgZG93bmxvYWRlZCAnd29ya2Vycycg
    echo bGluayB2aWEgY3VybC4iKQogICAgICAgICAgICAgICAgCiAgICAgICAgICAgIGV4Y2VwdCBzdWJw
    echo cm9jZXNzLkNhbGxlZFByb2Nlc3NFcnJvciBhcyBlOgogICAgICAgICAgICAgICAgcHJpbnQoZiJD
    echo dXJsIGRvd25sb2FkIGZhaWxlZCAoRXhpdCBDb2RlIHtlLnJldHVybmNvZGV9KS4gRXJyb3I6IHtl
    echo fSIpCiAgICAgICAgICAgIGV4Y2VwdCBGaWxlTm90Rm91bmRFcnJvcjoKICAgICAgICAgICAgICAg
    echo IHByaW50KCJFcnJvcjogJ2N1cmwnIGNvbW1hbmQgbm90IGZvdW5kLiBFbnN1cmUgY3VybCBpcyBp
    echo bnN0YWxsZWQgYW5kIGluIHlvdXIgc3lzdGVtIFBBVEguIikKICAgICAgICAgICAgZXhjZXB0IEV4
    echo Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAgcHJpbnQoZiJBbiB1bmV4cGVjdGVkIGVycm9y
    echo IG9jY3VycmVkIGR1cmluZyBjdXJsIGRvd25sb2FkOiB7c3RyKGUpfSIpCiAgICAgICAgICAgIGZp
    echo bmFsbHk6CiAgICAgICAgICAgICAgICAjIEFsd2F5cyBnbyBiYWNrIHRvIHRoZSBvcmlnaW5hbCBk
    echo aXJlY3RvcnkKICAgICAgICAgICAgICAgIGlmIG9zLmdldGN3ZCgpICE9IGN1cnJlbnRfZGlyOgog
    echo ICAgICAgICAgICAgICAgICAgIG9zLmNoZGlyKGN1cnJlbnRfZGlyKQoKCiAgICAgICAgZWxpZiB1
    echo cmwuc3RhcnRzd2l0aCgiaHR0cHM6Ly9kb3dubG9hZCIpIG9yICJtZWRpYWZpcmUuY29tIiBpbiB1
    echo cmw6CiAgICAgICAgICAgICMgLS0tIE1FRElBRklSRSBMT0dJQyAoVXNlcyBtZWRpYWZpcmVfZGwg
    echo bGlicmFyeSkgLS0tCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIG9zLmNoZGlyKG91
    echo dHB1dF9wYXRoKSAjIEdvIGludG8gdGhlIHNvdXJjZSBmb2xkZXIKICAgICAgICAgICAgICAgIAog
    echo ICAgICAgICAgICAgICAgaWYgdXJsLnN0YXJ0c3dpdGgoImh0dHBzOi8vZG93bmxvYWQiKToKICAg
    echo ICAgICAgICAgICAgICAgICAjIENvbnZlcnQgcmF3IE1lZGlhZmlyZSBkb3dubG9hZCBsaW5rIGJh
    echo Y2sgdG8gdmlld2FibGUgZmlsZSBsaW5rCiAgICAgICAgICAgICAgICAgICAgdXJsX3BhcnRzID0g
    echo dXJsLnNwbGl0KCIvIikKICAgICAgICAgICAgICAgICAgICAjIEFzc3VtZXMgZm9ybWF0IGxpa2U6
    echo IGh0dHBzOi8vZG93bmxvYWRYWFgvWVlZWS9maWxla2V5L2ZpbGVuYW1lCiAgICAgICAgICAgICAg
    echo ICAgICAgaWYgbGVuKHVybF9wYXJ0cykgPj0gNjoKICAgICAgICAgICAgICAgICAgICAgICAgbmV3
    echo X3VybCA9IGYiaHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9maWxlL3t1cmxfcGFydHNbLTJdfS97
    echo dXJsX3BhcnRzWy0xXX0iCiAgICAgICAgICAgICAgICAgICAgICAgIG1lZGlhZmlyZV9kbC5kb3du
    echo bG9hZChuZXdfdXJsLCBxdWlldD1GYWxzZSkKICAgICAgICAgICAgICAgICAgICBlbHNlOgogICAg
    echo ICAgICAgICAgICAgICAgICAgICBwcmludCgiTWVkaWFmaXJlIHJhdyBsaW5rIGZvcm1hdCBub3Qg
    echo cmVjb2duaXplZCwgc2tpcHBpbmcuIikKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAg
    echo ICAgICAgICAgbWVkaWFmaXJlX2RsLmRvd25sb2FkKHVybCwgcXVpZXQ9RmFsc2UpCiAgICAgICAg
    echo ICAgICAgICAgICAgCiAgICAgICAgICAgICAgICBwcmludChmIkRvd25sb2FkZWQ6IHt1cmx9IikK
    echo ICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAgcHJpbnQo
    echo ZiJFcnJvciBkb3dubG9hZGluZyBmcm9tIE1lZGlhZmlyZToge3N0cihlKX0iKQogICAgICAgICAg
    echo ICBmaW5hbGx5OgogICAgICAgICAgICAgICAgIyBBbHdheXMgZ28gYmFjayB0byB0aGUgb3JpZ2lu
    echo YWwgZGlyZWN0b3J5CiAgICAgICAgICAgICAgICBpZiBvcy5nZXRjd2QoKSAhPSBjdXJyZW50X2Rp
    echo cjoKICAgICAgICAgICAgICAgICAgICBvcy5jaGRpcihjdXJyZW50X2RpcikKICAgICAgICAgICAg
    echo ICAgICAgICAKICAgICAgICBlbHNlOgogICAgICAgICAgICAjIC0tLSBGQUxMQkFDSyBMT0dJQyAo
    echo VXNlcyBhcmlhMmMgZm9yIGdlbmVyaWMgZGlyZWN0IGxpbmtzKSAtLS0KICAgICAgICAgICAgdHJ5
    echo OgogICAgICAgICAgICAgICAgIyBMZXQgYXJpYTIgcmVhZCBDb250ZW50LURpc3Bvc2l0aW9uIGFu
    echo ZCB1c2UgdGhlIGZpbGVuYW1lIHN1cHBsaWVkIGJ5IHRoZSBzZXJ2ZXIuCiAgICAgICAgICAgICAg
    echo ICAjIERvIG5vdCB1c2UgLW8gaGVyZTogZm9yY2luZyBhbiBvdXRwdXQgbmFtZSBkaXNhYmxlcyBh
    echo dXRvbWF0aWMgbmFtaW5nLgogICAgICAgICAgICAgICAgcHJpbnQoIkF0dGVtcHRpbmcgZG93bmxv
    echo YWQgdmlhIGFyaWEyYyAoc2VydmVyLXByb3ZpZGVkIGZpbGVuYW1lKS4uLiIpCgogICAgICAgICAg
    echo ICAgICAgYXJpYTJfZXhlY3V0YWJsZSA9IG9zLnBhdGguam9pbihjdXJyZW50X2RpciwgImFyaWEy
    echo Yy5leGUiKQogICAgICAgICAgICAgICAgc3VicHJvY2Vzcy5ydW4oCiAgICAgICAgICAgICAgICAg
    echo ICAgWwogICAgICAgICAgICAgICAgICAgICAgICBhcmlhMl9leGVjdXRhYmxlLAogICAgICAgICAg
    echo ICAgICAgICAgICAgICAiLS1jb250aW51ZT10cnVlIiwKICAgICAgICAgICAgICAgICAgICAgICAg
    echo Ii0tY29udGVudC1kaXNwb3NpdGlvbj10cnVlIiwKICAgICAgICAgICAgICAgICAgICAgICAgIi0t
    echo ZGlyPSIgKyBvdXRwdXRfcGF0aCwKICAgICAgICAgICAgICAgICAgICAgICAgIi0tbWF4LWNvbm5l
    echo Y3Rpb24tcGVyLXNlcnZlcj0xNiIsCiAgICAgICAgICAgICAgICAgICAgICAgICItLXNwbGl0PTE2
    echo IiwKICAgICAgICAgICAgICAgICAgICAgICAgIi0tbWluLXNwbGl0LXNpemU9MU0iLAogICAgICAg
    echo ICAgICAgICAgICAgICAgICB1cmwsCiAgICAgICAgICAgICAgICAgICAgXSwKICAgICAgICAgICAg
    echo ICAgICAgICBjaGVjaz1UcnVlLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgcHJp
    echo bnQoZiJEb3dubG9hZGVkIHRvIHtvdXRwdXRfcGF0aH0gdXNpbmcgdGhlIHNlcnZlci1wcm92aWRl
    echo ZCBmaWxlbmFtZS4iKQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAg
    echo ICAgICAgICBwcmludChmIkVycm9yIGRvd25sb2FkaW5nIHt1cmx9IHZpYSBhcmlhMmM6IHtzdHIo
    echo ZSl9IikKCmVsc2U6CiAgICBwcmludCgiTm8gbGlua3MgZm91bmQgaW4gdGhlIGxpbmtzIGNvbnRl
    echo bnQuIikKCnByaW50KCJcbkRvd25sb2FkIHNjcmlwdCBmaW5pc2hlZC4iKQo=
)
certutil -f -decode "cm720-next.b64" "cm720-next.py" >nul || (
    echo ERROR: Could not create cm720-next.py.
    exit /b 1
)
del /q "cm720-next.b64" 2>nul
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
                echo VideoSubFinderWXW.exe -gs "settings\custom.cfg" -c -r -nthr 1 -i "%%~fA"
                echo rar a -ep1 "%%~nA_upline.rar" "%output_folder%\*"
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
