from graphlib import TopologicalSorter
from logging import NullHandler
import re
import cv2
import keyboard
import numpy as np
import pytesseract

DEVICE_ID = 2 #仮想カメラのID

# パラメータ設定
DEATH_FRAME_NUM = 8  # 马里奥死亡时出现的黑色画面连续帧数
THRESHOLD = 20  # 被视为黑色的像素值阈值
BLACK_RATIO = 0.99  # 屏幕应该判断黑色百分比 (BLACK_RATIO*100 %以上が黒)

WIDTH = 1920 #switchの解像度
HEIGHT = 1080

input_source = cv2.VideoCapture(DEVICE_ID) #映像の取得

input_source.set(cv2.CAP_PROP_FPS, 1)  #画面設定
input_source.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
input_source.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT) 



def main():
    blackFrameCout = 0
    while True:
        if keyboard.is_pressed('q'):
            break
        else:
            frame = get_frame()
            if is_black_screen(frame):
                blackFrameCout += 1
                print(blackFrameCout)
            else:
                if blackFrameCout >= DEATH_FRAME_NUM and blackFrameCout <= DEATH_FRAME_NUM + 3: #死亡判定(DEATH_FRAME_NUM如果检测到连续黑屏帧)
                    prev_death_count = read_death_count() #总死亡次数增加
                    write_death_count(prev_death_count) #总死亡次数写入
                    print("death")
                blackFrameCout = 0
            level_id = read_level_id(frame)
            if level_id != "" and level_id != None:
                print(level_id)
            else:
                continue


def get_frame(): #画像の取得
    if not input_source.isOpened():
        print("failed to open camera")
        exit()

    ret, frame_origin = input_source.read()
    if not ret:
        print("failed to get frame")
        exit()

    cv2.imshow("input_source", frame_origin)
    cv2.waitKey(1)
    return frame_origin



def is_black_screen(frame): #判断画面是否为黑色
    # 将框架转换为灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 计算黑色像素的百分比
    black_pixels = np.sum(gray < THRESHOLD)
    total_pixels = gray.size
    black_ratio = black_pixels / total_pixels

    if black_ratio > BLACK_RATIO:
        return True
    else:
        return False

def read_death_count():
    try:
        with open("death_count.txt", "r") as file:
            death_count = int(file.read())
    except FileNotFoundError:
        death_count = 0
    return death_count


def write_death_count(prev_death_count):
    with open("death_count.txt", "w") as file:
        file.write(str(prev_death_count + 1))


def read_level_id(frame):
    x, y = 50, 150 # 要裁剪的坐标
    h, w =  HEIGHT-900, WIDTH-1500 # 要裁剪的尺寸
    frame = frame[y:h, x:w]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 图像预处理：二值化（增强对比度）
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 使用 Tesseract 识别
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6")

    # 提取字母和数字（过滤分隔符）
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-")
    filtered_text = "".join([c if c in allowed_chars else " " for c in text])
    cleaned_text = " ".join(filtered_text.replace(" ","").split())
    pattern = r"^[A-Za-z0-9]{3}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3}$"
    if re.fullmatch(pattern, cleaned_text):
        return cleaned_text
    else:
        return None

def read_level_id():
    try:
        with open("level_id.txt", "r") as file:
            level_id = int(file.read())
    except FileNotFoundError:
        level_id = ""
    return level_id


def write_level_id(prev_level_id):
    with open("death_count.txt", "w") as file:
        file.write(str(prev_level_id))



if __name__ == "__main__":
    main()

    input_source.release()
    cv2.destroyAllWindows()


#TODO
'''
增加了新的功能之后黑屏的帧数变少了很多，需要知道原因
关卡死亡次数统计，随着关卡id的变化，死亡次数随着id重置，总死亡次数不变。
关卡id如何放到直播画面中去
通过的关卡数量统计？不同难度关卡的统计？团长信息 根据这些生成一个图？
'''



