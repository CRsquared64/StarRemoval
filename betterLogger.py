import os

from kivy.logger import Logger as _Logger

log_class_length = 18


def redo_logger_formatting():
    # noinspection PyProtectedMember
    from kivy.logger import formatter_message, COLOR_SEQ, COLORS, RESET_SEQ, ColoredFormatter as _ColoredFormatter
    import logging
    from kivy import logger as kvLogger


    class ColoredFormatter(_ColoredFormatter):
        def format(self, record: logging.LogRecord) -> str:
            # noinspection PyBroadException
            try:
                msg: (str, str) = record.msg.split(':', 1)
                if len(msg) == 2:
                    record.msg = ('[%-' + str(log_class_length) + 's]%s') % (msg[0], msg[1])
            except Exception:
                print("redo_logger_formatting broke!")
            levelname: str = record.levelname
            if record.levelno == kvLogger.LOG_LEVELS["trace"]:
                levelname: str = 'TRACE'
                record.levelname = levelname
            if self.use_color and levelname in COLORS:
                levelname_color: str = (
                        str(COLOR_SEQ % (30 + COLORS[levelname])) + "[" + levelname)
                record.levelname = levelname_color
            return logging.Formatter.format(self, record)




    # noinspection SpellCheckingInspection
    use_color: bool = (
            (
                    os.environ.get("WT_SESSION") or
                    os.environ.get("COLORTERM") == 'truecolor' or
                    os.environ.get('PYCHARM_HOSTED') == '1' or
                    os.environ.get('TERM') in (
                        'rxvt',
                        'rxvt-256color',
                        'rxvt-unicode',
                        'rxvt-unicode-256color',
                        'xterm',
                        'xterm-256color',
                    )
            ) and os.environ.get('KIVY_BUILD') not in ('android', 'ios')
    )
    if not use_color:
        color_fmt: str = formatter_message(
            '[%(threadName)-18s] [%(levelname)-7s] %(message)s', use_color)

    else:
        color_fmt: str = formatter_message(
            RESET_SEQ + '[%(threadName)-18s] %(levelname)-18s] %(message)s', use_color)

    formatter: ColoredFormatter = ColoredFormatter(color_fmt, use_color=use_color)

    _Logger.handlers[2].setFormatter(formatter)
