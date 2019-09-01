import traceback

from .common import RequestError
from .daka import Daka

class plantTree(Daka):
    job_name = '种豆得豆'

    index_url = 'https://m.jr.jd.com/vip/activity/newperback/index.html?source=ymgc'
    water_url = 'https://api.m.jd.com/client.action?functionId=plantBeanIndex'
    sign_url = 'https://api.m.jd.com/client.action?functionId=cultureBean'

    def is_signed(self):
        signed = False

        # try:
        #     json = jdUtil.toJson(self, self.page_data())
        #     resultData = json.get('resultData')
        #     if resultData != None:
        #         ableDrawCount = resultData.get('ableDrawCount')
        #         if ableDrawCount != None and ableDrawCount > 0:
        #             self.logger.info("有 {} 个京豆可以领取".format(str(ableDrawCount)))
        #         else:
        #             self.logger.info("{}-没有可领取的京豆--视为已经领取完了".format(self.job_name))
        #             signed = True;
        #     else:
        #         resultCode = json.get('resultCode')
        #         resultMsg = json.get('resultMsg')
        #         self.logger.info('{}-返回中没有resultData--resultData:{} resultMsg:{}'.format(self.job_name, resultCode, resultMsg))
        #         signed = True;
        # except Exception as e:
        #     self.logger.error('返回数据结构可能有变化, {} 失败: {}'.format(self.job_name, e))
        #     traceback.print_exc()

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

        payload = {"roundId": "qde6xhb53gt44oqbns6eertieu", "monitor_source": "plant_app_plant_index",
         "monitor_refer": "plant_index"}
        r = self.session.post((self.sign_url), data=payload)

        # 返回格式:
        # {
        #     "code": "0",
        #     "data": {
        #         "growth": "18",
        #         "nutrients": "0",
        #         "beanState": "2"
        #     }
        # }
        try:
            as_json = r.json()
        except ValueError:
            raise RequestError('unexpected response: url: {}; http code: {}'.format(self.sign_url, r.status_code), response=r)

        code = as_json.get('code')
        growth = as_json.get('data').get('growth')

        if code == '0':
            self.logger.info("{}-当前种豆进度 {}".format(self.job_name, growth))
        else:
            raise RequestError(as_json, -1)

        return '种豆得豆完毕';

    def page_data(self):
        # 需要先领取营养液
        if not hasattr(self, '_page_data'):
            payload =  {"shareUuid": "", "monitor_refer": "", "wxHeadImgUrl": "", "followType": "1",
         "monitor_source": "plant_app_plant_index"}
            r = self.session.post((self.water_url), data=payload)
        return self._page_data

