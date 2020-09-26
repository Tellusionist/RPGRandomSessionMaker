
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL

class MapWidget(QtOpenGL.QGLWidget):

    initialize_cb    = QtCore.pyqtSignal()
    resize_cb        = QtCore.pyqtSignal(int,int)
    idle_cb          = QtCore.pyqtSignal()
    render_cb        = QtCore.pyqtSignal()

    mouse_move_cb    = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_press_cb   = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_release_cb = QtCore.pyqtSignal( QtGui.QMouseEvent )
    mouse_wheel_cb   = QtCore.pyqtSignal( QtGui.QWheelEvent )

    key_press_cb     = QtCore.pyqtSignal( QtGui.QKeyEvent )
    key_release_cb   = QtCore.pyqtSignal( QtGui.QKeyEvent )

    def __init__(self, parent=None):
        self.parent = parent
        super(MapWidget, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent( self, evt ):
        self.mouse_move_cb.emit( evt )

    def mouseWheelEvent(self, evt):
        self.mouse_wheel_cb.emit(evt)

    def mousePressEvent( self, evt ):
        self.mouse_press_cb.emit( evt )

    def mouseReleaseEvent( self, evt ):
        self.mouse_release_cb.emit( evt )

    def keyPressEvent( self, evt ):
        self.key_press_cb.emit(evt)

    def keyReleaseEvent( self, evt ):
        self.key_release_cb.emit(evt)

    def initializeGL(self):
        self.initialize_cb.emit()

    def resizeGL(self, width, height):
        if height == 0: height = 1
        self.resize_cb.emit(width,height)

    def paintGL(self):
        self.render_cb.emit()


import sys

from OpenGL.GL import *
from OpenGL.GLU import *

width = 800
height = 600
aspect = width/height

def resize( w, h ):
    width = w
    height = h
    aspect = w/h
    glViewport( 0, 0, width, height )

def initialize():
    glEnable(GL_DEPTH_TEST)
    glClearColor( 0.7, 0.7, 1.0, 0.0 )

def render():
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective( 45.0, aspect, 0.1, 10.0 )

    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    gluLookAt( 0.0, 2.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 )

    glPointSize(5.0)
    glLineWidth(5.0)
    glBegin(GL_LINES)
    glColor3f(  1.0, 0.0, 0.0 )
    glVertex3f( 1.0, 0.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glColor3f(  0.0, 1.0, 0.0 )
    glVertex3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glColor3f(  0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, 0.0 )
    glEnd()

def mouse_move( evt ):
    pass
    #print('Mouse move {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )


def mouse_wheel( evt ):
    print('Mouse wheel')
    #print('Mouse wheel {}'.format(evt.pixeldelta() ))

def mouse_press( evt ):
    print('Mouse press {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )

def mouse_release( evt ):
    print('Mouse release {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )

def key_press( evt ):
    print('Key press {}'.format(evt.key()) )

def key_release( evt ):
    print('Key release {}'.format(evt.key()) )
