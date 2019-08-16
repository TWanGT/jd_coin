import traceback
import json
from pyquery import PyQuery

from .common import RequestError
from .daka import Daka
import time
import datetime

class plusSign(Daka):
    job_name = '京东会员领京豆(摇一摇)'

    index_url = 'https://vip.m.jd.com/newPage/reward/a'
    sign_url = 'https://api.m.jd.com/client.action?appid=vip_h5&functionId=vvipclub_shaking&body={"type":"0","riskInfo":{"platform":5,"pageClickKey":"MJDVip_Shake","eid":"CUOXWN4AE33WZ7BA7BS5JGF6V3HX2MRWQVGEDEFFNM2M7ZL3POLERUY2VIEDSLSISDM6ORKEWJ2A7ZEVVOOXB6ISWU","fp":"bb44dcae58f1b92c6a4e324def0af721","shshshfp":"ba68ce9a9f8976522dcbf23773f0bb5a","shshshfpa":"be78a65a-1d1b-e9a7-cd39-afee9767c421-1560600395","shshshfpb":"zA3ASmGWYqBUgXFj8LUQI9g=="}}&jsonp=__jp4&_='
    test_url = index_url

    def is_signed(self):
        signed = False

        try:
            signed = PyQuery(self.page_data())('#awardFlag').val() == '2'
            self.logger.info('今日已{}: {}'.format(self.job_name, signed))

        except Exception as e:
            self.logger.error('返回数据结构可能有变化, {}失败: {}'.format(self.job_name, e))
            traceback.print_exc()

        return signed

    def formatResponseContent(self, str):
        s_from = str.find('(')
        e_from = str.find(')')
        jsonStr = str[s_from + 1: e_from]
        as_json = json.loads(jsonStr)
        return as_json

    def sign(self):
        # 参见 https://ljd.m.jd.com/js/countersign/countersign.js

        sign_success = True
        message = ''

        res = self.do_sign()


        self.logger.info('{}成功: {}; Message: {}'.format(self.job_name, sign_success, message))

        return sign_success

    def do_sign(self):
        i = 3
        num=0
        while(i>0):
            i = i - 1
            t = time.time()
            timestamp = int(round(t * 1000))
            r = self.session.get((self.sign_url+str(timestamp)))
            try:
                as_json = self.formatResponseContent(r.text);
            except ValueError:
                raise RequestError('unexpected response: url: {}; http code: {}'.format(self.sign_url, r.status_code), response=r)


            if 'resultCode' in as_json and as_json.get('resultCode') == '8000005':
                self.logger.info("{}, {}".format(self.job_name, as_json.get('resultTips')))
                break;

                json_data = as_json.get('data')
            if 'data' in as_json and 'luckyBox' in json_data:
                num = num + 1
                # 请求成功
                i = as_json.get('data').get('luckyBox').get('freeTimes')

                if 'prizeBean' in json_data:
                    jd_count=json_data.get('prizeBean').get('count')
                    self.logger('成功获取京豆{}个'.format(jd_count))
                else:
                    prizeCoupon=json_data.get('prizeCoupon')
                    endTime=prizeCoupon.get('endTime')
                    quota=prizeCoupon.get('quota')
                    discount=prizeCoupon.get('discount')
                    limitStr=prizeCoupon.get('limitStr')
                    self.logger('领取到{}-{}的优惠券, 使用范围:{}, 截止日期:{}'.format(quota, discount, limitStr, endTime))

            if num > 0:
                msg = self.job_name + "成功"
                code = "success"
            else:
                msg = self.job_name + "失败"
                code = "fail"
            raise RequestError(msg, code)
    def page_data(self):
        if not hasattr(self, '_page_data'):
            self._page_data = self.session.get(self.index_url+"?sid="+self.session.cookies.get('sid')).text

        return self._page_data

