from tkinter import *
from random import randrange as rnd, choice, uniform
import time


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, d1, d2):
        self.x += d1
        self.y += d2

    def refl_x(self):
        self.x = -self.x

    def refl_y(self):
        self.y = -self.y

    def new(self, x=0, y=0):
        self.x = x
        self.y = y


size_X = 1078  # > 200
size_Y = 600  # >200

root = Tk()
root.geometry(str(size_X) + 'x' + str(size_Y))

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

n = 1
score = 0


def new_ball():
    global n
    global x, y, r
    # canv.delete(ALL)
    x = rnd(100, size_X-100)
    y = rnd(100, size_Y-100)
    r = rnd(5, 30)
    canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=1, tags=r)
    n += 1
    if n <= len(vel):
        root.after(1000, new_ball)


def reflection(i):
    if canv.coords(i+1)[2] > size_X or canv.coords(i+1)[0] < 0:
        vel[i].refl_x()
    if canv.coords(i+1)[3] > size_Y or canv.coords(i+1)[1] < 0:
        vel[i].refl_y()


vel = [None]*100
for i in range(len(vel)):
    vel[i] = Vector(uniform(-2, 2), uniform(-3, 0.5))

new_ball()

for t in range(10000):
    canv.update()

    def click(event):
        global score
        x = event.x
        y = event.y
        for i in range(len(vel)):
            if i < n-1:
                r = float(canv.gettags(1)[0])
                if (canv.coords(i+1)[0]+r/2-x)**2 + (canv.coords(i+1)[1]+r/2-y)**2 <= r**2:
                    score += 1
                    canv.itemconfigure(i+1, state='hidden')
        print(score)


    canv.bind('<Button-1>', click)

    for i in range(len(vel)):
        canv.move(i+1, vel[i].x*2, vel[i].y*2)
        if i < n-1:
            vel[i].add(0, 0.1)
            reflection(i)
    time.sleep(0.02)


mainloop()
