import json
import os
import time
import re
import requests
import pygame
import pyautogui

# 直播间ID
roomid = '24005882'
# 外部音乐播放器暂停快捷键
hotkey_start = 'ctrl', 'alt', 'p'
# 外部音乐播放器下一首快捷键(可以跟暂停键一样)
hotkey_next = 'ctrl', 'alt', 'right'

# 直播间地址
bilibili_url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={roomid}&room_type=0'
# 浏览器UA
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
# 初始化混音器
pygame.mixer.init()
# 弹幕日志
item = []
# 文本列表, 用于点歌功能读弹幕
text_list = []
while True:
    # 获取弹幕
    bilibili = json.loads(requests.get(url=bilibili_url, headers=header).text)
    bilibili = bilibili['data']['room']
    for i in bilibili:
        # 弹幕文本
        text = i['text']
        # 用户名
        name = i['nickname']
        # 发送时间
        timeline = i['timeline']
        barrage = f'[{timeline}] {name}: {text}'
        if barrage not in item:
            item.append(barrage)
            text_list.append(text)
            print(barrage)
            # 点歌功能
            # 匹配点歌关键词
            if '点歌' in text_list[-1]:
                song_name = re.search(r'点歌\s*(.*)', text_list[-1]).group(1)
                print('收到点歌请求:', song_name)

                # 获取歌曲信息
                qqmusic_url = f'https://api.lolimi.cn/API/yiny/?word={song_name}&n=1'
                qqmusic = requests.get(url=qqmusic_url, headers=header).json()
                # 歌名
                song = qqmusic['data']['song']
                # 歌手
                song_singer = qqmusic['data']['singer']
                # 专辑
                song_album = qqmusic['data']['album']
                # 发布时间
                song_time = qqmusic['data']['time']
                # 音质
                song_quality = qqmusic['data']['quality']
                # 歌曲时长
                song_interval = qqmusic['data']['interval']
                # 歌曲链接
                song_url = qqmusic['data']['url']
                print('歌曲链接:', song_url)

                # 下载歌曲
                song_file_path = f'{song}.flac'
                if not os.path.exists(song_file_path):
                    print('正在下载歌曲:', song)
                    song_file = requests.get(url=song_url, headers=header).content
                    with open(song_file_path, 'wb') as f:
                        f.write(song_file)
                else:
                    print('歌曲文件已存在:', song_file_path)
                print(  # '已保存歌曲到本地:', song_file_path,
                    '\n歌名:', song,
                    '\n歌手:', song_singer,
                    '\n音质:', song_quality,
                    '\n专辑:', song_album,
                    '\n时长:', song_interval,
                    '\n发布时间:', song_time,
                )

                # 加载音乐文件
                try:
                    pygame.mixer.music.load(song_file_path)
                except pygame.error:
                    print('音乐文件格式非flac, 尝试转换...')
                    continue
                # 从文件或缓冲区对象创建新的 Sound 对象
                sound = pygame.mixer.Sound(song_file_path)
                # 获取音乐文件时长
                interval = pygame.mixer.Sound.get_length(sound)
                # 设置音量
                pygame.mixer.music.set_volume(0.3)
                # 按下快捷键暂停外部音乐播放
                # pyautogui.hotkey('ctrl', 'alt', 'p')
                pyautogui.hotkey(hotkey_start)
                print('(已暂停外部音乐播放...)')
                # 播放音乐
                pygame.mixer.music.play()
                print('开始播放, 时长:', interval)
                # PS: 由于pygame.mixer.music.play()是非阻塞的, 需要使用time.sleep()来等待音乐播放完毕
                time.sleep(interval)
                # 卸载音乐文件
                pygame.mixer.music.unload()
                # 音乐播放完毕后, 按下快捷键恢复外部音乐播放
                # pyautogui.hotkey('ctrl', 'alt', 'right')
                pyautogui.hotkey(hotkey_next)
                print('(已恢复外部音乐播放...)')
        else:
            print("(目前还没有新弹幕)")

        time.sleep(0.5)
