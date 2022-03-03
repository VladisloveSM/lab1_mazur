from tkinter import *
from tkinter import colorchooser
import tkinter as tk
import math

RGB_SCALE = 255
CMYK_SCALE = 100


def rec_create(my_color):
    canvas.create_rectangle(20, 20, 190, 100, fill=my_color)


def color():
    my_color = colorchooser.askcolor()
    print(my_color)
    cmyk = rgb_to_cmyk(my_color[0])
    print_cmyk(cmyk)
    lab = rgb2lab(my_color[0])
    printLAB(lab)
    lab2rgb(lab)
    xyz = rgb2xyz(my_color[0])
    print_xyz(xyz)
    rec_create(my_color[1])


def rgb_to_cmyk(rgb):
    if rgb == (0, 0, 0):
        return 0, 0, 0, CMYK_SCALE

    c = 1 - rgb[0] / RGB_SCALE
    m = 1 - rgb[1] / RGB_SCALE
    y = 1 - rgb[2] / RGB_SCALE

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c*CMYK_SCALE, m*CMYK_SCALE, y*CMYK_SCALE, k*CMYK_SCALE


def print_cmyk(cmyk):
    CMYK_C.delete(0, END)
    CMYK_K.delete(0, END)
    CMYK_M.delete(0, END)
    CMYK_Y.delete(0, END)
    CMYK_C.insert(0, str(math.trunc(cmyk[0])) + '')
    CMYK_M.insert(0, str(math.trunc(cmyk[1])) + '')
    CMYK_Y.insert(0, str(math.trunc(cmyk[2])) + '')
    CMYK_K.insert(0, str(math.trunc(cmyk[3])) + '')


def cmyk_to_rgb(cmyk):
    C = cmyk[0]
    M = cmyk[1]
    Y = cmyk[2]
    K = cmyk[3]
    if (C, M, Y) == (0, 0, 0) and K == 100:
        return 0, 0, 0
    C /= CMYK_SCALE
    M /= CMYK_SCALE
    Y /= CMYK_SCALE
    K /= CMYK_SCALE
    min_cmy = K
    C = C * (1 - min_cmy) + min_cmy
    M = M * (1 - min_cmy) + min_cmy
    Y = Y * (1 - min_cmy) + min_cmy
    r = (1 - C) * RGB_SCALE
    g = (1 - M) * RGB_SCALE
    b = (1 - Y) * RGB_SCALE
    r = math.trunc(r)
    g = math.trunc(g)
    b = math.trunc(b)

    return r, g, b


def cmyk_command():
    C = int(CMYK_C.get())
    M = int(CMYK_M.get())
    Y = int(CMYK_Y.get())
    K = int(CMYK_K.get())
    cmyk = (C, M, Y, K)
    rgb = cmyk_to_rgb(cmyk)
    rec_create('#{:X}{:X}{:X}'.format(rgb[0], rgb[1], rgb[2]))
    lab = rgb2lab((rgb[0], rgb[1], rgb[2]))
    xyz = rgb2xyz(rgb)
    print_xyz(xyz)
    printLAB(lab)


def rgb2xyz(rgb):
    r = rgb[0] / RGB_SCALE
    g = rgb[1] / RGB_SCALE
    b = rgb[2] / RGB_SCALE

    if r > 0.04045 :
        r = (((r + 0.055) / 1.055) ** 2.4)
    else:
        r = r / 12.92

    if g > 0.04045 :
        g = (((g + 0.055) / 1.055) ** 2.4)
    else:
        g = g / 12.92

    if b > 0.04045:
        b = (((b + 0.055) / 1.055) ** 2.4)
    else:
        b = b / 12.92

    x = (r * 0.4124564) + (g * 0.3575761) + (b * 0.1804375)
    y = (r * 0.2126729) + (g * 0.7151522) + (b * 0.072175)
    z = (r * 0.0193339) + (g * 0.119192) + (b * 0.9503041)

    return x*100, y*100, z*100


def rgb2lab(rgb):
    xyz = rgb2xyz(rgb)
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    x /= 95.047
    y /= 100
    z /= 108.883

    if x > 0.008856:
        x = (x ** (1 / 3))
    else:
        x = (7.787 * x) + (16 / 116)

    if y > 0.008856:
        y = (y ** (1 / 3))
    else:
        y = (7.787 * y) + (16 / 116)

    if z > 0.008856:
        z = (z ** (1 / 3))
    else:
        z = (7.787 * z) + (16 / 116)

    l = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return l, a, b


def lab2xyz(lab):
    l = lab[0]
    a = lab[1]
    b = lab[2]

    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    y2 = y ** 3
    x2 = x ** 3
    z2 = z ** 3

    if y2 > 0.008856:
        y = y2
    else:
        y = (y - 16 / 116) / 7.787

    if x2 > 0.008856:
        x = x2
    else:
        x = (x - 16 / 116) / 7.787

    if z2 > 0.008856:
        z = z2
    else:
        z = (z - 16 / 116) / 7.787

    x *= 95.047
    y *= 100
    z *= 108.883

    return x, y, z


def xyz2rgb(xyz):
    x = xyz[0] / 100
    y = xyz[1] / 100
    z = xyz[2] / 100

    r = (x * 3.2404542) + (y * -1.5371385) + (z * -0.4985314)
    g = (x * -0.969266) + (y * 1.8760108) + (z * 0.041556)
    b = (x * 0.0556434) + (y * -0.2040259) + (z * 1.0572252)

    if r > 0.0031308:
        r = ((1.055 * (r ** (1.0 / 2.4))) - 0.055)
    else:
        r = r * 12.92

    if g > 0.0031308:
        g = ((1.055 * (g ** (1.0 / 2.4))) - 0.055)
    else:
        g = g * 12.92

    if b > 0.0031308:
        b = ((1.055 * (b ** (1.0 / 2.4))) - 0.055)
    else:
        b = b * 12.92

    r = min(max(0, r), 1)
    g = min(max(0, g), 1)
    b = min(max(0, b), 1)

    return r * 255, g * 255, b * 255


def lab2rgb(lab):
    xyz = lab2xyz(lab)
    rgb = xyz2rgb(xyz)
    return rgb


def printLAB(lab):
    LAB_L.delete(0, END)
    LAB_A.delete(0, END)
    LAB_B.delete(0, END)
    LAB_L.insert(0, str(round(lab[0], 3)))
    LAB_A.insert(0, str(round(lab[1], 3)))
    LAB_B.insert(0, str(round(lab[2], 3)))


def Lab_command():
    l = float(LAB_L.get())
    a = float(LAB_A.get())
    b = float(LAB_B.get())

    lab = (l, a, b)
    rgb = lab2rgb(lab)
    cmyk = rgb_to_cmyk(rgb)
    print_cmyk(cmyk)
    xyz = rgb2xyz(rgb)
    print_xyz(xyz)
    rec_create('#{:X}{:X}{:X}'.format(round(rgb[0]), round(rgb[1]), round(rgb[2])))


def XYZ_command():
    x = float(XYZ_X.get())
    y = float(XYZ_Y.get())
    z = float(XYZ_Z.get())
    xyz = (x, y, z)
    rgb = xyz2rgb(xyz)
    cmyk = rgb_to_cmyk(rgb)
    print_cmyk(cmyk)
    lab = rgb2lab(rgb)
    printLAB(lab)
    rec_create('#{:X}{:X}{:X}'.format(round(rgb[0]), round(rgb[1]), round(rgb[2])))



def print_xyz(xyz):
    XYZ_X.delete(0, END)
    XYZ_Y.delete(0, END)
    XYZ_Z.delete(0, END)
    XYZ_X.insert(0, str(round(xyz[0], 3)))
    XYZ_Y.insert(0, str(round(xyz[1], 3)))
    XYZ_Z.insert(0, str(round(xyz[2], 3)))


if __name__ == '__main__':
    root = Tk()
    root.title("Color-converter")
    root.geometry("650x400")

    my_button = Button(root, text="Chose A Color", command=color).grid(row=0, column=8, padx=1, pady=15)

    canvas = Canvas(root)

    canvas.grid(row=4, column=9, padx=0, pady=0)

    button_CMYK = Button(root, text="UseCMYK", command=cmyk_command).grid(row=1, column=8, padx=4, pady=0)

    Label_C = tk.Label(root, text='C:').grid(row=1, column=0, padx=0, pady=20)
    CMYK_C = tk.Entry(root, width=5)
    CMYK_C.grid(row=1, column=1, padx=15, pady=20)
    Label_C = tk.Label(root, text='M:').grid(row=1, column=2, padx=0, pady=20)
    CMYK_M = tk.Entry(root, width=5)
    CMYK_M.grid(row=1, column=3, padx=15, pady=20)
    Label_C = tk.Label(root, text='Y:').grid(row=1, column=4, padx=0, pady=20)
    CMYK_Y = tk.Entry(root, width=5)
    CMYK_Y.grid(row=1, column=5, padx=15, pady=20)
    Label_C = tk.Label(root, text='K:').grid(row=1, column=6, padx=0, pady=20)
    CMYK_K = tk.Entry(root, width=5)
    CMYK_K.grid(row=1, column=7, padx=15, pady=20)

    button_LAB = Button(root, text="UseLAB", command=Lab_command).grid(row=2, column=8, padx=4, pady=0)

    Label_L = tk.Label(root, text='L:').grid(row=2, column=0, padx=0, pady=20)
    LAB_L = tk.Entry(root, width=7)
    LAB_L.grid(row=2, column=1, padx=15, pady=20)
    Label_A = tk.Label(root, text='A:').grid(row=2, column=2, padx=0, pady=20)
    LAB_A = tk.Entry(root, width=7)
    LAB_A.grid(row=2, column=3, padx=15, pady=20)
    Label_B = tk.Label(root, text='B:').grid(row=2, column=4, padx=0, pady=20)
    LAB_B = tk.Entry(root, width=7)
    LAB_B.grid(row=2, column=5, padx=15, pady=20)

    button_XYZ = Button(root, text='UseXYZ', command=XYZ_command).grid(row=3, column=8, padx=4, pady=0)

    Label_X = tk.Label(root, text='X:').grid(row=3, column=0, padx=0, pady=20)
    XYZ_X = tk.Entry(root, width=7)
    XYZ_X.grid(row=3, column=1, padx=15, pady=20)
    Label_Y = tk.Label(root, text='Y:').grid(row=3, column=2, padx=0, pady=20)
    XYZ_Y = tk.Entry(root, width=7)
    XYZ_Y.grid(row=3, column=3, padx=15, pady=20)
    Label_Z = tk.Label(root, text='Z:').grid(row=3, column=4, padx=0, pady=20)
    XYZ_Z = tk.Entry(root, width=7)
    XYZ_Z.grid(row=3, column=5, padx=15, pady=20)

    root.mainloop()
