import threading

from kivy.clock import Clock


def mainloop(function):
    def wrapper(*args, **kwargs):
        if threading.current_thread():
            function(*args, **kwargs)

        else:
            Clock.schedule_once(lambda _elapsed_time: function(*args, **kwargs), 0)

    return wrapper



def next_frame(function):
    def wrapper(*args, **kwargs):
        Clock.schedule_once(lambda _elapsed_time: function(*args, **kwargs), 0)

    return wrapper
