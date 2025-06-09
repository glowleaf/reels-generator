@echo off
set PATH=%PATH%;C:\Program Files\ffmpeg-7.1.1-full_build\bin
python main.py "Μια γυναίκα που πάλευε με την εικόνα του σώματός της στην παραλία" --duration 180 --background "assets/daphnebeach.mp4"
pause 