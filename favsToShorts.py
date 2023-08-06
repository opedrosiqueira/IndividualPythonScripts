# cria um atalho na pasta documentos para cada favorito da lista de favoritos do nemo

import subprocess
import os
import ast
from urllib.parse import unquote

# para cada arquivo marcado como favorito no linux mint cria um atalho em Documents

files = ast.literal_eval(
    subprocess.run(['gsettings', 'get', 'org.x.apps.favorites', 'list'], stdout=subprocess.PIPE)
    .stdout.decode('utf-8'))

for file in files:
    if file.startswith("file:///"):
        file = unquote(file[7:file.rfind("::")])
        link = os.path.expanduser("~/Documents") + file[file.rfind("/"):]
        if os.path.exists(link):
            print("already exists", file)
        else:
            print(file, link)
            subprocess.run(['ln', '-s', file, link], stdout=subprocess.PIPE)
