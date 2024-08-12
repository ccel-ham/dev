import os
import numpy as np
from PIL import ImageGrab, Image, ImageDraw
import moviepy.editor as mp
import win32api
import win32con
import keyboard

# キャプチャしたフレームを保存するリスト
frames = []

# カーソル画像のパス
cursor_image_path = "cursor.png"  # ここにカーソル画像のパスを指定

# カーソルのサイズとイメージを定義
cursor_size = 75  # カーソル画像のサイズ


def load_cursor_image():
    """
    カーソル画像をロードし、サイズを調整する関数。
    """
    if os.path.isfile(cursor_image_path):
        cursor_img = Image.open(cursor_image_path).convert("RGBA")
        # カーソル画像をリサイズ
        cursor_img = cursor_img.resize(
            (cursor_size, cursor_size), Image.Resampling.LANCZOS
        )
        return cursor_img
    else:
        print(f"カーソル画像が見つかりません: {cursor_image_path}")
        return None


def get_mouse_position():
    return win32api.GetCursorPos()


def is_left_button_down():
    return win32api.GetKeyState(win32con.VK_LBUTTON) < 0


def draw_cursor(image, pos, clicked, cursor_img):
    """
    画面にカーソルを描画する関数。
    pos: カーソルの位置 (x, y)
    clicked: クリック中かどうか (True/False)
    cursor_img: カーソル画像
    """
    if cursor_img:
        # カーソル画像を描画
        if clicked:
            # カーソル画像を少し変えるか色を変更してクリック状態を表現する
            cursor_img = cursor_img.point(lambda p: p * 0.7)  # 色を少し暗くする例
        image.paste(
            cursor_img,
            (pos[0] - cursor_size // 2, pos[1] - cursor_size // 2),
            cursor_img,
        )


def capture_screen():
    print("全画面キャプチャを開始します。終了するには 'q' キーを押してください。")

    cursor_img = load_cursor_image()

    try:
        while True:
            # 全画面のスクリーンショットをキャプチャ
            screenshot = ImageGrab.grab()
            mouse_x, mouse_y = get_mouse_position()
            clicked = is_left_button_down()

            # カーソルを描画
            draw_cursor(screenshot, (mouse_x, mouse_y), clicked, cursor_img)

            frames.append(np.array(screenshot))

            # 'q' キーが押されたら終了
            if keyboard.is_pressed("q"):
                break
    except KeyboardInterrupt:
        print("キャプチャを終了しました。")
    finally:
        print("キャプチャを終了しました。")
        save_video()


# 画像フレームを結合して動画を保存する関数
def save_video():
    video_output_filename = "output.mp4"

    if frames:
        try:
            # 画像フレームを動画に変換
            clip = mp.ImageSequenceClip([f for f in frames], fps=20)
            clip.write_videofile(video_output_filename, codec="libx264")
            print(f"動画を作成しました: {video_output_filename}")
        except Exception as e:
            print(f"動画作成中にエラーが発生しました: {e}")
    else:
        print("フレームがありません。動画は作成されませんでした。")


if __name__ == "__main__":
    capture_screen()
