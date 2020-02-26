#!/usr/local/bin/python3


from logic_IJK import Game_IJK
import random
import copy
import time


class InvalidMoveException(Exception):
    pass

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

'''
def cover_up(mat):
    new = [[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' ']]
    done = False
    for i in range(6):
        count = 0
        for j in range(6):
            if mat[i][j] != ' ':
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return (new, done)
'''
def cover_up(mat):
	new = [[' ' for _ in range(6)]for _ in range(6)]

	done = False
	for i in range(6):
		count = 0
		for j in range(6):
			if mat[i][j] != ' ':
				new[i][count] = mat[i][j]
				if j != count:
					done = True
				count += 1
	return (new, done)
'''
def merge(mat, current_player):

    done = False
    for i in range(6):
        for j in range(5):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != ' ':
                mat[i][j] = chr(ord(mat[i][j])+ 1)
                mat[i][j+1] = ' '
                done = True
            elif mat[i][j].upper() == mat[i][j+1].upper() and mat[i][j] != ' ':
                mat[i][j] = chr(ord(mat[i][j])+ 1)
                mat[i][j] = mat[i][j].upper() if current_player > 0 else mat[i][j].lower()
                mat[i][j+1] = ' '
                done = True
    return (mat, done)
'''
def merge(mat, current_player):
	done = False
	for i in range(6):
		for j in range(5):
			if mat[i][j] == mat[i][j+1] and mat[i][j] != ' ':
				mat[i][j] = chr(ord(mat[i][j])+ 1)
				mat[i][j+1] = ' '
				done = True
			elif mat[i][j].upper() == mat[i][j+1].upper() and mat[i][j] != ' ':
				mat[i][j] = chr(ord(mat[i][j])+ 1)
				mat[i][j] = mat[i][j].upper() if current_player > 0 else mat[i][j].lower()
				mat[i][j+1] = ' '
				done = True
	return (mat, done)


def left(g, current_player):
    g, done = cover_up(g)
    temp = merge(g, current_player)
    g = temp[0]
    done = done or temp[1]
    g = cover_up(g)[0]
    if done == True:
        g = copy.deepcopy(g)
    return (g, done)


def down(g, current_player):
    g = reverse(transpose(g))
    g, done = cover_up(g)
    temp = merge(g, current_player)
    g = temp[0]
    done = done or temp[1]
    g = cover_up(g)[0]
    g = transpose(reverse(g))
    if done == True:
        g = copy.deepcopy(g)
    return (g, done)

def up(g, current_player):
    g = transpose(g)
    g, done = cover_up(g)
    temp = merge(g, current_player)
    g = temp[0]
    done = done or temp[1]
    g = cover_up(g)[0]
    g = transpose(g)
    if done == True:
        g = copy.deepcopy(g)
    return (g, done)

def right(g, current_player):
    #print("right")
    # return matrix after shifting right
    g = reverse(g)
    g, done = cover_up(g)
    temp = merge(g, current_player)
    g = temp[0]
    done = done or temp[1]
    g = cover_up(g)[0]
    g = reverse(g)
    if done == True:
        g = copy.deepcopy(g)
    return (g, done)


def makeMove(g, move, current_player):
    #if move not in ['U','L','D','R','S']:
    if move not in ['U','L','D','R']:
        raise InvalidMoveException
    if move == 'L':
        a=left(g, current_player)
    if move == 'R':
        a= right(g, current_player)
    if move == 'D':
        a=down(g, current_player)
    if move == 'U':
        a=up(g, current_player)
    #if move == 'S':
    #   a=skip(g)
    #return move, a
    return a[0]

def skip(g):
    return g


def get_children(board, current_player):
    children = []
    #for move in ['U', 'D', 'L', 'R', 'S']:
    for move in ['U', 'L', 'D', 'R']:
        children.append((makeMove(board, move, current_player), move))
    #print(children)
    return children


def game_state(board):
    zeros = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'K':
                return '+'
            if board[i][j] == 'k':
                return '-'
            if board[i][j] == '':
                zeros += 1
    return 0


def get_empty_location(board):
    if(board != None):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j] == ' '):
                    return i,j
    return -1, -1

def Decision(board, current_player, max=True):
    limit = 5
    start = time.clock()
    if max:
        return Maximize(board, '', limit, start, current_player, True, alpha=float('inf'), beta=float('inf'))
    else:
        return Minimize(board, '', limit, start, current_player, True, alpha=float('inf'), beta=float('inf'))


def Maximize(board, move, depth, start, current_player, first, alpha, beta):
    if(game_state(board) != 0 or depth==0 or (time.clock()-start)>2.5):
        #print('Eval Max: ', board, Eval(board))
        return Eval(board), move

    maxUtility =  -float("inf")
    final_move = ''

    #new_board = copy.deepcopy(board)
    if(first == False):
        i, j = get_empty_location(board)
        if(i != -1 and j != -1):
            #new_board[i][j] = 'A'
            board[i][j] = 'A'
    
    for child, move in get_children(board, current_player):
        m, new_move = Minimize(child, move, depth-1, start, current_player, False, alpha, beta)
        if(m > maxUtility):
            maxUtility = m
            final_move = move
        if maxUtility >= beta:
            #print('in break')
            break

        alpha = max(maxUtility, alpha)
    #print(maxUtility, move)
    return maxUtility, final_move


def Minimize(board, move, depth, start,current_player, first, alpha, beta):
    if(game_state(board)!=0  or depth==0 or (time.clock()-start)>2.5):
       #print('Eval Min: ', board, Eval(board))
       return Eval(board), move

    minUtility = float("inf")
    final_move = ''

    #new_board = copy.deepcopy(board)
    if(first == False):
        #print(board)
        i, j = get_empty_location(board)
        if(i != -1 and j != -1):
           #new_board[i][j] = 'a'
           board[i][j] = 'a'

    for child, move in get_children(board, current_player):
        m, new_move = Maximize(child, move, depth-1, start, current_player, False, alpha, beta)
        if(m < minUtility):
            minUtility = m
            final_move = move

        if minUtility <= alpha:
            #print('in break')
            break

        beta = min(minUtility, beta)

    #print(minUtility, move)
    return minUtility, final_move



def Eval(game):
   max1 = [0,0]
   max2 = [0,0]
   for i in range(len(game)):
       for j in range(len(game[0])):
           if game[i][j] != ' ':
               if game[i][j].isupper():
                   a = [ord(char) - 96 for char in game[i][j].lower()][0]
                   max1.append(a)
               else:
                   b = [ord(char) - 96 for char in game[i][j]][0]
                   max2.append(b)
   max1.sort()
   max2.sort()
   diff_from_k1 = ord('k')-96-max1[-1]
   diff_from_k2 = ord('k')-96-max2[-1]
   diff_btw_2 =  max2[-1] - max1[-1]
   internal_diff1 = max1[-1] - max1[-2]
   internal_diff2 = max2[-1] - max2[-2]
   eval_fun_val = diff_btw_2 - internal_diff1 + internal_diff2 #- diff_from_k1 + diff_from_k2
   return(eval_fun_val)




#Non-deterministic game plan
def Decision_nondet(board, current_player, max=True):
    limit = 5
    start = time.clock()
    if max:
        return Maximize_nondet(board, '', limit, start, current_player, True, alpha=float('inf'), beta=float('inf'))
    else:
        return Minimize_nondet(board, '', limit, start, current_player, True, alpha=float('inf'), beta=float('inf'))

def Maximize_nondet(board, move, depth, start, current_player, first, alpha, beta):
    if(game_state(board) != 0 or depth==0 or (time.clock()-start)>2.5):
        #print('Eval Max: ', board, Eval(board))
        return Eval(board), move

    maxUtility =  -float("inf")
    final_move = ''

    if(first == False):
        locs = get_empty_location_nondet(board)
        #old_board = board.copy()
        final_eval = float('-inf')
        for i,j in locs:
            new_board = copy.deepcopy(board)
            #print('New_board: ', new_board, i, j)
            new_board[i][j] = 'A'
            N_children = get_children(new_board, current_player)
            eval = 0
            for child, move in N_children:
                m, new_move = Minimize_nondet(child, move, depth-1, start, current_player, False, alpha, beta)
                if(m > maxUtility):
                    maxUtility = m
                    final_move = new_move
                if maxUtility >= beta:
                    #print('in break')
                    break

                eval += float((1/len(locs))*m)
                #print('EVAL: ', m, eval)

            if(eval > final_eval):
                final_eval = eval
                final_move = move
        #print('Final eval: ',final_eval, board)
        return final_eval, final_move
    else:
        N_children = get_children(board, current_player)
        for child, move in N_children:
            m, new_move = Minimize_nondet(child, move, depth-1, start, current_player, False, alpha, beta)
            if(m > maxUtility):
                maxUtility = m
                final_move = new_move
            if maxUtility >= beta:
                #print('in break')
                break

            alpha = max(maxUtility, alpha)

    return maxUtility, final_move


def Minimize_nondet(board, move, depth, start,current_player, first, alpha, beta):
    if(game_state(board)!=0  or depth==0 or (time.clock()-start)>2.5):
        #print('Eval Min: ', board, Eval(board))
        return Eval(board), move

    minUtility = float("inf")
    final_move = ''

    if(first == False):
        locs = get_empty_location_nondet(board)
        #old_board = copy.deepcopy(board)
        final_eval = float('inf')
        for i,j in locs:
            new_board = copy.deepcopy(board)
            #print('New_board min: ', new_board, i, j)
            new_board[i][j] = 'a'
            N_children = get_children(new_board, current_player)
            eval = 0
            for child, move in N_children:
                m, new_move = Maximize_nondet(child, move, depth-1, start, current_player, False, alpha, beta)
                if(m < minUtility):
                    minUtility = m
                    final_move = new_move

                if minUtility <= alpha:
                    #print('in break')
                    break

                eval += float((1/len(locs))*m)
                #print('EVAL: ', m, eval)

            if(eval < final_eval):
                final_eval = eval
                final_move = move

        #print('Final eval: ',final_eval, board)
        return final_eval, final_move

    N_children = get_children(board, current_player)
    for child, move in N_children:
        m, new_move = Maximize_nondet(child, move, depth-1, start, current_player, False, alpha, beta)
        if(m < minUtility):
            minUtility = m
            final_move = new_move

        if minUtility <= alpha:
            #print('in break')
            break

        beta = min(minUtility, beta)

    return minUtility, final_move


def get_empty_location_nondet(board):
    locs = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == ' '):
                 locs.append((i,j))
    return locs


def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''

    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    # You'll want to put in your fancy AI code here. For right now this just 
    # returns a random move.
    #print('Board: ', board)
    if(player == '+'):
        current_player = 1
    else:
        current_player = -1
    #print(merge(board, current_player))
    #children(board, current_player)
    #board = [['J', 'J', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], ['i', ' ', ' ', ' ']]
    if(deterministic == True):
        score, move = Decision(board, current_player, True)
        #print('MOVE', move, score)
        return move
    else:
        score, move = Decision_nondet(board, current_player, True)
        #print('MOVE: ', move, score)
        return move

    #yield random.choice(['U', 'D', 'L', 'R', 'S'])
    #yield random.choice(['U', 'D', 'L', 'R'])

