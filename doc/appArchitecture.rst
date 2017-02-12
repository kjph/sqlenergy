==========
Application Design
==========

The application is packaged in the module ``app`` under the ``sqlenergy`` directory, and serves
as the interface for the core functionality provided in the ``core`` module.

A simple Model, View, and ViewModel architecture (MVVW) is presented, where the Model contains
the relevant data for core functionality, whilst modular ViewModels manage both the
interface and event handlers for a particular grouping of functions. A simple View component
groups together the modular ViewModels together.

.. image:: applicationArchitecture.png

*********************************
View Class (View)
*********************************

The ``View`` class is simply a container which holds modular ViewModels.
For example, the ``FrameConnect``, ``FrameTable`` and ``FrameQuery`` frame classes.

Importantly, the View class simply ensures one instance of the ``Context`` class
is sent to each ViewModel.

An instance of the application is created by first instantiating a ``Context`` class and a Tkinter
``Tk`` class, then passing these classes to the ViewClass. The application begins
on calling the ``Tk``'s ``mainloop()`` method.

*************************
Frame Classes (ViewModel)
*************************

ViewModels provide one logical group of functions and consist of a grouping of user interfaces and their corresponding functions.
That are intermediate *black-boxes* which process information and accordingly
update the core Model (``Context``).

Each of these ViewModels must be designed to be modular, agnostic of the existence of other ViewModels, and should always be initialized
with the parent frame, ``parent``, and the model represented by the ``Context`` class (``ctx``).

::

    def __init__(self, parent, ctx, *args, **kwargs):

Each ViewModel assumes that a ``Context`` class exists with the information it requires.
Importantly, the ViewModel is able to call a single method from the ``Context`` class
to retrieve and update said information -- this method is the ``Context.update_context()`` method.

Similarly, the ViewModel must provide a function handle to the ``Context`` class,
which acts as a stream that the ``Context`` class can retrieve its information from.

Put simply, the ViewModel assumes a unified input from the ``Context`` class, whilst
also providing a function handle (staticmethod) to the ``Context`` class for other ViewModels
to retrieve **its** information.

*********************
Context Class (Model)
*********************

The ``Context`` class contains the information that each ViewModel requires to function.
It allows for different ViewModels to easily communicate with one another.

The ``Context`` class has a ``.func`` attribute (``list``-type) which stores
each ViewModel's function handles. These functions are the ViewModels stream to
provide information to the ``Context`` (and all other ViewModels)

The ``Context`` class then provides a single method, ``update_context()`` which
any ViewModel can call to update the entire state of the Model.
