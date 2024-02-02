import os
import time
from PIL import Image
import pyautogui, pyscreenshot
from pynput import mouse
import logging

total_page = 0
left_x, left_y, right_x, right_y, click_x, click_y = 0, 0, 0, 0, 0, 0


def mouse_click():
    with mouse.Listener(
            on_click=on_click) as listener:
        listener.join()


def on_click(x, y, button, pressed):
    global left_x, left_y, right_x, right_y, click_x, click_y

    if left_x == 0 and pressed:
        left_x, left_y = x, y
    elif right_x == 0 and pressed:
        right_x, right_y = x, y
    else:
        click_x, click_y = x, y

    if not pressed:
        return False


print("스크린샷 찍을 책 왼쪽 위 클릭")
mouse_click()

print("스크린샷 찍을 책 오른쪽 아래 클릭")
mouse_click()

path = pyautogui.prompt('저장할 경로 입력')


width = right_x - left_x
height = right_y - left_y

current_page = 0
total_page = pyautogui.prompt('총 페이지 수 입력')

pyautogui.moveTo((right_x + left_x)/2., (right_y + left_y)/2.)
pyautogui.click()

while (current_page < int(total_page)):
    if pyautogui.press('esc'):
        break
    image = pyscreenshot.grab(bbox=(left_x, left_y, right_x, right_y))
    image.save(path + '/page_' + str(current_page).zfill(3) + '.png')
    pyautogui.press('right')
    current_page += 1
    pyautogui.sleep(0.25)
    logging.info("current = " + str(int(current_page * 100 / int(total_page))) + "%")



logger = logging.getLogger();

logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 참고: https://stackoverflow.com/questions/47308541/how-to-save-an-image-list-in-pdf-using-pil-pillow
file_list = os.listdir(path)

file_list.sort()

pdf_name = pyautogui.prompt('pdf 이름 입력')
time.sleep(1)

img_list = []

if '.DS_Store' in file_list:
  file_list.remove('.DS_Store')

img_path = path + '/' + file_list[0]
first_img = Image.open(img_path).convert("RGB")

count = 1

for img in file_list:
  if not img.endswith('png'):
    continue
  next_img = Image.open(path + '/' + img).convert("RGB")
  img_list.append(next_img)
  logger.info("current = " + str(int((count * 100 / len(file_list)))) + "%")
  count += 1

del img_list[0]

logger.info("pdf로 변환 중")
first_img.save(path + '/' + pdf_name + '.pdf',save_all=True, append_images=img_list)

is_file_delete = pyautogui.confirm('스크린샷 파일 삭제 할까요?', buttons=['Yes', 'No'])

img_path = path + '/' + file_list[0]

if 'Yes' in is_file_delete:
    for img in file_list:
        img_path = path + '/' + img
        os.remove(img_path)

