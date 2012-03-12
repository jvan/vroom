#!/usr/bin/env vroom

from vroom import *
from random import randint

def render_cubes():
   Global.Size = 2.0
   Global.RenderFunc = cube

def render_spheres():
   Global.Size = 1.0
   Global.RenderFunc = sphere

def init():
   setMainMenuTitle('grid')
   addMainMenuItem('cubes', render_cubes)
   addMainMenuItem('spheres', render_spheres)

   Global.Size = 2.0

   Global.Width  = 30
   Global.Height = 30

   Nx = Global.Width / Global.Size
   Ny = Global.Height / Global.Size
   
   points = [[randint(0, Nx-Global.Size)*Global.Size + Global.Size/2.0,
              randint(0, Ny-Global.Size)*Global.Size + Global.Size/2.0,
              Global.Size/2.0] for i in range(20)]

   Global.Points = point_list(points)

   Global.RenderFunc = cube

def draw():

   # Draw grid
   lighting(False)
   color(0.4)

   grid(Global.Width, Global.Height, 15, 15)

   # Draw axes
   color(1.0)
   lineWidth(2.0)

   axes(36.0)

   # Draw solid objects
   lighting(True)
   material(1.0, 0.5, 0.0)

   glEnable(GL_POLYGON_OFFSET_FILL)
   glPolygonOffset(1.0, 1.0)

   Global.Points.for_each(Global.RenderFunc, Global.Size, style='solid')

   glDisable(GL_POLYGON_OFFSET_FILL)

   # Draw object outlines
   lighting(False)
   color(0.0)
   lineWidth(1.5)
   
   Global.Points.for_each(Global.RenderFunc, Global.Size)

