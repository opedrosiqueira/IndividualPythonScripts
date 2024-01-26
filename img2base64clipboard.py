import io
import base64
from PIL import ImageGrab
import pyperclip
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def get_image_from_clipboard():
    if sys.platform.startswith("linux"):
        try:
            cmd = ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"]
            image_data = subprocess.check_output(cmd)
            return image_data
        except subprocess.CalledProcessError:
            raise RuntimeError("Something went wrong while retrieving image data!")
    else:
        img = ImageGrab.grabclipboard()
        if img:
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                return output.getvalue()
        else:
            raise RuntimeError("No image found on clipboard!")


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--figure", help="image inside figure with figcaption", action="store_true")
parser.add_argument("-s", "--svg", help="svg from javascript", action="store_true")
args = parser.parse_args()

props = ""
img = ""

id = input("img id: ")
if not id:
    raise argparse.ArgumentTypeError("ID is required!")
elem = 'id="' + id + '"'

alt = input("img alt: ")
if alt:
    elem += ' alt="' + alt + '"'

if args.svg:
    img_data = Path(tempfile.gettempdir() + "/tmp.svg").read_text(encoding="utf8")  # fica na pasta temporária, o nome do arquivo deve ser tmp.svg
    img_data = img_data[img_data.find("<svg") :]  # pega de onde começa o svg
    img_data = img_data.replace("\n", "")  # retira todas as quebras de linha
    img_data = img_data.replace('"', '\\"') # svg pode ter aspas dentro, aí preciso normalizar
    props = elem
    js = f'document.getElementById("{id}").innerHTML = "{img_data}"\n'
else:
    img_data = get_image_from_clipboard()
    img_data = base64.b64encode(img_data).decode("utf-8")
    img_data = "data:image/png;base64," + img_data
    img = "<img " + elem + ">"
    js = f'document.getElementById("{id}").src = "{img_data}"\n'

if args.figure:
    cap = input("fig caption: ")
    js += f"<p>\n<figure {props}>{img}\n<figcaption>{cap}</figcaption></figure>\n</p>\n"
else:
    js += f"<p {props}>{img}</p>\n"

pyperclip.copy(js)
print("Image copied to clipboard!")
