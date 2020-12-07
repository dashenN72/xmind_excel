# -*- coding: utf-8 -*-
# @Time    : 2020/2/3 23:54
# @Author  : dashenN72

from xmindparser import xmind_to_dict
from tools import xmind
from tools import excel
import config

FileName = '.\\input\\接口测试模板.xmind'
XmindContent = xmind_to_dict(FileName)[0]['topic']   # xmind内容
print("原始内容：\n" + str(XmindContent))

content_params_test, content_logic_test = xmind.MindCase().mind_case_param(XmindContent)
print("【参数校验case数】：%d\n 【mind内容转换成list】：%s\n 【逻辑校验case数】：%d\n 【mind内容转换成list】：%s\n"
      % (len(content_params_test), str(content_params_test), len(content_logic_test), str(content_logic_test)))

# excel名称即mind中0级名称，1级开始才是用例
# 写参数校验数据
with excel.ExcelWriter(XmindContent['title'] + '_参数校验.xlsx', config.module_excel_sheet1) as ew1:
    ew1.init_title()  # 创建excel表格sheet标题，从配置文件
    if ew1.write_rows(content_params_test):  # 将mind内容写入excel
        print("[INFO]测试用例写入Excel成功！")
    else:
        print("[INFO]测试用例写入Excel失败！")
# 写逻辑校验数据
with excel.ExcelWriter(XmindContent['title'] + '_逻辑校验.xlsx', config.module_excel_sheet2) as ew2:
    ew2.init_title()  # 创建excel表格sheet标题，从配置文件
    if ew2.write_rows(content_logic_test):  # 将mind内容写入excel
        print("[INFO]测试用例写入Excel成功！")
    else:
        print("[INFO]测试用例写入Excel失败！")
