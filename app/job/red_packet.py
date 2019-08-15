from .daka import Daka


class RedPacket(Daka):
    job_name = '京东小金库现金红包'

    # index_url = 'https://m.jr.jd.com/udc-active/2017/618RedPacket/html/index.html'
    # sign_url = 'https://ms.jr.jd.com/gw/generic/activity/h5/m/receiveZhiBoXjkRedPacket'
    # test_url = 'https://home.m.jd.com'
    index_url = 'https://vip.m.jd.com/newPage/reward/a'
    sign_url = 'https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_shaking'
    # sign_url = 'https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_shaking&body=%7B%22type%22%3A%220%22%2C%22riskInfo%22%3A%7B%22platform%22%3A5%2C%22pageClickKey%22%3A%22MJDVip_Shake%22%2C%22eid%22%3A%22CUOXWN4AE33WZ7BA7BS5JGF6V3HX2MRWQVGEDEFFNM2M7ZL3POLERUY2VIEDSLSISDM6ORKEWJ2A7ZEVVOOXB6ISWU%22%2C%22fp%22%3A%2266ce4f72c4e55e6b4a220cb6844cd593%22%2C%22shshshfp%22%3A%228c3b19e7f6dc6ecb82b14c490234a95e%22%2C%22shshshfpa%22%3A%22be78a65a-1d1b-e9a7-cd39-afee9767c421-1560600395%22%2C%22shshshfpb%22%3A%22zA3ASmGWYqBUgXFj8LUQI9g%3D%3D%22%7D%7D&_=1564741272432&jsonp=__jp4'
    test_url = 'https://home.m.jd.com'

    def is_signed(self):
        # 这个任务在领取前不能知道今天是否领取过, 因此返回 None 以便任务能够执行.
        return None

    def sign(self):
        # 参见 red_packet_index.js

        payload = {}
        # payload = {
        #     'reqData': '{"activityCode":"ying_yong_bao_618"}',
        #     'sid': self.session.cookies.get('sid')
        # }

        response = self.session.post(self.sign_url, data=payload).json()

        if response['resultCode'] == 0:
            sign_success = response['resultData']['success']

            if sign_success:
                self.logger.info('领取成功, 获得 {} 元.'.format(response['resultData']['data']))

            else:
                message = response['resultData'].get('msg') or response.get('resultMsg')
                self.logger.info('领取结果: {}'.format(message))

                if response['resultData'].get('code') == '03':
                    # 当 code 为 03 时, 表示今天已领过了, 因为领取前无法知道是否领过, 此处也当做任务成功返回
                    sign_success = True

            return sign_success

        else:
            message = response.get('resultMsg')
            self.logger.error('领取失败: {}'.format(message))
            return False
