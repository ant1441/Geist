Geist
=====

[![Build Status](https://travis-ci.org/thetestpeople/Geist.svg?branch=master)](https://travis-ci.org/thetestpeople/Geist)

Computer vision based UI automation library.

Please file bug reports.

To start using geist, execute the `prereq.py` file with:

``` python
ipython -i prereq.py
```

This will import some useful things, and set the following aliases, which you may find useful:

 * C: Show capture. Shows a capture of the current screen.
 * V: Viewer. An instance of the Viewer class, with the current gui and repo set.
 * S: Save current image. Saves the current image into the repo.
 * F: Show found. Highlights locations on the screen where the finder matched.
 * R: Show repo. Display a saved image.

This prereq file creates a `DirectoryRepo` in the current directory, allowing you to store images here.
It also sets up two of the most basic finders `approx_finder` and `exact_finder`, which can be used to match the stored images.


Finders
=======
Geist uses _finders_ to locate locations on the screen.
The most simple finder is `geist.finders.Location`, which simply represents a location on the screen.

## Searching for a finder
To actual perform the search for a location on a screen, use `gui.find_all`

``` python
# Search for a 15x15 square with top left at (10, 10)
gui.find_all(Location(10, 10, 15, 15))
```

There are many other methods on `GUI` which allow more nuanced searches.

 * `gui.find_all` returns all locations found by a finder.
 * `gui.wait_find_n` returns if it finds `n` matches within the timeout, else it raises `NotFoundError`.
 * `gui.exists` returns `True` if a match is found, else returns `False`.
 * `gui.exists_within_timeout` returns `True` if a match is found within the timeout, else returns `False`.

## Finder Composition
Some finders work on external information, such as `Location` which works on coordinates and `ApproxTemplateFinder`, which works with images.
However, many finders, such as `geist.filters.LocationFinderFilter` work with other finders.
Using these finders and filters we can join multiple finders, filter them, sort them and work on them in other ways.
This allows us to create powerful, flexible finders out of other, more simplistic finders.

For example, a common use case is to find the topmost result out of a finder.

``` python
top_most = lambda finder: SliceFinderFilter(
    SortingFinder(finder, lambda loc: loc.y)
)[0]

```

(`top_most` is actually available at `geist.filters.top_most`)


Repository
==========

A repository is a store of captured images.
Geist includes `geist.repo.DirectoryRepo` which stores images as .npy blobs in a directory.
These images can be used to search within the display, using `geist.visualfinders.ApproxTemplateFinder`.

Example:

``` python
from geist import DirectoryRepo

repo = DirectoryRepo('root_folder/folder/geist_repo')

approx_finder = TemplateFinderFromRepo(repo, ApproxTemplateFinder)
```

Backends
========

A backend is how geist interacts with the screen.
`geist.backends.get_platform_backend` will return the correct backend for the current system.

Example:

``` python
from geist.backends import get_platform_backend

backend = get_platform_backend()
```

GUI
===

The gui represents the user interface that geist will begin watching on.
This contains a number of properties/methods used to interact with the screen.
It is initialised with a backend.

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

The first useful method a viewer provides is the ability to view what is happening on the gui with show_capture.
You can zoom in to a particular part of the image using the magnifying glass button and return the the original view with the home button.

Example:

``` python
viewer.show_capture()
```

You can also save the image that is displayed in the viewer to the repository, which can then be used later to build finders.
To call the save method, pass in the name you want to save the image as.

Example:

``` python
viewer.save('image_name')
```

You can view the results of a particular finder with the show_found function.
This will highlight any part of the gui which the finder matches, whether it is one result or many.
It is called with the finder as an argument.

Example:

``` python
viewer.show_found(finder)
```

You can get the colour of the image in the viewer by using the get_colour method.
This will return a hsv object which can be used to create finders.
If there is just one colour in this image, it will match only this colour.
If there are multiple colours, it will match a range where h is between the minimum h value and maximum h value with the same being true for s and v.

Example:

``` python
colour = viewer.get_colour()
```
