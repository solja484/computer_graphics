import cv2													#Лабораторна робота №6
import numpy as np											#Побудувати 3D об'єкт (куля, еліпсоїд, тор)
import math													#з обертанням, освітленням
            												#виконала Андрусів Соломія


def make_ellips(a,b,c):                                    #функція, що формує об'єкти vector та face
                                                           #аналогічні до тих що викор. при малюванні голови
    vectors = []                                           #для 3D фігури еліпса

    circles = 0                                            #кількість кіл
    segments = 0                                           #кількість сегментів на колі
    t = 0
    step=math.pi/10                                        #крок(буквально - ширина та висота сегменту еліпса)

    while t < 2 * math.pi:                                 #кут тета
        f =0
        segments = 0
        while f <= (math.pi):                              #кут фі
            vectors.append([a * math.sin(f) * math.cos(t),
                            b * math.sin(f) * math.sin(t), #обчислення координат точок
                            c * math.cos(f)])              #задопомогою параметричного рівняння еліпса
            f += step
            segments += 1
        t += step
        circles += 1

    faces=make_face(circles,segments)                      #формування об'єкту face

    return faces, vectors


def make_face(circles, segments):                          #формування об'єкту face
    faces=[]                                               #зв'язування точок по 3 у трикутники
    for i in range(circles - 1):
        for j in range(segments - 1):                      #дві точки з поточного (j-го) сегменту кола
                                                           #та одна з наступного (j+1-го)
            a = [i * segments + j,                         #і-того кола
                 (i + 1) * segments + j,
                 i * segments + (j + 1)]
                                                           # і навпаки
            b = [(i + 1) * segments + j + 1,               # оскільки всі точки в масиві векторів
                 i * segments + (j + 1),                   # додавались по порядку від 0го кола
                 (i + 1) * segments + j]                   # до номерів у face додаємо координату і помножену
                                                           # на номер поточного кола

            faces.append(a)
            faces.append(b)

    i = circles - 1                                        #те ж саме для останнього "шва", що з'єднує
    for j in range(segments - 1):                          #0ий сегмент з останнім
        a = [i * segments + j, j, i * segments + j + 1]
        b = [j + 1, i * segments + j + 1, j]
        faces.append(a)
        faces.append(b)
    return faces

def make_sphere(width, R):                                  #функція, що формує об'єкти vector та face
    vectors = []                                            #для 3D фігури сфери

    circles = 0                                             #кількість кіл
    segments = 0                                            #кількість сегментів на колі
    t = 0
    step=math.pi/10                                         #крок(буквально - ширина та висота сегменту сфери)

    while t < 2 * math.pi:                                  #кут тета
        f = 0
        segments = 0
        while f <=  math.pi:                                #кут фі
            x = width + R * math.sin(f) * math.cos(t)       #обчислення координат точок
            y = width + R * math.sin(f) * math.sin(t)       #задопомогою параметричного рівняння еліпса
            z = width + R * math.cos(f)
            vectors.append([x, y, z])
            f += step
            segments += 1
        t += step
        circles += 1

    faces=make_face(circles,segments)                       #формування об'єкту face

    return faces, vectors


def make_torus(R, r):                                       #функція, що формує об'єкти vector та face
    vectors = []                                            #для 3D фігури сфери

    parts = 0                                               #к-сть частин з довжиною step, на які можна "розрізати" тор
    segments = 0                                            #к-сть сегментів, на які ділиться частина тора
    step=math.pi/10                                         #крок(буквально - ширина та висота сегменту)
    t = 0
    while t < 2 * math.pi:                                  #кут тета
        f = -1.0*math.pi
        segments = 0
        while f < (math.pi):                                #кут фі
            x = (R + r*math.cos(f))*math.cos(t)             #обчислення координат точок
            y = (R + r*math.cos(f))*math.sin(t)             #задопомогою параметричного рівняння тора
            z = r * math.sin(f)                             #R-відстань від цетра до зовнішнього краю тора
            vectors.append([x, y, z])                       #r - "товщина бублика", радіус заповненої частини тора
            f += step
            segments += 1
        t += step
        parts += 1

    faces=make_face(parts,segments)                         #формування об'єкту face

    return faces, vectors


def sort(faces, vector):                                     #сортування відносно z-координати
    return sorted(faces, key=lambda i: vector[int(i[0])][2], reverse=True)


def get_color():                                           #функція повертає основний колір фігури
    return np.array([128, 56, 98])                         #(без освітлення)


def draw_model(vector, faces, width, height):              #малювання фігури трикутниками
    img=np.zeros((width, height, 3), dtype=np.uint8)       #з використанням функції з cv2 drawContours

    faces = sort(faces, vector)                            #сортування відносно z-координати

    for i in range(len(faces)):                            # малювання трикутників та відображення голови
        f = faces[i]
        c = [0, 0, 0]
        for j in range(3):
            world_coords = vector[f[j]]
            c[j] = int(world_coords[0]  + width/2), \
                               int(world_coords[1]  + height/2)

        cv2.drawContours(img, [np.array([c[0], c[1], c[2]])], 0, get_face_color(faces[i],vector), -1)
    cv2.imshow('Result', img)
    cv2.waitKey(1)


def rotate(vector, x, y, z):                                #обертання фігури з використанням матриці
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
    ambient_strength = 0.24;                               #коефіцієнт фонового освітлення
    ambient = ambient_strength * light_color;              #фонова складова освітлення

    #Diffuse
    light_pos=np.array([ -3.5, -2.0,-0.5])                 #позиція світла
    light_dir = light_pos - normal                         #вектор напряму світла
    light_dir = light_dir / np.linalg.norm(light_dir)      #(нормалізований)

    diff = max(np.dot(normal, light_dir), 0.0)             #коефіцієнт розсіяного освітлення
    diffuse = diff * light_color                           #розсіяна складова освітлення


    # Specular
    specular_strength = 0.3                                #коефіцієнт дзеркальної складової
    view_pos=np.array([ 0.1, 0.4,1])

    reff_light_vect = normal*(2*np.dot(normal, view_pos)/np.dot(normal,normal)) - view_pos
    reff_comp = max(np.dot(view_pos, reff_light_vect), 0.0)
    reff_comp = pow(reff_comp, 15)
    specular = reff_comp*specular_strength                  #дзеркальна складова освітлення

    result = (ambient + diffuse +specular) * object_color   #результуючий колір трикутника

    return result


def main():

    width = 400                                             #розмір вікна
    faces, vector = make_torus(100,50)                      #будування фігури тору з заданими параметрами
    #faces, vector = make_sphere(0,150)                     #будування фігури сфери з заданими параметрами
    #faces, vector = make_ellips(100,80,70)                 #будування фігури тору з заданими параметрами
    draw_model(vector, faces, width, width)                 #налювання фігури по заданих координатах
    while True:
       vector = rotate(vector, 0.01, -0.01, 0.01)           #обертання
       draw_model(vector, faces, width, width)              #і малювання по точках з новими координатами

main()
