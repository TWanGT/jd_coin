import argparse
import json
import logging
import sys
from base64 import b85decode
from pathlib import Path

log_format = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)


class Config:
    def __init__(self):
        self.debug = False
        self.log_format = log_format
        self.ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0'
        # self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/application=JDJR-App&deviceId=01865C86-9AB1-4F17-8FF6-8BD111E9036D&clientType=ios&iosType=iphone&clientVersion=5.2.32&HiClVersion=5.2.32&isUpdate=0&osVersion=12.4&osName=iOS&platform=iPhone 7 Plus (A1661/A1785/A1786)&screen=736*414&src=App Store&ip=2409:8954:3060:18b8:1c91:bd12:7cc3:351d&mac=02:00:00:00:00:00&netWork=1&netWorkType=1&stockSDK=stocksdk-iphone_3.0.0&sPoint=MTUwMDMjIzcxOTUzX3sicG9zaWQiOiIqMTMwNzYqMjM5MzgiLCJzeXNDb2RlIjoibWMtbWt0LWNtcyIsIm1hdGlkIjoiMzAy5qih5p2%2FKuavj%2BaXpeetvuWIsOmihuemj%2BWIqSoiLCJwYWdpZCI6IjEiLCJvcmRpZCI6IiozKjAtdG9wUmVnaW9uIn0%3D&jdPay=(*#@jdPaySDK*#@jdPayChannel=jdfinance&jdPayChannelVersion=5.2.32&jdPaySdkVersion=2.23.3.0&jdPayClientName=iOS*#@jdPaySDK*#@)',
        self.jd = {
            'username': '',
            'password': ''
        }

        self.jobs_skip = []

    @classmethod
    def load(cls, d):
        the_config = Config()

        the_config.debug = d.get('debug', False)

        try:
            the_config.jd = {
                'username': b85decode(d['jd']['username']).decode(),
                'password': b85decode(d['jd']['password']).decode()
            }
        except Exception as e:
            logging.error('获取京东帐号出错: ' + repr(e))

        if not (the_config.jd['username'] and the_config.jd['password']):
            # 有些页面操作还是有用的, 比如移动焦点到输入框... 滚动页面到登录表单位置等
            # 所以不禁止 browser 的 auto_login 动作了, 但两项都有才自动提交, 否则只进行自动填充动作
            the_config.jd['auto_submit'] = 0  # used in js
            logging.info('用户名/密码未找到, 自动登录功能将不可用.')

        else:
            the_config.jd['auto_submit'] = 1

        the_config.jobs_skip = d.get('jobs_skip', [])

        return the_config


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name')
    args = parser.parse_args()

    config_name = args.config or 'config.json'
    logging.info('使用配置文件 "{}".'.format(config_name))

    config_file = Path(__file__).parent.joinpath('../conf/', config_name)

    if not config_file.exists():
        config_name = 'config.default.json'
        logging.warning('配置文件不存在, 使用默认配置文件 "{}".'.format(config_name))
        config_file = config_file.parent.joinpath(config_name)

    try:
        # 略坑, Path.resolve() 在 3.5 和 3.6 上表现不一致... 若文件不存在 3.5 直接抛异常, 而 3.6
        # 只有 Path.resolve(strict=True) 才抛, 但 strict 默认为 False.
        # 感觉 3.6 的更合理些...
        config_file = config_file.resolve()
        config_dict = json.loads(config_file.read_text())
    except Exception as e:
        sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    the_config = Config.load(config_dict)

    return the_config


config = load_config()
