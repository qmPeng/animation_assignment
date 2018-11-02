
from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
import wx


class MyFrame(wx.Frame):

    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title = "wx frame", size = self.size, style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.panel = MyPanel(self)


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.canvas = OpenGLCanves(self)
        self.x_slider = wx.Slider(self, -1, pos = (1130, 180), size = (40,150), style = wx.SL_VERTICAL|wx.SL_AUTOTICKS, value = 0, minValue = -5, maxValue = 5)


class OpenGLCanves(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.initialized = False
        self.size = (1024, 720)
        self.aspect_ratio = 1
        self.angle = 0.0
        glcanvas.GLCanvas.__init__(self, parent, -1, size = self.size)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.Bind(wx.EVT_PAINT, self.OnDraw)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.InitGL()

    def InitGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.aspect_ratio = float(self.size[0] / self.size[1])
        gluPerspective(60, self.aspect_ratio, 0.1, 100.0)
        glViewport(0, 0, self.size[0], self.size[1])

    def OnIdle(self, event):
        self.angle += 1.0
        self.Refresh()

    def OnDraw(self, event):
        if not self.initialized:
            self.InitGL()
            self.initialized = True
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -2)
        glRotate(self.angle, 0, 0, 1)

        glBegin(GL_QUADS)
        glVertex3f(0.5, 0.5, 0)
        glVertex3f(-0.5, 0.5, 0)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f(0.5, -0.5, 0)
        glEnd()
        self.SwapBuffers()


def main():

    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()