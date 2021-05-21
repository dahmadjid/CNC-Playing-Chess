from CVFunctions import *


img = cv2.imread("corners1.jpg")
img = ResizeWithAspectRatio(img,width = 600)
img = crop(img,50,20)
board_corners_list = findChessBoardCorners(img,2) 
warped_board = cropWarp(img,board_corners_list)
warped_board = crop(warped_board,5,5)
corners_list = findSquaresCorners(warped_board)
corners_list = sortPts(corners_list)
squares_dict,squares_color_dict = makeSquaresDicts(makeSquares(warped_board,corners_list))
squares_state_dict = makeSquaresStateDict(squares_dict,squares_color_dict,warped_board)
print(squares_state_dict)
