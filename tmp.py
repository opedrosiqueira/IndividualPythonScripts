import os
from pathlib import PureWindowsPath


def convert(path):
    return PureWindowsPath(os.path.abspath(PureWindowsPath(path).as_posix())).as_posix()

print('Windows path: ' + convert(r'.\tmp.html'))
print('Posix path: ' + convert('tmp.html'))

print(os.name)
print(os.environ['tmp'])