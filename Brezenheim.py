import cv2
import numpy as np


def print_cv2(filename,color):

    # print cv2 circle and line
    img = cv2.imread(filename)
    half = int(img.shape[0]/2)
    img = cv2.line(img, (0, 0), (img.shape[0], img.shape[1]), color, 1)
    img = cv2.circle(img, (half, half), 100, color, 1)
    return img


def print_my(filename,color):

    # print my circle and line
    img = cv2.imread(filename);
    half = int(img.shape[0]/2)
    img = my_line(img, 0, 0, img.shape[0]-1, img.shape[1]-1, color)
    img = my_circle(img, half, half, 100, color)
    return img


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


def print_head(width,height,vector, face, color,filename):
    img = cv2.imread(filename)
    img2 = cv2.imread(filename)

    for i in range (len(face)):
        f=face[i]

        for j in range(3):
            v0=vector[f[j]]
            v1=vector[f[(j+1)%3]]
            x0=int((v0[0]+1)*width/2) -1
            y0=height -int((v0[1]+1)*height/2) -1
            x1=int((v1[0]+1)*width/2) -1
            y1=height -int((v1[1]+1)*height/2) -1
            res=my_line(img,x0,y0,x1,y1,color)
            res2=cv2.line(img2,(x0,y0),(x1,y1),color,1)


    cv2.imshow("my head", res)
    cv2.imshow("cv2 head", res2)


def my_line(img,x0,y0,x1,y1,color):
    steep = False
    if abs(x0-x1)<abs(y0-y1) :
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep=True

    if x0>x1 :
        x0,x1=x1,x0
        y0,y1=y1,y0

    dx=x1-x0
    dy=y1-y0
    derror2=abs(dy)*2
    error2=0
    y=y0

    for x in range(x0, x1+1):
        if steep:
            img[x, y] = color
        else:
            img[y, x] = color
        error2 += derror2
        if error2 > dx:
            if y1 > y0:
                y += 1
            else:
                y -= 1
            error2 -= dx * 2
    return img


def my_circle(img,x1,y1,r,color):

    #my circle with brezenheim algoritm
    x = 0
    y = r
    delta = 1 - 2 * r
    error = 0

    while y >= 0:
        img[x1 + x, y1 + y] = color
        img[x1 + x, y1 - y] = color
        img[x1 - x, y1 + y] = color
        img[x1 - x, y1 - y] = color
        error = 2 * (delta + y) - 1

        if delta < 0 and error <= 0:
            x = x + 1
            delta += 2 * x + 1
            continue

        error = 2 * (delta - x) - 1

        if delta > 0 and error > 0:
            y = y - 1
            delta += 1 - 2 * y
            continue

        x = x + 1
        delta += 2 * (x - y)
        y = y - 1

    return img


def main():
    color = (11,255,57)
    width = 400
    height = 400

    # print cv2 circle and line
    cv2.imshow('cv2 line & circle', print_cv2("black.png", color))

    # print my circle and line
    cv2.imshow('my line & circle', print_my("black.png", (1,132,255)))

    # read faces and vectors coordinates from model file
    vector, face = read_model("african_head.obj")

    # print head
    print_head(width,height,vector,face,color,"black400.png")


    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
