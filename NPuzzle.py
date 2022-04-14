import math
import time
from copy import deepcopy
from heapq import heapify, heappush
from random import randint
from tkinter import *
from tkinter import ttk


class State:
    def __init__(self):
        # parent, op: toan tu
        self.list_tiles = None
        self.parent = None
        self.g = 0
        self.h = 0
        self.op = None

    def getvalues(self):
        if self.list_tiles is None:
            return None
        res = ''
        for x in self.list_tiles:
            res += str(x)
        return res

    def __lt__(self, other):
        if other is None:
            return False
        return self.g + self.h < other.g + other.h

    def docopy(self):
        sn = deepcopy(self)
        return sn

    def printmatrix(self):
        size = matrixsize
        for i in range(size):
            for j in range(size):
                print(self.list_tiles[i * size + j], end=' ')
            print()
        print()

    def getposbyvalue(self, val):
        sz = matrixsize
        for i in range(sz):
            for j in range(sz):
                if self.list_tiles[i * sz + j] == val:
                    return i, j


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add(self, item):
        heappush(self.queue, item)

    def get(self):
        return self.queue[0]

    def remove(self, item):
        self.queue.remove(item)
        heapify(self.queue)
        h = []
        for value in self.queue:
            heappush(h, value)
        self.queue = h

    def __len__(self):
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def ifcontain(self, node):
        if node is None:
            return False
        for value in self.queue:
            if equal(node, value):
                return True
        return False


class Operator:
    def __init__(self, i):
        self.i = i

    def checkstate(self, c):
        if c.list_tiles is None:
            return True
        return False

    def position0(self, c):
        sz = matrixsize
        for i in range(sz):  # i= 0 1 2
            for j in range(sz):
                if c.list_tiles[i * sz + j] == 0:
                    return i, j
        # return None

    def moveup(self, s):
        if self.checkstate(s):
            return None
        x, y = self.position0(s)
        if x == 0:
            return None
        return self.swap(s, x, y, self.i)

    def movedown(self, s):
        if self.checkstate(s):
            return None
        x, y = self.position0(s)
        if x == (matrixsize - 1):
            return None
        return self.swap(s, x, y, self.i)

    def moveright(self, s):
        if self.checkstate(s):
            return None
        x, y = self.position0(s)
        if y == (matrixsize - 1):
            return None
        return self.swap(s, x, y, self.i)

    def moveleft(self, s):
        if self.checkstate(s):
            return None
        x, y = self.position0(s)
        if y == 0:
            return None
        return self.swap(s, x, y, self.i)

    def swap(self, s, x, y, i):
        sz = matrixsize
        sn = s.docopy()
        x_new = x
        y_new = y

        if i == 0:  # xet down
            x_new = x + 1
            y_new = y
        if i == 1:  # xet up
            x_new = x - 1
            y_new = y
        if i == 2:  # xet Right
            x_new = x
            y_new = y + 1
        if i == 3:
            x_new = x
            y_new = y - 1
        sn.list_tiles[x * sz + y] = s.list_tiles[x_new * sz + y_new]  # gan vi tri = 0 cho vi tri New
        sn.list_tiles[x_new * sz + y_new] = 0  # gan gia tri vi tri New = 0
        return sn

    def move(self, s):
        if self.i == 0:
            return self.movedown(s)
        if self.i == 1:
            return self.moveup(s)
        if self.i == 2:
            return self.moveright(s)
        if self.i == 3:
            return self.moveleft(s)
        return None


def equal(A, B):
    if A is None:
        return False
    return A.getvalues() == B.getvalues()


# Print the matrix at each step
def tracepath(O):
    if O.parent is not None:
        tracepath(O.parent)
        global total_move
        total_move = total_move + 1
        print(O.op.i)
    O.printmatrix()
    drawMatrix(O)
    time.sleep(1)


# Calculate H()
def hx(S, G):
    sz = matrixsize
    res = 0.0
    for i in range(sz):
        for j in range(sz):
            if S.list_tiles[i * sz + j] != G.list_tiles[i * sz + j] and G.list_tiles[i * sz + j] != 0:
                if dropdownlisth.get() == "Number of misplaced tiles":
                    res += 1
                elif dropdownlisth.get() == "Eucledian distance":
                    x, y = S.getposbyvalue(G.list_tiles[i * sz + j])
                    res += math.sqrt(pow(x - i, 2) + pow(y - j, 2))
                else:
                    x, y = S.getposbyvalue(G.list_tiles[i * sz + j])
                    res += abs(x - i) + abs(y - j)
    return res


# For A*
def RUN_A(S, G):
    start = PriorityQueue()
    close = PriorityQueue()
    S.g = 0
    S.h = hx(S, G)
    start.add(S)
    enodes = 0
    dnodes = 0
    while True:
        if start.empty():
            print('searching failed')
            return
        O = start.get()
        enodes = enodes + 1
        start.remove(O)
        close.add(O)
        if equal(O, G):
            print('success')
            total_time = time.time() - t_start
            txttime.set(str(total_time) + " s")
            txtdnodes.set(str(dnodes))
            txtenodes.set(str(enodes))
            liststep.insert(END, "-------Begin-------\n")
            global total_move
            total_move = 0
            tracepath(O)
            return

        for i in range(4):  # i = 0 1 2 3
            op = Operator(i)
            child = op.move(O)  # child is the next node
            if child is None:
                continue

            if not start.ifcontain(child) and not close.ifcontain(child):
                child.parent = O
                child.op = op
                child.g = O.g + 1
                child.h = hx(child, G)
                start.add(child)
                dnodes = dnodes + 1


# For Greedy
def RUN_B(S, G):
    start1 = PriorityQueue()
    close1 = PriorityQueue()
    S.g = 0
    S.h = hx(S, G)
    start1.add(S)
    enodes = 0
    dnodes = 0
    while True:
        if start1.empty():
            print('searching failed')
            return
        O = start1.get()
        enodes = enodes + 1
        start1.remove(O)
        close1.add(O)  # get O from Open and add into Close
        if equal(O, G):
            print('success')
            total_time = time.time() - t_start
            txttime.set(str(total_time) + " s")
            txtdnodes.set(str(dnodes))
            txtenodes.set(str(enodes))
            liststep.insert(END, "-------Begin-------\n")
            global total_move
            total_move = 0
            tracepath(O)
            return
        for i in range(4):  # i = 0 1 2 3
            op = Operator(i)
            child = op.move(O)  # child is the next node
            if child is None:
                continue
            if not start1.ifcontain(child) and not close1.ifcontain(child):
                child.parent = O  # set parent is O
                child.op = op
                child.g = 0
                child.h = hx(child, G)
                start1.add(child)
                dnodes = dnodes + 1


def initmatrix(num):
    G = State()
    sz = matrixsize
    G.list_tiles = []
    for i in range(sz):
        for j in range(sz):
            G.list_tiles.append((i * sz + j + 1) % (sz * sz))
    # fix matrix
    # T = State()
    # T.list_tiles = []
    # T.list_tiles.append(1)
    # T.list_tiles.append(2)
    # T.list_tiles.append(3)
    # T.list_tiles.append(8)
    # T.list_tiles.append(0)
    # T.list_tiles.append(4)
    # T.list_tiles.append(7)
    # T.list_tiles.append(6)
    # T.list_tiles.append(5)
    # G = T.docopy()
    # fix matrix
    # T1 = State()
    # T1.list_tiles = []
    # T1.list_tiles.append(0)
    # T1.list_tiles.append(7)
    # T1.list_tiles.append(4)
    # T1.list_tiles.append(1)
    # T1.list_tiles.append(8)
    # T1.list_tiles.append(3)
    # T1.list_tiles.append(2)
    # T1.list_tiles.append(5)
    # T1.list_tiles.append(6)
    # S = T1.docopy()
    S = G.docopy()
    for i in range(num):
        op = Operator(randint(0, 3))
        k = op.move(S)
        if k != None:
            S = k
    return S, G


def configtostart():
    # Disable config side
    dropdownlist["state"] = DISABLED
    dropdownlisth["state"] = DISABLED
    startbutton["state"] = "disabled"
    initmatrixbutton["state"] = "disabled"
    newmatrixbutton["state"] = "disabled"
    # Clear result information side
    global t_start
    t_start = time.time()
    txttime.set("0.0s")
    txtdnodes.set("0")
    txtenodes.set("0")
    global liststep
    liststep.delete('1.0', END)
    root.update()


def startprocess():
    configtostart()
    # Run algorithm
    if dropdownlist.get() == "A* Algorithm":
        RUN_A(startboard, resultboard)
    else:
        RUN_B(startboard, resultboard)


def redrawinitmatrix():
    txttime.set("0.0s")
    txtdnodes.set("0")
    txtenodes.set("0")
    drawMatrix(startboard)


def gen_new_matrix():
    global startboard, resultboard
    global matrixsize
    global canvas
    if (matrixsize != int(ematrixs.get())):
        matrixsize = int(ematrixs.get())
    canvas["width"] = sqsize * matrixsize + 1
    canvas["height"] = sqsize * matrixsize + 1
    startboard, resultboard = initmatrix(50) #move the empty 50 times
    drawMatrix(startboard)
    global liststep
    liststep.delete('1.0', END)
    txttime.set("0.0s")
    txtdnodes.set("0")
    txtenodes.set("0")


def drawMatrix(newmatrix):
    print("Draw matrix function")
    canvas.delete("all")
    for row in range(matrixsize):
        for col in range(matrixsize):
            top = row * sqsize
            left = col * sqsize
            bottom = row * sqsize + sqsize - 1
            right = col * sqsize + sqsize - 1
            bgcolor = 'white'
            txtinside = newmatrix.list_tiles[row * matrixsize + col]
            if newmatrix.list_tiles[row * matrixsize + col] == 0:
                bgcolor = 'gray'
                txtinside = ""
                if (not equal(startboard, newmatrix)):
                    step = ""
                    if newmatrix.op.i == 0:
                        step = "Move " + str(newmatrix.list_tiles[row * matrixsize + col - matrixsize]) + " up\n"
                    if newmatrix.op.i == 1:
                        step = "Move " + str(newmatrix.list_tiles[row * matrixsize + col + matrixsize]) + " down\n"
                    if newmatrix.op.i == 2:
                        step = "Move " + str(newmatrix.list_tiles[row * matrixsize + col - 1]) + " to left\n"
                    if newmatrix.op.i == 3:
                        step = "Move " + str(newmatrix.list_tiles[row * matrixsize + col + 1]) + " to right\n"
                    liststep.insert(END, step)
            canvas.create_rectangle(left, top, right, bottom, outline='gray', fill=bgcolor)
            canvas.create_text(left + 50, top + 50, text=txtinside, font=("Purisa", 20))
    canvas.update()
    if (equal(resultboard, newmatrix)):
        liststep.insert(END, "----End with " + str(total_move) + " moves----")
        dropdownlist["state"] = NORMAL
        dropdownlisth["state"] = NORMAL
        startbutton["state"] = "normal"
        initmatrixbutton["state"] = "normal"
        newmatrixbutton["state"] = "normal"


root = Tk()
root.geometry("1200x700")
root.title("N Puzzle")
frame = Frame(root, width=1000, height=700)
frame.pack()
# Left side - Select Algorithm . Heuristic and Size of Matrix
leftframe = Frame(frame, width=270)
leftframe.pack(side=LEFT)
label = Label(leftframe, text="Select Algorithm")
label.pack()
vallist = ["A* Algorithm", "Greedy-Best-Search Algorithm"]
dropdownlist = ttk.Combobox(leftframe, values=vallist)
dropdownlist.set(vallist[0])
dropdownlist.pack()
space1 = Label(leftframe, text="")
space1.pack(padx=10, pady=10)
labelh = Label(leftframe, text="Select Heuristic Function")
labelh.pack()
hlist = ["Number of misplaced tiles", "Euclidean distance", "Manhattan distance"]
dropdownlisth = ttk.Combobox(leftframe, values=hlist, width=25)
dropdownlisth.set(hlist[0])
dropdownlisth.pack()
space2 = Label(leftframe, text="")
space2.pack(padx=10, pady=10)
matrixs_frame = Frame(leftframe)
matrixs_frame.pack()
lmatrixs = Label(matrixs_frame, text="Size of board: ").grid(row=0)
ematrixs = Entry(matrixs_frame, width=10)
ematrixs.insert(0, '3')
ematrixs.grid(row=0, column=1)
newmatrixbutton = Button(leftframe, text="Generate new board", command=gen_new_matrix)
newmatrixbutton.pack()
space3 = Label(leftframe, text="")
space3.pack(padx=10, pady=10)
startbutton = Button(leftframe, text="Start", command=startprocess)
startbutton.pack()
space4 = Label(leftframe, text="")
space4.pack(padx=10, pady=10)
initmatrixbutton = Button(leftframe, text="Back to init board", command=redrawinitmatrix)
initmatrixbutton.pack()
# ----------
# Right side - Result informations
stepsframe = Frame(frame, width=250)
stepsframe.grid_propagate(0)
stepsframe.pack(side=RIGHT)
time_frame = Frame(stepsframe)
time_frame.pack()
ltime = Label(time_frame, text="Time: ").grid(row=0)
txttime = StringVar()
txttime.set("0.0s")
etime = Label(time_frame, textvariable=txttime).grid(row=0, column=1)
discovernodes_frame = Frame(stepsframe)
discovernodes_frame.pack()
ldiscovernodes = Label(discovernodes_frame, text="Discovered nodes: ").grid(row=0)
txtdnodes = StringVar()
txtdnodes.set("0")
ediscovernodes = Label(discovernodes_frame, textvariable=txtdnodes).grid(row=0, column=1)
explorenodes_frame = Frame(stepsframe)
explorenodes_frame.pack()
lexplorenodes = Label(explorenodes_frame, text="Explored nodes: ").grid(row=0)
txtenodes = StringVar()
txtenodes.set("0")
eexplorenodes = Label(explorenodes_frame, textvariable=txtenodes).grid(row=0, column=1)
space4 = Label(stepsframe, text="")
space4.pack(padx=10, pady=10)
steplabel = Label(stepsframe, text="Steps")
steplabel.pack()
liststep = Text(stepsframe, width=30, wrap=NONE)
liststep.pack(padx=40)
scrollb = Scrollbar()
scrollb.place(in_=liststep, relx=1.0, relheight=1.0, bordermode="outside")
scrollb.configure(command=liststep.yview)
# ----------
# Center side - N-Puzzle
canvasframe = Frame(frame, width=500, height=700)
canvasframe.grid_propagate(0)
canvasframe.pack(padx=40, pady=50)
sqsize = 100
matrixsize = 3
canvas = Canvas(canvasframe, bg="white", width=sqsize * matrixsize + 1, height=sqsize * matrixsize + 1)
canvas.place(in_=canvasframe, anchor="c", relx=.5, rely=.5)
canvas.configure(borderwidth=0, highlightthickness=0)
startboard, resultboard = initmatrix(matrixsize * matrixsize - randint(matrixsize, matrixsize * (matrixsize - 1)))
drawMatrix(startboard)
# ----------
root.mainloop()
