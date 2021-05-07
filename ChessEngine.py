import cv2
import chess
import chess.engine
import serial
from UCI_TO_CORDS import UCI2CORDS,fenToMatrix
from CVFunctions import *
#from updateboard import *
#TODO: Take Picture of blank board:

try:
        engine = chess.engine.SimpleEngine.popen_uci("/home/madjid/stockfish_13_linux_x64_avx2/stockfish_13_linux_x64_avx2/stockfish_13_linux_x64_avx2")
except:
    print("engine not found pick a correct directory")
    exit()
board = chess.Board()
limit = chess.engine.Limit(time=1.5, depth=15) #time is how much will the engine take to think
                                                #depth is how much moves ahead the engine can think
                                                #these two values are the limit of the engine and not enforced
print(board)

#Set up port------------------------------
# set_up_complete = False
# while set_up_complete == False:
#     com = input("port?\n")        
#     try:
#         arduino = serial.Serial("COM"+com, 9600 , timeout = 0.1)
#         set_up_complete = True
#     except:
#         print("invalid port. try again\n")
#         continue

#-----------------------------------------
while not board.is_game_over():


    #TODO: Take picture of the board before the player plays
    player_move = input("player move?") #TODO variable from open cv
#Chess----------------------------------------------------------------------------------------------
    try:
        pmove = chess.Move.from_uci(player_move)
    except:
        print("type in correct coordinates in the uci format , example : e2e4")
        continue
    if pmove in board.legal_moves:
        board.push(pmove)
    else:
        print("move is illegal try again")
        continue

    result = engine.play(board,limit)
    rmove = result.move
    print(rmove)
    output =UCI2CORDS(str(rmove),board.board_fen())
    board.push(rmove)
    print(output)
    
#----------------------------------------------------------------------------------------------------
    try:
        arduino.write(output.encode('utf-8'))
    except:
        pass
    print(board)
engine.quit()
