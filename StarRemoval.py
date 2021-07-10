if __name__ == '__main__':
    from tkinter import Tk
    window = Tk()
    window.withdraw()

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    from kivy import *

    from kivy.logger import Logger, formatter, formatter_message
    from logging import _STYLES

    formatter._fmt = formatter_message(
                '[%(threadName)-18s] [%(levelname)-18s] %(message)s', True)
    formatter._style = _STYLES["%"][0](formatter._fmt)
    Logger.info("AppBase: All things setup")

    import threadingFuncs
    from starRemovalApp import StarRemoval

    try:
        Logger.info("AppBase: Running app")
        Star = StarRemoval()
        Star.run()

    except Exception as e:
        raise e

    finally:
        Logger.info("AppBase: Killing all other threads")
        amount = threadingFuncs.kill_all()
        Logger.info(f"AppBase: Killed {amount} threads")

        import sys
        sys.exit()
