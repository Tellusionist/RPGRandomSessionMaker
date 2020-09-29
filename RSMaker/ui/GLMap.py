
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
# source http://jamesgregson.ca/pyqt5-pyopengl-example.html

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
        print('Paint')
        #self.render_cb.emit()


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

    # glMatrixMode( GL_MODELVIEW ) # not sure
    # glLoadIdentity() # not sure
    # gluLookAt( 0.0, 2.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 ) # moves the camera?

def render():
    print('render')
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective( 45.0, WIDGET_ASPECT, 0.1, 10.0 )

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

def box(GLWidget, scene_objs ):
    print('Boxing')
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT ) # must have, not sure why
    
    glBegin(GL_LINES)
    for obj in scene_objs:
        for edge in obj["edges"]:
            for vertex in edge:
                glVertex3fv(obj["vertices"][vertex])
    glEnd()
    GLWidget.update()


def mouse_move( evt ):
    pass
    #print('Mouse move {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )


def mouse_wheel( evt, GLWidget, scene_objs ):
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
