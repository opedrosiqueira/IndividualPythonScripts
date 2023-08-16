import io
import base64
from PIL import ImageGrab
import pyperclip
import argparse
import subprocess
import sys


def get_image_from_clipboard():
    if sys.platform.startswith('linux'):
        try:
            cmd = ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o']
            image_data = subprocess.check_output(cmd)
            return image_data
        except subprocess.CalledProcessError:
            raise RuntimeError("Something went wrong while retrieving image data!")
    else:
        img = ImageGrab.grabclipboard()
        if img:
            with io.BytesIO() as output:
                img.save(output, format='PNG')
                return output.getvalue()
        else:
            raise RuntimeError("No image found on clipboard!")


parser = argparse.ArgumentParser()
parser.add_argument("-f", '--figure', help="image inside figure with figcaption", action='store_true')
parser.add_argument("-j", '--javascript', help="image src from javascript", action='store_true')
args = parser.parse_args()

img_data = get_image_from_clipboard()
img_base64 = base64.b64encode(img_data).decode('utf-8')

id = input('img id: ')
if id:
    id = "id='" + id + "'"

alt = input('img alt: ')
if alt:
    alt = "alt='" + alt + "'"


if args.javascript:
    if not id:
        raise argparse.ArgumentTypeError("ID is required for javascript option!")
    tag = f"document.getElementById({id[3:]}).src = 'data:image/png;base64,{img_base64}'\n"
    src = ''
else:
    tag = ''
    src = f"src='data:image/png;base64,{img_base64}'"

if args.figure:
    cap = input('fig caption: ')
    tag += f"<p>\n<figure><img {id} {alt} {src}>\n<figcaption>{cap}</figcaption></figure>\n</p>\n"
else:
    tag += f"<p>\n<img {id} {alt} {src}>\n</p>\n"

pyperclip.copy(tag)
print("Image base64 copied to clipboard!")
