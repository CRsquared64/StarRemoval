if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()

    from tkinter import Tk
    window = Tk()
    window.withdraw()

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    from kivy import *

    import killableThreads
    from starRemovalApp import StarRemoval

    try:
        Star = StarRemoval()
        Star.run()
    finally:
        killableThreads.kill_all()
