cd ..\
python -m pip install -r requirements.txt pysdl2-dll pyinstaller
python scripts\dll.py
python scripts\DiscordSDK.py
python -m PyInstaller --onefile --clean --noconsole --add-data "layout;layout" --add-data "dll\*.dll;." --add-data "lib;lib" --add-data "scripts\urlRegister.reg;urlRegister.reg" --icon=layout\resources\logo.ico --name=Razor app.py
start dist
