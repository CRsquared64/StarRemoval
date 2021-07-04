if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    threading_manager = multiprocessing.Manager()

    from tkinter import Tk
    window = Tk()
    window.withdraw()

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    from kivy import *

    import threadingFuncs
    from starRemovalApp import StarRemoval

    try:
        Star = StarRemoval()
        Star.run()
    finally:
        threadingFuncs.kill_all()
