"""
  Ideas

    Game Call Phaze - overlapping patterns (rotate, etc)

"""

#region - hexy \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#region - Initialization ======================================================

import sys

# p(sys.version)

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

#endregion - Initialization ------------------------------------------------------

#region - Constants ===========================================================

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

HEALTH_FONT = pygame.font.SysFont('comicsans', 24)
WINNER_FONT = pygame.font.SysFont('comicsans', 32)

#endregion - Constants --------------------------------------------------------

def p(s): print(str(s))

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

#region - Objects =============================================================

class App:

  def __init__(self, size) -> None:
      
    self.size = size

    self.grid = []            # list holding the cell objects
    self.swap = []            # list of references to cell objects
    self.current_cell = None  # which hexagonal cell has the focus
    self.grid_size = 7        # of hexagonal layers - defaults to 7
    self.fps = 60
    self.orientation = VERTICAL

class point:

  def __init__(self, x, y) -> None:
    
    self.x = x
    self.y = y

class hex:

  id = 0

  def __init__(self, x, y, diameter, color, orientation) -> None:

    self.id = hex.id                    # identification Number

    hex.id+=1                           # Increment overall object count

    self.x = int(x)                     # horizontal position of centre
    self.y = int(y)                     # vertical position of centre
    
    self.row = 0                        # row of cell in grid array
    self.col = 0                        # col of cell in grid array

    self.diameter = diameter            # full diameter width of hexagon
    self.radius = diameter/2            # distance from center to corner point
    
    self.center = point(x, y)           # Center Point
    self.points = []                    # list of 6 vertex points
    self.border = []                    # list of 6 vertex points of border

    self.orientation = orientation      # HORIZONTAL or VERTICAL rows
    
    self.color = color                  # Background Color
    self.center_color = color           # Interior Color

    self.hit = False                    # Mouse is currently over the cellw
    
    # References to adjacent cells - Cells wrap
    self.top = None                     # Reference to the cell above
    self.bottom = None                  # Reference to the cell below

    self.upper_right = None             # Reference to the cell above right
    self.upper_left = None              # Reference to the cell above left
    
    self.lower_right = None             # Reference to the cell below right
    self.lower_left = None              # Reference to the cell below left

    self.left = None                    # Reference to the cell left
    self.right = None                   # Reference to the cell right

    # Aliases
    sX = self.x
    sY = self.y
    r = self.radius
    pts = self.points
    brd = self.border

    # Calculate Corner Points
    if self.orientation == HORIZONTAL:

      # Offsets
      oX = math.cos(math.pi/6)*self.radius # Offset x
      oY = math.sin(math.pi/6)*self.radius # Offset Y

      pts.append((sX,      sY + r ))
      pts.append((sX + oX, sY + oY))
      pts.append((sX + oX, sY - oY))
      pts.append((sX,      sY - r ))
      pts.append((sX - oX, sY - oY))
      pts.append((sX - oX, sY + oY))

      r  = r*0.965
      oX = oX*0.965
      oY = oY*0.965

      brd.append((sX,      sY + r ))
      brd.append((sX + oX, sY + oY))
      brd.append((sX + oX, sY - oY))
      brd.append((sX,      sY - r ))
      brd.append((sX - oX, sY - oY))
      brd.append((sX - oX, sY + oY))

    else: # Vertical
      
      # Offsets
      oX = math.cos(math.pi/3)*self.radius # Offset x
      oY = math.sin(math.pi/3)*self.radius # Offset Y

      pts.append((sX + r,  sY))
      pts.append((sX + oX, sY - oY ))
      pts.append((sX - oX, sY - oY))
      pts.append((sX - r,  sY))
      pts.append((sX - oX, sY + oY))
      pts.append((sX + oX, sY + oY))

      r  = r*0.96
      oX = oX*0.96
      oY = oY*0.96

      brd.append((sX + r,  sY))
      brd.append((sX + oX, sY - oY ))
      brd.append((sX - oX, sY - oY))
      brd.append((sX - r,  sY))
      brd.append((sX - oX, sY + oY))
      brd.append((sX + oX, sY + oY))

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

    pygame.gfxdraw.filled_polygon(WIN, self.points, self.color)    
    pygame.gfxdraw.filled_circle(WIN, self.x, self.y, int(app.size*0.25), self.center_color)

    text = HEALTH_FONT.render(str(self.id),True,WHITE)
    text_rect = text.get_rect(center=(self.x, self.y))
    WIN.blit(text,text_rect)

    if self.hit:
      
      app.current_cell = self

      pygame.draw.polygon(WIN, WHITE, self.border, width=5)
      # pygame.gfxdraw.aapolygon(w, self.points, VASARELY_COLORS.RED.value)

      # draw_text()

      # draw_text = WINNER_FONT.render('3', 1, WHITE)

      # WIN.blit(WINNER_FONT.render(str(self.x)+','+str(self.y), 1, WHITE), (self.x, self.y))

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
      p(str(self.x) + ',' + str(self.y))
      p(app.current_cell.id)

#endregion - Objects ----------------------------------------------------------

app = App(HEIGHT/(7+1))
app.size = HEIGHT/(app.grid_size+1)

#region - Load Grid ===========================================================

def load_grid():

  if   app.orientation == HORIZONTAL: load_grid_horizontal()
  elif app.orientation == VERTICAL:   load_grid_vertical()

def load_grid_horizontal():

  p('HORIZONTAL')

  hex.id = 0

  # Add center row
  sz = app.size*1/math.cos(math.pi/6)
  
  app.grid.clear
  app.swap.clear

  temp = []

  for cell in range(app.grid_size):

    colPos = app.size + cell*sz*math.cos(math.pi/6)

    h=hex(colPos, HEIGHT/2, sz, get_Color(), app.orientation)

    temp.append(h)
    app.swap.append(h)

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

      h = hex(colPos, rowPos, sz, get_Color(), app.orientation)

      above.append(h)
      app.swap.append(h)
      # above.append(hex(colPos, rowPos, sz, (hex.counter,hex.counter, hex.counter)))

      # Add to end
      rowPos = HEIGHT/2 + row_offset * (row+1)
      colPos = app.size + col*coef + row*coef/2 + coef/2

      h = hex(colPos, rowPos, sz, get_Color(), app.orientation)

      below.append(h)
      app.swap.append(h)
      # below.append(hex(colPos, rowPos, sz, (hex.counter,hex.counter, hex.counter)))

    app.grid.insert(0,above)
    app.grid.append(below)
    
    col_limit-=1

    above = []
    below = []

  # p(app.swap)

  # p(hex.counter)

def load_grid_vertical():

  try:

    limit = app.grid_size
    sz = app.size*1/math.cos(math.pi/6)

    cof3 = math.sin(math.pi/3)
    cof6 = math.sin(math.pi/6)

    for row in range(limit):

      temp = []

      for col in range(limit):
        
        h = hex(sz + col*sz*cof3, sz + row*sz*cof3, sz, get_Color(), app.orientation)
        
        h.row = row
        h.col = col

        temp.append(h)

      app.grid.append(temp)

    count=0

    for row in range(len(app.grid)):
      for col in range(len(app.grid[row])):
        count+=1

    p('Count: ' + str(count))

  except:

    p('Load Grid Horizontal Error' + Exception.__name__)

def _load_grid_vertical():

  p('VERTICAL')
  hex.id = 0

  # Add center row
  sz = app.size*1/math.cos(math.pi/6)
  
  app.grid.clear
  app.swap.clear

  temp = []
  
  # Add Center Column
  for cell in range(app.grid_size):

    colPos = app.size + cell*sz*math.cos(math.pi/6)

    h = hex(WIDTH/2, colPos, sz, get_Color(), app.orientation)

    # h.row = row
    # h.col = col

    temp.append(h)
    app.swap.append(h)
    
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

      h = hex(colPos, rowPos, sz, get_Color(), app.orientation)
      
      h.row = row
      h.col = col

      above.append(h)
      app.swap.append(h)

      # Add to end
      colPos = WIDTH/2 + col_offset * (row+1)
      rowPos = app.size + col*coef + row*coef/2 + coef/2

      h = hex(colPos, rowPos, sz, get_Color(), app.orientation)

      h.row = row
      h.col = col

      below.append(h)
      app.swap.append(h)

    app.grid.insert(0,above)
    app.grid.append(below)
    
    col_limit-=1

    above = []
    below = []

    # p(app.swap)

#endregion - Load Grid --------------------------------------------------------

#region - Commands ============================================================

def connect_grid():

  def load_up_down():

    try:
      
      g = app.grid

      for row in range(len(g)):
        for col in range(len(g[row])):
          
          if row == 0: g[col][row].top = g[len(g)-1][row]
          else:        g[col][row].top = g[col][row-1]

    except:

      p('ERROR LOADING UP / DOWN ' + str(row) + ', ' + str(col))

  load_up_down()

def swap_grid():

  def get_cell():
    
    return app.swap[int(random.random()*len(app.swap))]

  for cell in range(len(app.swap)):
    
    temp = app.swap[cell].center_color    
    random_cell = get_cell()
    
    while (app.swap[cell].center_color == random_cell.color) or \
          (app.swap[cell].color == random_cell.center_color):

      random_cell = get_cell()

    app.swap[cell].center_color = random_cell.center_color
    random_cell.center_color = temp

def draw_board():
    
  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      app.grid[row][col].draw()

def draw_window():

  WIN.fill(BACKGROUND)

  draw_board()

  w = WIDTH/(app.grid_size+1)

  # pygame.draw.rect(WIN, (128,0,0), (w/2, w/2, WIDTH-w, HEIGHT-w), 1, 15)

  if app.current_cell.top is not None:
    WIN.blit(WINNER_FONT.render(str(app.current_cell.top.id), 1, WHITE), (20, 20))

  pygame.display.update()

def up():

  g = app.grid
  c = app.current_cell
  length = len(app.grid)
  temp_color = app.grid[0][c.col].center_color
  
  for row in range(length):
    
    if row==length-1: g[row][c.col].center_color = temp_color
    else:             g[row][c.col].center_color = g[row+1][c.col].center_color

def down():
  
  g = app.grid
  c = app.current_cell
  length = len(app.grid)
  temp_color = app.grid[length-1][c.col].center_color
  
  for row in reversed(range(length)):
    
    if row==0: g[row][c.col].center_color = temp_color
    else:      g[row][c.col].center_color = g[row-1][c.col].center_color

def up_left():    return
def up_right():   return
def down_left():  return
def down_right(): return
def right():      return
def left():       return

def toggle_orientation():

  if app.orientation == HORIZONTAL:
    
    app.orientation = VERTICAL
    app.grid.clear()
    app.swap.clear()

    load_grid()

  else:                 
    
    app.orientation = HORIZONTAL
    app.grid.clear()
    app.swap.clear()

    load_grid()
    
  swap_grid()

def reset_grid():

  hex.id =  0
  
  app.grid.clear()
  app.swap.clear()

  load_grid()     # Load the grid... duh
  connect_grid()  # Load cell adjacentcy (above/below etc)
  swap_grid()     # Scramble the inner circles

def increment_grid():

  app.grid_size += 2
  app.size = math.floor(WIDTH/(app.grid_size+1))

  reset_grid()

def decrement_grid(): 

  if app.grid_size>3:

    app.grid_size -= 2  
    app.size = math.floor(WIDTH/(app.grid_size+1))

    reset_grid()

#endregion - Commands ---------------------------------------------------------

#region - Events ==============================================================

def handle_keys(event):

  key = event.key

  if event.mod & pygame.KMOD_CTRL:

    if   key == pygame.K_SPACE: toggle_orientation()
    elif key == pygame.K_UP:    increment_grid()
    elif key == pygame.K_DOWN:  decrement_grid()

  else:

    if   key == pygame.K_w:   up()
    elif key == pygame.K_s:   down()
    elif key == pygame.K_q:   up_left()
    elif key == pygame.K_e:   up_right()
    elif key == pygame.K_a:   down_left()    
    elif key == pygame.K_d:   down_right()

def handle_click(event):

  # for row in range(len(app.grid)):
  #   for col in range(len(app.grid[row])):
  #     app.grid[row][col].click()  

  # return

  # p(pygame.mouse.get_pos())

  if   event.button == LEFT:          

    for row in range(len(app.grid)):
      for col in range(len(app.grid[row])):
        app.grid[row][col].click()  

  elif event.button == SCROLL_UP:   increment_grid()
  elif event.button == SCROLL_DOWN: decrement_grid()

  # elif event.button == CENTRE:      p('Wheel')
  elif event.button == RIGHT:
    
    reset_grid()

def handle_move():

  for row in range(len(app.grid)):
    for col in range(len(app.grid[row])):
      app.grid[row][col].move()  

#endregion - Events -----------------------------------------------------------

reset_grid()
app.current_cell = app.grid[0][0]

#region - Main Loop ===========================================================

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
      if event.type == pygame.MOUSEBUTTONUP: handle_click(event)
      
      handle_move()
  
    draw_window()  
    
if __name__ == "__main__":
  main()

#endregion - Main Loop --------------------------------------------------------

#endregion - hexy /////////////////////////////////////////////////////////////
