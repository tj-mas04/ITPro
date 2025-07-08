import pyautogui
import time 


time.sleep(5)

for i in range(900):
    pyautogui.moveTo(1050, 534, duration=0.5)
    pyautogui.click()
    time.sleep(1)
