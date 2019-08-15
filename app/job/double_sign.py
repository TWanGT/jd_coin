import traceback

from pyquery import PyQuery

from .common import RequestError
from .daka import Daka
import time
import datetime

class DoubleSign(Daka):
    job_name = '双签赢奖励'

    index_url = 'https://m.jr.jd.com/integrate/signin/index.html'
    # index_url = 'https://ljd.m.jd.com/countersign/index.action'
    # sign_url = 'https://ljd.m.jd.com/countersign/receiveAward.json'
    sign_url = 'https://nu.jr.jd.com/gw/generic/jrm/h5/m/process?_='
    test_url = index_url

    def is_signed(self):
        signed = False

        try:
            signed = PyQuery(self.page_data())('#awardFlag').val() == '2'
            self.logger.info('今日已双签: {}'.format(signed))

        except Exception as e:
            self.logger.error('返回数据结构可能有变化, 获取双签数据失败: {}'.format(e))
            traceback.print_exc()

        return signed

    def sign(self):
        # 参见 https://ljd.m.jd.com/js/countersign/countersign.js

        sign_success = True
        message = ''

        document = PyQuery(self.page_data())

        # TODO 这个双签到目前坏了, 把判断暂时屏蔽了
        # jd_signed = document('#jd-sign-done').val() == 'true'
        # jr_signed = document('#jr-sign-done').val() == 'true'
        jd_signed = 'true';
        jr_signed = 'true';

        if not (jd_signed and jr_signed):
            sign_success = False
            message = '完成双签才可领取礼包'

        else:
            try:
                res = self.do_sign()
            except RequestError as e:
                self.logger.error('双签失败: {}'.format(e.message))
                return False

            if res['code'] == '0':
                award_data = res.get('data')

                if not award_data:
                    message = '运气不佳，领到一个空空的礼包'

                else:
                    award = award_data[0]
                    sign_success = True
                    message = '领到 {} 个{}'.format(award['awardCount'], award['awardName'])

            else:
                # 活动不定时开启，将活动时间未开始/已结束等情况都视作签到成功

                if res['code'] == 'DS102':
                    message = '来早了，活动还未开始'
                elif res['code'] == 'DS103':
                    message = '来晚了，活动已经结束了'
                elif res['code'] == 'DS104':
                    message = '运气不佳，领到一个空空的礼包'
                elif res['code'] == 'DS106':
                    sign_success = False
                    message = '完成双签才可领取礼包'
                else:
                    sign_success = False
                    message = '未知错误，Code={}'.format(res['code'])

        self.logger.info('双签成功: {}; Message: {}'.format(sign_success, message))

        return sign_success

    def do_sign(self):
        payload = {
            'reqData': '{ "actCode": "FBBFEC496C", "type": "3"}',
        }
            # 'sid': self.session.cookies.get('sid'),
            # 'source': 'jrm'

        t = time.time()
        timestamp = int(round(t * 1000))
        r = self.session.post((self.sign_url+str(timestamp)), data=payload)

        try:
            as_json = r.json()
        except ValueError:
            raise RequestError('unexpected response: url: {}; http code: {}'.format(self.sign_url, r.status_code), response=r)

        if 'resultCode' in as_json and 'resultData' in as_json:
            # 请求成功
            msg = as_json.get('resultData').get('data').get('businessData').get('businessMsg') or as_json.get(
                'resultMsg') or str(as_json)
            code = as_json.get('resultData').get('data').get('businessCode') or as_json.get('resultCode')
            raise RequestError(msg, code)

        else:
            error_msg = as_json.get('message') or str(as_json)
            error_code = as_json.get('businessCode') or as_json.get('code')
            raise RequestError(error_msg, error_code)

    def page_data(self):
        if not hasattr(self, '_page_data'):
            self._page_data = self.session.get(self.index_url+"?sid="+self.session.cookies.get('sid')).text

        return self._page_data
