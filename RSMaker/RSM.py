import sys
from random import randint, randrange

from PyQt5 import QtCore, QtWidgets, QtGui
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

        # self.btn_in_the_way = QtWidgets.QPushButton(self.centralwidget)
        # self.btn_in_the_way.setGeometry(QtCore.QRect(630, 670, 75, 23))
        # self.btn_in_the_way.setObjectName("btn_in_the_way")
        # self.btn_in_the_way.setText(QtCore.QCoreApplication.translate("MainWindow", "Hallo"))
        # self.btn_in_the_way.clicked.connect(self.addbox)

        # Fancy Map Stuff
        # Store a list of scene objects
        self.scene_objs = [] 
        
        self.viewer = GLMap.MapWidget(self.centralwidget)
        self.viewer.resize_cb.connect( GLMap.resize )
        self.viewer.initialize_cb.connect( GLMap.initialize )
        #viewer.render_cb.connect( GLMap.render )
        self.viewer.renderbox_cb.connect( GLMap.box )
        self.btn_drawbox.clicked.connect(self.addbox)
        
        

        self.viewer.setGeometry(QtCore.QRect(40, 600, 920, 240))
        self.viewer.setMouseTracking(True)

        

        # keyboard & mouse interactions
        self.viewer.key_press_cb.connect( GLMap.key_press )
        self.viewer.key_release_cb.connect( GLMap.key_release )
        self.viewer.mouse_press_cb.connect( GLMap.mouse_press )
        self.viewer.mouse_release_cb.connect( GLMap.mouse_release )
        self.viewer.mouse_move_cb.connect( GLMap.mouse_move )
        self.viewer.mouse_wheel_cb.connect( GLMap.mouse_wheel )
        
        
        #self.btn_draw.clicked.connect(self.add_rectangle)
        #self.canvas = Canvas(self)
        #self.canvas.setGeometry(QtCore.QRect(710, 340, 300, 220))

        
    
    # override the mouse wheelEvent to check and send event to OpenGL widget
    def wheelEvent(self, evt):
        if self.viewer.underMouse():
            self.viewer.mouse_wheel_cb.emit(evt, self.viewer, self.scene_objs)
        
    def addbox(self):
        base_vertices = (
            ( 1, -1, -1),
            ( 1,  1, -1),
            (-1,  1, -1),
            (-1, -1, -1)
        )
        
        offest_x = randint(-10,10)
        offest_y = randint(-10,10)

        new_vertices = []
        for base_v in base_vertices:
            new_v = []
            new_x = base_v[0] + offest_x
            new_y = base_v[1] + offest_y
            new_z = base_v[2]
            new_v.append(new_x)
            new_v.append(new_y)
            new_v.append(new_z)
            
            new_vertices.append(new_v)

        
        base_edges = edges = (
            (0,1),
            (0,3),
            (2,1),
            (2,3)
        )

        new_obj = {"vertices":new_vertices, "edges":base_edges}

        self.scene_objs.append(new_obj)
        self.viewer.renderbox_cb.emit(self.viewer, self.scene_objs)


    # def add_rectangle(self):
    #     w = self.canvas.width()
    #     h = self.canvas.height()
    #     x0, y0 = randrange(w), randrange(h)
    #     x1, y1 = randrange(w), randrange(h)

    #     shape = QtCore.QRect(min(x0,x1), min(y0,y1), abs(x0-x1), abs(y0-y1))
    #     color = QtGui.QColor.fromRgb(*(randrange(256) for i in range(3)), 180)
    #     self.canvas.add_rectangle(shape, color)
        

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

class Canvas(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rectangles = []

    def add_rectangle(self, rect, color):
        self.rectangles.append((rect, color))
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtCore.Qt.white)
        painter.setBrush(brush)
        painter.drawRect(event.rect())

        pen = QtGui.QPen()
        pen.setWidth(3)
        for rect, color in self.rectangles:
            pen.setColor(color)
            painter.setPen(pen)
            brush.setColor(color)
            painter.setBrush(brush)
            painter.drawRect(rect)

if __name__ == "__main__":  
    # load Ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())