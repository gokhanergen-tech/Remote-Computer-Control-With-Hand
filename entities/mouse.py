from concurrent.futures import ThreadPoolExecutor

import psutil
import pyautogui
import time

pool = ThreadPoolExecutor(max_workers=psutil.cpu_count())


class Mouse():
    before = None
    after = None

    hasClick = False

    def __init__(self, screen_width, screen_height):
        self._swidth = screen_width
        self._sheight = screen_height

    def move(self, x, y):

        if (y > 0 and x > 0 and y < self._sheight and x < self._swidth):
            pyautogui.moveTo((x, y))

    def start_click(self, button):
        self.hasClick = True
        if (self._swidth > pyautogui.position()[0] and pyautogui.position()[1] < self._sheight):
            if (button == "left"):
                pyautogui.click(pyautogui.position()[0]
                                , pyautogui.position()[1])
            elif (button == "right"):
                pyautogui.click(pyautogui.position()[0], pyautogui.position()[1], button="right")
            else:
                pyautogui.doubleClick(pyautogui.position()[0], pyautogui.position()[1])
            self.hasClick = False

    def click(self, button="left"):
        time.sleep(0.15)
        if (not self.hasClick):
            pool.submit(self.start_click, button)
