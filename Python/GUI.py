from CVFunctions import *
def do():
    try:
        url = 'http://172.20.13.144:8080/shot.jpg'
        #url = 'http://192.168.43.1:8080/shot.jpg'
        img = takeImage(url)
        img = ResizeWithAspectRatio(img,width = 768)
        img = hFlip(img)
        img = rotate(img)

        height,width,c = img.shape
        return height,width
    except:
        print("failed. check connection")
        do()
height,width = do()
import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import os, sys
from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.popup import Popup
import cv2
from functools import partial
import os
import threading
import json

class Widgets():
    def __init__(self):
        self.slider_list = [] 
        self.dict = {}

widgets = Widgets()

def getValues():
    values_list = []
    for tuple in widgets.slider_list:
        label,slider = tuple
        values_list.append(slider.value)
    x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold = values_list
    return x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold  
def initializeDetection(instance,x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold):
    # x_size = 400
    # y_size = img.shape[0]
    # blank_board_threshold = 195
    # cell_threshold = 60
    # h_crop = 0
    # w_crop = 0
    widgets.url = 'http://172.20.13.144:8080/shot.jpg'
    #widgets.url = 'http://192.168.43.1:8080/shot.jpg'
    img = takeImage(widgets.url)
    img = ResizeWithAspectRatio(img,width = 768)
    
    img = rotate(img)
    img = img[:int(y_size),:int(x_size)]
    img = crop(img,int(h_crop),int(w_crop))
    #cv2.imwrite("board.jpg",img)
    cv2.imshow("ss",img)
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    ret, thresh = cv2.threshold(grey,board_corner_threshold,255,cv2.THRESH_BINARY)
    cv2.imshow("thresh",thresh)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if key == 27:
        instance.disabled = False
        return
    widgets.board_corners_list,key = findChessBoardCorners(img,1,board_corner_threshold,debugging = True) 
    if key == 27:
        instance.disabled = False
        return
    widgets.dict["board_corners_list"] = widgets.board_corners_list
    warped_board = cropWarp(img,widgets.board_corners_list)
    warped_board = crop(warped_board,3,3)
    try:
        corners_list = findSquaresCorners(warped_board,blank_board_threshold)
        if key == 27:
            instance.disabled = False
            return
        widgets.corners_list = sortPts(corners_list)
        widgets.dict["corners_list"] = widgets.corners_list
        widgets.dict["params"] = [x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold]
        # with open("config.json",'w+') as f:
        #         json.dump(widgets.dict,f,indent = 0)
    except Exception as e:
        print(e)
        instance.disabled = False
        return

    instance.disabled = False

def initializeDetectionThreaded(instance):
    instance.disabled = True
    x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold = getValues()
    thread = threading.Thread(target=partial(initializeDetection,instance,x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold))
    thread.daemon = True
    thread.start()  
    

def beginDetection(instance,x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold):
    url,board_corners_list,corners_list = widgets.url,widgets.board_corners_list,widgets.corners_list
    input("set up board")
    new = takeImage(url)
    
    new = ResizeWithAspectRatio(new,width = 768)
    new = rotate(new)
    new = new[:int(y_size),:int(x_size)]
    new = crop(new,int(h_crop),int(w_crop))
    #cv2.imwrite("filled_board.jpg",new)
    new = cropWarp(new,board_corners_list)
    new = crop(new,3,3)
    # sd1,scd1 = makeSquaresDicts(makeSquares(new,corners_list))
    # for square in sd1:
    #     print(square)
    #     cv2.imshow(square,sd1[square])
    #     cv2.waitKey()
    #     cv2.destroyAllWindows()
    i = 0
    while True:
        old = new
        quit=input("waiting for player to play")
        if quit == "q": 
            break
        new = takeImage(url)
        new = ResizeWithAspectRatio(new,width = 768)
        new = rotate(new)
        new = new[:int(y_size),:int(x_size)]
        new = crop(new,int(h_crop),int(w_crop))
        
        #cv2.imwrite(f"filledboard{i}.jpg",new)
        new = cropWarp(new,board_corners_list)
        new = crop(new,3,3)
  
        i += 1
        cv2.imshow("old",old)
        cv2.imshow("new",new)
        grey_square = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY)
        # crop_size = min(grey_square.shape[0],grey_square.shape[1])*0.4
        # grey_square = crop(grey_square,crop_size ,crop_size)
        ret,old_thresh = cv2.threshold(grey_square, cell_threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow("old_thresh",old_thresh)
        grey_square = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
        ret,new_thresh = cv2.threshold(grey_square, cell_threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow("new_thresh",new_thresh)
        cv2.waitKey()
        cv2.destroyAllWindows()   
        try:      
            move = compareOldNew(old,new,corners_list,cell_threshold)
        except Exception as e:
            print(e)
            instance.disabled = False
            return
        print(move)
def beginDetectionThreaded(instance):
    instance.disabled = True
    x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold = getValues()
    thread = threading.Thread(target=partial(beginDetection,instance,x_size,y_size,h_crop,w_crop,board_corner_threshold,blank_board_threshold,cell_threshold))
    thread.daemon = True
    thread.start()          
def root():
    def onSliderValueChange(instance,value,label,name):
        label.text = name+":"+str(int(value))
    grid = GridLayout(cols=1,spacing = 1)
    for name in ["x_size","y_size","h_crop","w_crop","board_corner_threshold","blank_board_threshold","cell_threshold"]:
        
        if name == "x_size":
            max = width
            min = 200
            value = 371
        elif name == "y_size": 
            max = height
            min = 200
            value = 400
        elif name == "h_crop": 
            max = 100
            min = 0
            value = 0    
        elif name == "w_crop": 
            max = 100
            min = 0
            value = 0        
        elif name == "board_corner_threshold":
            max = 255
            min = 0
            value = 67
        elif name == "blank_board_threshold": 
            max = 255
            min = 0
            value = 175
        elif name == "cell_threshold": 
            max = 255
            min = 0
            value = 60    
        slider = Slider(min=min, max=max, value=value)
        label = Button(text = name+":"+str(int(slider. value)),background_disabled_normal='',disabled=True,background_color=hex("212121"),color = hex("ffffff"))
        slider.bind(value=partial(onSliderValueChange,label=label,name=name))
        grid.add_widget(label)
        grid.add_widget(slider)
        widgets.slider_list.append((label,slider))
    init_btn = Button(text="Init Detection",background_normal="",background_color = hex("#212121"),font_size = 18)
    init_btn.bind(on_release = initializeDetectionThreaded )
    grid.add_widget(init_btn)
    begin_button = Button(text="Begin Detection",background_normal="",background_color = hex("#212121"),font_size = 18)
    begin_button.bind(on_release = beginDetectionThreaded)
    grid.add_widget(begin_button)
    return grid
class CamApp(App):
    def build(self):
        top_root = root()
        return top_root

CamApp().run()
    



