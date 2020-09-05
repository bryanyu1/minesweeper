# mine_counter(grid,row_list,col_list,changing_cols_list,row,col) returns a 
#   natural number representing the number of adjacent mines to the position 
#   indicated by the row and column on the grid. 
# mine_counter: MineGrid (listof Nat) (listof Nat) (listof Nat) Nat Nat -> Nat
# Requires:
#   row and col has to correspond to a position on the grid
#   cols_list = changing_cols_list 

def mine_counter(grid,row_list,col_list,changing_cols_list,row,col):
    if row_list == []:
        return 0
    elif changing_cols_list == []:
        return mine_counter(grid,row_list[1:],col_list,col_list,row,col)
    elif row_list[0] == row and changing_cols_list[0] == col:
        return mine_counter(grid,row_list,col_list, \
                            changing_cols_list[1:],row,col)    
    elif grid[row_list[0]][changing_cols_list[0]]:
        return 1 + mine_counter(grid,row_list,col_list, \
                                changing_cols_list[1:],row,col)
    else: 
        return mine_counter(grid,row_list,col_list, \
                            changing_cols_list[1:],row,col) 

# count_mines(grid,row,col) returns a natural number representing the number 
#   of adjacent mines to the position indicated by the row and column on the 
#   grid. Note: mines can be adjacent diagonally, but does not wrap around. 
# count_mines: MineGrid Nat Nat -> Nat
# Requires:
#   row and col has to correspond to a position on the grid

def count_mines(grid,row,col):
    row_list = [row - 1, row, row + 1]
    altered_row_list = list \
        (filter(lambda x: x >= 0 and x <= (len(grid) - 1),row_list))
    column_list = [col - 1, col, col + 1]
    altered_column_list = list \
        (filter(lambda y: y >= 0 and y <= (len(grid[row]) - 1),column_list))
    return mine_counter(grid,altered_row_list,altered_column_list, \
                       altered_column_list,row,col)

# flatten(grid_or_board) returns a list of strings from the inputted list of
#   lists, grid_or_board. 
# flatten: (listof (listof Str)) -> (listof Str)

def flatten(grid_or_board):
    if grid_or_board == []:
        return []
    else:
        return grid_or_board[0] + flatten(grid_or_board[1:])

# is_game_won(grid_list,board_list) returns True if all safe tiles are 
#   revealed, and no mine tiles are revealed, and False otherwise. 
# is_game_won: (listof Bool) (listof Str) -> Bool
# Requires:
#   grid_list and board_list to correspond to the same game (same dimensions 
#   and bomb locations) 

def is_game_won(grid_list,board_list):
    if grid_list == []:
        return True 
    elif board_list[0] == "*":
        return False  
    elif board_list[0].isdigit():
        return is_game_won(grid_list[1:],board_list[1:])
    elif grid_list[0] and board_list[0] == " ":
        return is_game_won(grid_list[1:],board_list[1:]) 
    else:
        return False

# game_won(grid,board) returns True if the game has been won (all safe tiles 
#   are revealed, and no mine tiles are revealed), and False otherwise. 
# game_won: MineGrid MineBoard -> Bool
# Requires:
#   grid and board to correspond to the same game (same dimensions 
#   and bomb locations) 

def game_won(grid,board):
    flatten_grid = flatten(grid)
    flatten_board = flatten(board)
    return is_game_won(flatten_grid,flatten_board)

# reveal(grid,board, row, col) reveals the tile at the given row and col(umn)
#   in board, using the mine positions from grid
# reveal: MineGrid MineBoard -> None
# requires: grid and board have the same dimensions and are consistent
#           0 <= row < height of board
#           0 <= col < width  of board
# effects: board is mutated

def reveal(grid,board,row,col):
    if grid[row][col]:
        board[row][col] = '*'
    else:
        board[row][col] = str(count_mines(grid,row,col))

# game_lost(board) returns true if board contains one or more revealed mines,
#   false otherwise
# game_lost: GameBoard -> Bool

def game_lost(board):
    mined_rows = len(list(filter(lambda row: '*' in row, board)))
    return mined_rows != 0

row_prompt = "Please enter a row number: "
col_prompt = "Please enter a column number: "
range_error = "Value out of range!"

# read_pos(limit,prompt) prompts the user using the given prompt, and then 
#   reads an int.  If int is not in range 0 .. limit-1 then prompt and read
#   are repeated, otherwise the read value is returned
# read_pos: Nat Str -> Nat
# requires: limit > 0
# effects: input and output

def read_pos(limit,prompt):
    n = int(input(prompt))
    if n < 0 or n >= limit:
        print(range_error)
        return read_pos(limit,prompt)
    else:
        return n

# draw_board(board) prints the board to the screen
# draw_board: MineBoard -> None
# effects: prints to screen

def draw_board(board):
    print("\n".join(map(lambda row: "".join(row),board)))

# make_board(width,height) returns a MineBoard with all tiles hidden, 
#   the board has "height" rows and "width" columns
# make_board: Nat Nat -> MineBoard
# requires: width, height are positive

def make_board(width,height):
    return list(map(lambda i: [' '] * width, range(height)))

# play_minesweeper(grid) plays a game of minesweeper, using grid for the mine
#   positions
# play_minesweeper: MineGrid -> None
# effects: reads input, prints to the screen

def play_minesweeper(grid):
    height = len(grid)
    width = len(grid[0])
    board = make_board(width,height)
    play_game(grid,board)

# play_game(grid,board) plays a game of minesweeper, using grid for the mine 
#   positions, and board as the current visible tiles
# play_game: MineGrid MineBoard -> None
# requires: grid and board are consistent
# effects: reads input, prints to the screen
    
def play_game(grid,board):
    height = len(grid)
    width = len(grid[0])
    print("="*width)
    draw_board(board)
    print("="*width)
    win = game_won(grid,board)
    lose = game_lost(board)
    if win:
        print("Game over, you win!")
    elif lose:
        print("Game over, you lose!")
    else:
        row = read_pos(height,row_prompt)
        col = read_pos(width,col_prompt)        
        reveal(grid,board,row,col)
        play_game(grid,board)
