import math
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
# references
# http://jamesgregson.ca/pyqt5-pyopengl-example.html
# https://github.com/baoboa/pyqt5/blob/master/examples/opengl/grabber.py


class MapWidget(QtOpenGL.QGLWidget):

    xTranslationChanged = QtCore.pyqtSignal(int)
    yTranslationChanged = QtCore.pyqtSignal(int)
    zTranslationChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        self.parent = parent
        super(MapWidget, self).__init__(parent)
        self.setMouseTracking(True)

        self.xOff = 0
        self.yOff = 0
        self.zOff = 0 

        self.clipNear = 5.0
        self.clipFar = 60.0
        self.zoomStep = 3.0
        self.xPanMax = 30
        self.yPanMax = 6

        self.boxinit = False
        
        self.lastPos = QtCore.QPoint()
    
    def setXTranslation(self, offset):
        self.xOff = offset
        self.xTranslationChanged.emit(offset)
        self.update()

    def setYTranslation(self, offset):
        self.yOff = offset
        self.yTranslationChanged.emit(offset)
        self.update()

    def setZTranslation(self, offset):
        self.zOff = offset
        self.zTranslationChanged.emit(offset)
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            matModelView = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
            matProjection = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
            viewPort = gl.glGetIntegerv(gl.GL_VIEWPORT)
            mx = event.x()
            my = event.y()
            print("Mouse Coords:", mx, my)
            
            # Should return the normalize mouse start and end coords in worldspace
            # not exactly following, prolly just should do the matrix mult manually
            psx, psy, psz = glu.gluUnProject(mx, my, 0.0, matModelView, matProjection, viewPort)
            pex, pey, pez = glu.gluUnProject(mx, my, self.clipFar, matModelView, matProjection, viewPort)

            # Gets the correct color for box 1 without zoom
            # I think I need to re-draw vs translate the view port?
            read = gl.glReadPixels(mx, my, 1, 1, gl.GL_RGB, gl.GL_FLOAT )
            r = read[0][0][0]
            g = read[1][0][0]
            b = read[2][0][0]
            print("RGB:",r,g,b)


    def mouseMoveEvent( self, event ):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
       
        # normalize speed based on current z position, 13 @ 40z seems good
        model = gl.glGetDoublev( gl.GL_MODELVIEW_MATRIX )
        z_curr = -model[3][2]
        normalizer = (40/z_curr) *13

        # get x and y for panning limitations
        x_curr = model[3][0]
        y_curr = model[3][1]

        if event.buttons() & QtCore.Qt.RightButton:
            # limit x panning (doesn't scale currently)
            if x_curr > self.xPanMax and dx >0:
                dx = 0
            elif x_curr < -self.xPanMax and dx <0:
                dx = 0
            
            # limit y panning (doesn't scale currently)
            if y_curr > self.yPanMax and dy <0:
                dy = 0
            elif y_curr < -self.yPanMax and dy >0:
                dy = 0
            
            self.setXTranslation(dx/normalizer)
            self.setYTranslation(dy/normalizer)

        self.lastPos = event.pos()
    
    def mouseWheelEvent(self, event):
                
        # get current z position
        model = gl.glGetDoublev( gl.GL_MODELVIEW_MATRIX )
        z_curr = -model[3][2]

        # limit zoom based on clipping plan
        if event.angleDelta().y() < 0:
            if z_curr > self.clipFar - self.zoomStep:
                pass
            else:
                self.setZTranslation(-self.zoomStep)
        else:
            if z_curr < self.clipNear + self.zoomStep:
                pass
            else:
                self.setZTranslation(self.zoomStep)


    def initializeGL(self):
        print('InitializeGL')

        square_vertices = (
            ( 1, -1, -1),
            ( 1,  1, -1),
            (-1,  1, -1),
            (-1, -1, -1)
        )

        square2_vertices = (
            ( 3,  1, -1),
            ( 3,  3, -1),
            ( 1,  3, -1),
            ( 1,  1, -1)
        )


        square_edges = edges = (
            (0,1),
            (0,3),
            (2,1),
            (2,3)
        )

        self.box1 = self.makeBox(square_vertices, square_edges)
        self.box2 = self.makeBox(square2_vertices, square_edges)

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        
        aspect = width/height
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glFrustum(-aspect, +aspect, -1.0, 1.0, self.clipNear, self.clipFar)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -40.0)
        
        

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        #model = gl.glGetDoublev( gl.GL_MODELVIEW_MATRIX )
        #print("model Z value:", str(model[3][2]))

        # model = gl.glGetDoublev( gl.GL_MODELVIEW_MATRIX )
        # print("{:.2f}".format(model[3][2]))
        # print('#### MODEL MATRIX ####')
        # print("0\t1\t2\t3")
        # for p in model: 
        #     print(
        #             "{:.2f}".format(p[0]),
        #             "{:.2f}".format(p[1]),
        #             "{:.2f}".format(p[2]),
        #             "{:.2f}".format(p[3]),
        #             sep='\t'
        #         )

        # proj = gl.glGetDoublev( gl.GL_PROJECTION_MATRIX )
        # print('#### PROJECTION MATRIX ####')
        # print("0\t1\t2\3")
        # for p in proj:
        #     print(
        #             "{:.2f}".format(p[0]),
        #             "{:.2f}".format(p[1]),
        #             "{:.2f}".format(p[2]),
        #             "{:.2f}".format(p[3]),
        #             sep='\t'
        #         )

        gl.glTranslated(self.xOff, 0.0, 0.0)
        gl.glTranslated( 0.0, -self.yOff, 0.0)
        gl.glTranslated( 0.0, 0.0, self.zOff)
        
        # reset zOff as to not zoom if wasn't triggered
        self.zOff = 0

        if not self.boxinit:
            self.drawBox(self.box1)
            self.drawBox(self.box2)

    def xTranslation(self):
        return self.xOff

    def yTranslation(self):
        return self.yOff

    def zTranslation(self):
        return self.zOff

    def normalizeOffset(self, offset):
        # plan on using this to offset x/y mouse movement
        pass

    def makeBox(self, vertices, edges):
        print('Make box')
        list = gl.glGenLists(1)
        gl.glNewList(list, gl.GL_COMPILE)

        gl.glBegin(gl.GL_POLYGON)
        for edge in edges:
            for vertex in edge:
                gl.glVertex3fv(vertices[vertex])
        gl.glEnd()

        gl.glEndList()
        
        return list

    def drawBox(self, box):
        gl.glPushMatrix()
        gl.glCallList(box)
        gl.glPopMatrix()