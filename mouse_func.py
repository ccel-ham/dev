import pyautogui as pygui
from pynput.mouse import Listener, Button
import time

def on_move(x, y):
    print(f"move to : ({x}, {y})")

def on_click(x, y, button, pressed):
    button_name = None
    if button == Button.left:
        button_name = "left "
    elif button == Button.right:
        button_name = "right "
    elif button == Button.middle:
        button_name = "middle "
    elif button == Button.x:
        button_name = f"button {button.value}"
    elif button == Button.y:
        button_name = f"button {button.value}"
    
    action = "clicked" if pressed else "relese"
    print(f"{button_name}  {action} : ({x}, {y})")

def on_scroll(x, y, dx, dy):
    print(f"scroll : ({x}, {y}) ({dx}, {dy})")

def check_mouse_info():
    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def pyautogui_functions():
    # serch image by screen
    image = 0
    box = pygui.locateOnScreen(image)
    while box is None:
        time.sleep(2)
        box = pygui.locateOnScreen(image)
    # return box center
    center_point = pygui.center(box)
    # Click
    pygui.click(center_point)
