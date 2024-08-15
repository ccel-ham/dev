import os

import keyboard
import moviepy.editor as mp
import numpy as np
import win32api
import win32con
from PIL import Image, ImageGrab

# キャプチャしたフレームを保存するリスト
frames = []

# カーソル画像のパス
normal_cursor_image_path = "border_normal.png"  # 通常時のカーソル画像のパス
click_cursor_image_path = "border_click.png"  # クリック時のカーソル画像のパス

# カーソルのサイズ（両方のカーソル画像で同じサイズを使用）
cursor_size = 75

# クリック画像を表示するフレーム数
CLICK_FRAMES = 3


def load_cursor_image(image_path):
    """
    カーソル画像をロードし、サイズを調整する関数。
    """
    if os.path.isfile(image_path):
        cursor_img = Image.open(image_path).convert("RGBA")
        # カーソル画像をリサイズ
        cursor_img = cursor_img.resize(
            (cursor_size, cursor_size), Image.Resampling.LANCZOS
        )
        return cursor_img
    else:
        print(f"カーソル画像が見つかりません: {image_path}")
        return None


def get_mouse_position():
    return win32api.GetCursorPos()


def is_left_button_down():
    return win32api.GetKeyState(win32con.VK_LBUTTON) < 0


def draw_cursor(image, pos, normal_cursor_img, click_cursor_img, click_count):
    """
    画面にカーソルを描画する関数。
    pos: カーソルの位置 (x, y)
    normal_cursor_img: 通常時のカーソル画像
    click_cursor_img: クリック時のカーソル画像
    click_count: クリック画像を表示するフレーム数カウンタ
    """
    cursor_img = click_cursor_img if click_count > 0 else normal_cursor_img
    if cursor_img:
        image.paste(
            cursor_img,
            (pos[0] - cursor_size // 2, pos[1] - cursor_size // 2),
            cursor_img,
        )


def capture_screen():
    print("全画面キャプチャを開始します。終了するには 'q' キーを押してください。")

    normal_cursor_img = load_cursor_image(normal_cursor_image_path)
    click_cursor_img = load_cursor_image(click_cursor_image_path)
    click_count = 0

    try:
        while True:
            # 全画面のスクリーンショットをキャプチャ
            screenshot = ImageGrab.grab()
            mouse_x, mouse_y = get_mouse_position()

            if is_left_button_down():
                click_count = CLICK_FRAMES  # クリックが検出されたらカウンタをリセット
            else:
                if click_count > 0:
                    click_count -= 1  # クリックカウンタを減らす

            # カーソルを描画
            draw_cursor(
                screenshot,
                (mouse_x, mouse_y),
                normal_cursor_img,
                click_cursor_img,
                click_count,
            )

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
