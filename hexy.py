# Game Call Phaze - overlapping patterns (rotate, etc)

# Initialization ==================================================================================

import sys

# print(sys.version)

from sys import winver
import pygame
from pygame import gfxdraw
from pygame.constants import KEYUP
import os
import math
import random
import helper

from enum import IntEnum
from enum import Enum

from helper import board

pygame.font.init()
pygame.mixer.init()
pygame.init()

# Constants =======================================================================================

# Initial Display Size
WIDTH  = 1000
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Habitat for Humanity Game")

# Color Constants
WHITE = (255,255,255,128)
BACKGROUND = (32,32,32)

# Mouse Button Constants
LEFT        = 1
CENTRE      = 2
RIGHT       = 3
SCROLL_UP   = 4
SCROLL_DOWN = 5

# Coordinate Constants
X = 0
Y = 1

# Orientation
VERTICAL = 0
HORIZONTAL = 1

class VASARELY_COLORS(Enum):

  PINK     = (181, 42,142)
  PURPLE   = ( 90, 24,120)
  
  BLUE     = ( 39,105,176)
  CYAN     = ( 79,168,219)
  NAVY     = ( 42, 40,143)

  DORANGE  = (227,102, 79)
  LORANGE  = (250,147, 95)
  
  LYELLOW  = (244,255,173)
  DYELLOW  = (247,194,119)
  
  LGREEN   = (  0,173,147)
  DGREEN   = (  0,110,110)

  RED      = (222, 33, 49)
  MAROON   = (135, 26, 35)
  PEACH    = (247,194, 11) 

  BLACK    = ( 64,64,64)
  GRAY     = (122,135,191)

class COLORS(IntEnum):

  PINK    = 0
  PURPLE  = 1
  CYAN    = 2
  NAVY    = 3
  BLUE    = 4
  DORANGE = 5
  LORANGE = 6
  LYELLOW = 7
  DYELLOW = 8
  LGREEN  = 9
  DGREEN  = 10
  PEACH   = 11
  RED     = 12
  MAROON  = 13
  BLACK   = 14
  GRAY    = 15

BULLET_HIT_SOUND  = pygame.mixer.Sound(os.path.join('C:/Users/ssbbc/Desktop/Brad/python/assets', 'Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('C:/Users/ssbbc/Desktop/Brad/python/assets', 'Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 12)

# Globals =========================================================================================

# Methods =========================================================================================

def get_Color():

  clr = int(random.random()*16)

  ret = VASARELY_COLORS.PINK.value

  if   clr == COLORS.PINK:    ret = VASARELY_COLORS.PINK.value
  elif clr == COLORS.PURPLE:  ret = VASARELY_COLORS.PURPLE.value
  elif clr == COLORS.CYAN:    ret = VASARELY_COLORS.CYAN.value
  elif clr == COLORS.NAVY:    ret = VASARELY_COLORS.NAVY.value
  elif clr == COLORS.BLUE:    ret = VASARELY_COLORS.BLUE.value
  elif clr == COLORS.DORANGE: ret = VASARELY_COLORS.DORANGE.value
  elif clr == COLORS.LORANGE: ret = VASARELY_COLORS.LORANGE.value
  elif clr == COLORS.LYELLOW: ret = VASARELY_COLORS.LYELLOW.value
  elif clr == COLORS.DYELLOW: ret = VASARELY_COLORS.DYELLOW.value
  elif clr == COLORS.LGREEN:  ret = VASARELY_COLORS.LGREEN.value
  elif clr == COLORS.DGREEN:  ret = VASARELY_COLORS.DGREEN.value
  elif clr == COLORS.PEACH:   ret = VASARELY_COLORS.PEACH.value
  elif clr == COLORS.RED:     ret = VASARELY_COLORS.RED.value
  elif clr == COLORS.MAROON:  ret = VASARELY_COLORS.MAROON.value
  elif clr == COLORS.BLACK:   ret = VASARELY_COLORS.BLACK.value
  elif clr == COLORS.GRAY:    ret = VASARELY_COLORS.GRAY.value
  else:                       ret = VASARELY_COLORS.GRAY.value

  return ret
  #   clr = int(random.random()*16)

  #   match clr:
      
  #     case COLORS.PINK:    return PINK
  #     case COLORS.PURPLE:  return PURPLE
  #     case COLORS.CYAN:    return CYAN
  #     case COLORS.NAVY:    return NAVY
  #     case COLORS.BLUE:    return BLUE
  #     case COLORS.DORANGE: return DORANGE
  #     case COLORS.LORANGE: return LORANGE
  #     case COLORS.LYELLOW: return LYELLOW
  #     case COLORS.DYELLOW: return DYELLOW
  #     case COLORS.LGREEN:  return LGREEN
  #     case COLORS.DGREEN:  return DGREEN
  #     case COLORS.PEACH:   return PEACH
  #     case COLORS.RED:     return RED
  #     case COLORS.MAROON:  return MAROON
  #     case COLORS.BLACK:   return BLACK
  #     case COLORS.GRAY:    return GRAY
  #     case _:              return -16

def initialize_Game():
  
  return

# Objects =========================================================================================

class App:

  def __init__(self, size):
      
    self.size = size

    self.grid = []           # list holding the cell objects
    self.current_cell = None # which hexagonal cell has the focus
    self.grid_size = 7       # of hexagonal layers - defaults to 4
    self.fps = 60
    self.orientation = VERTICAL

class point:

  def __init__(self, x, y) -> None:
    
    self.x = x
    self.y = y

class hex:

  id = 0

  def __init__(self, x, y, diameter, color, orientation):

    self.id = hex.id    # identificaion Number
    # print(self.id)

    hex.id+=1

    self.x = int(x)               # horizontal position of centre
    self.y = int(y)               # vertical position of centre
    
    self.diameter = diameter # full diameter width of hexagon
    self.radius = diameter/2 # distance from center to corner point
    
    self.width = math.cos(math.pi/6)*diameter
    
    self.center = point(self.x, self.y) # Center Point
    self.points = []

    self.orientation = orientation
    
    self.color = color
    self.center_color = color

    self.hit = False
    
    # Aliases
    sX = self.x
    sY = self.y
    r = self.radius
    pts = self.points

    if self.orientation == HORIZONTAL:

      # Calculate Corner Points

      # Offsets
      oX = math.cos(math.pi/6)*self.radius # Offset x
      oY = math.sin(math.pi/6)*self.radius # Offset Y

      pts.append((sX,      sY + r ))
      pts.append((sX + oX, sY + oY))
      pts.append((sX + oX, sY - oY))
      pts.append((sX,      sY - r ))
      pts.append((sX - oX, sY - oY))
      pts.append((sX - oX, sY + oY))

    else:

      oX = math.cos(math.pi/3)*self.radius # Offset x
      oY = math.sin(math.pi/3)*self.radius # Offset Y

      pts.append((sX + r,  sY))
      pts.append((sX + oX, sY - oY ))
      pts.append((sX - oX, sY - oY))
      pts.append((sX - r,  sY))
      pts.append((sX - oX, sY + oY))
      pts.append((sX + oX, sY + oY))

  def reset(self):

    id = 0

  def draw(self):

    def draw_text():
      
      pts = self.points

      WIN.blit(WINNER_FONT.render('0', 1, WHITE), (pts[0][0], pts[0][1]))
      WIN.blit(WINNER_FONT.render('1', 1, WHITE), (pts[1][0], pts[1][1]))
      WIN.blit(WINNER_FONT.render('2', 1, WHITE), (pts[2][0], pts[2][1]))
      WIN.blit(WINNER_FONT.render('3', 1, WHITE), (pts[3][0], pts[3][1]))
      WIN.blit(WINNER_FONT.render('4', 1, WHITE), (pts[4][0], pts[4][1]))
      WIN.blit(WINNER_FONT.render('5', 1, WHITE), (pts[5][0], pts[5][1]))

    w = WIN
    c = self.color

    pygame.gfxdraw.filled_polygon(w, self.points, self.color)
    
    # pygame.gfxdraw.filled_circle(WIN, self.x, self.y, int(app.size*0.35), self.center_color)
    # pygame.gfxdraw.circle(WIN, self.x, self.y, int(app.size*0.35), (128,128,128))

    text = HEALTH_FONT.render(str(self.id),True,WHITE)
    text_rect = text.get_rect(center=(self.x, self.y))
    # WIN.blit(text,text_rect)

    if self.hit:
      
      app.current_cell = self

      pygame.gfxdraw.filled_polygon(w, self.points, (0,0,0,64))
      # pygame.gfxdraw.aapolygon(w, self.points, VASARELY_COLORS.RED.value)

      # draw_text()

      # draw_text = WINNER_FONT.render('3', 1, WHITE)

      # WIN.blit(WINNER_FONT.render('0', 1, WHITE), (self.points[0][0], self.points[0][1]))
      # WIN.blit(WINNER_FONT.render('1', 1, WHITE), (self.points[1][0], self.points[1][1]))
      # WIN.blit(WINNER_FONT.render('2', 1, WHITE), (self.points[2][0], self.points[2][1]))
      # WIN.blit(WINNER_FONT.render('3', 1, WHITE), (self.points[3][0], self.points[3][1]))
      # WIN.blit(WINNER_FONT.render('4', 1, WHITE), (self.points[4][0], self.points[4][1]))
      # WIN.blit(WINNER_FONT.render('5', 1, WHITE), (self.points[5][0], self.points[5][1]))

  def hitTest(self):

    x = pygame.mouse.get_pos()[X]
    y = pygame.mouse.get_pos()[Y]

    if(math.dist((self.x, self.y), (x, y))<=self.radius): self.hit = True
    else:                                                 self.hit = False

  def move(self):

    self.hitTest()

  def click(self):

    if self.hit:
      app.current_cell = self
      print(app.current_cell.id)

app = App(WIDTH/(7+1))
app.size = WIDTH/(app.grid_size+1)

def load_grid():

  if app.orientation == HORIZONTAL: load_grid_horizontal()
  elif app.orientation == VERTICAL: load_grid_vertical()

def load_grid_horizontal():

  hex.id = 0

  # Add center row
  sz = app.size*1/math.cos(math.pi/6)
  
  app.grid.clear

  temp = []

  for cell in range(app.grid_size):

    colPos = app.size + cell*sz*math.cos(math.pi/6)

    temp.append(hex(colPos, HEIGHT/2, sz, get_Color(), HORIZONTAL))
    
  app.grid.append(temp)

  # Add Rows above and below
  row_offset = sz - sz*math.sin(math.pi/6)/2
  
  above = []
  below = []

  col_limit = int(app.grid_size-1)
  row_limit = math.ceil(app.grid_size/2-1)

  coef = sz*math.cos(math.pi/6)

  for row in range(row_limit):

    for col in range(col_limit):

      # Add to Start
      rowPos = HEIGHT/2 - row_offset * (row+1)
      colPos = app.size + col*coef + row*coef/2 + coef/2

      above.append(hex(colPos, rowPos, sz, get_Color(), HORIZONTAL))
      # above.append(hex(colPos, rowPos, sz, (hex.counter,hex.counter, hex.counter)))

      # Add to end
      rowPos = HEIGHT/2 + row_offset * (row+1)
      colPos = app.size + col*coef + row*coef/2 + coef/2

      below.append(hex(colPos, rowPos, sz, get_Color(), HORIZONTAL))
      # below.append(hex(colPos, rowPos, sz, (hex.counter,hex.counter, hex.counter)))

    app.grid.insert(0,above)
    app.grid.append(below)
    
    col_limit-=1

    above = []
    below = []

  # print(hex.counter)

def load_grid_vertical():

  hex.id = 0

  # Add center row
  sz = app.size*1/math.cos(math.pi/6)
  
  app.grid.clear

  temp = []

  # Add Center Column
  for cell in range(app.grid_size):

    colPos = app.size + cell*sz*math.cos(math.pi/6)

    temp.append(hex(WIDTH/2, colPos, sz, get_Color(), VERTICAL))
    
  app.grid.append(temp)

  # Add Rows above and below
  col_offset = sz - sz*math.sin(math.pi/6)/2
  
  above = []
  below = []

  col_limit = int(app.grid_size-1)
  row_limit = math.ceil(app.grid_size/2-1)

  coef = sz*math.cos(math.pi/6)

  for row in range(row_limit):

    for col in range(col_limit):

      # Add to Start
      colPos = WIDTH/2 - col_offset * (row+1)
      rowPos = app.size + col*coef + row*coef/2 + coef/2

      above.append(hex(colPos, rowPos, sz, get_Color(), VERTICAL))

      # Add to end
      colPos = WIDTH/2 + col_offset * (row+1)
      rowPos = app.size + col*coef + row*coef/2 + coef/2

      below.append(hex(colPos, rowPos, sz, get_Color(), VERTICAL))

    app.grid.insert(0,above)
    app.grid.append(below)
    
    col_limit-=1

    above = []
    below = []

def get_cell(cell):

  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      return app.grid[row][col].center_color

def swap_grid():

  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      get_cell(app.grid[row][col])

  return

def cell_count():

  return
  count=0

  for row in range(len(app.grid)):
    
    print(len(app.grid[row]))

def draw_board():
    
  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      app.grid[row][col].draw()

def draw_window():

  WIN.fill(BACKGROUND)

  draw_board()

  w = WIDTH/(app.grid_size+1)

  # pygame.draw.rect(WIN, (128,0,0), (w/2, w/2, WIDTH-w, HEIGHT-w), 1, 15)

  if app.current_cell is not None:
    WIN.blit(WINNER_FONT.render(str(app.current_cell.id), 1, WHITE), (20, 20))

  pygame.display.update()

# Event handlers ==================================================================================

def handle_keys(event):

  key = event.key

  if event.mod & pygame.KMOD_CTRL:

    if key == pygame.K_SPACE: toggle_orientation()

  else:

    if   key == pygame.K_q:     print('Up Left')
    elif key == pygame.K_w:     print("Up")
    elif key == pygame.K_e:     print("Up Right")
    elif key == pygame.K_a:     print("Down Left")
    elif key == pygame.K_s:     print("Down")
    elif key == pygame.K_d:     print("Down Right")

def toggle_orientation():

  if app.orientation == HORIZONTAL:
    
    app.orientation = VERTICAL
    app.grid.clear()

    load_grid_vertical()

  else:                 
    
    app.orientation = HORIZONTAL
    app.grid.clear()

    load_grid_horizontal()
    
def increment_grid():

  app.grid_size += 2
  app.size = math.floor(WIDTH/(app.grid_size+1))
  app.grid.clear()

  load_grid()

def decrement_grid():

  if app.grid_size>2:

    app.grid_size -= 2  
    app.size = math.floor(WIDTH/(app.grid_size+1))
    app.grid.clear()

    load_grid()

def handle_click(button):

  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      app.grid[row][col].click()  

  # return

  # print(pygame.mouse.get_pos())

  # if   button == LEFT:        print('left')       
  # elif button == CENTRE:      print('Wheel')
  # elif button == RIGHT:       print('rightt')
  # elif button == SCROLL_UP:   increment_grid()
  # elif button == SCROLL_DOWN: decrement_grid()

def handle_move():

  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      app.grid[row][col].move()  

# Main Loop =======================================================================================

# print(app.size)

load_grid()

swap_grid()

def main():

  clock = pygame.time.Clock()

  run = True

  while run:

    clock.tick(app.fps)

    for event in pygame.event.get():
      
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
      
      if event.type == pygame.KEYUP:         handle_keys(event)
      if event.type == pygame.MOUSEBUTTONUP: handle_click(event.button)
      
      handle_move()
  
    draw_window()  
    
if __name__ == "__main__":
  main()



