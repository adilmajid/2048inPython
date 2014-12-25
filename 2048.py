#!usr/bin/python

import random
from math import log
from Tkinter import *

def run(boardRows, boardCols):
	global canvas

	boardMargin = 70
	cellSize = 100
	cellMargin = 10
	defaultValue = 0

	root = Tk()
	canvas = Canvas(root, width=((boardCols*cellSize)+2*boardMargin), height=((boardRows*cellSize)+2*boardMargin))
	root.bind("<Key>", keyPressed)
	canvas.pack()
	root.resizable(width=0, height=0)	
	
	class Struct: pass
	canvas.data = Struct()
	canvas.data.boardRows = boardRows
	canvas.data.boardCols = boardCols 
	canvas.data.boardMargin = boardMargin
	canvas.data.cellSize = cellSize
	canvas.data.cellMargin = cellMargin
	canvas.data.defaultValue = defaultValue
	canvas.data.youWin = False
	canvas.data.canvasWidth = canvas.data.boardRows*canvas.data.cellSize + 2*boardMargin
	canvas.data.canvasHeight = canvas.data.boardCols*canvas.data.cellSize + 2*boardMargin

	init()
	root.mainloop()


def init():
	board = []
	for row in range(canvas.data.boardRows):
		emptyRow = []
		for col in range(canvas.data.boardCols):
			emptyRow.append(canvas.data.defaultValue)
		board.append(emptyRow)

	canvas.data.board = board
	canvas.data.pieceColors = ["grey", "white smoke", "bisque2", "sandy brown", "chocolate", "coral", "orange red", "khaki2", "yellow", "yellow2", "gold2", "DarkGoldenRod1", "SeaGreen1", "SpringGreen3", "SpringGreen4", "CadetBlue3", "DarkGoldenRod3", "DarkOrchid3"]
	canvas.data.score = 0

	timerFired()
	redrawAll()


def redrawAll():
	canvas.delete(ALL)
	resetCombinationBoard()
	drawGame()
	drawNewPiece()


def resetCombinationBoard():
	#COMBINATION BOARD	
	#this is the board that ensures we don't run into the "combination bug"
	#the "combination bug" is when there are three or four tiles that combine at once
	#keeping track of which tiles have combined using combinationboard
	#prevents multiple combinations happening in one turn

	#for instance, consider the row: 2, 2, 4, 8
	#if the user hits "left", the correct outcome would be 4, 4, 8, 0
	#however, our program *without* combinationboard yields something different
	#for us, if the user hits left, first 2 and 2 will combine
	#the row will become 4, 0, 4, 8
	#next, 4 and 4 will combine, and the row will be 8, 0, 0, 8
	#next, 8 and 8 will combine. so without combinationboard,
	#our final results will be 16, 0, 0, 0 instead of 4, 4, 8, 0

	combinationboard = []
	for row in range(canvas.data.boardRows):
		emptyRow = []
		for col in range(canvas.data.boardCols):
			emptyRow.append(False)
		combinationboard.append(emptyRow)

	canvas.data.combinationboard = combinationboard


def drawGame():
	canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="seashell2", width=0)
	drawBoard()


def drawBoard():
	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			drawCell(canvas, row, col, canvas.data.board[row][col])
	drawScore()		


def drawScore():
	canvas.create_text(canvas.data.canvasWidth/2, canvas.data.boardMargin/2, text="Score: %r" % canvas.data.score, fill="black", font="Helvetica 30 bold")


def drawCell(canvas, row, col, cellValue):
	x0 = canvas.data.boardMargin + col*canvas.data.cellSize
	y0 = canvas.data.boardMargin + row*canvas.data.cellSize
	x1 = x0 + canvas.data.cellSize
	y1 = y0 + canvas.data.cellSize
	textColor = "black"
	if cellValue == 0:
		colorValue = 0
		cellValue = ""
	else:
		colorValue = int(log(cellValue, 2))

	if cellValue > 4:
		textColor = "white"
	
	color = canvas.data.pieceColors[colorValue]
	canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=canvas.data.cellMargin)
	canvas.create_text(x0 + canvas.data.cellSize/2, y0+canvas.data.cellSize/2, text=cellValue, fill=textColor, font="Helvetica 30 bold")


def drawNewPiece():
	newPiece()
	drawCell(canvas, canvas.data.newPositionRow, canvas.data.newPositionCol, canvas.data.board[canvas.data.newPositionRow][canvas.data.newPositionCol])


def newPiece():
	newValue = int(random.choice("248"))
	canvas.data.newPositionRow = int(random.choice("0123"))
	canvas.data.newPositionCol = int(random.choice("0123"))

	temp = canvas.data.board[canvas.data.newPositionRow][canvas.data.newPositionCol]
	canvas.data.board[canvas.data.newPositionRow][canvas.data.newPositionCol] = newValue

	if temp == 0:
		pass
	else:
		canvas.data.board[canvas.data.newPositionRow][canvas.data.newPositionCol] = temp
		if not gameOverCheck():
			count = 0
			for row in range(canvas.data.boardRows):
				for col in range(canvas.data.boardCols):
					if canvas.data.board[row][col] == canvas.data.defaultValue:
						count += 1
			if count > 0:
				newPiece()
						
		else: 
			gameOverScreen()


def moveUp():
	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			canvas.data.tempPiece = canvas.data.board[row][col]
			moveUpCheck(row, col)

	if gameOverCheck() == False:
		drawBoard()
	else:
		gameOverScreen()


def moveUpCheck(row, col):
	for i in reversed(range(row)):
		if canvas.data.board[i][col] == 0:
			canvas.data.board[i][col] = canvas.data.board[row][col]
			canvas.data.board[row][col] = 0
			if i > 0:
				moveUpCheck(i, col)
		elif canvas.data.board[i][col] == canvas.data.board[row][col]:
			if canvas.data.combinationboard[i][col] == False:
				canvas.data.combinationboard[i][col] = True
				canvas.data.board[i][col] = canvas.data.board[i][col]*2
				canvas.data.score = canvas.data.score + canvas.data.board[i][col]
				canvas.data.board[row][col] = 0
		else:
			return False


def moveLeft():
	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			canvas.data.tempPiece = canvas.data.board[row][col]
			moveLeftCheck(row, col)

	if gameOverCheck() == False:
		drawBoard()
	else:	
		gameOverScreen()


def moveLeftCheck(row, col):
	for i in reversed(range(col)):
		if canvas.data.board[row][i] == 0:
			canvas.data.board[row][i] = canvas.data.board[row][col]
			canvas.data.board[row][col] = 0
			if i > 0:
				moveLeftCheck(row, i)
		elif canvas.data.board[row][i] == canvas.data.board[row][col]:
			if canvas.data.combinationboard[row][i] == False:
				canvas.data.combinationboard[row][i] = True
				canvas.data.board[row][i] = canvas.data.board[row][i]*2
				canvas.data.score = canvas.data.score + canvas.data.board[row][i]
				canvas.data.board[row][col] = 0
		else:
			return False


def moveDown():
	for row in reversed(range(canvas.data.boardRows)):
		for col in range(canvas.data.boardCols):
			canvas.data.tempPiece = canvas.data.board[row][col]
			moveDownCheck(row, col)
	print gameOverCheck()
	if gameOverCheck() == False:
		drawBoard()
	else:	
		gameOverScreen()


def moveDownCheck(row, col):
	for i in (range(row+1, canvas.data.boardRows)):
		if canvas.data.board[i][col] == 0:
			canvas.data.board[i][col] = canvas.data.board[row][col]
			canvas.data.board[row][col] = 0
			if i < canvas.data.boardRows-1:
				moveDownCheck(i, col)
		elif canvas.data.board[i][col] == canvas.data.board[row][col]:
			if canvas.data.combinationboard[i][col] == False:
				canvas.data.combinationboard[i][col] = True	
				canvas.data.board[i][col] = canvas.data.board[i][col]*2
				canvas.data.score = canvas.data.score + canvas.data.board[i][col]
				canvas.data.board[row][col] = 0
		else:
			return False


def moveRight():
	for row in (range(canvas.data.boardRows)):
		for col in reversed(range(canvas.data.boardCols)):
			canvas.data.tempPiece = canvas.data.board[row][col]
			moveRightCheck(row, col)

	if gameOverCheck() == False:
		drawBoard()
	else:	
		gameOverScreen()


def moveRightCheck(row, col):
	for i in (range(col+1, canvas.data.boardCols)):
		if canvas.data.board[row][i] == 0:
			canvas.data.board[row][i] = canvas.data.board[row][col]
			canvas.data.board[row][col] = 0
			if i < canvas.data.boardCols-1:
				moveRightCheck(row, i)
		elif canvas.data.board[row][i] == canvas.data.board[row][col]:
			if canvas.data.combinationboard[row][i] == False:
				canvas.data.combinationboard[row][i] = True	
				canvas.data.board[row][i] = canvas.data.board[row][i]*2
				canvas.data.score = canvas.data.score + canvas.data.board[i][col]
				canvas.data.board[row][col] = 0
		else:
			return False


def gameOverCheck():
	#if the gameOverCheck returns False, the game is not over
	#if returns True, the game is over

	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			if canvas.data.board[row][col] >= 131072:
				return True

	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			if canvas.data.board[row][col] == canvas.data.defaultValue:
				return False

	for row in range(canvas.data.boardRows):
		for col in range(canvas.data.boardCols):
			if upDownLeftRightCheck(row, col) == False:
				return False

	return True


def upDownLeftRightCheck(row, col):
	#returns True if the piece can not move (game MAY be over)
	#returns False is the piece CAN move, which means the game is definitely not over
	if row != 0:
		if canvas.data.board[row][col] == canvas.data.board[row-1][col]:
			return False
	if col != 0 :
		if canvas.data.board[row][col] == canvas.data.board[row][col-1]:
			return False
	if row < (canvas.data.boardRows-1):
		if canvas.data.board[row][col] == canvas.data.board[row+1][col]:
			return False
	if col < (canvas.data.boardCols-1):	
		if canvas.data.board[row][col] == canvas.data.board[row][col+1]:
			return False
	
	return True
	

def gameOverScreen():
	canvas.create_rectangle(0, 0, canvas.data.canvasWidth, canvas.data.canvasHeight, fill="seashell2", width=0)
	canvas.create_text(canvas.data.canvasWidth/2, canvas.data.canvasHeight/2, text="GAME OVER\nYOUR SCORE: %r\nPRESS 'R' TO PLAY AGAIN." % canvas.data.score, fill="black", font="Helvetica 30 bold")


def timerFired():
	if gameOverCheck():
		gameOverScreen()
	else:
		canvas.after(100,timerFired)


def keyPressed(event):
	if not gameOverCheck():
		if event.keysym == "Up":
			moveUp()
			redrawAll()

		if event.keysym == "Down":
			moveDown()
			redrawAll()

		if event.keysym == "Left": 	
			moveLeft()
			redrawAll()

		if event.keysym == "Right": 	
			moveRight()
			redrawAll()

	if event.char == "r":
		init()

run(4, 4)