import cv2													#Лабораторна робота №7
import numpy as np											#Побудувати 3D модель (голови)
import math													#зафарбовану з освітленням
import random												#виконала Андрусів Соломія


def get_color():                                           #функція повертає основний колір фігури
    return np.array([92, 78, 160])                         #(без освітлення)

def get_face_color(face, vector):                          #функція повертає колір трикутника з освітленням
    object_color =get_color()                              #основний колір
    light_color=np.array([1, 1, 1])                        #колір світла

    x1, y1, z1 = vector[face[0]]                           #координати трьох точок трикутника,
    x2, y2, z2 = vector[face[1]]                           #який зафарбовуємо
    x3, y3, z3 = vector[face[2]]

    xn=(y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)       #обчислення координат вектора нормалі
    yn=(z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)       #до площини трикутника
    zn=(x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    normal = np.array([xn, yn, zn])                        #вектор нормалі
    normal = normal / np.linalg.norm(normal)               #нормалізуємо вектор нормалі

    # Ambient
    ambient_strength = 0.3;                                #коефіцієнт фонового освітлення
    ambient = ambient_strength * light_color;              #фонова складова освітлення


    #Diffuse
    light_pos=np.array([1.2, 1.0, 2.0])                    #позиція світла
    light_dir = light_pos - normal                         #вектор напряму світла
    light_dir = light_dir / np.linalg.norm(light_dir)      #(нормалізований)

    diff = max(np.dot(normal, light_dir), 0.0)             #коефіцієнт розсіяного освітлення
    diffuse = diff * light_color                           #розсіяна складова освітлення


    # Specular
    specular_strength = 0.3                                #коефіцієнт дзеркальної складової
    view_pos=[0.1, 0.3, 1]
    reff_light_vect = normal * (2 * np.dot(normal, view_pos) / np.dot(normal, normal)) - view_pos
    reff_comp = max(np.dot(view_pos, reff_light_vect), 0.0)
    reff_comp = pow(reff_comp, 13)
    specular = reff_comp*specular_strength                 #дзеркальна складова освітлення

    result = (ambient + diffuse +specular) * object_color  #результуючий колір трикутника

    return result


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

    for i in range(len(face)):                              # малювання трикутників та відображення голови
                                                            # задопомогою cv2
        f = face[i]
        c = [0, 0, 0]
        for j in range(3):
            world_coords = vector[f[j]]
            c[j] = int((world_coords[0] + 1) * width/2), \
                               int(abs(height - (world_coords[1] + 1) * height/2))

        color= get_face_color(f,vector)                     # викликається функція що обчислює колір з освітленням
        cv2.drawContours(img, [np.array([c[0], c[1], c[2]])], 0,color , -1)
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

                                                            #в наступних рядках @ - операція множення матриць
    for i, c in enumerate(vector):
        vector[i] = rx @ c
    for i, c in enumerate(vector):
        vector[i] = ry @ c
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
