import copy
from PIL import Image
import re
import numpy as np
import math

width = 800  # Ширина картинки
height = width  # Высота картинки


class Screen(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = Image.new('RGB', (width, height), 'black')
        self.canvas = self.img.load()
        self.z_buffer = [[0] * width for i in range(height)]

    def point(self, *coords):
        return TexturePoint(self, *coords)

    @staticmethod
    def triangle(coords, texture):
        a, b, c = sorted(coords, key=lambda p: p.y)
        p1, p2 = a.copy(), a.copy()
        height = c.y - a.y
        delta_x2 = float(c.x - a.x) / height
        deltas = lambda i, j, divider: [float(i.z-j.z)/divider, float(i.u-j.u)/divider, float(i.v-j.v)/divider]
        delta_z2, delta_u2, delta_v2 = deltas(c, a, height)
        for p in (b, c):
            height = (p.y - p1.y) or 1
            delta_x1 = float(p.x - p1.x) / height
            delta_z1, delta_u1, delta_v1 = deltas(p, p1, height)
            while p1.y < p.y:
                p3, p4 = (p2.copy(), p1) if p1.x > p2.x else (p1.copy(), p2)
                delta_z3, delta_u3, delta_v3 = deltas(p4, p3, (p4.x - p3.x) or 1)
                while p3.x < p4.x:
                    p3.show(texture[p3.u, p3.v])
                    p3.add(x=1, z=delta_z3, u=delta_u3, v=delta_v3)
                p1.add(x=delta_x1, y=1, z=delta_z1, u=delta_u1, v=delta_v1)
                p2.add(x=delta_x2, y=1, z=delta_z2, u=delta_u2, v=delta_v2)
            p1 = b.copy()


class Point(object):
    def __init__(self, screen, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.screen = screen

    def show(self, color=None):
        screen = self.screen
        x = int(self.x)
        y = int(self.y)
        if self.z <= screen.z_buffer[y][x]:
            return
        screen.z_buffer[y][x] = self.z
        screen.canvas[x, screen.height-y] = color or (255, 255, 255)

    def copy(self):
        return copy.copy(self)


class TexturePoint(Point):
    def __init__(self, screen, x, y, z, u, v):
        super(TexturePoint, self).__init__(screen, x, y, z)
        self.u = u
        self.v = v

    def add(self, x=0, y=0, z=0, u=0, v=0):
        self.x += x
        self.y += y
        self.z += z
        self.u += u
        self.v += v

def read_model(model,  texture_img):
    middle_x = int(width / 2)
    middle_y = int(height / 2)

    lines = model.read()
    vector = []
    textures = []
    face = []
    for line in lines.split('\n'):
        try:
            v, x, y, z = re.split('\s+', line)
        except ValueError:
            continue
        if v == 'v':
            x = int((float(x) + 1) * middle_x)
            y = int((float(y) + 1) * middle_y)
            z = float(z) + 1
            vector.append([x, y, z])
        if v == 'vt':
            u = float(x) * texture_img.width
            v = (1 - float(y)) * texture_img.height
            textures.append([u, v])
        if v == 'f':
            f = line.split(" ")
            f1 = f[1].split('/')[0]
            f2 = f[2].split('/')[0]
            f3 = f[3].split('/')[0]
            face.append([int(f1)-1, int(f2)-1, int(f3)-1,
                        int(f[1].split('/')[1])-1, int(f[2].split('/')[1])-1, int(f[3].split('/')[1])-1])


    #print(textures[0])
    return face, vector, textures

def show_face(face, vector, textures,texture_img):
    texture_model = texture_img.load()

    screen = Screen(width, height)
    for i in range (len(face)):
        f=face[i]
        tr_points = []
        for j in range(3):
            print(vector[f[j]])
            print(textures[f[j+3]])
            params=[vector[f[j]][0],vector[f[j]][1],vector[f[j]][2],textures[f[j+3]][0],textures[f[j+3]][1]]

            tr_points.append(screen.point(*params))
        screen.triangle(tr_points,texture_model)

    screen.img.show()



def rotate(vector,textures, x, y, z):
    print("rotate")
    sinx, siny, sinz = math.sin(x), math.sin(y),math.sin(z)
    cosx, cosy, cosz = math.cos(x),math.cos(y),math.cos(x)

    rx = np.array([[1, 0, 0], [0, cosx , -sinx], [0, sinx, cosx]])
    ry = np.array([[cosy, 0, siny], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[cosz, -sinz, 0], [sinz, cosz, 0], [0, 0, 1]])
    for i, c in enumerate(vector):
        vector[i] = rx @ c
    for i, c in enumerate(vector):
        vector[i] = ry @ c
    for i, c in enumerate(vector):
        vector[i] = rz @ c

    return vector

def main():
    texture_img = Image.open('african_head_diffuse.tga')

    model = open('african_head.obj', 'r')
    face, vector, textures = read_model(model,texture_img)
    show_face(face, vector, textures,texture_img)

main()
