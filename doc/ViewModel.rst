========================
ViewModels (Frames)
========================

ViewController Frames are always initialized with the definition:

::

    def __init__(self, parent, ctx, *args, **kwargs):

In general, every Tkinter Frame object should further have a ``.frames`` and a ``.widget``
dictionary attribute assigned to it. This ensures there is no namespace clashes.

Subsequent Frames nested inside will be binded to a key-value map in the ``.frames`` dictionary
and widgets will be binded to a key-value map in the ``.widgets`` dictionary.

This further paves the path for a patch which allows building the UI using descriptor files
such as a ``.json`` or ``.xml`` file

**************************
Making and Fetching Frames
**************************

Frames are to be made with the function ``ViewModel.mk_frames_in(parent, frame_list, **pack_opts)``
The function will make all frames specified in ``frame_list`` under the parent object. These frames
will all be packed with options specified in ``pack_opts``.

Accessing frames is to be done with the function ``ViewModel.get_frame()``. This
ensures that a uniformed access method is done, and allows for each modification
should a patch require so

**************************
Code Structure for Layouts
**************************

It is recommended that for each **complicated** frame, a ``def initUI_*()`` method
is created. This method should be structured by first creating the frames' ``.widget()``
dictionary, and then followed by the ``.pack()``-ing order.

The motivation for this is, to separate the Model and View aspects into two distinct sections
of code for each Frame. That is, the ``.widget()`` gives readers an understanding of the Model of a frame (the UI components, their functions and their properties), whilst the ``.pack()``-ing
order is only related to the layout.

For example, in the ``def initUI_btn()`` method of ``FrameTable.py``

::

    def initUI_btn(self, parent):

        #Make widgets
        #'Model'
        parent.widgets = {'btn-fetch': Button(parent, text="Fetch", width=8, command=self.fetch_tables),
                          'btn-clear': Button(parent, text="Clear", width=8, command=self.clear_tables),
                          'btn-loadf': Button(parent, text="Load from File", width=12, command=self.load_tables)}

        #Packing order
        #'View' or Layout
        parent.widgets['btn-fetch'].pack(side=tk.LEFT)
        parent.widgets['btn-clear'].pack(side=tk.RIGHT)
        parent.widgets['btn-loadf'].pack(side=tk.RIGHT)

Note that this method of declaring ``Tk`` widgets in a dictionary is **very likely** to cause
``PEP8`` contraventions.

****************************************
Remarks on the ``Pack()`` layout manager
****************************************

The ``.pack()`` method was selected because of its ease of use.
Importantly, when ``.pack``-ing, a new widget it does not need to know about the existence
of other widgets or any predefined grid, it simply is packed where called. This allows
for an easily expandable GUI if need be. However, because the ``.pack()`` method
is relatively simple, extensive frames must be created to allow for more complicated
layouts. As such the use of the ``ViewModel`` module is important to ensure scalability

Because of the way that ``.pack()`` is designed, a frame must be made each time
a group of widgets is to be packed along another direction (different from the last
packing direction). As stated above, this will lead to a large number of frames, which
are best managed through one unified access/manager

Understanding the layout should be fairly simple. For example the ``__init()__`` function
for the ``FrameTables`` class is as below:

::

    def __init__(self, parent, ctx, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #Frames (containers for UIs)
        ViewModel.mk_frames_in(self, ['top', 'main', 'btn'],
                       **{'fill': tk.BOTH})

        #Widget
        self.initUI_top(ViewModel.get_frame(self, 'top'))
        self.initUI_main(ViewModel.get_frame(self, 'main'))
        self.initUI_btn_frame(ViewModel.get_frame(self, 'btn'))

It can be see that under the ``#Frames...`` section, three frames are made and packed
below each other (``'top'``, ``'main'``, and ``'btn'``).

Their own widgets are then created using the ``initUI_*()`` methods. We know that the frames split the parent frame into thirds, and to examine each third we simply look at the ``initUI_*()`` method
for the frame in question.

A similar structure should then exist for these methods, and if frames are to be continuously nested; then in the same fashion.
