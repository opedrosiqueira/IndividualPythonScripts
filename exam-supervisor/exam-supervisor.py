'''
O que é cada uma dessas janelas? elas devem ser permitidas?

2023-10-30 18:52:26,243 [INFO] what is "Nova notificação" (None) (uiawrapper.UIAWrapper - 'Nova notificação', Dialog)? # ao chegar uma notificação
2023-10-30 20:54:54,625 [INFO] what is "Início" (None) (uiawrapper.UIAWrapper - 'Início', Dialog)?
2023-10-30 19:57:31,116 [INFO] what is "Iniciar" (None) (uiawrapper.UIAWrapper - 'Iniciar', Dialog)? # ao teclar ou clicar no menu iniciar
2023-10-30 19:55:33,842 [INFO] what is "Contexto" (None) (uia_controls.MenuWrapper - 'Contexto', Menu)? # ao escolher arquivo, quando abre a janela de seleção de arquivo, se der clique direito em algum arquivo

ideia: inserir senha para limpar o workspace e desligar pc
'''

from pathlib import Path
import sys
import time
import logging
import os
from pywinauto import Desktop
from pywinauto.application import Application, AppStartError
import tkinter as tk
from tkinter import simpledialog


def allowed_window(w):
    return (
        f"prova - Visual Studio Code" in w.window_text()
        or "Mudar papel para... - Google Chrome (Modo anônimo)" == w.window_text()
        or "ead" in w.window_text().lower()
        or "60537" in w.window_text()
        or "Mudar papel para..." in w.window_text()
        or "Barra de Tarefas" == w.window_text()
        # to-do depois remover program manager e gerenciador de tarefas da lista de janelas permitidas
        or "Program Manager" == w.window_text()
        or "Visão de Tarefas" == w.window_text()
        or "Gerenciador de Tarefas" == w.window_text()
        or "alternador de tarefas" == w.window_text().lower()
        or "alternância de tarefas" == w.window_text().lower()
        or "" == w.window_text()
        or "Drag" == w.window_text()
        or "Assistente de Ajuste" == w.window_text()        
    )


def start():
    global os
    production = True if "production" in sys.argv else False
    folder = os.path.expanduser(
        sys.argv[sys.argv.index("folder") + 1]
        if "folder" in sys.argv
        else "~/Desktop/prova"
    )
    url = (
        sys.argv[sys.argv.index("url") + 1]
        if "url" in sys.argv
        else "https://ead.ifms.edu.br/course/view.php?id=34005"
    )

    path = os.path.expanduser("~")

    # to-do salvar log no arquivo em vez de apenas imprimi-lo
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{path}/log.log"), logging.StreamHandler()],
    )

    windows = Desktop(backend="uia").windows()

    logging.info("closing all windows...")
    for w in windows:
        # if not f"Visual Studio Code" in w.window_text():
        logging.info("closing %s", w.window_text())
        w.close()

    logging.info("opening %s on vscode...", folder)
    code = Application(backend="uia").start(
        f"C:/VSCode-win32-x64-1.83.1/Code.exe {folder}"
    )

    logging.info("opening %s on chrome...", url)
    try:
        chrome = Application(backend="uia").start(
            # f'"C:/Program Files/Google/Chrome/Application/chrome.exe" --host-resolver-rules --ignore-certificate-errors --ignore-ssl-errors --incognito --new-window {url}'
            f'"C:/Program Files/Google/Chrome/Application/chrome.exe" --incognito --new-window {url}'
        )
    except AppStartError:
        chrome = Application(backend="uia").start(
            f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" --incognito --new-window {url}'
        )

    time.sleep(1)

    suspect = False
    logging.info("starting supervision...")
    janelas = set()
    logging.info("janelas abertas permitidas:")
    while not suspect:
        windows = Desktop(backend="uia").windows()
        time.sleep(1)
        for w in windows:
            if not allowed_window(w):
                logging.info(
                    'what is "%s" (%s) (%s)?', w.window_text(), w.friendlyclassname, w
                )
                logging.info("closing...")
                suspect = True
                break
            if str(w) not in janelas:
                janelas.add(str(w))
                logging.info(w)

    logging.info("end")
    logging.shutdown()

    if suspect and production:
        import os

        os.system("shutdown /p /f")


def enter(event):
    p = password.get()  # get password from entry
    if p == "c0nt1nu4r":
        master.destroy()
    elif p == "s41r":
        master.destroy()


def disable_event():
    pass


if __name__ == "__main__":
    continuar = True
    while continuar:
        try:
            start()
        finally:
            master = tk.Tk()
            master.wm_attributes("-topmost", True)
            master.attributes('-fullscreen', True)
            master.title("Por favor, chame o professor")
            master.overrideredirect(True)
            master.protocol("WM_DELETE_WINDOW", disable_event)

            tk.Label(
                master, text="Por favor, chame o professor", font=("Arial", 35)
            ).pack()

            password = tk.StringVar()  # Password variable

            entry = tk.Entry(master, textvariable=password, show="*")
            entry.pack()
            entry.bind("<Return>", enter)

            master.mainloop()

            if password.get() == "s41r":
                continuar = False



'''
# get windows titles on linux

import subprocess
import re


result = subprocess.run(["xprop", "-root", "_NET_CLIENT_LIST"], stdout=subprocess.PIPE).stdout.decode()
windows_ids = re.split("# |, ", result.strip())[1:]
windows_titles = []
for w in windows_ids:
    window_title = subprocess.run(["xprop", "-id", w, "_NET_WM_NAME"], stdout=subprocess.PIPE).stdout.decode()
    first_occurrence = window_title.find('"') + 1
    last_occurrence = window_title.rfind('"')
    windows_titles.append(window_title[first_occurrence:last_occurrence])
'''