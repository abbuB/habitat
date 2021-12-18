"""
  IDEAS

    Game Called Phaze - overlapping patterns (rotate, etc)

  TO DO:

    - check linked list connections
    - current cell selected after each move
    - hexagonal grid shape
    - center grid in window (properly)
    - background hexagons
    - animation for disappearing cells
    - error coding
    - select and inplement music    
    - scoring display

        i.    New Game
        ii.   Score
        iii.  Best
        iv.   Sound/ music toggle
        v.    Link to youtube demonstration
        vi.   Increment/Decrement Grid Size
        vii.  

  BUGS:

    - Connections are fucky


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
  ##  Styles:
  ##  0 : OK
  ##  1 : OK | Cancel
  ##  2 : Abort | Retry | Ignore
  ##  3 : Yes | No | Cancel
  ##  4 : Yes | No
  ##  5 : Retry | Cancel 
  ##  6 : Cancel | Try Again | Continue

  return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#endregion - Initialization ------------------------------------------------------

#region - Constants ===========================================================

DEBUG = True

# Initial Display Size
WIDTH  = 1000
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Habitat for Humanity Game")

# Color
WHITE  = (255,255,255,255)
BLACK  = (  0,  0,  0,255)
RED    = (255,  0,  0,255)
GREEN  = (  0,255,  0,255)
BLUE   = (  0,  0,255,255)
YELLOW = (255,255,  0,255)

BACKGROUND = (8,8,8)

# Mouse Button
LEFT         = 1
CENTRE       = 2
RIGHT        = 3
SCROLL_UP    = 4
SCROLL_DOWN  = 5

# Coordinate
X            = 0
Y            = 1

# Orientation
# VERTICAL     = 0
# HORIZONTAL   = 1

class ORIENTATIONS(Enum):

  VERTICAL   = 0
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
# WINNER_FONT = pygame.font.SysFont('arial', 32)

WINNER_FONT = pygame.font.Font(pygame.font.get_default_font(), 18)

#endregion - Constants --------------------------------------------------------

#region - Misc =============================================================

def p(s): print(str(s))

def get_background_color():

  clr = int(random.random()*16)

  ret = VASARELY_COLORS.PINK.value

  alpha = int(random.random()*64)

  if   clr == COLORS.PINK:        ret = (181, 42,142, alpha)
  elif clr == COLORS.PURPLE:      ret = ( 90, 24,120, alpha)
  elif clr == COLORS.CYAN:        ret = ( 39,105,176, alpha)
  elif clr == COLORS.NAVY:        ret = ( 79,168,219, alpha)
  elif clr == COLORS.BLUE:        ret = ( 42, 40,143, alpha)
  elif clr == COLORS.DORANGE:     ret = (227,102, 79, alpha)
  elif clr == COLORS.LORANGE:     ret = (250,147, 95, alpha)
  elif clr == COLORS.LYELLOW:     ret = (244,255,173, alpha)
  elif clr == COLORS.DYELLOW:     ret = (247,194,119, alpha)
  elif clr == COLORS.LGREEN:      ret = (  0,173,147, alpha)
  elif clr == COLORS.DGREEN:      ret = (  0,110,110, alpha)
  elif clr == COLORS.RED:         ret = (222, 33, 49, alpha)
  elif clr == COLORS.MAROON:      ret = (135, 26, 35, alpha)
  elif clr == COLORS.PEACH:       ret = (247,194, 11, alpha)
  elif clr == COLORS.BLACK:       ret = ( 32, 32, 32, alpha)
  elif clr == COLORS.GRAY:        ret = (122,135,191, alpha)
  elif clr == COLORS.TRANSPARENT: ret = (255,  0,  0, alpha)
  else:                           ret = ( 64, 64, 64, alpha)

  return ret
  
def get_color():

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

    # clr = int(random.random()*16)

    # match clr:
      
    #   case COLORS.PINK:         ret = VASARELY_COLORS.PINK.value
    #   case COLORS.PURPLE:       ret = VASARELY_COLORS.PURPLE.value
    #   case COLORS.CYAN:         ret = VASARELY_COLORS.CYAN.value
    #   case COLORS.NAVY:         ret = VASARELY_COLORS.NAVY.value
    #   case COLORS.BLUE:         ret = VASARELY_COLORS.BLUE.value
    #   case COLORS.DORANGE:      ret = VASARELY_COLORS.DORANGE.value
    #   case COLORS.LORANGE:      ret = VASARELY_COLORS.LORANGE.value
    #   case COLORS.LYELLOW:      ret = VASARELY_COLORS.LYELLOW.value
    #   case COLORS.DYELLOW:      ret = VASARELY_COLORS.DYELLOW.value
    #   case COLORS.LGREEN:       ret = VASARELY_COLORS.LGREEN.value
    #   case COLORS.DGREEN:       ret = VASARELY_COLORS.DGREEN.value
    #   case COLORS.PEACH:        ret = VASARELY_COLORS.PEACH.value
    #   case COLORS.RED:          ret = VASARELY_COLORS.RED.value
    #   case COLORS.MAROON:       ret = VASARELY_COLORS.MAROON.value
    #   case COLORS.BLACK:        ret = VASARELY_COLORS.BLACK.value
    #   case COLORS.GRAY:         ret = VASARELY_COLORS.GRAY.value
      
    #   case COLORS.TRANSPARENT:  ret = VASARELY_COLORS.TRANSPARENT.value
    #   case default:             ret = VASARELY_COLORS.GRAY.value

    # return ret

def semi_perimeter(a,b,c):  # a, b, and c are lengths of the triangles sides

  return (a+b+c)/2

def triangle_area(a,b,c):

  # Heron's Formula
  # https://en.wikipedia.org/wiki/Heron%27s_formula

  s = semi_perimeter(a,b,c)

  temp = s*(s-a)*(s-b)*(s-c)

  retval = 0

  if temp > 0: retval = math.floor(math.sqrt(temp))
  
  return retval

#endregion - Misc ----------------------------------------------------------

#region - Objects =============================================================

class App:

  def __init__(self) -> None:

    self.fps = 60                 # Frames Per Second

    self.moves = 0                # Number of moves taken

    self.mouseX = 0               # current mouse x positon
    self.mouseY = 0               # current mouse y positon

    self.dragging = False
    self.mouse_start = None

    self.background = []

class Point:

  def __init__(self, x, y) -> None:
    
    self.x = x
    self.y = y

class Hex:

  id = 0
  orientation = ORIENTATIONS.VERTICAL
  area = 0
  perimeter = 0
  side_length = 0
  tri_area = 0

  offset = 0

  def __init__(self, x, y, diameter, color, background=False) -> None:

    self.id = Hex.id                                # identification Number

    Hex.id+=1                                       # Increment overall object count

    self._x = int(x)                                # horizontal position of centre
    self._y = int(y)                                # vertical position of centre
    # self._z = int(z)                                # vertical position of centre

    self.row = 0                                    # row of cell in grid array
    self.col = 0                                    # col of cell in grid array

    self.background  = background                   # is the hex a background element

    self.diameter = diameter                        # full diameter width of hexagon
    self.radius = diameter/2                        # distance from center to corner point
    self.inradius = self.radius*math.cos(math.pi/6) # distance from center to center of a side
    self.maximal_diameter = self.radius * 2         # twice the radius         
    self.minimal_diameter = self.inradius * 2       # twice the inradius

    self.center = Point(x, y)                       # Center Point
    self.points = []                                # list of 6 vertex points
    self.border = []                                # list of 6 vertex points of border

    self.color = color                              # Background Color
    self.center_color = color                       # Interior Color

    self.hit = False                                # Mouse is currently over the cell
    self.active = True                              # Cell has not been solved

    self.delta_x = 10                               # horizontal speed
    self.delta_y = 10                               # vertical speed

    # References to adjacent cells - Cells wrap
    self.top = None                                 # cell above
    self.bottom = None                              # cell below

    self.top_right = None                           # cell above right
    self.top_left = None                            # cell above left

    self.bottom_right = None                        # cell below right
    self.bottom_left = None                         # cell below left

    self.left = None                                # cell left
    self.right = None                               # cell right
    
    # Aliases
    sX = self._x
    sY = self._y
    r = self.radius
    pts = self.points
    brd = self.border

    # Calculate Corner Points
    if self.orientation == ORIENTATIONS.HORIZONTAL:

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

    if Hex.area == 0:
      
      # p("Calculate Area")
      pts = self.points

      a = math.floor(math.dist((self.center.x, self.center.y), (pts[0][X], pts[0][Y])))
      b = math.floor(math.dist((self.center.x, self.center.y), (pts[1][X], pts[1][Y])))
      c = math.floor(math.dist((pts[0][X], pts[5][0]), (pts[1][X], pts[1][Y])))

      Hex.perimeter = c * 6 # Perimeter is six times side length
      Hex.side_length = a

      Hex.tri_area = math.floor(triangle_area(a,b,c))
      Hex.area = Hex.tri_area * 6

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

    if(self.background == False):
      pygame.gfxdraw.filled_circle(WIN, self._x, int(self._y + Hex.offset), int(grid.cell_size*0.25), self.center_color)

    Hex.offset -= 0.0

    if self.active == False:

      self.color = VASARELY_COLORS.TRANSPARENT.value
      pygame.draw.polygon(WIN, VASARELY_COLORS.GRAY.value, self.points, width=1)
      
    else:

      if grid.focus_cell == self: pygame.draw.polygon(WIN, WHITE, self.border, width=3)

    if self.hit:

      if self.active:
        
        pygame.draw.polygon(WIN, WHITE, self.border, width=1)

      # pygame.gfxdraw.aapolygon(w, self.points, VASARELY_COLORS.RED.value)

      # text = HEALTH_FONT.render(str(self.row) + ', ' + str(self.col), True, WHITE)

      # if self.bottom_left != None:

      #   text = HEALTH_FONT.render(str(self.bottom_left.id), True, WHITE)
      #   text_rect = text.get_rect(center=(self._x, self._y))
      #   WIN.blit(text, text_rect)

    # else:

      # text = HEALTH_FONT.render(str(self.id),True,WHITE)
      # text_rect = text.get_rect(center=(self._x, self._y))
      # WIN.blit(text,text_rect)

      # if self.top != None:          pygame.draw.line(WIN, RED, (self._x, self._y), (self.top._x, self.top._y), width=5)
      # if self.bottom != None:       pygame.draw.line(WIN, GREEN, (self._x, self._y), (self.bottom._x, self.bottom._y), width=5)
      
      # if self.top_left != None:   pygame.draw.line(WIN, YELLOW, (self._x, self._y), (self.top_left._x, self.top_left._y), width=5)
      # if self.top_right != None:  pygame.draw.line(WIN, BLUE, (self._x, self._y), (self.top_right._x, self.top_right._y), width=5)
      
      # if self.bottom_left != None:   pygame.draw.line(WIN, BLACK, (self._x, self._y), (self.bottom_left._x, self.bottom_left._y), width=5)
      # if self.bottom_right != None:  pygame.draw.line(WIN, WHITE, (self._x, self._y), (self.bottom_right._x, self.bottom_right._y), width=5)

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
    
    if self.top_left != None:   pygame.draw.line(WIN, YELLOW, (self._x, self._y), (self.top_left._x, self.top_left._y), width=5)
    if self.top_right != None:  pygame.draw.line(WIN, BLUE, (self._x, self._y), (self.top_right._x, self.top_right._y), width=5)
    
    if self.bottom_left != None:   pygame.draw.line(WIN, BLACK, (self._x, self._y), (self.bottom_left._x, self.bottom_left._y), width=5)
    if self.bottom_right != None:  pygame.draw.line(WIN, WHITE, (self._x, self._y), (self.bottom_right._x, self.bottom_right._y), width=5)

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

  def mouse_move(self):

    self.hitTest()

  def mouse_up(self) -> None:

    if self.hit:

      if self.active:
        
        grid.focus_cell = self



class Background_Hex:

  id = 0
  orientation = ORIENTATIONS.VERTICAL
  count = 0

  def __init__(self, x, y, diameter, color) -> None:

    self.id = Hex.id                                # identification Number

    Hex.id+=1                                       # Increment overall object count

    self._x = int(x)                                # horizontal position of centre
    self._y = int(y)                                # vertical position of centre
    # self._z = int(z)                                # vertical position of centre

    self.diameter = diameter                        # full diameter width of hexagon
    self.radius = diameter/2                        # distance from center to corner point
    self.inradius = self.radius*math.cos(math.pi/6) # distance from center to center of a side
    self.maximal_diameter = self.radius * 2         # twice the radius         
    self.minimal_diameter = self.inradius * 2       # twice the inradius

    self.center = Point(x, y)                       # Center Point
    self.points = []                                # list of 6 vertex points

    self.color = color                              # Background Color

    speed = 2

    self.delta_x = random.uniform(-speed, speed)    # horizontal speed
    self.delta_y = random.uniform(-speed, speed)    # vertical speed

    # Aliases
    sX = self._x
    sY = self._y
    r = self.radius
    pts = self.points
    # brd = self.border

    # Offsets
    oX = math.cos(math.pi/3)*self.radius # Offset x
    oY = math.sin(math.pi/3)*self.radius # Offset Y

    pts.append([sX + r,  sY     ])
    pts.append([sX + oX, sY - oY])
    pts.append([sX - oX, sY - oY])
    pts.append([sX - r,  sY     ])
    pts.append([sX - oX, sY + oY])
    pts.append([sX + oX, sY + oY])

  def draw(self):

    s_dx = self.delta_x
    s_dy = self.delta_y

    pts = self.points
    # self.points[0] = [self.points[0][X] + self.delta_x,  self.points[0][Y] + self.delta_y]
    
    pts[0][X] += s_dx;    pts[0][Y] += s_dy
    pts[1][X] += s_dx;    pts[1][Y] += s_dy
    pts[2][X] += s_dx;    pts[2][Y] += s_dy
    pts[3][X] += s_dx;    pts[3][Y] += s_dy
    pts[4][X] += s_dx;    pts[4][Y] += s_dy
    pts[5][X] += s_dx;    pts[5][Y] += s_dy

    for pt in pts:

      if pt[X] > WIDTH or \
         pt[X] < 0:

        self.delta_x *= -1
        # break
      
      if pt[Y] > HEIGHT or \
         pt[Y] < 0:

        self.delta_y *= -1
        break

    pygame.gfxdraw.filled_polygon(WIN, self.points, self.color)

class Grid:

  id = 0
  orientation = ORIENTATIONS.VERTICAL
  area = 0
  perimeter = 0
  side_length = 0
  tri_area = 0

  def __init__(self, x, y, cell_size, grid_size, orientation) -> None:

    self._x = int(x)                                # horizontal position of centre
    self._y = int(y)                                # vertical position of centre
    
    self.orientation = orientation

    self.cells = []                                 # list holding the cell objects

    self.focus_cell = None                          # which hexagonal cell has the focus

    self.size = grid_size                           # of hexagonal layers
    self.cell_size = cell_size

  def draw(self):
    
    for row in self.cells:
      for cell in row:
        cell.draw()

    if DEBUG: self.focus_cell.draw_links()

  def load(self):
    
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

          h = Hex(colPos, rowPos, radius, get_color())

          h.col = col
          h.row = row

          temp.append(h)

        app.grid.append(temp)

    def load_grid_vertical():
    
      p('VERTICAL')

      radius = self.cell_size*1/math.cos(math.pi/6)
      limit = self.size
      inRadius = radius*math.cos(math.pi/6)

      for row in range(limit):
        
        temp = []

        for col in range(limit):
        
          x = 2.5 * radius/2 + (0.75 * radius) * col

          if col%2 == 0: y = inRadius * 0.75 + row * inRadius + inRadius/2
          else:          y = inRadius * 0.75 + row * inRadius

          h = Hex(x, y, radius, get_color())

          h.col = col
          h.row = row

          # if row == 0 and col == 0: h.active = False

          temp.append(h)

        self.cells.append(temp)

    if   self.orientation == ORIENTATIONS.HORIZONTAL: load_grid_horizontal()
    elif self.orientation == ORIENTATIONS.VERTICAL:   load_grid_vertical()

  def shuffle(self):
    
    def get_cell():
    
      length = len(self.cells)

      return self.cells[int(random.random()*length)] \
                       [int(random.random()*length)]

    for rowIndex, row in enumerate(self.cells):
      for colIndex, col in enumerate(row):
        
        cell = self.cells[rowIndex][colIndex]
        temp = cell.center_color

        random_cell = get_cell()

        while (cell.center_color == random_cell.color) or \
              (cell.color == random_cell.center_color):
        
          random_cell = get_cell()

        cell.center_color = random_cell.center_color
        random_cell.center_color = temp

  def connect(self):
    
    def get_top_left(hex):
      
      temp = hex

      while temp.bottom_right is not None:

        temp = temp.bottom_right

      return temp

    def get_top_right(hex):
      
      temp = hex

      while temp.bottom_left is not None:

        temp = temp.bottom_left

      return temp

    def get_bottom_left(hex):
      
      temp = hex

      while temp.top_right is not None:

        # p(temp.id)
        temp = temp.top_right

        if temp.top_right.id == hex.id:

          break

      return temp

    def get_bottom_right(hex):
      
      temp = hex

      while temp.top_left is not None:

        temp = temp.top_left

        if temp.top_left.id == hex.id:

          break

      return temp

    # try:

    cells = self.cells
    sz = len(cells)-1

    for rowIndex, row in enumerate(cells):
      for colIndex, cell in enumerate(row):

        even_Col = colIndex%2==0

        # Top 
        if rowIndex == 0:                  cell.top = cells[sz        ][colIndex]
        else:                              cell.top = cells[rowIndex-1][colIndex]

        # Bottom
        if rowIndex == len(cells)-1:       cell.bottom = cells[0         ][colIndex]
        else:                              cell.bottom = cells[rowIndex+1][colIndex]

        # Upper Left
        if(colIndex == 0):

          cell.top_left = None

        else:

          if(rowIndex==0):
            
            if(even_Col):  cell.top_left = cells[rowIndex  ][colIndex-1]
            else:          cell.top_left = None

          else:             
            
            if(even_Col):  cell.top_left = cells[rowIndex  ][colIndex-1]              
            else:          cell.top_left = cells[rowIndex-1][colIndex-1]
            

        # Upper Right
        if(colIndex == sz):
          
          cell.top_right = None
        
        else:
          
          if(rowIndex == 0):

            if(even_Col):  cell.top_right = cells[rowIndex][colIndex+1]
            else:          cell.top_right = None

          else:

            if(even_Col):  cell.top_right = cells[rowIndex  ][colIndex+1]
            else:          cell.top_right = cells[rowIndex-1][colIndex+1]

        # Lower Left
        if(colIndex == 0):

          cell.bottom_left = None
        
        else:

          if(rowIndex==sz):
            
            if(even_Col):  cell.bottom_left = None
            else:          cell.bottom_left = cells[rowIndex][colIndex-1]

          else:             
            
            if(even_Col):  cell.bottom_left = cells[rowIndex+1][colIndex-1]
            else:          cell.bottom_left = cells[rowIndex][colIndex-1]

        # Lower Right
        if(colIndex == sz):
          
          cell.bottom_right = None
        
        else:
          
          if(rowIndex==sz):

            if(even_Col):  cell.bottom_right = None
            else:          cell.bottom_right = cells[rowIndex][colIndex+1]

          else:

            if(even_Col):  cell.bottom_right = cells[rowIndex+1][colIndex+1]
            else:          cell.bottom_right = cells[rowIndex  ][colIndex+1]

    # Get Upper Left
    for rowIndex, row in enumerate(cells):
      for colIndex, cell in enumerate(row):
        
        if cells[rowIndex][colIndex].top_left is None:
          
          cells[rowIndex][colIndex].top_left = get_top_left(cells[rowIndex][colIndex])
    
    # Get Upper Right
    for rowIndex, row in enumerate(cells):
      for colIndex, cell in enumerate(row):
        
        if cells[rowIndex][colIndex].top_right is None:
          
          cells[rowIndex][colIndex].top_right = get_top_right(cells[rowIndex][colIndex])

    # Get Lower Left
    for rowIndex, row in enumerate(cells):
      for colIndex, cell in enumerate(row):
        
        cell = cells[rowIndex][colIndex]

        if cell.bottom_left is None:

          cell.bottom_left = get_bottom_left(cell)

    # Get Lower Right
    for rowIndex, row in enumerate(cells):
      for colIndex, cell in enumerate(row):
        
        if cells[rowIndex][colIndex].bottom_right is None:
          
          cells[rowIndex][colIndex].bottom_right = get_bottom_right(cells[rowIndex][colIndex])

    # except:

    #   p('ERROR LOADING UP / DOWN ' + str(row) + ', ' + str(col))

    x = 1
    assert x > 0, 'Only positive numbers are allowed'
    # print('x is a positive number.')

  def toggle_orientation(self):
    
    if self.orientation == ORIENTATIONS.HORIZONTAL:
    
      self.orientation = ORIENTATIONS.VERTICAL
      Hex.orientation = ORIENTATIONS.VERTICAL
    
    else:                 
      
      self.orientation = ORIENTATIONS.HORIZONTAL
      Hex.orientation = ORIENTATIONS.HORIZONTAL
      
    self.cells.clear()

    self.load()
    self.connect()  # Load cell adjacentcy (above/below etc)
    self.shuffle()
    

  def reset(self):
    
    def load_background():
      
      app.background.clear()

      for row in range(50):

        h = Background_Hex(random.random()*WIDTH, random.random()*HEIGHT, random.random()*250, get_background_color())

        app.background.append(h)

      p(len(app.background))
      
    Hex.id =  0
    Hex.area = 0

    self.moves = 0
    self.cells.clear()
    
    self.load()     # Load the grid... duh
    self.connect()  # Load cell adjacentcy (above/below etc)
    self.shuffle()  # Scramble the inner circles

    load_background()

    self.set_focus()
    
  def increment(self):
    
    self.size += 2
    self.cell_size = math.floor(WIDTH/(self.size+1))

    self.reset()

    self.focus_cell = self.cells[0][0]
    
  def decrement(self):
    
    if self.size>4:

      self.size -= 2  
      self.cell_size = math.floor(WIDTH/(self.size+1))

      self.reset()
      
  def check_cells(self):
    
    def reconnect_cell(cell):

      cell.top.bottom = cell.bottom
      cell.bottom.top = cell.top
      cell.top_left.bottom_right = cell.bottom_right
      cell.top_right.bottom_left = cell.bottom_left
      cell.bottom_left.top_right = cell.top_right
      cell.bottom_right.top_left = cell.top_left

    for row in self.cells:
      for cell in row:

        if cell.color == cell.center_color:
          cell.color        = VASARELY_COLORS.TRANSPARENT.value
          cell.center_color = VASARELY_COLORS.TRANSPARENT.value
          cell.active = False

          reconnect_cell(cell)
          
  def check_game(self):
    
    for row in self.cells:
      for col in row:
        if(col.top == col and
          col.bottom == col and
          col.top_left == col and
          col.top_right == col and
          col.bottom_left == col and
          col.bottom_right == col):
          p('GAME OVER')
          break


  def move_focus(self, direction):

    if   direction == DIRECTIONS.UP:
      if self.focus_cell.top is not None: self.focus_cell = self.focus_cell.top 

    elif direction == DIRECTIONS.DOWN:    
      if self.focus_cell.bottom is not None: self.focus_cell = self.focus_cell.bottom 

    elif direction == DIRECTIONS.UP_LEFT:
      if self.focus_cell.top_left is not None: self.focus_cell = self.focus_cell.top_left

    elif direction == DIRECTIONS.UP_RIGHT:
      if self.focus_cell.top_right is not None: self.focus_cell = self.focus_cell.top_right

    elif direction == DIRECTIONS.DOWN_LEFT:
      if self.focus_cell.bottom_left is not None: self.focus_cell = self.focus_cell.bottom_left

    elif direction == DIRECTIONS.DOWN_RIGHT:
      if self.focus_cell.bottom_right is not None: self.focus_cell = self.focus_cell.bottom_right

  def move(self, direction):

    def get_first_active(col) -> Hex:

      for row_index, row in enumerate(grid.cells):

        if row[col].active:

          return row[col]

    def get_last_active(col) -> Hex:

      last_active = 0

      for row_index, row in enumerate(grid.cells):

        if row[col].active:

          last_active = row[col]

      return last_active

    def up():

      col = self.focus_cell.col

      temp_color = get_first_active(col).center_color
      last_active = get_last_active(col)

      for row_index, row in enumerate(self.cells):
        
        cell = row[col]

        if cell.active:

          if cell == last_active: cell.center_color = temp_color
          else:                   cell.center_color = cell.bottom.center_color

    def down():

      col = self.focus_cell.col
      length = len(self.cells)
      
      temp_color = get_last_active(col).center_color
      first_active = get_first_active(col)

      for row in reversed(range(length)):
        
        cell = self.cells[row][col]

        if cell.active:

          if cell == first_active: cell.center_color = temp_color
          else:                    cell.center_color = cell.top.center_color

    def up_left():

      temp_color = self.focus_cell.bottom_right.center_color
      hex = self.focus_cell.bottom_right

      while hex.id != self.focus_cell.id:

        hex.center_color = hex.bottom_right.center_color

        hex = hex.bottom_right

      hex.center_color = temp_color

    def up_right():
      
      temp_color = self.focus_cell.bottom_left.center_color
      hex = self.focus_cell.bottom_left

      while hex.id != self.focus_cell.id:

        hex.center_color = hex.bottom_left.center_color

        hex = hex.bottom_left

      hex.center_color = temp_color

    def down_left():

      temp_color = self.focus_cell.top_right.center_color
      hex = self.focus_cell.top_right

      while hex.id != self.focus_cell.id:

        hex.center_color = hex.top_right.center_color

        hex = hex.top_right

      hex.center_color = temp_color

    def down_right():

      temp_color = self.focus_cell.top_left.center_color
      hex = self.focus_cell.top_left

      while hex.id != self.focus_cell.id:

        hex.center_color = hex.top_left.center_color

        hex = hex.top_left

      hex.center_color = temp_color

    # def right(): p('right() placeholder')
    # def left():  p('left() placeholder')

    if   direction == DIRECTIONS.UP:         up()
    elif direction == DIRECTIONS.DOWN:       down()
    elif direction == DIRECTIONS.UP_LEFT:    up_left()
    elif direction == DIRECTIONS.UP_RIGHT:   up_right()
    elif direction == DIRECTIONS.DOWN_LEFT:  down_left()
    elif direction == DIRECTIONS.DOWN_RIGHT: down_right()

    self.check_cells()
    self.increment_moves()
    self.check_game()
  
  def increment_moves(self):
    
    app.moves+=1

  def set_focus(self):
    
    for rowIndex, row in enumerate(self.cells):
      for colIndex, col in enumerate(row):
      
        # p(col.active)
        if col.active: 

          self.focus_cell = col
          return

  def mouse_move(self):

    for row in self.cells:
      for cell in row:
        cell.mouse_move()  

  def mouse_up(self):
  
    for row in self.cells:
      for cell in row:        
        cell.mouse_up()

#endregion - Objects ----------------------------------------------------------

app = App()

m = 7

grid = Grid(0, 0, HEIGHT/(m+1), m, ORIENTATIONS.VERTICAL)
grid.reset()

#region - Commands ============================================================

def draw_window():

  # try:

    WIN.fill(BACKGROUND)

    draw_background()

    # grid.draw()

    w = WIDTH/(grid.size+1)

    # pygame.draw.rect(WIN, (128,0,0), (w/2, w/2, WIDTH-w, HEIGHT-w), 1, 15)

    if grid.focus_cell is not None:
      WIN.blit(WINNER_FONT.render(str(grid.focus_cell.row), 1, WHITE), (20, 20))
      WIN.blit(WINNER_FONT.render('Moves: ' + str(app.moves), 1, WHITE), (20, 50))
      WIN.blit(WINNER_FONT.render('Current Cell: ' + str(grid.focus_cell.id), 1, WHITE), (800, 20))
      WIN.blit(WINNER_FONT.render('Dragging: ' + str(app.dragging), 1, WHITE), (800, 50))

    pygame.display.update()

  # except:

  #   Mbox('Exception - Hexy.py', 'draw_window() - ' + Exception.__name__, 1)

def draw_background():

  for cell in app.background:
    cell.draw()

#endregion - Commands ---------------------------------------------------------

#region - Events ==============================================================

def handle_keys(event):

  key = event.key

  if event.mod & pygame.KMOD_CTRL:

    if   key == pygame.K_SPACE: grid.toggle_orientation()    

    elif key == pygame.K_LEFT:  grid.move_focus(DIRECTIONS.DOWN_LEFT)
    elif key == pygame.K_RIGHT: grid.move_focus(DIRECTIONS.DOWN_RIGHT)

  elif event.mod & pygame.KMOD_ALT:

    if   key == pygame.K_UP:    grid.increment()
    elif key == pygame.K_DOWN:  grid.decrement()

  else:

    if   key == pygame.K_w:     grid.move(DIRECTIONS.UP)
    elif key == pygame.K_s:     grid.move(DIRECTIONS.DOWN)
    elif key == pygame.K_q:     grid.move(DIRECTIONS.UP_LEFT)
    elif key == pygame.K_e:     grid.move(DIRECTIONS.UP_RIGHT)
    elif key == pygame.K_a:     grid.move(DIRECTIONS.DOWN_LEFT)
    elif key == pygame.K_d:     grid.move(DIRECTIONS.DOWN_RIGHT)

    elif key == pygame.K_UP:    grid.move_focus(DIRECTIONS.UP)
    elif key == pygame.K_DOWN:  grid.move_focus(DIRECTIONS.DOWN)
    elif key == pygame.K_LEFT:  grid.move_focus(DIRECTIONS.UP_LEFT)
    elif key == pygame.K_RIGHT: grid.move_focus(DIRECTIONS.UP_RIGHT)

    elif key == pygame.K_u:     grid.move_focus(DIRECTIONS.UP_LEFT)
    elif key == pygame.K_i:     grid.move_focus(DIRECTIONS.UP)
    elif key == pygame.K_o:     grid.move_focus(DIRECTIONS.UP_RIGHT)
    elif key == pygame.K_j:     grid.move_focus(DIRECTIONS.DOWN_LEFT)
    elif key == pygame.K_k:     grid.move_focus(DIRECTIONS.DOWN)
    elif key == pygame.K_l:     grid.move_focus(DIRECTIONS.DOWN_RIGHT)

    elif key == pygame.K_r:     grid.reset()

    # check_cells()

  # if grid.focus_cell.active == False:

    # grid.set_focus()

def handle_up(event):

  if   event.button == LEFT:        grid.mouse_up()
  elif event.button == SCROLL_UP:   grid.move(DIRECTIONS.UP)
  elif event.button == SCROLL_DOWN: grid.move(DIRECTIONS.DOWN)
  elif event.button == CENTRE:      p('Wheel')
  elif event.button == RIGHT:       grid.reset()

  app.dragging = False

def handle_move():

  app.mouseX = pygame.mouse.get_pos()[X]
  app.mouseY = pygame.mouse.get_pos()[Y]
  
  grid.mouse_move()

def handle_down(event):

  # grid.set_focus()

  app.dragging = True  
  app.mouse_start = (app.mouseX, app.mouseY)

def handle_motion(event):

  if(app.dragging):

    theta = math.atan2(app.mouse_start[0] - app.mouseX, app.mouse_start[1] - app.mouseY) * 180 / math.pi

    if(theta != 0):

      if( (theta >=  150 and theta <=  180) or \
          (theta <= -150 and theta >= -180) ):    grid.move(DIRECTIONS.DOWN)
      elif(theta <=   30 and theta >=  -30):      grid.move(DIRECTIONS.UP)
      elif(theta >    30 and theta <=   90):      grid.move(DIRECTIONS.UP_LEFT)
      elif(theta >    90 and theta <=  150):      grid.move(DIRECTIONS.DOWN_LEFT)
      elif(theta <   -30 and theta >=  -90):      grid.move(DIRECTIONS.UP_RIGHT)
      elif(theta <   -90 and theta >= -150):      grid.move(DIRECTIONS.DOWN_RIGHT)

      app.dragging = False

    # p(theta)

#endregion - Events -----------------------------------------------------------

#region - Main Loop ===========================================================

# p(24/2)
# p(24//2)

# Mbox('Title', "Now is the time for all good men to come to the aid of the party.", 6)

def main():

  clock = pygame.time.Clock()

  while True:

    clock.tick(app.fps)

    for event in pygame.event.get():
      
      if event.type == pygame.QUIT:
        pygame.quit()
        return

      if event.type == pygame.MOUSEBUTTONUP:    handle_up(event)
      if event.type == pygame.MOUSEBUTTONDOWN:  handle_down(event)
      if event.type == pygame.MOUSEMOTION:      handle_motion(event)
      
      if event.type == pygame.KEYDOWN:          handle_keys(event)
      
      handle_move()

    draw_window()  
    
if __name__ == "__main__":
  main()

#endregion - Main Loop --------------------------------------------------------

#endregion - hexy /////////////////////////////////////////////////////////////
