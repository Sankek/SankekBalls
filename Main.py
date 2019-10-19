from tkinter import *
from random import randrange, choice, uniform
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
size_Y = 600  # > 200

root = Tk()
root.geometry(str(size_X) + 'x' + str(size_Y))

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

n = 0
score = 0


def new_ball():
    global n
    global x, y, r
    x = randrange(100, size_X-100)
    y = randrange(100, size_Y-100)
    r = randrange(10, 35)
    canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=1, tags=r)
    n += 1
    if n % 5 == 0:
        print('A nubmer of created balls: ', n)
    if n < len(vel):
        root.after(2500, new_ball)


def reflection(i):
    if canv.coords(i+1)[2] >= size_X:
        if vel[i].x > 0:
            vel[i].refl_x()
    elif canv.coords(i+1)[0] <= 0:
        if vel[i].x < 0:
            vel[i].refl_x()
    elif canv.coords(i+1)[3] >= size_Y:
        if vel[i].y > 0:
            vel[i].refl_y()
    elif canv.coords(i+1)[1] <= 0:
        if vel[i].y < 0:
            vel[i].refl_y()
    else:
        return True


vel = [None]*100  # list that stores velocities of balls from the start of the programm
for i in range(len(vel)):
    vel[i] = Vector(uniform(-2, 2), uniform(-3, 0.5))

new_ball()
start_time = time.time()
current_time = 0
previous_time = 0

for t in range(10000):
    canv.update()

    def click(event):
        global score
        '''
        A way to check if mouse click is on a ball offered by Hirianov
        x = event.x
        y = event.y
        for i in range(len(vel)):
            if i < n-1:
                r = float(canv.gettags(i+1)[0])
                if (canv.coords(i+1)[0]+r/2-x)**2 + (canv.coords(i+1)[1]+r/2-y)**2 <= r**2:
                    score += 1
                    canv.itemconfigure(i+1, state='hidden')  # or canv.delete(i+1)
        '''
        if len(canv.coords(CURRENT)) > 0:
            canv.delete(CURRENT)
            score += 1
        print('score: ', score)

    canv.bind('<Button-1>', click)

    for i in range(len(vel)):
        if len(canv.coords(i+1)) > 0:  # checks if that ball exists
            canv.move(i+1, vel[i].x, vel[i].y)
            reflection(i)
            if reflection(i) is True:
                vel[i].add(0, 0.1)

    current_time = int(time.time() - start_time)
    if current_time >= previous_time:
        print('t: ', current_time)
        previous_time += 1

    time.sleep(0.017)

mainloop()
