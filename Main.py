"""
In this 'game' you play you play you win. Good game.
"""


from tkinter import *
from random import randrange, choice, uniform
from os import path
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
N = 20  # quantity of balls that is need to complete the game

root = Tk()
root.title('SankekBalls')
root.geometry(str(size_X) + 'x' + str(size_Y))

highscore = 'no results'
if path.exists('results.txt'):
    results = open('results.txt')
    k = 0

    for i in results:
        k += 1
        i = i.replace('\n', '')

        try:
            if float(i) < scr:
                scr = float(i)
                best_player_line = k-2
        except NameError:
            scr = float(i)
            best_player_line = 0
        except ValueError:
            pass

    try:
        results.seek(0)
        best_player = results.readlines()[best_player_line].replace('\n', '')
        highscore = str(scr) + ' seconds (' + best_player + ').'
    except (IndexError, NameError):
        pass
    results.close()


title = Label(root, text='SankekBalls', font=('Bahnschrift SemiBold', 44))
title.pack(expand=1, anchor=S)
lbl = Label(root, text='Catch ' + str(N) + ' balls as fast as you can!!!\n\nThe best result: ' 
                       + str(highscore), font=('Bahnschrift', 15))
lbl.pack(expand=1, anchor=S)
lbl_n = Label(root, text='Enter your name:', font=('Bahnschrift', 8))
lbl_n.pack(expand=1, anchor=S)
txt = Entry(root, width=20)
txt.pack(expand=1, anchor=CENTER)


def clicked():
    global click, player
    player = txt.get()
    click = True


btn = Button(root, text="Play", command=clicked)
btn.pack(expand=1, ipady=20, ipadx=40)

click = None

while True:
    root.update()
    if click is True:
        title.destroy()
        lbl.destroy()
        txt.destroy()
        btn.destroy()
        lbl_n.destroy()
        click = None
        break


canv = Canvas(root, bg='white')
canv.create_text(200, 50, fill="darkblue", font="Times 20 italic bold")
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']
n = 0
score = 0
game_is_on = True


def new_ball():
    global n
    if game_is_on:
        x = randrange(100, size_X-100)
        y = randrange(100, size_Y-100)
        r = randrange(10, 35)
        canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=1, tags=r)
        n += 1
        if n % 5 == 0:
            print('A nubmer of created balls: ', n)
        if n < len(vel):
            root.after(500, new_ball)


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


vel = [None]*N  # list that stores velocities of balls from the start of the programm
for i in range(len(vel)):
    vel[i] = Vector(uniform(-4, 4), uniform(-3, 0.5))

new_ball()
start_time = time.time()
current_time = 0
previous_time = 0


def click(event):
    global score, results

    if len(canv.find_withtag(CURRENT)) > 0 and canv.find_withtag(CURRENT)[0] != 1:
        canv.delete(CURRENT)
        score += 1
    print('score: ', score)

    if score == N and game_is_on is True:
        off_the_game()


canv.bind('<Button-1>', click)


def stopwatch():
    global current_time, previous_time
    if game_is_on:
        current_time = round(time.time() - start_time, 2)
        if current_time >= previous_time:
            print('t: ', current_time)
            previous_time += 1

        canv.itemconfigure(1, text='Current time is ' + str(current_time) + ' sec' + '\nScore:' + str(score))

        root.after(100, stopwatch)  # FIXME: if set it to faster speed it moves back and forth (text box changes)


def movement():
    if game_is_on:
        for i in range(len(vel)):
            if len(canv.coords(i+2)) > 0:  # checks if that ball exists
                canv.move(i+2, vel[i].x, vel[i].y)
                reflection(i)
                if reflection(i) is True:  # This condition is need to make a ball bouncing with the same velocity
                    vel[i].add(0, 0.3)

        root.after(17, movement)


def off_the_game():
    global game_is_on, results, title, lbl, lbl_n, txt, btn, highscore, scr
    game_is_on = False
    canv.destroy()
    your_result = round(time.time()-start_time, 2)
    try:
        if your_result < scr:
            highscore = str(your_result) + " seconds. (You're the best!!!)"
    except NameError:
        highscore = str(your_result) + " seconds. (You're the first.)"

    with open('results.txt', 'a+') as results:
        results.write(player + '\n' + str(your_result) + '\n' + '\n')

    title = Label(root, text='SankekBalls', font=('Bahnschrift SemiBold', 44))
    title.pack(expand=1, anchor=S)
    lbl = Label(root, text='Your result: ' + str(your_result) + ' seconds.'
                           '\n\nThe best result: ' + str(highscore), font=('Bahnschrift', 15))
    lbl.pack(expand=1, anchor=S)

    def last_click():
        quit()

    btn = Button(root, text='Quit', command=last_click)
    btn.pack(expand=1, ipady=20, ipadx=40)


stopwatch()
movement()


mainloop()
