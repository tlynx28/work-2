import tkinter.messagebox
from tkinter import *
from tkinter.messagebox import *
from math import sin, cos, pi, exp


def factorial(q):
    for i in range(1, q):
        q *= i
    return q


def f():
    eps = 0.0001
    Lfun = []
    x = Xmin
    while x <= Xmax:
        an = 1
        Sum = an
        n = 1
        while abs(an) > eps:
            try:
                an = (-1)**n * x**(2*n) / factorial(2*n)
            except OverflowError:
                tkinter.messagebox.showerror('E', 'Числа слишком большие для отображения первой функции!')
                return []
            Sum += an
            n += 1
        Lfun.append((x, 2*Sum))
        x += 1 / Kx
    return Lfun


def g():
    Lfun = []
    x = Xmin
    while x <= Xmax:
        if x != 0:
            fun = cos(x) + dY
        else:
            fun = 2.0
        Lfun.append((x, fun))
        x += 1 / Kx
    return Lfun


def GetData():
    global Xmax, Xmin, Ymax, Ymin
    global dX, dY, Kx, Ky
    try:
        tmpXmax = float(ent3.get())
        tmpXmin = float(ent2.get())
        tmpYmax = float(ent5.get())
        tmpYmin = float(ent4.get())
        tmpdY = float(ent7.get())
        tmpdX = float(ent6.get())
    except ValueError:
        tkinter.messagebox.showerror('Ошибка', 'Число введенно не корректно')
        return False
    if ((tmpXmin >= tmpXmax) or
            (tmpYmin >= tmpYmax) or
            (tmpdX <= 0)):
        showwarning(title="Ошибка задания границ", message="Должны выполняться "
                                                               " неравенства:\n"
                                                               "Xmax > Xmin;\n"
                                                               "Ymax > Ymin;\n"
                                                               "Шаг меток > 2")
    else:
        Xmax = tmpXmax
        Xmin = tmpXmin
        Ymax = tmpYmax
        Ymin = tmpYmin
        dX = tmpdX
        dY = tmpdY
        Kx = MaxX / abs((Xmax - Xmin))
        Ky = MaxY / abs((Ymax - Ymin))
    return True


def SetMark(a, b, LrBt=1):
    ax_XY = []
    if LrBt:
        ax_XY.append((a, b))
        ax_XY.append((a + 10, b))
    else:
        ax_XY.append((a,b))
        ax_XY.append((a, b - 10))
    cv.create_line(ax_XY, fill='black', width = 2)


def plotXY():
    ax_XY = []
    ax_XY.append((5, 5))
    ax_XY.append((MaxX - 5, MaxY - 5))
    cv.create_rectangle(ax_XY, fill="white", outline="green", width=2)
    y = Ymin
    y_pix = MaxY
    flg = False
    while y < Ymax:
        textY = str(round(y, 2))
        SetMark(0, y_pix, 1)
        if flg:
            cv.create_text(15, y_pix, text=textY, anchor=W)
        SetMark(MaxX-10, y_pix, 1)
        if flg:
            cv.create_text(MaxX - 15, y_pix, text=textY, anchor=E)
        y += dX
        y_pix -= dX * Ky
        flg = not flg
    x = Xmin
    x_pix = 0
    flg = False
    while x < Xmax:
        textX = str(round(x, 2))
        SetMark(x_pix, 0, 0)
        if flg:
            cv.create_text(x_pix, 15, text=textX, anchor=N)
        SetMark(x_pix, MaxY, 0)
        if flg:
            cv.create_text(x_pix, MaxY - 15, text=textX, anchor=S)
        x += dX
        x_pix += dX*Kx
        flg = not flg


def Draw(event):
    cv.delete("all")
    fg = GetData()
    if fg:
        plotXY()
        Fdraw(f, 'blue')
        Fdraw(g, 'red')


def Fdraw(func, color):
    try:
        Lxy = func()
        Lpix = []
        for xy in Lxy:
            x = Kx * (xy[0] - Xmin)
            if xy[1] is not None:
                y = MaxY - Ky * (xy[1] - Ymin)
            else:
                y = 0
            Lpix.append((x, y))
        cv.create_line(Lpix, fill=color)
    except IndexError:
        pass


def Final(event):
    window_deleted()


def window_deleted():
    if askyesno("Выход", "Завершить работу?"):
        root.destroy()


def showXY(event):
    global ID1, ID2
    x = event.x
    y = event.y
    ent0.delete(0, END)
    ent1.delete(0, END)
    ent0.insert(0, str(round(Xmin + x/Kx, 2)))
    ent1.insert(0, str(round(Ymin + (MaxY - y)/Ky, 2)))
    cv.delete(ID1)
    cv.delete(ID2)
    ID1 = cv.create_line(0, y, MaxX, y, dash=(3, 5))
    ID2 = cv.create_line(x, 0, x, MaxY, dash=(3, 5))


root = Tk()
root.title("Графика")
root.protocol('WM_DELETE_WINDOW', window_deleted)
root.resizable(False, False)
Kp = 0.7
MaxX = root.winfo_screenwidth() * Kp
MaxY = root.winfo_screenheight() * Kp
cv = Canvas(root, width=MaxX, height=MaxY, bg="white")
cv.grid(row=0, columnspan=9)
cv.bind('<Button-1>', showXY)
Xmin = -10.0; Xmax = 10.0
Ymin = -5.0; Ymax = 5.0
Xmid = 0; Ymid = 0
dY = 1.0
dX = 1.0
ID1 = 0; ID2 = 0
Kx = MaxX / abs((Xmax - Xmin))
Ky = MaxY / abs((Ymax - Ymin))
lba0 = Label(root, text="X:", width=10, fg="blue", font="Ubutu, 12")
lba0.grid(row=1, column=0, sticky='e')
ent0 = Entry(root, width=5, font="Ubuntu, 12")
ent0.grid(row=1, column=1, sticky='w')
ent0.insert(0, '0')
lba1 = Label(root, text="Y:", width=10, fg="blue", font="Ubutu, 12")
lba1.grid(row=2, column=0, sticky='e')
ent1 = Entry(root, width=5, font="Ubuntu, 12")
ent1.grid(row=2, column=1, sticky='w')
ent1.insert(0, '0')
lba2 = Label(root, text="Xmin:", width=10, fg="blue", font="Ubutu, 12")
lba2.grid(row=1, column=2, sticky='e')
ent2 = Entry(root, width=5, font="Ubuntu, 12")
ent2.grid(row=1, column=3)
ent2.insert(0, Xmin)
lba3 = Label(root, text="Xmax:", width=10, fg="blue", font="Ubutu, 12")
lba3.grid(row=1, column=4, sticky='e')
ent3 = Entry(root, width=5, font="Ubuntu, 12")
ent3.grid(row=1, column=5)
ent3.insert(0, Xmax)
lba4 = Label(root, text="Ymin:", width=10, fg="blue", font="Ubutu, 12")
lba4.grid(row=2, column=2, sticky='e')
ent4 = Entry(root, width=5, font="Ubuntu, 12")
ent4.grid(row=2, column=3)
ent4.insert(0, Ymin)
lba5 = Label(root, text="Ymax:", width=10, fg="blue", font="Ubutu, 12")
lba5.grid(row=2, column=4, sticky='e')
ent5 = Entry(root, width=5, font="Ubuntu, 12")
ent5.grid(row=2, column=5)
ent5.insert(0, Ymax)
lba6 = Label(root, text="Шаг меток:", width=10, fg="blue", font="Ubutu, 12")
lba6.grid(row=1, column=6, sticky='e')
ent6 = Entry(root, width=5, font="Ubuntu, 12")
ent6.grid(row=1, column=7)
ent6.insert(0, dX)
lba7 = Label(root, text="Смещение:", width=10, fg="blue", font="Ubutu, 12")
lba7.grid(row=2, column=6, sticky='e')
ent7 = Entry(root, width=5, font="Ubuntu, 12")
ent7.grid(row=2, column=7)
ent7.insert(0, dY)
btn1 = Button(root, width=20, bg="#ccc", text="Рисовать")
btn1.grid(row=1, column=8)
btn1.bind("<Button-1>", Draw)
btn2 = Button(root, width=20, bg="#ccc", text="Выход")
btn2.grid(row=2, column=8)
btn2.bind("<Button-1>", Final)
root.mainloop()
