import sys
import time
import logging
import os
from pywinauto import Desktop
from pywinauto.application import Application, AppStartError


def allowed_window(w):
    return (
        "Visual Studio Code" in w.window_text()
        or "ead" in w.window_text().lower()
        or "60537" in w.window_text()
        or "Mudar papel para..." in w.window_text()
        or "Barra de Tarefas" == w.window_text()
        # to-do depois remover program manager e gerenciador de tarefas da lista de janelas permitidas
        or "Program Manager" == w.window_text()
        or "Gerenciador de Tarefas" == w.window_text()
        or "alternador de tarefas" == w.window_text().lower()
        or "alternância de tarefas" == w.window_text().lower()
        or ("" == w.window_text() and "Pane" == w.friendlyclassname)
        or ("" == w.window_text() and "Dialog" == w.friendlyclassname)
        or ("" == w.window_text() and "None" == w.friendlyclassname)
        or "" == w.window_text()
    )


path = os.path.expanduser("~")

# to-do salvar log no arquivo em vez de apenas imprimi-lo
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(filename=f"{path}/log.log", encoding="utf-8", level=logging.DEBUG)

windows = Desktop(backend="uia").windows()

logging.info("closing undesired windows...")
for w in windows:
    if "Visual Studio Code" in w.window_text():
        code = w
    if not allowed_window(w):
        logging.info(w.window_text())
        w.close()

logging.info("opening vscode and ead.ifms...")
if not code:
    code = Application(backend="uia").start(
        "C:/portables/VSCode-win32-x64-1.82.2/Code.exe"
    )

try:
    chrome = Application(backend="uia").start(
        '"C:/Program Files/Google/Chrome/Application/chrome.exe" --incognito --new-window ead.ifms.edu.br'
    )
except AppStartError:
    chrome = Application(backend="uia").start(
        '"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" --incognito --new-window ead.ifms.edu.br'
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
            logging.info("shutting down...")
            suspect = True
            break
        if str(w) not in janelas:
            janelas.add(str(w))
            logging.info(w)

logging.info("end")
