# vroom

Vroom is a high-level programming framework for developing immersive virtual
reality applications. It is written in python and uses the [Vrui][vrui] 
(Virtual Reality User-Interface) library.

The goal of vroom is to make it easy to visualize and interact with 3D data
and simulations. This is what a vroom application looks like.

   ```python
   #!/usr/bin/env vroom
   from vroom import *

   def init():
      Global.points = []  # list of (x,y,z) position values

      # add a clear button to the main menu
      addMainMenuItem('clear', clear_points)

   def clear_points(button):
      # remove all points
      Global.points = []

   def display():
      # set up the rendering environment
      lighting(False)
      color(green)

      # draw a wireframe sphere at each point
      draw(sphere, 3.0).for_each(Global.points)

   def button_press(pos, button);
      # add a point whenever the user presses a button
      Global.points.append(pos)
   ```

[vrui]: http://keckcaves.org/software/vrui


### Installation

On Ubuntu, vroom can be installed from the [KeckCAVES PPA][keckcaves-ppa].

   ```sh
   sudo add-apt-repository ppa:keckcaves/ppa
   sudo apt-get update
   sudo apt-get install vroom
   ```

[pyvrui]: https://github.com/ComSciCtr/pyvrui


### Example Programs

Check out the [vroom example programs][vroom-examples] repository for more
examples of using vroom. There is a package available in the 
[KeckCAVES PPA][keckcaves-ppa].

   ```sh
   sudo apt-get install vroom-examples
   ```

[vroom-examples]: https://github.com/ComSciCtr/vroom-examples


### Learn More

Documentation for vroom can be found [here](http://comscictr.github.io/vroom).

