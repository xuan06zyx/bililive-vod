import os
import re
import time
import json
import asyncio
import tkinter
import requests
import threading
import pyautogui
import websockets


class Bililive_Vod:
    def __init__(self):
        # 设置VLC库路径，需在import vlc之前
        path = os.getcwd()
        vcl_path = os.environ['PYTHON_VLC_MODULE_PATH'] = f"{path}\\VLC"
        os.environ['PYTHON_VLC_LIB_PATH'] = f'{vcl_path}\\libvlc.dll'

        # 初始化界面
        self.root = tkinter.Tk()
        self.root.title('Bililive Vod')
        self.root.iconbitmap("ayaka.ico")
        self.root.geometry('460x300+500+300')
        self.root.resizable(False, False)  # 不能拉伸

        # 文本框输入房间号
        self.roomid_tkinter = tkinter.Text(self.root, height=1, width=10)
        self.roomid_tkinter.place(x=180, y=50)

        import vlc

        # 浏览器UA
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
        }

        # 创建全局变量(普通用户不需要管)
        self.roomid = ''  # 房间号
        # 弹幕信息
        self.room_list = []  # 用户弹幕列表
        self.room_text_list = []  # 用户文本列表, 用于点歌功能读弹幕
        self.admin = None  # 房管弹幕
        self.admin_list = []  # 房管弹幕列表
        self.admin_text_list = []  # 房管文本列表, 用于停止播放
        self.song = None  # 歌曲
        self.last_song = ''  # 上一首歌
        self.song_url = None  # 歌曲链接
        self.song_url_list = []  # 歌曲链接列表
        self.song_list = []  # 歌单列表
        self.song_list_data = {}  # 歌单列表数据, 用于上传至ws服务器

        # 创建vlc播放器实例
        self.instance = vlc.Instance()
        # 创建媒体播放器
        self.player = self.instance.media_player_new()

    def control_voice(self, value=50):
        self.player.audio_set_volume(int(value))  # 设置音量

    # 获取弹幕
    def get_barrage(self):
        self.roomid = self.roomid_tkinter.get("1.0", tkinter.END)  # 获取 Text 部件中的文本内容
        print("直播间号:", self.roomid)
        while True:
            try:
                bilibili_url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={self.roomid}&room_type=0'
                # 获取弹幕
                bilibili = json.loads(requests.get(url=bilibili_url, headers=self.header).text)
                room = bilibili['data']['room']
                self.admin = bilibili['data']['admin']
            except KeyError:
                exit()
            # 获取所有弹幕
            for i in room:
                room_text = i['text']  # 弹幕文本
                room_name = i['nickname']  # 用户名
                room_timeline = i['timeline']  # 发送时间
                room_barrage = f'[{room_timeline}] {room_name}: {room_text}'
                if room_barrage not in self.room_list:
                    self.room_list.append(room_barrage)
                    self.room_text_list.append(room_text)
                    print(room_barrage)
            time.sleep(0.3)  # 每隔0.3秒获取一次弹幕

    # 点歌功能
    def get_music(self):
        while True:
            #  判断是否有弹幕
            if self.room_text_list:
                # 正则表达式
                diange = re.search(r'^点歌\s+(.*)', self.room_text_list[-1])
                if diange:
                    # 匹配点歌关键词
                    song_name = diange.group(1)
                    # 通过歌名判断歌曲是否在歌单中
                    if song_name in self.song_list:
                        continue
                    # 获取歌曲信息
                    qqmusic_url = f'https://api.lolimi.cn/API/yiny/?n=1&word={song_name}'
                    qqmusic = requests.get(url=qqmusic_url, headers=self.header).json()
                    # print(qqmusic)
                    if qqmusic['code'] != 200:
                        print(f'获取歌曲 {song_name} 失败! 错误代码:', qqmusic['code'], 'msg:', qqmusic['msg'])
                        continue
                    self.song = qqmusic['data']['song']  # 歌名
                    if self.song == self.last_song:  # 避免弹幕与获取到的歌名不同名所以二次判断是否与上次歌曲同名
                        continue
                    print('收到点歌请求:', song_name)
                    song_singer = qqmusic["data"]["singer"]  # 歌手
                    song_album = qqmusic['data']["album"]  # 专辑
                    song_time = qqmusic["data"]["time"]  # 发布时间
                    song_quality = qqmusic["data"]["quality"]  # 音质
                    song_interval = qqmusic["data"]["interval"]  # 歌曲时长
                    self.song_url = qqmusic["data"]["url"]  # 歌曲链接
                    # 写入歌单列表
                    self.song_list.append(self.song)

                    # 写入歌曲链接列表
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
            time.sleep(0.8)  # 每隔0.8秒获取一次弹幕

    # 播放音乐
    def play_music(self):
        while True:
            if len(self.song_url_list) > 0:
                for _ in self.song_url_list:
                    print('歌曲链接:', _)
                    # 加载音乐文件
                    media = self.instance.media_new(_)
                    self.player.set_media(media)
                    print('(已暂停外部音乐播放...)')
                    self.player.play()  # 播放音乐
                    time.sleep(0.8)
                    # 等待音乐播放完毕
                    while self.player.is_playing():
                        time.sleep(1)
                    # 删除播放过的歌曲的信息
                    del self.song_url_list[0]
                    del self.song_list[0]
                    print('(已恢复外部音乐播放...)')
            time.sleep(0.5)

    # 弹幕控制点歌机停止播放(仅限拥有房管权限的用户)
    def stop_music(self):
        while True:
            if self.room_text_list:
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
                                print('(弹幕触发停止音乐播放)')
            time.sleep(0.3)

    def stop(self):
        self.player.stop()
        print('(已停止播放音乐...)')

    async def send_data(self, websocket):
        """
        发送数据
        :param websocket:
        :return:
        """
        while True:
            # 将歌单列表数据提交到前端
            self.song_list_data = {'song_list': self.song_list}
            await websocket.send(json.dumps(self.song_list_data, ensure_ascii=False))
            await asyncio.sleep(0.5)  # 每秒发送一次数据

    # 使用 asyncio 形成循环
    async def start_server(self):
        # 创建WebSocket服务器
        async with websockets.serve(self.send_data, "localhost", 8765):
            await asyncio.Future()

    def start_websocket_server(self):
        # 启动WebSocket服务器
        asyncio.run(self.start_server())

    def start_web(self):
        # 启动WebSocket线程
        websocket_thread = threading.Thread(target=self.start_websocket_server)
        websocket_thread.start()

    def start(self):
        # 创建监听弹幕线程并启动
        get_barrage = threading.Thread(target=self.get_barrage)
        get_barrage.start()
        # 创建点歌机线程并启动
        get_music = threading.Thread(target=self.get_music)
        get_music.start()
        # 创建播放歌曲线程并启动
        play_music = threading.Thread(target=self.play_music)
        play_music.start()
        # 创建停播线程并启动
        stop_music = threading.Thread(target=self.stop_music)
        stop_music.start()


# 主程序入口
def main():
    bililive_vod = Bililive_Vod()

    # 启动按钮
    buttonStop = tkinter.Button(bililive_vod.root, text='启动', command=bililive_vod.start)
    buttonStop.place(x=120, y=10, width=50, height=20)

    # Web按钮
    pause_resume = tkinter.StringVar(bililive_vod.root, value='Web')
    buttonPlay = tkinter.Button(bililive_vod.root, textvariable=pause_resume, command=bililive_vod.start_web)
    buttonPlay.place(x=190, y=10, width=50, height=20)

    # 下一首
    buttonNext = tkinter.Button(bililive_vod.root, text='下一首', command=bililive_vod.stop)
    buttonNext.place(x=260, y=10, width=50, height=20)

    # 音量控制
    # HORIZONTAL表示为水平放置，默认为竖直,竖直为vertical
    s = tkinter.Scale(bililive_vod.root, label='音量', from_=0, to=100, orient=tkinter.HORIZONTAL,
                      length=240, showvalue=True, tickinterval=100, resolution=1, command=bililive_vod.control_voice)
    s.place(x=50, y=100, width=200)

    # 显示
    bililive_vod.root.mainloop()


if __name__ == '__main__':
    main()
