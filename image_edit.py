from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
from statistics import mean
import time



def image_downsampling(image, format):
   img = Image.open(image)
   width = img.size[0]
   height = img.size[1]
   new_width = width // format
   new_height = height // format
   small_image = Image.new(img.mode, (new_width, new_height))

   for i in range(width - format + 1):
      for j in range(height - format + 1):
         if ((i % format == 0) and (j % format == 0)):
            small_image.putpixel((i // format, j // format), img.getpixel((i, j)))
   small_image.show()

def image_grey_shades(image):
   img = Image.open(image)
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

def image_upsampling(image, format):
   img = Image.open(image)
   width = img.size[0]
   height = img.size[1]
   new_width = width * format
   new_height = height * format
   bigger_img = Image.new(img.mode, (new_width, new_height))

   for i in range(new_width - format + 1):
      for j in range(new_height - format + 1):
         if ((i % format == 0) and (j % format == 0)):
            bigger_img.putpixel((i, j), img.getpixel((i // format, j // format)))
         else:
            x1 = (i - 1) // format
            x2 = (i - 1) // format + 1
            y1 = (j - 1) // format
            y2 = (j - 1) // format + 1
            f11 = np.array(img.getpixel((x1, y1)))
            f22 = np.array(img.getpixel((x2, y2)))
            f12 = np.array(img.getpixel((x1, y2)))
            f21 = np.array(img.getpixel((x2, y1)))
            fn = (1 / ((x2 - x1) * (y2 - y1))) * (f11 * (x2 - i / format) * (y2 - j / format) + f21 * (i / format - x1) * (y2 - j / format) + f12 * (x2 - i / format) * (j / format - y1) + f22 * (i / format - x1) * (j / format - y1))
            f = list()
            for q in fn:
               f.append(int(round(q, 0)))
            bigger_img.putpixel((i, j), tuple(f))

   bigger_img.show()

def image_1_prohod(image, m, n):
   img = Image.open(image)
   width = img.size[0]
   height = img.size[1]
   new_width = int(width * m / n - 1)
   new_height = int(height * m / n - 1)

   new_image = Image.new(img.mode, (new_width, new_height))
   for x in range(new_width):
      for y in range(new_height):
         new_image.putpixel((x, y), img.getpixel((x * n / m, y * n / m)))
   new_image.show()

def image_2_prohod(image, m, n):
   img = Image.open(image)
   width = img.size[0]
   height = img.size[1]
   new_width = int(width * m - 1)
   new_height = int(height * m - 1)

   new_image = Image.new(img.mode, (new_width, new_height))
   for x in range(new_width):
      for y in range(new_height):
         new_image.putpixel((x, y), img.getpixel((x / m, y / m)))

   new_width_2 = int(new_width / n - 1)
   new_height_2 = int(new_height / n - 1)
   new_image_2 = Image.new(new_image.mode, (new_width_2, new_height_2))

   for x in range(new_width_2):
      for y in range(new_height_2):
         new_image_2.putpixel((x, y), new_image.getpixel((x * n, y * n)))
   new_image_2.show()


def create_hist(image):
   img = image
   width = img.size[0]
   height = img.size[1]
   pix = list()
   for i in range(width):
      for j in range(height):
         pixel = img.getpixel((i, j))
         pix.append(pixel)
   hist = plt.hist(pix, range(0, max(pix) + 1))[0]
   return hist

def create_hist(img, start_tuple, end_tuple):
   pix = list()
   for i in range(start_tuple[0], end_tuple[0]):
      for j in range(start_tuple[1], end_tuple[1]):
         pix.append(img.getpixel((i, j)))
   hist = plt.hist(pix, range(0, max(pix) + 1))
   return hist


'''def otsu_threshold(histogram):
   t_max = 0
   var_max = 0
   pixels_sum = sum(histogram)
   hist_length = len(histogram)

   for i in range(hist_length - 1):
      w1 = sum(histogram[0 : i + 1]) / pixels_sum
      w2 = sum(histogram[i + 1 : hist_length]) / pixels_sum
      a1 = mean(histogram[0 : i + 1])
      a2 = mean(histogram[i + 1 : hist_length])
      var = w1 * w2 * (a1 - a2) ** 2

      if var > var_max:
         var_max = var
         t_max = i

   return t_max'''

def otsu_threshold(histogram):
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

   return t_max



def eyquill_method(img, epsilon):
   result_img = img.copy()
   start_time = time.time()
   for x in range(7, img.width - 7, 3):
         for y in range(7, img.height - 7, 3):
            big_window_hist_for_threshold = create_hist(img, (x - 7, y - 7), (x + 8, y + 8))
            t = otsu_threshold(big_window_hist_for_threshold)
            big_window_hist = big_window_hist_for_threshold[0]
            big_window_hist_len = len(big_window_hist)
            big_window_mean = mean(big_window_hist)
            mean_left = mean(big_window_hist[0: t + 1])
            mean_right = mean(big_window_hist[t + 1: big_window_hist_len])

            if abs(mean_right - mean_left) > epsilon:
               for i in range(x - 2, x + 1):
                  for j in range(y - 2, y + 1):
                     if result_img.getpixel((i, j)) < t:
                        result_img.putpixel((i, j), 0)
                     else:
                        result_img.putpixel((i, j), 255)
            else:
               for i in range(x - 2, x + 1):
                  for j in range(y - 2, y + 1):
                     if big_window_mean > 127:
                        result_img.putpixel((i, j), 255)
                     else:
                        result_img.putpixel((i, j), 0)
   print(time.time() - start_time)
   return result_img






#image_downsampling('spiderman_2.jpg', 3)
#image_grey_shades('pict.jpg')
#image_upsampling('spiderman_2.jpg', 2)
#image_1_prohod('pict.jpg', 1, 1)p
#image_2_prohod('spiderman_2.jpg', 7, 2)
#print(otsu_threshold(create_hist('spiderman_2.jpg')))
#create_hist('spiderman_2.jpg')
#img_color =  Image.open('smile.png').convert('RGB')
img_color =  Image.open('lednikoviy.jpeg').convert('RGB')
img_grey = image_grey_shades_for_threshold(img_color)
print(otsu_threshold(create_hist('spiderman_2.jpg')))
#eyquill_method(img_grey, 0.15).show()



