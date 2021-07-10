if __name__ == '__main__':
    from tkinter import Tk
    window = Tk()
    window.withdraw()

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    from kivy import *

    from kivy.logger import Logger
    Logger.info("AppBase: All things setup")

    import threadingFuncs
    from starRemovalApp import StarRemoval

    try:
        Logger.info("AppBase: Running app")
        Star = StarRemoval()
        Star.run()
    except Exception as e:
        raise e

    Logger.info("AppBase: Killing all other threads")
    amount = threadingFuncs.kill_all()
    Logger.info(f"AppBase: Killed {amount} threads")

    import sys
    sys.exit()
