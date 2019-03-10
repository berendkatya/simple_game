from math import sqrt
from time import sleep, time
from random import randint
from tkinter import *
HEIGHT = 800
WIDTH = 1000
window = Tk()
window.title('Bubble Blaster')

c = Canvas(window, width=WIDTH, height=HEIGHT, bg='black')


filename = PhotoImage(file="C:/Users/N551/SPoW_82318_01.png")
filename2 = PhotoImage(file="C:/Users/N551/ship.png")

c.create_image((0, 0), image=filename, anchor="nw")
c.pack()

ship_id2 = c.create_oval(0, 0, 10, 10, outline='black')
ship_id = c.create_image((0, 0), image=filename2, anchor="center")
SHIP_R = 35
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)
SHIP_SPD = 10


def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        c .move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)


c.bind_all('<Key>', move_ship)
bub_id = list()
bub_r = list()
bub_speed = list()
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100


def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r,
                        dash=(10, 10), outline='lightgrey', fill=None)
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))


def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)


BUB_CHANCE = 5
TIME_LIMIT = 30
BONUS_SCORE = 1000


def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0]+pos[2])/2
    y = (pos[1]+pos[3])/2
    return x, y


def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]


def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)


def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R+bub_r[bub]):
            points += (bub_r[bub]+bub_speed[bub])
            del_bubble(bub)
    return points


score = 0
bonus = 0
end = time() + TIME_LIMIT
c.create_text(50, 30, text='TIME', fill='white', font=('Helvetica', 16))
c.create_text(150, 30, text='SCORE', fill='white', font=('Helvetica', 16))
time_text = c.create_text(50, 50, fill='white', font=('Helvetica', 20))
score_text = c.create_text(150, 50, fill='white', font=('Helvetica', 20))


def show_score(score):
    c.itemconfig(score_text, text=str(score))


def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))


# MAIN GAME LOOP
while time() < end and score <= 5000:
    if randint(1, BUB_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision()
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    show_score(score)
    show_time(int(end-time()))
    window.update()
    sleep(0.01)
if time() > end and score <= 5000:
    c.create_text(MID_X, MID_Y,
                  text='GAME OVER', fill='white', font=('Helvetica', 50))
    c.create_text(MID_X, MID_Y + 50,
                  text='Score:' + str(score), fill='white', font=('Helvetica', 40))
    c.create_text(MID_X, MID_Y + 100,
                  text='Bonus Time:' + str(bonus*TIME_LIMIT), fill='white', font=('Helvetica', 40))
if time() < end and score >= 5000:
    c.create_text(MID_X, MID_Y, text='YOU WON!',
                  fill='white', font=('Helvetica', 50))
