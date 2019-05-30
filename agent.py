#!/usr/bin/python3
# RKSP



# Names : 1. Rishabh Khurana
#         zID: z5220427
#         2. Sahil Punchhi
#         zID: z5204256
# Artificial Intelligence - Assignment 3
# Date : 01 May 2019





# INITIAL DEFINITIONS:
# We have identified possible ojective wins as all the cases when a player can win in a small board(3 x 3)
# Then initial big board is defined as a string of 81 elements, with index ranging from 0 to 80 which indicates positions of X and O on the big board (9 x 9)
# user board is when user places last move on the board and bot board is when agent places last move on the big board

# FLOW OF THE PROGRAM
# Probable objectives are defined, initial game board, players, boxes are defined. For each command, 'second move',
# 'third move', 'last move' - input values (in terms of response) are taken for the board number and cell number played by the user.
# These values are modified for other functions. Then player move and player game board are taken as inputs and best possible move by the agent is returned.
# Best possible move is calculated by making a game tree of all possible further moves.

# ALPHA BETA PRUNING
# To evaluate the best possible next move we have implemented depth limited search in a min-max tree (default value of depth as 5)
# and applied alpha beta pruning to the same. To increase the efficiency of alpha-beta pruning , we have defined
# a score heuristic value for different scenarios.

# HEURISTIC
# Heuristic evaluates winning and losing with high absolute values. First, absolute scoring for every small box is done in each possible case.
# Then scores of all the small boxes are added and possible best move is calculated as per the heuristic value returned.
# Alpha-beta pruning seeks to reduce the number of nodes that needs to be evaluated
# in the search tree by the minimax algorithm.

# SCORING
# One player in the possible objective win(row, column, diagonal) and rest 2 cells are empty(1 point)
# Two player in a possible objective win(row, column, diagonal) and third cell is empty (10 points)
# Three player in a possible objective win(row, column, diagonal) (100 points)
# rival player in the possible objective win(row, column, diagonal) and rest 2 cells are empty(-1 point)
# Two rival player in a possible objective win(row, column, diagonal) and third cell is empty (-10 points)
# Three player player in a possible objective win(row, column, diagonal) (-100 points)





import socket
import sys
from math import inf
from collections import Counter
import itertools



INITIAL_big_board = "." * 81
global big_board # big board is a string of 81 characters
big_board = INITIAL_big_board
global winner
winner=["."] * 9
global probable_objectives # possible objective wins
global curr # current small box
probable_objectives = [(0, 4, 8), (2, 4, 6)]
probable_objectives += [(i, i+3, i+6) for i in range(3)]
probable_objectives += [(3*i, 3*i+1, 3*i+2) for i in range(3)]



# index on the board

def index(x, y):
    x -= 1
    y -= 1
    return ((x//3)*27) + ((x % 3)*3) + ((y//3)*9) + (y % 3)



def box(x, y):
    return index(x,y)



# returns upcoming box
def upcomer_box(i):
    return i % 9



# returns corresponding indices of box big_board
def indices_of_box(b):
    return list(range(b*9, b*9 + 9))



def print_board(big_board):

    for row in range(1, 10):

        row_str = ["|"]

        for col in range(1, 10):

            row_str += [big_board[index(row, col)]]

            if (col) % 3 == 0:

                row_str += ["|"]

        if (row-1) % 3 == 0:

            print("-"*(len(row_str)*2-1))

        print(" ".join(row_str))

    print("-"*(len(row_str)*2-1))



# places the player move on respective cell

def placing_move(big_board, move, player):

    if not isinstance(move, int):

        move = index(move[0], move[1])

    return big_board[: move] + player + big_board[move+1:]



# updates winner

def update_winner(big_board):

    winner1 = ["."] * 9

    for b in range(9):

        idxs_box = indices_of_box(b)

        small_box_string = big_board[idxs_box[0]: idxs_box[-1]+1]

        winner1[b] = check_small_box(small_box_string)

    return winner1



# check if a particular sub board is winning

def check_small_box(small_box_string):

    global probable_objectives

    for idxs in probable_objectives:

        (a, b, c) = idxs

        if (small_box_string[a] == small_box_string[b] == small_box_string[c]) and small_box_string[x] != ".":

            return small_box_string[x]

    return "."



# returns possible indices of moves that can be made by a player in a particular sub-box

def possible_moves(last_move):

    if not isinstance(last_move, int):

        last_move = index(last_move[0], last_move[1])

    box_to_play = upcomer_box(last_move)

    possible_indices = indices_of_box(box_to_play)

    return possible_indices



# returns all the possible moves on upcoming boards

def upcoming_board(big_board, player, last_move):

    moves_idx = []

    upcomers = []

    possible_indexes = possible_moves(last_move)

    for idx in possible_indexes:

        if big_board[idx] == ".":

            moves_idx.append(idx)

            upcomers.append(placing_move(big_board, idx, player))

    return zip(upcomers, moves_idx)



def print_upcoming_board(big_board, player, last_move):

    for st in upcoming_board(big_board, player, last_move):

        print_board(st[0])



# returns the other player marker

def rival(m):

    return "O" if m == "X" else "X"



# score heuristic evaluation

def calculate_small_box(small_box_string, player):

    global probable_objectives

    score_heuristic = 0

    # for the rival

    three_rival = Counter(rival(player) * 3)

    two_rival = Counter(rival(player) * 2 + ".")

    one_rival = Counter(rival(player) * 1 + "." * 2)

    

    # for the player

    three_player = Counter(player * 3)

    two_player = Counter(player * 2 + ".")

    one_player = Counter(player * 1 + "." * 2)



    for idxs in probable_objectives:

        (a, b, c) = idxs

        current = Counter([small_box_string[a], small_box_string[b], small_box_string[c]])

        

        if current == three_player:

            score_heuristic = score_heuristic + 100

        elif current == two_player:

            score_heuristic = score_heuristic + 10

        elif current == one_player:

            score_heuristic = score_heuristic + 1

        elif current == three_rival:

            score_heuristic = score_heuristic - 100

            return score_heuristic

        elif current == two_rival:

            score_heuristic = score_heuristic - 10

        elif current == one_rival:

            score_heuristic = score_heuristic - 1



    return score_heuristic



# calculates score for all the boards in each particular case

def calculate(big_board, last_move, player):

    score_heuristic = 0

    for b in range(9):

        idxs = indices_of_box(b)

        small_box_string = big_board[idxs[0]: idxs[-1]+1]

        score_heuristic += calculate_small_box(small_box_string, player)

    return score_heuristic



# limited depth tree_pruning function returns the best possible move after calculating score heuristic

def tree_pruning(big_board, last_move, player, depth):

    best_move = (-inf, None)

    upcomers = upcoming_board(big_board, player, last_move)

    for t in upcomers:

        val = player_1_turn(t[0], t[1], rival(player), depth-1, -inf, inf)

        if val > best_move[0]:

            best_move = (val, t)

    return best_move[1]



# alpha beta pruning, when depth is 0 i.e. at leaf node, score is calculated

def player_1_turn(big_board, last_move, player, depth, alpha, beta):

    # when depth of tree is 0 calculates score

    if depth <= 0:

        return calculate(big_board, last_move, rival(player))

    upcomers = upcoming_board(big_board, player, last_move)

    for t in upcomers:

        val = player_2_turn(t[0], t[1], rival(player), depth-1,alpha, beta)

        if val < beta:

            beta = val

        if alpha >= beta:

            # prunes tree

            break

    return beta



# alpha beta pruning (player 2 turn)

def player_2_turn(big_board, last_move, player, depth, alpha, beta):

    # when depth of tree is 0, calculates score

    if depth <= 0:

        return calculate(big_board, last_move, player)

    upcomers = upcoming_board(big_board, player, last_move)

    for t in upcomers:

        val = player_1_turn(t[0], t[1], rival(player), depth-1, alpha, beta)

        if alpha < val:

            alpha = val

        if alpha >= beta:

            # prunes tree

            break

    return alpha



# converts to row number ranging from 1 to 9 and column number ranging from 1 to 9

def convert_tuple(x,y):

    if x in (1,2,3):
        if y in (1,2,3):
            x1 = 1
        elif y in (4,5,6):
            x1 = 2
        elif y in (7,8,9):
            x1 = 3

    elif x in (4,5,6):
        if y in (1,2,3):
            x1 = 4
        elif y in (4,5,6):
            x1 = 5
        elif y in (7,8,9):
            x1 = 6

    elif x in (7,8,9):
        if y in (1,2,3):
            x1 = 7
        elif y in (4,5,6):
            x1 = 8
        elif y in (7,8,9):
            x1 = 9

    if x in (1,4,7):
        if y in (1,4,7):
            y1 = 1
        elif y in (2,5,8):
            y1 = 2
        elif y in (3,6,9):
            y1 = 3

    elif x in (2,5,8):
        if y in (1,4,7):
            y1 = 4
        elif y in (2,5,8):
            y1 = 5
        elif y in (3,6,9):
            y1 = 6

    elif x in (3,6,9):
        if y in (1,4,7):
            y1 = 7
        elif y in (2,5,8):
            y1 = 8
        elif y in (3,6,9):
            y1 = 9

    return tuple((x1,y1))



# read what the server sent us and

# only parses the strings that are necessary

def parse(string,depth=5):

    global curr
    global big_board

    if "(" in string:

        command, args = string.split("(")

        args = args.split(")")[0]

        args = args.split(",")

    else:

        command, args = string, []

    

    if command == "second_move":

        #print_board(big_board)

        # convert_tuple return tuple of the form (row,column) of big_board

        # update their move

        user_move=convert_tuple(int(args[0]),int(args[1]))

        curr=int(args[1])

        user_big_board=placing_move(big_board, user_move, "X")

        # calculate best move

        bot_big_board, bot_move = tree_pruning(user_big_board, user_move, "O", depth)

        curr=(bot_move%9)+1

        # update our move

        big_board=bot_big_board

        # convert bot move from 0-80 to cell number of box

        return (bot_move%9)+1

    elif command == "third_move":

        #print_board(big_board)

        # place the move that was generated for us

        bot_move=convert_tuple(int(args[0]),int(args[1]))

        bot_big_board=placing_move(big_board,bot_move,"O")

        big_board=bot_big_board

        curr=int(args[1])

        # place their last move

        user_move=convert_tuple(curr,int(args[2]))

        curr=int(args[2])

        user_big_board=placing_move(big_board, user_move, "X")

        # calculate best move

        bot_big_board,bot_move = tree_pruning(user_big_board, user_move, "O", depth)

        curr=(bot_move%9)+1

        # update our move

        big_board=bot_big_board

        return (bot_move%9)+1

    elif command == "next_move":

        #print_board(big_board)

        # place their last move

        #print(f"curr and argu {curr},{int(args[0])}")

        user_move=convert_tuple(curr,int(args[0]))

        #print(f"user move is{user_move}")

        curr=int(args[0])

        #print(f"curr is{curr}")

        user_big_board=placing_move(big_board, user_move, "X")

        # calculate best move

        #print(f"user big_board is{user_big_board}")

        bot_big_board,bot_move = tree_pruning(user_big_board, user_move, "O", depth)

        #print("bot big_board and bot move")

        #print(bot_big_board)

        #print(bot_move)

        curr=(bot_move%9)+1

        # update our move

        big_board=bot_big_board

        return (bot_move%9)+1

    elif command =="last_move":

        #print_board(big_board)

        # place their last move

        user_move=convert_tuple(curr,int(args[0]))

        user_big_board=placing_move(big_board, user_move, "X")

        # box we are playing

        box_to_play=int(args[0])-1

        idxs=indices_of_box(box_to_play)

        for idx in idxs:

            if big_board[idx]==".":

                big_board[idx]=="O"

                return (idx%9)+1



    elif command=="draw":

        print("Its a draw")

        return -1

    elif command == "win":

        print("Yay!! We win!! :)")

        return -1

    elif command == "loss":

        print("We lost :(")

        return -1

    return 0



# connect to socket

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    

    s.connect(('localhost', port))

    while True:

        text = s.recv(1024).decode()

        if not text:

            continue

        for line in text.split("\n"):

            response = parse(line)

            if response == -1:

                s.close()

                return

            elif response > 0:

                s.sendall((str(response) + "\n").encode())



if __name__ == "__main__":

    main()

