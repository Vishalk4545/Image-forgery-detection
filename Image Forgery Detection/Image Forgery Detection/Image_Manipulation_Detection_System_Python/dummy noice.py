import sys
import cv2
from ForgeryDetection import Detect
import re
from datetime import datetime
import os.path as path
# from exif import Image

from PIL import Image, ExifTags


import copy_move_cfa


from optparse import OptionParser

# copy-move parameters
cmd = OptionParser("usage: %prog image_file [options]")
cmd.add_option('', '--imauto',
               help='Automatically search identical regions. (default: %default)', default=1)
cmd.add_option('', '--imblev',
               help='Blur level for degrading image details. (default: %default)', default=8)
cmd.add_option('', '--impalred',
               help='Image palette reduction factor. (default: %default)', default=15)
cmd.add_option(
    '', '--rgsim', help='Region similarity threshold. (default: %default)', default=5)
cmd.add_option(
    '', '--rgsize', help='Region size threshold. (default: %default)', default=1.5)
cmd.add_option(
    '', '--blsim', help='Block similarity threshold. (default: %default)', default=200)
cmd.add_option('', '--blcoldev',
               help='Block color deviation threshold. (default: %default)', default=0.2)
cmd.add_option(
    '', '--blint', help='Block intersection threshold. (default: %default)', default=0.2)
opt, args = cmd.parse_args()
if not args:
    cmd.print_help()
    sys.exit()


def PrintBoundary():
    for i in range(50):
        print('*', end='')
    print()


file_name = sys.argv[1]
input = './/input//' + file_name
if not path.exists(input):
    sys.exit(
        "Image not found: {}. Please place the image in the images subdirectory.".format(file_name))



















# Copy-Move detection Start

eps = 60
min_samples = 2

PrintBoundary()
print('Use \'q\' for exit and\n\'s/S\' for saving the Forgery Detected.')
PrintBoundary()
flag = True

try:
    value = sys.argv[2]

except IndexError:
    flag = False
if flag:
    try:
        value = int(value)
        if(value < 0 or value > 500):
            print('Value not in range (0,500)........ using default value.')
        else:
            eps = value
    except ValueError:
        print('Value not integer........ using default value.')

flag2 = True
try:
    value = sys.argv[3]
except IndexError:
    flag2 = False

if flag2:
    try:
        value = int(value)
        if(value < 0 or value > 50):
            print('Value not in range (0,50)........ using default value.')
        else:
            min_samples = value
    except ValueError:
        print('Value not integer........ using default value.')

PrintBoundary()
print('Detecting Copy-Move Forgery with parameter value as\neps:{}\nmin_samples:{}'.format(
    eps, min_samples))
PrintBoundary()

detect = Detect(input)

key_points, descriptors = detect.siftDetector()

forgery = detect.locateForgery(eps, min_samples)
if forgery is None:
    sys.exit(0)
cv2.imshow('Original image', detect.image)
cv2.imshow('Forgery', forgery)
wait_time = 1000
while(cv2.getWindowProperty('Forgery', 0) >= 0) or (cv2.getWindowProperty('Original image', 0) >= 0):
    keyCode = cv2.waitKey(wait_time)
    if (keyCode) == ord('q') or keyCode == ord('Q'):
        cv2.destroyAllWindows()
        break
    elif keyCode == ord('s') or keyCode == ord('S'):
        name = re.findall(r'(.+?)(\.[^.]*$|$)', file_name)
        date = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        new_file_name = name[0][0]+'_'+str(eps)+'_'+str(min_samples)
        new_file_name = new_file_name+'_'+date+name[0][1]
        PrintBoundary()

        vaue = cv2.imwrite(new_file_name, forgery)
        print('Image Saved as....', new_file_name)

cv2.destroyAllWindows()
# Copy-Move detection End



