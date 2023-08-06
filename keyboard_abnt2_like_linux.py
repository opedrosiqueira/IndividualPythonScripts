"""
mapeia algumas teclas do teclado abnt2 (que contém a tecla altgr) no windows como no linux, por exemplo, altgr+y é mapeado para ←
"""

from pynput import keyboard

controller = keyboard.Controller()


def left_arrow():
    controller.type('←')


def down_arrow():
    controller.type('↓')


def up_arrow():
    controller.type('↑')


def right_arrow():
    controller.type('→')


def grave_accent():
    controller.type('`')


def left_double_angle_quote():
    controller.type('«')


def right_double_angle_quote():
    controller.type('»')


def left_single_angle_quote():
    controller.type('‹')


def right_single_angle_quote():
    controller.type('›')


def left_double_quote():
    controller.type('“')


def right_double_quote():
    controller.type('”')


def left_single_quote():
    controller.type('‘')


def right_single_quote():
    controller.type('’')


with keyboard.GlobalHotKeys({
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
}) as h:
    h.join()
