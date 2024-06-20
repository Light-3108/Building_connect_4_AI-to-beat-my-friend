import numpy as np
import sys
import pygame
import math

YELLOW = (255,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
PURPLE = (255,255,255)
ROW = 6
COLUMN = 7
WIDTH = 700
HIGHT = 600
SQUARE_SIZE = 100
RADIUS = 50
screen = pygame.display.set_mode((WIDTH,HIGHT))



def position_score(board, player):
    score = 0

    # Score center column for higher importance
    center_array = [int(i) for i in list(board[:, COLUMN//2])]
    
    center_count = center_array.count(player)

    score += center_count*3


    # Score horizontal
    for r in reversed(range(ROW)):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)

    #Score vertical
    for c in reversed(range(COLUMN)):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    # Score positive sloped diagonal
    for r in reversed(range(ROW-3)):
        for c in range(COLUMN-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score negative sloped diagonal
    for r in reversed(range(ROW-3)):
        for c in range(COLUMN-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score


def evaluate_window(window, player):
    score = 0


    opp_player = 2
    if(player == 2):
        opp_player = 1
    if window.count(player) == 4:
        score += 400
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    flag = False
    if window.count(opp_player) == 3 and window.count(0) == 1:
        score -= 4

    return score



def is_valid_location(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in reversed(range(ROW)):
        if board[r][col] == 0:
            return r
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN-3):
        for r in range(ROW):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN):
        for r in range(ROW-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN-3):
        for r in range(ROW-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN-3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False
        

def minimax(board, depth, alpha, beta, maximizingPlayer):

    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 1):
                return (None, 100000000)  #yesma winning_move(board,1) hunu parxa jasto lagyo
            elif winning_move(board, 2):
                return (None, -100000000)
            else:
                return (None, 0)
        else:
            return (None, position_score(board, 1))
    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()   
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            # print(f"depth: {depth} column: {col} player 1: score: {new_score}")
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            # print(f"depth: {depth} column: {col} player 1: score: {new_score}")
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
   
def AI_play():
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    return col

def make_board():
    board = np.zeros((ROW,COLUMN))
    return board
board = make_board()

def check_win(board,r,c):
    for c1 in range(COLUMN):
        if c1 + 3 < COLUMN and board[r][c1] == board[r][c1+1] == board[r][c1+2] == board[r][c1+3] != 0:
            pygame.draw.line(screen,PURPLE,(c1*SQUARE_SIZE + (int)(SQUARE_SIZE/2), r*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),((c1+3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2), (r)*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),7)            
    for r1 in range(ROW):
        if r1 + 3 < ROW and board[r1][c] == board[r1+1][c] == board[r1+2][c] == board[r1+3][c] !=0:
            pygame.draw.line(screen,PURPLE,(c*SQUARE_SIZE + (int)(SQUARE_SIZE/2), r1*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),((c)*SQUARE_SIZE + (int)(SQUARE_SIZE/2), (r1+3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),7)
    for c in range(COLUMN-3):
        for r in range(ROW-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]!=0:
                pygame.draw.line(screen,PURPLE,(c*SQUARE_SIZE + (int)(SQUARE_SIZE/2), r*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),((c+3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2), (r+3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),7)
    for c in range(COLUMN-3 ):
        for r in range(3, ROW):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]!=0:
                pygame.draw.line(screen,PURPLE,(c*SQUARE_SIZE + (int)(SQUARE_SIZE/2), r*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),((c+3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2), (r-3)*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),7)
    pygame.display.update()

def update_position(board, col, color):
    for r in reversed(range(ROW)):
        if board[r][col] == 0:
            if color == RED:
                board[r][col] = 1
            else:
                board[r][col] = 2
            pygame.draw.circle(screen, color, (col * SQUARE_SIZE + (int)(SQUARE_SIZE / 2), r * SQUARE_SIZE + (int)(SQUARE_SIZE / 2)), RADIUS - 2)
            pygame.display.update()
            check_win(board, r, col)
            break


def draw_game():
    for r in range(ROW):
        for c in range(COLUMN):
            pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,BLACK,(c*SQUARE_SIZE + (int)(SQUARE_SIZE/2), r*SQUARE_SIZE + (int)(SQUARE_SIZE/2)),RADIUS-4)

draw_game()
pygame.display.update()

turn = 0
game_end = 0
while not game_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:

                #update position le position update garxa
                #vanepaxi paile AI le position thapaunu paryo
                #tespaxi hamle update position garne
                #col thapaye hunxa
                #turn == 1 ma ta hamle garne ho so no worry tala ko
                #ata nai change garnu paryo maile
            p_mouse = event.pos[0]
            col = math.floor(p_mouse/100)
            update_position(board,col,YELLOW)
            col = AI_play()
            update_position(board,col,RED)