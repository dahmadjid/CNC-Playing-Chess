import cv2
import numpy as np
import chess
import requests
from PIL import Image
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    d = h-w
    if d >0:
        cv2.transpose(image,image)
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def takeImage(url):


    resp = requests.get(url, stream=True).raw
    print("img")
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

    # # for testing
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
def rotate(img):
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img    
def findChessBoardCorners(img,accuracy,board_corner_threshold,debugging = False):  #the smaller the accuracy the better
    
    imgoriginal = img
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

    ret, thresh = cv2.threshold(img,board_corner_threshold,255,cv2.THRESH_BINARY)

    black_list = []
    y = 0
    for row in thresh:
        x = 0
        for col in row:
            if int(col) == 0:
                black_list.append([y,x])
            x += 1
        y +=1         
        
    for i in range(len(black_list)-1):
            if i%accuracy != 0:
                continue
            y1,x1 = black_list[i]
            for j in range(len(black_list)-1):
                y2,x2 = black_list[j]
                cv2.line(thresh,(x1,y1),(x2,y2),(0,255,0),1)

    corners = cv2.goodFeaturesToTrack(thresh, 4, 0.001, 100)
    corners_list = []
    for c in corners:
        x, y = c.ravel()
        cv2.circle(img , (int(x),int(y)) , 10 ,(255,0,0) ,-1)
        corners_list.append([y,x])
    if debugging:
        cv2.imshow("d",thresh)
        cv2.imshow("qwdqwdwq",img)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()  
        if key == 27:
            return None,-1
    sorted_list = [0,0,0,0]
    print(img.shape)
    #sorting
    average_y = (corners_list[0][0] + corners_list[1][0] + corners_list[2][0] + corners_list[3][0])/4
    average_x = (corners_list[0][1] + corners_list[1][1] + corners_list[2][1] + corners_list[3][1])/4
    print(average_y,average_x)
    for corner in corners_list:
        y,x = corner
        print(corner)
        if y < average_y and x < average_x:
            sorted_list[0] = [int(y),int(x)]
        elif y < average_y and x > average_x:
            sorted_list[1] = [int(y),int(x)]
        elif y > average_y and x > average_x:
            sorted_list[2] = [int(y),int(x)]
        elif y > average_y and x < average_x:
            sorted_list[3] = [int(y),int(x)]
    return sorted_list
def cropWarp(img,corners_list):  # corners_list : list of 4 points (height,width) or (y,x)
                                # img should be same size as the img used to find corners_list from function findChessBoardCorners
                                # yes the function later flips the coordinates but the input is (y,x)
    top_left, top_right, bottom_right, bottom_left = corners_list
    top_left = [top_left[1],top_left[0]]
    top_right = [top_right[1],top_right[0]]
    bottom_right = [bottom_right[1],bottom_right[0]]
    bottom_left = [bottom_left[1],bottom_left[0]]

    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')
    width_AD = np.sqrt(((top_left[0] - top_right[0]) ** 2) + ((top_left[1] - top_right[1]) ** 2))
    width_BC = np.sqrt(((bottom_left[0] - bottom_right[0]) ** 2) + ((bottom_left[1] - bottom_right[1]) ** 2))
    max_width = max(int(width_AD), int(width_BC))
    height_AB = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
    height_CD = np.sqrt(((bottom_right[0] - top_right[0]) ** 2) + ((bottom_right[1] - top_right[1]) ** 2))
    max_height = max(int(height_AB), int(height_CD))
    dst = np.float32([[0, 0],[max_width, 0],[max_width , max_height],[0, max_height]])
    m = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, m,(max_width,max_height)) 
def addPadding(img,size):
    newimg=cv2.copyMakeBorder(img, size, size, size, size, cv2.BORDER_CONSTANT, value=200)
    return newimg
def crop(img,height_size,width_size):
    h,w,c = img.shape
    img = img[height_size:h-height_size,width_size:w-width_size]
    return img
def vFlip(img):
    img = cv2.flip(img, 0)
    return img
def findSquaresCorners(blank,blank_board_threshold):

    blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
     
    ret, thresh = cv2.threshold(blank, blank_board_threshold, 255, cv2.THRESH_BINARY)
    thresh = vFlip(thresh)
    # thresh = cv2.GaussianBlur(thresh,(15,15),0)
    thresh = cv2.bilateralFilter(thresh,9,75,75)
    # kernel_v = np.array([[1,1,1],[1,1,1],[0,0,0]],np.float32())
    # kernel_h = np.array([[0,1,1],[0,1,1],[0,1,1]],np.float32())
    # thresh = cv2.filter2D(thresh,-1,kernel_h)
    # thresh = cv2.filter2D(thresh,-1,kernel_v)
    ref, thresh = cv2.threshold(thresh, 175, 255, cv2.THRESH_BINARY)
    padded = addPadding(thresh, 50)
    cv2.imshow('ss',padded)
    cv2.waitKey()
    cv2.destroyAllWindows()
    corners = cv2.goodFeaturesToTrack(padded, 81, 0.01, 30)
    corners_list = []
    for c in corners:
        x, y = c.ravel()
        corners_list.append([int(y - 50), int(x - 50)])
        cv2.circle(blank , (int(x - 50),int(y - 50)) , 2 ,(0,0,0) ,-1)
    cv2.imshow("cell_corners",blank)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
    print(len(corners_list))
    return corners_list

def sortPts(corners_list:list) ->list:   #list of the 81pts of the chess board of each cell 
                                         #list should be sorted so that later they are sorted according to chess.SQUARE_NAMES
    sorted_pts = [0 for k in range(81)]
    for i in range(81):
        min = 600
        for idx,c in enumerate(corners_list):
            y = c[0]
            x = c[1]

            if y<min:
                min = y
                min_idx = idx

        sorted_pts[i] = corners_list[min_idx]
        corners_list.pop(min_idx)
    #bubble sort according to the 2nd coordinate
    devided_arr = [[sorted_pts[0:9]],[sorted_pts[9:18]],[sorted_pts[18:27]],[sorted_pts[27:36]],[sorted_pts[36:45]],[sorted_pts[45:54]],[sorted_pts[54:63]],[sorted_pts[63:72]],[sorted_pts[72:]]]
    temp = []
    for section in devided_arr:
        section = section[0]
        n = len(section)
        for i in range(n-1):
            for j in range(0, n - i - 1):
                if section[j][1] > section[j + 1][1]:
                    section[j], section[j + 1] = section[j + 1], section[j]
        temp.append(section)
    sorted_pts = []
    for section in temp:
        for pt in section:
            sorted_pts.append(pt)
    return sorted_pts
def makeSquares(img,sorted_pts:list):
    squares = []
    
    for i in range(71):
        if i in [8,17,26,35,44,53,62]:
            continue
        cv2.line
        square = img[sorted_pts[i][0]:sorted_pts[i+10][0],sorted_pts[i][1]:sorted_pts[i+10][1]]
        squares.append(square)
 
    print(len(squares))    
    return squares
    
def makeSquaresDicts(squares:list):
    squares_dict = {}        #dict to link cell names with the 64 squares of the image
    squares_color_dict = {}  #dict for what color is each square to help with threshholding
    for i in range(8): #a,b,c,d,...
        for j in range(8): #1 2 3 4....
            if i%2 == j%2: #odd-odd or even-even (a is like 1 and b like 2 ....) are black cells and different are white
                squares_color_dict[chess.FILE_NAMES[i]+chess.RANK_NAMES[j]] = 'b'
            else:
                squares_color_dict[chess.FILE_NAMES[i] + chess.RANK_NAMES[j]] = 'w'


    i =0
    for square in squares:
        if square.shape[1] != 0:
            square = vFlip(square)
            squares_dict[chess.SQUARE_NAMES[i]] = square
            i += 1
    return squares_dict,squares_color_dict
    

    
    
def makeSquaresStateDict(squares_dict,squares_color_dict,board,cell_threshold):
    squares_state_dict = {}
    for square_name,square in squares_dict.items():
        
        # piece = getPiece(board,square_name)
        # piece_color = piece[0]
        # square_color = squares_color_dict[square_name]
        square = crop(square, 7,7)
        grey_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(grey_square, cell_threshold, 255, cv2.THRESH_BINARY)

        # cv2.imshow(square_name,thresh)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # #TODO: use for a real chess picture cuz 125/255 threshhold works for 2d flat pic so far
        # if not piece_color == ' ':
        #     if piece_color == square_color:
        #         if piece_color == 'w':
        #             pass
        #             #TODO: use certain threshhold for white-white colors
        #         elif piece_color == 'b':
        #             # TODO: use certain threshhold for black-black colors
        #             pass
        #     else:
        #         # TODO: use certain threshhold when they are different
        #         pass
        # else:
        #     #TODO: use certain threshhold when the cell is empty
        #     pass


        corners = cv2.goodFeaturesToTrack(thresh,8, 0.001, 1)
        if corners is None:
            square_state = 0
            squares_state_dict[square_name] = square_state #square is empty ie has no piece in it
        else:
            square_state = 1
            squares_state_dict[square_name] = square_state #square in not empty ie has a piece in it
    return squares_state_dict
    
def wholeProcess(blank_board,board):
    
    corners_list = findSquaresCorners(blank_board)
    sorted_pts = sortPts(corners_list)
    squares_list = makeSquares(board,sorted_pts)
    squares_dict, squares_color_dict = makeSquaresDicts(squares_list)
    
    
    return squares_dict,squares_color_dict
def compare_pil(img1,img2):

    
    i1 = Image.fromarray(img1)
    i2 = Image.fromarray(img2)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
    
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    
    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents

def compareOldNew(b1,b2,corners_list,cell_threshold):  #1 is old board, 2 is new board 
    from_cord = '00'
    to_cord = '00'
    sum1 = 0
    sum2 = 0
    sd1,scd1 = makeSquaresDicts(makeSquares(b1,corners_list))
    sd2,scd2 = makeSquaresDicts(makeSquares(b2,corners_list))
    ssd1 = makeSquaresStateDict(sd1,scd1,b1,cell_threshold)
    ssd2 = makeSquaresStateDict(sd2,scd2,b2,cell_threshold)
    for i in range(64):
        sum1 = sum1 + ssd1[chess.SQUARE_NAMES[i]] 
    for i in range(64):    
        sum2 = sum2 + ssd2[chess.SQUARE_NAMES[i]]
    print("sum1,sum2:",sum1,sum2)
    if sum1-sum2 == 0:
        #normal movement happend/castling
        print("normal movement or castling")
        for square in chess.SQUARE_NAMES:
            
            diff = ssd2[square] - ssd1[square]

            if diff==-1:
                from_cord = square 
            elif diff==1:
                to_cord = square
            elif diff==0:
                pass
            else:
                print('wtf happend')    
        return from_cord + to_cord
    
    elif sum1-sum2 > 0: 
        print("eating")
        #eating happend
        for square in chess.SQUARE_NAMES:
            diff = ssd2[square] - ssd1[square]

            if diff==-1:
                from_cord = square
                break
            elif diff==0:
                pass

            else:
                print('wtf happend')   
        percent_max = 0
        for square in chess.SQUARE_NAMES:
            if square == from_cord:
                continue
            sq1 = cv2.cvtColor(sd1[square], cv2.COLOR_BGR2GRAY)
            sq2 = cv2.cvtColor(sd2[square], cv2.COLOR_BGR2GRAY)
            percentage = compare_pil(sq1,sq2)
            #finds how much each cell changed from old to new.
            #the cell with most change is the to_cord.

            print('percentage',percentage,percent_max)
            if percentage > percent_max:
                percent_max = percentage
                to_cord = square
        return from_cord + to_cord
    return "wtf"        



#def DrawCirclesOnCorners(img,y1,x1,y2,x2,y3,x3,y4,x4,f):

#     Corners=[(y1,x1),(y2,x2),(y3,x3),(y4,x4)]
#     for y,x in Corners:
#         cv2.circle(img , (x,y) , 1 ,(255,0,0) ,-1)
#     cv2.imwrite('ChessDataset/new/withcircles/'+f,img)


# def findCorners(img):

#     img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     ret , thresh = cv2.threshold(img ,3 , 255,cv2.THRESH_BINARY)
#     corners=cv2.goodFeaturesToTrack(thresh , 4 , 0.01 , 10)
#     Corners=[]
#     sum = 0
#     try:

#         for c in corners:
#             x,y = c.ravel()
#             Corners.append((y,x))
#             sum = y + x + sum
#         avg=sum/8 #sort the corners
#         output = [(1,1),(2,2),(3,3),(4,4)]
#         check_output = [(1,1),(2,2),(3,3),(4,4)]
#         for y,x in Corners:

#             if x < avg and y < avg :
#                 output[0]=(y,x)
#             elif x>avg and y<avg:
#                 output[1]=(y,x)
#             elif x<avg and y>avg:
#                 output[2]=(y,x)
#             elif x>avg and y>avg:
#                 output[3]=(y,x)

#     except:
#         output = None
#     if corners is not None:
#         if output[0] == check_output[0] or output[1] == check_output[1] or output[2] == check_output[2] or output[3] == check_output[3]:
#             output = None

#     return output



    
    