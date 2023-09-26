from pathlib import Path
import sys
import time
import logging
import os
from pywinauto import Desktop
from pywinauto.application import Application, AppStartError


def allowed_window(w):
    global folder
    return (
        f"{folder} - Visual Studio Code" in w.window_text()
        or "Sem título - Google Chrome (Modo anônimo)" in w.window_text()
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
        or ("" == w.window_text() and "Pane" == w.friendlyclassname)
        or ("" == w.window_text() and "Dialog" == w.friendlyclassname)
        or ("" == w.window_text() and "None" == w.friendlyclassname)
        or "" == w.window_text()
    )


production = True if "production" in sys.argv else False
folder = os.path.expanduser(
    sys.argv[sys.argv.index("folder") + 1]
    if "folder" in sys.argv
    else "~/Desktop/prova"
)
url = sys.argv[sys.argv.index("url") + 1] if "url" in sys.argv else "ead.ifms.edu.br"

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
    logging.info("closing %s", w.window_text())
    w.close()

logging.info("creating/opening %s on vscode...", folder)
Path(folder).mkdir(parents=True, exist_ok=True)
code = Application(backend="uia").start(f"C:/VSCode-win32-x64-1.82.2/Code.exe {folder}")

logging.info("opening %s on chrome...", url)
try:
    chrome = Application(backend="uia").start(
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
