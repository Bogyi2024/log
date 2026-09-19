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

rem --- Embedded downloader (cm720-next.py) ------------------------------------
rem Self-contained on purpose: no extra file has to exist in the repo, so this
rem .bat and the downloader can never drift apart again (the old blob silently
rem kept the 16-connection version, which caused the HTTP 429 failures).
rem
rem cm720-next.py sha256 = a637815e2f873e1b9eeacbbfe55de8cef5c789b2f73c67632f979137cdccf26a
rem The printed hash below lets you verify in the CI log which revision ran.
rem
rem Prefer fetching from the repo instead? Comment out the block below and use:
rem   curl -fL -o "cm720-next.py" https://raw.githubusercontent.com/Bogyi2024/log/main/cm720-next.py
> "cm720-next.b64" (
    echo IiIiCmNtNzIwLW5leHQucHkgIC0gIG11bHRpLWhvc3QgZG93bmxvYWRlciBmb3IgdGhlIEgyUyAv
    echo IENNIHBpcGVsaW5lLgoKV2hhdCBjaGFuZ2VkIHZzLiB0aGUgdmVyc2lvbiBlbWJlZGRlZCAoYmFz
    echo ZTY0KSBpbiBkaXJlY3RjbTcyMGN1c3RvbWR1YWwyLW5leHQuYmF0OgoKICAxLiBQT0xJVEVORVNT
    echo LiAgYXJpYTIgbm93IG9wZW5zIDIgY29ubmVjdGlvbnMgcGVyIHNlcnZlciBpbnN0ZWFkIG9mIDE2
    echo IGFuZAogICAgIG9ubHkgMSBmaWxlIGF0IGEgdGltZS4gIFRoZSBvbGQgIi0tc3BsaXQ9MTYgLS1t
    echo YXgtY29ubmVjdGlvbi1wZXItc2VydmVyPTE2IgogICAgIGJ1cnN0IGlzIHdoYXQgbWFkZSBtZWdh
    echo ZGwuYm9hdHMgYW5zd2VyIEhUVFAgNDI5IGFuZCBkcm9wIGVwaXNvZGVzIDItNC4KCiAgMi4gUkVU
    echo UklFUyBXSVRIIFJFQUwgQkFDSy1PRkYuICBFYWNoIFVSTCBnZXRzIHVwIHRvIERPV05MT0FEX0FU
    echo VEVNUFRTIG91dGVyCiAgICAgYXR0ZW1wdHMsIHdhaXRpbmcgNDVzLCA5MHMsIDE4MHMgLi4uIGJl
    echo dHdlZW4gdGhlbSwgb24gdG9wIG9mIGFyaWEyJ3Mgb3duCiAgICAgLS1tYXgtdHJpZXMvLS1yZXRy
    echo eS13YWl0LiAgQSA0MjkgbmVlZHMgdGltZSB0byBjbGVhcjsgcmV0cnlpbmcgaW5zdGFudGx5CiAg
    echo ICAgd2l0aCB0aGUgc2FtZSBzZXR0aW5ncyBjYW4gbmV2ZXIgc3VjY2VlZC4KCiAgMy4gVkVSSUZJ
    echo Q0FUSU9OLiAgRXZlcnkgVVJMIG11c3QgZmluaXNoIHN1Y2Nlc3NmdWxseS4gIElmIGFueSBsaW5r
    echo IGZhaWxlZCB0aGUKICAgICBzY3JpcHQgcHJpbnRzIGEgc3VtbWFyeSBhbmQgZXhpdHMgd2l0aCBz
    echo dGF0dXMgMSwgc28gdGhlIEdpdEh1YiBqb2IgZ29lcyBSRUQKICAgICBpbnN0ZWFkIG9mIHF1aWV0
    echo bHkgZW1haWxpbmcgYSBwYXJ0aWFsIGJhdGNoICh0aGF0IGlzIGhvdyAxIG9mIDQgZXBpc29kZXMK
    echo ICAgICB3YXMgZGVsaXZlcmVkIGxhc3QgdGltZSkuCgogIDQuIFVzZWZ1bCBsb2dnaW5nOiBwZXIt
    echo VVJMIHJlc3VsdCwgZmlsZXMgYWRkZWQsIGFuZCBhIGZpbmFsIHJlY2FwLgoKRW52aXJvbm1lbnQg
    echo KGFsbCBvcHRpb25hbCwgc2Vuc2libGUgZGVmYXVsdHMpOgogICAgTElOS1NfQ09OVEVOVCAgICAg
    echo ICAgICAgIG5ld2xpbmUgc2VwYXJhdGVkIGxpbmtzIChyZXF1aXJlZCkKICAgIE9VVFBVVF9QQVRI
    echo ICAgICAgICAgICAgICBkb3dubG9hZCBkaXIgICAgICAgICAgICAgICAgICAgICAoZGVmYXVsdCBz
    echo b3VyY2UvKQogICAgRE9XTkxPQURfQVRURU1QVFMgICAgICAgIG91dGVyIGF0dGVtcHRzIHBlciBV
    echo UkwgICAgICAgICAgIChkZWZhdWx0IDQpCiAgICBET1dOTE9BRF9CQUNLT0ZGX1NUQVJUICAgc2Vj
    echo b25kcyBiZWZvcmUgZmlyc3QgcmV0cnkgICAgICAgKGRlZmF1bHQgNDUpCiAgICBET1dOTE9BRF9C
    echo QUNLT0ZGX0ZBQ1RPUiAgYmFjay1vZmYgbXVsdGlwbGllciAgICAgICAgICAgICAgKGRlZmF1bHQg
    echo MikKICAgIERPV05MT0FEX0RFTEFZX1NFQ09ORFMgICBwYXVzZSBiZXR3ZWVuIHR3byBVUkxzICAg
    echo ICAgICAgICAoZGVmYXVsdCAyMCkKICAgIEFSSUEyX0NPTk5FQ1RJT05TICAgICAgICBjb25uZWN0
    echo aW9ucyBwZXIgc2VydmVyICAgICAgICAgIChkZWZhdWx0IDIpCiAgICBBUklBMl9TUExJVCAgICAg
    echo ICAgICAgICAgYXJpYTIgc3BsaXQgY291bnQgICAgICAgICAgICAgICAoZGVmYXVsdCAyKQoiIiIK
    echo CmltcG9ydCBvcwppbXBvcnQgcmUKaW1wb3J0IHN1YnByb2Nlc3MKaW1wb3J0IHN5cwppbXBvcnQg
    echo dGltZQoKaW1wb3J0IGdkb3duCmltcG9ydCBtZWRpYWZpcmVfZGwKCk9VVFBVVF9QQVRIID0gb3Mu
    echo Z2V0ZW52KCJPVVRQVVRfUEFUSCIsICJzb3VyY2UvIikKCk9VVEVSX0FUVEVNUFRTID0gaW50KG9z
    echo LmdldGVudigiRE9XTkxPQURfQVRURU1QVFMiLCAiNCIpKQpCQUNLT0ZGX1NUQVJUID0gaW50KG9z
    echo LmdldGVudigiRE9XTkxPQURfQkFDS09GRl9TVEFSVCIsICI0NSIpKQpCQUNLT0ZGX0ZBQ1RPUiA9
    echo IGZsb2F0KG9zLmdldGVudigiRE9XTkxPQURfQkFDS09GRl9GQUNUT1IiLCAiMiIpKQpERUxBWV9C
    echo RVRXRUVOX0ZJTEVTID0gaW50KG9zLmdldGVudigiRE9XTkxPQURfREVMQVlfU0VDT05EUyIsICIy
    echo MCIpKQoKQVJJQTJfQ09OTkVDVElPTlMgPSBpbnQob3MuZ2V0ZW52KCJBUklBMl9DT05ORUNUSU9O
    echo UyIsICIyIikpCkFSSUEyX1NQTElUID0gaW50KG9zLmdldGVudigiQVJJQTJfU1BMSVQiLCAiMiIp
    echo KQpBUklBMl9NSU5fU1BMSVQgPSBvcy5nZXRlbnYoIkFSSUEyX01JTl9TUExJVF9TSVpFIiwgIjVN
    echo IikKCiMgU29tZSBmcmVlIGZpbGUgaG9zdHMgcmVqZWN0IHRoZWlyIG93biBob3N0aW5nIG5vZGVz
    echo IHdoZW4gdGhlIGNsaWVudCBjbGFpbXMgdG8KIyBiZSAiYXJpYTIvLi4uIiAuIEEgYnJvd3NlciBV
    echo QSBhdm9pZHMgdGhhdCBjbGFzcyBvZiByZWZ1c2FsLgpVU0VSX0FHRU5UID0gb3MuZ2V0ZW52KAog
    echo ICAgIkRPV05MT0FEX1VTRVJfQUdFTlQiLAogICAgIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEw
    echo LjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAiCiAgICAiKEtIVE1MLCBsaWtlIEdl
    echo Y2tvKSBDaHJvbWUvMTI1LjAgU2FmYXJpLzUzNy4zNiIsCikKCk1FRElBX0VYVEVOU0lPTlMgPSAo
    echo CiAgICAiLm1wNCIsICIubWt2IiwgIi5tNHYiLCAiLmF2aSIsICIubW92IiwgIi50cyIsICIud2Vi
    echo bSIsICIuZmx2IiwgIi53bXYiLAogICAgIi5yYXIiLCAiLnppcCIsICIuN3oiLCAiLnNydCIsICIu
    echo YXNzIiwgIi52dHQiLAopCgoKZGVmIGV4dHJhY3RfZ29vZ2xlX2RyaXZlX2lkKHVybCk6CiAgICAi
    echo IiJFeHRyYWN0IGEgR29vZ2xlIERyaXZlIGZpbGUgb3IgZm9sZGVyIElEIGZyb20gdGhlIHVzdWFs
    echo IFVSTCBzaGFwZXMuIiIiCiAgICBwYXR0ZXJuID0gcmUuY29tcGlsZSgKICAgICAgICByImRyaXZl
    echo Lmdvb2dsZS5jb20vLio/KD86ZmlsZS9kL3xkcml2ZS9mb2xkZXJzL3xvcGVuXD9pZD18dWNcP2lk
    echo PSkoW14vJj9dKykiCiAgICApCiAgICBtYXRjaCA9IHBhdHRlcm4uc2VhcmNoKHVybCkKICAgIHJl
    echo dHVybiBtYXRjaC5ncm91cCgxKSBpZiBtYXRjaCBlbHNlIE5vbmUKCgpkZWYgc25hcHNob3QoZm9s
    echo ZGVyKToKICAgICIiIlNldCBvZiBmaW5pc2hlZCBmaWxlcyBpbiBgZm9sZGVyYCAoYXJpYTIgLmFy
    echo aWEyIGNvbnRyb2wgZmlsZXMgZXhjbHVkZWQpLiIiIgogICAgdHJ5OgogICAgICAgIHJldHVybiB7
    echo biBmb3IgbiBpbiBvcy5saXN0ZGlyKGZvbGRlcikgaWYgbm90IG4uZW5kc3dpdGgoIi5hcmlhMiIp
    echo fQogICAgZXhjZXB0IE9TRXJyb3I6CiAgICAgICAgcmV0dXJuIHNldCgpCgoKZGVmIHJlcG9ydF9h
    echo ZGRlZChiZWZvcmUpOgogICAgIiIiTG9nIGZpbGVzIHRoYXQgYXBwZWFyZWQgc2luY2UgYGJlZm9y
    echo ZWAuIFB1cmVseSBpbmZvcm1hdGlvbmFsLiIiIgogICAgYWRkZWQgPSBzb3J0ZWQoc25hcHNob3Qo
    echo T1VUUFVUX1BBVEgpIC0gYmVmb3JlKQogICAgaWYgYWRkZWQ6CiAgICAgICAgcHJpbnQoIiAgLT4g
    echo YWRkZWQ6ICIgKyAiLCAiLmpvaW4oYWRkZWQpKQogICAgcmV0dXJuIGFkZGVkCgoKZGVmIGxlZnRv
    echo dmVyX2NvbnRyb2xfZmlsZXMoZm9sZGVyKToKICAgIHRyeToKICAgICAgICByZXR1cm4gW24gZm9y
    echo IG4gaW4gb3MubGlzdGRpcihmb2xkZXIpIGlmIG4uZW5kc3dpdGgoIi5hcmlhMiIpXQogICAgZXhj
    echo ZXB0IE9TRXJyb3I6CiAgICAgICAgcmV0dXJuIFtdCgoKZGVmIGFyaWEyX2V4ZWN1dGFibGUoKToK
    echo ICAgICIiImFyaWEyYy5leGUgc2l0cyBuZXh0IHRvIHRoaXMgc2NyaXB0ICh0aGUgLmJhdCBkb3du
    echo bG9hZHMgaXQgdGhlcmUpLiIiIgogICAgaGVyZSA9IG9zLnBhdGguZGlybmFtZShvcy5wYXRoLmFi
    echo c3BhdGgoX19maWxlX18pKQogICAgZm9yIGNhbmRpZGF0ZSBpbiAoCiAgICAgICAgb3MucGF0aC5q
    echo b2luKGhlcmUsICJhcmlhMmMuZXhlIiksCiAgICAgICAgb3MucGF0aC5qb2luKG9zLmdldGN3ZCgp
    echo LCAiYXJpYTJjLmV4ZSIpLAogICAgICAgICJhcmlhMmMuZXhlIiwKICAgICk6CiAgICAgICAgaWYg
    echo b3MucGF0aC5pc2ZpbGUoY2FuZGlkYXRlKSBvciBjYW5kaWRhdGUgPT0gImFyaWEyYy5leGUiOgog
    echo ICAgICAgICAgICByZXR1cm4gY2FuZGlkYXRlCiAgICByZXR1cm4gImFyaWEyYy5leGUiCgoKZGVm
    echo IHJ1bl9hcmlhMih1cmwpOgogICAgIiIiT25lIGFyaWEyIGF0dGVtcHQuIFJldHVybnMgVHJ1ZSB3
    echo aGVuIHRoZSB0cmFuc2ZlciByZWFsbHkgZmluaXNoZWQuIiIiCiAgICBvcy5tYWtlZGlycyhPVVRQ
    echo VVRfUEFUSCwgZXhpc3Rfb2s9VHJ1ZSkKICAgIGJlZm9yZSA9IHNuYXBzaG90KE9VVFBVVF9QQVRI
    echo KQoKICAgIGNvbW1hbmQgPSBbCiAgICAgICAgYXJpYTJfZXhlY3V0YWJsZSgpLAogICAgICAgICIt
    echo LWNvbnRpbnVlPXRydWUiLAogICAgICAgICItLWNvbnRlbnQtZGlzcG9zaXRpb249dHJ1ZSIsCiAg
    echo ICAgICAgIi0tZGlyPSIgKyBPVVRQVVRfUEFUSCwKICAgICAgICAiLS1tYXgtY29ubmVjdGlvbi1w
    echo ZXItc2VydmVyPSVkIiAlIEFSSUEyX0NPTk5FQ1RJT05TLAogICAgICAgICItLXNwbGl0PSVkIiAl
    echo IEFSSUEyX1NQTElULAogICAgICAgICItLW1pbi1zcGxpdC1zaXplPSIgKyBBUklBMl9NSU5fU1BM
    echo SVQsCiAgICAgICAgIi0tbWF4LWNvbmN1cnJlbnQtZG93bmxvYWRzPTEiLAogICAgICAgICItLW1h
    echo eC10cmllcz0xMCIsCiAgICAgICAgIi0tcmV0cnktd2FpdD0yMCIsCiAgICAgICAgIi0tdGltZW91
    echo dD02MCIsCiAgICAgICAgIi0tY29ubmVjdC10aW1lb3V0PTMwIiwKICAgICAgICAiLS11c2VyLWFn
    echo ZW50PSIgKyBVU0VSX0FHRU5ULAogICAgICAgICItLWNvbnNvbGUtbG9nLWxldmVsPXdhcm4iLAog
    echo ICAgICAgICItLXN1bW1hcnktaW50ZXJ2YWw9MCIsCiAgICAgICAgdXJsLAogICAgXQogICAgcHJp
    echo bnQoIiAgYXJpYTJjOiAiICsgIiAiLmpvaW4oY29tbWFuZCkpCiAgICByZXN1bHQgPSBzdWJwcm9j
    echo ZXNzLnJ1bihjb21tYW5kKQogICAgcmVwb3J0X2FkZGVkKGJlZm9yZSkKCiAgICBpZiByZXN1bHQu
    echo cmV0dXJuY29kZSAhPSAwOgogICAgICAgIHByaW50KCIgIC0+IGFyaWEyYyBleGl0IGNvZGUgJWQi
    echo ICUgcmVzdWx0LnJldHVybmNvZGUpCiAgICAgICAgcmV0dXJuIEZhbHNlCgogICAgY29udHJvbHMg
    echo PSBsZWZ0b3Zlcl9jb250cm9sX2ZpbGVzKE9VVFBVVF9QQVRIKQogICAgaWYgY29udHJvbHM6CiAg
    echo ICAgICAgcHJpbnQoIiAgLT4gaW5jb21wbGV0ZSB0cmFuc2ZlciwgY29udHJvbCBmaWxlKHMpIGxl
    echo ZnQ6ICIgKyAiLCAiLmpvaW4oY29udHJvbHMpKQogICAgICAgIHJldHVybiBGYWxzZQoKICAgIHJl
    echo dHVybiBUcnVlCgoKZGVmIHJ1bl93Z2V0KHVybCk6CiAgICBvcy5tYWtlZGlycyhPVVRQVVRfUEFU
    echo SCwgZXhpc3Rfb2s9VHJ1ZSkKICAgIGJlZm9yZSA9IHNuYXBzaG90KE9VVFBVVF9QQVRIKQogICAg
    echo cmVzdWx0ID0gc3VicHJvY2Vzcy5ydW4oWyJ3Z2V0IiwgIi1QIiwgT1VUUFVUX1BBVEgsIHVybF0p
    echo CiAgICByZXBvcnRfYWRkZWQoYmVmb3JlKQogICAgaWYgcmVzdWx0LnJldHVybmNvZGUgIT0gMDoK
    echo ICAgICAgICBwcmludCgiICAtPiB3Z2V0IGV4aXQgY29kZSAlZCIgJSByZXN1bHQucmV0dXJuY29k
    echo ZSkKICAgICAgICByZXR1cm4gRmFsc2UKICAgIHJldHVybiBUcnVlCgoKZGVmIHJ1bl9jdXJsKHVy
    echo bCk6CiAgICBvcy5tYWtlZGlycyhPVVRQVVRfUEFUSCwgZXhpc3Rfb2s9VHJ1ZSkKICAgIGJlZm9y
    echo ZSA9IHNuYXBzaG90KE9VVFBVVF9QQVRIKQogICAgcmVzdWx0ID0gc3VicHJvY2Vzcy5ydW4oWyJj
    echo dXJsIiwgIi1mTCIsICItTyIsICItSiIsICItLWNyZWF0ZS1kaXJzIiwgdXJsXSwKICAgICAgICAg
    echo ICAgICAgICAgICAgICAgICAgIGN3ZD1PVVRQVVRfUEFUSCkKICAgIHJlcG9ydF9hZGRlZChiZWZv
    echo cmUpCiAgICBpZiByZXN1bHQucmV0dXJuY29kZSAhPSAwOgogICAgICAgIHByaW50KCIgIC0+IGN1
    echo cmwgZXhpdCBjb2RlICVkIiAlIHJlc3VsdC5yZXR1cm5jb2RlKQogICAgICAgIHJldHVybiBGYWxz
    echo ZQogICAgcmV0dXJuIFRydWUKCgpkZWYgcnVuX2dkb3duKGZpbGVfaWQpOgogICAgb3MubWFrZWRp
    echo cnMoT1VUUFVUX1BBVEgsIGV4aXN0X29rPVRydWUpCiAgICBiZWZvcmUgPSBzbmFwc2hvdChPVVRQ
    echo VVRfUEFUSCkKICAgIHRyeToKICAgICAgICBnZG93bi5kb3dubG9hZChpZD1maWxlX2lkLCBvdXRw
    echo dXQ9T1VUUFVUX1BBVEgsIHF1aWV0PUZhbHNlKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlcnJv
    echo cjogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBub3FhOiBCTEUwMDEKICAgICAg
    echo ICBwcmludCgiICBnZG93biBmaWxlIGRvd25sb2FkIGZhaWxlZCAoJXMpLiBUcnlpbmcgYXMgZm9s
    echo ZGVyLi4uIiAlIGVycm9yKQogICAgICAgIHRyeToKICAgICAgICAgICAgZ2Rvd24uZG93bmxvYWRf
    echo Zm9sZGVyKGlkPWZpbGVfaWQsIG91dHB1dD1PVVRQVVRfUEFUSCwgcXVpZXQ9RmFsc2UsCiAgICAg
    echo ICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXN1bWU9VHJ1ZSkKICAgICAgICBleGNlcHQg
    echo RXhjZXB0aW9uIGFzIGZvbGRlcl9lcnJvcjogICAgICAgICAgICAgICAgICAgICAgICMgbm9xYTog
    echo QkxFMDAxCiAgICAgICAgICAgIHByaW50KCIgIGdkb3duIGZvbGRlciBkb3dubG9hZCBmYWlsZWQ6
    echo ICVzIiAlIGZvbGRlcl9lcnJvcikKICAgICAgICAgICAgcmV0dXJuIEZhbHNlCiAgICByZXBvcnRf
    echo YWRkZWQoYmVmb3JlKQogICAgcmV0dXJuIFRydWUKCgpkZWYgcnVuX21lZGlhZmlyZSh1cmwpOgog
    echo ICAgb3MubWFrZWRpcnMoT1VUUFVUX1BBVEgsIGV4aXN0X29rPVRydWUpCiAgICBiZWZvcmUgPSBz
    echo bmFwc2hvdChPVVRQVVRfUEFUSCkKCiAgICB0YXJnZXQgPSB1cmwKICAgIGlmIHVybC5zdGFydHN3
    echo aXRoKCJodHRwczovL2Rvd25sb2FkIik6CiAgICAgICAgcGFydHMgPSB1cmwuc3BsaXQoIi8iKQog
    echo ICAgICAgIGlmIGxlbihwYXJ0cykgPCA2OgogICAgICAgICAgICBwcmludCgiICBNZWRpYUZpcmUg
    echo cmF3IGxpbmsgZm9ybWF0IG5vdCByZWNvZ25pc2VkLiIpCiAgICAgICAgICAgIHJldHVybiBGYWxz
    echo ZQogICAgICAgIHRhcmdldCA9ICJodHRwczovL3d3dy5tZWRpYWZpcmUuY29tL2ZpbGUvJXMvJXMi
    echo ICUgKHBhcnRzWy0yXSwgcGFydHNbLTFdKQogICAgZWxpZiAibWVkaWFmaXJlLmNvbSIgbm90IGlu
    echo IHVybDoKICAgICAgICByZXR1cm4gRmFsc2UKCiAgICBwcmV2aW91c19kaXIgPSBvcy5nZXRjd2Qo
    echo KQogICAgdHJ5OgogICAgICAgIG9zLmNoZGlyKE9VVFBVVF9QQVRIKQogICAgICAgIG1lZGlhZmly
    echo ZV9kbC5kb3dubG9hZCh0YXJnZXQsIHF1aWV0PUZhbHNlKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBh
    echo cyBlcnJvcjogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBub3FhOiBCTEUwMDEK
    echo ICAgICAgICBwcmludCgiICBNZWRpYUZpcmUgZG93bmxvYWQgZmFpbGVkOiAlcyIgJSBlcnJvcikK
    echo ICAgICAgICByZXR1cm4gRmFsc2UKICAgIGZpbmFsbHk6CiAgICAgICAgb3MuY2hkaXIocHJldmlv
    echo dXNfZGlyKQoKICAgIHJlcG9ydF9hZGRlZChiZWZvcmUpCiAgICByZXR1cm4gVHJ1ZQoKCmRlZiBh
    echo dHRlbXB0X29uY2UodXJsKToKICAgICIiIlJvdXRlIG9uZSBVUkwgdG8gdGhlIHJpZ2h0IHRvb2wu
    echo IFRydWUgPSBmaWxlIHJlYWxseSBhcnJpdmVkLiIiIgogICAgZmlsZV9pZCA9IGV4dHJhY3RfZ29v
    echo Z2xlX2RyaXZlX2lkKHVybCkKICAgIHRyeToKICAgICAgICBpZiBmaWxlX2lkOgogICAgICAgICAg
    echo ICBwcmludCgiICBob3N0OiBHb29nbGUgRHJpdmUgKCVzKSIgJSBmaWxlX2lkKQogICAgICAgICAg
    echo ICByZXR1cm4gcnVuX2dkb3duKGZpbGVfaWQpCiAgICAgICAgaWYgIm1zdWJiMi5uZXQiIGluIHVy
    echo bDoKICAgICAgICAgICAgcHJpbnQoIiAgaG9zdDogbXN1YmIyLm5ldCAod2dldCkiKQogICAgICAg
    echo ICAgICByZXR1cm4gcnVuX3dnZXQodXJsKQogICAgICAgIGlmICJ3b3JrZXJzIiBpbiB1cmw6CiAg
    echo ICAgICAgICAgIHByaW50KCIgIGhvc3Q6IHdvcmtlcnMgKGN1cmwpIikKICAgICAgICAgICAgcmV0
    echo dXJuIHJ1bl9jdXJsKHVybCkKICAgICAgICBpZiB1cmwuc3RhcnRzd2l0aCgiaHR0cHM6Ly9kb3du
    echo bG9hZCIpIG9yICJtZWRpYWZpcmUuY29tIiBpbiB1cmw6CiAgICAgICAgICAgIHByaW50KCIgIGhv
    echo c3Q6IE1lZGlhRmlyZSIpCiAgICAgICAgICAgIHJldHVybiBydW5fbWVkaWFmaXJlKHVybCkKCiAg
    echo ICAgICAgcHJpbnQoIiAgaG9zdDogZ2VuZXJpYyBkaXJlY3QgbGluayAoYXJpYTJjKSIpCiAgICAg
    echo ICAgcmV0dXJuIHJ1bl9hcmlhMih1cmwpCiAgICBleGNlcHQgRmlsZU5vdEZvdW5kRXJyb3IgYXMg
    echo ZXJyb3I6CiAgICAgICAgcHJpbnQoIiAgcmVxdWlyZWQgdG9vbCBub3QgZm91bmQ6ICVzIiAlIGVy
    echo cm9yKQogICAgICAgIHJldHVybiBGYWxzZQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlcnJvcjog
    echo ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBub3FhOiBCTEUwMDEKICAgICAgICBw
    echo cmludCgiICB1bmV4cGVjdGVkIGVycm9yOiAlcyIgJSBlcnJvcikKICAgICAgICByZXR1cm4gRmFs
    echo c2UKCgpkZWYgbWFpbigpOgogICAgbGlua3NfY29udGVudCA9IG9zLmdldGVudigiTElOS1NfQ09O
    echo VEVOVCIpIG9yICIiCiAgICBsaW5rcyA9IFtsaW5lLnN0cmlwKCkgZm9yIGxpbmUgaW4gbGlua3Nf
    echo Y29udGVudC5zcGxpdGxpbmVzKCkgaWYgbGluZS5zdHJpcCgpXQoKICAgIGlmIG5vdCBsaW5rczoK
    echo ICAgICAgICBwcmludCgiRVJST1I6IExJTktTX0NPTlRFTlQgZW52aXJvbm1lbnQgdmFyaWFibGUg
    echo aXMgbWlzc2luZyBvciBlbXB0eS4iKQogICAgICAgIHJldHVybiAxCiAgICBwcmludCgiTG9hZGVk
    echo ICVkIGxpbmtzIGZyb20gZW52aXJvbm1lbnQgdmFyaWFibGUuIiAlIGxlbihsaW5rcykpCgogICAg
    echo b3MubWFrZWRpcnMoT1VUUFVUX1BBVEgsIGV4aXN0X29rPVRydWUpCgogICAgZmFpbGVkID0gW10K
    echo ICAgIGZvciBpbmRleCwgdXJsIGluIGVudW1lcmF0ZShsaW5rcywgc3RhcnQ9MSk6CiAgICAgICAg
    echo cHJpbnQoIlxuLS0tIFslZC8lZF0gUHJvY2Vzc2luZyBVUkw6ICVzIC0tLSIgJSAoaW5kZXgsIGxl
    echo bihsaW5rcyksIHVybCkpCgogICAgICAgIGRlbGF5ID0gQkFDS09GRl9TVEFSVAogICAgICAgIGZv
    echo ciBhdHRlbXB0IGluIHJhbmdlKDEsIE9VVEVSX0FUVEVNUFRTICsgMSk6CiAgICAgICAgICAgIHBy
    echo aW50KCJBdHRlbXB0ICVkLyVkIiAlIChhdHRlbXB0LCBPVVRFUl9BVFRFTVBUUykpCiAgICAgICAg
    echo ICAgIGlmIGF0dGVtcHRfb25jZSh1cmwpOgogICAgICAgICAgICAgICAgcHJpbnQoIk9LOiBkb3du
    echo bG9hZCBmaW5pc2hlZC4iKQogICAgICAgICAgICAgICAgYnJlYWsKCiAgICAgICAgICAgIGlmIGF0
    echo dGVtcHQgPT0gT1VURVJfQVRURU1QVFM6CiAgICAgICAgICAgICAgICBwcmludCgiRkFJTEVEIGFm
    echo dGVyICVkIGF0dGVtcHRzOiAlcyIgJSAoT1VURVJfQVRURU1QVFMsIHVybCkpCiAgICAgICAgICAg
    echo ICAgICBmYWlsZWQuYXBwZW5kKHVybCkKICAgICAgICAgICAgICAgIGJyZWFrCgogICAgICAgICAg
    echo ICBwcmludCgiUmV0cnlpbmcgaW4gJWRzICh0aGUgaG9zdCBtYXkgYmUgcmF0ZSBsaW1pdGluZyB1
    echo cykuLi4iCiAgICAgICAgICAgICAgICAgICUgZGVsYXkpCiAgICAgICAgICAgIHRpbWUuc2xlZXAo
    echo ZGVsYXkpCiAgICAgICAgICAgIGRlbGF5ID0gaW50KGRlbGF5ICogQkFDS09GRl9GQUNUT1IpCgog
    echo ICAgICAgIGlmIGluZGV4IDwgbGVuKGxpbmtzKSBhbmQgREVMQVlfQkVUV0VFTl9GSUxFUzoKICAg
    echo ICAgICAgICAgcHJpbnQoIlBhdXNpbmcgJWRzIGJlZm9yZSB0aGUgbmV4dCBsaW5rLi4uIiAlIERF
    echo TEFZX0JFVFdFRU5fRklMRVMpCiAgICAgICAgICAgIHRpbWUuc2xlZXAoREVMQVlfQkVUV0VFTl9G
    echo SUxFUykKCiAgICBmaWxlcyA9IHNvcnRlZChzbmFwc2hvdChPVVRQVVRfUEFUSCkpCiAgICBwcmlu
    echo dCgiXG49PT09PT09PT09PT09PT09IERPV05MT0FEIFNVTU1BUlkgPT09PT09PT09PT09PT09PSIp
    echo CiAgICBwcmludCgiTGlua3MgcmVxdWVzdGVkIDogJWQiICUgbGVuKGxpbmtzKSkKICAgIHByaW50
    echo KCJMaW5rcyBmYWlsZWQgICAgOiAlZCIgJSBsZW4oZmFpbGVkKSkKICAgIGZvciB1cmwgaW4gZmFp
    echo bGVkOgogICAgICAgIHByaW50KCIgICBGQUlMRUQgICVzIiAlIHVybCkKICAgIHByaW50KCJGaWxl
    echo cyBpbiAlczoiICUgT1VUUFVUX1BBVEgpCiAgICBmb3IgbmFtZSBpbiBmaWxlczoKICAgICAgICBw
    echo cmludCgiICAgJXMiICUgbmFtZSkKICAgIHByaW50KCI9PT09PT09PT09PT09PT09PT09PT09PT09
    echo PT09PT09PT09PT09PT09PT09PT09PT09IikKCiAgICBpZiBmYWlsZWQ6CiAgICAgICAgcHJpbnQo
    echo IlxuRVJST1I6ICVkIG9mICVkIGRvd25sb2FkcyBmYWlsZWQgLSByZWZ1c2luZyB0byBjb250aW51
    echo ZSB3aXRoIGEgIgogICAgICAgICAgICAgICJwYXJ0aWFsIGJhdGNoLiIgJSAobGVuKGZhaWxlZCks
    echo IGxlbihsaW5rcykpKQogICAgICAgIHJldHVybiAxCgogICAgcHJpbnQoIlxuRG93bmxvYWQgc2Ny
    echo aXB0IGZpbmlzaGVkIC0gYWxsICVkIGxpbmtzIGFyZSBjb21wbGV0ZS4iICUgbGVuKGxpbmtzKSkK
    echo ICAgIHJldHVybiAwCgoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgIHN5cy5leGl0KG1h
    echo aW4oKSkK
)
certutil -f -decode "cm720-next.b64" "cm720-next.py" >nul || (
    echo ERROR: Could not create cm720-next.py.
    exit /b 1
)
del /q "cm720-next.b64" 2>nul

python -c "import hashlib;print('cm720-next.py sha256', hashlib.sha256(open('cm720-next.py','rb').read()).hexdigest())"
rem --- end of embedded downloader --------------------------------------------

python cm720-next.py
if errorlevel 1 (
    echo ERROR: One or more downloads failed. Aborting before processing so the
    echo        job goes red instead of emailing a partial batch.
    exit /b 1
)
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
if errorlevel 1 (
    echo ERROR: The processing chain failed. Not sending a receipt email.
    exit /b 1
)

popd
endlocal

rem This script is stored in Hard2SoftsubV1_5_2, not in core.
python send_email_file-next.py
