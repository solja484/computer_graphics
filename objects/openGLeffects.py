import pygame as pg                                        #Лабораторна 9
import math                                                #Засобами OpenGL побудувати об'єкт з додатковим ефектом
from OpenGL.GL import *                                    #(туман, тінь або дзеркальне відображення)
from OpenGL.GLU import *                                   #виконала Андрусів Соломія
from pygame.locals import *                                #вибраний ефект - туман

                                                           #Наступні функції, окрім main()
                                                           # такі ж, як у лабораторній 8

def make_ellipse(a,b,c):                                   #функція, що формує об'єкти vector та face
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



def drawFigure(faces, vectors,black):

    glBegin(GL_TRIANGLES)
    for face in faces:
        if black:
            glColor3fv([0, 0, 0])
        else:
            glColor3fv([face[0]%25/10, 1, 1.7])
        for vert in face:
            glVertex3fv(vectors[vert])

    glEnd()

def drawFigure(faces, vectors,black):                      #функція приймає на всіх об'єкти face та vector
                                                           #та малює фігури трикутниками використовуючи
    glBegin(GL_TRIANGLES)                                  #вбудовану функцію openGL
    for face in faces:
        if black:
            glColor3fv([0, 0, 0])
        else:
            glColor3fv([face[0]%25/10, 1, 1.7])            # колір фігури псевдовипадковий
        for vert in face:
            glVertex3fv(vectors[vert])                     #додаємо координати вершини
    glEnd()



def main():
    width=800                                              #розмір вікна
    height=500

    pg.init()                                              #для відображення фігур використовуєтьс
    display = (width, height)                              #фреймворк pygame
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)       #встановлюємо подвійну буферизацію
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)                                #буфер глибини для z-координати
    glEnable(GL_COLOR_MATERIAL)                            #включили колір
    glEnable(GL_LIGHTING)                                  #включили освітлення

    ambient=0.2                                            #коефіцієнт фонового освітлення
    glEnable(GL_LIGHT1)                                    #вибираємо світловий потік
    glLightfv(GL_LIGHT1,GL_AMBIENT,[ambient, ambient, ambient, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.05, 0.05, 0.05, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0, 1, 0, 1])        #встановлюємо значення для трьох світлових компонент

    glEnable(GL_FOG)                                       #включаємо туман
    glFogfv(GL_FOG_MODE,GL_EXP)                            # спосіб поширення туману в глибину - експоненційний
    glFogfv(GL_FOG_DENSITY,0.8)                            # щільність туману
    glFogfv(GL_FOG_COLOR,[0.3,0.3,0.3,1])                  #встан. туману світло-сірий колір

    a1, a2 = make_torus(0.3,0.1)                           #тор 1
    rotation1 = 0
    t1,t2=make_torus(0.3,0.1)                              #тор 2, аналогічний по розміру
    rotation2= 0
    c1,c2=make_ellipse(1,1,1)                              #сфера 1
    rotation3=0
    c3,c4=make_ellipse(10,10,10)                           #сфера 2


    while True:                                            #цикл для постійного обертання фігур
        for event in pg.event.get():
            if event.type == pg.QUIT:                      #умова дя зупинення циклу при закриванні вікна
                pg.quit()
                quit()

        # clear all
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #чистимо буфер
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # object 1
        glPushMatrix()
        glTranslatef(0.3, 0.3, -1.4)                       #тор 1 з-координата більша
        glRotatef(rotation1,2, 0, 2)
        rotation1 +=  5
        drawFigure(a1, a2,False)
        glPopMatrix()


        glPushMatrix()
        glTranslatef(0, 0.3, -2.5)                         #тор 2 з-координата менша
        glRotatef(rotation2,2, 0, 2)
        rotation2 += 5
        drawFigure(t1, t2,False)
        glPopMatrix()


        glPushMatrix()                                     #сфера 1 (знаходиться за торами)
        glTranslatef(-1, 0, -5)
        glRotatef(rotation3, 0.5, 0.5, 0.5)
        rotation3 += 3
        drawFigure(c1, c2,False)
        glPopMatrix()

        glPushMatrix()                                     #сфера 4 (знаходить дуже далеко ззаду
        glTranslatef(0, 0, -10)                            # тому повністю ховається в тумані
        drawFigure(c3, c4,False)                           #і на скріншотах її не видно
        glPopMatrix()

        pg.display.flip()                                  #оновлюємо вміст вікна pygame
        pg.time.wait(10)                                   #затримка анімації (мілісекунди)



main()
