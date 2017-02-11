==========
GUI Design
==========

The GUI is packaged in a module under the ``sqlenergy`` directory, and serves
as the interface for the core functionality provided in the `core` module.

A simple MVC design approached is used for the GUI, when the ``Context`` class is the
model, the ``View`` class is the view, and the ``Main`` class is the controller.

****
View
****

The ``View`` class is simply a container which holds modular Tkinter Frames.
Specifically, the ``FrameConnect``, ``FrameTable`` and ``FrameQuery`` frame classes.
Each of these classes are designed to be modular, and should always be initialized
with the parent frame, ``parent`` and the model represented by the ``Context`` class (``ctx``).

::

    def __init__(self, parent, ctx, *args, **kwargs):

*******
Context
*******

The ``Context`` class contains the information that each Frame requires to function.
It allows for different Frames to easily communicate with one another.
