import os
import time
import msvcrt
import copy
import sys
import math
import random

def printBoard(board):

    print("\033[H", end="")

    for row in board:
        print("".join(row))


def checkCollision(ballPos, ballSpeed, player1Pos, player2Pos):

    ballRadius = len(ball) // 2

    print(ballSpeed)
    """
    Checks if ball is at player X location
    First check is for left player, second for right. Adds 
    """
    if (
        player1Pos[0] - ballSpeed[0] <= ballPos[0] <= player1Pos[0]
        or player2Pos[0] - ballRadius <= ballPos[0] <= player2Pos[0] - ballSpeed[0]
    ):

        # Checks if ball is at player Y location
        # Get middlepoint of playerPos
        player1MidPos = (player1Pos[1] + player1Pos[1] + 1) / 2
        player2MidPos = (player2Pos[1] + player2Pos[1] + 1) / 2

        print(player1MidPos, player2MidPos, ballPos[1])

        if (
            ballSpeed[0] > 0 and (player1MidPos - 2 <= ballPos[1] <= player1MidPos + 1)
        ) or (
            ballSpeed[0] < 0 and (player2MidPos - 2 <= ballPos[1] <= player2MidPos + 1)
        ):
            
            ballSpeed[0] *= -1
            ballSpeed[2] = min(ballSpeed[2] * ballSpeedMulti, maxSpeed)

            if ballSpeed[0] < 0:
                diff = player1MidPos - ballPos[1] - 0.5
                ballSpeed[1] = diff / 50 + random.randrange(-1, 1)/1000
            elif ballSpeed[0] > 0:
                diff = player2MidPos - ballPos[1] - 0.5
                ballSpeed[1] = diff / 50 + random.randrange(-1, 1)/1000



    # If ball hits border, reverse Y speed
    if ballPos[1] + 1 >= 19 or ballPos[1] <= 1:
        ballSpeed[1] *= -1


    # For testing bounce from right wall
    if ballPos[0] > 99:
        ballSpeed[0] *= -1

def insertObjects(board, ballPos, player1Pos, player2Pos):

    tempBoard = copy.deepcopy(board)
    for i in range(playerLen):
        tempBoard[round(player1Pos[1]) + i][round(player1Pos[0])] = "┃"
        tempBoard[round(player2Pos[1]) + i][round(player2Pos[0])] = "┃"


    for i, row in enumerate(ball):
        ballPosY = round(ballPos[1]) + i
        if 1 <= ballPosY <= 19:
            for j, item in enumerate(row):
                ballPosX = round(ballPos[0]) + j

                if 1 <= ballPosX <= 99:
                    tempBoard[ballPosY][ballPosX] = item

    return tempBoard

def normalizeVelocity(speed):
    # Calculate the magnitude of the velocity vector
    magnitude = math.sqrt(speed[0]**2 + speed[1]**2)

    # Avoid division by zero
    if magnitude == 0:
        return [0, 0]

    # Normalize the vector and scale it to the desired speed
    normalized_x = speed[0] / magnitude
    normalized_y = speed[1] / magnitude

    return [normalized_x * speed[2], normalized_y * speed[2], speed[2]]

def startGame(board):

    halfHeightBoard = len(board) // 2 - 1

    player1Pos = [playerDistanceBorder, halfHeightBoard]
    player2Pos = [len(board[0]) - playerDistanceBorder - 1, halfHeightBoard]
    ballPos = [playerDistanceBorder + ballDistanceFromPlayer, halfHeightBoard]

    ballSpeed = [1, 0, 0.05]

    while True:
        time.sleep(1 / FRAMERATE)

        if msvcrt.kbhit():
            key = msvcrt.getch()

            try:
                key = key.decode("utf-8")
            except Exception as e:
                continue

            if key == "w":
                if player1Pos[1] - 1 > 0:
                    player1Pos[1] -= playerSpeed
            elif key == "s":
                if player1Pos[1] + 1 < len(board) - 2:
                    player1Pos[1] += playerSpeed

        ballPos[0] -= ballSpeed[0] / FRAMERATE

        checkCollision(ballPos, ballSpeed, player1Pos, player2Pos)
        
        ballSpeed = normalizeVelocity(ballSpeed)
        ballPos[0] -= ballSpeed[0]
        ballPos[1] -= ballSpeed[1]
        
        tempBoard = insertObjects(board, ballPos, player1Pos, player2Pos)
        printBoard(tempBoard)


def drawCircle(board):
    rows, cols = len(board), len(board[0])
    cx = len(board[0]) // 2 - 1
    cy = len(board) // 2

    for y in range(rows):
        for x in range(cols):
            # Check if the point (x, y) is approximately on the circle
            if abs((x - cx)**2 + (y - cy)**2 - 3**2) < 3:  # Allow some tolerance
                
                # Increase X based on distance to center to have a rounder circle
                new_x = round((abs(cx - x) * 2) + cx) 

                board[y][new_x] = '*'
                board[y][cx-(new_x-cx)] = '*'
                
    
def initBoard(rows=20, cols=100):
    board = [[" " for _ in range(cols)] for _ in range(rows)]

    drawCircle(board)

    for col in range(cols):
        if col == 0:
            board[0][col] = "┏"
            board[rows - 1][col] = "┗"
        elif col == cols // 2 - 1:
            board[0][col] = "┳"
            board[rows - 1][col] = "┻"
        elif col == cols - 1:
            board[0][col] = "┓"
            board[rows - 1][col] = "┛"
        else:
            board[0][col] = "━"
            board[rows - 1][col] = "━"

    for row in range(1, rows - 1):
        board[row][0] = "|"
        board[row][cols // 2 - 1] = "┃"
        board[row][cols - 1] = "|"

    return board


def main():
    print("Welcome to Pong!")

    board = initBoard()
    printBoard(board)

    startGame(board)


if __name__ == "__main__":

    os.system("cls" if os.name == "nt" else "clear")

    print("\033[?25l")  # Hide cursor

    FRAMERATE = 1000

    playerDistanceBorder = 3
    playerLen = 2
    playerSpeed = 1

    ballDistanceFromPlayer = 30
    ballSpeedMulti = 1.08
    maxSpeed = 0.3
    ball = [["┏", "━", "┓"], ["┗", "━", "┛"]]

    main()
