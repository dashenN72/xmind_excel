# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 23:00
# @Author  : dashenN72
# (xmind节点对应excel的列名, 是否合并(1-合并，0-不合并))
# module_excel = [('用例名称', 0), ('优先级', 0), ('功能点', 1), ('测试类型', 1), ('测试用例', 0), ('预期结果', 0), ('实际结果', 0), ('用例结果', 0)]
module_excel_sheet1 = [('参数校验', 0), ('用例编号', 0), ('接口名称', 0), ('请求方法', 0), ('请求地址', 0), ('请求参数', 0), ('预期结果', 0), ('实际结果', 0), ('测试结果', 0), ('状态', 0)]
module_excel_sheet2 = [('逻辑校验', 0), ('用例编号', 0), ('优先级', 0), ('接口名称', 0), ('场景描述', 0), ('前置条件', 0), ('请求方法', 0), ('请求地址', 0), ('请求参数', 0), ('预期结果', 0), ('实际结果', 0), ('测试结果', 0), ('状态', 0)]
# 参数校验的规则
mind_case_regular = ['name_mind', 'name_interface', 'type_check', 'name_param', 'value_param', 'result_test']
# 接口域名
host_interface = 'http://101.91.227.223:8100'
# 存储xmind转excel的中转文件
file1 = './output/temp_interface_params.txt'
file2 = './output/temp_interface_logic.txt'