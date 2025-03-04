COLUMNS = 10
ROWS = 10


def print_matrix(matrix):
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            value = row[j]
            print(value, end=" ")
        print()


def generate_board(rows, columns):
    board = []
    for row in range(rows):
        temp = []
        if row == 0 or row == rows - 1:
            temp = ['w' for _ in range(columns)]
        else:
            for column in range(columns):
                if column == 0 or column == columns - 1:
                    temp.append('w')
                else:
                    temp.append('-')
        board.append(temp)
    return board


def draw_player(board, p_x, p_y):
    board[p_x][p_y] = 'o'
    return board


def main():
    board = generate_board(ROWS, COLUMNS)
    player_x = 1
    player_y = 1
    print_matrix(board)
    board = draw_player(board, player_x, player_y)
    print_matrix(board)


if __name__ == "__main__":
    main()
