import cv2
import keyboard
import numpy as np

DEVICE_ID = 4 #仮想カメラのID

# パラメータ設定
DEATH_FRAME_NUM = 115  # マリオが死んだ際に発生する真っ黒の画面が連続するフレーム数
THRESHOLD = 10  # 真っ黒とみなすピクセル値の閾値
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
            if check_black_screen(frame):
                blackFrameCout += 1
            else:
                if blackFrameCout >= DEATH_FRAME_NUM and blackFrameCout <= DEATH_FRAME_NUM + 3: #死亡判定(DEATH_FRAME_NUMフレーム連続で真っ黒の画面が検出されたら)    
                    print("death detected")
                    blackFrameCout = 0
                blackFrameCout = 0
                



def get_frame(): #画像の取得
    if not input_source.isOpened():
        print("failed to open camera")
        exit()

    ret, frame_origin = input_source.read()
    if not ret:
        print("failed to get frame")
        exit()

    x, y = 0, 0 # トリミングする座標
    h, w =  HEIGHT-106, WIDTH-188 # トリミングするサイズ
    frame = frame_origin[y:y+h, x:x+w]
    cv2.imshow("input_source", frame)
    cv2.waitKey(1)
    return frame



def check_black_screen(frame): #真っ黒の画面かどうかの判定
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


if __name__ == "__main__":
    main()


input_source.release()
cv2.destroyAllWindows()