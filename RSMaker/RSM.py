import sys
from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QOpenGLWidget

from QTemplates import RSM_Main, Chamber
from ui import QtSetup, GLMap

from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

class MainWindow(QMainWindow, RSM_Main.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        QtSetup.generic_setup(self)

        

        # initialize list and helpers for chambers
        self.btn_gen_chamber.clicked.connect(self.new_chamber)
        self.chambers = list()
        self.chamber_btn_x = 10
        self.chamber_btn_y = 20
        self.chamber_btn_x_initial = 10
        self.chamber_btn_x_offset = 120
        self.chamber_btn_y_offset = 30
        self.chamber_btn_x_limit = 251
        self.chamber_btn_y_limit = 201
        self.chamber_id = 0

        # Map Stuff
        
        
        # print('creating widget')
        # self.gl_map = GLMap.MapWidSimpleViewerget(self.centralwidget)
        # print('Changing geometry')
        # self.gl_map.setGeometry(QtCore.QRect(710, 330, 300, 300))
        # print('Updating name')
        # self.gl_map.setObjectName("gl_map")
        # #print('Calling update from RSM')
        # #self.gl_map.update()
        # #print('Calling initalize')
        # #self.gl_map.initializeGL()
        # #print('Calling update')
        # #self.gl_map.update()
        # #print('Calling cube from RSM')
        # #self.gl_map.makeCurrent()
        # #self.gl_map.cube()
        # #self.gl_map.show()
        
        viewer = GLMap.MapWidget(self.centralwidget)
        viewer.resize_cb.connect( GLMap.resize )
        viewer.initialize_cb.connect( GLMap.initialize )
        viewer.render_cb.connect( GLMap.render )

        viewer.setGeometry(QtCore.QRect(710, 330, 300, 300))
        viewer.setMouseTracking(True)

        # keyboard & mouse interactions
        viewer.key_press_cb.connect( GLMap.key_press )
        viewer.key_release_cb.connect( GLMap.key_release )
        viewer.mouse_press_cb.connect( GLMap.mouse_press )
        viewer.mouse_release_cb.connect( GLMap.mouse_release )
        viewer.mouse_move_cb.connect( GLMap.mouse_move )
        viewer.mouse_wheel_cb.connect( GLMap.mouse_wheel )

    # custom functions for this window
    def new_chamber(self):
        if self.chamber_btn_y > self.chamber_btn_y_limit:
            QtSetup.warning_popup("Max Chambers reached.")
            return
        
        # create new button
        c_btn = QtWidgets.QPushButton(self.box_chambers)
        c_btn.setGeometry(QtCore.QRect(self.chamber_btn_x, self.chamber_btn_y, 111, 23))
        c_btn.setObjectName("btn_chamber_"+str(self.chamber_id))
        c_btn.setText(QtCore.QCoreApplication.translate("MainWindow", "Chamber "+str(self.chamber_id)))
        c_btn.clicked.connect(self.pull_chamber)
        c_btn.show()

        # add and show new chamber window
        chamber = ChamberWindow(self)
        self.chambers.append(chamber)
        if self.b_ShowChamber.isChecked():
            chamber.show()

        # increment chamber helpers
        self.chamber_btn_x += self.chamber_btn_x_offset
        
        if self.chamber_btn_x > 251:
            self.chamber_btn_x = self.chamber_btn_x_initial # reset x position
            self.chamber_btn_y += self.chamber_btn_y_offset # increment y

        self.chamber_id +=1

    def pull_chamber(self):
        try:
            cid = self.sender().objectName()
            cid = int(cid[cid.rfind('_')+1:])
            chamber = self.chambers[cid]
            chamber.show()
        except Exception as e:
            print("Error received:", e)
            QtSetup.warning_popup(e)

    

class ChamberWindow(QMainWindow, Chamber.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ChamberWindow, self).__init__(parent)
        self.setupUi(self)
        QtSetup.generic_setup(self)
    

if __name__ == "__main__":  
    # load Ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())