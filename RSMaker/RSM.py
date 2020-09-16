import sys, json
from random import randint

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./QTemplates/RSM_Main.ui', self)
        self.initial_setup()



    def initial_setup(self):
        _translate = QtCore.QCoreApplication.translate
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
        
        self.btn_rr_StartArea.clicked.connect(lambda: self.simple_reroll(self.txt_StartArea, self.lck_StartArea, rt_id['StartArea']))
        
        # Set default starting area
        roll = randint(1, len(rolltables[rt_id['StartArea']]['Data'])-1)
        self.txt_StartArea.appendPlainText(rolltables[rt_id['StartArea']]['Data'][roll]['Value'])
    
    def simple_reroll(self, pt_target, lck, tableid):
        try:
            if not self.lck_StartArea.isChecked():
                roll = randint(0, len(rolltables[tableid]['Data'])-1)
                print("Rolled an", roll, "target:", pt_target.objectName(), "object type:", type(pt_target))
                txt = rolltables[tableid]['Data'][roll]['Value']
                pt_target.clear()
                pt_target.appendPlainText(txt)
            else:
                print("Field is locked, not updating")
        except Exception as e:
            print("Error received:", e)
            self.warning_popup(e)
    
    def warning_popup(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(str(message))
        msgBox.setWindowTitle("Error!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()    

if __name__ == "__main__":  
    # import roll tables
    with open('rolltables.json','r') as f:
        rolltables = json.load(f)
    
    # map table id and names to rt_id dictionary
    i=0
    rt_id = {}
    for t in rolltables:
        rt_id.update({t['Table']:i})
        i+=1

    # load Ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())


