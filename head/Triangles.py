import cv2
import numpy as np
import random

#Реалізувати функцію зафарбовування трикутника. Використати власну функцію для відображення моделі.

def read_model(filename):

    #read necessary coordinates from object file
    vector= []
    face = []
    model = open(filename, "r")
    content = model.readlines()

    for line in content:
        if line[0] == 'v' and line[1] == ' ':
            v = line.split(" ")
            vector.append([float(v[1]), float(v[2]), float(v[3])])
        elif line[0] == 'f' and line[1] == ' ':
            f = line.split(" ")
            f1 = f[1].split('/')[0]
            f2 = f[2].split('/')[0]
            f3 = f[3].split('/')[0]
            face.append([int(f1)-1, int(f2)-1, int(f3)-1])
    return vector, face


def sort(face, vector):
    return sorted(face, key=lambda i: vector[int(i[0])][2], reverse=False)

def draw_triangle(x0,y0,x1,y1,x2,y2,img,color):
    if y0>y2 :
        x0, x2=x2, x0
        y0, y2=y2, y0

    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y1 > y2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    cv2.line(img, (x0, y0), (x1, y1), color)
    cv2.line(img, (x1, y1), (x2, y2), color)
    cv2.line(img, (x2, y2), (x0, y0), color)
    return img


def fill_triangle(x1, y1, x2, y2,x3, y3, img, color):
    #sort points so that y0<y1<y2
    if (y2 < y1):
            y1,y2=y2,y1
            x1,x2=x2,x1

    if (y3 < y1):
            y1,y3=y3,y1
            x1,x3=x3,x1

    if (y2 > y3):
            y3,y2=y2,y3
            x3,x2=x2,x3

    #find x coordinates of lines
    if (y3 != y1):
            dx13 = (x3 - x1)/(y3 - y1)
    else:
            dx13 = 0

    if (y2 != y1) :
            dx12 = (x2 - x1)/(y2 - y1)
    else:
            dx12 = 0

    if (y3 != y2) :
            dx23 = (x3 - x2)/(y3 - y2)
    else:
            dx23 = 0

    wx1 = x1
    wx2 = wx1

    _dx13 = dx13

    #sort x coordinates so that lines will be [dx13,dx12] and [dx13,dx23]
    if (dx13 > dx12):
            dx12,dx13=dx13,dx12

    if (_dx13 < dx23):
        _dx13, dx23=dx23,_dx13

    #color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for i in range (y1,y2):
         #color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
         for j in range (int(wx1),int(wx2)+1):
                img[i,j]=color

         wx1 += dx13
         wx2 += dx12

    if (y1 == y2):
        wx1 = x1
        wx2 = x2


    #color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    for  y in range(y2,y3+1):
            #color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for x in range (int(wx1),int(wx2)+1):
                  if(y==400):
                      img[y-1,x]=color
                  else:
                      img[y,x]=color

            wx1 += _dx13
            wx2 += dx23


    return img


def main():
    color = (11,255,57)
    width = 400
    height = 400

    img0 = np.zeros((width, height, 3), dtype=np.uint8)
    cv2.imshow('Result0', fill_triangle(50,50,345,18,120,298,img0,color))

    img = np.zeros((width, height, 3), dtype=np.uint8)

    vector, face = read_model("african_head.obj")
    face = sort(face, vector)
    for i in range(len(face)):
        f = face[i]
        c = [0, 0, 0]
        for j in range(3):
            world_coords = vector[f[j]]
            c[j] = int((world_coords[0] + 1) * width/2), \
                               int(abs(height - (world_coords[1] + 1) * height/2))

        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        res= fill_triangle(c[0][0], c[0][1], c[1][0], c[1][1], c[2][0], c[2][1], img, color)

    cv2.imshow('Result', res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
