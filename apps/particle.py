#!/usr/bin/env vroom
from vroom import *
import random

class Particle:

   dt = 0.01

   @staticmethod
   def random_velocity():
      rand = lambda: random.random()*5.0 - 2.5
      return [rand() for i in range(3)]

   def __init__(self, pos):
      self.position = pos
      self.velocity = Particle.random_velocity()
      self.age = 0
      self.lifetime = random.randint(100, 500)

   def __str__(self):
      return '({:.2f}, {:.2f}, {:.2f}), ({:.2f}, {:.2f}, {:.2f})'.format(*(self.position+self.velocity))

   def move(self):
      for i in range(3):
         self.position[i] += self.velocity[i] * Particle.dt

      self.age += 1

   def expired(self):
      return self.age > self.lifetime

class ParticleEngine:

   def __init__(self):
      self.particles = []
      self.array = PointCloud()
      self.color_map = ColorMap('hot') 
      self.color_map_data = [self.color_map(i, 255, alpha=0.4) for i in range(256)]

   def _update_array_data(self):
      vertices = [x.position for x in self.particles] 
      colors = [self.color_map_data[int(255.0*(x.lifetime-x.age)/x.lifetime)] for x in self.particles]
      self.array.loadVertexData(vertices, mode='dynamic')
      self.array.loadColorData(colors, mode='dynamic')


   def add_particle(self, particle):
      self.particles.append(particle)
      self._update_array_data()

   def add_particles(self, positions):
      for pos in positions:
         self.particles.append(Particle(pos))
      self._update_array_data()

   def draw(self):
      self.array.draw()

   def frame(self):
      for particle in self.particles:
         particle.move()

      self.particles = filter(lambda x: not x.expired(), self.particles)
      self._update_array_data()

particles = ParticleEngine()

def gl_init():
   global particles
   particles.array.sprite('share/particle.bmp')

def draw():
   lighting(False)
   particles.draw()

def frame():
   for i in range(5):
      particles.add_particle(Particle([0.0,0.0,0.0]))
   particles.frame()
