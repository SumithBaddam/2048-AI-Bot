#!/usr/local/bin/python3


import random
import copy

class InvalidMoveException(Exception):
    pass

class GameFullException(Exception):
    pass

'''Gives an object of Game_IJK with initial empty game and first player as uppercase
'''
def initialGame(size = 4, player = '+', deterministic = True):
    game = [[' ' for _ in range(size)]for _ in range(size)]
    game[0][0] = 'A' if player == '+' else 'a'
    return Game_IJK(game, player, deterministic)

class Game_IJK:
    def __init__(self, game, currentPlayer, deterministic):
        self.__game = game
        self.__current_player = +1 if currentPlayer == '+' else -1
        self.__previous_game = self.__game
        self.__new_piece_loc = (0,0)
        self.__deterministic = deterministic

    def __switch(self):
        self.__current_player = -self.__current_player
    
    def __game_state(self,mat):
        zeros = 0
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 'K':
                    return '+'
                if mat[i][j] == 'k':
                    return '-'
                if mat[i][j] == '':
                    zeros += 1
#        if zeros == 0 and self.__previous_game == self.__game:
#            raise GameFullException
        return 0

    def __reverse(self,mat):
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat[0])):
                new[i].append(mat[i][len(mat[0])-j-1])
        return new
    
    def __transpose(self,mat):
        new = []
        for i in range(len(mat[0])):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[j][i])
        return new
    
    def __cover_up(self,mat):
        new = [[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' '],[' ',' ',' ',' ']]
        done = False
        for i in range(4):
            count = 0
            for j in range(4):
                if mat[i][j] != ' ':
                    new[i][count] = mat[i][j]
                    if j != count:
                        done = True
                    count += 1
        return (new, done)
    
    def __merge(self,mat):
        global current_player

        done = False
        for i in range(4):
            for j in range(3):
                if mat[i][j] == mat[i][j+1] and mat[i][j] != ' ':
                    mat[i][j] = chr(ord(mat[i][j])+ 1)
                    mat[i][j+1] = ' '
                    done = True
                elif mat[i][j].upper() == mat[i][j+1].upper() and mat[i][j] != ' ':
                    mat[i][j] = chr(ord(mat[i][j])+ 1)
                    mat[i][j] = mat[i][j].upper() if self.__current_player > 0 else mat[i][j].lower()
                    mat[i][j+1] = ' '
                    done = True
        return (mat, done)
    
    def __up(self,game):
        #print("up")
        # return matrix after shifting up
        game = self.__transpose(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(game)
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)
    
    def __down(self,game):
        #print("down")
        game = self.__reverse(self.__transpose(game))
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__transpose(self.__reverse(game))
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)
    
    def __left(self,game):
        #print("left")
        # return matrix after shifting left
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)
    
    def __right(self,game):
        #print("right")
        # return matrix after shifting right
        game = self.__reverse(game)
        game, done = self.__cover_up(game)
        temp = self.__merge(game)
        game = temp[0]
        done = done or temp[1]
        game = self.__cover_up(game)[0]
        game = self.__reverse(game)
        if done == True:
            self.__game = copy.deepcopy(game)
        return (game, done)
    
    def __skip(self):
        x, y = self.__new_piece_loc
        self.__game[x][y] = self.__game[x][y].swapcase()
    '''
    Expose this method to client to print the current state of the board
    '''
    def printGame(self):
        str_game = [['______' for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                str_game[i][j] = "_"+self.__game[i][j]+"_"
        
        for i in range(4):
            print("|".join(str_game[i]))
        print("\n")

    def __add_piece(self):
        if self.__deterministic:
            for i in range(4):
                for j in range(4):
                    if self.__game[i][j] == ' ':
                        self.__game[i][j] = 'A' if self.__current_player>0 else 'a'
                        self.__new_piece_loc = (i,j)
                        return
        else:
            open=[]
            for i in range(4):
                for j in range(4):
                    if self.__game[i][j] == ' ':
                        open += [(i,j),]

            if len(open) > 0:
                r = random.choice(open)
                self.__game[r[0]][r[1]] = 'A' if self.__current_player>0 else 'a'

                
    def makeMove(self,move):
        if move not in ['U','L','D','R','S']:
            raise InvalidMoveException

        self.__previous_game = self.__game
        if move == 'L':
            self.__left(self.__game)
        if move == 'R':
            self.__right(self.__game)
        if move == 'D':
            self.__down(self.__game)
        if move == 'U':
            self.__up(self.__game)
        if move == 'S':
            self.__skip()
        
        '''
        Switch player after the move is done
        '''
        self.__switch()
        if move != 'S':
            self.__add_piece()
        #self.printGame()
        
        return copy.deepcopy(self)

    def getDeterministic(self):
        return self.__deterministic
    
    def getGame(self):
        return copy.deepcopy(self.__game)
    
    '''player who will make the next move'''
    def getCurrentPlayer(self):
        return '+' if self.__current_player > 0 else '-'

    ''' '+' : '+' has won
       '-1' : '-' has won
       '' : Game is still on
    '''
    def state(self):
        return self.__game_state(self.__game)
    