import math, os, time, random
import threading, keyboard
import pyautogui

import pygame
import win32api
import win32con
import win32gui
import ctypes

print("f4로 그림 모드 진입, f4 다시 눌러서 그리기on/off, esc로 그림모드 종료, esc로 전체 종료")
mx, my = pyautogui.position()
mode = 1

pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
screen = pygame.display.set_mode(screensize, pygame.NOFRAME)
done = False
fuchsia = (100, 100, 100)  # Transparency color
dark_red = (139, 0, 0)


win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)


class Hook(threading.Thread):
    def __init__(self):
        super(Hook, self).__init__()
        self.daemon = True
        self.end = False
        
        keyboard.unhook_all()
        
    def run(self):
        global mode
        while True:
            key = keyboard.read_hotkey(suppress=False)
            if key == 'esc':
                if mode != 1:
                    mode = 1
                else:
                   self.end = True
                
            if key == 'f4':
                if mode == 1:
                    mode = 2
                elif mode == 2:
                    mode = 0
                elif mode == 0:
                    mode = 2
h = Hook()
h.start()

class point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set_point(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def get_point_3d(self):
        return (self.x, self.y, self.z)
    def get_point_2d(self):
        d = (8000)/(8000 + self.z)
        return (self.x * d, self.y * d)
class cube:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0

        self.points = []

    def rotate(self):
        for p in self.points:
            tempx = p.x*math.cos(self.ry)*math.cos(self.rz) - p.y*math.cos(self.ry)*math.sin(self.rz)+ p.z*math.sin(self.ry)
            tempy = p.x*(math.cos(self.rx)*math.sin(self.rz) + math.sin(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + p.y*(math.cos(self.rx)*math.cos(self.rz) - math.sin(self.rx)*math.sin(self.ry)*math.sin(self.rz)) - p.z*math.sin(self.rx)*math.cos(self.ry)
            tempz = p.x*(math.sin(self.rx)*math.sin(self.rz) - math.cos(self.rx)*math.sin(self.ry)*math.cos(self.rz)) + p.y*(math.sin(self.rx)*math.cos(self.rz) + math.cos(self.rx)*math.sin(self.ry)*math.sin(self.rz)) + p.z*math.cos(self.rx)*math.cos(self.ry)
            p.x = tempx
            p.y = tempy
            p.z = tempz

c = cube()

max_x = 1000
max_y = 1000

def draw():
    d = 10


def update():

    return 

while True:
    mx, my = pyautogui.position()
    c.rx = 0
    c.ry = 0
    c.rz = 0
    if mode == 1:
        c.ry = max(min(-(15*(screensize[0]//2 - mx)/screensize[0] - c.rx)/80.0, 20), -20)
        c.rx = max(min((15*(screensize[1]//2 - my)/screensize[1] - c.ry)/80.0, 20), -20)
        c.rz = 0
    elif mode == 0:
        mx -= screensize[0]/2
        my -= screensize[1]/2
        FTR = point()
        FTR.set_point(max(min(mx, max_x), -max_x), max(min(my, max_y), -max_y), 0)
        c.points.append(FTR)


    c.rotate()

    if h.end == True:
        break
    screen.fill(fuchsia)
    mx, my = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    for p in c.points:
        z_s = (p.z + max_x*2)/4000
        tx, ty = p.get_point_2d()
        tx += screensize[0]//2
        ty += screensize[1]//2
        pygame.draw.circle(screen, (255-max(min(int(z_s*255), 255), 0), 100, 100), (tx, ty), 11-max(0, min(int(z_s*10), 10)))
    
    
    pygame.display.update()
    print("\r", end="")
