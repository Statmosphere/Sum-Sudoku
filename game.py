from random import random, randrange

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
            
solution = getGrid()
for i in range(9):
    if i % 3 == 0:
        print("- - - - - - - - - - - - -")
    print("| " + str(solution[i*9]) + " " + str(solution[i*9+1]) + " " + str(solution[i*9+2]) + " | " + str(solution[i*9+3]) + " " + str(solution[i*9+4]) + " " + str(solution[i*9+5]) + " | " + str(solution[i*9+6]) + " " + str(solution[i*9+7]) + " " + str(solution[i*9+8]) + " |")