import chess
def fenToMatrix(fen):
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    
    fen_list = fen.split("/")
    fen = ""
    i = 7
    for row in fen_list:
        
        fen = fen + fen_list[i] 
        i = i -1   
    board = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    i = 0
    for char in fen:
        if char in "rnbqkpRNBQKP":
            board[i] = char
            i += 1
        elif char in "12345678":
            for empty in board[i:i+int(char)]:
                board[i] = "0"
                i+=1
    board_dict = {}
    i = 0
    for square in chess.SQUARE_NAMES:
        board_dict[square] = board[i]
        i += 1
    return board_dict      
def UCI2CORDS_SEPARATE(UCImove):
    a = UCImove[0]
    b = UCImove[1]
    c = UCImove[2]
    d = UCImove[3]
    letters = [a, c]
    x = None
    for letter in letters:
        x0 = x
        if letter == 'a':
            x = 0
        elif letter == 'b':
            x = 1
        elif letter == 'c':
            x = 2
        elif letter == 'd':
            x = 3
        elif letter == 'e':
            x = 4
        elif letter == 'f':
            x = 5
        elif letter == 'g':
            x = 6
        elif letter == 'h':
            x = 7
        else:
            print("the coordinates given are not in UCI format")
            exit()
    y0 = int(b) - 1
    y = int(d) - 1
    return x0 ,y0 ,x ,y
def UCI2CORDS(UCImove,fen):
    board = fenToMatrix(fen)
    piece = board[UCImove[2:]]
    

    print(piece,"\n")
    if UCImove == 'e8c8':
        output  = "0000c"
        return output
    elif UCImove == "e8g8":
        output = "1111c"
        return output
    else:    
        
        x0 ,y0 ,x ,y =UCI2CORDS_SEPARATE(UCImove)
        output = str(x0)+ str(y0) + str(x)+str(y)
        if piece != "0":
            output = output + "e"
        else:
            output = output + "m"
        return output
