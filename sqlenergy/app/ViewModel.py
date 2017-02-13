from collections import OrderedDict
from Tkinter import Frame
from ttk import *

def add_func_group(context, func, group):
    """
    Function binding to context for on_call method
    """

    context.funcgroup[group].append(func)

def set_update_func(context, func):
    """
    Function binding to context for global update
    """

    context.func.append(func)

def get_frame(obj, frame_list):
    """
    return frame specifed in frame_list
    """

    if isinstance(frame_list, str):
        frame_list = [frame_list]

    for f in frame_list:
        obj = obj.frames[f]

    return obj

def get_widget(obj, frame_list, widget):
    """
    Return widget under the frame tree
    """

    f = get_frame(obj, frame_list)
    return f.widgets[widget]

def pack_widgets(widgets, packing, globalconf=None):
    """
    Pack all widgets specified in packing dictionary

    Parameters
    ----------
    widgets:    dict; values are Tkinter Objects
    packing:    list of tuples; keys are matching with widgets, values are packopts
                specify a 'extconf' key with an additional dictionary to extend options
                this key will be removed on packing.
                Alternatively, use this key to overwrite the globalconf option
                Note that the packing order is presrved
    globalconf: Specify a global dictionary to append to all packopts (extconf keys are taken priority)
    """

    corrected_packing = []
    for p in packing:
        if isinstance(p, tuple):
            corrected_packing.append(p)
        elif isinstance(p, str):
            corrected_packing.append((p, None))

    packing = OrderedDict(corrected_packing)
    for wid, packopts in packing.iteritems():

        if packopts == None:
            if isinstance(globalconf, dict) and len(globalconf) > 0:
                packopts = globalconf
            else:
                packopts = {}
        elif 'extconf' in packopts:
            packopts.update(packopts['extconf'])
            packopts.pop('extconf', None)
        elif isinstance(globalconf, dict) and len(globalconf) > 0:
            packopts.update(globalconf)

        widgets[wid].pack(**packopts)

def mk_frames_in(obj, frame_spec, globalconf=None):
    """
    Create frames under obj specified in frame_spec.

    Parameters
    ----------
    obj:            Parent container
    frame_spec:     list; Each element contains a single frame specification
                    Each element may be a
                    - str; in which case the packing options is set to globalconf (if set)
                      Or to an empty dict elsewise
                    - tuple; in which case the first tuple element is the frame name (str)
                      and the second tuple element is the frame packing opts (dict). A dictionary
                      can be extended in this second element by using the key 'extconf' (not that
                      this will override any globalconf spec used)
    global_conf:    A dictionary which will be appended to all frame_specs for packing
                    Individual frames may 'opt-out' of this global_conf by including the key
                    'extconf' in their tuple spec with value = {} (or any other dict)
    """

    corrected_frame_spec = []
    for f in frame_spec:
        if isinstance(f, tuple):
            corrected_frame_spec.append(f)
        elif isinstance(f, str):
            corrected_frame_spec.append((f, None))

    frame_spec = OrderedDict(corrected_frame_spec)

    #Create the frames
    frame_list = [f for f in frame_spec]
    try:
        obj.frames.update(OrderedDict((f, Frame(obj)) for f in frame_list))
    except AttributeError:
        obj.frames = OrderedDict((f, Frame(obj)) for f in frame_list)

    #Pack the frames
    for f, packopts in frame_spec.iteritems():

        if packopts == None:
            if isinstance(globalconf, dict) and len(globalconf) > 0:
                packopts = globalconf
            else:
                packopts = {}
        elif 'extconf' in packopts:
            packopts.update(packopts['extconf'])
            packopts.pop('extconf', None)
        elif isinstance(globalconf, dict) and len(globalconf) > 0:
            packopts.update(globalconf)

        obj.frames[f].pack(**packopts)
