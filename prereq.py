try:
    get_ipython().magic(u'pylab')
except NameError
    pass
import sys

from geist import *
from geist.backends.fake import GeistFakeBackend
from geist.pyplot import Viewer


def init_gui():
    backend = get_platform_backend()
    gui = GUI(backend)
    return backend, gui


def fake_gui(filename):
    backend = GeistFakeBackend(image=filename)
    gui = GUI(backend)
    return backend, gui


backend, gui = init_gui()
if sys.platform == 'linux2':
    backend.create_process('fluxbox')
#backend, gui = fake_gui('submit.npy')

repo = DirectoryRepo('.')
approx_finder = TemplateFinderFromRepo(repo, ApproxTemplateFinder)
exact_finder = TemplateFinderFromRepo(repo, ExactTemplateFinder)

V = Viewer(gui, repo)
S = V.save
C = V.show_capture
F = V.show_found
R = V.show_repo
