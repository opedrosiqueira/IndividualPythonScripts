"""
mapeia algumas teclas do teclado abnt2 (que contém a tecla altgr) no windows como no linux, por exemplo, altgr+y é mapeado para ←
"""

from PIL import Image
from pynput import keyboard
import pystray


def left_arrow():
    Global.controller.type('←')


def down_arrow():
    Global.controller.type('↓')


def up_arrow():
    Global.controller.type('↑')


def right_arrow():
    Global.controller.type('→')


def grave_accent():
    Global.controller.type('`')


def left_double_angle_quote():
    Global.controller.type('«')


def right_double_angle_quote():
    Global.controller.type('»')


def left_single_angle_quote():
    Global.controller.type('‹')


def right_single_angle_quote():
    Global.controller.type('›')


def left_double_quote():
    Global.controller.type('“')


def right_double_quote():
    Global.controller.type('”')


def left_single_quote():
    Global.controller.type('‘')


def right_single_quote():
    Global.controller.type('’')


def set_hotkeys():
    Global.h = keyboard.GlobalHotKeys({
        '<alt_gr>+y': left_arrow,
        '<alt_gr>+u': down_arrow,
        # não sei se é um bug ou 'feature' do pynput, mas seu eu pressionar <shift>+<alt_gr>+u, ele também dispara a hotkey <alt_gr>+shift+u
        '<shift>+<alt_gr>+u': up_arrow,
        '<alt_gr>+i': right_arrow,
        '<alt_gr>+´': grave_accent,
        '<alt_gr>+z': left_double_angle_quote,
        '<alt_gr>+x': right_double_angle_quote,
        '<alt_gr>+v': left_double_quote,
        '<alt_gr>+b': right_double_quote,
        '<shift>+<alt_gr>+v': left_single_quote,
        '<shift>+<alt_gr>+b': right_single_quote,
    })
    Global.h.start()


def quit_program(icon, item):
    icon.stop()
    # Global.h.stop()
    # os.kill(os.getpid(), signal.SIGTERM)


def create_tray_icon():
    image = Image.open("alt_gr.png")
    menu = (pystray.MenuItem("Quit", quit_program),)
    icon = pystray.Icon("ABNT2_Hotkeys", image, "ABNT2_Hotkeys", menu)
    icon.run()


class Global:
    pass


if __name__ == "__main__":
    set_hotkeys()
    Global.controller = keyboard.Controller()
    create_tray_icon()
