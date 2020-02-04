import numpy as np
import wave
import struct

# sine波作ってtemp.waveとして保存

# sin波
# --------------------------------------------------------------------------------------------------------------------


def create_wave(A, f0, fs, t, filename):  # A:振幅,f0:基本周波数,fs:サンプリング周波数,再生時間[s]
    # nポイント
    # --------------------------------------------------------------------------------------------------------------------
    point = np.arange(0, fs*t)
    sin_wave = A * np.sin(2*np.pi*f0*point/fs)

    sin_wave = [int(x * 32767.0) for x in sin_wave]  # 16bit符号付き整数に変換

    # バイナリ化
    binwave = struct.pack("h" * len(sin_wave), *sin_wave)

    # サイン波をwavファイルとして書き出し
    w = wave.Wave_write(filename)
    # (チャンネル数(1:モノラル,2:ステレオ)、サンプルサイズ(バイト)、サンプリング周波数、フレーム数、圧縮形式(今のところNONEのみ)、圧縮形式を人に判読可能な形にしたもの？通常、 'NONE' に対して 'not compressed' が返されます。)
    p = (1, 2, fs, len(binwave), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(binwave)
    w.close()
