import cv2													#Лабораторна робота №5
import numpy as np											#Реалізувати функцію 3-D перетворення, з використанням матриці.
import math													#Побудувати 3D модель з обертанням
import random												#виконала Андрусів Соломія



def read_model(filename):                               	#зчитування координат з файлу .obj

    vector= []
    face = []
    model = open(filename, "r")
    content = model.readlines()

    for line in content:
        if line[0] == 'v' and line[1] == ' ':           	#зчитую координати точок
            v = line.split(" ")
            vector.append([float(v[1]), float(v[2]), float(v[3])])
        elif line[0] == 'f' and line[1] == ' ':         	#зчитую елементи з face
            f = line.split(" ")
            f1 = f[1].split('/')[0]                     	#беру тільки номери точок
            f2 = f[2].split('/')[0]                     	#без текстур та нормалей
            f3 = f[3].split('/')[0]
            face.append([int(f1)-1, int(f2)-1, int(f3)-1])
    return vector, face




def show_head(vector,face,width, height):                   #малювання голови трикутниками
    img=np.zeros((width, height, 3), dtype=np.uint8)        # з використанням функції з cv2 drawContours


    face = sort(face, vector)                               #сортування відносно z-координати

    for i in range(len(face)):
        f = face[i]
        c = [0, 0, 0]
        for j in range(3):
            world_coords = vector[f[j]]
            c[j] = int((world_coords[0] + 1) * width/2), \
                               int(abs(height - (world_coords[1] + 1) * height/2))

        color = (0, random.randint(0, 255), 0)              # випадковий зелений колір
                                                            # малювання трикутників та відображення голови
                                                            # задопомогою cv2
        cv2.drawContours(img, [np.array([c[0], c[1], c[2]])], 0, color, -1)
    cv2.imshow('Result', img)
    cv2.waitKey(1)



def sort(face, vector):                                     #сортування відносно z-координати
    return sorted(face, key=lambda i: vector[int(i[0])][2], reverse=False)



def rotate(vector, x, y, z):                                #обертання голови з використанням матриці
                                                            #(реалізується як зміна координат точок)
    sinx, siny, sinz = math.sin(x), math.sin(y),math.sin(z)
    cosx, cosy, cosz = math.cos(x),math.cos(y),math.cos(x)

                                                            #матрицi 3х3 для обертання по трьох різних осях
    rx = np.array([[1, 0, 0], [0, cosx , -sinx], [0, sinx, cosx]])
    ry = np.array([[cosy, 0, siny], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[cosz, -sinz, 0], [sinz, cosz, 0], [0, 0, 1]])

    if x>0:                                                 #в наступних рядках @ - операція множення матриць
        for i, c in enumerate(vector):
            vector[i] = rx @ c
    if y>0:
        for i, c in enumerate(vector):
            vector[i] = ry @ c
    if z>0:
        for i, c in enumerate(vector):
            vector[i] = rz @ c
    return vector


def main():
    width,height = 400, 400                                 #розмір вікна
    vector,face  = read_model('african_head.obj')           #зчитування координат з файлу .obj
    show_head(vector, face, width, height)                  #малювання голови трикутниками
    while True:
        vector = rotate(vector, 0, 0.05, 0)                 #обертання голови
        show_head(vector, face, width, height)              #і малювання по точках з новими координатами


main()
