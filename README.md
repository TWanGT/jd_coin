## 自动登录京东，打卡领钢镚，签到领京豆

[![Python](https://img.shields.io/badge/Python-3.5%2B-blue.svg)](https://www.python.org)

> 基于这个老哥的, [传送门](https://github.com/CaoZ/JD-Coin)
> `CaoZ` 已经2年多没有维护了, 在 `CaoZ` 的基础上修复了一些因为变动导致失效的签到点, 并新增了一些
> 我主要用的是方法一(基于内置浏览器实现签到), 方法二没有进行维护

### 使用方法：

1. 安装`Python` (3.5 或更高版本）

2. 建立虚拟运行环境（可选）

3. 下载代码

4. 安装依赖：`pip install -r requirements.txt`

5. 创建配置文件（可选）

6. 运行：`python app/main.py`

<br>


## 说明

直接登录京东较复杂，不易实现，因此采用了以下两种方式进行登录：

#### 方式一：

> 2017-08-13 更新：即现在的默认分支`browser`。

借助内置浏览器登录。本方式中使用 `PyQt5` 的 `WebEngine` 构建了个简易浏览器，在其中登录京东即可。

登录后浏览器窗口会自动关闭，程序会获取到 cookie，然后就可以继续签到了~

![浏览器方式登录](docs/browser.png)


#### 方式二：

> 2017-08-13 更新：目前此方式[依赖的包](https://github.com/gera2ld/qqlib)存在一些问题，暂不可用，请使用「浏览器方式」登录。

通过第三方登录的方式，登录了[绑定的 QQ 帐号](https://safe.jd.com/union/index.action)，也就登录了京东。

在登录 QQ 时有时会出现需要输入验证码的情况，若是在 [iTerm2](http://www.iterm2.com/) 中运行，验证码图片会显示在终端中，直接输入即可；否则会调用系统关联应用打开验证码图片。

![通过 QQ 登录](docs/qq.png)


## 其他

### 配置文件说明

#### 帐号/密码：

可以将帐号/密码保存到配置文件中（若使用浏览器方式，可以只保存帐号），这样就不用在每次登录时手动输入了（虽然使用了 cookie 保存登录状态，但京东还是会每隔几天就让你重新登录的...）。

将默认配置文件复制为`config.json`，然后使用 [Base85](https://en.wikipedia.org/wiki/Ascii85) 方式将对应的帐号、密码编码后填入配置文件中即可，完成后是这样子的：

```json
{
  "debug": false,
  "jd": {
    "username": "b#rBMZeeX@",
    "password": "aA9+EcW-iJ"
  }
}
```

（是不是比明文安全性多了一点点呢？^_^)

编码示例（Python）：

```python
>>> import base64
>>> base64.b85encode(b'username').decode()
'b#rBMZeeX@'
```

#### 我没有小白卡/我想跳过某些任务：

将想要跳过的任务填写到配置文件中的 `jobs_skip` 中即可。比如想跳过「小白卡钢镚打卡」任务，填写 `Daka` 即可：

```json
"jobs_skip": ["Daka"]
```

跳过多个任务:

```json
"jobs_skip": ["DataStation", "Daka"]  
```

任务列表:

| 任务 | 描述 |
| --- | --- |
| DaKa | 小白卡钢镚打卡（已下线） |
| DakaApp | 京东客户端钢镚打卡 |
| BeanApp | 京东客户端签到领京豆 |
| DoubleSign | 客户端双签赢奖励活动（不定时开放） |
| Bean | 京东会员页签到领京豆 |
| SignJR | 京东金融签到领奖励 |
| DataStation | 流量加油站签到领流量 |
| RedPacket | 京东小金库现金红包（已下线） |
| plusSign | 京东会员领京豆(摇一摇) |
| jr_fanpai | 京东金融翻牌） |
| payBack | 京东支付返京豆 |

<br>


### 设置网络代理

设置环境变量 `HTTP_PROXY` / `HTTPS_PROXY` 即可。

<br>


## Example

```log
2019-08-23 18:26:44,626 root[config] INFO: 使用配置文件 "config.json".
2019-08-23 18:26:45,469 root[main] INFO: # 从文件加载 cookies 成功.
2019-08-23 18:26:45,469 jobs[daka] INFO: Job Start: 京东客户端钢镚打卡
2019-08-23 18:26:45,793 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:45,793 jobs[daka_app] INFO: 今日已打卡: True
2019-08-23 18:26:45,794 jobs[daka] INFO: Job End.
2019-08-23 18:26:45,794 jobs[daka] INFO: Job Start: 京东客户端签到领京豆
2019-08-23 18:26:46,086 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:46,497 jobs[bean_app] INFO: 今日已签到: True; 签到天数: 6; 现有京豆: 2038
2019-08-23 18:26:46,497 jobs[daka] INFO: Job End.
2019-08-23 18:26:46,497 jobs[daka] INFO: Job Start: 流量加油站签到领流量
2019-08-23 18:26:46,777 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:47,098 jobs[data_station] INFO: 今日已签到: True; Message: 您今日已签到.
2019-08-23 18:26:47,098 jobs[daka] INFO: Job End.
2019-08-23 18:26:47,099 jobs[daka] INFO: Job Start: 京东会员页签到领京豆
2019-08-23 18:26:47,406 jobs[daka] INFO: 登录状态: False
2019-08-23 18:26:47,406 jobs[daka] INFO: 进行登录...
[30443:24579:0823/182649.631287:ERROR:adm_helpers.cc(62)] Failed to query stereo recording.
2019-08-23 18:26:50.181 QtWebEngineProcess[30443:3864402] Couldn't set selectedTextColor from default ()
[30442:45059:0823/182650.266490:ERROR:service_manager.cc(156)] Connection InterfaceProviderSpec prevented service: content_renderer from binding interface: blink::mojom::BudgetService exposed by: content_browser
[30443:775:0823/182650.309632:ERROR:BudgetService.cpp(167)] Unable to connect to the Mojo BudgetService.
[30442:45059:0823/182654.146448:ERROR:service_manager.cc(156)] Connection InterfaceProviderSpec prevented service: content_renderer from binding interface: blink::mojom::BudgetService exposed by: content_browser
[30443:775:0823/182654.150090:ERROR:BudgetService.cpp(167)] Unable to connect to the Mojo BudgetService.
2019-08-23 18:26:56,301 jobs[daka] INFO: 登录成功
2019-08-23 18:26:56,573 jobs[bean] INFO: 今日已签到: False; 现在有 2038 个京豆.
2019-08-23 18:26:56,710 jobs[bean] INFO: 已领取 1 京豆，请明日再来
2019-08-23 18:26:56,711 jobs[daka] INFO: Job End.
2019-08-23 18:26:56,711 jobs[daka] INFO: Job Start: 京东金融签到领奖励
2019-08-23 18:26:56,972 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:57,176 jobs[sign_jr] INFO: 今日已签到: True; 签到天数: 5; 现有钢镚: 3.55
2019-08-23 18:26:57,176 jobs[daka] INFO: Job End.
2019-08-23 18:26:57,176 jobs[daka] INFO: Job Start: 京东小金库现金红包
2019-08-23 18:26:57,235 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:57,287 jobs[red_packet] ERROR: 领取失败: None
2019-08-23 18:26:57,287 jobs[daka] INFO: Job End.
2019-08-23 18:26:57,287 jobs[daka] INFO: Job Start: 京东金融翻牌
2019-08-23 18:26:57,365 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:57,366 jobs[jr_fanpai] INFO: 今日已翻牌: True
2019-08-23 18:26:57,366 jobs[daka] INFO: Job End.
2019-08-23 18:26:57,366 jobs[daka] INFO: Job Start: 双签赢奖励
2019-08-23 18:26:57,528 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:57,585 jobs[double_sign] INFO: 今日已双签: False
2019-08-23 18:26:57,856 jobs[double_sign] INFO: 双签成功: True; Message:
2019-08-23 18:26:57,856 jobs[daka] INFO: Job End.
2019-08-23 18:26:57,856 jobs[daka] INFO: Job Start: 京东会员领京豆(摇一摇)
2019-08-23 18:26:58,080 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:58,273 jobs[plusSign] INFO: 今日已京东会员领京豆(摇一摇): False
2019-08-23 18:26:58,345 jobs[plusSign] INFO: 京东会员领京豆(摇一摇), 无免费次数可用
2019-08-23 18:26:58,345 jobs[plusSign] INFO: 京东会员领京豆(摇一摇)成功: True; Message:
2019-08-23 18:26:58,345 jobs[daka] INFO: Job End.
2019-08-23 18:26:58,345 jobs[daka] INFO: Job Start: 京东支付返京豆
2019-08-23 18:26:58,523 jobs[daka] INFO: 登录状态: True
2019-08-23 18:26:58,653 jobs[payBack] INFO: 京东支付返京豆-没有可领取的京豆--视为已经领取完了
2019-08-23 18:26:58,653 jobs[daka] INFO: Job End.
=================================
= 任务数: 10; 失败数: 1
= 失败的任务: ['京东小金库现金红包']
=================================
```
