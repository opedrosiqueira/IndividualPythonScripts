# macro para baixar as páginas carregadas do bvpearson, no meu windows 10, mas precisa estar com as ferramentas do desenvolvedor aberta na aba networks

import time
from pynput.keyboard import Key, Controller as KeyController, Listener as KeyListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
import mss


def action():
    global current
    changeposition(48, 824)
    click(delay=0.1)
    tap_button(Key.down, 2, delay=0.1)
    changeposition(610, 673, delay=0.5)
    click(Button.right, delay=0.1)
    tap_button(Key.up, delay=0.1)
    tap_button(Key.enter, delay=0.5)
    # changeposition(679, 760, delay=0.1)
    # click(delay=1.0)
    keyboard.type(f"{current:03d}.jpg")
    time.sleep(0.1)
    tap_button(Key.enter, delay=0.3)
    current += 1


def tap_button(key, times=1, delay=0.005):
    for _ in range(times):
        keyboard.tap(key)
        if delay > 0.0:
            time.sleep(delay)


def click(side=Button.left, delay=0.005):
    mouse.click(side)
    time.sleep(delay)


def changeposition(x, y, delay=0.005):
    mouse.position = (x, y)
    time.sleep(delay)


def on_release(key):
    if key == Key.esc:
        mouse_listener.stop()
        return False  # Stop listener
    elif key == Key.shift_l:
        for _ in range(count):
            action()


def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released', (x, y)), mouse.position)


# --- main ---

current = 6
count = 20


keyboard = KeyController()
mouse = MouseController()


# Setup the listener threads
keyboard_listener = KeyListener(on_release=on_release)
mouse_listener = MouseListener(on_click=on_click)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
