cd ..\
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --onefile --clean --noconsole --add-data "layout;layout" --add-data "VLC;VLC" --add-data "ffmpeg;ffmpeg" --icon=layout\resources\logo.ico --name=Razor app.py
start dist
