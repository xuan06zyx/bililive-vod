<div align="center">

<h1>Bililive-Vod</h1>

</div>

*****本软件由纯Python制作而成，项目还在开发测试极度不成熟，推荐有一定代码基础的用户使用本软件*****
## 免责声明

本软件仅供学习交流使用，请于下载后24小时内删除，不得用于任何商业用途，否则后果自负。

## 功能

- [x] 监控弹幕
- [x] 弹幕点歌
- [x] 联动外部音乐播放器
- [ ] 多线程实现同时监控弹幕及点歌

## 使用说明

1. 安装[Python 3.11](https://www.python.org/downloads/release/python-3113/) (其他版本安装依赖项时可能会出现问题)
2. 安装本软件:
   
   ```shell
   git clone https://github.com/xuan06zyx/Bililive-Vod.git
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
4. 解压文件，并进入文件夹
5. 复制文件夹路径
6. 右键开始菜单(win + x)，选择`终端管理员`，输入`cd 刚刚复制的路径`
7. 国内用户可以输入`pip config set global.index-url `设置国内pip源
8. 输入`pip install -r requirements.txt`安装依赖
9. 输入`Python vod.py`运行本软件

## 问题反馈

1. 有任何问题都可以提issues（新手程序员很少会看）
2. 国内用户可以加我[QQ](https://api.lolimi.cn/API/tzmp/api.php?qq=2015441509)

⭐**如果喜欢，点个star~**⭐
