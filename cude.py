import dot
import math, os, time, random
import threading, keyboard
import pyautogui

import pygame
import win32api
import win32con
import win32gui
import ctypes

mx, my = pyautogui.position()


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
                self.end = True

h = Hook()
h.start()

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

dist = 200
FTR = dot.point()
FTR.set_point(dist, dist, dist)
c.points.append(FTR)
FTL = dot.point()
FTL.set_point(-dist, dist, dist)
c.points.append(FTL)
BTL = dot.point()
BTL.set_point(-dist, dist, -dist)
c.points.append(BTL)
BTR = dot.point()
BTR.set_point(dist, dist, -dist)
c.points.append(BTR)

FBR = dot.point()
FBR.set_point(dist, -dist, dist)
c.points.append(FBR)
FBL = dot.point()
FBL.set_point(-dist, -dist, dist)
c.points.append(FBL)
BBL = dot.point()
BBL.set_point(-dist, -dist, -dist)
c.points.append(BBL)
BBR = dot.point()
BBR.set_point(dist, -dist, -dist)
c.points.append(BBR)


#for _ in range(20):
#    FTR = dot.point()
#    FTR.set_point(random.randint(-200, 200), random.randint(-200, 200), random.randint(-200, 200))
#    c.points.append(FTR)


def draw():
    d = 10




def update():

    return 

while True:
    mx, my = pyautogui.position()
    c.ry = max(min(-(15*(screensize[0]//2 - mx)/screensize[0] - c.rx)/50.0, 20), -20)
    c.rx = max(min((15*(screensize[1]//2 - my)/screensize[1] - c.ry)/50.0, 20), -20)
    c.rz = 0
    
    c.rotate()

    if h.end == True:
        break
    screen.fill(fuchsia)
    mx, my = pyautogui.position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    for p in c.points:
        z_s = min(int(255*(p.z + 400)/1000.0), 255)
        tx, ty = p.get_point_2d()
        tx += screensize[0]//2
        ty += screensize[1]//2
        pygame.draw.circle(screen, (255-z_s, 100, 100), (tx, ty), int(4000/(p.z+500)))
    
    
    pygame.display.update()
    time.sleep(0.01)
    print("\r", end="")
