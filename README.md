<div align="center">

<h1>Bililive-Vod</h1>
<h1>Bilibili直播弹幕点歌姬</h1>

</div>

*****本脚本由纯Python制作而成，项目还在开发测试中极度不成熟，推荐有一定代码基础的用户使用本软件*****
## 免责声明

本软件仅供学习交流使用，请于下载后24小时内删除，不得用于任何商业用途，否则后果自负。

## 功能

- [x] 监控弹幕
- [x] 弹幕点歌
- [x] 联动外部音乐播放器
- [x] 多线程实现同时监控弹幕及点歌
- [ ] 歌单列表、显示歌词等等
- [ ] 支持更多音乐播放器
- [ ] 制作UI 让配置以及启动软件更简单易上手

## 使用说明

1. 安装[Python 3.11](https://www.python.org/downloads/release/python-3113/) (其他版本安装依赖项时可能会出现问题)
2. 安装[VLCforWindows](https://www.videolan.org/vlc/download-windows.html) (务必安装该应用,否则将无法使用本项目)
3. 使用打包好的程序
   1. 下载[Release](https://github.com/xuan06zyx/bililive-vod/releases)中的最新版本压缩包解压双击Bililive-Vod.exe即可
4. 源码运行：
   1. 安装本脚本:
      ```shell
      git clone https://github.com/xuan06zyx/bililive-vod.git
      cd bililive-vod
      ```
   2. 如果您是第一次运行本脚本，你可以打开 config.json 文件，修改如下配置参数：
      ```json
      {
      "roomid": "your_roomid", (请替换成您的直播间ID)
      "hotkey_stop": ["ctrl", "alt", "p"], (用于点歌时暂停外部音乐 没有或不需要可以不填)
      "hotkey_next": ["ctrl", "alt", "right"], (可以设置跟暂停音乐一样的 那样是继续播放外部音乐而不是放下一首 没有或不需要可以不填)
      "volume": 50 (音量0~100 默认50)
      }
      ```
   3. 国内用户可以输入`pip config set global.index-url https://mirrors.aliyun.com/pypi/simple` 设置国内pip源
   4. 输入`pip install -r requirements.txt`安装依赖
   5. 输入`Python Bililive-Vod.py`运行本软件
5. 在目标直播间输入点歌+空格+歌曲名称，如`点歌 青花瓷`

## 问题反馈

1. 有任何问题都可以提issues（新手程序员很少会看）
2. 国内用户可以加我[QQ](https://api.lolimi.cn/API/tzmp/api.php?qq=2015441509)

## 注意事项
1. 建议先开始播放外部音乐再启动本脚本, 否则在触发点歌功能时会启动外部音乐播放器导致同时播放
2. 由于B站直播弹幕会有历史记录，如果历史记录中最新一条弹幕含有点歌会直接触发点歌功能
3. 本软件目前仅支持QQ音乐, 不支持以歌名+歌手的形式搜索指定歌曲
<br>
⭐**如果喜欢，点个star~**⭐
