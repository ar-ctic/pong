import os
import time
import msvcrt  
import copy
import sys


def printBoard(board):
    
    
    print("\033[H", end="")  

    for row in board:
        print("".join(row))



def insertObjects(board, ballPos, player1Pos, player2Pos):
    
    tempBoard = copy.deepcopy(board)
    for i in range(playerLen):
        tempBoard[player1Pos[1]+i][player1Pos[0]] = '┃'
        tempBoard[player2Pos[1]+i][player2Pos[0]] = '┃'

    for i, row in enumerate(ball):
        for j, item in enumerate(row):
            tempBoard[ballPos[1]+i][ballPos[0]+j] = item

    return tempBoard


def startGame(board):
    
    halfHeightBoard = len(board)//2 - 1
    
    player1Pos = [playerDistanceBorder, halfHeightBoard]
    player2Pos = [len(board[0]) - playerDistanceBorder - 1, halfHeightBoard]
    ballPos = [playerDistanceBorder + ballDistanceFromPlayer, halfHeightBoard]
    
    while True:
        time.sleep(0.1)
        
        if msvcrt.kbhit():  
            key = msvcrt.getch() 
            
            try: 
                key = key.decode('utf-8') 
            except Exception as e:
                continue
            
            if key == 'w':
                if player1Pos[1]-1 > 0:
                    player1Pos[1] -= 1
            elif key == 's':
                if player1Pos[1]+1 < len(board)- 2:
                    player1Pos[1] += 1

        tempBoard = insertObjects(board, ballPos, player1Pos, player2Pos)
        printBoard(tempBoard)


def initBoard(rows = 20, cols = 100):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]

    for col in range(cols):
        if col == 0:
            board[0][col] = '┏'  
            board[rows - 1][col] = '┗'  
        elif col == cols // 2 - 1:
            board[0][col] = '┳'  
            board[rows - 1][col] = '┻' 
        elif col == cols - 1:
            board[0][col] = '┓'  
            board[rows - 1][col] = '┛'  
        else:
            board[0][col] = '━'  
            board[rows - 1][col] = '━'  
    
    
    for row in range(1, rows - 1):
        board[row][0] = '┃'  
        board[row][cols // 2 - 1] = '┃'  
        board[row][cols - 1] = '┃'  
    
    return board

def main():
    print("Welcome to Pong!")
    
    board = initBoard()
    printBoard(board)
    
    startGame(board)
     
    
if __name__ == '__main__':
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('\033[?25l') # Hide cursor
    
    playerDistanceBorder = 3
    ballDistanceFromPlayer = 30
    playerLen = 2
    
    ball = [['┏', '━', '┓'],
            ['┗', '━', '┛']]

    main()