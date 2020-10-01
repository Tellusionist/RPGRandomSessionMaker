import math
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL

import OpenGL.GL as gl
# references
# http://jamesgregson.ca/pyqt5-pyopengl-example.html
# https://github.com/baoboa/pyqt5/blob/master/examples/opengl/grabber.py

class MapWidget(QtOpenGL.QGLWidget):

    initialize_cb    = QtCore.pyqtSignal()
    resize_cb        = QtCore.pyqtSignal(int,int)
    idle_cb          = QtCore.pyqtSignal()
    render_cb        = QtCore.pyqtSignal()
    renderbox_cb     = QtCore.pyqtSignal(object, list)

    mouse_move_cb    = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_press_cb   = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_release_cb = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_wheel_cb   = QtCore.pyqtSignal( QtGui.QWheelEvent, object, list)

    key_press_cb     = QtCore.pyqtSignal( QtGui.QKeyEvent )
    key_release_cb   = QtCore.pyqtSignal( QtGui.QKeyEvent )

    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        self.parent = parent
        super(MapWidget, self).__init__(parent)
        self.setMouseTracking(True)

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.gear1 = 0
        self.gear1Rot = 0
        self.boxinit = False
    
        
        self.lastPos = QtCore.QPoint()

        # timer = QTimer(self)
        # timer.timeout.connect(self.advanceGears)
        # timer.start(20)

    def setXRotation(self, angle):
        #self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        #self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        #self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def mouseMoveEvent( self, event ):
        #self.mouse_move_cb.emit( evt )
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()


        if event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(dx/20)
            self.setYRotation(dy/20)

        self.lastPos = event.pos()

    def mouseWheelEvent(self, evt):
        self.mouse_wheel_cb.emit(evt)

        
    def mousePressEvent( self, event ):
        #self.mouse_press_cb.emit( evt )
        self.lastPos = event.pos()

    def mouseReleaseEvent( self, evt ):
        self.mouse_release_cb.emit( evt )

    def keyPressEvent( self, evt ):
        self.key_press_cb.emit(evt)

    def keyReleaseEvent( self, evt ):
        self.key_release_cb.emit(evt)

    def initializeGL(self):
        #self.initialize_cb.emit()
        print('InitializeGL')
        # lightPos = (5.0, 5.0, 10.0, 1.0)
        # reflectance1 = (0.8, 0.1, 0.0, 1.0)
        # reflectance2 = (0.0, 0.8, 0.2, 1.0)
        # reflectance3 = (0.2, 0.2, 1.0, 1.0)

        # glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glEnable(GL_DEPTH_TEST)

        # glMatrixMode( GL_PROJECTION ) # not sure
        # glLoadIdentity() # not sure
        # gluPerspective( 45.0, WIDGET_ASPECT, 0.1, 50.0 ) # FOV, aspect ratio, clipping plane
        # glTranslate(0.0, 0.0, -15) # move camera

        #self.gear1 = self.makeGear(reflectance1, 1.0, 4.0, 1.0, 0.7, 20)

        square_vertices = (
            ( 1, -1, -1),
            ( 1,  1, -1),
            (-1,  1, -1),
            (-1, -1, -1)
        )

        square_edges = edges = (
            (0,1),
            (0,3),
            (2,1),
            (2,3)
        )

        self.box1 = self.makeBox(square_vertices, square_edges)

        #gl.glEnable(gl.GL_NORMALIZE)
        #gl.glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, width, height):
        print('resizeGL')
        # if height == 0: height = 1
        # self.resize_cb.emit(width,height)
        side = min(width, height)
        if side < 0:
            return

        #glViewport((width - side) // 2, (height - side) // 2, side, side)
        glViewport(0, 0, 920, 240)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def paintGL(self):
        print('Paint')
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #glPushMatrix()
        # glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        # glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        # glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
        glTranslated(self.xRot, 0.0, 0.0)
        glTranslated( 0.0, -self.yRot, 0.0)
        glTranslated( 0.0, 0.0, self.zRot)

        #self.drawBox(self.box1, -3.0, -2.0, 0.0)
        if not self.boxinit:
            self.drawBox(self.box1, 0.0, 0.0, 0.0)

        #glTranslated(1.0, 0.0, 0.0)

        #glPopMatrix()
        #self.render_cb.emit()

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def normalizeAngle(self, angle):
        # while (angle < 0):
        #     angle += 360 * 16

        # while (angle > 360 * 16):
        #     angle -= 360 * 16
        pass

    def makeBox(self, vertices, edges):
        print('Make box')
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)

        glBegin(GL_POLYGON)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        glEndList()
        
        return list

    def drawBox(self, box, dx, dy, dz):
        print('drawbox')
        gl.glPushMatrix()
        #gl.glTranslated(dx, dy, dz)
        #gl.glRotated(angle, 0.0, 0.0, 1.0)
        gl.glCallList(box)
        gl.glPopMatrix()



import sys

from OpenGL.GL import *
from OpenGL.GLU import *

WIDGET_WIDTH = 920
WIDGET_HEIGHT = 240
WIDGET_ASPECT = WIDGET_WIDTH/WIDGET_HEIGHT


def resize( w, h ):
    print('resize')
    WIDGET_WIDTH = w
    WIDGET_HEIGHT = h
    WIDGET_ASPECT = w/h
    glViewport( 0, 0, WIDGET_WIDTH, WIDGET_HEIGHT )

def initialize():
    print('initialize')
    # glEnable(GL_DEPTH_TEST) # not sure
    # glClearColor( 0.7, 0.7, 1.0, 0.0 ) # background color

    glMatrixMode( GL_PROJECTION ) # not sure
    glLoadIdentity() # not sure
    gluPerspective( 45.0, WIDGET_ASPECT, 0.1, 50.0 ) # FOC, aspect ratio, clipping plane
    glTranslate(0.0, 0.0, -15) # move camera
    
    # setup a frame buffer for object detection
    framebuffer = glGenFramebuffers(1)
    glBindFramebuffer(GL_READ_FRAMEBUFFER, framebuffer) # Not doing GL_FRAMEBUFFER since just reading

    # # we'll use a color buffer to make object picking easier
    colorbuffer = glGenRenderbuffers (1)
    glBindRenderbuffer(GL_RENDERBUFFER, colorbuffer)

    # glMatrixMode( GL_MODELVIEW ) # not sure
    # glLoadIdentity() # not sure
    # gluLookAt( 0.0, 2.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 ) # moves the camera?



def box(GLWidget, scene_objs ):
    print('Boxing')
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) # must have, not sure why
    
    for obj in scene_objs:
        glBegin(GL_POLYGON)
        for edge in obj["edges"]:
            for vertex in edge:
                glVertex3fv(obj["vertices"][vertex])
        glEnd()
    GLWidget.update()



    

def mouse_move( evt ):
    pass
    #print('Mouse move {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )
    #mouse_x = evt.x()
    #mouse_y = evt.y()


def mouse_wheel( evt, GLWidget, scene_objs ):
    print('Whee!')
    if evt.angleDelta().y() < 0:
        glTranslate(0.0, 0.0, -1)
    else:
        glTranslate(0.0, 0.0, 1)
    GLWidget.renderbox_cb.emit(GLWidget, scene_objs)


def mouse_press( evt ):
    print('Mouse press {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )

def mouse_release( evt ):
    print('Mouse release {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )

def key_press( evt ):
    print('Key press {}'.format(evt.key()) )

def key_release( evt ):
    print('Key release {}'.format(evt.key()) )
