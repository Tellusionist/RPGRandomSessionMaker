# RPGRandomSessionMaker
A random dungeon and mob generator tool used to run random sessions (in real-time) or to be used as inspiration for future sessions. Random roll tables are based inspired by the 5e DMG, but can be used for any RPG setting. 


## Setup
Run `pipenv install` at the root directory to setup the the virtual environment. 

If you want to use Qt designer, first `pipenv install --dev` to get the packages. After installation you will likely need to copy the contents of the platforms folder from .\site-packages\PyQt5\Qt\plugins\platforms to .\site-packages\pyqt5_tools\Qt\bin\platforms or you might see a dll or plugin error.

## Using QtDesigner
Check .\site-packages\pyqt5_tools\Qt\bin for designer.exe which is the tool used to help design the front end forms. DesignerTemplates includes the .ui files from the Designer.exe and the associate python file of each form. To generate the python from the .ui designer file, navigate to the DesignerTemplates folder and in command prompt type `pyuic5 -x FileName.ui -o PythonFilename.py`