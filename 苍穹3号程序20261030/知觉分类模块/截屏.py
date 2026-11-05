import pyautogui
img=pyautogui.screenshot(region=(0,0,960,1080))
img.save("screenshot.png")