# -*- coding: utf-8 -*-
# @Time    : 2020/2/6 23:45
# @Author  : dashenN72
"""
1.只支持值和优先级两种
2.每一条链路（场景）都应该有优先级，否则默认使用上一级的优先级；
"""
from copy import deepcopy


class XmindCase(object):
    def __init__(self):
        self.result_xmind_case = []
        self.sub_xmind_case = ['']
        self.level = 0

    def xmind_case(self, value_xmind):
        """
        递归处理xmind解析后的数据生成以一条数据为一个case的列表
        :param value_xmind: xmind解析后的数据
        :return: list形式的数据
        """
        if isinstance(value_xmind, dict):  # 入参是字典
            if int(value_xmind['level']) >= len(self.sub_xmind_case):
                pass
            elif int(value_xmind['level']) < len(self.sub_xmind_case):
                num_pop = len(self.sub_xmind_case) - int(value_xmind['level'])
                for num in range(num_pop):
                    self.sub_xmind_case.pop()
            else:
                print("未知的异常！")
            value_priority = value_xmind.get('makers', ['-'])[0].split('-')[1]
            if value_priority:
                self.sub_xmind_case[0] = value_priority
            else:
                pass
            self.sub_xmind_case.append(value_xmind.get('title', ''))
            if isinstance(value_xmind.get('topics', ''), list):
                # 增加层级键值对
                [param.setdefault('level', value_xmind.get('level', '')+1) for param in value_xmind['topics']]
                for param in value_xmind['topics']:
                    self.xmind_case(param)
            else:
                temp = deepcopy(self.sub_xmind_case)
                self.result_xmind_case.append(temp)
        elif isinstance(value_xmind, list):  # 入参是列表
            [param.setdefault('level', param.get('level', 0)+1) for param in value_xmind]  # 增加层级键值对
            for param in value_xmind:
                self.xmind_case(param)
        return self.result_xmind_case


if __name__ == "__main__":
    xc = XmindCase()
    value = {'topics': [{'topics': [{'topics': [{'makers': ['priority-1', 'task-start', 'smiley-smile'], 'topics': [{'title': '注册成功'}, {'title': '提示语友好'}], 'title': '合规的用户名+密码'}, {'makers': ['priority-2'], 'topics': [{'note': '这是一个备注', 'title': '注册失败'}], 'title': '已存在的用户名'}, {'makers': ['priority-3'], 'topics': [{'title': '注册失败'}], 'title': '不合法的用户名'}, {'makers': ['priority-4'], 'topics': [{'title': '注册失败'}, {'title': '密码错误'}], 'title': '不合法的密码'}], 'title': '功能测试'}, {'topics': [{'makers': ['priority-1'], 'title': '界面满足要求'}], 'title': 'UI测试'}, {'topics': [{'topics': [{'makers': ['priority-1'], 'title': 'cpu'}, {'makers': ['priority-1'], 'title': 'mem'}], 'title': 'pftest'}], 'title': '性能测试'}], 'title': '注册'}, {'topics': [{'makers': ['priority-3'], 'topics': [{'title': '符合设计'}], 'title': '界面测试'}, {'makers': ['priority-1'], 'title': '响应时间'}], 'title': '登录'}, {'topics': [{'makers': ['priority-1'], 'topics': [{'title': '提示正常'}], 'title': '有效期内验证码'}, {'makers': ['priority-2'], 'topics': [{'title': '提示错误'}], 'title': '过期验证码'}], 'title': '验证码'}], 'title': 'app测试用例'}
    print(xc.xmind_case(value['topics']))


