import time
import psutil

def computer_usage(cpu_percent, memory_percent):
    while True:
        time.sleep(2.5)
        cpu_percent(psutil.cpu_percent())
        memory_percent(psutil.virtual_memory())

