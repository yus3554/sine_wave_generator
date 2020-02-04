#!/usr/bin/env python3

import tkinter as tk
import pygame.mixer
import sine


def main():
    # rootウィンドウを作成
    root = tk.Tk()
    # StringVar
    var = tk.StringVar()

    # rootウィンドウに表示する部品
    hz_entry = tk.Entry(root)
    hz_entry_label = tk.Label(root, text="Hz")
    info_label = tk.Label(root, textvariable=var)
    ps_button = tk.Button(root, text='PLAY / STOP',
                          command=lambda: ps_pushed(root, info_label, var, hz_entry))

    # 部品の初期化
    init_tkinter(root, hz_entry, hz_entry_label, var, info_label, ps_button)
    # ボタンが表示されなくなるバグの対処
    button_fix(root)
    # メインループ
    root.mainloop()


def music_play(hz):  # temp.wavを再生
    A = 1  # 振幅
    fs = 44100  # サンプリング周波数
    sec = 1  # 秒
    filename = "temp.wav"
    # sine.pyから呼び出し
    sine.create_wave(A, hz, fs, sec, filename)
    pygame.mixer.init(frequency=fs//1)
    pygame.mixer.music.load(filename)  # ファイル名
    pygame.mixer.music.play(-1)  # -1で無限ループ


def ps_pushed(root, info_label, var, hz_entry):  # play/stopボタン押した時
    # label内がStoppedじゃなかったら停止  ←絶対良くないけど
    if info_label.cget("text") != "Stopped":
        pygame.mixer.music.stop()
        var.set("Stopped")
    else:
        # 入力されたHzを取得
        hz = get_hz_entry(hz_entry)
        music_play(hz)
        var.set("Playing " + str(hz) + " Hz")
    # 更新しないとなんか変なんなる
    root.update()


def enter_hz_entry(hz_entry, var):
    hz = get_hz_entry(hz_entry)
    music_play(hz)
    var.set("Playing " + str(hz) + " Hz")


def get_hz_entry(hz_entry):  # entryから取得した周波数を軽くバリデートして返す
    hz = hz_entry.get()
    hz = hz if hz.isdecimal() else '0'
    return int(hz)


def button_fix(root):  # ボタン表示のおまじない
    def fix():
        a = root.winfo_geometry().split('+')[0]
        b = a.split('x')
        w = int(b[0])
        h = int(b[1])
        root.geometry('%dx%d' % (w+1, h+1))

    root.update()
    root.after(0, fix)


def init_tkinter(root, hz_entry, hz_entry_label, var, info_label, ps_button):  # rootウィンドウの部品の初期化
    # rootウィンドウのタイトルを変える
    root.title("Sine Wave Generator")

    # 再生周波数
    hz_entry.grid(column=0, row=0)
    hz_entry.insert(tk.END, "100")
    hz_entry.bind('<Return>', lambda self: enter_hz_entry(hz_entry, var))
    hz_entry_label.grid(column=1, row=0)

    # 情報表示
    var.set("Stopped")
    info_label.grid(column=0, row=1, columnspan=2)

    # 再生・停止ボタン
    ps_button.grid(column=0, row=2, columnspan=2)


if __name__ == "__main__":
    main()
