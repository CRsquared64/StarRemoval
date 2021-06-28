import cv2
import numpy as np
import time
import psutil


def RemoveStars(dio, jotaro):
    i = 0

    start = time.time()
    threshold = jotaro
    global image
    image = cv2.imread(dio)
    # image = cv2.resize(image, (800,800))
    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('original', image)
    # cv2.imshow('greyscale', imageG)

    template = cv2.imread('template2.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(imageG, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # masking by rotem on stackoverflow
    global mask
    mask = np.zeros_like(imageG)
    for pt in zip(*loc[::-1]):
        # a = cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        cv2.rectangle(mask, (pt[0] + 4, pt[1] + 4), (pt[0] + w - 3, pt[1] + h - 3), 255, -1)
        # Reduce the size of the rectangle by 3 pixels from each side. old method by rotem
        cv2.circle(mask, (pt[0] + 4, pt[1] + 4), (w - h + 3), 255, -3)  # faster method
        # use both methods and it stil workss/might be better idk its late ok
        i = i + 1

    image = cv2.inpaint(image, mask, 2, cv2.INPAINT_NS)
    cv2.imwrite("finished.jpg", image)


# use this to resize image if its too large image = cv2.resize(image, (800,800))


    # end = time.time()
    # final = end - start
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    # print("Generated in: ", final)
    # print(i, "Stars Detected and masked.")
    print("CPU Usage:", cpu)
    print("Memory used: ", memory[2])
    print("Cpu and Memory values may not be accurate, measures full pc usage.")
    cv2.destroyAllWindows()
