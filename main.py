import easyocr
from pynput import mouse
import pyscreenshot as ImageGrab

file_name = 'screen.png'
click_count = 0
x1 = 0
y1 = 0
x2 = 0
y2 = 0


def on_click(x, y, button, pressed):
    global x1, x2
    global y1, y2
    global click_count

    if not pressed:
        if click_count == 0:
            x1 = x
            y1 = y

        if click_count == 1:
            x2 = x
            y2 = y

        click_count += 1

        if click_count == 1:
            print('One more click! Just little more right please!')

        if click_count == 2:
            if x1 >= x2 or y1 >= y2:
                click_count = 0
                print('You need to click on two points of the screen! From LEFT to RIGHT please!')
            else:
                click_count = 0
                return False


def text_recognition(file_path: str):
    reader = easyocr.Reader(['ru', 'en'])
    result = reader.readtext(file_path, detail=0, paragraph=True)

    print('Screenshot has been recognize!')
    return result


def write_recognized_text(recognized_text):
    if len(recognized_text) > 0:
        with open('result.txt', 'w') as result_file:
            result_string = ' '.join(recognized_text)
            result_file.write(result_string)
        result_file.close()
        print('Success! Recognized text was wrote in the result text file!')
    else:
        print('Cannot recognize text!')


def create_screenshot(coordinates: tuple[int, int, int, int]):
    screen = ImageGrab.grab(bbox=coordinates)
    screen.save(file_name)
    print('Screenshot has been save!')


def initial_click_listener():
    print('Click on two points of the screen!')
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def main():
    initial_click_listener()
    create_screenshot((x1, y1, x2, y2))

    recognized_text = text_recognition(file_name)
    write_recognized_text(recognized_text)


if __name__ == '__main__':
    main()
