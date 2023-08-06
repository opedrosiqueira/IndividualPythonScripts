"""
sincroniza as tags artist e title das músicas com os nomes dos arquivos ou pastas que os contêm.
"""

import glob
import re
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
from pathlib import Path


def createTagsIfNotExist(song, tag):
    try:
        tagvalue = song[tag]
    except KeyError:
        song[tag] = ''


def main():
    path = str(Path.home()) + "/Mega/Music"
    tmp = input("Deixe em branco para procurar em " + path + "\nProcurar em: ")
    if tmp:
        path = tmp
    path += "/**/*"  # **: procura recursivamente em diretórios. *: qualquer arquivo no diretório atual

    for file in glob.iglob(path, recursive=True):
        info = EasyMP4(file) if file.endswith(".m4a") else EasyID3(file) if file.endswith(".mp3") else None
        if not info:
            continue

        folder = Path(file)

        title = folder.name[:-4]  # só o nome do arquivo
        if title.rfind(" - ") > -1:  # só a parte depois do traço
            title = title[title.rfind(" - ")+3:]  # +3 pois quero o que vem depois de " - ", que possui 3 chars
        if title[0].isdigit():  # só o que vem depois do número
            title = re.sub(r"(.*?)([^\W\d].*)", r"\2", title)  # remove o número inicial (tem que usar lazy regex (.*?)) # ^\W\d https://stackoverflow.com/a/1673804/4072641

        artist = [folder.name[0:folder.name.rfind(" - ")], folder.parents[0].name, folder.parents[1].name]

        createTagsIfNotExist(info, 'title')
        createTagsIfNotExist(info, 'artist')
        createTagsIfNotExist(info, 'album')

        tituloDiferente = True if info['title'][0] != title else False
        artistaDiferente = True if info['artist'][0] not in artist[0] and artist[1] not in info['artist'][0] and artist[2] not in info['artist'][0] else False

        if tituloDiferente or artistaDiferente:
            print("\n" + folder.name)
            print('álbum: ' + str(info['album'])) if 'album' in info else ""

            if tituloDiferente:
                asw = input("substituir título " + str(info['title']) + " por: (1) \"" + title + "\" (2) Outra coisa (0) Nada? ")
                if asw == "1":
                    editID3Tag(info, 'title', title)
                elif asw == "2":
                    editID3Tag(info, 'title', input("informe um novo título: "))

            if artistaDiferente:
                asw = input("substituir artista " + str(info['artist']) + " por: (1)\"" + folder.parents[0].name + "\" (2) \""+folder.parents[1].name+"\" (3) \""+folder.name[0:folder.name.rfind(" - ")]+"\" (4) Outra coisa (0) Nada? ")
                if asw == "1":
                    editID3Tag(info, 'artist', folder.parents[0].name)
                elif asw == "2":
                    editID3Tag(info, 'artist', folder.parents[1].name)
                elif asw == "3":
                    editID3Tag(info, 'artist', folder.name[0:folder.name.rfind(" - ")])
                elif asw == "4":
                    editID3Tag(info, 'artist', input("informe um novo artista: "))


def editID3Tag(song, tag, value):
    song[tag] = value
    song.save()
    print("substituído!")


def tmp():
    for file in glob.iglob("/home/pedro/Mega/Music/**/*.m4a", recursive=False):
        info = EasyMP4(file)
        folder = Path(file)
        if info['artist'][0] != folder.parents[0].name:
            if info['artist'][0] != folder.parents[1].name:
                if not folder.name.startswith(info['artist'][0]):
                    print(info['artist'][0] + "\t" + file)

        # +3 pois ' - ' possui 3 chars, e quero o que vem depois disso
        title = file[file.rfind(" - ")+3:-4]
        if title.startswith("ome/pedro"):
            title = folder.name[:-4]

        if not info['title'][0] in folder.name:
            print("\n" + folder.name)
            print('artist: ' + str(info['artist'])) if 'artist' in info else ""
            print(' album: ' + str(info['album'])) if 'album' in info else ""
            print(' title: ' + str(info['title'])) if 'title' in info else ""
            asw = input("substituir título por: \"" + title + "\"? ")
            if asw.lower() == "s":
                info['title'][0] = title
                info.save()
                print("substituído!")
            elif asw.lower() == 'q':
                break


if __name__ == "__main__":
    main()
