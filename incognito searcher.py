import pyautogui
import keyboard

pyautogui.PAUSE = 0.3
keyboard.press_and_release('alt+tab')
pyautogui.moveTo(1896, 63)
pyautogui.click()  
pyautogui.moveTo(1789, 158)
pyautogui.click()
pyautogui.write('search something')
pyautogui.press('enter')
pyautogui.moveTo(830, 860)
pyautogui.click()  
pyautogui.moveTo(295, 230)
pyautogui.click()
pyautogui.moveTo(275, 285)
pyautogui.click()
pyautogui.click()
 