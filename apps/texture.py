#!/usr/bin/env vroom

from vroom import *

def gl_init():
   texture_file = get_resource('crate.png')
   Global.texture = Texture.from_file(texture_file)

def draw():
   cube(5.0, texture=Global.texture)
