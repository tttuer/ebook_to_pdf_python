from PIL import Image
import os

# 참고: https://stackoverflow.com/questions/47308541/how-to-save-an-image-list-in-pdf-using-pil-pillow
path = input("폴더 경로를 입력하세요\n")
file_list = os.listdir(path)

file_list.sort()

pdf_name = input("pdf 이름을 입력하세요\n")

img_list = []

img_path = path + '/' + file_list[0]
first_img = Image.open(img_path).convert("RGB")

for img in file_list:
  if not img.endswith('png'):
    continue
  next_img = Image.open(path + '/' + img).convert("RGB")
  img_list.append(next_img)
  print('current = ' + img)

del img_list[0]

first_img.save(path + '/' + pdf_name + '.pdf',save_all=True, append_images=img_list)