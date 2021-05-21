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
for square_name,square in squares_dict.items():
    cv2.imshow(square_name,square)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

