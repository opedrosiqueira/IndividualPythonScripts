from PIL import Image
from PIL.ExifTags import TAGS

file_path = '/home/siqueira/Mega/Pictures/2020/IMG-20200105-WA0003.jpg'

# open the image
image = Image.open(file_path)
try:
    # extracting the exif metadata
    exifdata = image._getexif()
    print(f"{'Name':25}: {file_path[file_path.rfind('/')+1:]}")
    # looping through all the tags present in exifdata
    for tag, value in exifdata.items():
        # getting the tag name instead of tag id
        tagname = TAGS.get(tag, tag)
        # printing the final result
        print(f"{tagname:25}: {value}")
except AttributeError:
    print(f"{'Exif Data':25}: Not available")
