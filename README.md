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


# 在树莓派上运行

因为树莓派本身是只有音频输出，而没有音频输入的，所以需要外接usb的声卡。另外，我们还需要将外接的usb声卡设置为系统默认的音频输入和输出。

## 设置默认声卡为USB声卡

创建并编辑此文件：`sudo vim /etc/modprobe.d/alsa-base.conf`，输入下面内容：
```
options snd_usb_audio index=0
options snd_bcm2835 index=1

options snd slots=snd_usb_audio,snd_bcm2835
```
保存退出后，重启树莓派生效。

## 检测是否配置成功

通过下面命令可以验证USB声卡是否为默认声卡
```
pi@raspberrypi:~ $ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 1: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

如果默认为USB声卡，那么`card 0`后面就是你的声卡设备名，类似上面内容。

## 在文本界面下更改音频输出和输入的大小

在图形界面我们，可以通过任务栏的音量图标更改声音大小，以及麦克风声音大小。而在文本界面或者远程ssh登录界面，我们需要通过`alsamixer`命令来执行操作。
