import os

import cv2
import numpy as np
import time
import psutil
from kivy import Logger
from kivy.clock import Clock


def remove_stars(dio, jotaro, on_finish, _set_processing_text, _set_stars_amount, time_taken):
    set_processing_text = lambda text: Clock.schedule_once(lambda _elapsed_time: _set_processing_text(text), 0)
    set_stars_amount = lambda amount: Clock.schedule_once(lambda _elapsed_time: _set_stars_amount(amount), 0)
    time_taken = lambda amount: Clock.schedule_once(lambda _elapsed_time: time_taken(amount), 0)

    start = time.time()
    image = cv2.imread(path)
    # image = cv2.resize(image, (800,800))
    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('original', image)
    # cv2.imshow('greyscale', imageG)

    Logger.info("Processor: Loaded image and converted to grey")
    set_processing_text("Loaded image and converted to grey")

    template = cv2.imread('star.png', 0)
    w, h = template.shape[::-1]
    Logger.info("Processor: Loaded template")
    set_processing_text("Loaded template")

    res = cv2.matchTemplate(imageG, template, cv2.TM_CCOEFF_NORMED)
    Logger.info("Processor: Matched template")
    set_processing_text("Matched template")

    loc = np.where(res >= threshold)
    # masking by rotem on stackoverflow
    mask = np.zeros_like(imageG)

    i = 0
    for pt in zip(*loc[::-1]):
        # a = cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        cv2.rectangle(mask, (pt[0] + 4, pt[1] + 4), (pt[0] + w - 3, pt[1] + h - 3), 255, -1)
        # Reduce the size of the rectangle by 3 pixels from each side. old method by rotem
        cv2.circle(mask, (pt[0] + 4, pt[1] + 4), (w - h + 3), 255, -3)  # faster method
        # use both methods and it stil workss/might be better idk its late ok
        i = i + 1

    set_stars_amount(i)

    Logger.info("Processor: Generated mask")
    set_processing_text("Generated mask")

    set_processing_text("Using Mask...")
    Logger.info("Processor: Using Mask...")
    image = cv2.inpaint(image, mask, 2, cv2.INPAINT_NS)
    Logger.info("Processor: Used mask ")
    set_processing_text("Used Mask")

    cv2.imwrite(str(os.path.splitext(path)[0] + "-no_stars-" + str(threshold) + os.path.splitext(path)[1]), image)
    Logger.info(f"Processor: Wrote image to file "
                f"{str(os.path.splitext(path)[0] + '-no_stars-' + str(threshold) + os.path.splitext(path)[1])}")
    set_processing_text("Saved to file")

    Logger.info(f"Processor: Finished in {time.time() - start}")
    set_processing_text("Done")
    finished_time = time.time() - start
    time_taken(finished_time)

    on_finish_callback()

    cpu = psutil.cpu_percent()
    Logger.info(f"Processor: CPU Usage: {cpu}")
    memory = psutil.virtual_memory()
    Logger.info(f"Processor: Memory used: {memory[2]}")
    Logger.info(f"Processor: Cpu and Memory values may not be accurate, measures full pc usage.")
