# -*- coding: utf-8 -*-
# @Time    : 2020/2/6 23:45
# @Author  : dashenN72
"""
1.只支持值和优先级两种
2.每一条链路（场景）都应该有优先级，否则默认使用上一级的优先级；
"""
from copy import deepcopy
from itertools import product
import config
from copy import deepcopy


class MindCase(object):
    def __init__(self):
        self.result_xmind_case = []
        self.sub_xmind_case = ['']
        self.level = 0
        self.result_params_test = []  # 参数校验构造的所有请求数据
        self.result_logic_test = []  # 逻辑校验构造的所有请求数据
        self.id_case_param_test = 0  # 参数校验case起始编号
        self.id_case_logic_test = 0  # 逻辑校验case起始编号

    def have_next_sub_topic(self, param):
        """
        判断当前主体是否有子主题
        :param param: 主体json格式数据
        :return: 有 返回子主题，无，返回空
        """
        if 'topics' in param:  # 存在子主题
            return param['topics']
        else:
            return []

    def generate_case_free_combine(self, params):
        """
        通过给定的参数及其值的情况下，自动组合成请求参数
        :param params: 请求参数为字典，key是参数名，value是参数名对应值的可能情况组成的列表
        :return: 包含多个字典型请求参数组成的列表 [{'a': 1, 'b': 2},{'a': 'test', 'b': ''}]
        """
        params_request = params[0]  # 获取请求参数名组成的list
        temp_values_request = params[1]  # 获取请求参数值组成的list
        values_request = [list(value) for value in product(*temp_values_request)]  # 值的自由组合
        param_value_request = [dict(zip(params_request, value_request)) for value_request in values_request]
        return param_value_request

    def generate_case_one_change(self, params):
        """
        通过给定的参数及其值的情况下,只有一个参数值变化，其他参数值正确，组合成请求参数
        :param params:
        :return:
        """
        param_value_request_full = []
        copy_temp_values_request = deepcopy(params[1])  # 深度复制
        for i in range(len(copy_temp_values_request)):
            params_request = deepcopy(params[0])  # 获取请求参数名组成的list
            temp_values_request = deepcopy(params[1])  # 获取请求参数值组成的list
            value_change_list = temp_values_request[i][1:]  # 变化参数值组成的列表
            temp_values_request.remove(temp_values_request[i])  # 剩下的值组成的列表
            value_right_list = [[value_right[0]] for value_right in temp_values_request]  # 正确的参数值组成的列表
            value_right_list.append(value_change_list)
            values_request = [list(value) for value in product(*value_right_list)]  # 值的组合
            param = params_request[i]
            params_request.remove(param)
            params_request.append(param)
            param_value_request = [dict(zip(params_request, value_request)) for value_request in values_request]  # 参数和值组合
            param_value_request_full.extend(param_value_request)
        return param_value_request_full

    def mind_case_logic(self, value_xmind):
        """
        递归处理xmind解析后的数据生成以一条数据为一个case的列表,适用于接口测试中的逻辑校验
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
                    self.mind_case_logic(param)
            else:
                temp = deepcopy(self.sub_xmind_case)
                self.result_xmind_case.append(temp)
        elif isinstance(value_xmind, list):  # 入参是列表
            [param.setdefault('level', param.get('level', 0)+1) for param in value_xmind]  # 增加层级键值对
            for param in value_xmind:
                self.mind_case_logic(param)
        return self.result_xmind_case

    def mind_case(self, value_xmind):
        """
        解析指定格式的xmind，得到参数校验和逻辑校验数据(包含预期结果)
        :param value_xmind: xmind解析后的数据
        :return: list形式的数据
        """

        title = value_xmind['title']  # xmind标题
        topics = value_xmind['topics']  # 接口所有参数组成的list
        data_param_verify = {'name': title, 'data': []}
        for topic in topics:
            params_value = {}
            name = topic['title']  # 接口名称
            url = topic['topics'][0]['title']  # 接口请求地址
            method = topic['topics'][1]['title']  # 接口请求方法
            type_verify = topic['topics'][2]['title']  # 接口校验方法
            if type_verify == '参数校验':
                for value_topic in topic['topics'][2]['topics']:
                    name_param = value_topic['title']  # 接口参数名
                    value_param = [[value['title'], [value['title'] for value in value.get('topics', [{'title': []}])]] for value in value_topic['topics']]  # 参数组合
                    params_value[name_param] = value_param
                sub_data_param_verify = {'name': name, 'url': url, 'method': method, 'status': 1, 'params_value': params_value}
                data_param_verify['data'].append(sub_data_param_verify)
            elif type_verify == '逻辑校验':
                pass
        return data_param_verify

    def mind_case_param(self, value_xmind):
        """
        将title与topics组成参数及其值的组合形式
        :return:
        """
        title = value_xmind['title']  # xmind标题
        topics = value_xmind['topics']  # 接口所有参数组成的list
        # 参数校验中参数名及其值的组合，序列0中存储的是参数名，序列1中存储的是参数名的值组成的list在组成的list
        for topic in topics:
            data_param_verify = [[], []]
            name = topic['title']  # 接口名称
            url = topic['topics'][0]['title']  # 接口请求地址
            method = topic['topics'][1]['title']  # 接口请求方法
            for type_params in topic['topics'][2:]:
                type_verify = type_params['title']  # 接口校验方法
                if type_verify == '参数校验':
                    for value_topic in type_params['topics']:
                        for value_case in value_topic['topics']:
                            name_param = value_case['title']  # 接口参数名
                            value_param = [topic['title'] for topic in value_case['topics']]  # 参数可能值组成的list
                            data_param_verify[0].append(name_param)
                            data_param_verify[1].append(value_param)
                    result_param_combine = self.generate_case_one_change((data_param_verify[0], data_param_verify[1]))
                    result_param_combine.pop(0)  # 将第一个全部正确的入参输入，此校验在逻辑校验中
                    for param in result_param_combine:
                        self.id_case_param_test += 1
                        self.result_params_test.append([self.id_case_param_test, name, method, config.host_interface+url, param])
                elif type_verify == '逻辑校验':
                    for value_topic in type_params['topics']:
                        for value_case in value_topic['topics']:
                            desc_logic = value_case['title']  # 逻辑场景描述
                            priority = value_case['makers'][0].split('-')[1] if 'makers' in value_case else 5  # 场景优先级
                            pre_condition = value_case['note'] if 'note' in value_case else ''  # 场景前置条件
                            checklist_logic = [topic['title'] for topic in value_case['topics']]  # 逻辑校验检查点
                            for check_point in checklist_logic:
                                self.id_case_logic_test += 1
                                self.result_logic_test.append([self.id_case_logic_test, priority, name, desc_logic,
                                                               pre_condition, method, config.host_interface+url, '',
                                                               check_point])
                else:
                    print('[ERROR]校验类型不在"参数校验和逻辑校验之间"')
        return self.result_params_test, self.result_logic_test


if __name__ == "__main__":
    xc = MindCase()
    value = [['name', 'type', 'status'], [['正确name', '123', '"test"', 'NULL'], ['正确type', '1'], ['正确status', '1', '0']]]
    print(xc.generate_case_one_change(value))


