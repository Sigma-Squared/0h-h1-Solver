import pygame
BLACK = 0
RED = 1
BLUE = 2
COLORS = (0x000000, 0xC24B31, 0x35B8D5)


def main(sz=10):
    pygame.init()
    running = True
    cell = 64
    screen = pygame.display.set_mode((sz * cell, sz * cell))
    pygame.display.set_caption(
        "0h h1 (press SPACE to solve and mouse to input)")
    board = [[0] * sz for i in range(sz)]

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    yloc = event.pos[1] / cell
                    xloc = event.pos[0] / cell
                    board[yloc][xloc] = (board[yloc][xloc] + 1) % 3
                    refresh(screen, board)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        board = solve(board, sz)
                        refresh(screen, board)
                    if event.key == pygame.K_r:
                        for y in range(len(board)):
                            for x in range(len(board[y])):
                                board[y][x] = 0
                        refresh(screen, board)
        except:
            pygame.quit()
            running = False
            raise

#refreshes the screen
def refresh(surface, m):
    surface.fill(COLORS[BLACK])
    draw_board(surface, m)
    pygame.display.flip()

#function purely for drawing the board on the screen, no manipulations here
def draw_board(surface, m):
    inf = pygame.display.Info()
    w = inf.current_w
    step = w / len(m)
    for y, row in enumerate(m):
        for x, item in enumerate(row):
            surface.fill(
                COLORS[item], (x * step, y * step, (x + 1) * step, (y + 1) * step))

#returns the opposite of a color (RED->BLUE, BLUE->RED)
def inv(col):
    if col is RED:
        return BLUE
    if col is BLUE:
        return RED
    return BLACK

#returns a transpose copy of a matrix
def transpose(matrix):
    return map(list, zip(*matrix))

#the following three functions are functions for solving the 
#board according to the three rules of ohh1. Each function
#solves each rule seperately.

#this function solves the rule "no three of the same color next to each other"
def solveThrees(M):
    #all three functions work primarily by defining a _matrixprocess
    #subfunction which does all the algorithmic work and actually
    #solves the matrix, returning the original matrix solved for
    #the particular rule.
    def _matrixprocess(m):
        for y, row in enumerate(m):
            for pos in range(len(row) - 1):
                if (row[pos] != 0):
                    if row[pos + 1] == row[pos]:
                        ncol = inv(row[pos])
                        try:
                            m[y][pos + 2] = ncol
                        except:
                            pass
                        try:
                            if (pos - 1) >= 0:
                                m[y][pos - 1] = ncol
                        except:
                            pass
                    if (pos + 2) < len(row):
                        if row[pos + 2] == row[pos]:
                            ncol = inv(row[pos])
                            m[y][pos + 1] = ncol
        return m

    #it then performs the _matrixprocess subfunction on the given matrix.
    #however the _matrixprocess function only solves for the rule on the
    #rows of the matrix. To solve for both rows and columns, the matrix
    #is transposed, and then _matrixprocess function is run again for the
    #transposed matrix, essentially solving for columns. The matrix
    #is then transposed again to return it to it's original transposition
    #and returned
    first_pass = _matrixprocess(M)
    second_pass = _matrixprocess(transpose(first_pass))

    return transpose(second_pass)

#the other functions follow the exact same pattern. The only thing that changes
#is the actualy _matrixprocess function for solving the rule (for rows only).

#this function is for the rule "all rows and columns must have the same # of
#reds and blues"
def solveHalves(M, sz):
    def _matrixprocess(m):
        for y, row in enumerate(m):
            if row.count(RED) >= (sz / 2):
                m[y] = [ (BLUE if i is BLACK else i) for i in row]
            elif row.count(BLUE) >= (sz / 2):
                m[y] = [ (RED if i is BLACK else i) for i in row]
        return m

    first_pass = _matrixprocess(M)
    second_pass = _matrixprocess(transpose(first_pass))
    return transpose(second_pass)

#this function is for rule "no rows or columns can be duplicates of each
#other"
def solveDuplicates(M):
    #this one has a slightly different structure, as it uses a helper
    #function. the _similarity function returns whether two rows have
    #the same nonblack blocks.
    def _similarity(r1, r2):
        r2_s = list(r2)
        for i, e in enumerate(r1):
            if (e == BLACK):
                r2_s[i] = BLACK
        return (r2_s == r1)

    def _matrixprocess(m):
        dup_list = []
        for y1, row1 in enumerate(m):
            for y2, row2 in enumerate(m):
                if _similarity(row1, row2) and (y1 != y2):
                    if [y2, y1] not in dup_list:
                        dup_list.append([y1, y2])
        for r1, r2 in dup_list:
            if (m[r1].count(BLACK) == 2) and (m[r2].count(BLACK) == 0):
                for i, e in enumerate(m[r1]):
                    if e == BLACK:
                        m[r1][i] = inv(m[r2][i])
                        # print r1,i,"was set to inv ",r2,i
            elif (m[r2].count(BLACK) == 2) and (m[r1].count(BLACK) == 0):
                for i, e in enumerate(m[r2]):
                    if e == BLACK:
                        m[r2][i] = inv(m[r1][i])
                        # print r1,i,"was set to inv ",r2,i
        # print dup_list
        return m
    first_pass = _matrixprocess(M)
    second_pass = _matrixprocess(transpose(first_pass))
    return transpose(second_pass)

#simple function for calling the other three functions
def solve(m, sz):
    #this loop runs the three functions on the matrix until the matrix 
    #doesn't change, which means it's solved; then returns it.
    while True:
        new_m = solveDuplicates(solveHalves(solveThrees(m), sz))
        if new_m == m:
            break
        m = new_m
    return m


if __name__ == '__main__':
    main(sz=4) #the sz argument is the size of the board (4x5 or 10x10, etc.) 
