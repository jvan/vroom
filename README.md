# vroom

## Installation

vroom is built using [pyvrui](https://github.com/jvan/pyvrui). You will need
to install it before you can run vroom.

Additionally, vroom depends on the following libraries/packages:

 * pyftgl
 * pyinotify
 * pyopengl
 * numpy

## Running vroom

To run a vroom application: make sure the `vroom` executable is in your `$PATH`
and the `vroom/` source directory is in your `$PYTHONPATH`. 

### Live Coding

To run an application in live coding mode add the flag `--live` when launching
the program. When live coding is enabled the application will automatically
update every time the source code is saved.

## Example Program

Here is a simple vroom program which draws a wireframe cube.

    #!/usr/bin/env/vroom
    from vroom import *

    def draw():
      lighting(False)
      color(1.0)
      cube(4.0)


## Learn More

Documentation for vroom can be found [here](http://iviz.csc.ucdavis.edu/vroom).

