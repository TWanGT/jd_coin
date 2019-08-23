import traceback

from .daka import Daka


class fanpai(Daka):
    job_name = '京东金融翻牌'

    index_url = 'https://m.jr.jd.com/spe/qyy/main/index.html?userType=41'
    sign_url = 'https://gpm.jd.com/signin_new/choice?sid=fa7fb27bbce3960532d3821a9765f61w&uaType=2&position=2&_=1564739714208&callback=Zepto1564739633694'
    test_url = 'https://ms.jr.jd.com/gw/generic/base/h5/m/baseGetMessByGroupType'

    # https://ms.jr.jd.com/jrmserver/base/user/getNewTokenJumpUrl?accessKey=33fd5ddc-a586-47cb-aa2d-1e6b5de2a946&pin=amRfNDMyMDMyMmE1MDRhNQ%3D%3D&deviceId=01865C86-9AB1-4F17-8FF6-8BD111E9036D&clientType=ios&targetUrl=aHR0cHM6Ly9zdG9jay1zci5qZC5jb20vaDUvamQtZmxpcERyYXcvaHRtbC9pbmRleC5odG1sP211c3RMb2dpbj0x&a2=AAFc6BSvAEB36YAyvw-7aweVDP6Z9z_ivXLJ4NxfUf4GsKarMBdjKED4l4l-s0xrlXwSKjKzCFXdZZtm1A2EpupJulg19zX4&sign=505c50adb662a2b5f27a82ea8217cad0
    def __init__(self, session):
        super().__init__(session)
        self.sign_data = {}

    def get_sign_data(self):
        payload = {
            'reqData': '{"clientType":"outH5","userType":41,"groupType":154}',
            'sid': self.session.cookies.get('sid'),
            'source': 'jrm'
        }

        sign_data = {}

        try:
            r = self.session.post(self.test_url, data=payload)
            as_json = r.json()

            if 'resultData' in as_json:
                sign_data = r.json()['resultData']['53']

            else:
                error_msg = as_json.get('resultMsg') or as_json.get('resultMessage')
                self.logger.error('获取翻牌数据失败: {}'.format(error_msg))

        except Exception as e:
            self.logger.error('获取翻牌数据失败: {}'.format(e))

        return sign_data

    def is_login(self):
        sign_data = self.get_sign_data()

        # 参见 daka_app_min.js, 第 1835 行
        is_login = 'suitable' in sign_data

        if is_login:
            # 用户已登录, sign_data 有效, 存储下
            self.sign_data = sign_data

        return is_login

    def is_signed(self):
        sign_data = self.sign_data or self.get_sign_data()

        signed = False

        try:
            signed = sign_data['signInStatus'] == 1
            self.logger.info('今日已翻牌: {}'.format(signed))

        except Exception as e:
            self.logger.error('返回数据结构可能有变化, 获取发翻牌数据失败: {}'.format(e))
            traceback.print_exc()

        return signed

    def sign(self):
        payload = {
            'reqData': '{}',
            'sid': self.session.cookies.get('sid'),
            'source': 'gpm'

        }
        # 'source': 'jrm'
        r = self.session.post(self.sign_url, data=payload)
        as_json = r.json()

        if 'resultData' in as_json:
            result_data = as_json['resultData']
            # statusCode 14 似乎是表示延期到帐的意思, 如: 签到成功，钢镚将于15个工作日内发放到账
            sign_success = result_data['isSuccess'] or result_data['statusCode'] == 14
            message = result_data['showMsg']

            # 参见 daka_app_min.js, 第 1893 行
            continuity_days = result_data['continuityDays']

            if continuity_days > 1:
                message += '; 签到天数: {}'.format(continuity_days)

        else:
            sign_success = False
            message = as_json.get('resultMsg') or as_json.get('resultMessage')

        self.logger.info('打卡成功: {}; Message: {}'.format(sign_success, message))

        return sign_success
