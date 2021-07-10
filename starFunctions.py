import os
import time

import cv2
import numpy as np
from kivy import Logger


def get_amount_of_stars(path, threshold, callbacks):
    image = cv2.imread(path)
    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    Logger.info("Processor: Loading template")
    template = cv2.imread('star.png', 0)
    w, h = template.shape[::-1]

    Logger.info("Processor: Matching template")
    res = cv2.matchTemplate(imageG, template, cv2.TM_CCOEFF_NORMED)

    Logger.info("Processor: Generating mask")
    loc = np.where(res >= threshold)

    callbacks["stars"](len([i for i in zip(*loc[::-1])]))


def remove_stars(path, threshold, out_path, save_mask, callbacks, mask_path=None):
    Logger.info("Processor: Loading image and converting to grey")
    Logger.debug(f"Threshold: current set to {threshold}")

    start = time.time()
    image = cv2.imread(path)
    # image = cv2.resize(image, (800,800))
    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('original', image)
    # cv2.imshow('greyscale', imageG)


    Logger.info("Processor: Loading template")
    template = cv2.imread('star.png', 0)
    w, h = template.shape[::-1]

    Logger.info("Processor: Matching template")
    res = cv2.matchTemplate(imageG, template, cv2.TM_CCOEFF_NORMED)

    Logger.info("Processor: Generating mask")
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

    callbacks["stars"](i)


    if save_mask:
        Logger.debug(f"Processor: Saving mask to {mask_path}")
        try:
            os.makedirs(os.path.split(mask_path)[0])

        except FileExistsError:
            pass

        cv2.imwrite(mask_path, mask)


    Logger.info("Processor: Using Mask...")
    image = cv2.inpaint(image, mask, 2, cv2.INPAINT_NS)


    Logger.info(f"Processor: Writing image to file "
                f"{out_path}")
    try:
        os.makedirs(os.path.split(out_path)[0])

    except FileExistsError:
        pass
    cv2.imwrite(out_path, image)

    Logger.info(f"Processor: Finished in {time.time() - start}")
    callbacks["time"](time.time() - start)


    callbacks["finished"]()

