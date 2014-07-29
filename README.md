Geist
=====

[![Build Status](https://travis-ci.org/thetestpeople/Geist.svg?branch=master)](https://travis-ci.org/thetestpeople/Geist)

Computer vision based UI automation library.

Please file bug reports.

To start using geist, execute the `prereq.py` file with:

``` python
ipython -i prereq.py
```

This will set the following aliases, which you may find useful:

 * C: Show capture. Shows a capture of the current screen.
 * V: Viewer. An instance of the Viewer class, with the current gui and repo set.
 * S: Save current image. Saves the current image into the repo.
 * F: Show found. Highlights locations on the screen where the finder matched.
 * R: Show repo. Display a saved image.


Repository
========== 

Folder to serve as a location for saved images. These images take the form of
an npy file, a numpy array. These can be used to search for the image within the
display.

Example:

``` python
from geist import DirectoryRepo

repo = DirectoryRepo('root_folder/folder/geist_repo')
```

Backends
========

A backend is how geist interacts with the screen. This is different depending on
which operating system geist is being run from. This is called with the argument
of a screen number. For example, Xvfb based backends on linux can be passed the 
number 2 to start the Xvfb backend on screen number 2.

Example:

``` python
from geist.backends import get_platform_backend

backend = get_platform_backend(screen_number)
```

GUI
===

The gui is the user interface that geist will begin watching on. This contains 
a number of properties/methods used to interact with the screen. It is 
initialised with a backend.

Example:

``` python
from geist import GUI

gui = GUI(backend)
```

Viewer
======

A viewer is used to display an image of what geist is looking at at any one 
time, as well as some functionality to interactively extract and save image
data. It is initialised with a gui and a repository.

Example:

``` python
from geist.pyplot import Viewer

viewer = Viewer(gui, repository)
```

The first useful method a viewer provides is the ability to view what is
happening on the gui with show_capture. You can zoom in to a particular part of
the image using the magnifying glass button and return the the original view
with the home button.

Example:

``` python
viewer.show_capture()
```

You can also save the image that is displayed in the viewer to the repository,
which can then be used later to build finders. To call the save method, pass in
the name you want to save the image as.

Example:

``` python
viewer.save('image_name')
```

You can view the results of a particular finder with the show_found function.
This will highlight any part of the gui which the finder matches, whether it is
one result or many. It is called with the finder as an argument.

Example:

``` python
viewer.show_found(finder)
```

You can get the colour of the image in the viewer by using the get_colour
method. This will return a hsv object which can be used to create finders. If
there is just one colour in this image, it will match only this colour. If there
are multiple colours, it will match a range where h is between the minimum h
value and maximum h value with the same being true for s and v.

Example:

``` python
colour = viewer.get_colour()
```
