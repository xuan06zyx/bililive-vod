import json
import time
import re
import threading
import requests
import pyautogui
import vlc

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as r:
    config = json.loads(r.read())
# 从配置文件获取直播间ID
roomid = config['roomid']
if roomid == 'your_roomid':
    roomid = input('请输入您的直播间ID(音量等配置可以打开 config.json 修改):')
    config['roomid'] = roomid
    with open('config.json', 'w', encoding='utf-8') as w:
        w.write(json.dumps(config))
# 外部音乐播放器暂停快捷键(默认是 ctrl + alt + p)
hotkey_stop = config['hotkey_stop']
# 外部音乐播放器下一首快捷键(可以跟暂停键一样, 默认是 ctrl + alt + right)
hotkey_next = config['hotkey_next']
# 音量 0~100 (默认是 50)
volume = config['volume']

# 直播间地址(修改roomid即可)
bilibili_url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={roomid}&room_type=0'
# 浏览器UA
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 变量声明(普通用户不需要管)
# 弹幕日志
item = []
# 文本列表, 用于点歌功能读弹幕
text_list = []
# 上一首歌
last_song = ''
# 歌曲链接
song_url = None

# 创建vlc播放器实例
instance = vlc.Instance()
# 创建媒体播放器
player = instance.media_player_new()


def get_barrage():
    global text_list
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
        time.sleep(0.5)


def play_music():
    global last_song, song_url
    while '点歌' in text_list[-1]:
        # 点歌功能
        # 匹配点歌关键词
        song_name = re.search(r'点歌\s*(.*)', text_list[-1]).group(1)

        # 获取歌曲信息
        qqmusic_url = f'https://api.lolimi.cn/API/yiny/?n=1&word={song_name}'
        qqmusic = requests.get(url=qqmusic_url, headers=header).json()
        # 歌名
        song = qqmusic['data']['song']
        # 通过歌名判断是否是与上次播放的是同一首歌
        if song == last_song:
            continue
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
        # 留作下一次触发点歌使用
        last_song = song
        # 如果点歌机触发时有歌曲在播放, 先停止
        if player.is_playing():
            player.stop()
        print('收到点歌请求:', song_name)
        print('\n歌名:', song,
              '\n歌手:', song_singer,
              '\n音质:', song_quality,
              '\n专辑:', song_album,
              '\n时长:', song_interval,
              '\n发布时间:', song_time,
              )
        time.sleep(0.8)


def hk_next():
    global song_url
    while True:
        if song_url:
            print('歌曲链接:', song_url)
            # 加载音乐文件
            media = instance.media_new(song_url)
            player.set_media(media)
            # 设置音量
            player.audio_set_volume(volume)
            # 按下快捷键暂停外部音乐播放
            pyautogui.hotkey(hotkey_stop)
            print('(已暂停外部音乐播放...)')
            # 播放音乐
            player.play()
            time.sleep(1)
            # 等待音乐播放完毕
            while player.is_playing():
                time.sleep(1)
            # 按下快捷键恢复外部音乐播放
            pyautogui.hotkey(hotkey_next)
            print('(已恢复外部音乐播放...)')
            song_url = None
        time.sleep(0.8)


# 创建监听弹幕线程并启动
get_barrage = threading.Thread(target=get_barrage)
get_barrage.start()

# 等待一段时间, 确保弹幕信息已加载完毕
time.sleep(1)

# 创建点歌机线程并启动
play_music = threading.Thread(target=play_music)
play_music.start()

# 等待一段时间, 确保歌曲信息已加载完毕
time.sleep(1)

#  创建播放歌曲线程并启动
hk_next = threading.Thread(target=hk_next)
hk_next.start()

get_barrage.join()
play_music.join()
hk_next.join()
