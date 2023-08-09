"""
mapeia algumas teclas do teclado abnt2 (que contém a tecla altgr) no windows como no linux, por exemplo, altgr+y é mapeado para ←
"""

import base64
from io import BytesIO
from PIL import Image
from pynput import keyboard
import pystray


def en_dash():
    Global.controller.type('–')

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


def circumflex_accent():
    Global.controller.type('^')


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
        '<alt_gr>+-': en_dash,
        '<alt_gr>+y': left_arrow,
        '<alt_gr>+u': down_arrow,
        # não sei se é um bug ou 'feature' do pynput, mas seu eu pressionar <shift>+<alt_gr>+u, ele também dispara a hotkey <alt_gr>+shift+u
        '<shift>+<alt_gr>+u': up_arrow,
        '<alt_gr>+i': right_arrow,
        '<alt_gr>+´': grave_accent,
        '<alt_gr>+~': circumflex_accent,
        '<alt_gr>+z': left_double_angle_quote,
        '<alt_gr>+x': right_double_angle_quote,
        '<alt_gr>+v': left_double_quote,
        '<alt_gr>+b': right_double_quote,
        '<shift>+<alt_gr>+v': left_single_quote,
        '<shift>+<alt_gr>+b': right_single_quote,
    })
    Global.h.start()


def open_image_from_base64(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_bytes))
    return image


def quit_program(icon, item):
    icon.stop()
    # Global.h.stop()
    # os.kill(os.getpid(), signal.SIGTERM)


def create_tray_icon():
    image = open_image_from_base64('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADh0lEQVR4nL2Xv08jRxTHP7PeRDpTUKFrYjCItWVMCksGXdA1VLGEiJCoyB9wTegorslfkNJNKoqr0hFRpEFXXIEOCSKkiMLCCAsLOmx+GNYrjHdfirsd7drGNrHJSKP35s2beT++82Z2lYgAUK1WLeA98CPw2pf7NMh3kvWa/0qrwEcR+S0Wix0BKBGhWq3+BPwBRIdgpJ/5hoi8Gx8f/6AqlYoF/CMir4ZspNeaRxF5Y4rIe+BVcPLh4QHbtmk2mwAopfQGQb7X2OcNw8A0TQzDCDrxjYj8qi4vL89F5Dt/Ua1Wo1ar6cX90n50TNPENM2gE7YpIq99QaPR4O7uDqXUQIaeop7n4XmeHovIiBnEp16vD2SgH+p5XggKM5AOms1m1+iHAYPffJtm60l9qfQHadBmCIJBon9OlkIOBAXDMtBLR0Q6Q/B/pT/ogBEcBA2l02nS6XToYKZSKVKplB4Hu+u6FItFLMtienqam5ubjnqtZ8AIpsRXaDQa2plSqRTKjO9gMpkkkUiglMJxHFKpFEtLS1onm81ycnLSswqMTlWQyWTI5XLk83lWVlbaHEgkEpq3LIu9vT0Ajo6OKJVKlEolACKRCEoptra2iMfjxONxJicnQzA8WQXLy8vMzMwwOjqK4zhEo1Gtd3x8TDKZBKBYLGqHRkZGAKhUKuzv7+v9NjY2ANjd3WVsbKx7Fdzf3+vJq6srbm9vKRQKZLNZrROJRDTv3+1+ACLC/Py8lpXLZc1PTEzgeR6O43SGQCnF3NwcAOvr66yurgKwtrbWsRr8trm5CYBt2xiGQblcZnt7u023tQzbIPBbPp8nl8uhlOLi4oLFxUWur687OjA1NUWhUABgdna2ba9WB7pWgeu6ACwsLGjlWCzWcSM/aoBoNMrp6Sk7Oztadnh4yPn5uV53cHDQlgUAdXZ21uDLxwGu62oogsrDvIxc16VWq7XfhMMy8OzHKJSOIUTar07X53hQA91o8D0IOTDoxs+hXSHo9iIOA4bWxy8Eged5mKb5ojA4jhPKgiEil/7A/2rttdF/7Y7jUK/XgxA8mMAnEfnZj+zx8TGUiacOZ2smuvEiQr1ex7btUPTAR1UsFr8H/haRb1smX+KfMCgT4K1hWdaRiLzjy7+aVmrlO8lajfSz5msX4JdMJvPZAEgkEh9E5AfgTxGxBzXSZc0D8BfwNpPJ/A7wL9uCAUGUrGuVAAAAAElFTkSuQmCC')
    menu = (pystray.MenuItem("Quit", quit_program),)
    icon = pystray.Icon("ABNT2_Hotkeys", image, "ABNT2_Hotkeys", menu)
    icon.run()


class Global:
    pass


if __name__ == "__main__":
    set_hotkeys()
    Global.controller = keyboard.Controller()
    create_tray_icon()
