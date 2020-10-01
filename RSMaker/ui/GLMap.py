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
    
        
        self.lastPos = QtCore.QPoint()

        # timer = QTimer(self)
        # timer.timeout.connect(self.advanceGears)
        # timer.start(20)

    def setXRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def mouseMoveEvent( self, event ):
        #self.mouse_move_cb.emit( evt )
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

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
        lightPos = (5.0, 5.0, 10.0, 1.0)
        reflectance1 = (0.8, 0.1, 0.0, 1.0)
        reflectance2 = (0.0, 0.8, 0.2, 1.0)
        reflectance3 = (0.2, 0.2, 1.0, 1.0)

        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        self.gear1 = self.makeGear(reflectance1, 1.0, 4.0, 1.0, 0.7, 20)

        gl.glEnable(gl.GL_NORMALIZE)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, width, height):
        # if height == 0: height = 1
        # self.resize_cb.emit(width,height)
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def paintGL(self):
        print('Paint')
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
        #self.box
        self.drawGear(self.gear1, -3.0, -2.0, 0.0, self.gear1Rot / 16.0)
        # self.drawGear(self.gear2, +3.1, -2.0, 0.0,
        #         -2.0 * (self.gear1Rot / 16.0) - 9.0)

        glRotated(+90.0, 1.0, 0.0, 0.0)
        # self.drawGear(self.gear3, -3.1, -1.8, -2.2,
        #         +2.0 * (self.gear1Rot / 16.0) - 2.0)

        glPopMatrix()
        #self.render_cb.emit()

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16

    def makeGear(self, reflectance, innerRadius, outerRadius, thickness, toothSize, toothCount):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,
                reflectance)

        r0 = innerRadius
        r1 = outerRadius - toothSize / 2.0
        r2 = outerRadius + toothSize / 2.0
        delta = (2.0 * math.pi / toothCount) / 4.0
        z = thickness / 2.0

        glShadeModel(GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            glNormal3d(0.0, 0.0, sign)

            glBegin(GL_QUAD_STRIP)

            for j in range(toothCount+1):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

            glBegin(GL_QUADS)

            for j in range(toothCount):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r2 * math.cos(angle + delta), r2 * math.sin(angle + delta), sign * z)
                glVertex3d(r2 * math.cos(angle + 2 * delta), r2 * math.sin(angle + 2 * delta), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount):
            for j in range(2):
                angle = 2.0 * math.pi * (i + (j / 2.0)) / toothCount
                s1 = r1
                s2 = r2

                if j == 1:
                    s1, s2 = s2, s1

                glNormal3d(math.cos(angle), math.sin(angle), 0.0)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), +z)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), -z)

                glNormal3d(s2 * math.sin(angle + delta) - s1 * math.sin(angle), s1 * math.cos(angle) - s2 * math.cos(angle + delta), 0.0)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), +z)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), -z)

        glVertex3d(r1, 0.0, +z)
        glVertex3d(r1, 0.0, -z)
        glEnd()

        glShadeModel(GL_SMOOTH)

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount+1):
            angle = i * 2.0 * math.pi / toothCount
            glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), +z)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), -z)

        glEnd()

        glEndList()

        return list

    def drawGear(self, gear, dx, dy, dz, angle):
        gl.glPushMatrix()
        gl.glTranslated(dx, dy, dz)
        gl.glRotated(angle, 0.0, 0.0, 1.0)
        gl.glCallList(gear)
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

def makeBox(self, vertices, edges):
    list = glGenLists(1)
    glNewList(list, GL_COMPILE)

    glBegin(GL_POLYGON)
    for edge in edges:
        for vertex in vertices:
            glVertex3fv(vertices[vertex])
    glEnd()

    glEndList()
    
    return list

    

def mouse_move( evt ):
    pass
    #print('Mouse move {}: [{},{}]'.format(evt.button(),evt.x(),evt.y()) )
    #mouse_x = evt.x()
    #mouse_y = evt.y()


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

def drawBox(self, box, dx, dy, dz, angle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        glCallList(box)
        glPopMatrix()
    
