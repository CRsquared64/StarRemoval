if __name__ == '__main__':
    from tkinter import Tk
    window = Tk()
    window.withdraw()

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    from kivy import *

    from kivy.logger import Logger
    from betterLogger import redo_logger_formatting

    redo_logger_formatting()
    Logger.info("AppBase: All things setup")

    import threadingFuncs
    from starRemovalApp import StarRemoval

    e = None

    try:
        Logger.info("AppBase: Running app")
        Star = StarRemoval()
        Star.run()

    except Exception as _e:
        e = _e

    finally:
        Logger.info("AppBase: Killing all other threads")
        amount = threadingFuncs.kill_all()
        Logger.info(f"AppBase: Killed {amount} threads")

        if e is not None:
            raise e
