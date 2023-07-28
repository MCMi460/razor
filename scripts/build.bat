cd ..\
python -m pip install -r requirements.txt pysdl2-dll pyinstaller
python scripts\dll.py
python -m PyInstaller --onefile --clean --noconsole --add-data "layout;layout" --add-data "dll\*.dll;." --icon=layout\resources\logo.ico --name=Razor app.py
start dist
