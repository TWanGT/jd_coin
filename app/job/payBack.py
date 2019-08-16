import traceback

from .common import RequestError
from .daka import Daka
from .jd_util import jdUtil

class payBack(Daka):
    job_name = '京东支付返京豆'

    index_url = 'https://m.jr.jd.com/vip/activity/newperback/index.html?source=ymgc'
    sign_url = 'https://ms.jr.jd.com/gw/generic/jrm/h5/m/acquireJingdou?_='
    test_url = 'https://ms.jr.jd.com/gw/generic/jrm/h5/m/getjingdouRecodeEquityCenter?_='
    # 返回数据格式:
    # {
    #     "resultCode": 0,
    #     "resultMsg": "操作成功",
    #     "resultData": {
    #         "ableDrawCount": 3,
    #         "unsumInsured": 0,
    #         "jingdouRecordCount": 358,
    #         "sumInsured": 2978,
    #         "code": 0,
    #         "balance": 41450.0
    #     },
    #     "channelEncrypt": 0
    # }

    def is_signed(self):
        signed = False

        try:
            json = jdUtil.toJson(self, self.page_data())
            resultData = json.get('resultData')
            if resultData != None:
                ableDrawCount = resultData.get('ableDrawCount')
                if ableDrawCount != None and ableDrawCount > 0:
                    self.logger.info("有 {} 个京豆可以领取".format(str(ableDrawCount)))
                else:
                    self.logger.info("{}-没有可领取的京豆--视为已经领取完了".format(self.job_name))
                    signed = True;
            else:
                resultCode = json.get('resultCode')
                resultMsg = json.get('resultMsg')
                self.logger.info('{}-返回中没有resultData--resultData:{} resultMsg:{}'.format(self.job_name, resultCode, resultMsg))
                signed = True;
        except Exception as e:
            self.logger.error('返回数据结构可能有变化, {} 失败: {}'.format(self.job_name, e))
            traceback.print_exc()

        return signed

    def sign(self):
        sign_success = True
        try:
            msg = self.do_sign()
        except RequestError as e:
            self.logger.error('{}失败: {}'.format(self.job_name, e.message))
            return False

        self.logger.info('{}成功: {}; Message: {}'.format(self.job_name, sign_success, msg))
        return sign_success

    def do_sign(self):
        r = self.session.get((self.sign_url+str(jdUtil.timeStamp(self))))

        try:
            as_json = r.json()
        except ValueError:
            raise RequestError('unexpected response: url: {}; http code: {}'.format(self.sign_url, r.status_code), response=r)

        resultCode = as_json.get('resultCode')
        resultMsg = as_json.get('resultMsg')
        resultData = as_json.get('resultData')
        message = resultData.get('message')
        currentjingdoucount = resultData.get('currentjingdoucount')
        code = resultData.get('code')

        if currentjingdoucount != None:
            self.logger.info("{}-{} 个京豆, {}".format(self.job_name, currentjingdoucount, message))
        elif code != 1:
            self.logger.info("{}-code:{}, message:{}".format(self.job_name, code, message))
        else:
            raise RequestError(resultMsg, resultCode)

        return message;

    def page_data(self):
        if not hasattr(self, '_page_data'):
            self._page_data = self.session.get(self.test_url + str(jdUtil.timeStamp(self))).text

        return self._page_data

