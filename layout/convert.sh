rm ./*.py
pyuic5 -x mainwindow.ui > ./mainwindow.py
pyuic5 -x credits.ui > ./credits.py
pyuic5 -x terms.ui > ./terms.py
pyuic5 -x miniplayer.ui > ./miniplayer.py
pyuic5 -x settings.ui > ./settings.py
pyuic5 -x install.ui > ./install.py
