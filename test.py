from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
from statistics import mean
from statistics import variance
import time

def image_grey_shades_for_threshold(img):
   width = img.size[0]
   height = img.size[1]
   grey_img = Image.new('L', (width, height))

   for i in range(width):
      for j in range(height):
         pixel = img.getpixel((i, j))
         sr = 0
         for color in pixel:
            sr += color // 3
            grey_img.putpixel((i, j), (sr))
   return grey_img

def create_hist(image):
   img = Image.open(image)
   img_grey = image_grey_shades_for_threshold(img)
   width = img_grey.size[0]
   height = img_grey.size[1]
   pix = list()
   for i in range(width):
      for j in range(height):
         pixel = img_grey.getpixel((i, j))
         pix.append(pixel)
   hist = plt.hist(pix, range(0, max(pix) + 1))
   return hist

def otsu_threshold(histogram):
   start_time = time.time()
   t_max = 0
   var_max = 0
   pixels_sum = sum(histogram[0])
   hist = histogram[0]
   base = histogram[1]
   hist_length = len(hist)


   for i in range(hist_length - 1):
      w1 = np.sum(np.array(hist[0: i + 1]) / pixels_sum)
      w2 = np.sum(np.array(hist[i + 1: hist_length]) / pixels_sum)
      a1 = np.sum(np.array(hist[0: i + 1]) * np.array(base[0: i + 1])/ (pixels_sum * w1))
      a2 = np.sum(np.array(hist[i + 1: hist_length]) * np.array(base[i + 1: hist_length]) / (pixels_sum * w2))
      var = w1 * w2 * (a1 - a2) ** 2

      if var > var_max:
         var_max = var
         t_max = i

   print(time.time() - start_time)
   return t_max

create_hist('black_white.jpg')
print(otsu_threshold(create_hist('V-rukah-monaha.jpg')))