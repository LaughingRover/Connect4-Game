import sys
from termcolor import colored, cprint

# The draw_field function will print the game field
# We will put our current field into the draw_field


def draw_field(field):
    # Takes the currentField input and uses it to display the playing field
    """
              0111111
    01234567891123456
      1 2 3 4 5 6 7
    -----------------0  1
    | 0 0 0 0 0 0 0 |1  2
    | 0 0 0 0 0 0 0 |2  3
    | 0 0 0 0 0 0 0 |3  4
    | 0 0 0 0 0 0 0 |4  5
    | 0 0 0 0 0 0 0 |5  6
    | 0 0 0 0 0 0 0 |6  7
    -----------------7  8
    """
    count = 1
    for row in range(8):
        if row == 0:
            print("  1 2 3 4 5 6 7  \n-----------------")
        elif row == 7:
            print("-----------------")
        elif row != 0 or row != 7:
            for column in range(17):
                if column == 0 or column == 16:
                    print("|", end='')
                    if column == 16:
                        print('')
                elif column % 2 == 0:
                    # The even columns are where our moves are made
                    # To map our current field to our draw field, we divide by 2
                    # 2->1, 4->2, 6->3, 8->4, 10->5, 12->6, 14->7
                    activeColumn = int(column/2) - 1
                    activeRow = int(row) - 1
                    print(field[activeColumn][activeRow], end='')
                else:
                    print(" ", end='')
            count += 1


def players_move(cplayer):
    """
    Collects and returns the valid input of a player
    """
    while True:
        try:
            column = int(
                input(cplayer + " enter a column number \n>>> ")) - 1
            if column < 0:
                print("Out of range! Pick a column between 1 - 7")
            elif column >= 0 and column < 7:
                return column
        except IndexError:
            print("Out of range, pick a column between 1 - 7")
        except ValueError:
            print("There is no such column!")


def column_checker(field, column, player_num):
    """
    Can also be known as _get_color function
    Checks each column of the field(list) from the last item to see if
    It is empty(white) and returns False if it's not.
    """
    white = '\x1b[37m⬤\x1b[0m'

    for i in reversed(range(6)):
        if field[column][i] == white:
            # Value returned is a tuple
            return column, i
        elif i == 0 and field[column][i] != white:
            # i is the top of the column, if it has hit the top and the
            # color is not white then that column is full
            print("Column " + str(column+1) + " is full!")
            return False


def make_move(verifiedMove, field):
    """
    Takes the value return by the column checker and makes a move
    """

    def chip(player_num):
        """
        Different colored chip for players
        """
        chip1 = colored(u'\u2B24', 'red')
        chip2 = colored(u'\u2B24', 'green')
        if player_num == 1:
            chip = chip1
        else:
            chip = chip2
        return chip

    column = verifiedMove[0]
    row = verifiedMove[1]
    field[column][row] = chip(player_num)


player_num = 1
currentField = [
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m'],
    ['\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m',
        '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m', '\x1b[37m⬤\x1b[0m']
]


def check_for_win(coordinates):
    """
    From the position of where a move is made, checking for win is done
    in 7 different directions simultaneously
    """
    # global currentField
    # board_map = currentField[:]
    column = coordinates[0]
    row = coordinates[1]

    def diagonalCheck(column, row):
        """
        Checks the game field for where the diagonal checks will start from
        """
        ColStartUp = column - (5 - row)
        RowStartUp = row + column
        if ColStartUp < 0:
            ColStartUp = 0
        if RowStartUp > 5:
            RowStartUp = 5
        diagUp = (ColStartUp, RowStartUp)

        ColStartDown = column - row
        RowStartDown = row - column
        if ColStartDown < 0:
            ColStartDown = 0
        if RowStartDown < 0:
            RowStartDown = 0
        diagDown = (ColStartDown, RowStartDown)

        return [diagUp, diagDown]

    diag_coord = diagonalCheck(column, row)

    def diagonalUp():
        diagColStartUP = diag_coord[0][0]
        diagRowStartUp = diag_coord[0][1]
        diagUp = ""

        for value in currentField[diagColStartUP][diagRowStartUp]:
            if diagColStartUP > 6 or diagRowStartUp < 0:
                break
            diagUp += currentField[diagColStartUP][diagRowStartUp]
            diagColStartUP += 1
            diagRowStartUp -= 1
        return diagUp

    def diagonalDown():
        diagColStartDown = diag_coord[1][0]
        diagRowStartDown = diag_coord[1][1]
        diagDown = ""

        for value in currentField[diagColStartDown][diagRowStartDown]:
            if diagColStartDown > 6 or diagRowStartDown > 5:
                break
            diagDown += currentField[diagColStartDown][diagRowStartDown]
            diagColStartDown += 1
            diagRowStartDown += 1
        return diagDown

    def verticalCheck():
        vertical = ""
        for value in currentField[column]:
            vertical += value
        return vertical

    def horizontalCheck():
        horizontal = ""
        for value in currentField:
            for i in value[row]:
                horizontal += i
        return horizontal

    # print("Diagonal Up: ", diagonalUp())
    # print("Diagonal down: ", diagonalDown())
    # print("Vertical: ", verticalCheck())
    # print("Horizontal: ", horizontalCheck())

    red = '\x1b[31m⬤\x1b[0m'*4
    green = '\x1b[32m⬤\x1b[0m'*4
    tests = (red, green)

    if any(x in verticalCheck() for x in tests):
        return(True)
    elif any(x in horizontalCheck() for x in tests):
        return(True)
    elif any(x in diagonalUp() for x in tests):
        return(True)
    elif any(x in diagonalDown() for x in tests):
        return(True)


def game_loop():
    print(""""
    --------------CONNECT4-------------
    . Choose a column to make a move
    . Get four in a row to win
    . Have fun!

    Enter ctrl+z at any time to exit
    """)

    draw_field(currentField)
    global player_num

    while True:
        try:
            if player_num == 1:
                cplayer = colored('\nPlayer ' + str(player_num), 'red')
            else:
                cplayer = colored('\nPlayer ' + str(player_num), 'green')

            verifiedColumn = players_move(cplayer)
            verifiedMove = column_checker(
                currentField, verifiedColumn, player_num)

            if verifiedMove == False:
                continue
            else:
                make_move(verifiedMove, currentField)
                draw_field(currentField)
                if check_for_win(verifiedMove) == True:
                    print('Player ' + str(player_num), 'wins')
                    break
                if player_num == 1:
                    player_num += 1
                elif player_num == 2:
                    player_num -= 1
        except EOFError:
            print("Game exited :(")
            break


game_loop()
