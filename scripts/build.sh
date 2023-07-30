cd ..

# Delete previous build files
if [ -d ./build/ ]
then
  rm -rf ./build/
fi
if [ -d ./dist/ ]
then
  rm -rf ./dist/
fi

# Actual building
python3 -m pip install -r requirements.txt py2app # Install requirements + py2app
python3 -m pip uninstall -y pysdl2-dll # pysdl2-dll WILL cause failures on MacOS
python3 scripts/DiscordSDK.py
python3 scripts/setupMac.py py2app -O2 # Build
open dist # Open for user's benefit
