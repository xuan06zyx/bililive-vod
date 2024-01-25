<div align="center">

<h1>Bililive-Vod</h1>
<h1>Bilibili直播弹幕点歌姬</h1>

</div>

*****本软件由纯Python制作而成，项目还在开发测试极度不成熟，推荐有一定代码基础的用户使用本软件*****
## 免责声明

本软件仅供学习交流使用，请于下载后24小时内删除，不得用于任何商业用途，否则后果自负。

## 功能

- [x] 监控弹幕
- [x] 弹幕点歌
- [x] 联动外部音乐播放器
- [ ] 多线程实现同时监控弹幕及点歌
- [ ] 歌单列表、歌词等等添加到OBS显示

## 使用说明

1. 安装[Python 3.11](https://www.python.org/downloads/release/python-3113/) (其他版本安装依赖项时可能会出现问题)
2. 安装本软件:
   ```shell
   git clone https://github.com/xuan06zyx/bililive-vod.git
   cd bililive-vod
   ```
3. 如果您是第一次运行本软件，还请先打开vod.py文件，在修改开头的配置参数(如下)：
   ```text
   # 直播间ID
   roomid = 'your-roomid'
   # 外部音乐播放器暂停快捷键
   hotkey_start = 'ctrl', 'alt', 'p'
   # 外部音乐播放器下一首快捷键(可以跟暂停键一样)
   hotkey_next = 'ctrl', 'alt', 'right'
   ```
4. 国内用户可以输入`pip config set global.index-url https://mirrors.aliyun.com/pypi/simple` 设置国内pip源
5. 输入`pip install -r requirements.txt`安装依赖
6. 输入`Python vod.py`运行本软件

## 问题反馈

1. 有任何问题都可以提issues（新手程序员很少会看）
2. 国内用户可以加我[QQ](https://api.lolimi.cn/API/tzmp/api.php?qq=2015441509)

## 注意事项
1. 目前只支持高音质歌曲，即后缀为flac的，非flac后缀音乐（下载下来统一是flac，从歌曲链接中查看原后缀）会直接跳过
2. 建议先播放外部音乐再启动本脚本
3. 由于B站直播弹幕会有历史记录，如果历史记录中有点歌记录会直接触发点歌功能
4. 由于本软件是单线程的，监听弹幕和播放音乐是同一个线程里的，播放音乐时不会再监听弹幕，所以在播放途中点歌了，点歌的弹幕不会被监听到，也就不会打断当前音乐的播放
5. 实际上由于 pygame 和 API 的限制，标准及以下音质的音乐文件是 .m4a 的，而pygame 恰巧无法播放该格式的文件，所以我连自适应文件名后缀都没做XD

⭐**如果喜欢，点个star~**⭐
