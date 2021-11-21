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
from pygame.locals import *
from pygame import gfxdraw
from pygame.constants import KEYUP
import os
import math
import random
import helper

from enum import IntEnum
from enum import Enum
from array import *

from helper import board

pygame.font.init()
pygame.mixer.init()
pygame.init()

pygame.RESIZABLE

import ctypes  # An included library with Python install

def Mbox(title, text, style):
  
  return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#endregion - Initialization ------------------------------------------------------

#region - Constants ===========================================================

# Initial Display Size
WIDTH  = 1000
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Habitat for Humanity Game")

# Color Constants
WHITE  = (255,255,255,255)
BLACK  = (  0,  0,  0,255)
RED    = (255,  0,  0,255)
GREEN  = (  0,255,  0,255)
BLUE   = (  0,  0,255,255)
YELLOW = (255,255,  0,255)

BACKGROUND = (8,8,8)

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

class DIRECTIONS(Enum):

  UP         = 0
  DOWN       = 1
  UP_LEFT    = 2
  UP_RIGHT   = 3
  DOWN_LEFT  = 4
  DOWN_RIGHT = 5

class VASARELY_COLORS(Enum):

  PINK        = (181, 42,142)
  PURPLE      = ( 90, 24,120)

  BLUE        = ( 39,105,176)
  CYAN        = ( 79,168,219)
  NAVY        = ( 42, 40,143)

  DORANGE     = (227,102, 79)
  LORANGE     = (250,147, 95)

  LYELLOW     = (244,255,173)
  DYELLOW     = (247,194,119)

  LGREEN      = (  0,173,147)
  DGREEN      = (  0,110,110)

  RED         = (222, 33, 49)
  MAROON      = (135, 26, 35)
  PEACH       = (247,194, 11) 

  BLACK       = (32,32,32)
  GRAY        = (122,135,191)
  
  TRANSPARENT = (255,0,0,0)

class COLORS(IntEnum):

  PINK        = 0
  PURPLE      = 1
  CYAN        = 2
  NAVY        = 3
  BLUE        = 4
  DORANGE     = 5
  LORANGE     = 6
  LYELLOW     = 7
  DYELLOW     = 8
  LGREEN      = 9
  DGREEN      = 10
  PEACH       = 11
  RED         = 12
  MAROON      = 13
  BLACK       = 14
  GRAY        = 15
  TRANSPARENT = 16

BULLET_HIT_SOUND  = pygame.mixer.Sound(os.path.join('C:/Users/ssbbc/Desktop/Brad/python/assets', 'Grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('C:/Users/ssbbc/Desktop/Brad/python/assets', 'Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 24)
WINNER_FONT = pygame.font.SysFont('comicsans', 32)

#endregion - Constants --------------------------------------------------------

def p(s): print(str(s))

def get_Color():

  clr = int(random.random()*16)

  ret = VASARELY_COLORS.PINK.value

  if   clr == COLORS.PINK:        ret = VASARELY_COLORS.PINK.value
  elif clr == COLORS.PURPLE:      ret = VASARELY_COLORS.PURPLE.value
  elif clr == COLORS.CYAN:        ret = VASARELY_COLORS.CYAN.value
  elif clr == COLORS.NAVY:        ret = VASARELY_COLORS.NAVY.value
  elif clr == COLORS.BLUE:        ret = VASARELY_COLORS.BLUE.value
  elif clr == COLORS.DORANGE:     ret = VASARELY_COLORS.DORANGE.value
  elif clr == COLORS.LORANGE:     ret = VASARELY_COLORS.LORANGE.value
  elif clr == COLORS.LYELLOW:     ret = VASARELY_COLORS.LYELLOW.value
  elif clr == COLORS.DYELLOW:     ret = VASARELY_COLORS.DYELLOW.value
  elif clr == COLORS.LGREEN:      ret = VASARELY_COLORS.LGREEN.value
  elif clr == COLORS.DGREEN:      ret = VASARELY_COLORS.DGREEN.value
  elif clr == COLORS.PEACH:       ret = VASARELY_COLORS.PEACH.value
  elif clr == COLORS.RED:         ret = VASARELY_COLORS.RED.value
  elif clr == COLORS.MAROON:      ret = VASARELY_COLORS.MAROON.value
  elif clr == COLORS.BLACK:       ret = VASARELY_COLORS.BLACK.value
  elif clr == COLORS.GRAY:        ret = VASARELY_COLORS.GRAY.value
  elif clr == COLORS.TRANSPARENT: ret = VASARELY_COLORS.TRANSPARENT.value
  else:                           ret = VASARELY_COLORS.GRAY.value

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

  def __init__(self, cell_size, grid_size) -> None:
      
    self.cell_size = cell_size
    self.grid_size = grid_size    # of hexagonal layers - defaults to 7

    self.grid = []                # list holding the cell objects
    self.swap = []                # list of references to cell objects

    self.current_cell = None      # which hexagonal cell has the focus
    
    self.fps = 60                 # Frames Per Second
    self.orientation = VERTICAL
    self.moves = 0

    self.mouseX = 0
    self.mouseY = 0

class point:

  def __init__(self, x, y) -> None:
    
    self.x = x
    self.y = y

def semi_perimeter(a,b,c):  # a, b, and c are lengths of the triangles sides

  return (a+b+c)/2

def triangle_area(a,b,c):

  s = semi_perimeter(a,b,c)

  temp = s*(s-a)*(s-b)*(s-c)

  retval = 0

  if temp > 0: retval = math.floor(math.sqrt(temp))
  
  return retval

class hex:

  id = 0
  orientation = VERTICAL
  area = 0
  perimeter = 0
  side_length = 0
  tri_area = 0

  def __init__(self, x, y, diameter, color) -> None:

    self.id = hex.id                                # identification Number

    hex.id+=1                                       # Increment overall object count

    self._x = int(x)                                # horizontal position of centre
    self._y = int(y)                                # vertical position of centre
    # self._z = int(z)                                # vertical position of centre

    self.row = 0                                    # row of cell in grid array
    self.col = 0                                    # col of cell in grid array

    self.diameter = diameter                        # full diameter width of hexagon
    self.radius = diameter/2                        # distance from center to corner point
    self.inradius = self.radius*math.cos(math.pi/6) # distance from center to center of a side
    self.maximal_diameter = self.radius * 2         # twice the radius         
    self.minimal_diameter = self.inradius * 2       # twice the inradius

    self.center = point(x, y)                       # Center Point
    self.points = []                                # list of 6 vertex points
    self.border = []                                # list of 6 vertex points of border

    self.color = color                              # Background Color
    self.center_color = color                       # Interior Color

    self.hit = False                                # Mouse is currently over the cell
    self.active = True                              # Cell has not been solved

    # References to adjacent cells - Cells wrap
    self.top = None                                 # cell above
    self.bottom = None                              # cell below

    self.upper_right = None                         # cell above right
    self.upper_left = None                          # cell above left

    self.lower_right = None                         # cell below right
    self.lower_left = None                          # cell below left

    self.left = None                                # cell left
    self.right = None                               # cell right
    
    # Aliases
    sX = self._x
    sY = self._y
    r = self.radius
    pts = self.points
    brd = self.border

    # Calculate Corner Points
    if self.orientation == HORIZONTAL:

      # Offsets
      oX = self.inradius # Offset x
      oY = math.sin(math.pi/6)*self.radius # Offset Y

      pts.append((sX,      sY + r ))
      pts.append((sX + oX, sY + oY))
      pts.append((sX + oX, sY - oY))
      pts.append((sX,      sY - r ))
      pts.append((sX - oX, sY - oY))
      pts.append((sX - oX, sY + oY))

      r  = r*0.97
      oX = oX*0.97
      oY = oY*0.97

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

      r  = r*0.97
      oX = oX*0.97
      oY = oY*0.97

      brd.append((sX + r,  sY))
      brd.append((sX + oX, sY - oY ))
      brd.append((sX - oX, sY - oY))
      brd.append((sX - r,  sY))
      brd.append((sX - oX, sY + oY))
      brd.append((sX + oX, sY + oY))

    if hex.area == 0:
      
      # p("Calculate Area")
      pts = self.points

      a = math.floor(math.dist((self.center.x, self.center.y), (pts[0][X], pts[0][Y])))
      b = math.floor(math.dist((self.center.x, self.center.y), (pts[1][X], pts[1][Y])))
      c = math.floor(math.dist((pts[0][X], pts[5][0]), (pts[1][X], pts[1][Y])))

      hex.perimeter = c * 6 # Perimeter is six times side length
      hex.side_length = a

      hex.tri_area = math.floor(triangle_area(a,b,c))
      hex.area = hex.tri_area * 6

      # p(str(hex.area) + ", " + str(hex.perimeter))

  def reset(self):

    id = 0

  def draw(self):

    def draw_text():
      
      pts = self.points

      WIN.blit(WINNER_FONT.render('0', 1, WHITE), (pts[0][X], pts[0][Y]))
      WIN.blit(WINNER_FONT.render('1', 1, WHITE), (pts[1][X], pts[1][Y]))
      WIN.blit(WINNER_FONT.render('2', 1, WHITE), (pts[2][X], pts[2][Y]))
      WIN.blit(WINNER_FONT.render('3', 1, WHITE), (pts[3][X], pts[3][Y]))
      WIN.blit(WINNER_FONT.render('4', 1, WHITE), (pts[4][X], pts[4][Y]))
      WIN.blit(WINNER_FONT.render('5', 1, WHITE), (pts[5][X], pts[5][Y]))

    pygame.gfxdraw.filled_polygon(WIN, self.points, self.color)
    pygame.gfxdraw.filled_circle(WIN, self._x, self._y, int(app.cell_size*0.25), self.center_color)

    if app.current_cell == self: pygame.draw.polygon(WIN, WHITE, self.border, width=3)

    # text = HEALTH_FONT.render(str(self.id),True,WHITE)
    # text_rect = text.get_rect(center=(self.x, self.y))
    # WIN.blit(text,text_rect)

    if self.active == False:

      pygame.draw.polygon(WIN, VASARELY_COLORS.GRAY.value, self.points, width=1)
      self.color = VASARELY_COLORS.TRANSPARENT.value

    if self.hit:

      pygame.draw.polygon(WIN, WHITE, self.border, width=1)
      # pygame.gfxdraw.aapolygon(w, self.points, VASARELY_COLORS.RED.value)

      # text = HEALTH_FONT.render(str(self.row) + ', ' + str(self.col), True, WHITE)
      text = HEALTH_FONT.render(str(self.active), True, WHITE)
      text_rect = text.get_rect(center=(self._x, self._y))
      WIN.blit(text, text_rect)

      # if self.top != None:          pygame.draw.line(WIN, RED, (self._x, self._y), (self.top._x, self.top._y), width=5)
      # if self.bottom != None:       pygame.draw.line(WIN, GREEN, (self._x, self._y), (self.bottom._x, self.bottom._y), width=5)
      
      # if self.upper_left != None:   pygame.draw.line(WIN, YELLOW, (self._x, self._y), (self.upper_left._x, self.upper_left._y), width=5)
      # if self.upper_right != None:  pygame.draw.line(WIN, BLUE, (self._x, self._y), (self.upper_right._x, self.upper_right._y), width=5)
      
      # if self.lower_left != None:   pygame.draw.line(WIN, BLACK, (self._x, self._y), (self.lower_left._x, self.lower_left._y), width=5)
      # if self.lower_right != None:  pygame.draw.line(WIN, WHITE, (self._x, self._y), (self.lower_right._x, self.lower_right._y), width=5)

      # draw_text()

      # draw_text = WINNER_FONT.render('3', 1, WHITE)

      # WIN.blit(WINNER_FONT.render(str(self._x)+','+str(self._y), 1, WHITE), (self._x, self._y))

      # WIN.blit(WINNER_FONT.render('0', 1, WHITE), (self.points[0][X]-20, self.points[0][Y]-10))
      # WIN.blit(WINNER_FONT.render('1', 1, WHITE), (self.points[1][X]-15, self.points[1][Y]+10))
      # WIN.blit(WINNER_FONT.render('2', 1, WHITE), (self.points[2][X], self.points[2][Y]))
      # WIN.blit(WINNER_FONT.render('3', 1, WHITE), (self.points[3][X], self.points[3][Y]))
      # WIN.blit(WINNER_FONT.render('4', 1, WHITE), (self.points[4][X], self.points[4][Y]))
      # WIN.blit(WINNER_FONT.render('5', 1, WHITE), (self.points[5][X], self.points[5][Y]))

  def draw_links(self):

    if self.top != None:          pygame.draw.line(WIN, RED, (self._x, self._y), (self.top._x, self.top._y), width=5)
    if self.bottom != None:       pygame.draw.line(WIN, GREEN, (self._x, self._y), (self.bottom._x, self.bottom._y), width=5)
    
    if self.upper_left != None:   pygame.draw.line(WIN, YELLOW, (self._x, self._y), (self.upper_left._x, self.upper_left._y), width=5)
    if self.upper_right != None:  pygame.draw.line(WIN, BLUE, (self._x, self._y), (self.upper_right._x, self.upper_right._y), width=5)
    
    if self.lower_left != None:   pygame.draw.line(WIN, BLACK, (self._x, self._y), (self.lower_left._x, self.lower_left._y), width=5)
    if self.lower_right != None:  pygame.draw.line(WIN, WHITE, (self._x, self._y), (self.lower_right._x, self.lower_right._y), width=5)

  def hitTest(self):
    
    def get_area(p0, p1):
    
      retval = 0

      x = app.mouseX
      y = app.mouseY

      a = math.dist((p0[X], p0[Y]), (p1[X], p1[Y]))
      b = math.dist((x,     y),     (p0[X], p0[Y]))
      c = math.dist((x,     y),     (p1[X], p1[Y]))

      area = triangle_area(a,b,c)

      if area>0: retval = area
      else:      retval = math.inf

      return retval

    def rectangle():
      
      retval = False

      x = app.mouseX
      y = app.mouseY

      assert x>=0, "Rectangle X is fucked"
      assert y>=0, "Rectangle Y is fucked"

      if(x>self.points[2][X] and
         x<self.points[1][X] and
         y>self.points[2][Y] and
         y<self.points[4][Y]): retval = True

      return retval

    def right_triangle():
      
      retval = False

      pts = self.points

      A_area = get_area(pts[0],pts[1])
      B_area = get_area(pts[1],pts[5])
      C_area = get_area(pts[5],pts[0])

      area = A_area + B_area + C_area

      a = math.dist((pts[0][X], pts[0][Y]), (pts[1][X], pts[1][Y]))
      b = math.dist((pts[1][X], pts[1][Y]), (pts[5][X], pts[5][Y]))
      c = math.dist((pts[5][X], pts[5][Y]), (pts[0][X], pts[0][Y]))

      t_area = triangle_area(a,b,c)

      if(abs(area - t_area) <= 2):

        retval = True

      return retval

    def left_triangle():
      
      retval = False

      pts = self.points

      A_area = get_area(pts[2],pts[3])
      B_area = get_area(pts[3],pts[4])
      C_area = get_area(pts[4],pts[2])

      area = A_area + B_area + C_area

      a = math.dist((pts[2][X], pts[2][Y]), (pts[3][X], pts[3][Y]))
      b = math.dist((pts[3][X], pts[3][Y]), (pts[4][X], pts[4][Y]))
      c = math.dist((pts[4][X], pts[4][Y]), (pts[2][X], pts[2][Y]))

      t_area = triangle_area(a,b,c)

      # p(area - t_area)

      if(abs(area - t_area) <= 2):

        retval = True

      return retval

    x = app.mouseX
    y = app.mouseY

    if math.dist((self._x, self._y), (x, y))<=self.radius:
      
      if rectangle() or right_triangle() or left_triangle():

        self.hit = True

      else: 

        self.hit = False

    else:
      
      self.hit = False

  def move(self):

    self.hitTest()

  def click(self) -> None:

    if self.hit:

      app.current_cell = self
      # p(self.id)
      if self.center_color == self.color:

        self.color        = VASARELY_COLORS.TRANSPARENT.value
        self.center_color = VASARELY_COLORS.TRANSPARENT.value

#endregion - Objects ----------------------------------------------------------

m = 7
app = App(HEIGHT/(m+1), m)
app.cell_size = HEIGHT/(app.grid_size+1)

#region - Load Grid ===========================================================

def load_grid():

  if   app.orientation == HORIZONTAL: load_grid_horizontal()
  elif app.orientation == VERTICAL:   load_grid_vertical()

def load_grid_horizontal():

  p('Horizontal')

  radius = app.cell_size*1/math.cos(math.pi/6)
  limit = app.grid_size
  inRadius = radius*math.cos(math.pi/6)

  for row in range(limit):
    
    temp = []

    for col in range(limit):
    
      colPos = 2.5 * radius/2 + (0.75 * radius) * col

      if col%2 == 0: rowPos = inRadius * 0.75 + row * inRadius + inRadius/2
      else:          rowPos = inRadius * 0.75 + row * inRadius

      h = hex(colPos, rowPos, radius, get_Color())

      h.col = col
      h.row = row

      temp.append(h)

    app.grid.append(temp)

def load_grid_vertical():
 
  p('VERTICAL')

  radius = app.cell_size*1/math.cos(math.pi/6)
  limit = app.grid_size
  inRadius = radius*math.cos(math.pi/6)

  for row in range(limit):
    
    temp = []

    for col in range(limit):
    
      x = 2.5 * radius/2 + (0.75 * radius) * col

      if col%2 == 0: y = inRadius * 0.75 + row * inRadius + inRadius/2
      else:          y = inRadius * 0.75 + row * inRadius

      h = hex(x, y, radius, get_Color())

      h.col = col
      h.row = row

      # if row == 0 and col == 0: h.active = False

      temp.append(h)

    app.grid.append(temp)

def shuffle_grid():

  def get_cell():
    
    length = len(app.grid)

    return app.grid[int(random.random()*length)] \
                   [int(random.random()*length)]

  for rowIndex, row in enumerate(app.grid):
    for colIndex, col in enumerate(row):
      
      cell = app.grid[rowIndex][colIndex]
      temp = cell.center_color

      random_cell = get_cell()

      while (cell.center_color == random_cell.color) or \
            (cell.color == random_cell.center_color):
      
        random_cell = get_cell()

      cell.center_color = random_cell.center_color
      random_cell.center_color = temp

#endregion - Load Grid --------------------------------------------------------

#region - Commands ============================================================

def get_count() -> int:

  try:

    count=0 

    for row in app.grid:
      for col in row:
        count+=1

    return count
  
  except:

    Mbox('Exception - Hexy.py', 'get_count() - ' + Exception.__name__, 1)

def connect_grid():

  def load_up_down():

    # try:

    g = app.grid

    for rowIndex, row in enumerate(g):
      for colIndex, cell in enumerate(row):
        
        # Top 
        if rowIndex == 0:                  cell.top = g[len(g)-1][colIndex]
        else:                              cell.top = g[rowIndex-1][colIndex]

        # Bottom
        if rowIndex == len(g)-1:           cell.bottom = g[0][colIndex]
        else:                              cell.bottom = g[rowIndex+1][colIndex]

        # Upper Left
        if rowIndex == 0:                  cell.upper_left = g[len(g)-1][colIndex-1]
        else:                              cell.upper_left = g[rowIndex-1][colIndex-1]

        # Upper Right
        # if rowIndex == 1:
          
        #   if rowIndex==6: cell.upper_right = g[0][3]
        #   else:           cell.upper_right = g[len(g)-1][colIndex]

        # elif rowIndex%2 == 0:

        #   if rowIndex==6: cell.upper_right = g[0][3]
        #   else:           cell.upper_right = g[len(g)][colIndex]

        # else:
          
        #   if rowIndex==6: cell.upper_right = g[0][3]
        #   else:           cell.upper_right = g[len(g)][colIndex]

        # # Lower Left
        # if rowIndex == 6 or colIndex == 1: cell.lower_left = None
        # else:                              cell.lower_left = g[rowIndex][colIndex-1]

        # # Lower Right
        # if rowIndex == 6 or colIndex == 6: cell.lower_right = None
        # else:                              cell.lower_right = g[rowIndex][colIndex+1]

    # except:

    #   p('ERROR LOADING UP / DOWN ' + str(row) + ', ' + str(col))

  load_up_down()

  x = 1
  assert x > 0, 'Only positive numbers are allowed'
  # print('x is a positive number.')
  
def draw_board():
    
  for row in app.grid:
    for cell in row:
      cell.draw()

  app.current_cell.draw_links()

def draw_window():

  # try:

    WIN.fill(BACKGROUND)

    draw_board()
    
    

    w = WIDTH/(app.grid_size+1)

    # pygame.draw.rect(WIN, (128,0,0), (w/2, w/2, WIDTH-w, HEIGHT-w), 1, 15)

    if app.current_cell is not None:
      WIN.blit(WINNER_FONT.render(str(app.current_cell.row), 1, WHITE), (20, 20))
      WIN.blit(WINNER_FONT.render('Moves: ' + str(app.moves), 1, WHITE), (20, 50))

    pygame.display.update()

  # except:

  #   Mbox('Exception - Hexy.py', 'draw_window() - ' + Exception.__name__, 1)

def up():

  g = app.grid
  col = app.current_cell.col
  length = len(g)-1

  temp_color = app.grid[0][col].center_color

  for rowIndex, row in enumerate(g):
    
    if rowIndex == length: row[col].center_color = temp_color
    else:                  row[col].center_color = g[rowIndex+1][col].center_color

  increment_moves()

def down():

  g = app.grid
  colIndex = app.current_cell.col
  length = len(g)
  
  temp_color = g[length-1][colIndex].center_color
  
  for rowIndex in reversed(range(len(g))):
    
    if rowIndex == 0: g[rowIndex][colIndex].center_color = temp_color
    else:             g[rowIndex][colIndex].center_color = g[rowIndex-1][colIndex].center_color

  increment_moves()

def increment_moves(): app.moves+=1

def up_left():    increment_moves()
def up_right():   increment_moves()
def down_left():  increment_moves()
def down_right(): increment_moves()
def right():      increment_moves()
def left():       increment_moves()

def toggle_orientation():

  if app.orientation == HORIZONTAL:
    
    app.orientation = VERTICAL
    hex.orientation = VERTICAL
  
  else:                 
    
    app.orientation = HORIZONTAL
    hex.orientation = HORIZONTAL
    
  app.grid.clear()
  app.swap.clear()

  load_grid()
  connect_grid()  # Load cell adjacentcy (above/below etc)
  shuffle_grid()

def reset_grid():

  hex.id =  0
  hex.area = 0

  app.moves = 0
  app.grid.clear()

  load_grid()     # Load the grid... duh
  connect_grid()  # Load cell adjacentcy (above/below etc)
  shuffle_grid()  # Scramble the inner circles

def increment_grid():

  app.grid_size += 2
  app.cell_size = math.floor(WIDTH/(app.grid_size+1))

  reset_grid()

def decrement_grid(): 

  if app.grid_size>4:

    app.grid_size -= 2  
    app.cell_size = math.floor(WIDTH/(app.grid_size+1))

    reset_grid()

def check_cells():

  for row in app.grid:
    for cell in row:

        if cell.color == cell.center_color:
          cell.color        = VASARELY_COLORS.TRANSPARENT.value
          cell.center_color = VASARELY_COLORS.TRANSPARENT.value
          cell.active = False

def current_cell_move(direction):

  if direction == DIRECTIONS.UP:
    if app.current_cell.top is not None: app.current_cell = app.current_cell.top 

  elif direction == DIRECTIONS.DOWN:    
    if app.current_cell.bottom is not None: app.current_cell = app.current_cell.bottom 

  elif direction == DIRECTIONS.UP_LEFT:
    if app.current_cell.upper_left is not None: app.current_cell = app.current_cell.upper_left

  elif direction == DIRECTIONS.UP_RIGHT:
    if app.current_cell.upper_right is not None: app.current_cell = app.current_cell.upper_right

  elif direction == DIRECTIONS.DOWN_LEFT:
    if app.current_cell.lower_right is not None: app.current_cell = app.current_cell.lower_right

  elif direction == DIRECTIONS.DOWN_RIGHT:
    if app.current_cell.lower_right is not None: app.current_cell = app.current_cell.lower_right

#endregion - Commands ---------------------------------------------------------

#region - Events ==============================================================

def handle_keys(event):

  key = event.key

  if event.mod & pygame.KMOD_CTRL:

    if   key == pygame.K_SPACE: toggle_orientation()
    elif key == pygame.K_UP:    increment_grid()
    elif key == pygame.K_DOWN:  decrement_grid()
    elif key == pygame.K_LEFT:  current_cell_move(DIRECTIONS.DOWN_LEFT)
    elif key == pygame.K_RIGHT: current_cell_move(DIRECTIONS.DOWN_RIGHT)

  else:

    if   key == pygame.K_w:     up()
    elif key == pygame.K_s:     down()
    elif key == pygame.K_q:     up_left()
    elif key == pygame.K_e:     up_right()
    elif key == pygame.K_a:     down_left()    
    elif key == pygame.K_d:     down_right()
    elif key == pygame.K_UP:    current_cell_move(DIRECTIONS.UP)
    elif key == pygame.K_DOWN:  current_cell_move(DIRECTIONS.DOWN)
    elif key == pygame.K_LEFT:  current_cell_move(DIRECTIONS.UP_LEFT)
    elif key == pygame.K_RIGHT: current_cell_move(DIRECTIONS.UP_RIGHT)

    check_cells()

def handle_click(event):

  def left_click():

    for row in app.grid:
      for cell in row:        
        cell.click()

    # for row in app.grid:

  if   event.button == LEFT:        left_click()
  elif event.button == SCROLL_UP:   up();         check_cells()   #increment_grid()
  elif event.button == SCROLL_DOWN: down();       check_cells()   #decrement_grid()
  elif event.button == CENTRE:      p('Wheel')
  elif event.button == RIGHT:       reset_grid()

def handle_move():

  app.mouseX = pygame.mouse.get_pos()[X]
  app.mouseY = pygame.mouse.get_pos()[Y]
  
  for row in app.grid:
    for cell in row:
      cell.move()  

#endregion - Events -----------------------------------------------------------

#region - Main Loop ===========================================================

reset_grid()
app.current_cell = app.grid[0][0]

def main():

  clock = pygame.time.Clock()

  run = True

  while run:

    clock.tick(app.fps)

    for event in pygame.event.get():
      
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        return

      if event.type == pygame.KEYUP:         handle_keys(event)
      if event.type == pygame.MOUSEBUTTONUP: handle_click(event)
      
      handle_move()

    draw_window()  
    
if __name__ == "__main__":
  main()

#endregion - Main Loop --------------------------------------------------------

#endregion - hexy /////////////////////////////////////////////////////////////
