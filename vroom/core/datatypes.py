class BooleanOption:
   def __init__(self, state=False):
      self.state = state
   def toggle(self):
      self.state = not self.state
   def __nonzero__(self):
      return self.state

