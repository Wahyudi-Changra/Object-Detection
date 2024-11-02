from PIL import Image
import os

source_folder = 'thrasholds/'
destination_folder = 'thrasholds/'

directory = os.listdir(source_folder)
print(directory)

for item in directory:
    img = Image.open(source_folder + item)
    width, height = img.size
    ratio = width / height
    new_width = 640
    new_height = int(new_width / ratio)
    imgResize = img.resize((new_width, new_height), Image.LANCZOS)
    imgResize.save(destination_folder + item[:-4] + '.jpg', quality=100)
