#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Tetяis

    Keys
    --------------------------------------------------
    left   : request to translate left by one column
    right  : request to translate right by one column
    up     : request to do a counterclockwise rotation
    down   : request to translate down by one row

__author__ = 'Leonardo Vidarte'

"""

import time
import random
import copy
import platform

import tkinter as tk
from tkinter import messagebox
from os import getpid
from os import system

# ===============================================
# WINDOW OPTIONS
# ===============================================
BG_COLOR = 'black'

# Board
BOARD_BG_COLOR = 'black'
BOARD_FG_COLOR = 'white'
BOARD_GRID_COLOR = '#333'

# Status
FONT_SIZE = 12
FONT_COLOR = 'white'

# Tetrominos
TETROMINO_FG_COLOR = 'black'
TETROMINO_BORDER_WIDTH = 2 # in pixels
I_COLOR = 'cyan'
O_COLOR = 'yellow'
T_COLOR = 'magenta'
J_COLOR = 'blue'
L_COLOR = 'orange'
S_COLOR = 'green'
Z_COLOR = 'red'
COMPLETE_ROW_BG_COLOR = 'white' # None for inherit
COMPLETE_ROW_FG_COLOR = None
# ===============================================


# Levels
LEVEL_0_DELAY = 1000 # inital delay between steps
ROWS_BY_LEVEL = 10
POINTS = [40, 100, 300, 1200] # 1 , 2, 3, Tetris

#
MENU_FONTS = 'TkDefaultFont 12'
MENU_BIG_FONTS = 'TkDefaultFont 14'
WIDTH = 13
HEIGHT = 20
SIZE = 30 # square size in pixels

# Tetrominos
I = (
     ((0,0,0,0),
      (1,1,1,1),
      (0,0,0,0),
      (0,0,0,0)),
     ((0,1,0,0),
      (0,1,0,0),
      (0,1,0,0),
      (0,1,0,0)),
     )

O = (
     ((1,1),
      (1,1)),
     )

T = (
     ((0,0,0),
      (1,1,1),
      (0,1,0)),
     ((0,1,0),
      (1,1,0),
      (0,1,0)),
     ((0,1,0),
      (1,1,1),
      (0,0,0)),
     ((0,1,0),
      (0,1,1),
      (0,1,0)),
     )

J = (
     ((0,1,0),
      (0,1,0),
      (1,1,0)),
     ((1,0,0),
      (1,1,1),
      (0,0,0)),
     ((0,1,1),
      (0,1,0),
      (0,1,0)),
     ((0,0,0),
      (1,1,1),
      (0,0,1)),
     )

L = (
     ((0,1,0),
      (0,1,0),
      (0,1,1)),
     ((0,0,0),
      (1,1,1),
      (1,0,0)),
     ((1,1,0),
      (0,1,0),
      (0,1,0)),
     ((0,0,1),
      (1,1,1),
      (0,0,0)),
     )

S = (
     ((0,0,0),
      (0,1,1),
      (1,1,0)),
     ((1,0,0),
      (1,1,0),
      (0,1,0)),
     )

Z = (
     ((0,0,0),
      (1,1,0),
      (0,1,1)),
     ((0,0,1),
      (0,1,1),
      (0,1,0)),
     )



class Application(tk.Tk):

    def __init__(self, width=WIDTH, height=HEIGHT, size=SIZE):
        tk.Tk.__init__(self)
        self.title('Tetris')
        self.option_add('*Font', MENU_FONTS)
        self.configTop = None
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.create_widgets()
        self.draw_grid()
        self.create_events()
        self.tetrominos = self.get_tetrominos()
        self.game_init()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.config(bg=BG_COLOR)

        width = self.width * self.size
        height = self.height * self.size

        # main menu
        self.menuBar = tk.Menu()
        self.config(menu=self.menuBar)

        # file submenu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Exit', command=self.onExit)

        # configuration submenu
        self.confMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label='Configuration', menu=self.confMenu)
        self.confMenu.add_command(label='Game', command=self.generalConfig)


        self.canvas = tk.Canvas(self, width=width, height=height,
                                bg=BOARD_BG_COLOR,
                                highlightbackground=BOARD_FG_COLOR)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)


        lb_status = self.lb_status = tk.Label(
            self, bg=BG_COLOR, fg=FONT_COLOR, font=('monospace', FONT_SIZE))
        lb_status.grid(row=0, column=1, padx=(0, 20), pady=20, sticky=tk.N)



    def generalConfig(self):

        gameTypeVar = tk.IntVar()
        shapeL = tk.IntVar()
        shapeO = tk.IntVar()
        shapeI = tk.IntVar()
        shapeS = tk.IntVar()
        shapeT = tk.IntVar()
        shapeZ = tk.IntVar()
        shapeJ = tk.IntVar()
        photoL = tk.PhotoImage(file='images/L.png')
        photoO = tk.PhotoImage(file='images/O.png')
        photoI = tk.PhotoImage(file='images/I.png')
        photoS = tk.PhotoImage(file='images/S.png')
        photoT = tk.PhotoImage(file='images/T.png')
        photoZ = tk.PhotoImage(file='images/Z.png')
        photoJ = tk.PhotoImage(file='images/J.png')


        # Toplevel window for configuration
        self.configTop = tk.Toplevel(takefocus=True)
        self.configTop.focus_set()
        self.configTop.grab_set()
        self.configTop.title='Configurations'


        # Dimensions frame
        self.dimensionsFrame = tk.Frame(self.configTop,
                                        borderwidth=2, relief=tk.GROOVE,
                                        padx=10, pady=10)
        self.dimensionsFrame.grid(row=0, column=0)
        self.dimensionLabel = tk.Label(self.dimensionsFrame,
                                       font=MENU_BIG_FONTS,
                                       text='Dimensions')
        self.dimensionLabel.grid(row=0, column=0, columnspan=2)
        self.heightLabel = tk.Label(self.dimensionsFrame, text='Height:')
        self.heightLabel.grid(row=1, sticky=tk.W)
        self.widthLabel = tk.Label(self.dimensionsFrame, text='Width:')
        self.widthLabel.grid(row=2, sticky=tk.W)
        self.boxSizeLabel= tk.Label(self.dimensionsFrame, text='Box Size:')
        self.boxSizeLabel.grid(row=3, sticky=tk.W)
        self.heightSpin = tk.Spinbox(self.dimensionsFrame, from_=10, to=40)
        self.heightSpin.grid(row=1, column=1)
        self.widthSpin = tk.Spinbox(self.dimensionsFrame, from_=6, to=30)
        self.widthSpin.grid(row=2, column=1)
        self.boxSizeSpin = tk.Spinbox(self.dimensionsFrame, from_=10, to=100)
        self.boxSizeSpin.grid(row=3, column=1)

        # Game type frame
        self.gameTypeFrame = tk.Frame(self.configTop,
                                      borderwidth=2, relief=tk.GROOVE,
                                      padx=10, pady=10)
        self.gameTypeFrame.grid(row=1, column=0)
        self.gameLabel = tk.Label(self.gameTypeFrame,
                                  font=MENU_BIG_FONTS,
                                  text='Game Type')
        self.gameLabel.grid(row=0)
        self.normalGameRadio = tk.Radiobutton(self.gameTypeFrame,
                                              text='Normal',
                                              variable=gameTypeVar,
                                              value=1)
        self.normalGameRadio.grid(row=1, sticky=tk.W)
        self.pausedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Paused',
                                              variable=gameTypeVar,
                                              value=2)
        self.pausedGameRadio.grid(row=2, sticky=tk.W)
        self.changeSpeedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Change Speed',
                                              variable=gameTypeVar,
                                              value=3)
        self.changeSpeedGameRadio.grid(row=3, sticky=tk.W)


        # Select shapes frame
        self.selectShapesFrame = tk.Frame(self.configTop,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.selectShapesFrame.grid(row=0, column=1, rowspan=2)
        self.selectLabel = tk.Label(self.selectShapesFrame,
                                    text='Select Shapes', font=MENU_BIG_FONTS)
        self.selectLabel.grid(row=0, column=0)

        self.L_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoL,
                                      variable=shapeL, onvalue=1, offvalue=0)
        self.L_check.image = photoL
        self.L_check.grid(row=1, column=0)

        self.J_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoJ,
                                      variable=shapeJ, onvalue=1, offvalue=0)
        self.J_check.image = photoJ
        self.J_check.grid(row=2, column=0)

        self.O_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoO,
                                      variable=shapeO, onvalue=1, offvalue=0)
        self.O_check.image = photoO
        self.O_check.grid(row=3, column=0)

        self.I_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoI,
                                      variable=shapeI, onvalue=1, offvalue=0)
        self.I_check.image = photoI
        self.I_check.grid(row=4, column=0)

        self.Z_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoZ,
                                      variable=shapeZ, onvalue=1, offvalue=0)
        self.Z_check.image = photoZ
        self.Z_check.grid(row=5, column=0)

        self.S_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoS,
                                      variable=shapeS, onvalue=1, offvalue=0)
        self.S_check.image = photoS
        self.S_check.grid(row=6, column=0)

        self.T_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoT,
                                      variable=shapeT, onvalue=1, offvalue=0)
        self.T_check.image = photoT
        self.T_check.grid(row=7, column=0)

        # Submit button
        self.resultFrame = tk.Frame(self.configTop,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.resultFrame.grid(row=2, column=0, rowspan=2)
        cancelButton = tk.Button(self.resultFrame, text='Cancel',
                                 command=self.configTop.destroy)
        cancelButton.grid(column=0, row=0)
        submitButton = tk.Button(self.resultFrame, text='Submit',
                                      command=self.configTop.destroy)
        submitButton.grid(column=1, row=0)


    # Exit function
    def onExit(self):
        id = getpid()
        os = platform.system()
        if os == 'Linux':
            command = 'kill ' + str(id)
            system(command)
        else:
            command = 'taskkill -f /pid ' + str(id)
            system(command)

    def draw_grid(self):
        for i in range(self.width - 1):
            x = (self.size * i) + self.size
            y0 = 0
            y1 = self.size * self.height
            self.canvas.create_line(x, y0, x, y1, fill=BOARD_GRID_COLOR)
        for i in range(self.height - 1):
            x0 = 0
            x1 = self.size * self.width
            y = (self.size * i) + self.size
            self.canvas.create_line(x0, y, x1, y, fill=BOARD_GRID_COLOR)

    def create_events(self):
        self.bind('<KeyPress-Up>', self.rotate)
        self.bind('<KeyPress-Down>', self.move)
        self.bind('<KeyPress-Left>', self.move)
        self.bind('<KeyPress-Right>', self.move)

    def get_tetrominos(self):
        tetrominos = []
        for name in 'IOTLJSZ':
            tetromino = globals()[name]
            data = {
                'name'  : name,
                'pieces': tetromino,
                'actual': 0,
                'color' : globals()[name + '_COLOR'],
                'coords': self.get_init_coords(tetromino),
                'rows': len(tetromino[0]),
                'cols': len(tetromino[0][0]),
                'total_pieces': len(tetromino),
                'can_rotate'  : True if len(tetromino) > 1 else False,
                'ids': [],
                }
            tetrominos.append(data)
        return tetrominos

    def get_init_coords(self, tetromino):
        return (int(self.width / 2.0 - len(tetromino[0]) / 2.0), 1)

    def game_init(self):
        self.board = self.get_init_board()
        self.next = copy.deepcopy(random.choice(self.tetrominos))
        self.tetromino = None
        self.status = self.get_init_status()
        self.delay = LEVEL_0_DELAY
        self.job_id = None
        self.running = True
        self.step()

    def get_init_board(self):
        if getattr(self, 'board', None) is None:
            self.board = [[0] * self.width for _ in range(self.height)]
        else:
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x]:
                        self.canvas.delete(self.board[y][x])
                        self.board[y][x] = 0
        return self.board

    def get_init_status(self):
        return {'score': 0, 'rows': 0, 'level': 0,
                'O': 0, 'I': 0, 'S': 0, 'T': 0, 'Z': 0, 'L': 0, 'J': 0,
                'total': 0, 'next': ''}

    def step(self):
        if self.configTop is not None  and self.configTop.winfo_exists():
            self.job_id = self.canvas.after(100, self.step)
        else:
            if self.tetromino and self.can_be_moved('Down'):
                self.move_tetromino((0, 1))
                self.job_id = self.canvas.after(self.delay, self.step)
            else:
                self.check_status()
                if self.is_gameover(self.next):
                    title = 'Game Over'
                    message = 'Your score: %d' % self.status['score']
                    messagebox.showinfo(title, message)
                    self.game_init()
                else:
                    self.tetromino = self.next
                    self.next = copy.deepcopy(random.choice(self.tetrominos))
                    self.status[self.tetromino['name']] += 1
                    self.status['total'] += 1
                    self.status['next'] = self.next['name']
                    self.update_label_status()
                    self.draw_tetromino()

                    self.job_id = self.canvas.after(self.delay, self.step)

    def check_status(self):
        rows = []
        for row in range(self.height):
            if 0 not in self.board[row]:
                rows.append(row)
        if rows:
            self.del_rows(rows)
            self.set_score(rows)

    def del_rows(self, rows):
        for row in rows:
            for id in self.board[row]:
                self.canvas.tag_raise(id) # bring to front
                self.canvas.itemconfig(id, fill=COMPLETE_ROW_BG_COLOR,
                                       outline=COMPLETE_ROW_FG_COLOR)
        self.canvas.update()
        time.sleep(0.5)
        for row in rows:
            for id in self.board[row]:
                self.canvas.delete(id)
            del self.board[row]
            self.board.insert(0, [0] * self.width)
            for row0 in range(row + 1):
                for id0 in self.board[row0]:
                    self.canvas.move(id0, 0, self.size)
        self.canvas.update()

    def set_score(self, rows):
        points = POINTS[len(rows) - 1]
        self.status['rows'] += len(rows)
        if self.status['rows'] % ROWS_BY_LEVEL == 0:
            self.status['level'] += 1
            if self.delay > 100:
                self.delay -= 100
        self.status['score'] += points
        self.update_label_status()

    def update_label_status(self):
        lines = [
            'Score: %6s' % self.status['score'],
            '',
            'Level: %6s' % self.status['level'],
            'Rows : %6s' % self.status['rows'],
            '',
            'O    : %6s' % self.status['O'],
            'I    : %6s' % self.status['I'],
            'J    : %6s' % self.status['J'],
            'L    : %6s' % self.status['L'],
            'T    : %6s' % self.status['T'],
            'S    : %6s' % self.status['S'],
            'Z    : %6s' % self.status['Z'],
            'Total: %6s' % self.status['total'],
            '',
            'Next : %6s' % self.status['next'],
            ]
        self.lb_status.config(text='\n'.join(lines))

    def is_gameover(self, next):
        x, y = next['coords']
        for y0 in range(next['rows']):
            for x0 in range(next['cols']):
                x1 = x0 + x
                y1 = y0 + y
                if self.board[y1][x1]:
                    self.running = False
                    self.canvas.after_cancel(self.job_id)
                    return True
        return False

    def draw_tetromino(self):
        self.del_tetromino()
        piece = self.tetromino['pieces'][self.tetromino['actual']]
        x0, y0 = self.tetromino['coords']
        for y in range(self.tetromino['rows']):
            for x in range(self.tetromino['cols']):
                if piece[y][x] == 1:
                    x1 = (x0 + x) * self.size
                    y1 = (y0 + y) * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    id = self.canvas.create_rectangle(
                            x1, y1, x2, y2, width=TETROMINO_BORDER_WIDTH,
                            outline=TETROMINO_FG_COLOR,
                            fill=self.tetromino['color'])
                    self.tetromino['ids'].append(id)
                    self.board[y0 + y][x0 + x] = id
        self.canvas.update()

    def del_tetromino(self):
        if self.tetromino['ids']:
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x] in self.tetromino['ids']:
                        self.board[y][x] = 0
            for id in self.tetromino['ids']:
                self.canvas.delete(id)
            self.tetromino['ids'] = []

    def rotate(self, event):
        if self.tetromino['can_rotate']:
            if self.tetromino['actual'] < self.tetromino['total_pieces'] - 1:
                next = self.tetromino['actual'] + 1
            else:
                next = 0
            if self.can_be_rotated(next):
                self.tetromino['actual'] = next
                self.draw_tetromino()

    def can_be_rotated(self, next):
        piece = self.tetromino['pieces'][next]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in range(self.tetromino['rows']):
            for x0 in range(self.tetromino['cols']):
                if piece[y0][x0] == 1:
                    if x == -1 and x0 == 1:
                        return False
                    if x + x0 >= self.width:
                        return False
                    if y + y0 >= self.height:
                        return False
                    x1 = x + x0
                    y1 = y + y0
                    if board[y1][x1] and \
                       (board[y1][x1] not in self.tetromino['ids']):
                        return False
        return True

    def move(self, event):
        if self.running and self.can_be_moved(event.keysym):
            x, y = self.tetromino['coords']
            if event.keysym == 'Left':
                self.move_tetromino((-1, 0))
            if event.keysym == 'Right':
                self.move_tetromino((1, 0))
            if event.keysym == 'Down':
                self.canvas.after_cancel(self.job_id)
                self.move_tetromino((0, 1))
                self.job_id = self.canvas.after(self.delay, self.step)

    def move_tetromino(self, offset):
        x, y = offset
        ranges = {
            (-1, 0): ((0, self.width, 1), (0, self.height, 1)),
            ( 1, 0): ((self.width-1, -1, -1), (0, self.height, 1)),
            ( 0, 1): ((0, self.width, 1), (self.height-1, -1, -1))
            }

        x_start_stop_step, y_start_stop_step = ranges[offset]
        for y0 in range(*y_start_stop_step):
            for x0 in range(*x_start_stop_step):
                id = self.board[y0][x0]
                if id in self.tetromino['ids']:
                    self.board[y0 + y][x0 + x] = self.board[y0][x0]
                    self.board[y0][x0] = 0
                    self.canvas.move(id, x * self.size, y * self.size)

        x1, y1 = self.tetromino['coords']
        self.tetromino['coords'] = (x1 + x, y1 + y)
        self.canvas.update()

    def can_be_moved(self, direction):
        piece = self.tetromino['pieces'][self.tetromino['actual']]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in range(self.tetromino['rows']):
            for x0 in range(self.tetromino['cols']):
                if piece[y0][x0] == 1:
                    if direction == 'Left':
                        x1 = x + x0 - 1
                        y1 = y + y0
                        if x1 < 0 or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
                            return False
                    if direction == 'Right':
                        x1 = x + x0 + 1
                        y1 = y + y0
                        if x1 >= self.width or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
                            return False
                    if direction == 'Down':
                        x1 = x + x0
                        y1 = y + y0 + 1
                        if y1 >= self.height or (board[y1][x1] and
                           board[y1][x1] not in self.tetromino['ids']):
                            return False
        return True


if __name__ == '__main__':

    prog = u'Tetяis'
    app = Application()
    app.mainloop()

