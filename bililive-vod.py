import re
import vlc
import json
import time
import requests
import threading
import pyautogui
import tkinter as tk


class Bililive_Vod:
    def __init__(self):
        # 读取配置文件
        with open('config.json', 'r', encoding='utf-8') as r:
            self.config = json.loads(r.read())
        # 从配置文件获取直播间ID
        self.roomid = self.config['roomid']
        if self.roomid == 'your_roomid':
            self.roomid = input('请输入您的直播间ID 音量(volume)等配置可以打开 config.json 修改:')
            self.config['roomid'] = self.roomid
            with open('config.json', 'w', encoding='utf-8') as w:
                w.write(json.dumps(self.config))
        # 外部音乐播放器暂停快捷键(默认是 ctrl + alt + p)
        self.hotkey_stop = self.config['hotkey_stop']
        # 外部音乐播放器下一首快捷键(可以跟暂停键一样, 默认是 ctrl + alt + right)
        self.hotkey_next = self.config['hotkey_next']
        # 音量 0~100 (默认是 50)
        self.volume = self.config['volume']

        # 直播间地址(修改roomid即可)
        self.bilibili_url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={self.roomid}&room_type=0'
        # 浏览器UA
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        # 变量声明(普通用户不需要管)
        # 弹幕信息
        # 用户弹幕列表
        self.room_list = []
        # 用户文本列表, 用于点歌功能读弹幕
        self.room_text_list = []
        # 房管弹幕
        self.admin = None
        # 房管弹幕列表
        self.admin_list = []
        # 房管文本列表, 用于停止播放
        self.admin_text_list = []
        # 上一首歌
        self.last_song = ''
        # 歌曲链接
        self.song_url = None
        # 歌曲链接列表
        self.song_url_list = []
        # 歌单列表
        self.song_list = []
        # 歌名
        self.song = None

        # 创建vlc播放器实例
        self.instance = vlc.Instance()
        # 创建媒体播放器
        self.player = self.instance.media_player_new()

    # 获取弹幕
    def get_barrage(self):
        while True:
            # 获取弹幕
            bilibili = json.loads(requests.get(url=self.bilibili_url, headers=self.header).text)
            room = bilibili['data']['room']
            self.admin = bilibili['data']['admin']
            # 获取所有弹幕
            for i in room:
                # 弹幕文本
                room_text = i['text']
                # 用户名
                room_name = i['nickname']
                # 发送时间
                room_timeline = i['timeline']
                room_barrage = f'[{room_timeline}] {room_name}: {room_text}'
                if room_barrage not in self.room_list:
                    self.room_list.append(room_barrage)
                    self.room_text_list.append(room_text)
                    print(room_barrage)
            time.sleep(0.5)

    # 点歌功能
    def get_music(self):
        while True:
            # 正则表达式
            diange = re.search(r'^点歌\s+(.*)', self.room_text_list[-1])
            if diange:
                # 匹配点歌关键词
                song_name = diange.group(1)
                # 通过歌名判断是否在歌单中
                if song_name in self.song_list:
                    continue
                # 获取歌曲信息
                qqmusic_url = f'https://api.lolimi.cn/API/yiny/?n=1&word={song_name}'
                qqmusic = requests.get(url=qqmusic_url, headers=self.header).json()
                # print(qqmusic)
                if qqmusic['code'] != 200:
                    print(f'获取歌曲 {song_name} 失败! 错误代码:', qqmusic['code'])
                    continue
                # 歌名
                self.song = qqmusic['data']['song']
                # 避免不同名所以二次判断是否与上次歌曲同名
                if self.song == self.last_song:
                    continue
                print('收到点歌请求:', song_name)
                # 歌手
                song_singer = qqmusic["data"]["singer"]
                # 专辑
                song_album = qqmusic['data']["album"]
                # 发布时间
                song_time = qqmusic["data"]["time"]
                # 音质
                song_quality = qqmusic["data"]["quality"]
                # 歌曲时长
                song_interval = qqmusic["data"]["interval"]
                # 歌曲链接
                self.song_url = qqmusic["data"]["url"]
                # 写入歌单列表
                self.song_list.append(self.song)
                # 写入歌曲链接
                self.song_url_list.append(self.song_url)
                print('\n歌名:', self.song,
                      '\n歌手:', song_singer,
                      '\n音质:', song_quality,
                      '\n专辑:', song_album,
                      '\n时长:', song_interval,
                      '\n发布时间:', song_time,
                      )
                print('当前歌单列表:', self.song_list)
                # 留作下一次触发点歌使用
                self.last_song = self.song
            time.sleep(0.8)

    def play_music(self):
        while True:
            for _ in self.song_url_list:
                print('歌曲链接:', _)
                # 加载音乐文件
                media = self.instance.media_new(_)
                self.player.set_media(media)
                # 设置音量
                self.player.audio_set_volume(self.volume)
                # 按下快捷键暂停外部音乐播放
                pyautogui.hotkey(self.hotkey_stop)
                print('(已暂停外部音乐播放...)')
                # 播放音乐
                self.player.play()
                time.sleep(1)
                # 等待音乐播放完毕
                while self.player.is_playing():
                    time.sleep(1)
                # 删除播放过的歌曲的信息
                if len(self.song_url_list) > 0:
                    del self.song_url_list[0]
                    del self.song_list[0]
                # 按下快捷键恢复外部音乐播放
                if len(self.song_url_list) > 0:
                    continue
                pyautogui.hotkey(self.hotkey_next)
                print('(已恢复外部音乐播放...)')
            time.sleep(1)

    # 控制点歌机停止播放(仅限拥有房管权限的用户)
    def stop_music(self):
        while True:
            # 获取房管弹幕
            for o in self.admin:
                # 弹幕文本
                admin_text = o['text']
                # 用户名
                admin_name = o['nickname']
                # 发送时间
                admin_timeline = o['timeline']
                admin_barrage = f'[{admin_timeline}] {admin_name}: {admin_text}'
                if admin_barrage not in self.admin_list:
                    self.admin_list.append(admin_barrage)
                    self.admin_text_list.append(admin_text)
                    # 如果有音乐在播放同时歌曲链接大于 0 则停止播放音乐, 将会自动跳转到下一首
                    if self.player.is_playing() and len(self.song_url_list) > 0:
                        if self.admin_text_list[-1] == '下一首' or self.admin_text_list[-1] == '停止播放':
                            self.player.stop()
                            print('(已停止播放当前歌曲...)')
            time.sleep(1)

    def stop(self):
        self.player.stop()


bililive_vod = Bililive_Vod()


def main():
    # 创建监听弹幕线程并启动
    get_barrage = threading.Thread(target=bililive_vod.get_barrage)
    get_barrage.start()

    # 等待一段时间, 确保弹幕信息已加载完毕
    time.sleep(1)

    # 创建点歌机线程并启动play_music
    get_music = threading.Thread(target=bililive_vod.get_music)
    get_music.start()

    # 等待一段时间, 确保歌曲信息已加载完毕
    time.sleep(1)

    # 创建播放歌曲线程并启动
    play_music = threading.Thread(target=bililive_vod.play_music)
    play_music.start()

    # 等待一段时间, 确保弹幕信息已加载完毕
    time.sleep(1)

    # 创建停播线程并启动
    stop_music = threading.Thread(target=bililive_vod.stop_music)
    stop_music.start()


if __name__ == '__main__':
    root = tk.Tk()
    # 设置窗口title
    root.title('Bililive-Vod')
    # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
    root.geometry('400x250+480+270')

    # 更改左上角窗口的的icon图标
    root.iconbitmap('ayaka.ico')
    # 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
    root["background"] = "white"

    # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
    text = tk.Label(root, text="Bilibili直播点歌姬", font=('Times', 20, 'bold italic'))
    # 将文本内容放置在主窗口内
    text.pack()

    # 启动按钮 调用main函数
    button = tk.Button(root, text="启动", command=main)
    # 将按钮放置在主窗口内
    button.pack(side="bottom")

    # 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
    button = tk.Button(root, text="停止播放", command=bililive_vod.stop)
    # 将按钮放置在主窗口内
    button.pack(side="bottom")

    # 进入主循环，显示主窗口
    root.mainloop()
