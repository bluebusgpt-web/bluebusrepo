"""
Simple Tetris implementation using tkinter.
- Single-file, no external dependencies.
- Controls:
  Left/Right: move
  Up: rotate
  Down: soft drop
  Space: hard drop
  p: pause
  q or Esc: quit
"""

import tkinter as tk
import random

CELL_SIZE = 24
COLUMNS = 10
ROWS = 20
DELAY = 400  # ms per tick, will speed up

SHAPES = {
    'I': [[1,1,1,1]],
    'O': [[1,1],[1,1]],
    'T': [[0,1,0],[1,1,1]],
    'S': [[0,1,1],[1,1,0]],
    'Z': [[1,1,0],[0,1,1]],
    'J': [[1,0,0],[1,1,1]],
    'L': [[0,0,1],[1,1,1]],
}
COLORS = {
    'I':'#00f0f0', 'O':'#f0f000', 'T':'#a000f0', 'S':'#00f000',
    'Z':'#f00000', 'J':'#0000f0', 'L':'#f0a000'
}

class Piece:
    def __init__(self, shape):
        self.shape_name = shape
        self.matrix = [row[:] for row in SHAPES[shape]]
        self.x = COLUMNS // 2 - len(self.matrix[0]) // 2
        self.y = 0

    def rotate(self):
        # rotate clockwise
        self.matrix = [list(row) for row in zip(*self.matrix[::-1])]

    def width(self):
        return len(self.matrix[0])

    def height(self):
        return len(self.matrix)

class Tetris:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CELL_SIZE*COLUMNS+150, height=CELL_SIZE*ROWS, bg='#111111')
        self.canvas.pack()
        self.board = [[None]*COLUMNS for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False
        self.delay = DELAY
        self.current = self.new_piece()
        self.next_piece = self.new_piece()
        self._draw_grid()
        self._bind_keys()
        self._tick()

    def new_piece(self):
        return Piece(random.choice(list(SHAPES.keys())))

    def _bind_keys(self):
        self.root.bind('<Left>', lambda e: self.move(-1))
        self.root.bind('<Right>', lambda e: self.move(1))
        self.root.bind('<Up>', lambda e: self.rotate())
        self.root.bind('<Down>', lambda e: self.soft_drop())
        self.root.bind('<space>', lambda e: self.hard_drop())
        self.root.bind('p', lambda e: self.toggle_pause())
        self.root.bind('P', lambda e: self.toggle_pause())
        self.root.bind('q', lambda e: self.quit())
        self.root.bind('<Escape>', lambda e: self.quit())

    def _tick(self):
        if not self.game_over and not self.paused:
            moved = self._try_move(self.current, self.current.x, self.current.y+1)
            if not moved:
                self._lock_piece()
            self._redraw()
        self.root.after(self.delay, self._tick)

    def _try_move(self, piece, x, y):
        if self._valid_position(piece, x, y):
            piece.x = x
            piece.y = y
            return True
        return False

    def move(self, dx):
        if self.game_over or self.paused: return
        self._try_move(self.current, self.current.x+dx, self.current.y)
        self._redraw()

    def rotate(self):
        if self.game_over or self.paused: return
        old = [row[:] for row in self.current.matrix]
        self.current.rotate()
        if not self._valid_position(self.current, self.current.x, self.current.y):
            # simple wall kick attempts
            if not self._valid_position(self.current, self.current.x-1, self.current.y):
                if not self._valid_position(self.current, self.current.x+1, self.current.y):
                    self.current.matrix = old
        self._redraw()

    def soft_drop(self):
        if self.game_over or self.paused: return
        if not self._try_move(self.current, self.current.x, self.current.y+1):
            self._lock_piece()
        self._redraw()

    def hard_drop(self):
        if self.game_over or self.paused: return
        while self._try_move(self.current, self.current.x, self.current.y+1):
            pass
        self._lock_piece()
        self._redraw()

    def _valid_position(self, piece, x, y):
        for r, row in enumerate(piece.matrix):
            for c, val in enumerate(row):
                if val:
                    bx = x + c
                    by = y + r
                    if bx < 0 or bx >= COLUMNS or by < 0 or by >= ROWS:
                        return False
                    if self.board[by][bx] is not None:
                        return False
        return True

    def _lock_piece(self):
        for r, row in enumerate(self.current.matrix):
            for c, val in enumerate(row):
                if val:
                    bx = self.current.x + c
                    by = self.current.y + r
                    if 0 <= by < ROWS and 0 <= bx < COLUMNS:
                        self.board[by][bx] = self.current.shape_name
                    else:
                        # piece locked out of bounds -> game over
                        self.game_over = True
        self._clear_lines()
        if not self.game_over:
            self.current = self.next_piece
            self.next_piece = self.new_piece()
            if not self._valid_position(self.current, self.current.x, self.current.y):
                self.game_over = True

    def _clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = ROWS - len(new_board)
        if cleared:
            for _ in range(cleared):
                new_board.insert(0, [None]*COLUMNS)
            self.board = new_board
            self.lines += cleared
            self.score += [0,40,100,300,1200][cleared] * self.level
            # level up every 10 lines
            self.level = 1 + self.lines // 10
            self.delay = max(50, DELAY - (self.level-1)*30)

    def _draw_grid(self):
        # background grid
        for r in range(ROWS):
            for c in range(COLUMNS):
                x1 = c*CELL_SIZE
                y1 = r*CELL_SIZE
                x2 = x1+CELL_SIZE
                y2 = y1+CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='#222', fill='#111', tags='cell')

    def _redraw(self):
        self.canvas.delete('block')
        # draw board
        for r in range(ROWS):
            for c in range(COLUMNS):
                color = self.board[r][c]
                if color is not None:
                    self._draw_cell(c, r, COLORS[color])
        # draw current
        for r, row in enumerate(self.current.matrix):
            for c, val in enumerate(row):
                if val:
                    self._draw_cell(self.current.x+c, self.current.y+r, COLORS[self.current.shape_name])
        # next piece preview
        self.canvas.create_text(CELL_SIZE*COLUMNS+10, 20, anchor='nw', fill='#fff', text=f"Score: {self.score}", tags='block')
        self.canvas.create_text(CELL_SIZE*COLUMNS+10, 40, anchor='nw', fill='#fff', text=f"Lines: {self.lines}", tags='block')
        self.canvas.create_text(CELL_SIZE*COLUMNS+10, 60, anchor='nw', fill='#fff', text=f"Level: {self.level}", tags='block')
        self.canvas.create_text(CELL_SIZE*COLUMNS+10, 100, anchor='nw', fill='#fff', text="Next:", tags='block')
        # draw small preview
        px = COLUMNS*CELL_SIZE + 10
        py = 120
        for r, row in enumerate(self.next_piece.matrix):
            for c, val in enumerate(row):
                if val:
                    x = px + c* (CELL_SIZE//2)
                    y = py + r* (CELL_SIZE//2)
                    self.canvas.create_rectangle(x, y, x+CELL_SIZE//2, y+CELL_SIZE//2, fill=COLORS[self.next_piece.shape_name], outline='#222', tags='block')
        if self.game_over:
            self.canvas.create_text(CELL_SIZE*COLUMNS//2, CELL_SIZE*ROWS//2, fill='#fff', text='GAME OVER', font=('Helvetica',24), tags='block')

    def _draw_cell(self, c, r, color):
        x1 = c*CELL_SIZE
        y1 = r*CELL_SIZE
        x2 = x1+CELL_SIZE
        y2 = y1+CELL_SIZE
        self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, fill=color, outline='#222', tags='block')

    def toggle_pause(self):
        self.paused = not self.paused

    def quit(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tetris - simple')
    game = Tetris(root)
    root.mainloop()
