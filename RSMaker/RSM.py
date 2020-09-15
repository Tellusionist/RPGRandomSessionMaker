from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint
import json

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowIcon(QtGui.QIcon('./assets/5e_logo_dark_256.ico')) 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_Header = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Header.setGeometry(QtCore.QRect(0, 0, 261, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_Header.setFont(font)
        self.lbl_Header.setObjectName("lbl_Header")
        self.btn_rr_all = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rr_all.setGeometry(QtCore.QRect(30, 440, 131, 31))
        self.btn_rr_all.setObjectName("btn_rr_all")
        self.lbl_DungeonType = QtWidgets.QLabel(self.centralwidget)
        self.lbl_DungeonType.setGeometry(QtCore.QRect(170, 70, 31, 16))
        self.lbl_DungeonType.setObjectName("lbl_DungeonType")
        self.cb_DungeonType = QtWidgets.QComboBox(self.centralwidget)
        self.cb_DungeonType.setGeometry(QtCore.QRect(210, 70, 91, 22))
        self.cb_DungeonType.setObjectName("cb_DungeonType")
        self.lck_Dungeontype = QtWidgets.QCheckBox(self.centralwidget)
        self.lck_Dungeontype.setGeometry(QtCore.QRect(100, 70, 16, 18))
        self.lck_Dungeontype.setText("")
        self.lck_Dungeontype.setObjectName("lck_Dungeontype")
        self.lbl_Locked = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Locked.setGeometry(QtCore.QRect(90, 50, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_Locked.setFont(font)
        self.lbl_Locked.setObjectName("lbl_Locked")
        self.lbl_Environment = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Environment.setGeometry(QtCore.QRect(140, 100, 71, 16))
        self.lbl_Environment.setObjectName("lbl_Environment")
        self.lck_Environment = QtWidgets.QCheckBox(self.centralwidget)
        self.lck_Environment.setGeometry(QtCore.QRect(100, 100, 16, 18))
        self.lck_Environment.setText("")
        self.lck_Environment.setObjectName("lck_Environment")
        self.cb_Environment = QtWidgets.QComboBox(self.centralwidget)
        self.cb_Environment.setGeometry(QtCore.QRect(210, 100, 91, 22))
        self.cb_Environment.setObjectName("cb_Environment")       
        self.lbl_StartArea = QtWidgets.QLabel(self.centralwidget)
        self.lbl_StartArea.setGeometry(QtCore.QRect(130, 130, 71, 16))
        self.lbl_StartArea.setObjectName("lbl_StartArea")
        self.lck_StartArea = QtWidgets.QCheckBox(self.centralwidget)
        self.lck_StartArea.setGeometry(QtCore.QRect(100, 130, 16, 18))
        self.lck_StartArea.setText("")
        self.lck_StartArea.setObjectName("lck_StartArea")
        self.txt_StartArea = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_StartArea.setGeometry(QtCore.QRect(210, 130, 461, 31))
        self.txt_StartArea.setObjectName("txt_StartArea")
        self.btn_rr_type = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rr_type.setGeometry(QtCore.QRect(10, 70, 71, 21))
        self.btn_rr_type.setObjectName("btn_rr_type")
        self.btn_rr_environment = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rr_environment.setGeometry(QtCore.QRect(10, 100, 71, 21))
        self.btn_rr_environment.setObjectName("btn_rr_environment")
        self.btn_rr_StartArea = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rr_StartArea.setGeometry(QtCore.QRect(10, 130, 71, 21))
        self.btn_rr_StartArea.setObjectName("btn_rr_StartArea")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuGenerators = QtWidgets.QMenu(self.menubar)
        self.menuGenerators.setObjectName("menuGenerators")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionChamber = QtWidgets.QAction(MainWindow)
        self.actionChamber.setObjectName("actionChamber")
        self.actionPassage = QtWidgets.QAction(MainWindow)
        self.actionPassage.setObjectName("actionPassage")
        self.actionDoor = QtWidgets.QAction(MainWindow)
        self.actionDoor.setObjectName("actionDoor")
        self.actionEntrance = QtWidgets.QAction(MainWindow)
        self.actionEntrance.setObjectName("actionEntrance")
        self.actionMonster = QtWidgets.QAction(MainWindow)
        self.actionMonster.setObjectName("actionMonster")
        self.actionNPC = QtWidgets.QAction(MainWindow)
        self.actionNPC.setObjectName("actionNPC")
        self.actionPlayer = QtWidgets.QAction(MainWindow)
        self.actionPlayer.setObjectName("actionPlayer")
        self.actionCity = QtWidgets.QAction(MainWindow)
        self.actionCity.setObjectName("actionCity")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionRoll_Tables = QtWidgets.QAction(MainWindow)
        self.actionRoll_Tables.setObjectName("actionRoll_Tables")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addAction(self.actionRoll_Tables)
        self.menuGenerators.addAction(self.actionChamber)
        self.menuGenerators.addAction(self.actionPassage)
        self.menuGenerators.addAction(self.actionDoor)
        self.menuGenerators.addAction(self.actionEntrance)
        self.menuGenerators.addSeparator()
        self.menuGenerators.addAction(self.actionMonster)
        self.menuGenerators.addAction(self.actionNPC)
        self.menuGenerators.addAction(self.actionPlayer)
        self.menuGenerators.addSeparator()
        self.menuGenerators.addAction(self.actionCity)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuGenerators.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # import roll tables
        with open('rolltables.json','r') as f:
            rolltables = json.load(f)
        
        # map table id and names to rt_id dictionary
        i=0
        rt_id = {}
        for t in rolltables:
            rt_id.update({t['Table']:i})
            i+=1

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RPG Random Session Maker"))
        self.lbl_Header.setText(_translate("MainWindow", "Welcome to the RPG Random Session Maker!"))
        self.btn_rr_all.setText(_translate("MainWindow", "Generate Starting Area"))
        self.lbl_Locked.setText(_translate("MainWindow", "Locked"))

        self.lbl_DungeonType.setText(_translate("MainWindow", "Type:"))  
        
        # load dungeon type values (limit to distinct values)
        i = 0
        for item in list(set(val for dic in rolltables[rt_id['DungeonType']]['Data'] for val in dic.values())):
            self.cb_DungeonType.addItem("")
            self.cb_DungeonType.setItemText(i, _translate("MainWindow", item))
            i+=1        

        self.lbl_Environment.setText(_translate("MainWindow", "Environment:"))
        # load environment values
        i = 0
        for item in list(set(val for dic in rolltables[rt_id['Environment']]['Data'] for val in dic.values())):
            self.cb_Environment.addItem("")
            self.cb_Environment.setItemText(i, _translate("MainWindow", item))
            i+=1

        self.lbl_StartArea.setText(_translate("MainWindow", "Starting Area:"))
        
        # Set default starting area
        roll = randint(1, len(rolltables[rt_id['StartArea']]['Data']))
        self.txt_StartArea.textCursor().insertText(rolltables[rt_id['StartArea']]['Data'][roll]['Value'])

        self.btn_rr_type.setText(_translate("MainWindow", "Re-Roll"))
        self.btn_rr_environment.setText(_translate("MainWindow", "Re-Roll"))
        self.btn_rr_StartArea.setText(_translate("MainWindow", "Re-Roll"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuGenerators.setTitle(_translate("MainWindow", "Generators"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionChamber.setText(_translate("MainWindow", "Chamber"))
        self.actionPassage.setText(_translate("MainWindow", "Passage"))
        self.actionDoor.setText(_translate("MainWindow", "Door"))
        self.actionEntrance.setText(_translate("MainWindow", "Entrance"))
        self.actionMonster.setText(_translate("MainWindow", "Monster"))
        self.actionNPC.setText(_translate("MainWindow", "NPC"))
        self.actionPlayer.setText(_translate("MainWindow", "Player"))
        self.actionCity.setText(_translate("MainWindow", "City"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionRoll_Tables.setText(_translate("MainWindow", "Roll Tables"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

