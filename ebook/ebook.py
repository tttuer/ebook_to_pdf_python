import pyautogui, pyscreenshot
from pynput import mouse, keyboard

total_page = 0
left_x, left_y, right_x, right_y, click_x, click_y = 0, 0, 0, 0, 0, 0

def mouse_click():
  with mouse.Listener(
      on_click=on_click) as listener:
    listener.join()

def on_click(x, y, button, pressed):
  global left_x, left_y, right_x, right_y, click_x, click_y

  if left_x == 0 and pressed:
    print('now')
    left_x, left_y = x, y
  elif right_x == 0 and pressed:
    print('here')
    right_x, right_y = x, y
  else:
    click_x, click_y = x, y

  print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
  if not pressed:
    return False

print("스크린샷 찍을 책 왼쪽 위 클릭")
mouse_click()

print("스크린샷 찍을 책 오른쪽 아래 클릭")
mouse_click()

print("다음 페이지 버튼 위치")
mouse_click()

path = input('input path\n')

print(left_x, left_y, right_x, right_y, click_x, click_y)
print(path)

width = right_x - left_x
height = right_y - left_y

current_page = 0
total_page = input('input total pages\n')

while(current_page < int(total_page)):
  if pyautogui.press('k'):
    break
  image = pyscreenshot.grab(bbox=(left_x, left_y, right_x, right_y))
  image.save(path + '/page_' + str(current_page).zfill(3) + '.png')
  pyautogui.click(click_x, click_y)
  current_page += 1
  pyautogui.sleep(0.2)
