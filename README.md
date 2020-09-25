# RPGRandomSessionMaker
A random dungeon and mob generator tool used to run random sessions (in real-time) or to be used as inspiration for future sessions. Random roll tables are based inspired by the 5e DMG, but can be used for any RPG setting. 


## Setup
Run `pipenv install` at the root directory to setup the the virtual environment. 

If you want to use Qt designer, first `pipenv install --dev` to get the packages. After installation you will likely need to copy the contents of the platforms folder from .\site-packages\PyQt5\Qt\plugins\platforms to .\site-packages\pyqt5_tools\Qt\bin\platforms or you might see a dll or plugin error.

## Using QtDesigner
Check .\site-packages\pyqt5_tools\Qt\bin for designer.exe which is the tool used to help design the front end forms. DesignerTemplates includes the .ui files from the Designer.exe and the associate python file of each form. To generate the python from the .ui and .qrc file use the make_ut.bat under RSMaker\QTemplates.

All python resource files must reside in the same location as the RSM_Main.py. This is to get around the ui/py file calling the resource import from the root location.

Finally got it working after watching https://www.youtube.com/watch?v=umU9VP_uX34 (check minute 20)