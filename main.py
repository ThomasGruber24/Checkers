import tkinter as tk

# basic config
BOARD_SIZE = 8
TILE_SIZE = 80

# game state
board = [[None for r in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]
selected = None
turn = 'red'

# set up window
root = tk.Tk()
root.title("Checkers")
canvas = tk.Canvas(root, width=BOARD_SIZE*TILE_SIZE, height=BOARD_SIZE*TILE_SIZE)
canvas.pack()


def init_board():
    # fill starting positions
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                if row < 3:
                    board[row][col] = ('black', False)
                elif row > 4:
                    board[row][col] = ('red', False)


def draw_piece(row, col, color, king):
    # draw piece as a circle
    padding = 10
    x1 = col * TILE_SIZE + padding
    y1 = row * TILE_SIZE + padding
    x2 = (col + 1) * TILE_SIZE - padding
    y2 = (row + 1) * TILE_SIZE - padding

    canvas.create_oval(x1, y1, x2, y2, fill=color)

    # mark king
    if king:
        canvas.create_text((x1+x2)//2, (y1+y2)//2, text="K", fill="gold", font=("Arial", 20, "bold"))


def draw_board():
    # clear and redraw everything
    canvas.delete("all")

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1 = col * TILE_SIZE
            y1 = row * TILE_SIZE
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE

            color = "#DDB88C" if (row + col) % 2 == 0 else "#A66D4F"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

            piece = board[row][col]
            if piece:
                draw_piece(row, col, piece[0], piece[1])


def check_king(row, col):
    # promote piece if it reaches the end
    color, king = board[row][col]
    if (color == 'red' and row == 0) or (color == 'black' and row == BOARD_SIZE - 1):
        board[row][col] = (color, True)


def move_piece(start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]

    # can't move into occupied space
    if board[er][ec] is not None:
        return False

    direction = -1 if piece[0] == 'red' else 1
    is_king = piece[1]

    # normal move
    if abs(er - sr) == 1 and abs(ec - sc) == 1:
        if is_king or (er - sr == direction):
            board[er][ec] = piece
            board[sr][sc] = None
            check_king(er, ec)
            return True

    # capture move
    if abs(er - sr) == 2 and abs(ec - sc) == 2:
        mid_r = (sr + er) // 2
        mid_c = (sc + ec) // 2
        mid_piece = board[mid_r][mid_c]

        if mid_piece and mid_piece[0] != piece[0]:
            if is_king or (er - sr == 2 * direction):
                board[er][ec] = piece
                board[sr][sc] = None
                board[mid_r][mid_c] = None
                check_king(er, ec)
                return True

    return False


def on_click(event):
    global selected, turn

    col = event.x // TILE_SIZE
    row = event.y // TILE_SIZE

    # if something is selected, try to move
    if selected:
        if move_piece(selected, (row, col)):
            selected = None
            turn = 'black' if turn == 'red' else 'red'
        else:
            selected = None
    else:
        piece = board[row][col]
        if piece and piece[0] == turn:
            selected = (row, col)

    draw_board()


# init + run
init_board()
draw_board()
canvas.bind("<Button-1>", on_click)

root.mainloop()
