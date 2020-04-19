import numpy as np
import matplotlib.pyplot as plt
plt.interactive(False)
from PIL import Image



def pillow_mandelbrot(xa, xb, ya, yb, maxIt,imgx, imgy,border=10):

    image = Image.new("RGBA", (imgx, imgy))

    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1)  + xa
            z = zx + zy * 1j
            c = z

            for i in range(maxIt):
                if abs(z) > border: break
                z = z * z + c
            image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16))

    image.show()

def get_mandelbrot(pmin, qmin, pmax, qmax, max_iterations, ppoints, qpoints,infinity_border=10):
    image = np.zeros((ppoints, qpoints))

    p, q = np.mgrid[pmin:pmax:(ppoints*1j), qmin:qmax:(qpoints*1j)]
    c = p + 1j*q
    z = np.zeros_like(c)
    for k in range(max_iterations):
        z = z**2 + c
        mask = (np.abs(z) > infinity_border) & (image == 0)
        image[mask] = k
        z[mask] = np.nan

    plt.imsave('new.png', -image.T, cmap='flag')
    return -image.T


def main():
    pmin, pmax, qmin, qmax = -2.5, 1.5, -2, 2
    ppoints, qpoints = 600, 600
    max_iterations = 400
    plt.xticks([])
    plt.yticks([])

    mandelbrot=get_mandelbrot(pmin,qmin,pmax,qmax,max_iterations,ppoints,qpoints)
    plt.imshow(mandelbrot, cmap='flag', interpolation='none')
    plt.show()

    pillow_mandelbrot(pmin, pmax, qmin, qmax, max_iterations, ppoints, qpoints)

main()
