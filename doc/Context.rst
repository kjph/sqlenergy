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

******************
Context Attributes
******************

The ``core`` model attributes are defined with immutable attributes in the Class definition
of ``Context``. These immutable tuples ensures that object instances cannot vary these attributes
and cause problems in the code. This is especially important when scaling, without which it would
be difficult to track what the attribute is.

Furthermore, these immutable objects define the structure of the core attributes, and should
be used at all times. For example, for the database information attribute (``dbi``) we have the immutable tuple
in ``Context``

::

    class Context():

        def __init__(...):
            self.dbi_fields = ('host', 'user', 'passwd', 'db', 'port')

Now, all ViewModels concerned with ``dbi`` should create structures as follows:

::

    for field in self.ctx.dbi_fields:
        dbi[field] = #the field value

    self.ctx.dbi = dbi

This ensures uniform usage of keys is used, and that the ``Context`` class can easily be modified
to accommodate any changes in the ``core`` module

It is recommended that non-core attributes be assigned to object instances and not the class itself.
Furthermore, containers (dictionaries for example) should be used to group like-attributes.
This prevents polluting the attribute space.

An example container in an ``Context`` instance is:

::

        self.ctx.const = {'win_width': 760,#Window width
                          'font_title': "Arial 9 bold"}#Font of titles
