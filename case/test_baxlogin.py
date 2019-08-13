# coding=utf-8 
"""
@Time    : 2019/05/25  上午 12:50
@Author  : hzsyy
@FileName: test_创建项目配置.py
@IDE     : PyCharm
"""
import os

from  ddt import  ddt,unpack,data

import unittest
import json
import requests
from common import readConfig
from common.operToken import read_token
from common.readYaml import operYaml
from getRootPath import root_dir
from common.logger import Log


@ddt
class test_baxlogin(unittest.TestCase):
    yaml_path = os.path.join(root_dir, "caseyaml", "baxlogin.yaml")
    oper_yaml = operYaml(yaml_path)
    case_list = oper_yaml.caseList()
    case_list1=[{'登录普通用户': {'data': {'user_id': 303}, 'assert': 'Success'}}, {'登录运营用户': {'data': {'user_id': 1}, 'assert': 'Success'}}, {'登录用户2': {'data': {'user_id': 252}, 'assert': 'Success'}}]

    # 跳过说明
    #reason = readConfig.skip_reason

    @classmethod
    def setUpClass(cls):

        # log 实例化
        cls.log = Log()

        cls.url = readConfig.hostName + "/bax/user/login/local"
        #cls.headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": read_token()["assertToken"]}

    # case_list传进去做数据驱动
    @data(*case_list1)
    def test_baxlogin(self, cases):

        for caseName, caseInfo in cases.items():
            caseName = caseName
            caseData = caseInfo["data"]
            check = caseInfo["assert"]
            self.__dict__['_testMethodDoc'] = caseName

        config_dict = {"projectName": readConfig.projectName}
        data = caseData
        # 发送请求
        response = requests.get(self.url,params=data)
        text = response.text  # 接口返回信息

        self.log.info("#" * 100 + "开始测试" + "#" * 100)
        self.log.info("用例名字：{}".format(caseName))
        self.log.info("请求参数：{}".format(data))
        self.log.info("-" * 200)
        self.log.info("期望结果：{}, 实际结果：{}".format(check, text))
        self.log.info("#" * 100 + "测试结束" + "#" * 100)

        # 断言
        self.assertIn(check, text)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()


