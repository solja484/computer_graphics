from PIL import Image


def julia(width,height,zoom):
    img = Image.new("CMYK", (width, height), "black")
    pix = img.load()

    cX, cY = -0.7, 0.27015

    #inside mandelbrot
    #cX, cY=-1,0.1
    #cX, cY = -1.1, 0
    cX, cY=-0.624,0.435
    #cX, cY=-3,3
    #cX, cY = 0.285, 0.01
    #cX, cY=-1.75,0

    #outside mandelbrot
    #cX,cY=2,0
    #cX,cY=1,0

    moveX, moveY = 0.0, 0.0
    maxIter = 255

    for ip in range(width):
        for iq in range(height):
            zx = 1.5 * (ip - width / 2) / (0.5 * zoom * width) + moveX
            zy = 1.0 * (iq - height / 2) / (0.5 * zoom * height) + moveY
            i = maxIter
            while zx*zx + zy*zy < 4 and i > 1:
                  zy,zx = 2.0*zx*zy + cY, zx*zx - zy*zy + cX
                  i -= 1
            pix[ip, iq] = (i << 21) + (i << 10) + (i << 3)
    return img


def main():
    width = 400
    height = 300
    zoom = 1

    img=julia(width,height,zoom)
    img.show()

main()
