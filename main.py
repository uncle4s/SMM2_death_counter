import cv2
import keyboard
import numpy as np

DEVICE_ID = 4 #仮想カメラのID

# パラメータ設定
DEATH_FRAME_NUM = 124  # マリオが死んだ際に発生する真っ黒の画面が連続するフレーム数
THRESHOLD = 20  # 真っ黒とみなすピクセル値の閾値
BLACK_RATIO = 0.99  # 画面が真っ黒と判定する割合 (BLACK_RATIO*100 %以上が黒)

WIDTH = 1920 #switchの解像度
HEIGHT = 1080

input_source = cv2.VideoCapture(DEVICE_ID) #映像の取得

input_source.set(cv2.CAP_PROP_FPS, 30) #画面設定
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
                if blackFrameCout >= DEATH_FRAME_NUM and blackFrameCout <= DEATH_FRAME_NUM + 3: #死亡判定(DEATH_FRAME_NUMフレーム連続で真っ黒の画面が検出されたら)    
                    prev_death_count = read_death_count() #死亡回数の読み込み
                    write_death_count(prev_death_count) #死亡回数の書き込み
                    print("death")
                blackFrameCout = 0
                



def get_frame(): #画像の取得
    if not input_source.isOpened():
        print("failed to open camera")
        exit()

    ret, frame_origin = input_source.read()
    if not ret:
        print("failed to get frame")
        exit()

    x, y = 265, 71 # トリミングする座標
    h, w =  HEIGHT-90, WIDTH-20 # トリミングするサイズ
    frame = frame_origin[y:h, x:w]
    cv2.imshow("input_source", frame)
    cv2.waitKey(1)
    return frame



def is_black_screen(frame): #真っ黒の画面かどうかの判定
    # フレームをグレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 黒いピクセルの割合を計算
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



if __name__ == "__main__":
    main()

    input_source.release()
    cv2.destroyAllWindows()


