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
root.title('SankekBalls')
root.geometry(str(size_X) + 'x' + str(size_Y))


canv = Canvas(root, bg='white')
canv.create_text(200, 50, fill="darkblue", font="Times 20 italic bold")
canv.pack(fill=BOTH, expand=1)


colors = ['red', 'orange', 'yellow', 'green', 'blue']

n = 0
score = 0


def new_ball():
    global n
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
    if canv.coords(i+2)[2] >= size_X:
        if vel[i].x > 0:
            vel[i].refl_x()
    elif canv.coords(i+2)[0] <= 0:
        if vel[i].x < 0:
            vel[i].refl_x()
    elif canv.coords(i+2)[3] >= size_Y:
        if vel[i].y > 0:
            vel[i].refl_y()
    elif canv.coords(i+2)[1] <= 0:
        if vel[i].y < 0:
            vel[i].refl_y()
    else:
        return True


vel = [None]*100  # list that stores velocities of balls from the start of the programm
for i in range(len(vel)):
    vel[i] = Vector(uniform(-4, 4), uniform(-3, 0.5))

new_ball()
start_time = time.time()
current_time = 0
previous_time = 0


def click(event):
    global score

    if len(canv.find_withtag(CURRENT)) > 0 and canv.find_withtag(CURRENT)[0] != 1:
        canv.delete(CURRENT)
        score += 1
    print('score: ', score)


canv.bind('<Button-1>', click)


def stopwatch():
    global current_time
    global previous_time

    current_time = int(time.time() - start_time)
    if current_time >= previous_time:
        print('t: ', current_time)
        previous_time += 1

    canv.itemconfigure(1, text='Current time is ' + str(current_time) + ' sec' + '\nScore:' + str(score))

    root.after(500, stopwatch)


def movement():
    for i in range(len(vel)):
        if len(canv.coords(i+2)) > 0:  # checks if that ball exists
            canv.move(i+2, vel[i].x, vel[i].y)
            reflection(i)
            if reflection(i) is True:  # This condition is need to make a ball bouncing with the same velocity
                vel[i].add(0, 0.3)
    root.after(17, movement)


stopwatch()
movement()

mainloop()
