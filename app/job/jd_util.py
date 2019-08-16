import time
import json

class jdUtil:

    def formatResponseContent(self, str):
        s_from = str.find('(')
        e_from = str.find(')')
        jsonStr = str[s_from + 1: e_from]
        as_json = json.loads(jsonStr)
        return as_json

    def timeStamp(self):
        t = time.time()
        return int(round(t * 1000))

    def toJson(self, str) -> json:
        return json.loads(str)