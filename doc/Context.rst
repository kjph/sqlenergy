==================
Context Management
==================

*****************
Function Bindings
*****************

There are two methods to bind a function to the Context class.

::

    ViewModel.set_update_func(context, func)
    ViewModel.add_func_group(context, func, group)

``set_update_func`` binds ``func`` (must be a ``staticmethod()``) to the current
``Context`` class, and is called every time the ``Context.update_context()`` method
is called.

``add_func_group`` allows ViewModels to call other ViewModels' methods for certain
events.

For example, consider two ViewModels ``A`` and ``B``. Every time ``A.func()``
is called, we also want to call ``B.func()``. This can be done by binding ``B.func``
to some function group using the command below:

::

    Class B(tk.Frame):

        def __init__(...):
            ViewModel.add_func_group(context, staticmethod(self.func), 'someGroup')

        def func(self):
            #do something

And in the ``A`` class

::

    Class A(tk.Frame):

        def func(self):
            self.ctx.on_call('someGroup')

            #Do more things
