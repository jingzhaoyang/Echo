# Echo 简介

它是一个语音问答的机器人，使用百度的语音识别和语音合成API，同时问答部分使用了图灵机器人的API。

# 安装

安装依赖库
```
sudo pip install PyAudio requests
```

# 配置

配置文件是`config.py`, 其中阀值设置建议打开debug信息，根据自己麦克风在安静环境中的音量值进行设置。

# 运行

```
python app.py
```
