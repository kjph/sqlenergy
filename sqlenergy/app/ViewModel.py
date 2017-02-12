from collections import OrderedDict
import Tkinter as tk
from Tkinter import Frame

def add_func_group(context, func, group):
    context.funcgroup[group].append(func)

def set_update_func(context, func):
    context.func.append(func)

def get_frame(obj, frame_list):

    if isinstance(frame_list, str):
        frame_list = [frame_list]

    for f in frame_list:
        obj = obj.frames[f]

    return obj

def get_widget(obj, frame_list, widget):

    f = get_frame(obj, frame_list)
    return f.widgets[widget]

def pack_widgets(widgets, packing):

    packing = OrderedDict(packing)
    for wid, packopts in packing.iteritems():
        widgets[wid].pack(**packopts)

def mk_frames_in(obj, frame_list, **pack_opts):

    if isinstance(frame_list, str):
        frame_list = [frame_list]

    try:
        obj.frames.update(OrderedDict((f, Frame(obj)) for f in frame_list))
    except AttributeError:
        obj.frames = OrderedDict((f, Frame(obj)) for f in frame_list)

    for f in frame_list:
        obj.frames[f].pack(**pack_opts)
