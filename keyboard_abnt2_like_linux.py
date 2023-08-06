"""
mapeia algumas teclas do teclado abnt2 (que contém a tecla altgr) no windows como no linux, por exemplo, altgr+y é mapeado para ←
"""

from enum import Enum
from pynput.keyboard import Key, KeyCode, Controller as KeyController, Listener as KeyListener
import time


class Keyboard(Enum):
    Escape = 'Escape'
    AltRight = 'AltRight'


def get_key(key):
    if isinstance(key, KeyCode):
        if key.char is not None:
            return key.char
        elif key.vk is not None:
            return key.vk
        else:
            return None
    elif isinstance(key, Key):
        if key == Key.alt_gr:
            print("AltGr (Right Alt) key pressed.")
        return {
            27: Keyboard.Escape,
            165: Keyboard.AltRight
        }.get(key.value)
    else:
        return 'i dont know'


def tap_button(key, times=1, delay=0.005):
    for _ in range(times):
        keyboard.tap(key)
        if delay > 0.0:
            time.sleep(delay)


def on_press(key):
    if keyboard.alt_gr_pressed:
        print('altgr')
    return
    if get_key(key) == Keyboard.Escape:
        return False
    keys.keys[get_key(key)] = True


def on_release(key):
    if keyboard.alt_gr_pressed:
        print('altgr')
    # print(get_key(key), keys.keys[get_key(key)])
    # keys.keys[get_key(key)] = False
    if get_key(key) == 'y':
        print('y')


class Keys:
    def __init__(self) -> None:
        self.keys = {}


if __name__ == '__main__':
    keys = Keys()
    keyboard = KeyController()
    keyboard_listener = KeyListener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    keyboard_listener.join()
