from random import random, randrange
from graphics import *

def getGrid():
    grid = []
    possibilites = []
    for i in range(81):
        grid.append(0)
        possibilites.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for i in range(81):
        position = -1
        for j in range(81):
            if len(possibilites[j]) > 0:
                if position == -1:
                    position = j
                elif position != -1 and len(possibilites[j]) < len(possibilites[position]):
                    position = j
                elif position != -1 and len(possibilites[j]) == len(possibilites[position]):
                    if random() < 0.1:
                        position = j
        if position > -1:
            number = possibilites[position][randrange(0, len(possibilites[position]))]
            grid[position] = number
            for y in range(position//9//3*3, (position//9//3+1)*3):
                for x in range(position%9//3*3, (position%9//3+1)*3):
                    if possibilites[y*9+x].count(number) > 0:
                        possibilites[y*9+x].remove(number)
            for j in range(9):
                if possibilites[position//9*9+j].count(number) > 0:
                    possibilites[position//9*9+j].remove(number)
                if possibilites[j*9+position%9].count(number) > 0:
                    possibilites[j*9+position%9].remove(number)
                if possibilites[position].count(j+1) > 0:
                    possibilites[position].remove(j+1)
        else:
            grid = getGrid()
            break
    return grid

def partition():
    designations = []
    for i in range(81):
        designations.append(0)
    designations[40] = 1
    if random() < 0.5:
        designations[39] = 1
        designations[41] = 1
        if random() < 0.5:
            designations[38] = 1
            designations[42] = 1
    else:
        designations[31] = 1
        designations[49] = 1
        if random() < 0.5:
            designations[22] = 1
            designations[58] = 1
    while(designations.count(0) > 0):
        focus = designations.index(0)
        grouping = []
        length = 1
        moveOn = False
        while(not moveOn):
            grouping.append(focus)
            possibilities = [False, False, False, False]

            if focus%9 != 0:
                if designations[focus-1] == 0 and grouping.count(focus-1) == 0:
                    possibilities[0] = True
            if focus//9 != 0:
                if designations[focus-9] == 0 and grouping.count(focus-9) == 0:
                    possibilities[1] = True
            if focus%9 != 8:
                if designations[focus+1] == 0 and grouping.count(focus+1) == 0:
                    possibilities[2] = True
            if designations[focus+9] == 0 and grouping.count(focus+9) == 0:
                    possibilities[3] = True

            if random() > 1.25-length/4 or possibilities.count(True) == 0:
                moveOn = True
            else:
                choice = randrange(0, possibilities.count(True))
                counter = 0
                for i in range(len(possibilities)):
                    if counter == choice and possibilities[i] == True:
                        if i == 0:
                            focus -= 1
                        elif i == 1:
                            focus -= 9
                        elif i == 2:
                            focus += 1
                        else:
                            focus += 9
                        length += 1
                        break
                    elif possibilities[i] == True:
                        counter += 1
        colorNumber = 1
        while(designations[focus] == 0):
            moveOn = True
            for i in range(len(grouping)):
                if grouping[i]%9 != 0:
                    if designations[grouping[i]-1] == colorNumber:
                        moveOn = False
                if grouping[i]//9 != 0:
                    if designations[grouping[i]-9] == colorNumber:
                        moveOn = False
                if grouping[i]%9 != 8:
                    if designations[grouping[i]+1] == colorNumber:
                        moveOn = False
                if designations[grouping[i]+9] == colorNumber:
                    moveOn = False
            if moveOn:
                for i in range(len(grouping)):
                    designations[grouping[i]] = colorNumber
                    designations[80-grouping[i]] = colorNumber
            else:
                colorNumber += 1
    return designations
            
puzzle = GraphWin("Sum Sudoku", 500, 500)
puzzle.setCoords(0, -1, 9, 9)
solution = getGrid()
grouping = partition()
singles = []
for i in range(len(grouping)):
    neighboringColor = 0
    if i%9 != 0:
        if grouping[i] == grouping[i-1]:
            neighboringColor += 1
    if i//9 != 0:
        if grouping[i] == grouping[i-9]:
            neighboringColor += 1
    if i%9 != 8:
        if grouping[i] == grouping[i+1]:
            neighboringColor += 1
    if i//9 != 8:
        if grouping[i] == grouping[i+9]:
            neighboringColor += 1
    if neighboringColor == 0:
        singles.append(i)
for i in range(len(singles)-1):
    connectingSingles = []
    for j in range(i+1, len(singles)):
        if (abs(singles[i]-singles[j]) == 1 and i%9 != 8) or abs(singles[i]-singles[j]) == 9:
            grouping[singles[i]] = 6
            grouping[singles[j]] = 6
for i in range(len(grouping)):
    box = Rectangle(Point(i%9, 9-i//9), Point(i%9+1, 8-i//9))
    if grouping[i] == 1:
        box.setFill(color_rgb(255, 0, 0))
        box.setOutline(color_rgb(255, 0, 0))
    elif grouping[i] == 2:
        box.setFill(color_rgb(0, 255, 0))
        box.setOutline(color_rgb(0, 255, 0))
    elif grouping[i] == 3:
        box.setFill(color_rgb(0, 0, 255))
        box.setOutline(color_rgb(0, 0, 255))
    elif grouping[i] == 4:
        box.setFill(color_rgb(255, 255, 0))
        box.setOutline(color_rgb(255, 255, 0))
    elif grouping[i] == 5:
        box.setFill(color_rgb(255, 0, 255))
        box.setOutline(color_rgb(255, 0, 255))
    else:
        box.setFill(color_rgb(0, 255, 255))
        box.setOutline(color_rgb(0, 255, 255))
    box.draw(puzzle)
    cornerText = True
    if i // 9 != 0:
        if grouping[i-9] == grouping[i]:
            cornerText = False
        else:
            checkL = i+1
            if checkL < 81:
                while(grouping[i] == grouping[checkL] and i//9 == checkL//9 and checkL//9 != 0):
                    if grouping[i] == grouping[checkL-9]:
                        cornerText = False
                    checkL += 1
                    if checkL >= 81:
                        break
    if cornerText and i % 9 != 0:
        if grouping[i-1] == grouping[i]:
            cornerText = False
    if cornerText:
        total = solution[i]
        inEquation = [i]
        for j in range(i+1, len(grouping)):
            if grouping[i] == grouping[j]:
                for k in range(len(inEquation)):
                    if (j == inEquation[k]+1 and i%9 <= j%9) or j == inEquation[k]+9:
                        total += solution[j]
                        inEquation.append(j)
                        if j == inEquation[k]+9:
                            goBack = j-1
                            while(grouping[j] == grouping[goBack] and goBack//9 == j//9 and inEquation.count(goBack) == 0):
                                total += solution[goBack]
                                inEquation.append(goBack)
                                goBack -= 1
                        break
        cT = Text(Point(i%9+0.15, 8.85-i//9), str(total))
        cT.setSize(8)
        cT.draw(puzzle)
for i in range(1, 3):
    line = Line(Point(i*3, 0), Point(i*3, 9))
    line.setWidth(2)
    line.draw(puzzle)
    line = Line(Point(0, i*3), Point(9, i*3))
    line.setWidth(2)
    line.draw(puzzle)
message = Text(Point(4.5, -0.5), "Click on the window to show the solution!")
message.setStyle('bold')
message.setSize(16)
message.draw(puzzle)
cursor = Rectangle(Point(0, 8), Point(1, 9))
cursor.setOutline(color_rgb(191, 191, 191))
cursor.draw(puzzle)
coords = [0, 8]
display = []
locks = []
for i in range(len(solution)):
    if random() < 0.1:
        display.append(Text(Point(i%9+0.5, 8.5-i//9), str(solution[i])))
        display[i].setStyle('bold')
        locks.append(True)
    else:
        display.append(Text(Point(i%9+0.5, 8.5-i//9), ""))
        locks.append(False)
    display[i].draw(puzzle)
solved = False
while(puzzle.checkMouse() == None and not solved):
    key = puzzle.checkKey()
    if key == "Right" and coords[0] < 8:
        cursor.move(1, 0)
        coords[0] += 1
    elif key == "Down" and coords[1] > 0:
        cursor.move(0, -1)
        coords[1] -= 1
    elif key == "Left" and coords[0] > 0:
        cursor.move(-1, 0)
        coords[0] -= 1
    elif key == "Up" and coords[1] < 8:
        cursor.move(0, 1)
        coords[1] += 1
    elif key != "0" and key.isdigit() and not locks[(8-coords[1])*9+coords[0]]:
        display[(8-coords[1])*9+coords[0]].setText(key)
        solved = True
        for i in range(len(solution)):
            if str(solution[i]) != display[i].getText():
                solved = False
    elif key == "BackSpace" and not locks[(8-coords[1])*9+coords[0]]:
        display[(8-coords[1])*9+coords[0]].setText("")
cursor.undraw()
if solved:
    message.setText("Congratulations! You solved the puzzle!")
else:
    message.setText("This is the solution!")
for i in range(len(solution)):
    display[i].setText(solution[i])
puzzle.getMouse()