==========
GUI Design
==========

The GUI is packaged in a module under the ``sqlenergy`` directory, and serves
as the interface for the core functionality provided in the ``core`` module.

A simple Model and ViewModel architecture is presented, where the Model contains
the relevant data for core functionality, whilst the ViewModels manage both the
interface layout and event handlers.

.. image:: applicationArchitecture.png

*********************************
View Class (View)
*********************************

The ``View`` class is simply a container which holds modular Frame classes.
For example, the ``FrameConnect``, ``FrameTable`` and ``FrameQuery`` frame classes.

These Frame classes are the ViewModel components of the application.

Each of these ViewModels must be designed to be modular, and should always be initialized
with the parent frame, ``parent``, and the model represented by the ``Context`` class (``ctx``).

::

    def __init__(self, parent, ctx, *args, **kwargs):

Importantly, the View class simply ensures one instance of the ``Context`` class
is sent to each frame. The Frames (ViewModel components) do not know of the existence
of each other and rely on the

*************************
Frame Classes (ViewModel)
*************************

Importantly, each Frame class provides callback functions and controller functions to
its own interface. These functions are designed with the assumption that a
``Context`` class exists and

*********************
Context Class (Model)
*********************

The ``Context`` class contains the information that each Frame requires to function.
It allows for different Frames to easily communicate with one another.
