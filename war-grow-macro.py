import time
from pynput.keyboard import Key, Controller as KeyController, Listener as KeyListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
import mss

sct = mss.mss()
w = sct.monitors[1]["width"]
h = sct.monitors[1]["height"]
print("screen", w, h)

positions = [
    [(w*0.63103953147877, h*0.950520833333333), (w*0.631771595900439, h*0.87890625), (w*0.366764275256223, h*0.877604166666667), (w*0.676427525622255, h*0.8515625),
     (w*0.51683748169839, h*0.650462962962963), (w*0.64875, h*0.472222222222222), (w*0.284375, h*0.712222222222222), (w*0.648125, h*0.711111111111111), (w*0.685625, h*0.9)],
    [(w*0.590104166666667, h*0.908796296296296), (w*0.591145833333333, h*0.86712962962963), (w*0.4109375, h*0.868055555555556), (w*0.677083333333333, h*0.905092592592593),
     (w*0.557291666666667, h*0.606018518518519), (0.730208333333333, h*0.616666666666667), (w*0.829166666666667, h*0.605555555555555), (w*0.7265625, h*0.599074074074074), (w*0.505208333333333, h*0.853703703703704)]
]

stay = False
listenmouse = False
version = positions[0]


def on_press(key):
    global version
    global x
    global y
    global stay
    if not stay:
        x = mouse.position[0]
        y = mouse.position[1]
    stay = False

    try:
        if not hasattr(key, 'char'):
            key.char = None
        if key == Key.esc:
            if listenmouse:
                mouse_listener.stop()
            return False  # Stop listener
        elif key.char == 'z':  # all
            stay = True
            changeposition(version[0][0], version[0][1], sleeptime=0.1)
        elif key.char == 'x':  # plus
            stay = True
            changeposition(version[1][0], version[1][1])
        elif key.char == 'c':  # minus
            stay = True
            changeposition(version[2][0], version[2][1])
        elif key.char == 'v':  # pass
            changeposition(version[3][0], version[3][1], sleeptime=0.1)
        elif key.char == 'b':  # ok
            changeposition(version[4][0], version[4][1], sleeptime=0.1)
        elif key.char == 'n':  # click
            stay = True
        elif key.char == 'm':  # choose bot players
            stay = True

            changeposition(version[5][0], version[5][1], sleeptime=.1)
            clickleft(.1)

            changeposition(version[6][0], version[6][1], sleeptime=.1)
            clickleft(.1)

            changeposition(version[7][0], version[7][1], sleeptime=.1)
            clickleft(.1)

            changeposition(version[8][0], version[8][1], sleeptime=.5)
            clickleft(.1)
        elif key.char == ',': # change game between war and roman
            if version == positions[1]:
                version = positions[0]
                print("war")
            else:
                version = positions[1]
                print("roman")

        if key.char in ['x', 'c', 'n']:
            clickleft()
        if key.char in ['z', 'v', 'b']:
            clickleft(sleeptime=0.1)

    except Exception as ex:
        print(ex)

    if not stay:
        # pass
        changeposition(x, y)


def clickleft(sleeptime=0.005):
    mouse.click(Button.left)
    time.sleep(sleeptime)


def changeposition(x, y, sleeptime=0.005):
    mouse.position = (x, y)
    time.sleep(sleeptime)


def on_release(key):
    if key == Key.esc:
        if listenmouse:
            mouse_listener.stop()
        return False  # Stop listener


def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))


# --- main ---
keyboard = KeyController()
mouse = MouseController()


# Setup the listener threads
keyboard_listener = KeyListener(on_press=on_press, on_release=on_release)
if listenmouse:
    mouse_listener = MouseListener(on_click=on_click)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
if listenmouse:
    mouse_listener.start()
keyboard_listener.join()
if listenmouse:
    mouse_listener.join()
