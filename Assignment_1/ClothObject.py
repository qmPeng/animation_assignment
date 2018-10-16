import numpy as np
import math
from OpenGL.GL import *


class ClothObject:
    def __init__(self, sizeX, sizeZ, nW, nH):
        self.dx = sizeX / (nW - 1)
        self.dz = sizeZ / (nH - 1)
        self.dDiag = math.sqrt(self.dx**2.0 + self.dz**2.0)

        self.nW, self.nH = nW, nH
        self.clothSize = (sizeX, sizeZ)

        self.verts = np.zeros(shape=(nW * nH, 3))
        self.velocity = np.zeros(shape=(nW * nH, 3))

        self.springs = np.zeros(shape=((nW - 1) * nH + (nH - 1) * nW + (nW - 1) * (nH - 1) * 2, 2), dtype=np.int32)

        self.l0 = np.zeros(shape=(len(self.springs),))

        self.numXSprings = (self.nW - 1) * self.nH
        self.numZSprings = (self.nH - 1) * self.nW
        self.numDiagonalSprings = (self.nW - 1) * (self.nH - 1)

        self.resetMassSpring()

    def resetMassSpring(self):

        for i in range(0, self.nW * self.nH):
            self.verts[i] = [(i % self.nW) * self.dx, 1, (int(i / self.nW)) * self.dz]
            self.velocity[i] = [0, 0, 0]

        for i in range(0, self.numXSprings):
            row = int(i / (self.nW - 1))
            col = i % (self.nW - 1)
            self.springs[i] = [row * self.nW + col, row * self.nW + col + 1]
            self.l0[i] = self.dx

        for i in range(0, self.numZSprings):
            row = int(i / (self.nW))
            col = i % (self.nW)
            self.springs[self.numXSprings + i] = [row * self.nW + col, (row + 1) * self.nW + col]
            self.l0[(self.nW - 1) * self.nH + i] = self.dz

        for i in range(0, self.numDiagonalSprings):
            row = int(i / (self.nW - 1))
            col = i % (self.nW - 1)
            self.springs[self.numXSprings + self.numZSprings + 2 * i] = [row * self.nW + col, (row + 1) * self.nW + col + 1]
            self.l0[self.numXSprings + self.numZSprings + 2 * i] = self.dDiag

            self.springs[self.numXSprings + self.numZSprings + 2 * i + 1] = [row * self.nW + col + 1, (row + 1) * self.nW + col]
            self.l0[self.numXSprings + self.numZSprings + 2 * i + 1] = self.dDiag

    def drawSpring(self):
        glColor3f(1, 1, 1)

        glBegin(GL_LINES)
        for i in range(0, len(self.springs)):
            idx0 = self.springs[i][0]
            idx1 = self.springs[i][1]
            loc0 = self.verts[idx0]
            loc1 = self.verts[idx1]
            glVertex3fv(loc0)
            glVertex3fv(loc1)
        glEnd()

    def update(self, dt):
        numParticles = self.nW * self.nH
        gravity = np.array([0.0, -9.8, 0.0])

        for i in range(0, numParticles):
            self.velocity[i] = self.velocity[i] + gravity * dt
            self.verts[i] = self.verts[i] + self.velocity[i] * dt
