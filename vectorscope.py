import numpy as np
import cv2

def readcolor(filename):
     img = cv2.imread(filename)
     YCbCrimg = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

     B, G, R = img[:,:,0], img[:,:,1], img[:,:,2]
     Y = (0.299 * R) + (0.587 * G) + (0.114 * B)
     Cb = (-0.169 * R) - (0.331 * G) + (0.500 * B) + 128
     Cr = (-0.500 * R) + (0.418 * G) + (0.082 * B) + 128

     dst = np.zeros((256, 256, 3), dtype=img.dtype)

     for x in range(img.shape[0]):
       for y in range(img.shape[1]):
          dst[int(Cr[x, y]), int(Cb[x, y])] = np.array([B[x, y], G[x, y], R[x, y]])


     color = (30,165, 255)
     dst = cv2.circle(dst, (128, 128), 128, color, 1)
     dst = cv2.line(dst, (128,0), (128,256), color, 1)
     dst = cv2.line(dst, (0,128), (256,128), color, 1)
     cv2.imshow('window',img)
     cv2.imshow('window1',YCbCrimg)
     cv2.imshow('window2',dst)
     cv2.waitKey(0)
     cv2.destroyAllWindows()



readcolor("original.tif")
#readcolor("img2.jpg")

