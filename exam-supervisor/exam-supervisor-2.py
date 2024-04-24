"""
ideias:
- inserir senha para limpar o workspace e desligar pc
- enviar log para o servidor em vez de apenas imprimi-lo
"""

from dataclasses import make_dataclass
import logging
import os
import subprocess
import sys
import time
import tkinter as tk


Window = make_dataclass("Window", ("title", "id"))


def get_windows_ids():
    result = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "."], stdout=subprocess.PIPE).stdout.decode()
    return result.strip().split("\n")


def get_windows():
    windows_ids = get_windows_ids()
    windows = []
    for window_id in windows_ids:
        window_title = subprocess.run(["xdotool", "getwindowname", window_id], stdout=subprocess.PIPE).stdout.decode().strip()
        windows.append(Window(window_title, window_id))
    return windows


def close_window(id):
    subprocess.run(["xdotool", "windowclose", id], stdout=subprocess.PIPE)


def allowed_window(w):
    return (
        "mutter guard window" == w
        or "cinnamon" == w
        or "Desktop" == w
        or "Firefox" == w
        or "Mozilla Firefox Private Browsing" == w
        or "prova - Visual Studio Code" in w
        or "EAD IFMS: Acesso ao site" in w
        or "Mudar papel para..." in w
        or "2024-1 FLP" in w
    )


def start():
    production = True if "production" in sys.argv else False
    folder = os.path.expanduser(sys.argv[sys.argv.index("folder") + 1] if "folder" in sys.argv else "~/Desktop/prova")
    url = sys.argv[sys.argv.index("url") + 1] if "url" in sys.argv else "https://ead.ifms.edu.br/mod/assign/view.php?id=951420"

    path = os.path.expanduser("~")

    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(f"{path}/log.log"), logging.StreamHandler()],
    )

    windows = get_windows()

    logging.info("closing all windows...")
    for w in windows:
        if production or not allowed_window(w.title) and "Visual Studio Code" not in w.title:
            logging.info("closing %s", w.title)
            close_window(w.id)

    logging.info("opening %s on vscode...", folder)
    subprocess.Popen(["code", folder], stdout=subprocess.PIPE)

    logging.info("opening %s on firefox...", url)
    subprocess.Popen(["firefox", "-private-window", url], stdout=subprocess.PIPE)

    suspect = False
    logging.info("starting supervision...")
    janelas = set()
    logging.info("janelas abertas permitidas:")
    while not suspect:
        windows = get_windows()
        time.sleep(1)
        for w in windows:
            if not allowed_window(w.title):
                logging.info('what is "%s" (%s)?', w.title, w.id)
                logging.info("closing...")
                suspect = True
                break
            if w.title not in janelas:
                janelas.add(w.title)
                logging.info(w.title)

    logging.info("end")
    logging.shutdown()

    # if suspect and production:
    #     os.system("shutdown /p /f")


def enter(event):
    p = password.get()  # get password from entry
    if p == "0194":  # sair
        root.destroy()
    elif p == "5417":  # continuar
        root.destroy()


def disable_event():
    pass


if __name__ == "__main__":
    continuar = True
    while continuar:
        try:
            start()
        finally:
            root = tk.Tk()
            # root.overrideredirect(True) # Hide the title bar and borders
            root.attributes("-fullscreen", True)  # Adjust the window to fill the entire screen
            root.wm_attributes("-topmost", True)  # Make the window always on top

            root.title("Por favor, chame o professor")
            root.protocol("WM_DELETE_WINDOW", disable_event)

            tk.Label(root, text="Por favor, chame o professor", font=("Arial", 35)).pack()

            password = tk.StringVar()  # Password variable

            entry = tk.Entry(root, textvariable=password, show="*")
            entry.pack()
            entry.bind("<Return>", enter)

            root.mainloop()

            if password.get() == "5417":
                continuar = False
