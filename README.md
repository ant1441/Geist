Geist
=====

Computer vision based UI automation library

This is an Alpha Prerelease (codename "I think it might work")

Please file bug reports.

Documentation
=============

Geist can, with a suitable backend and repository of images, inspect the backend and recognise the location of the given image in it.

For this introduction we shall assume linux, with Xvfb as a backend.

```
from geist import GUI
from geist.backends.xvfb import GeistXvfbBackend

backend = GeistXvfbBackend(2)
gui = GUI(backend)
```

This will create an Xvfb process on screen 2, storing the frame buffer in a temporary directory.

We then want to define a repository.

```
from geist import DirectoryRepo

repo = DirectoryRepo("/tmp/geist-repo")                                         
```
