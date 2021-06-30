import time
import psutil


def computer_usage(set_cpu_percent, set_memory_percent):
    while True:
        set_cpu_percent(psutil.cpu_percent())
        set_memory_percent(psutil.virtual_memory().percent)
        time.sleep(2.5)

