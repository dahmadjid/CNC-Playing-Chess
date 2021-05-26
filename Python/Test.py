from CVFunctions import *
import json
blank = cv2.imread("board.jpg")
img_list = []
for i in range(11):
    img_list.append(cv2.imread(f"filledboard{i}.jpg"))
filled0 = cv2.imread("filledboard0.jpg")
filled1 = cv2.imread("filledboard1.jpg")

with open("config.json","r") as f:
    dict=json.load(f)

board_corners_list = dict["board_corners_list"]
corners_list = dict["corners_list"]
params = dict["params"]

x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold = params



print(len(board_corners_list))
print(len(corners_list))
print(params)


blank = cropWarp(blank,board_corners_list)
blank = crop(blank,3,3)
for i in range(10):
    filled0 = img_list[i]
    filled1 = img_list[i+1]
    filled0 = cropWarp(filled0,board_corners_list)
    filled0 = crop(filled0,3,3)

    filled1 = cropWarp(filled1,board_corners_list)
    filled1 = crop(filled1,3,3)
    move = compareOldNew(filled0,filled1,corners_list,75)
    print(move) 
    cv2.imshow("blank",blank)
    cv2.imshow("filled0",filled0)
    cv2.imshow("filled1",filled1)
    cv2.waitKey()
    cv2.destroyAllWindows()

#     if move == 'wtf':
#         squares = makeSquares(filled0,corners_list)
#         squares_dict,squares_color_dict=makeSquaresDicts(squares)
        
#         for square_name,square in squares_dict.items():
#             grey_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
#             ret,thresh = cv2.threshold(grey_square, 75, 255, cv2.THRESH_BINARY)
# #     bcount = 0
# #     wcount = 0
#     # for row in thresh:
        
#     #     for col in row:
#     #         if int(col) == 0:
#     #             bcount += 1
#     #         else:
#     #             wcount += 1
#     # average = bcount/(bcount + wcount)  
#     # print(square_name,int(average*100))     

#     # contours,hierarchy = cv2.findContours(thresh, 1, 2)
#     # cnt = contours[0]
#     # area = cv2.contourArea(cnt)
#     # print(square_name,area)
#             cv2.imshow(square_name,ResizeWithAspectRatio(square,width=300))
#         cv2.waitKey()
#         cv2.destroyAllWindows()
#         squares = makeSquares(filled1,corners_list)
#         squares_dict,squares_color_dict=makeSquaresDicts(squares)
#         for square_name,square in squares_dict.items():
#             grey_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
#             ret,thresh = cv2.threshold(grey_square, 75, 255, cv2.THRESH_BINARY)
#             cv2.imshow(square_name,ResizeWithAspectRatio(square,width=300))
#         cv2.waitKey()
#         cv2.destroyAllWindows()


