# 使用 Android 自动化工具获取评论数据

都是获取到当前布局的 uix 格式文件，解析得到数据

淘宝版本 10.32.10.16

## 原始方案

命令行调用 adb

装了 adb 就能用，直接 subprocess.run()，速度慢

## 拓展方案A

[uiautomator2](https://github.com/openatx/uiautomator2)

除了 adb 还需要装个三方库，简洁且速度快

<- Using this now

## 拓展方案B

[Appium](https://appium.io/) + Appium-Python-Client

除了 adb 还要配一堆东西（参照官方文档），但是确实很强大

使用体验很接近 selenium

```python
# 先去装个 Appium Server 然后启动
from appium import webdriver
from appium.options.android import UiAutomator2Options
desired_caps = {
        'platformName': 'Android',
        'deviceName': 'Android Emulator',  # 可替换为实际设备名称
        'automationName': 'UiAutomator2',
        'noReset': True,  # 保持应用状态，不重新启动
        'newCommandTimeout': 600  # 设置更长的等待时间，防止应用会话超时
    }

options = UiAutomator2Options().load_capabilities(desired_caps)
driver = webdriver.Remote('http://localhost:4723', options=options)
# 连接完毕，可进一步操作
```