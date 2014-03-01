from scipy import integrate, arange

class Solver:

    @staticmethod
    def vectorfield(f):
       def wrapped(p, t):
          (x, y, z) = p
          return f(x,y,z)
       return wrapped

    def __init__(self, dynamics):
        self.dynamics = dynamics

    #def solve(self, steps, dt, position):
       #t = arange(0.0, steps*dt, dt)
       #vertices = integrate.odeint(self.dynamics, position, t)
       #return vertices

    def step(self, pos, dt=0.01):
        soln = integrate.odeint(self.dynamics, pos, [0, dt])
        return soln[1]

    def generator(self, pos, n):
        for _ in range(n):
            yield pos
            pos = self.step(pos)
