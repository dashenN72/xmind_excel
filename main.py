# -*- coding: utf-8 -*-
# @Time    : 2020/2/3 23:54
# @Author  : dashenN72

from xmindparser import xmind_to_dict
from xmind2excel.tools import xmind
from xmind2excel.tools import excel
from xmind2excel import config

FileName = '.\\input\\app测试用例.xmind'
XmindContent = xmind_to_dict(FileName)[0]['topic']   # xmind内容
print("原始心得内容：\n" + str(XmindContent))

list_xmind_content = xmind.XmindCase().xmind_case(XmindContent['topics'])
print("case数：%d \n"
      "xmind内容转换成list：%s\n" % (len(list_xmind_content), str(list_xmind_content)))

# excel名称即xmind中0级名称，1级开始才是用例
with excel.ExcelWriter(XmindContent['title'] + '.xlsx', config.module_excel[0][0]) as ew:
    ew.init_title()  # 创建excel表格sheet标题，从配置文件
    ew.write_rows(list_xmind_content)  # 将xmind内容写入excel


