import os
import time
import msvcrt
import copy
import math
import random
import pyfiglet

def printBoard(board, score = [0, 0]):

    print("\033[H", end="")

    distanceFromLeft = [' ' for _ in range(len(board[0])//2 - 10)]
        
    displayScore = pyfiglet.figlet_format(f"{"".join(distanceFromLeft)}{score[0]} : {score[1]}        ")
    
    print(displayScore)
    
    for row in board:
        print("".join(row))


def isBallBetweenPaddle(ballPos, ballPast, player1Pos, player2Pos):
    if ballPos[0] <= player1Pos[0] <= ballPast[0] or ballPast[0] <= player2Pos[0] <= ballPos[0] + 1:
        return True
    return False

def isOnPaddleY(ballPosition, playerPos):
    if (playerPos[1] - 0.5 <= ballPosition <= playerPos[1] + 1.5 or playerPos[1] - 0.5 <= ballPosition + 1 <= playerPos[1] + 1.5):
        return True
    return False

def xDistancePlayerBall(ballPos, player1Pos, player2Pos):
    if ballPos[0] <= player1Pos[0]:
        distanceToPlayer = player1Pos[0] - ballPos[0]
    else:
        distanceToPlayer = player2Pos[0] - ballPos[0]

    return distanceToPlayer

def modifyBallSpeed(ballSpeed, ballPos, player1Pos, player2Pos):
    # Paddle middle position used for ball Y speed
    player1MidPos = (player1Pos[1] + player1Pos[1] + 1) / 2
    player2MidPos = (player2Pos[1] + player2Pos[1] + 1) / 2
    
    # Reverse speed of ball (bounce)
    ballSpeed[0] *= -1
    ballSpeed[2] = min(ballSpeed[2] * ballSpeedMulti, ballMaxSpeed)
    
    
    # Give ball Y speed based on distance to paddle Mid Position
    if ballSpeed[0] < 0:
        diff = player1MidPos - ballPos[1] - 0.5
        ballSpeed[1] = 10 * diff + random.randrange(-1, 1) / 50
    elif ballSpeed[0] > 0:
        diff = player2MidPos - ballPos[1] - 0.5
        ballSpeed[1] = 10 * diff + random.randrange(-1, 1) / 50


def checkCollision(board, ballPos, ballSpeed, player1Pos, player2Pos):
    """
    TODO: Use helper functions to organize
    
    Checks if ball collides with border or paddle and handles ball velocity accordingly
    
    @params {list} ballPos: X Y of ball at [0][0] 
    @params {list} ballSpeed: X Y speed of ball
    @params {list} player1Pos: X Y position of player1 at [0][0]
    @params {list} player2Pos: X Y position of player2 at [0][0]
    """

    # If ball touches top/bot border reverse Y speed
    if ballPos[1] + 1 >= len(board) - 1 or ballPos[1] <= 0:
        ballSpeed[1] *= -1
        

    # Get ball location 1. tick before
    ballPast = [ballPos[0] + ballSpeed[0] * deltaTime, ballPos[1] + ballSpeed[1] * deltaTime]

    # Get vector from old to new ball
    vectorBall = [ballPos[0] - ballPast[0], ballPos[1] - ballPast[1]]

    # Calculate slope 
    if vectorBall[0] != 0:
        slopeVectorBall = vectorBall[1]/vectorBall[0]
    else:
        slopeVectorBall = 0
        
        
    # If paddle is at/between past and new ball X location
    if isBallBetweenPaddle(ballPos, ballPast, player1Pos, player2Pos):
        
        # Distance to either player1 or player2 (left, right)
        distanceToPlayer = xDistancePlayerBall(ballPos, player1Pos, player2Pos)
        
        # ball Y position if it was at exactly the paddle location
        ballPosition = ballPos[1] + (distanceToPlayer * slopeVectorBall)

        # Check for Y location
        if isOnPaddleY(ballPosition, player1Pos) and ballSpeed[0] > 0:
            
            modifyBallSpeed(ballSpeed, ballPos, player1Pos, player2Pos)
        elif isOnPaddleY(ballPosition, player2Pos) and ballSpeed[0] < 0:
           modifyBallSpeed(ballSpeed, ballPos, player1Pos, player2Pos)
       
def hasBallScored(board, ballPos, score):

    if ballPos[0] < 0:
        score[0] += 1
        return True
    elif ballPos[0] > len(board[0]):
        score[1] += 1   
        return True

    return False

def insertObjects(board, ballPos, player1Pos, player2Pos):
    """
    Inserts ball, player paddles into board. Using deepcopy to not change mutable board
    
    @params {list} board: 2D list of gameboard
    @params {list} ballPos: X Y of ball at [0][o]
    @params {list} player1Pos: X Y of player1 at [0][o]
    @params {list} player2Pos: X Y of player2 at [0][o]
    
    @returns {list} tempBoard: 2D list of temporary board with object
    """

    # Deepcopy so Lists inside List are also copied without reference
    tempBoard = copy.deepcopy(board)
    
    # Insert player paddles
    for i in range(playerLen):
        tempBoard[round(player1Pos[1]) + i][round(player1Pos[0])] = "┃"
        tempBoard[round(player2Pos[1]) + i][round(player2Pos[0])] = "┃"

    # Insert ball
    for i, row in enumerate(ball):
        ballPosY = round(ballPos[1]) + i
        if 1 <= ballPosY <= len(board) - 1:
            for j, item in enumerate(row):
                ballPosX = round(ballPos[0]) + j

                if 1 <= ballPosX <= len(board[0]) - 1:
                    tempBoard[ballPosY][ballPosX] = item

    return tempBoard


def normalizeVelocity(speed):
    """
    To avoid faster ball when going diagonal use normalization
    """
    # Calculate the magnitude of the velocity vector
    magnitude = math.sqrt(speed[0] ** 2 + speed[1] ** 2)

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

    # [X speed, Y speed, normalized Speed (30 [] per second)
    ballSpeed = [ballStartDirection, 0, ballNormalizedSpeed]
    
    # Score [player1, player2]
    score = [0, 0]
    moveUp = moveDown = False

    # Gameloop
    while True:
        time.sleep(deltaTime)

        # Check for keypress
        if msvcrt.kbhit():
            key = msvcrt.getch()

            try:
                key = key.decode("utf-8")
            except Exception as e:
                continue

            if key == "w":
                moveUp = True
            elif key == "s":
                moveDown = True

        else:

            if moveUp:
                moveUp = False
            if moveDown:
                moveDown = False

        if moveUp and player1Pos[1] - playerSpeed > 0:
            player1Pos[1] -= playerSpeed
        if moveDown and player1Pos[1] + playerSpeed < len(board) - 2:
            player1Pos[1] += playerSpeed


        # Computer paddle (player2 -> player on right side) 
        if ballPos[1] < player2Pos[1]:
            if player2Pos[1] - 1 > 0:
                player2Pos[1] -= 10 * playerSpeed * deltaTime
        elif ballPos[1] > player2Pos[1]:
            if player2Pos[1] + 1 < len(board) - 2:
                player2Pos[1] += 10 * playerSpeed * deltaTime

        hasScored = hasBallScored(board, ballPos, score)
        
        if hasScored:
            ballSpeed = [ballStartDirection, 0, ballNormalizedSpeed]
            ballPos = [playerDistanceBorder + ballDistanceFromPlayer, halfHeightBoard]
            continue
        
        checkCollision(board, ballPos, ballSpeed, player1Pos, player2Pos)

        ballSpeed = normalizeVelocity(ballSpeed)
        ballPos[0] -= ballSpeed[0] * deltaTime
        ballPos[1] -= ballSpeed[1] * deltaTime

        tempBoard = insertObjects(board, ballPos, player1Pos, player2Pos)
        printBoard(tempBoard, score)


def drawCircle(board):
    rows, cols = len(board), len(board[0])
    cx = len(board[0]) // 2 - 1
    cy = len(board) // 2

    for y in range(rows):
        for x in range(cols):
            # Check if the point (x, y) is approximately on the circle
            if abs((x - cx) ** 2 + (y - cy) ** 2 - 3**2) < 3:  # Allow some tolerance

                # Increase X based on distance to center to have a rounder circle
                new_x = round((abs(cx - x) * 2) + cx)

                board[y][new_x] = "*"
                board[y][cx - (new_x - cx)] = "*"


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

    os.system("cls" if os.name == "nt" else "clear") # Clears terminal

    print("\033[?25l")  # Hide cursor

    FRAMERATE = 144
    deltaTime = 1/FRAMERATE
    
    playerDistanceBorder = 3
    playerLen = 2
    playerSpeed = 1

    ballDistanceFromPlayer = 30
    ballStartDirection = 1
    ballNormalizedSpeed = 30
    ballSpeedMulti = 1.08
    ballMaxSpeed = 100
    ball = [["┏", "━", "┓"], ["┗", "━", "┛"]]

    main()
