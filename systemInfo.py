import time
import psutil

def computer_usage(cpu_percent, memory_percent):
    time.sleep(5)
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()
